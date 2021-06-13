from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin



class OpticMiddleware(MiddlewareMixin):
    """
    Intercepts queries in a request and sends it to optic daemon
    The middleware is intended to be automatically added

    """

    def process_request(self, request: HttpRequest):
        self.cached_request_body = request.body
        return None

    def process_response(self, request: HttpRequest, response: HttpResponse):
        return response
