from __future__ import annotations

import re

TOKEN_RE = re.compile(r"\{(?:END|LB|HEX:[0-9A-Fa-f]{2}|WAIT:[0-9A-Fa-f]{2}|VAR:[^{}]+)\}")


def control_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text or "")


def missing_tokens(source: str, replacement: str) -> list[str]:
    remaining = control_tokens(replacement)
    missing: list[str] = []
    for token in control_tokens(source):
        if token in remaining:
            remaining.remove(token)
        else:
            missing.append(token)
    return missing

