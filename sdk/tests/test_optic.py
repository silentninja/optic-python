import io
import json
import os
import unittest
from os import path
from unittest.mock import patch

from optic import Optic, OpticConfig

from .fixtures import get_fixture


class OpticInitializationTestCase(unittest.TestCase):
    def test_optic_initialized_with_config(self):
        config = OpticConfig(
            framework="Unittest", DEV=True, CONSOLE=True, LOCAL=False, LOG=True
        )
        optic = Optic(config)
        self.assertEqual(optic.config, config)


class OpticTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.config_options = {
            "framework": "Unittest",
            "DEV": True,
            "CONSOLE": True,
            "LOCAL": False,
            "LOG": True,
        }

    def tearDown(self) -> None:
        super().tearDown()
        try:
            os.remove("./optic.log")
        except FileNotFoundError:
            pass

    def test_send_interaction_object_to_console(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        interactions = get_fixture("1.log")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            optic.send_to_console(interactions)
            self.assertEqual(fake_out.getvalue().strip("\n"), json.dumps(interactions))

    def test_send_interaction_object_to_file(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        interaction_object = get_fixture("1.log")
        self.assertFalse(path.exists("./optic.log"))
        optic.send_to_file([interaction_object])
        self.assertTrue(path.exists("./optic.log"))

    # Mock cli call if needed
    def test_ingest_url(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        self.assertIsNotNone(optic.get_ingest_url())
        self.assertIn("http://", optic.get_ingest_url())

    def test_send_interaction_to_optic(self):
        config = OpticConfig(**self.config_options)
        optic = Optic(config)
        interaction_object = get_fixture("1.log")
        self.assertEqual(optic.send_to_local_cli(interaction_object), 201)
