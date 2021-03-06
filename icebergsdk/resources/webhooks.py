# -*- coding: utf-8 -*-
import os
import time
from icebergsdk.resources.base import IcebergObject, UpdateableIcebergObject

if os.getenv('ICEBERG_DEBUG', False):
    MAX_NUMBER_OF_CHECKS = 2
    CHECK_EVERY_SECONDS = 5
else:
    MAX_NUMBER_OF_CHECKS = 10
    CHECK_EVERY_SECONDS = 1


class Webhook(UpdateableIcebergObject):
    endpoint = 'webhook'

    def test_trigger(self):
        data = self.request("%s%s/" % (self.resource_uri, 'test_trigger'), method = "post")
        return data

    def triggers(self, **filters):
        return self.get_list('%striggers/' % self.resource_uri, args=filters)


    def get_test_endpoint_url(self):
        return "%s/%s/" % ("/".join(self.resource_uri.split("/")[:-2]), 'test_endpoint')


    def wait_for_triggers(self, number_of_triggers_expected=1, max_number_of_checks=MAX_NUMBER_OF_CHECKS, check_every_seconds=CHECK_EVERY_SECONDS):
        webhook_triggers = []
        ## looping to wait for the webhook to be triggered
        number_of_attempts = 0
        while number_of_attempts<max_number_of_checks and len(webhook_triggers)<number_of_triggers_expected:
            if number_of_attempts > 0:
                time.sleep(check_every_seconds) ## check every X seconds except the 1st time
            webhook_triggers = self.triggers(status="succeeded")
            number_of_attempts += 1
        print "number_of_attempts = %s, %s webhook_triggers (expected %s)" % (number_of_attempts, len(webhook_triggers), number_of_triggers_expected)
        return webhook_triggers

class WebhookTrigger(IcebergObject):
    endpoint = 'webhook_trigger'
    raw_fields = ["payload"]

    def attempts(self, **filters):
        return self.get_list('%sattempts/' % self.resource_uri, args=filters)


class WebhookTriggerAttempt(IcebergObject):
    endpoint = 'webhook_trigger_attempt'
