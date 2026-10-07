from dataclasses import dataclass, field


@dataclass
class Base:
    name: str
    service: str
    options: list = field(default_factory=list)


@dataclass
class BaseExtension:
    name: str
    base_name: str
    options: list = field(default_factory=list)


@dataclass
class Flow:
    name: str
    steps: list
