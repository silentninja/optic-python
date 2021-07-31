#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import os
import sys
import unittest
from unittest import TestLoader

import django

from tests.test_query_count_runner import TestRunnerTest


def run_tests(*test_args):
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    django.setup()
    test_runner = unittest.TextTestRunner()
    test_runner.run(TestLoader().loadTestsFromTestCase(TestRunnerTest))


if __name__ == "__main__":
    run_tests(*sys.argv[1:])
