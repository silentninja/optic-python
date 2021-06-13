import io
import json
import os
from os import path
import unittest
from unittest.mock import patch

from optic.main import OpticConfig, Optic


class OpticInitializationTestCase(unittest.TestCase):
    def test_optic_initialized_with_config(self):
        config = OpticConfig(framework="Unittest", DEV=True, CONSOLE=True, LOCAL=False, LOG=True)
        optic = Optic(config)
        self.assertEqual(optic.config, config)


class OpticTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.config_options = {'framework': "Unittest", 'DEV': True, 'CONSOLE': True, 'LOCAL': False, 'LOG': True}

    def tearDown(self) -> None:
        super().tearDown()
        try:
            os.remove("./optic.log")
        except FileNotFoundError:
            pass

    def test_optic_version_on_production(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        self.assertEqual(optic.cli_command(), 'api')

    def test_optic_version_on_development(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        self.assertEqual(optic.cli_command(dev=True), 'apidev')

    def test_optic_cli_dev_installation_status_verification(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        self.assertEqual(optic.check_optic_command(), True)

    def test_optic_cli_production_installation_status_verification(self):
        self.config_options['DEV'] = False
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        self.assertEqual(optic.check_optic_command(), True)

    def test_send_interaction_object_to_console(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        interaction_object = {}
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            optic.send_to_console(interaction_object)
            self.assertEqual(fake_out.getvalue().strip("\n"), json.dumps(interaction_object))

    def test_send_interaction_object_to_file(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        interaction_object = {}
        self.assertFalse(path.exists(
                './optic.log'
        ))
        optic.send_to_file(interaction_object)
        self.assertTrue(path.exists(
                './optic.log'
        ))

    # Mock cli call if needed
    def test_ingest_url(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        self.assertIn("http://", optic.get_ingest_url())

    def test_send_interaction_to_optic(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        interaction_object = {}
        self.assertEqual(optic.send_to_local_cli(interaction_object), 204)

if __name__ == '__main__':
    unittest.main()
