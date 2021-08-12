import json
import os
from dataclasses import dataclass

import requests


@dataclass
class OpticConfig:
    framework: str
    ENABLE: bool = os.environ.get("OPTIC_ENABLE", True)
    DEV: bool = os.environ.get("OPTIC_DEV", False)
    LOCAL: bool = os.environ.get("OPTIC_LOCAL", True)
    CONSOLE: bool = os.environ.get("OPTIC_CONSOLE", False)
    LOG: bool = os.environ.get("OPTIC_LOG", False)
    LOG_PATH: str = os.environ.get("OPTIC_LOG_PATH", "./optic.log")
    UPLOAD_URL: str = os.environ.get("OPTIC_LOGGING_URL", "")


class Optic:
    def __init__(self, config: OpticConfig):
        super().__init__()
        self.config = config

    def send_to_file(self, interactions: list):
        with open(self.config.LOG_PATH, "w+") as f:
            f.write(json.dumps(interactions) + "\n")

    def send_to_console(self, interactions: list):
        print(json.dumps(interactions) + "\n")

    def get_ingest_url(self) -> str:
        if self.config.UPLOAD_URL == "":
            # TODO Add error message with instruction
            raise Exception(
                "Optic url could not be found. Please run optic with api exec <command>"
            )
        return self.config.UPLOAD_URL + "ecs"

    def send_to_local_cli(self, interactions) -> int:
        ingest_url = self.get_ingest_url()
        r = requests.post(ingest_url, json=interactions)
        return r.status_code

    def send_interactions(self, interactions: list):
        if not self.config.ENABLE:
            return
        if self.config.CONSOLE:
            self.send_to_console(interactions)
        if self.config.LOG:
            self.send_to_file(interactions)
        if self.config.LOCAL:
            self.send_to_local_cli(interactions)
