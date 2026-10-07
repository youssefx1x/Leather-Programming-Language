import argparse
import json
from pathlib import Path

from src.lth03 import LTH03Runner, LTH03Error


def main():
    parser = argparse.ArgumentParser(
        description="Leather 0.3 development runner"
    )

    parser.add_argument("source")
    parser.add_argument("--context")

    args = parser.parse_args()

    source_path = Path(args.source)

    source = source_path.read_text(
        encoding="utf-8"
    )

    context = {}

    if args.context:
        context = json.loads(
            Path(args.context).read_text(
                encoding="utf-8"
            )
        )

    try:
        state = LTH03Runner().run(
            source,
            context=context,
        )
    except LTH03Error as error:
        print(f"LTH 0.3 Error: {error}")
        raise SystemExit(1)

    print("LTH 0.3 RESULT")

    for name, value in state.values.items():
        print(f"  {name} = {value}")


if __name__ == "__main__":
    main()
