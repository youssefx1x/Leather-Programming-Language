from pathlib import Path

from src.lth10.selfhost.bridge import LeatherSourceBridge


class LeatherSelfHostExecutor:
    """
    Bootstrap executor for Leather-authored source.

    It delegates parsing/execution to the existing Leather
    implementation instead of creating a second incompatible
    language implementation.
    """

    VERSION = "1.0"

    def __init__(self):
        self.bridge = LeatherSourceBridge()

    def load(self, path):
        return self.bridge.load(path)

    def inspect(self, path):
        source = self.load(path)

        return {
            "version": self.VERSION,
            "valid": self.bridge.is_valid_core(source),
            "constructs": self.bridge.verify_core(source),
            "lines": len(source.splitlines()),
        }

    def execute(self, path):
        """
        Bootstrap execution boundary.

        For this first 1.0 step we return the validated source
        representation. Actual compiler execution remains owned
        by the existing canonical LTH pipeline.
        """
        report = self.inspect(path)

        if not report["valid"]:
            raise ValueError("invalid Leather 1.0 source")

        return report
