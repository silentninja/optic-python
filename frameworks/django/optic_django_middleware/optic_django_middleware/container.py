from django.http import HttpRequest, HttpResponse

from .apps import OpticDjangoAppConfig
from .serializers import OpticEcsLogger


class BasicInteractionContainer:

    def __init__(self) -> None:
        super().__init__()

    def capture_interaction(self, request: HttpRequest, response: HttpResponse, request_body: bytes):
        serialized_interaction = OpticEcsLogger().serialize_to_ecs(request, response, request_body)
        self.on_interaction_captured(serialized_interaction)

    def on_interaction_captured(self, serialized_interaction):
        manager = OpticDjangoAppConfig.get_manager()
        if manager:
            manager.optic.send_interactions([serialized_interaction])
