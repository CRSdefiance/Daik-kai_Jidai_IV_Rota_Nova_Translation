"""Six reviewed powder-fire alerts with one exact bounded selector addition."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.powder_fire_native_plan_v1309 import plan,compiled,SOURCE_COMMON,SOURCE_ARM
from scripts.powder_fire_layout_v1304 import IDS
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/powder_fire_editorial_release_v1.json'


def current_entries(common,arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config = read(path)
    assert config['format'] == 'dk4-powder-fire-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name,digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest,name
    doc = read(config['manuscript'])
    validate_natural_dialogue_batch(doc)
    assert tuple(row['message_id'] for row in doc['records']) == IDS
    assert not doc['formatting_review_pending'] and all(all(row['review'].values()) for row in doc['records'])
    c,a,proof = plan(common,arm,doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    fonts,copies,escape = [read(doc[key]) for key in ['native_font_proof','native_copy_proof','escape_regression_proof']]
    assert len(fonts['cases']) == 8 and fonts['all206_existing_noncaptain_source_selections_and_both_fallback_voices_pass']
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_original_direct_pipeline_cases']) == 13
    assert all(proof['ARM9_sha256'] == sha(a) and proof['COMMON_sha256'] == sha(c) for proof in [fonts,copies,escape])
    rows = {row['message_id']:row for row in doc['records']}
    assert all(case['compiled_hex'] == compiled(rows[case['message_id']]).hex() for case in fonts['cases'])
    visual = read(doc['visual_review'])
    assert visual['all8_voice_panels_and6_unique_messages_visually_reviewed']
    assert visual['zero_missing_letters_uneven_indents_internal_gaps_or_out_of_bounds_pixels']
    scope = read(config['native_scope'])
    assert scope['all524288_native_low_word_cases'] == 524288 and scope['total_cases'] == 529286
    runtime = read(config['runtime_plan'])
    assert runtime['encoded_table_bytes'] == 186 and runtime['owned_table_bytes'] == 188
    for patch in runtime['patches']:
        at = patch['address']-0x02000000
        value = bytes.fromhex(patch['target_hex'])
        assert a[at:at+len(value)] == value
    return c,a,proof
