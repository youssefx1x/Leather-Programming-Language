from dataclasses import dataclass
from typing import Any


@dataclass
class Program:
    statements: list


@dataclass
class Literal:
    value: Any


@dataclass
class ListLiteral:
    items: list


@dataclass
class MapLiteral:
    items: list


@dataclass
class Name:
    name: str


@dataclass
class Member:
    object: Any
    name: str


@dataclass
class Index:
    object: Any
    index: Any


@dataclass
class Unary:
    op: str
    operand: Any


@dataclass
class Binary:
    left: Any
    op: str
    right: Any


@dataclass
class Call:
    name: str
    args: list


@dataclass
class Assignment:
    name: str
    expr: Any
    op: str = "="


@dataclass
class Rule:
    name: str
    condition: Any
    actions: list
