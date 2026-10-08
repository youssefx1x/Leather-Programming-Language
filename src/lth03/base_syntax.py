import ast
import json
import re

from .base import BaseError, BaseRegistry


class BaseSyntaxError(BaseError):
    pass


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _normalize_literals(text):
    result = []
    quote = None
    escaped = False
    i = 0

    replacements = {
        "true": "True",
        "false": "False",
        "null": "None",
    }

    while i < len(text):
        ch = text[i]

        if quote is not None:
            result.append(ch)

            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None

            i += 1
            continue

        if ch in ("'", '"'):
            quote = ch
            result.append(ch)
            i += 1
            continue

        matched = False

        for word, replacement in replacements.items():
            end = i + len(word)

            if text[i:end] == word:
                left_ok = (
                    i == 0
                    or not (
                        text[i - 1].isalnum()
                        or text[i - 1] == "_"
                    )
                )
                right_ok = (
                    end == len(text)
                    or not (
                        text[end].isalnum()
                        or text[end] == "_"
                    )
                )

                if left_ok and right_ok:
                    result.append(replacement)
                    i = end
                    matched = True
                    break

        if not matched:
            result.append(ch)
            i += 1

    return "".join(result)


def _literal_value(text, filename="<base>"):
    normalized = _normalize_literals(text.strip())

    try:
        return ast.literal_eval(normalized)
    except Exception as error:
        raise BaseSyntaxError(
            f"base values must be literals "
            f"in {filename}: {text.strip()}"
        ) from error


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


def _parse_body(body, name):
    fields = {}

    for raw_line in body.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        if line.endswith(";"):
            line = line[:-1].rstrip()

        if "=" not in line:
            raise BaseSyntaxError(
                f"expected field assignment in base '{name}': "
                f"{line}"
            )

        field_name, expression = line.split("=", 1)
        field_name = field_name.strip()
        expression = expression.strip()

        if not _IDENTIFIER.fullmatch(field_name):
            raise BaseSyntaxError(
                f"invalid field name '{field_name}' "
                f"in base '{name}'"
            )

        if field_name in fields:
            raise BaseSyntaxError(
                f"duplicate field '{field_name}' "
                f"in base '{name}'"
            )

        fields[field_name] = _literal_value(expression)

    return fields


def extract_bases(source):
    registry = BaseRegistry()
    output = []

    lines = source.splitlines()
    index = 0

    header = re.compile(
        r"^\s*base\s+"
        r"([A-Za-z_][A-Za-z0-9_]*)"
        r"(?:\s+extends\s+"
        r"([A-Za-z_][A-Za-z0-9_]*))?"
        r"\s*\{\s*$"
    )

    while index < len(lines):
        line = lines[index]
        match = header.match(line)

        if not match:
            output.append(line)
            index += 1
            continue

        name = match.group(1)
        parent = match.group(2)

        body_lines = []
        depth = 1
        index += 1

        while index < len(lines):
            current = lines[index]
            next_depth = depth + _brace_delta(current)

            if next_depth == 0:
                break

            body_lines.append(current)
            depth = next_depth
            index += 1

        if index >= len(lines):
            raise BaseSyntaxError(
                f"unterminated base '{name}'"
            )

        fields = _parse_body(
            "\n".join(body_lines),
            name,
        )

        try:
            registry.define(
                name,
                fields,
                extends=parent,
            )
        except BaseError as error:
            raise BaseSyntaxError(str(error)) from error

        index += 1

        output.extend(
            [""] * (len(body_lines) + 2)
        )

    try:
        registry.validate()
    except BaseError as error:
        raise BaseSyntaxError(str(error)) from error

    return "\n".join(output), registry


def _find_matching_paren(source, start):
    depth = 0
    quote = None
    escaped = False
    i = start

    while i < len(source):
        ch = source[i]

        if quote is not None:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None

            i += 1
            continue

        if ch in ("'", '"'):
            quote = ch
            i += 1
            continue

        if ch == "#":
            newline = source.find("\n", i)
            if newline == -1:
                return -1
            i = newline + 1
            continue

        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1

            if depth == 0:
                return i

        i += 1

    return -1


def materialize_base_calls(source, registry):
    names = set(registry.names())

    if not names:
        return source

    output = []
    i = 0
    quote = None
    escaped = False

    while i < len(source):
        ch = source[i]

        if quote is not None:
            output.append(ch)

            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None

            i += 1
            continue

        if ch in ("'", '"'):
            quote = ch
            output.append(ch)
            i += 1
            continue

        if ch == "#":
            newline = source.find("\n", i)

            if newline == -1:
                output.append(source[i:])
                break

            output.append(source[i:newline])
            i = newline
            continue

        if ch.isalpha() or ch == "_":
            start = i
            i += 1

            while (
                i < len(source)
                and (
                    source[i].isalnum()
                    or source[i] == "_"
                )
            ):
                i += 1

            name = source[start:i]

            if name not in names:
                output.append(name)
                continue

            whitespace = i

            while (
                whitespace < len(source)
                and source[whitespace].isspace()
            ):
                whitespace += 1

            if (
                whitespace >= len(source)
                or source[whitespace] != "("
            ):
                output.append(name)
                continue

            close = _find_matching_paren(
                source,
                whitespace,
            )

            if close == -1:
                raise BaseSyntaxError(
                    f"unterminated base call '{name}'"
                )

            argument = source[
                whitespace + 1:
                close
            ].strip()

            if not argument:
                overrides = None
            else:
                overrides = _literal_value(argument)

                if not isinstance(overrides, dict):
                    raise BaseSyntaxError(
                        f"base '{name}' constructor "
                        f"expects a map"
                    )

            try:
                instance = registry.instantiate(
                    name,
                    overrides,
                )
            except BaseError as error:
                raise BaseSyntaxError(
                    str(error)
                ) from error

            payload = json.dumps(
                dict(instance),
                separators=(",", ":"),
                ensure_ascii=False,
            )

            # LTH 0.3 map syntax currently expects
            # identifier keys rather than quoted keys.
            payload = re.sub(
                r'"([A-Za-z_][A-Za-z0-9_]*)":',
                lambda match: match.group(1) + ":",
                payload,
            )

            output.append(payload)
            i = close + 1
            continue

        output.append(ch)
        i += 1

    return "".join(output)


def prepare_source(source):
    stripped, registry = extract_bases(source)
    prepared = materialize_base_calls(
        stripped,
        registry,
    )
    return prepared, registry
