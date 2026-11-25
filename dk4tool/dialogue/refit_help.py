"""Compile unpositioned Refit help for the captured original 168x84 painter."""

import textwrap

PROFILE = 'refit-help-168x84-pending-flush-v1'


def compile_paragraph(text):
    if not text or not text.isascii() or text != ' '.join(text.split()) or any(c in text for c in '{}%'):
        raise ValueError('Refit help requires one natural ASCII paragraph without controls or placeholders')
    lines = textwrap.wrap(text, width=27, break_long_words=False, break_on_hyphens=False)
    if not 1 <= len(lines) <= 5 or any(len(line) > 27 for line in lines):
        raise ValueError('Complete Refit paragraph exceeds the native five-row help surface')
    if ' '.join(lines) != text:
        raise ValueError('Refit wrapping changes the authored prose')
    compiled = bytearray()
    for index, line in enumerate(lines):
        compiled.extend(line.encode('ascii'))
        if index < len(lines) - 1:
            if len(line) % 2:
                compiled.extend(b' ')
            compiled.extend(b'\n')
    if any(len(line) % 2 for line in compiled.split(b'\n')[:-1]):
        raise ValueError('Pending font pair crosses a generated line break')
    return bytes(compiled) + b'\0', lines
