"""Restore source-verified tutorial selectors and format for their modal consumer."""

import json
import textwrap
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha

PATH = '/data/SC0.DK4'
TARGETS = {(45, 52), *((46, i) for i in (51, 54, 58, 62, 65, 68, 72, 76, 80, 83, 87, 91))}


def encode_panel(english, allocation, *, structured_rows=None):
    """Use the verified two-space modal continuation format for these repairs."""
    if not english.isascii() or '%' in english or '\n' in english:
        raise ValueError('Tutorial prose must be a printable English paragraph without printf tokens')
    if structured_rows:
        rows = structured_rows
        if ' '.join(rows) != english:
            raise ValueError('Structured panel rows change the reviewed prose')
    else:
        rows = textwrap.wrap(english, width=34, break_long_words=False, break_on_hyphens=False)
    if not rows or len(rows) > 5 or any(len(row.replace('FO', 'Castor Co.')) > 34 for row in rows):
        raise ValueError('Tutorial exceeds verified modal row bounds')
    body = b'\xfe' + '\n  '.join(rows).encode('ascii')
    if len(body) > allocation:
        raise ValueError(f'Tutorial needs {len(body)} bytes; allocation is {allocation}')
    return body.ljust(allocation, b' ')


def apply_release(source, baseline, clean, config_path, *, require_proof=True):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-raphael-system-panel-release-v1':
        raise ValueError('Wrong tutorial repair format')
    for key, data in (('source_file_sha256', source), ('canonical_file_sha256', baseline),
                      ('clean_file_sha256', clean)):
        if sha(data) != config[key]:
            raise ValueError(f'Tutorial {key} source lock differs')
    current, original, canonical = [IlnkContainer.parse(data) for data in (source, clean, baseline)]
    records = config['records']
    if {(r['block'], r['segment']) for r in records} != TARGETS or len(records) != 13:
        raise ValueError('Tutorial repair must cover exactly the 13 verified damaged panels')
    changed = []
    for record in records:
        block, segment = record['block'], record['segment']
        parts = current.blocks[block].split(b'\0')
        jp = original.blocks[block].split(b'\0')[segment]
        parent = canonical.blocks[block].split(b'\0')[segment]
        old = parts[segment]
        if (jp.hex() != record['clean_hex'] or parent.hex() != record['canonical_hex']
                or old.hex() != record['before_hex'] or not jp.startswith(b'\xfe')
                or not old.startswith(b'\xf8\xf2') or len(old) != len(jp)):
            raise ValueError(f'B{block} R{segment}: tutorial command/allocation source differs')
        if record.get('translation_policy') != 'natural-dialogue-v2' or not all(
                record['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness', 'formatting')):
            raise ValueError('Tutorial source/localization/formatting review incomplete')
        new = encode_panel(record['english'], len(jp), structured_rows=record.get('structured_rows'))
        if new.hex() != record['after_hex']:
            raise ValueError('Tutorial encoding differs from reviewed bytes')
        parts[segment] = new
        current.blocks[block] = b'\0'.join(parts)
        changed.append(f'DK4_MES_B{block:02d}_R{segment:04d}')
    saved = current.to_bytes()
    if sha(saved) != config['target_file_sha256'] or len(saved) != len(source):
        raise ValueError('Tutorial repair target/size differs')
    if require_proof:
        proof_path = Path(config['native_proof'])
        if sha(proof_path.read_bytes()) != config['native_proof_sha256']:
            raise ValueError('Tutorial native evidence changed')
        proof = json.loads(proof_path.read_text(encoding='utf-8'))
        if proof['verified_records'] != changed or len(proof['cases']) != 26 or not proof['all_glyphs_and_pixels_preserved']:
            raise ValueError('Tutorial native evidence incomplete')
        audit_path = Path(config['all_route_native_audit'])
        if sha(audit_path.read_bytes()) != config['all_route_native_audit_sha256']:
            raise ValueError('All-route system-panel audit changed')
        audit = json.loads(audit_path.read_text(encoding='utf-8'))
        if (audit['failures'] or not audit['all_readable_system_notices_pass']
                or len(audit['cases']) != 1061 or len(audit['excluded']) != 8
                or audit['source_files_sha256'][PATH] != sha(saved)):
            raise ValueError('All-route system-panel coverage incomplete')
    return saved, {'changed_records': changed, 'source_file_sha256': sha(source),
                   'target_file_sha256': sha(saved), 'source_FE_selectors_restored': 13,
                   'record_sizes_and_neighbor_commands_preserved': True,
                   'modal_continuation_guard_bytes': 2, 'runtime_verified': False}


def reject_corrupt_panel_selectors(files):
    """Fail releases with the known CP932 re-encoding of the raw FE command."""
    for path in (f'/data/SC{i}.DK4' for i in range(4)):
        for block, data in enumerate(IlnkContainer.parse(files[path]).blocks):
            for segment, record in enumerate(data.split(b'\0')):
                if record.startswith(b'\xf8\xf2'):
                    raise ValueError(f'{path} B{block} R{segment}: FE system selector was decoded as prose')
