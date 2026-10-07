import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.leather",
            *args,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_lexer_error():
    path = ROOT / "examples" / "_m3_bad_lexer.lth"

    path.write_text(
        'price = 150.5 @\n',
        encoding="utf-8",
    )

    try:
        result = run_cli(
            str(path),
        )

        assert result.returncode == 1
        assert "LTH Error [lexer]" in result.stderr
        assert "Traceback" not in result.stderr

    finally:
        path.unlink(missing_ok=True)


def test_semantic_error():
    path = ROOT / "examples" / "_m3_bad_semantic.lth"

    path.write_text(
        "price = 150.5\n"
        "rule discount when customer.vip -> "
        "unknown *= 0.9\n",
        encoding="utf-8",
    )

    try:
        result = run_cli(
            str(path),
        )

        assert result.returncode == 1
        assert "LTH Error [semantic]" in result.stderr
        assert "unknown value 'unknown'" in result.stderr
        assert "Traceback" not in result.stderr

    finally:
        path.unlink(missing_ok=True)


def test_context_error():
    source_path = (
        ROOT / "examples" / "_m3_context.lth"
    )
    context_path = (
        ROOT / "examples" / "_m3_context.json"
    )

    source_path.write_text(
        "price = 150.5\n",
        encoding="utf-8",
    )

    context_path.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    try:
        result = run_cli(
            str(source_path),
            "--context",
            str(context_path),
        )

        assert result.returncode == 1
        assert "LTH Error [input]" in result.stderr
        assert "invalid JSON context" in result.stderr
        assert "Traceback" not in result.stderr

    finally:
        source_path.unlink(missing_ok=True)
        context_path.unlink(missing_ok=True)


def test_runtime_error():
    source_path = (
        ROOT / "examples" / "_m3_runtime.lth"
    )
    context_path = (
        ROOT / "examples" / "_m3_runtime.json"
    )

    source_path.write_text(
        'name = "Leather"\n'
        "rule bad when customer.vip -> "
        "name *= 0.9\n",
        encoding="utf-8",
    )

    context_path.write_text(
        json.dumps(
            {
                "customer": {
                    "vip": True,
                }
            }
        ),
        encoding="utf-8",
    )

    try:
        result = run_cli(
            str(source_path),
            "--context",
            str(context_path),
        )

        assert result.returncode == 1
        assert "LTH Error [runtime]" in result.stderr
        assert "Traceback" not in result.stderr

    finally:
        source_path.unlink(missing_ok=True)
        context_path.unlink(missing_ok=True)


if __name__ == "__main__":
    test_lexer_error()
    test_semantic_error()
    test_context_error()
    test_runtime_error()
    print("LTH 0.2 ERROR INTEGRATION TEST: PASS")
