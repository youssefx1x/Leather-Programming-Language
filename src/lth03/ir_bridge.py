import hashlib
from dataclasses import asdict, dataclass, is_dataclass

from .base_syntax import prepare_source as prepare_bases
from .final_runner import LTH03FinalRunner
from .lexer import Lexer
from .parser import Parser


@dataclass(frozen=True)
class IRInstruction:
    op: str
    payload: dict


@dataclass(frozen=True)
class IRProgram:
    instructions: tuple
    source_hash: str
    flow_names: tuple
    system_names: tuple
    base_names: tuple


def _node_payload(value):
    if is_dataclass(value):
        return {
            key: _node_payload(item)
            for key, item in asdict(value).items()
        }

    if isinstance(value, dict):
        return {
            str(key): _node_payload(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            _node_payload(item)
            for item in value
        ]

    return value


class LTH03SemanticBridge:
    def prepare(self, source):
        runner = LTH03FinalRunner()

        advanced, flows, systems = runner.prepare(
            source
        )

        prepared, bases = prepare_bases(
            advanced
        )

        return (
            prepared,
            bases,
            flows,
            systems,
        )

    def analyze(self, source):
        prepared, bases, flows, systems = self.prepare(
            source
        )

        tokens = Lexer(prepared).tokenize()
        program = Parser(tokens).parse()

        assignments = 0
        rules = 0

        for statement in program.statements:
            name = type(statement).__name__

            if name == "Assignment":
                assignments += 1
            elif name == "Rule":
                rules += 1

        return {
            "assignments": assignments,
            "rules": rules,
            "flow_names": tuple(flows.names()),
            "system_names": tuple(systems.names()),
            "base_names": tuple(bases.names()),
            "statement_count": len(
                program.statements
            ),
        }

    def compile(self, source):
        prepared, bases, flows, systems = self.prepare(
            source
        )

        tokens = Lexer(prepared).tokenize()
        program = Parser(tokens).parse()

        instructions = []

        for name in bases.names():
            instructions.append(
                IRInstruction(
                    "BASE_DEFINE",
                    {"name": name},
                )
            )

        for name, definition in flows.items():
            instructions.append(
                IRInstruction(
                    "FLOW_DEFINE",
                    {
                        "name": name,
                        "source": definition.source,
                    },
                )
            )

        for name, definition in systems.items():
            instructions.append(
                IRInstruction(
                    "SYSTEM_DEFINE",
                    {
                        "name": name,
                        "flows": definition.flows,
                    },
                )
            )

        instructions.append(
            IRInstruction(
                "AST_PROGRAM",
                {
                    "program": _node_payload(
                        program
                    )
                },
            )
        )

        source_hash = hashlib.sha256(
            prepared.encode("utf-8")
        ).hexdigest()

        return IRProgram(
            instructions=tuple(instructions),
            source_hash=source_hash,
            flow_names=tuple(flows.names()),
            system_names=tuple(systems.names()),
            base_names=tuple(bases.names()),
        )
