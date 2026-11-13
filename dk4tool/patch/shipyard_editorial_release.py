"""Registered full Shipyard editorial layer with native runtime/copy evidence."""

from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_common import IDS, compile_text, plan
from dk4tool.patch.shipyard_editorial import runtime_transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read

ARGUMENTS = {786: ['native_mast_count', 'native_durability'], 789: ['typed_gold_currency'],
    798: ['native_discount_percent'], 799: ['typed_gold_currency'], 800: ['typed_gold_currency'],
    802: ['typed_gold_currency'], 803: ['literal_ship_name', 'typed_gold_currency', 'typed_preparation_duration'],
    804: ['literal_ship_name', 'typed_gold_currency']}


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    clean, canonical = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    japanese, accepted = [common_message_entries(r.read_file(path), r.read_file('/__arm9__.bin'), clean=(r is clean)) for r in (clean, canonical)]
    before = common_message_entries(common, arm, clean=False)
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert japanese[n].text == bytes.fromhex(row['source_hex'])
        assert accepted[n].text == bytes.fromhex(row['canonical_source_hex'])
        assert before[n].text == bytes.fromhex(row['current_text_hex'])
        assert row['runtime_argument_contract'] == ARGUMENTS.get(n, [])
        authored[n] = compile_text(row)
        assert authored[n].count(b'%s') == japanese[n].text.count(b'%s')
    runtime, runtime_proof = runtime_transform(arm)
    common2, arm2, fields, mapping = plan(common, runtime, authored)
    after = common_message_entries(common2, arm2, clean=False)
    assert all(b.text == authored.get(a.message_id, a.text) for a, b in zip(before, after, strict=True))
    blocks, rebuilt = [IlnkContainer.parse(c).blocks for c in (common, common2)]
    assert all(a == b for k, (a, b) in enumerate(zip(blocks, rebuilt, strict=True)) if k not in range(2, 19))
    restored = bytearray(arm2)
    for at, size in fields:
        restored[at:at + size] = runtime[at:at + size]
    assert bytes(restored) == runtime and cache_plan(arm2) == cache_plan(arm)
    return common2, arm2, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS],
        'owned_runtime': runtime_proof, 'metadata_fields': fields, 'complete1549_selection_map': mapping,
        'all3647_unselected_texts_and24_other_blocks_exact': True,
        'all_sections_pool_cache_startup_allocator_fonts_and_art_no_growth_or_change': True,
        'experimental': True, 'actual_gameplay_pending': True, 'full_goal_complete': False}


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-shipyard-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    for p, digest in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == digest, p
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    c, a, proof = transform(common, arm, read(manuscript))
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    return c, a, proof
