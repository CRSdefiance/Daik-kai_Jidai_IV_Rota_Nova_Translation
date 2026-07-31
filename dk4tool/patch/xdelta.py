from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class XdeltaError(RuntimeError):
    pass


def _executable() -> str:
    executable = shutil.which("xdelta3")
    if not executable:
        raise XdeltaError("xdelta3 was not found on PATH")
    return executable


def _native_binding():
    try:
        import pyxdelta
    except ImportError as error:
        raise XdeltaError(
            "neither xdelta3 nor pyxdelta was found; install the project dependencies"
        ) from error
    return pyxdelta


def make_xdelta(clean: Path, modified: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    executable = shutil.which("xdelta3")
    if not executable:
        try:
            _native_binding().run(str(clean), str(modified), str(output))
        except Exception as error:
            raise XdeltaError(f"pyxdelta patch creation failed: {error}") from error
        return
    result = subprocess.run(
        [executable, "-f", "-e", "-s", str(clean), str(modified), str(output)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise XdeltaError(result.stderr.strip() or "xdelta3 patch creation failed")


def apply_xdelta(clean: Path, patch: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    executable = shutil.which("xdelta3")
    if not executable:
        try:
            _native_binding().decode(str(clean), str(patch), str(output))
        except Exception as error:
            raise XdeltaError(f"pyxdelta patch application failed: {error}") from error
        return
    result = subprocess.run(
        [executable, "-f", "-d", "-s", str(clean), str(patch), str(output)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        raise XdeltaError(result.stderr.strip() or "xdelta3 patch application failed")
