"""Run the three pinned Unit B focused suites; no operative authority."""
from pathlib import Path
import subprocess
import sys

unit = Path(__file__).resolve().parents[1] / "qualification/authority-unit-b-v1.3"
command = [sys.executable, "-I", "-B"]
if sys.flags.optimize:
    command.append("-O")
for directory, pattern in (("reference", "test_authority_reference.py"),
                           ("custody", "test_custody.py"),
                           (".", "test_catalog.py")):
    subprocess.run(command + ["-m", "unittest", "discover", "-s", directory,
                              "-p", pattern], cwd=unit, check=True)
