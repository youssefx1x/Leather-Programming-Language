import re

from .flow import FlowError, FlowRegistry


class FlowSyntaxError(FlowError):
    pass


_FLOW_HEADER = re.compile(
    r"^\s*flow\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)"
    r"\s*\{\s*$"
)

_RUN_FLOW = re.compile(
    r"^\s*run\s+flow\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)"
    r"\s*;?\s*$"
)


def _brace_delta(text):
    delta = 0
    quote = None
    escaped = False

    for ch in text:
        if quote is not None:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue

        if ch in ("'", '"'):
            quote = ch
        elif ch == "{":
            delta += 1
        elif ch == "}":
            delta -= 1

    return delta


def extract_flows(source):
    registry = FlowRegistry()
    output = []

    lines = source.splitlines()
    index = 0

    while index < len(lines):
        match = _FLOW_HEADER.match(lines[index])

        if not match:
            output.append(lines[index])
            index += 1
            continue

        name = match.group(1)
        body = []
        depth = 1
        index += 1

        while index < len(lines):
            current = lines[index]
            depth += _brace_delta(current)

            if depth == 0:
                break

            body.append(current)
            index += 1

        if index >= len(lines):
            raise FlowSyntaxError(
                f"unterminated flow '{name}'"
            )

        try:
            registry.define(
                name,
                "\n".join(body),
            )
        except FlowError as error:
            raise FlowSyntaxError(
                str(error)
            ) from error

        index += 1
        output.extend(
            [""] * (len(body) + 2)
        )

    return "\n".join(output), registry


def expand_flow_runs(source, registry):
    def expand_text(text, stack=()):
        lines = []

        for line in text.splitlines():
            match = _RUN_FLOW.match(line)

            if not match:
                lines.append(line)
                continue

            name = match.group(1)

            if name in stack:
                chain = " -> ".join(
                    (*stack, name)
                )
                raise FlowSyntaxError(
                    f"flow composition cycle: {chain}"
                )

            try:
                expanded = registry.expand(
                    name,
                    stack=stack,
                )
            except FlowError as error:
                raise FlowSyntaxError(
                    str(error)
                ) from error

            lines.append(
                expand_text(
                    expanded,
                    stack=(*stack, name),
                )
            )

        return "\n".join(lines)

    return expand_text(source)
