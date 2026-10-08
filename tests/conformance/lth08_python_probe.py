#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


class LTH08Error(Exception):
    pass


def split_top(text: str):
    out = []
    current = []
    depth = 0
    quote = False
    escape = False

    for ch in text:
        if escape:
            current.append(ch)
            escape = False
            continue

        if quote:
            current.append(ch)
            if ch == "\\":
                escape = True
            elif ch == '"':
                quote = False
            continue

        if ch == '"':
            quote = True
            current.append(ch)
            continue

        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1

        if ch == "," and depth == 0:
            out.append("".join(current).strip())
            current = []
        else:
            current.append(ch)

    tail = "".join(current).strip()
    if tail:
        out.append(tail)

    return out


def parse_value(text: str):
    text = text.strip()

    if text == "None":
        return None

    if text.startswith("Int(") and text.endswith(")"):
        return int(text[4:-1])

    if text.startswith("Float(") and text.endswith(")"):
        return float(text[6:-1])

    if text.startswith("Str(") and text.endswith(")"):
        inner = text[4:-1]
        if len(inner) >= 2 and inner[0] == '"' and inner[-1] == '"':
            return bytes(inner[1:-1], "utf-8").decode("unicode_escape")
        return inner

    if text.startswith("List(") and text.endswith(")"):
        inner = text[5:-1].strip()

        if not (inner.startswith("[") and inner.endswith("]")):
            raise ValueError(text)

        body = inner[1:-1].strip()

        if not body:
            return []

        return [parse_value(item) for item in split_top(body)]

    if text.startswith("Map(") and text.endswith(")"):
        inner = text[4:-1].strip()

        if not (inner.startswith("{") and inner.endswith("}")):
            raise ValueError(text)

        body = inner[1:-1].strip()
        result = {}

        if body:
            for item in split_top(body):
                key, value = item.split(":", 1)
                key = key.strip()

                if key.startswith('"') and key.endswith('"'):
                    key = bytes(
                        key[1:-1],
                        "utf-8",
                    ).decode("unicode_escape")

                result[key] = parse_value(value)

        return result

    raise ValueError(f"unsupported value: {text}")


def truth(value) -> bool:
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        return value != 0

    if isinstance(value, str):
        return bool(value)

    if isinstance(value, (list, dict)):
        return bool(value)

    raise TypeError(type(value).__name__)


def equal(left, right) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right

    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right

    if type(left) is not type(right):
        return False

    return left == right


def floor_div(left: int, right: int) -> int:
    if right == 0:
        raise LTH08Error("division by zero")

    return left // right


def modulo(left: int, right: int) -> int:
    if right == 0:
        raise LTH08Error("modulo by zero")

    return left % right


def evaluate(operation, left, right):
    if operation == "add":
        if isinstance(left, str) and isinstance(right, str):
            return left + right

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right

        raise LTH08Error("unsupported add")

    if operation == "floor_div":
        return floor_div(left, right)

    if operation == "mod":
        return modulo(left, right)

    if operation == "eq":
        return equal(left, right)

    if operation == "truth":
        return truth(left)

    if operation == "and":
        return left if not truth(left) else right

    if operation == "or":
        return left if truth(left) else right

    raise LTH08Error(f"unsupported op: {operation}")


def fmt_float(value: float) -> str:
    if value == 0.0:
        return "0.0"

    if value.is_integer():
        return f"{value:.1f}"

    return format(value, ".17g")


def format_value(value) -> str:
    if value is None:
        return "None"

    if isinstance(value, bool):
        return f"Bool({'true' if value else 'false'})"

    if isinstance(value, int) and not isinstance(value, bool):
        return f"Int({value})"

    if isinstance(value, float):
        return f"Float({fmt_float(value)})"

    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'Str("{escaped}")'

    if isinstance(value, list):
        return "List([" + ",".join(
            format_value(item) for item in value
        ) + "])"

    if isinstance(value, dict):
        items = []

        for key in sorted(value):
            escaped = key.replace("\\", "\\\\").replace('"', '\\"')
            items.append(
                f'"{escaped}":{format_value(value[key])}'
            )

        return "Map({" + ",".join(items) + "})"

    raise TypeError(type(value).__name__)


def load_cases(path: Path):
    rows = []

    for line_no, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        1,
    ):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        fields = raw.split("\t")

        if len(fields) != 6:
            raise SystemExit(
                f"invalid case line {line_no}: expected 6 fields"
            )

        rows.append(fields)

    return rows


def main():
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("tests/conformance/lth08_cases.tsv")
    )

    for case_id, category, operation, left_s, right_s, expected in load_cases(path):
        del category, expected

        left = parse_value(left_s)
        right = None if right_s == "-" else parse_value(right_s)

        try:
            actual = format_value(
                evaluate(operation, left, right)
            )
        except LTH08Error as exc:
            actual = f'Error("{exc}")'

        print(f"{case_id}\t{actual}")


if __name__ == "__main__":
    main()
