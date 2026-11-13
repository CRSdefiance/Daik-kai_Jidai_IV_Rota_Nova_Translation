"""Generated36-cell Deck work comments with readable technical noun phrases."""

from functools import lru_cache

WIDTH = 36
MAX_LINES = 3
KEEP_TOGETHER = {('spare', 'parts'), ('chinese', 'medicine'),
                 ('medicinal', 'herbs'), ('seasickness', 'medicine')}
WEAK = {'a', 'an', 'and', 'as', 'at', 'but', 'for', 'from', 'gotta', 'i', 'if',
        'in', 'into', 'is', 'it', 'its', "it's", 'keep', 'my', 'of', 'or', 'so',
        'some', 'that', "that's", 'the', 'this', 'to', 'wanna', 'with', 'your'}


def layout(text):
    if not text or not text.isascii() or text != ' '.join(text.split()):
        raise ValueError('One natural ASCII paragraph required;no authored alignment or breaks')
    if any(ord(c) < 32 or ord(c) > 126 for c in text) or any(c in text for c in '%{}'):
        raise ValueError('This source family has no formatting arguments or author controls')
    words = text.split(' ')
    if any(len(w) > WIDTH for w in words):
        raise ValueError('Complete word exceeds the original Deck width')
    @lru_cache(None)
    def solve(start, rows):
        if start == len(words):
            return (0, ()) if rows == 0 else None
        if rows == 0:
            return None
        choices = []
        for end in range(start + 1, len(words) + 1):
            line = ' '.join(words[start:end])
            if len(line) > WIDTH:
                break
            tail = solve(end, rows - 1)
            if tail is None:
                continue
            weak = (end != len(words) and not line.endswith(('.', '!', '?', ';', ':'))
                    and words[end - 1].strip('.,!?;:').lower() in WEAK)
            orphan = end == len(words) and start != 0 and (end - start == 1 or len(line) < 12)
            # Fewest rows first;within that bound,balance readable phrases and
            # favor punctuation boundaries without changing the authored words.
            compound = (end != len(words) and
                        (words[end - 1].strip('.,!?;:').lower(), words[end].strip('.,!?;:').lower()) in KEEP_TOGETHER)
            cost = (WIDTH - len(line)) ** 2 + 2000 * weak + 4000 * orphan + 3000 * compound
            if end != len(words) and line.endswith(('.', '!', '?', '...')):
                cost -= 400
            choices.append((cost + tail[0], (line,) + tail[1]))
        return min(choices) if choices else None
    for count in range(1, MAX_LINES + 1):
        result = solve(0, count)
        if result is not None:
            lines = list(result[1])
            assert ' '.join(lines) == text
            return lines
    raise ValueError('Complete paragraph exceeds the three original Deck rows')


def compiled(row):
    return serialize(layout(row['english']))


def serialize(lines):
    """Machine phase space before LF;no visible continuation indentation."""
    if not lines or len(lines) > MAX_LINES or any(not line or len(line) > WIDTH or not line.isascii() for line in lines):
        raise ValueError('Generated complete native rows required')
    return b'\n'.join((line + (' ' if index < len(lines) - 1 and len(line) % 2 else '')).encode('ascii')
                      for index, line in enumerate(lines))
