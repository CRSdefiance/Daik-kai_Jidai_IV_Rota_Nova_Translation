"""Opt-in layout research for the proven guarded COMMON portrait consumer.

Historical release compilers deliberately remain unchanged. This planner does
not authorize another COMMON consumer or change native geometry, prose or font
metrics. Its output still needs source, native-copy, font and gameplay approval.
"""
from __future__ import annotations

from functools import cache


WEAK_ENDINGS = frozenset({
    'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with',
})


def compile_paragraph(english: str) -> tuple[bytes, list[str]]:
    """Choose complete word boundaries at full capacity, never a narrower view.

    Use the existing 34-cell nonfinal / 35-cell final budgets, two leading guard
    bytes and pre-LF parity repair. Weak endings and tiny final fragments remain
    hard constraints. Minimize rows first, then fill earlier rows in order.
    The final row is allowed to be short after the earlier rows use their width.
    """
    text = english.removesuffix('{PAD}')
    if (not text or not text.isascii() or text != ' '.join(text.split())
            or any(c in text for c in '{}%')
            or any(pair in text for pair in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('Expected one command-free ASCII portrait paragraph')
    words = text.split(' ')

    @cache
    def solve(start: int, row: int):
        if start == len(words):
            return (0, ()), ()
        if row == 4:
            return None
        best = None
        for stop in range(start + 1, len(words) + 1):
            line = ' '.join(words[start:stop])
            final = stop == len(words)
            if len(line) > (35 if final else 34):
                continue
            if not final and words[stop - 1].strip('.,!?;:').lower() in WEAK_ENDINGS:
                continue
            if final and start and len(line) <= 8:
                continue
            tail = solve(stop, row + 1)
            if tail is None:
                continue
            cost = (1 + tail[0][0], (() if final else (34 - len(line),)) + tail[0][1])
            proposal = cost, (line, *tail[1])
            if best is None or cost < best[0]:
                best = proposal
        return best

    plan = solve(0, 0)
    if plan is None:
        raise ValueError('No complete four-row layout within the verified portrait budgets')
    lines = list(plan[1])
    result = bytearray(b'  ')
    phase = 0
    for index, line in enumerate(lines):
        result.extend(line.encode('ascii'))
        phase = (phase + len(line)) & 1
        if index < len(lines) - 1:
            if phase:
                result.extend(b' ')
                phase = 0
            result.extend(b'\n  ')
    return bytes(result), lines
