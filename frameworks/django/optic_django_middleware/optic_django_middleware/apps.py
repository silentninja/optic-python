# -*- coding: utf-8
from dataclasses import dataclass, fields

from django.apps import AppConfig
from django.conf import settings

from optic.main import OpticConfig


@dataclass
class OpticDjangoConfig(OpticConfig):
    ENABLE = True
    LOG_PATH = "./optic.log"
    INTERACTION_CONTAINER = "optic_django_middleware.container.BasicInteractionContainer"


class OpticDjangoAppConfig(AppConfig):
    name = 'optic_django_middleware'
    verbose_name = 'Optic Middleware'

    setting_name = 'OPTIC'

    default_settings = OpticDjangoConfig(framework="Django")

    @classmethod
    def get_setting(cls, setting_name):
        return (getattr(settings, cls.setting_name, {})
                .get(setting_name, getattr(cls.default_settings, setting_name)))

    @classmethod
    def enabled(cls):
        return cls.get_setting('ENABLE')

    def ready(self):
        if self.enabled():
            from .manager import OpticManager
            OpticManager.set_up()

    @classmethod
    def get_optic_settings(cls):
        field_names = set(f.name for f in fields(OpticConfig))
        c = {k: cls.get_setting(k) for k in field_names}
        return OpticConfig(**c)
