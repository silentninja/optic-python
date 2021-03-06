import json
from unittest import TestLoader, mock
from unittest.mock import MagicMock

from django.test import TestCase
from django.test.runner import DiscoverRunner

from optic_django_middleware.apps import OpticDjangoAppConfig
from optic_django_middleware.middleware import OpticMiddleware


class TestMiddleWare(TestCase):
    def setUp(self):
        self.test_runner = DiscoverRunner()

    def test_middleware_called(self):
        with mock.patch(
            "optic_django_middleware.middleware.OpticMiddleware",
            new=MagicMock(wraps=OpticMiddleware),
        ) as mocked:
            self.client.get("/url-1")
            self.assertEqual(mocked.call_count, 1)

    def test_testcase_container_one_test(self):
        class Test(TestCase):
            def test_foo(self):
                self.client.get("/url-1")
                with open(OpticDjangoAppConfig.log_path(), "r+") as f:
                    log = json.load(f)
                    self.assertEqual(log[0]["url"]["path"], "/url-1")

        self.test_runner.run_suite(
            TestLoader().loadTestsFromTestCase(testCaseClass=Test)
        )
