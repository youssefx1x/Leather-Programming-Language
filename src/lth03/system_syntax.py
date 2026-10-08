import re

from .system import SystemError, SystemRegistry


class SystemSyntaxError(SystemError):
    pass


_SYSTEM_HEADER = re.compile(
    r"^\s*system\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)"
    r"\s*\{\s*$"
)

_USE_FLOW = re.compile(
    r"^\s*use\s+flow\s+"
    r"([A-Za-z_][A-Za-z0-9_]*)"
    r"\s*;?\s*$"
)

_RUN_SYSTEM = re.compile(
    r"^\s*run\s+system\s+"
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


def extract_systems(source):
    registry = SystemRegistry()
    output = []

    lines = source.splitlines()
    index = 0

    while index < len(lines):
        match = _SYSTEM_HEADER.match(lines[index])

        if not match:
            output.append(lines[index])
            index += 1
            continue

        name = match.group(1)
        flows = []
        depth = 1
        index += 1

        while index < len(lines):
            current = lines[index]
            next_depth = depth + _brace_delta(current)

            if next_depth == 0:
                break

            stripped = current.strip()

            if stripped and not stripped.startswith("#"):
                use_match = _USE_FLOW.match(current)

                if not use_match:
                    raise SystemSyntaxError(
                        f"invalid system member in "
                        f"'{name}': {stripped}"
                    )

                flows.append(
                    use_match.group(1)
                )

            depth = next_depth
            index += 1

        if index >= len(lines):
            raise SystemSyntaxError(
                f"unterminated system '{name}'"
            )

        try:
            registry.define(
                name,
                flows,
            )
        except SystemError as error:
            raise SystemSyntaxError(
                str(error)
            ) from error

        index += 1
        output.extend(
            [""] * (len(flows) + 2)
        )

    return "\n".join(output), registry


def expand_system_runs(
    source,
    system_registry,
    flow_registry,
):
    lines = []

    for line in source.splitlines():
        match = _RUN_SYSTEM.match(line)

        if match:
            name = match.group(1)

            try:
                expanded = system_registry.expand(
                    name,
                    flow_registry,
                )
            except SystemError as error:
                raise SystemSyntaxError(
                    str(error)
                ) from error

            lines.append(expanded)
        else:
            lines.append(line)

    return "\n".join(lines)
