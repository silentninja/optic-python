# -*- coding: utf-8
import importlib
from dataclasses import dataclass, fields

from django.apps import AppConfig
from django.conf import settings
from optic import OpticConfig


@dataclass
class OpticDjangoConfig(OpticConfig):
    INTERACTION_MANAGER = "optic_django_middleware.manager.BasicOpticManager"


class OpticDjangoAppConfig(AppConfig):
    name = "optic_django_middleware"
    verbose_name = "Optic Middleware"

    setting_name = "OPTIC"

    default_settings = OpticDjangoConfig(framework="Django")

    @classmethod
    def get_setting(cls, setting_name):
        return getattr(settings, cls.setting_name, {}).get(
            setting_name, getattr(cls.default_settings, setting_name)
        )

    @classmethod
    def enabled(cls) -> bool:
        return cls.get_setting("ENABLE")

    @classmethod
    def log_path(cls) -> str:
        return cls.get_setting("LOG_PATH")

    def ready(self):
        if self.enabled():
            OpticDjangoAppConfig.get_manager().set_up()

    @classmethod
    def get_manager(cls):
        module_name, class_name = OpticDjangoAppConfig.get_setting(
            "INTERACTION_MANAGER"
        ).rsplit(".", 1)
        InteractionManager = getattr(importlib.import_module(module_name), class_name)
        return InteractionManager

    @classmethod
    def get_optic_settings(cls) -> OpticConfig:
        field_names = set(f.name for f in fields(OpticConfig))
        c = {k: cls.get_setting(k) for k in field_names}
        return OpticConfig(**c)
