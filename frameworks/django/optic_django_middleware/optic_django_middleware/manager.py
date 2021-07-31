# -*- coding: utf-8
import inspect
import threading

from django.conf import settings
from django.utils.module_loading import import_string
from optic import Optic

from .apps import OpticDjangoAppConfig

local = threading.local()


class BasicOpticManager:
    optic = None

    @classmethod
    def get_interaction_container(cls):
        return getattr(cls, "interaction_container", None)

    @classmethod
    def is_middleware_class(cls, middleware_path) -> bool:
        from optic_django_middleware.middleware import OpticMiddleware

        try:
            middleware_cls = import_string(middleware_path)
        except ImportError:
            return False
        return inspect.isclass(middleware_cls) and issubclass(
            middleware_cls, OpticMiddleware
        )

    @classmethod
    def add_middleware(cls):
        middleware_class_name = "optic_django_middleware.middleware.OpticMiddleware"
        middleware_setting = getattr(settings, "MIDDLEWARE", None)
        setting_name = "MIDDLEWARE"
        if middleware_setting is None:
            middleware_setting = settings.MIDDLEWARE_CLASSES
            setting_name = "MIDDLEWARE_CLASSES"

        # add the middleware only if it was not added before
        if not any(map(cls.is_middleware_class, middleware_setting)):
            if isinstance(middleware_setting, list):
                new_middleware_setting = middleware_setting + [middleware_class_name]
            elif isinstance(middleware_setting, tuple):
                new_middleware_setting = middleware_setting + (middleware_class_name,)
            else:
                err_msg = "{} is missing from {}.".format(
                    middleware_class_name, setting_name
                )
                raise TypeError(err_msg)

            setattr(settings, setting_name, new_middleware_setting)

    @classmethod
    def capture_interaction(cls, request, response, cached_request_body):
        cls.get_interaction_container().capture_interaction(
            request, response, cached_request_body
        )

    @classmethod
    def set_up(cls):
        cls.add_middleware()
        cls.set_up_optic()
        cls.set_up_additional()

    @classmethod
    def set_up_additional(cls):
        cls.set_up_interaction_container()

    @classmethod
    def set_up_optic(cls):
        cls.optic = Optic(OpticDjangoAppConfig.get_optic_settings())

    @classmethod
    def set_up_interaction_container(cls):
        from optic_django_middleware.container import BasicInteractionContainer

        cls.interaction_container = BasicInteractionContainer()
