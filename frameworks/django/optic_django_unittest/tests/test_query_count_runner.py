import json
import os
from io import StringIO
from os.path import exists
from unittest import TestLoader, TextTestRunner

from django.test import TestCase
from django.test.runner import DiscoverRunner

from optic_django_middleware.apps import OpticDjangoAppConfig
from optic_django_unittest.manager import HttpInteractionManager


class TestRunnerTest(TestCase):

    def setUp(self):
        class StringIOTextRunner(TextTestRunner):
            def __init__(self, *args, **kwargs):
                kwargs['stream'] = StringIO()
                super().__init__(*args, **kwargs)

        self.test_runner = DiscoverRunner()
        self.test_runner.test_runner = StringIOTextRunner

    def tearDown(self):
        try:
            os.remove(OpticDjangoAppConfig.log_path())
        except FileNotFoundError:
            pass

    @classmethod
    def get_id(cls, test_class, method_name):
        return "{}.{}.{}".format(test_class.__module__,
                                 test_class.__qualname__,
                                 method_name)

    def test_log_sent_on_teardown(self):
        class Test(TestCase):
            def test_foo(self):
                self.client.get('/url-1')
                self.client.get('/url-1')
                self.client.get('/url-2')
                self.client.get('/json-url-3')
            def test_foo1(self):
                self.client.get('/url-2')

        self.test_runner.setup_test_environment()
        self.test_runner.run_suite(
                TestLoader().loadTestsFromTestCase(testCaseClass=Test)
        )
        self.test_runner.teardown_test_environment()
        self.assertEqual(exists(OpticDjangoAppConfig.log_path()), True)
        with open(OpticDjangoAppConfig.log_path(), "r+") as f:
            log = json.load(f)
            self.assertEqual(len(log), 5)
            self.assertEqual(log[0]['url']['path'], "/url-1")
    def test_success_only_log_sent_on_teardown(self):
        class Test(TestCase):
            def test_foo(self):
                self.client.get('/url-1')
                self.client.get('/url-1')
                self.client.get('/url-2')
                self.client.get('/json-url-3')
                self.assertEqual(True, False)
            def test_foo1(self):
                self.client.get('/url-2')

        self.test_runner.setup_test_environment()
        self.test_runner.run_suite(
                TestLoader().loadTestsFromTestCase(testCaseClass=Test)
        )
        self.test_runner.teardown_test_environment()
        self.assertEqual(exists(OpticDjangoAppConfig.log_path()), True)
        with open(OpticDjangoAppConfig.log_path(), "r+") as f:
            log = json.load(f)
            self.assertEqual(len(log), 1)
            self.assertEqual(log[0]['url']['path'], "/url-2")

    def test_custom_setup_teardown(self):
        class Test(TestCase):
            def setUp(self):
                self.test_data = "Hello World"

            def tearDown(self):
                pass

            def test_foo(self):
                self.client.get('/url-1')
                self.assertEqual(self.test_data, "Hello World")

        self.test_runner.setup_test_environment()
        self.test_runner.run_suite(
                TestLoader().loadTestsFromTestCase(testCaseClass=Test)
        )
        self.assertIn(
                self.get_id(Test, 'test_foo'),
                HttpInteractionManager.test_result_container.interactions_by_testcase
        )
        self.assertEqual(
                len(HttpInteractionManager.test_result_container.interactions_by_testcase[
                        self.get_id(Test, 'test_foo')]['interaction'].http_interactions),
                1
        )
        self.test_runner.teardown_test_environment()

