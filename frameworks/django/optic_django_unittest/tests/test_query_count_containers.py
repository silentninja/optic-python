from django.test import RequestFactory, TestCase
from freezegun import freeze_time
from optic_django_unittest.container import (
    TestCaseInteractionContainer,
    TestResultInteractionContainer,
)
from unittest_test_app.views import view1, view2

from optic_django_middleware.serializers import OpticEcsLogger


class MockRequest(object):
    def __init__(self, method, path):
        self.method = method
        self.path = path


class HttpInteractionCountContainerTestCase(TestCase):
    def test_case_container_empty(self):
        container = TestCaseInteractionContainer()
        self.assertEqual(len(container.http_interactions), 0)

    @freeze_time("2021-01-01")
    def test_case_add_different_path(self):
        container = TestCaseInteractionContainer()
        self.assertEqual(len(container.http_interactions), 0)

        rf = RequestFactory()
        request = rf.get("/url-1/")
        response = view1(request)
        container.capture_interaction(request, response, request.body)
        self.assertEqual(len(container.http_interactions), 1)
        self.assertEqual(
            container.http_interactions,
            [OpticEcsLogger().serialize_to_ecs(request, response, request.body)],
        )

        rf = RequestFactory()
        request1 = rf.get("/url-2/")
        response1 = view2(request1)
        container.capture_interaction(request1, response1, request1.body)

        self.assertEqual(len(container.http_interactions), 2)

        self.assertEqual(
            container.http_interactions,
            [
                OpticEcsLogger().serialize_to_ecs(request, response, request.body),
                OpticEcsLogger().serialize_to_ecs(request1, response1, request1.body),
            ],
        )

    @freeze_time("2021-01-01")
    def test_case_add_same_path(self):
        container = TestCaseInteractionContainer()
        self.assertEqual(len(container.http_interactions), 0)

        rf = RequestFactory()
        request = rf.get("/url-1/")
        response = view1(request)
        container.capture_interaction(request, response, request.body)
        self.assertEqual(len(container.http_interactions), 1)
        self.assertEqual(
            container.http_interactions,
            [OpticEcsLogger().serialize_to_ecs(request, response, request.body)],
        )

        rf = RequestFactory()
        request1 = rf.get("/url-1/")
        response1 = view1(request1)
        container.capture_interaction(request1, response1, request1.body)

        self.assertEqual(len(container.http_interactions), 2)

        self.assertEqual(
            container.http_interactions,
            [
                OpticEcsLogger().serialize_to_ecs(request, response, request.body),
                OpticEcsLogger().serialize_to_ecs(request1, response1, request1.body),
            ],
        )

    def test_case_merge(self):
        container = TestCaseInteractionContainer()
        rf = RequestFactory()
        request = rf.get("/url-1/")
        response = view1(request)
        container.capture_interaction(request, response, request.body)

        container_2 = TestCaseInteractionContainer()
        rf = RequestFactory()
        request = rf.get("/url-1/")
        response = view1(request)
        container.capture_interaction(request, response, request.body)

        container.merge(container_2)
        self.assertEqual(len(container.http_interactions), 2)

    def test_result_empty(self):
        container = TestResultInteractionContainer()
        self.assertEqual(len(container.interactions_by_testcase.keys()), 0)

    def test_result_add(self):
        result_container = TestResultInteractionContainer()
        rf = RequestFactory()
        request = rf.get("/url-1/")
        response = view1(request)

        test_case_container = TestCaseInteractionContainer()
        test_case_container.capture_interaction(request, response, request.body)

        result_container.add("some.test.test_function", test_case_container)
        self.assertEqual(len(result_container.interactions_by_testcase.keys()), 1)

        rf = RequestFactory()
        request = rf.get("/url-1/")
        response = view1(request)
        test_case_container = TestCaseInteractionContainer()
        test_case_container.capture_interaction(request, response, request.body)

        result_container.add("some.test.test_other", test_case_container)
        self.assertEqual(len(result_container.interactions_by_testcase.keys()), 2)
