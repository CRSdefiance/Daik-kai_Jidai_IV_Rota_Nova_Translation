"""Carry source-bound artwork checks and accepted font/layout invariants across rebasing."""

import hashlib
import json
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_baked_contracts(stack, current_profile, new_batches):
    reference = stack.get('baked_release_contracts')
    if reference is None:
        return None
    path = Path(reference['path'])
    if sha(path.read_bytes()) != reference['sha256']:
        raise ValueError('Accepted baseline preservation contract changed')
    contract = json.loads(path.read_text(encoding='utf-8'))
    if contract['accepted_ROM_sha256'] != stack['canonical_baseline']['sha256']:
        raise ValueError('Accepted font contract belongs to a different canonical baseline')
    source_path = Path(contract['construction_source']['path'])
    if sha(source_path.read_bytes()) != contract['construction_source']['sha256']:
        raise ValueError('Historical artwork construction reference changed')
    batches = []
    seen = set()
    for row in contract['baked_batches']:
        batch = Path(row['path'])
        if sha(batch.read_bytes()) != row['sha256']:
            raise ValueError('Baked preservation input changed: ' + str(batch))
        key = batch.as_posix().casefold()
        if key not in seen:
            batches.append(batch)
            seen.add(key)
    for batch in new_batches:
        key = batch.as_posix().casefold()
        if key not in seen:
            batches.append(batch)
            seen.add(key)
    return dict(contract=contract, source=NdsImage.open(source_path), batches=batches,
        profile={**contract['baked_profile'], **current_profile},
        report=dict(path=str(path), sha256=reference['sha256'],
            source_preservation_reference=str(source_path),
            source_preservation_reference_sha256=contract['construction_source']['sha256'],
            baked_batches_not_reapplied=len(contract['baked_batches'])))


def verify_font_layout(candidate, contract):
    arm = candidate.read_file('/__arm9__.bin')
    actual_font = sha(GameAsciiFont.from_arm9(arm).glyphs)
    if actual_font != contract['font']['sha256']:
        raise ValueError('Accepted improved font or punctuation was overwritten')
    checked = []
    for row in contract['font']['guarded_spans']:
        actual = arm[row['offset']:row['offset'] + row['length']]
        if len(actual) != row['length'] or sha(actual) != row['sha256']:
            raise ValueError('Accepted font offset/spacing code changed: ' + row['name'])
        checked.append(row['name'])
    return dict(applicable=True, accepted_font_sha256=actual_font,
        drawing_offset_y=1, ASCII_advance=6, biography_pitch=12, dialogue_pitch=16,
        protected_code_and_helper_spans=checked, accepted_font_and_offset_and_line_spacing_preserved=True)
