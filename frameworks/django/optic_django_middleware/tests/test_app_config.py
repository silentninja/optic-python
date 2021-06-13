from django.conf import settings
from django.test import TestCase, override_settings

from optic_django_middleware.apps import OpticDjangoAppConfig
from optic_django_middleware.manager import OpticManager


class TestAppConfig(TestCase):

    def test_default_enabled(self):
        self.assertTrue(OpticDjangoAppConfig.enabled())

    @override_settings(OPTIC={'ENABLE': False})
    def test_override_disabled(self):
        self.assertFalse(OpticDjangoAppConfig.enabled())

    @override_settings(OPTIC={'ENABLE': True})
    def test_override_enabled(self):
        self.assertTrue(OpticDjangoAppConfig.enabled())

    def test_add_middleware_twice(self):
        OpticManager.add_middleware()
        OpticManager.add_middleware()

        middlewares = settings.MIDDLEWARE
        self.assertEqual(len(middlewares), 1)
        self.assertEqual(middlewares[0],
                         'optic_django_middleware.middleware.OpticMiddleware'
                         )

    def test_list_middlewares_types(self):
        with override_settings(MIDDLEWARE=[]):
            OpticManager.add_middleware()
            self.assertEqual(settings.MIDDLEWARE, [
                             'optic_django_middleware.middleware.OpticMiddleware'
                             ])
        with override_settings(MIDDLEWARE=()):
            OpticManager.add_middleware()
            self.assertEqual(
                settings.MIDDLEWARE,
                ('optic_django_middleware.middleware.OpticMiddleware',)
            )
        with override_settings(MIDDLEWARE='some_nasty_thing'):
            with self.assertRaises(Exception):
                OpticManager.add_middleware()
