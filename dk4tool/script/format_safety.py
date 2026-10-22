"""Source-bound format contracts for final English story records."""

import re

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.scan.sjis_scan import contains_japanese

PRINTF = re.compile(rb'%(?:%|[-+ #0]*[0-9]*(?:\.[0-9]+)?(?:hh|ll|[hljztL])?[diouxXeEfFgGaAcspn])')


def percent_commands(raw: bytes) -> tuple[list[bytes], list[int]]:
    commands, invalid, at = [], [], 0
    while (position := raw.find(b'%', at)) >= 0:
        match = PRINTF.match(raw, position)
        if match:
            commands.append(match.group())
            at = match.end()
        else:
            invalid.append(position)
            at = position + 1
    return commands, invalid


def story_percent_findings(source: bytes, current: bytes) -> list[dict]:
    """Reject new argument reads even when the new command is valid C syntax.

    An unchanged source-leading 25 is a story presentation state. It is not a
    format command. Other executable/binary records are not interpreted as prose.
    This guard detects introduced commands; it is not a translation fidelity audit.
    """
    before, after = IlnkContainer.parse(source), IlnkContainer.parse(current)
    if len(before.blocks) != len(after.blocks):
        raise ValueError('Story format guard requires the original ILNK block identities')
    findings = []
    for block, data in enumerate(after.blocks):
        original = before.blocks[block].split(b'\0')
        for segment, raw in enumerate(data.split(b'\0')):
            old = original[segment] if segment < len(original) else b''
            if raw == old or b'%' not in raw:
                continue
            # The exception is source-bound and confined to byte zero.
            speaker25 = old.startswith(b'%') and raw.startswith(b'%')
            body, source_body = (raw[1:], old[1:]) if speaker25 else (raw, old)
            if b'%' not in body:
                continue
            try:
                decoded = body.decode('cp932')
            except UnicodeDecodeError:
                continue
            if contains_japanese(decoded) or not re.search(r'[A-Za-z]{3}', decoded):
                continue
            wanted, _ = percent_commands(source_body)
            actual, invalid = percent_commands(body)
            if actual != wanted or invalid:
                findings.append({'block': block, 'record': segment,
                    'id': f'DK4_MES_B{block:02d}_R{segment:04d}',
                    'source_percent_commands': [p.decode('ascii') for p in wanted],
                    'current_percent_commands': [p.decode('ascii') for p in actual],
                    'invalid_offsets': invalid, 'source_leading25_preserved': speaker25})
    return findings


def reject_story_percent_commands(source_files: dict[str, bytes], current_files: dict[str, bytes]) -> dict:
    counts, findings = {}, []
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        rows = story_percent_findings(source_files[path], current_files[path])
        counts[path] = len(rows)
        findings.extend(dict(row, file_path=path) for row in rows)
    if findings:
        raise ValueError(f'Introduced or invalid story printf commands: {findings}')
    return {'all_four_final_story_archives_checked': True, 'source_bound_new_command_counts': counts,
            'leading_source25_state_exception_is_byte_zero_only': True}
