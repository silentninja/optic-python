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
    LOG_PATH: str = os.environ.get("OPTIC_LOG_PATH", "./optic.log")
    UPLOAD_URL: str = os.environ.get("OPTIC_LOGGING_URL", "http://localhost:4001/")


class Optic:
    def __init__(self, config: OpticConfig) -> None:
        super().__init__()
        self.config = config

    def send_to_file(self, interactions: list) -> None:
        with open(self.config.LOG_PATH, "w+") as f:
            f.write(json.dumps(interactions) + "\n")

    def send_to_console(self, interactions: list) -> None:
        print(json.dumps(interactions) + "\n")

    def get_ingest_url(self) -> Optional[str]:
        if self.config.UPLOAD_URL == "":
            raise Exception("Optic url could not be found. Please run optic with api exec <command>")
        return self.config.UPLOAD_URL + "ecs"

    def send_to_local_cli(self, interactions):
        ingest_url = self.get_ingest_url()
        print(interactions)
        r = requests.post(ingest_url, json=interactions,)
        return r.status_code

    def send_interactions(self, interactions: list):
        if self.config.CONSOLE:
            self.send_to_console(interactions)
        if self.config.LOG:
            self.send_to_file(interactions)
        if self.config.LOCAL:
            self.send_to_local_cli(interactions)
