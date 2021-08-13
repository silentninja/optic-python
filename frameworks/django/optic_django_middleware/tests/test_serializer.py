from django.test import RequestFactory, TestCase
from django.utils.datastructures import MultiValueDict
from django.utils.http import urlencode
from fixtures import get_fixture
from freezegun import freeze_time
from middleware_test_app.views import form_view, json_view, view1

from optic_django_middleware.serializers import OpticEcsLogger


class HttpInteractionCountContainerTestCase(TestCase):
    @freeze_time("2021-01-01")
    def test_serialize_to_ecs(self):
        rf = RequestFactory(HTTP_USER_AGENT="DjangoTestServer")
        request = rf.get("/url-1/")
        response = view1(request)
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(
            request, response, request.body
        )
        interaction = get_fixture("1.log")
        self.assertDictEqual(interaction[0], serialized_interaction)

    @freeze_time("2021-01-01")
    def test_serialize_form_test(self):
        rf = RequestFactory(HTTP_USER_AGENT="DjangoTestServer")
        form_data = urlencode(
            MultiValueDict({"name": "Boo", "names": ["foo", "bar"]}), doseq=True
        )
        request = rf.post(
            "/form-url",
            data=form_data,
            content_type="application/x-www-form-urlencoded",
        )
        response = form_view(request)
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(
            request, response, request.body
        )
        interaction = get_fixture("2.log")
        self.assertDictEqual(interaction[0], serialized_interaction)

    @freeze_time("2021-01-01")
    def test_serialize_json_test(self):
        rf = RequestFactory(HTTP_USER_AGENT="DjangoTestServer")
        request = rf.put(
            "/json-url-3", data={"name": "Boo"}, content_type="application/json"
        )
        response = json_view(request)
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(
            request, response, request.body
        )
        interaction = get_fixture("3.log")
        self.assertDictEqual(interaction[0], serialized_interaction)
