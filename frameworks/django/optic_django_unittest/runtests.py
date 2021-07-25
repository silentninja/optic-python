#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os
import sys
import unittest
from unittest import TestLoader

import django
from django.conf import settings
from django.test.utils import get_runner

from tests.test_query_count_runner import TestRunnerTest


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(TestLoader().loadTestsFromTestCase(TestRunnerTest))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
