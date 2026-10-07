import hashlib

from src.lth03.base_syntax import prepare_source as prepare_bases
from src.lth03.final_runner import LTH03FinalRunner
from src.lth03.lexer import Lexer
from src.lth03.parser import Parser

from .model import BytecodeProgram, Instruction


class BytecodeCompiler:
    VERSION = "LTH04-BYTECODE-1"

    def __init__(self):
        self.final_runner = LTH03FinalRunner()

    def prepare(self, source):
        advanced, flows, systems = self.final_runner.prepare(
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

    def compile(self, source):
        (
            prepared,
            bases,
            flows,
            systems,
        ) = self.prepare(source)

        tokens = Lexer(prepared).tokenize()
        program = Parser(tokens).parse()

        source_hash = hashlib.sha256(
            (
                self.VERSION
                + "\n"
                + prepared
            ).encode("utf-8")
        ).hexdigest()

        instructions = (
            Instruction(
                "EXECUTE",
                prepared,
            ),
            Instruction(
                "HALT",
            ),
        )

        return BytecodeProgram(
            instructions=instructions,
            source_hash=source_hash,
            prepared_source=prepared,
            statement_count=len(
                program.statements
            ),
            flow_names=tuple(
                flows.names()
            ),
            system_names=tuple(
                systems.names()
            ),
            base_names=tuple(
                bases.names()
            ),
            optimized=False,
        )
