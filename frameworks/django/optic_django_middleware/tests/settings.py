# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

import os.path
from tempfile import mkdtemp

import django

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+++tu-okmph8o##2j4_cow30#j1*qdfvt0pj-+qsfc+i5_b0zx"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

tempdir = mkdtemp("optic_tests")

OPTIC = {
    "ENABLE": True,
    "LOG_PATH": os.path.join(tempdir, "optic.log"),
    "LOG": True,
    "CONSOLE": False,
    "LOCAL": False,
}

ROOT_URLCONF = "urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django",
    "optic_django_middleware",
]

SITE_ID = 1

if django.VERSION >= (1, 10):
    MIDDLEWARE = ()
else:
    MIDDLEWARE_CLASSES = ()
