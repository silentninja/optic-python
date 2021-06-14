import platform
from urllib.parse import urlparse

from django.http import HttpRequest, HttpResponse

from optic.main import Optic, OpticConfig
from .apps import OpticDjangoAppConfig
from .serializers import OpticEcsLogger


class BasicInteractionContainer:
    optic = None

    def __init__(self) -> None:
        super().__init__()

    def capture_interaction(self, request: HttpRequest, response: HttpResponse, request_body: bytes):
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(request, response, request_body)
        self.on_interaction_captured(serialized_interaction)

    def on_interaction_captured(self, serialized_interaction):
        self.optic.send_interaction(serialized_interaction)

    @classmethod
    def set_up(cls):
        cls.optic = Optic(OpticDjangoAppConfig.get_optic_settings())