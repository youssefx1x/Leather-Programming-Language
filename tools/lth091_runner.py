#!/usr/bin/env python3

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.lth091.runner import LeatherRunner


def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/lth091_runner.py <file.lth>")
        return 2

    runner = LeatherRunner()
    report = runner.run_file(sys.argv[1])

    print("========================================")
    print("LTH 0.9.1 RUNNER")
    print(f"VERSION: {runner.version()}")
    print(f"SUCCESS: {report.success}")
    print(f"OUTPUT: {report.output}")
    print(f"TIME_NS: {report.elapsed_ns}")
    print("========================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
