"""Source-locked follow-up paragraphs and exact private contract-table extension."""

from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import tavern_schemes_editorial as previous
from dk4tool.patch import scheme_followup_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read

ROOT = Path('work/analysis/scheme_followup_integration_v778')
IDS = tuple(range(964, 989))
ARGUMENTS = {n: ['town', 'faction'] for n in range(978, 984)}
compile_text = FunctionType(previous.compile_text.__code__, {**previous.__dict__, 'IDS': IDS, 'ARGUMENTS': ARGUMENTS})
plan = FunctionType(previous.plan.__code__, {**previous.__dict__, 'IDS': IDS})


def runtime_transform(arm):
    assert sha(arm) == runtime.SOURCE
    refs = read(ROOT/'current_storage_references.json')
    assert refs['source_ARM9_sha256'] == runtime.SOURCE and not refs['unexpected']
    proof = read(ROOT/'runtime_plan.json')
    assert proof['source_ARM9_sha256'] == runtime.SOURCE
    assert runtime.code() == {r['address']: bytes.fromhex(r['target_hex']) for r in proof['patches']}
    target = bytearray(arm)
    for row in proof['patches']:
        off = row['address'] - 0x02000000
        before, after = bytes.fromhex(row['source_hex']), bytes.fromhex(row['target_hex'])
        assert bytes(target[off:off+len(before)]) == before
        assert len(after) == len(before) <= row['existing_owned_capacity']
        target[off:off+len(after)] = after
    target = bytes(target)
    assert sha(target) == proof['target_ARM9_sha256']
    assert cache_plan(target) == cache_plan(arm) and len(target) == len(arm)
    return target, proof


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert sha(arm) == runtime.SOURCE
    contract = read(manuscript['input_contract'])
    assert contract['six_original_paths_include_Bribe_function_02056998']
    assert contract['editable_company_name_does_not_reach_these_original_scheme_consumers']
    layout = read(manuscript['prospective_layout_proof'])
    assert layout['native_supplied_layouts'] == 13699 and layout['findings_count'] == 0
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert source[n].text.hex() == row['source_hex']
        assert accepted[n].text.hex() == row['canonical_source_hex']
        assert before[n].text.hex() == row['current_text_hex']
        assert source[n].text.count(b'%s') == len(ARGUMENTS.get(n, []))
        authored[n] = compile_text(row)
    patched, proof = runtime_transform(arm)
    c, a, fields, mapping = plan(common, patched, authored)
    after = common_message_entries(c, a, clean=False)
    assert all(y.text == authored.get(x.message_id, x.text) for x, y in zip(before, after, strict=True))
    old, new = [IlnkContainer.parse(v).blocks for v in (common, c)]
    assert all(x == y for i, (x, y) in enumerate(zip(old, new, strict=True)) if i not in range(2, 30))
    for n in (1854, 1865):
        x, y = before[n], after[n]
        assert old[x.block][x.block_offset:x.copy_end] == new[y.block][y.block_offset:y.copy_end]
    restored = bytearray(a)
    for at, size in fields:
        restored[at:at+size] = patched[at:at+size]
    assert bytes(restored) == patched and cache_plan(a) == cache_plan(arm)
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS], 'private_runtime': proof,
                  'metadata_fields': fields, 'complete2697_selection_map': mapping,
                  'all3643_other_strings_and13_other_blocks_exact': True,
                  'opaque1854_1865_complete_native_payloads_exact': True,
                  'experimental': True, 'actual_gameplay_pending': True}


def apply_release(common, arm, path):
    cfg = read(path)
    assert cfg['format'] == 'dk4-scheme-followup-editorial-v1'
    assert sha(common) == cfg['source_common_sha256'] and sha(arm) == cfg['source_arm9_sha256']
    for p, h in cfg['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    manuscript = Path(cfg['manuscript'])
    assert sha(manuscript.read_bytes()) == cfg['manuscript_sha256']
    c, a, proof = transform(common, arm, read(manuscript))
    assert sha(c) == cfg['target_common_sha256'] and sha(a) == cfg['target_arm9_sha256']
    return c, a, proof
