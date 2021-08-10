# Optic Django Middleware

<!-- Badges -->
[![Build status](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml)

This module is an [Django](https://djangoproject.com/) middleware using [optic-sdk]() to capture and format HTTP data to send to [Optic](https://www.useoptic.com). We have a [list of middleware available for some frameworks](https://github.com/silentninja/optic-python), if we are missing the framework [join our community](https://useoptic.com/docs/community/) and suggest the next framework or develop it with us.

## Requirements

The module requires `@useoptic/cli` to be installed, instructions on installing it are available [https://www.useoptic.com/docs/](https://www.useoptic.com/docs/).

## Install

```sh
pip install optic-django-middlewaree
```

## Usage

The middleware takes a configuration object and captures traffic in the background as long as `@useoptic/cli` is installed.

### Configuration
Environment variables can also be used to set the values
- `ENABLE`: `boolean` (defaults to `FALSE`) Programmatically control if capturing data and sending it to Optic
- `UPLOAD_URL`: `string` (defaults to `os.environ['OPTIC_LOGGING_URL']`) The URL to Optics capture URL, if left blank it will expect `OPTIC_LOGGING_URL` environment variable set by the Optic CLI
- `CONSOLE`: `boolean` (defaults to `FALSE`) Send to stdout/console for debugging
- `framework`: `string` (defaults to '') Additional information to inform Optic of where it is capturing information
- `LOG`: `boolean` (defaults to `FALSE`) Send to log file
- `LOG_PATH`: `boolean` (defaults to `./optic.log`) Log file path
- `LOCAL`: `boolean` (defaults to `TRUE`) Send to optic cli
- `INTERACTION_MANAGER`: `string` (defaults to `optic_django_middleware.manager.BasicOpticManager`) Manager module to control the behaviour of capturing and sending interaction

### Example

```python
# settings.py
import os
from tempfile import mkdtemp
tempdir = mkdtemp('optic_django')
OPTIC = {
    'ENABLE': True,
    'LOG_PATH': os.path.join(tempdir, 'optic.log'),
    'LOG': True,
    'CONSOLE': False,
    'LOCAL': False
}

INSTALLED_APPS += [
    'optic_django_middleware',
]

```

To start capturing data from the SDK, run your application with

```sh
api exec "python manage.py runserver"
```

## License
This software is licensed under the [MIT license](../../../LICENSE).
