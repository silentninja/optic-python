import json
from pprint import pprint
from unittest import TestCase

from freezegun import freeze_time

from fixtures import get_fixture
from optic_django_middleware.serializers import OpticEcsLogger
from django.test import RequestFactory, TestCase

from tests.views import view1


class HttpInteractionCountContainerTestCase(TestCase):

    @freeze_time("2021-01-01")
    def test_serialize_to_ecs(self):
        rf = RequestFactory(HTTP_USER_AGENT="DjangoTestServer")
        request = rf.get('/url-1/')
        response = view1(request)
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(request, response, request.body)
        interaction = get_fixture("1.log")
        self.assertDictEqual(interaction, serialized_interaction)
