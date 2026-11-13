"""Scoped full-width generated layout for the source-reviewed sailor question.

The historical compiler and all executable wrapping filters remain unchanged.
This consumer does not dynamically wrap657; the host generates native-safe
breaks from one editable paragraph. A complete-word soft wrap after For is
reviewed here, rather than narrowing every row to avoid that one boundary.
"""
from dk4tool.dialogue.layout import format_markup
from dk4tool.patch.shop_business_editorial import PROFILE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.rom.nds import NdsImage
from pathlib import Path
import json


PARAGRAPH = "You're a sailor, aren't you? For bulk trade, try the trade house."


def compile_657(english):
    if english.removesuffix('{PAD}') != PARAGRAPH:
        raise ValueError('This scoped formatting correction preserves the reviewed657 wording')
    lines = format_markup(PARAGRAPH, PROFILE).split('{LB}')
    if lines != ["You're a sailor, aren't you? For", 'bulk trade, try the trade house.']:
        raise ValueError('The source-bound full-width layout changed; native review required')
    result = bytearray(b'  ')
    phase = 0
    for index, line in enumerate(lines):
        if len(line) > (35 if index == len(lines) - 1 else 34):
            raise ValueError('Native guarded width exceeded')
        result.extend(line.encode('ascii'))
        phase = (phase + len(line)) & 1
        if index < len(lines) - 1:
            if phase:
                result.extend(b' ')
                phase = 0
            result.extend(b'\n  ')
    return bytes(result), lines


def propose(common, arm, config):
    if sha(common) != config['source_COMMON_sha256'] or sha(arm) != config['source_ARM9_sha256']:
        raise ValueError('Exact cumulative COMMON and runtime required')
    doc = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(doc)
    if doc['translation_policy'] != 'natural-dialogue-v2' or len(doc['records']) != 1:
        raise ValueError('One individually reviewed natural-dialogue-v2 record required')
    row = doc['records'][0]
    if row['message_id'] != 657 or row['editorial_decision'] != 'retain-wording-reflow':
        raise ValueError('This layer only owns657 formatting')
    if not row['fresh_retained_wording_justification'] or not row['native_soft_wrap_reason']:
        raise ValueError('Wording retention and full-width soft-wrap decision must be justified')
    entries = owned_entries(common, arm, config['directory_sha256'])
    old = entries[657]
    if old.text.hex() != row['current_hex'] or old.text.hex() != config['source_text_hex']:
        raise ValueError('Current message source lock failed')
    clean = NdsImage.open('work/clean.nds')
    if sha(Path('work/clean.nds').read_bytes()) != doc['source_ROM_sha256']:
        raise ValueError('Clean Japanese source lock failed')
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))[657]
    if jp.text.hex() != row['source_hex']:
        raise ValueError('Japanese source changed')
    for key, entry in [('source_reference', jp), ('current_reference', old)]:
        if any(row[key][k] != v for k,v in dict(block=entry.block, offset=entry.block_offset,
                copy_end=entry.copy_end, bytes=len(entry.text), record_index=entry.record_index,
                table_offset=entry.table_offset, start_in_record=entry.start).items()):
            raise ValueError('Exact source/current reference changed')
    raw, lines = compile_657(row['english'])
    if b' '.join(old.text.split()) != PARAGRAPH.encode('ascii'):
        raise ValueError('Reflow must preserve every prose word')
    # Preserve the original NUL position, following native selection and table.
    # Three generated terminal spaces fit the final row's original35-cell budget.
    padding = len(old.text) - len(raw)
    if padding != 3 or len(lines[-1]) + padding > 35:
        raise ValueError('Allocation padding no longer fits the reviewed final row')
    target = raw + b' ' * padding
    if target.hex() != row['proposed_compiled_hex'] or target.hex() != config['target_text_hex']:
        raise ValueError('Native-reviewed target bytes changed')
    source = IlnkContainer.parse(common)
    blocks = list(source.blocks)
    body = bytearray(blocks[old.block])
    if body[old.block_offset:old.block_offset + len(old.text) + 1] != old.text + b'\0':
        raise ValueError('Native NUL ownership changed')
    body[old.block_offset:old.block_offset + len(target)] = target
    blocks[old.block] = bytes(body)
    result = IlnkContainer(blocks).to_bytes()
    after = owned_entries(result, arm, config['directory_sha256'])
    if len(result) != len(common) or sha(result) != config['target_COMMON_sha256']:
        raise ValueError('Reconstructed COMMON target mismatch')
    for a,b in zip(entries, after, strict=True):
        if (a.message_id,a.block,a.block_offset,a.copy_end,a.record_index,a.start,a.end) != (b.message_id,b.block,b.block_offset,b.copy_end,b.record_index,b.start,b.end):
            raise ValueError('Native message boundary moved')
        if b.text != (target if a.message_id == 657 else a.text):
            raise ValueError('An unselected message changed')
    if any(a != b for n,(a,b) in enumerate(zip(source.blocks, blocks, strict=True)) if n != old.block):
        raise ValueError('An unselected block changed')
    return result, dict(message_ID=657, lines=lines, generated_terminal_spaces=padding,
        all3668_native_boundaries_and_unselected_payloads_exact=True,
        ARM9_fonts_controls_geometry_substitutions_and_graphics_unchanged=True,
        changed_records=[{'id':'COMMON_MESSAGE_657'}], manuscript=config['manuscript'])


def apply_release(candidate, baseline, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-shop657-full-width-reflow-v1':
        raise ValueError('Wrong release config format')
    for name, digest in config['dependencies'].items():
        if sha(Path(name).read_bytes()) != digest:
            raise ValueError('Reviewed dependency changed: ' + name)
    if sha(baseline.read_file('/COMMON/MESFILE.DK4')) != config['canonical_COMMON_sha256']:
        raise ValueError('Canonical baseline changed')
    result, report = propose(candidate.read_file('/COMMON/MESFILE.DK4'), candidate.read_file('/__arm9__.bin'), config)
    # The sole mutation occurs after every source, dependency and target check.
    candidate.replace_file('/COMMON/MESFILE.DK4', result)
    return report
