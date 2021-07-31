# -*- coding: utf-8
import threading
from unittest import TestCase, TestResult

from django.conf import settings
from django.test import SimpleTestCase
from django.test.utils import get_runner
from optic_django_unittest.container import (
    TestCaseInteractionContainer,
    TestResultInteractionContainer,
)

from optic_django_middleware.apps import OpticDjangoAppConfig
from optic_django_middleware.manager import BasicOpticManager

local = threading.local()


class HttpInteractionManager(BasicOpticManager):
    LOCAL_TESTCASE_CONTAINER_NAME = "interaction_test_case_container"
    test_result_container: TestResultInteractionContainer = None

    @classmethod
    def get_interaction_container(cls) -> TestCaseInteractionContainer:
        return getattr(local, cls.LOCAL_TESTCASE_CONTAINER_NAME, None)

    @classmethod
    def set_interaction_container(cls, value):
        setattr(local, cls.LOCAL_TESTCASE_CONTAINER_NAME, value)

    @classmethod
    def wrap_pre_set_up(cls, set_up):
        def wrapped(self, *args, **kwargs):
            result = set_up(self, *args, **kwargs)
            if OpticDjangoAppConfig.enabled():
                cls.set_interaction_container(TestCaseInteractionContainer())
            return result

        return wrapped

    @classmethod
    def wrap_post_tear_down(cls, tear_down):
        def wrapped(self, *args, **kwargs):
            if (
                not hasattr(cls, "test_result_container")
                or not OpticDjangoAppConfig.enabled()
            ):
                return tear_down(self, *args, **kwargs)

            container = cls.get_interaction_container()
            if container is not None:
                all_interactions = cls.test_result_container
                all_interactions.add(self.id(), container)
                cls.set_interaction_container(None)
            return tear_down(self, *args, **kwargs)

        return wrapped

    @classmethod
    def patch_test_case(cls):
        SimpleTestCase._pre_setup = cls.wrap_pre_set_up(SimpleTestCase._pre_setup)

        SimpleTestCase._post_teardown = cls.wrap_post_tear_down(
            SimpleTestCase._post_teardown
        )

    @classmethod
    def wrap_setup_test_environment(cls, func):
        def wrapped(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not OpticDjangoAppConfig.enabled():
                return result
            cls.test_result_container = TestResultInteractionContainer()
            return result

        return wrapped

    @classmethod
    def wrap_teardown_test_environment(cls, func):
        def wrapped(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if not OpticDjangoAppConfig.enabled():
                return result
            interactions = cls.test_result_container.get_interaction_list()
            manager = OpticDjangoAppConfig.get_manager()
            if manager:
                manager.optic.send_interactions(interactions)
            cls.test_result_container = None
            return result

        return wrapped

    @classmethod
    def patch_runner(cls):
        # FIXME: this is incompatible with --parallel and --test-runner
        # command arguments
        test_runner = get_runner(settings)

        if not hasattr(test_runner, "setup_test_environment") or not hasattr(
            test_runner, "teardown_test_environment"
        ):
            return

        test_runner.setup_test_environment = cls.wrap_setup_test_environment(
            test_runner.setup_test_environment
        )
        test_runner.teardown_test_environment = cls.wrap_teardown_test_environment(
            test_runner.teardown_test_environment
        )

    @classmethod
    def set_up_additional(cls):
        cls.patch_test_case()
        cls.patch_result()
        cls.patch_runner()

    @classmethod
    def patch_result(cls):
        TestResult.addSuccess = cls.wrap_result_handler(TestResult.addSuccess, True)
        TestResult.addFailure = cls.wrap_result_handler(TestResult.addFailure, False)
        TestResult.addError = cls.wrap_result_handler(TestResult.addError, False)

    @classmethod
    def wrap_result_handler(cls, result_handler, success):
        """
        Intercepts Result handler hooks to update test containers about the status of the test result
        """

        def wrapped(self, test: TestCase, *args, **kwargs):
            if (
                not hasattr(cls, "test_result_container")
                or cls.test_result_container is None
                or not OpticDjangoAppConfig.enabled()
            ):
                return result_handler(self, test, *args, **kwargs)
            cls.test_result_container.update_test_result_status(test.id(), success)
            result = result_handler(self, test, *args, **kwargs)
            return result

        return wrapped
