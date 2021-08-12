import json
from typing import Dict
from urllib.parse import urlparse

from django.http import HttpRequest, HttpResponse
from kubi_ecs_logger import Logger
from kubi_ecs_logger.models import BaseSchema


class OpticEcsLogger(Logger):
    def __init__(self, *args, **kwargs):
        super(OpticEcsLogger, self).__init__(*args, **kwargs)

    def get_log_dict(self):
        return BaseSchema().dump(self._base)

    def serialize_to_ecs(
        self, request: HttpRequest, response: HttpResponse, request_body: bytes
    ) -> Dict:
        parsed_url = urlparse(request.build_absolute_uri())
        # Todo Add support for optional django-user-agents package
        user_agent_string = getattr(
            request.headers,
            "user_agent",
            None,
        )
        serialized_request_body: str
        if request.method == "GET":
            serialized_request_body = json.dumps(dict(request.GET))
        else:
            # For any other methods like POST, PUT, PATH
            if request.headers.get("content-type") == "application/json":
                serialized_request_body = request_body.decode("utf-8")
            else:
                serialized_request_body = json.dumps(dict(request.POST))

        if not user_agent_string and "HTTP_USER_AGENT" in request.META:
            user_agent_string = request.META["HTTP_USER_AGENT"]

        log = (
            self.url(
                full=parsed_url.geturl(),
                path=parsed_url.path,
                domain=parsed_url.hostname,
                port=parsed_url.port,
                query=parsed_url.query,
            )
            .http_response(
                status_code=response.status_code,
                body_content=response.content,
                bytes=len(response.content),
            )
            .http_request(
                body_content=serialized_request_body,
                method=request.method,
                bytes=len(serialized_request_body),
            )
            .user_agent(original=user_agent_string)
        )
        request_headers = {k: v for k, v in request.headers.items()}
        response_headers = {k: v for k, v in response.headers.items()}

        obj = log.get_log_dict()
        obj["http"] = {}
        if "httpresponse" in obj:
            obj["http"]["response"] = {
                "body": {
                    "content": obj["httpresponse"]["body_content"],
                    "bytes": obj["httpresponse"]["bytes"],
                },
                "status_code": int(obj["httpresponse"]["status_code"]),
                "headers": response_headers,
            }
        if "httprequest" in obj:
            obj["http"]["request"] = {
                "body": {
                    "content": obj["httprequest"]["body_content"],
                    "bytes": obj["httprequest"]["bytes"],
                },
                "method": obj["httprequest"]["method"],
                "headers": request_headers,
            }
        del obj["httpresponse"]
        del obj["httprequest"]
        return obj
