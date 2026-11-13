"""Sixteen reviewed sinking reports in the fixed native layout allocations."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.ship_sinking_native_plan_v1330 import plan,compiled,SOURCE_COMMON,SOURCE_ARM,IDS
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/ship_sinking_editorial_release_v1.json'


def current_entries(common,arm):
    config = read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config = read(path)
    assert config['format']=='dk4-ship-sinking-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON
    assert sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes())==digest,name
    doc = read(config['manuscript'])
    validate_natural_dialogue_batch(doc)
    assert tuple(r['message_id'] for r in doc['records'])==IDS
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    c,a,proof = plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    fonts,copies,escape = [read(doc[key]) for key in ['native_font_proof','native_copy_proof','escape_regression_proof']]
    assert len(fonts['cases'])==416 and not fonts['findings']
    assert fonts['all416_complete_native_substitution_macro_wrap_and_font_planes_equal']
    assert fonts['manuscript_sha256']==doc['reviewed_research_manuscript_sha256']
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies,escape])
    rows = {r['message_id']:r for r in doc['records']}
    assert all(case['compiled_hex']==compiled(rows[case['message_id']]).hex() for case in fonts['cases'])
    visual = read(doc['visual_review'])
    assert len(visual['all8_native_sheets_and128_rendered_panels_actually_visually_reviewed'])==8
    assert visual['zero_missing_letters_uneven_indents_internal_gaps_bounds_or_wrap_findings']
    scope = read(config['native_scope'])
    assert scope['all524288_native_low_word_cases']==524288 and scope['total_cases']==529312
    runtime = read(config['runtime_plan'])
    assert runtime['encoded_table_bytes']==runtime['owned_table_bytes']==188
    assert runtime['new_memberships']=={'0x2053db8':[0x79C0],'0x2053f40':[0x7A80]}
    for patch in runtime['patches']:
        at = patch['address']-0x02000000
        value = bytes.fromhex(patch['target_hex'])
        assert a[at:at+len(value)]==value
    return c,a,proof
