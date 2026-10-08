from pathlib import Path


class LeatherSourceBridge:
    """
    LTH 1.0 bridge for Leather-authored source.

    This is intentionally a bootstrap bridge:
    it validates and exposes Leather source to the existing
    implementation without pretending that the compiler is
    already self-hosted.
    """

    VERSION = "1.0"

    def load(self, path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix != ".lth":
            raise ValueError("Leather source must use .lth")

        source = path.read_text()

        if not source.strip():
            raise ValueError("Leather source is empty")

        return source

    def contains(self, source, keyword):
        return keyword in source

    def verify_core(self, source):
        required = (
            "value",
            "rule",
            "base",
            "flow",
            "system",
        )

        return {
            name: self.contains(source, name)
            for name in required
        }

    def is_valid_core(self, source):
        return all(self.verify_core(source).values())
