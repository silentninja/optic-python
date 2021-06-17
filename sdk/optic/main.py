import json
import os
import re
import subprocess
from dataclasses import dataclass
from subprocess import CalledProcessError
from typing import Optional

import requests


@dataclass
class OpticConfig:
    framework: str
    DEV: bool = os.environ.get("OPTIC_DEV", False)
    LOCAL: bool = os.environ.get("OPTIC_LOCAL", True)
    CONSOLE: bool = os.environ.get("OPTIC_CONSOLE", False)
    LOG: bool = os.environ.get("OPTIC_LOG", False)


class Optic:
    def __init__(self, config: OpticConfig) -> None:
        super().__init__()
        self.config = config

    @staticmethod
    def cli_command(dev: bool = False) -> str:
        optic_api_path = os.environ.get("OPTIC_API_PATH", None)
        if optic_api_path:
            return optic_api_path
        return 'api' + ('dev' if dev else "")

    def check_optic_command(self) -> bool:
        try:
            subprocess.check_call([Optic.cli_command(self.config.DEV)], shell=True)
            return True
        except CalledProcessError as e:
            return False

    def send_to_file(self, interactions: list) -> None:
        with open("./optic.log", "w+") as f:
            f.write(json.dumps(interactions) + "\n")

    def send_to_console(self, interactions: list) -> None:
        print(json.dumps(interactions) + "\n")

    def call_optic(self, parameters: str):
        result = subprocess.run([Optic.cli_command(self.config.DEV) + parameters], shell=True,
                                capture_output=True).stdout
        return result

    def get_ingest_url(self) -> Optional[str]:
        ingest_url = self.call_optic(" ingest:ingest-url")
        matches = re.match(r'^ingestUrl:\s+(?P<url>\S+)', ingest_url.decode("utf-8"))
        if matches is not None:
            matches = matches.groupdict()
            if 'url' in matches:
                return matches['url']
        return None

    def send_to_local_cli(self, interactions):
        ingest_url = self.get_ingest_url()
        r = requests.post(ingest_url, data=interactions)
        return r.status_code

    def send_interactions(self, interactions: list):
        if self.config.CONSOLE:
            self.send_to_console(interactions)
        if self.config.LOG:
            self.send_to_file(interactions)
        if self.config.LOCAL:
            self.send_to_local_cli(interactions)
