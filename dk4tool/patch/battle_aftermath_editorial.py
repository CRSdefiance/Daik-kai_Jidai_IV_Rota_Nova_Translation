"""Reviewed aftermath prose and exact fixed-footprint native formatting layer."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import plan, compiled, SOURCE_COMMON, SOURCE_ARM
from scripts.battle_aftermath_layout_v1250 import IDS
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/battle_aftermath_editorial_release_v1.json'


def current_entries(common,arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config = read(path)
    assert config['format'] == 'dk4-battle-aftermath-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name,digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest,name
    doc = read(config['manuscript'])
    validate_natural_dialogue_batch(doc)
    assert all(all(r['review'].values()) for r in doc['records']) and not doc['formatting_review_pending']
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    c,a,proof = plan(common,arm,doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    fonts,copies,escape = (read(doc[k]) for k in ('native_font_proof','native_copy_proof','escape_regression_proof'))
    assert len(fonts['cases']) == 783 and fonts['all114_native_town_names_for_each_of6_templates'] == 684
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_original_direct_pipeline_cases']) == 13
    assert fonts['COMMON_sha256'] == copies['COMMON_sha256'] == escape['COMMON_sha256'] == sha(c)
    assert fonts['ARM9_sha256'] == copies['ARM9_sha256'] == escape['ARM9_sha256'] == sha(a)
    rows = {r['message_id']:r for r in doc['records']}
    assert all(case['compiled_hex'] == compiled(rows[case['message_id']]).hex() for case in fonts['cases'])
    visual = read(doc['visual_review'])
    assert len(visual['all6_review_sheets_actually_visually_inspected']) == 6
    assert visual['all783_complete_native_fonts_pass'] and visual['zero_missing_letters_padding_gaps_or_out_of_bounds_pixels']
    scope = read(config['native_scope'])
    assert scope['total_cases'] == 529273 and scope['all524288_native_low_word_cases'] == 524288
    runtime = read(config['runtime_plan'])
    for patch in runtime['patches']:
        at = patch['address']-0x02000000
        value = bytes.fromhex(patch['target_hex'])
        assert a[at:at+len(value)] == value
    return c,a,proof
