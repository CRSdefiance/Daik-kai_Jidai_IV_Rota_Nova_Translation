"""Source-locked one-record precision correction after the full V1344 stack."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.flagship_precision_native_plan_v1356 import plan,compiled,SOURCE_COMMON,SOURCE_ARM,IDS
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/flagship_capture_precision_release_v1.json'


def current_entries(common,arm):
    config = read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config = read(path)
    assert config['format']=='dk4-flagship-capture-precision-v1'
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
    assert proof['all3667_unselected_texts_and_native_copy_spans_preserved']
    assert proof['entire188_byte_selector_and172_byte_gate_and_all_runtime_code_exact']
    fonts,copies,escape = [read(doc[k]) for k in ['native_font_proof','native_copy_proof','escape_regression_proof']]
    assert len(fonts['cases'])==8 and len(fonts['all206_existing_actor_choices'])==206 and not fonts['findings']
    assert fonts['only2015_prose_changed_other4_capture_alternatives_native_bytes_exact']
    assert fonts['manuscript_sha256']==doc['reviewed_research_manuscript_sha256']
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies,escape])
    row = doc['records'][0]
    assert all(case['compiled_hex']==compiled(row).hex() for case in fonts['cases'] if case['message_ID']==2015)
    visual = read(doc['visual_review'])
    assert visual['all8_panels_and5_unique_capture_variants_actually_visually_reviewed']
    assert visual['all_native_fonts_margins_bounds_first_final_letters_pass'] and visual['zero_orphans_weak_endings_or_waivers']
    return c,a,proof
