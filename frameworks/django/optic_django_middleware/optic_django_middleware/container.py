from django.http import HttpRequest, HttpResponse

from .manager import BasicOpticManager
from .serializers import OpticEcsLogger


class BasicInteractionContainer:

    def __init__(self) -> None:
        super().__init__()

    def capture_interaction(self, request: HttpRequest, response: HttpResponse, request_body: bytes):
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(request, response, request_body)
        self.on_interaction_captured(serialized_interaction)

    def on_interaction_captured(self, serialized_interaction):
        BasicOpticManager.optic.send_interaction(serialized_interaction)