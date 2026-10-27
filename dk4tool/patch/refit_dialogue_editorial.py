"""Late source-locked Refit dialogue and exact existing-allocation runtime."""

import struct
from pathlib import Path
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.refit_help_editorial import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts import refit_dialogue_runtime_v833 as runtime
from scripts.prepare_item_common_v788 import repack
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.verify_village_wrap_v608 import read

IDS = tuple(range(1256, 1268))
SOURCE_COMMON = '8a5b11e9149de02fcebd5b2526af865facf4b3de94d42d6f826927899b7bafd6'
SOURCE_ARM = runtime.SOURCE
CONFIG = 'translations/refit_dialogue_editorial_release_v1.json'


def compiled(row):
    i, text = row['message_id'], row['english']
    if i not in IDS or not text or text != ' '.join(text.split()) or not text.isascii():
        raise ValueError('One reviewed natural ASCII paragraph required')
    if any(ord(c) < 32 or ord(c) >= 127 or c in '{}' for c in text):
        raise ValueError('No authored controls or line positioning allowed')
    expected = 1 if i in (1263, 1267) else 0
    rest = text.replace('%s', '')
    if text.count('%s') != expected or ('%' in rest.replace('%%', '') if i == 1263 else '%' in rest):
        raise ValueError('Exact source argument/percent contract required')
    if i == 1263 and rest.count('%%') != 1:
        raise ValueError('Exactly one COMMON literal percent required')
    if len(text) >= 235 or any(t in text for t in ('FI', 'FA', 'FO', 'FU', 'IC')):
        raise ValueError('Literal Refit paragraph violates its bounded source contract')
    return b' ' + text.encode('ascii')


def plan(common, arm, doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    assert doc['current_COMMON_sha256'] == SOURCE_COMMON and doc['current_ARM9_sha256'] == SOURCE_ARM
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    jp = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    before = previous_entries(common, arm)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex'] == jp[n].text.hex()
        assert row['canonical_source_hex'] == accepted[n].text.hex()
        assert row['current_text_hex'] == before[n].text.hex()
        authored[n] = compiled(row)
    scoped = SimpleNamespace(common_message_entries=lambda c, a, clean=False: previous_entries(c, a))
    pack = FunctionType(repack.__code__, {**repack.__globals__, 'parser': scoped})
    before, blocks, first, last, selected, opaque, groups, attempts = pack(common, arm, authored)
    patched, runtime_proof = runtime.apply(arm)
    target, rebuilt, fields = bytearray(patched), list(blocks), []
    for block, (group, body) in zip(range(first, last + 1), groups, strict=True):
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET + n * 2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    directory = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = local_entries(directory)(c, a, clean=False)
    assert len(before) == len(after) == 3668
    assert all(b.text == authored.get(e.message_id, e.text) for e, b in zip(before, after, strict=True))
    assert all(blocks[n] == rebuilt[n] for n in range(41) if not first <= n <= last)
    for n, payload in opaque.items():
        e = after[n]
        assert rebuilt[e.block][e.block_offset:e.copy_end] == payload
    assert all(before[n].text == after[n].text for n in (64, 292, 346, 347, 348, 676, 677))
    restored = bytearray(a)
    for at, size in fields:
        restored[at:at + size] = patched[at:at + size]
    assert bytes(restored) == patched and cache_plan(a) == cache_plan(arm)
    old, new = MainCodeFile(arm, 0x02000000), MainCodeFile(a, 0x02000000)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in old.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in new.sections]
    assert old.sections[3].data == new.sections[3].data and len(new.sections[3].data) - 48 == 123040
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS],
                  'metadata_fields': fields, 'directory_sha256': directory,
                  'repacked_block_range': [first, last], 'packing_attempts': attempts,
                  'repacked_native_IDs': [e.message_id for e in selected],
                  'all3656_other_message_strings_exact': True,
                  'opaque_payload_IDs': sorted(opaque), 'all_opaque_payloads_and_unselected_blocks_exact': True,
                  'runtime': runtime_proof, 'all_section_BSS_cache_and123040_staged_bounds_unchanged': True,
                  'experimental': True, 'full_goal_complete': False}


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return local_entries(config['directory_sha256'])(common, arm, clean=False)


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-refit-dialogue-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    doc = read(manuscript)
    draft = Path(doc['reviewed_research_manuscript'])
    assert sha(draft.read_bytes()) == doc['reviewed_research_manuscript_sha256']
    assert [(r['message_id'], r['english'], r['source_meaning']) for r in doc['records']] == [
        (r['message_id'], r['english'], r['source_meaning']) for r in read(draft)['records']]
    native, fonts = read(doc['native_runtime_proof']), read(doc['native_font_proof'])
    assert native['runtime_sha256'] == sha(Path(runtime.__file__).read_bytes())
    assert fonts['manuscript_sha256'] == sha(draft.read_bytes()) and not fonts['visual_review_pending']
    assert fonts['matrix_case_count'] == 525 and len(fonts['complete_native_font_planes']) == 26 and not fonts['findings']
    c, a, proof = plan(common, arm, doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['directory_sha256'] == config['directory_sha256']
    copies = read(config['native_copy_proof'])
    assert copies['COMMON_sha256'] == sha(c) and copies['ARM9_sha256'] == sha(a)
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies']) == 3668
    return c, a, proof
