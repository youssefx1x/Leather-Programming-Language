from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class RustBootstrapResult:
    available: bool
    compiler: str
    version: str


class RustBootstrap:
    """
    Stable Rust bootstrap verifier.

    It verifies the Rust toolchain rather than replacing the existing
    Rust implementation.
    """

    def check(self):
        try:
            result = subprocess.run(
                ["rustc", "--version"],
                capture_output=True,
                text=True,
                check=True,
            )
        except (OSError, subprocess.CalledProcessError):
            return RustBootstrapResult(
                available=False,
                compiler="rustc",
                version="unavailable",
            )

        version = result.stdout.strip()

        return RustBootstrapResult(
            available=True,
            compiler="rustc",
            version=version,
        )

    def verify_source(self, path):
        path = Path(path)

        if not path.exists():
            return False

        return path.suffix == ".rs"
