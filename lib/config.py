import os
from dataclasses import asdict, dataclass, field
from typing import List
import yaml


class Loadable:
    def set_attributes(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)


@dataclass(init=False)
class Config(Loadable):
    bloom_versions: List[str]

    def __init__(self, config_path: str = "../app-config.yaml"):
        self._load(config_path)

    def _load(self, config_path: str):
        with open(os.path.join(os.path.dirname(__file__), config_path), "r") as f:
            raw = yaml.safe_load(f)
        self.set_attributes(raw)
