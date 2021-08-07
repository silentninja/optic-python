Optic Python Sdk

<!-- Badges -->
[![Build status](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/silentninja/optic-python/actions/workflows/run_tests.yml)

The code library standardizing data capture for [Optic](https://www.useoptic.com) in Python applications. We have a [list of middleware available for some frameworks](https://github.com/silentninja/optic-python), if we are missing the framework [join our community](https://useoptic.com/docs/community/) and suggest the next framework or develop it with us.

## Requirements

The library requires `@useoptic/cli` to be installed, instructions on installing it are available [https://www.useoptic.com/docs/](https://www.useoptic.com/docs/).

## Install

```sh
pip install optic-sdk
```

## Usage

The library provides apis to interact with optic cli. This library does not provide ecs converters and should be used
along with framework specific optic libraries

### Configuration

Environment variables can also be used to set the values.

- `ENABLE`: `boolean` (defaults to `True`) Programmatically control if capturing data and sending it to Optic
- `UPLOAD_URL`: `string` (defaults to `os.environ['OPTIC_LOGGING_URL']`) The URL to Optics capture URL, if left blank it
  will expect `OPTIC_LOGGING_URL` environment variable set by the Optic CLI
- `CONSOLE`: `boolean` (defaults to `False`) Send to stdout/console for debugging
- `framework`: `string`  Additional information to inform Optic of where it is capturing information
- `LOG`: `boolean` (defaults to `False`) Send to log file
- `LOG_PATH`: `boolean` (defaults to `./optic.log`) Log file path
- `LOCAL`: `boolean` (defaults to `True`) Send to optic cli

### Example

        from optic import OpticConfig, Optic
        def send_to_optic_cli(ecs_object):
            """
            ecs_object: Json serializble ecs object
            """
            config = OpticConfig(framework="<insert name>", CONSOLE=True)
            optic = Optic(config)
            optic.send_to_local_cli(ecs_object) //send to optic cli
            optic.send_to_file(ecs_object) //save to file
            optic.send_to_console(ecs_object) //send to stdout

## License
This software is licensed under the [MIT license](../LICENSE).
