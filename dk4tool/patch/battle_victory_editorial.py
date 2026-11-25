"""Source-locked victory prose after the complete registered V1364 stack."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_victory_native_plan_v1396 import plan,compiled,IDS,SOURCE_COMMON,SOURCE_ARM
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/battle_victory_editorial_release_v1.json'


def current_entries(common,arm):
    config = read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config = read(path)
    assert config['format']=='dk4-battle-victory-editorial-v1'
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
    assert proof['actual_changed_message_IDs']==[2136,2137]
    assert proof['all3666_unselected_or_retained_texts_and_native_copy_spans_preserved']
    assert proof['entire188_byte_selector_172_byte_gate_and_all_code_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    fonts,copies,escape = [read(doc[k]) for k in ['native_font_proof','native_copy_proof','escape_regression_proof']]
    assert len(fonts['cases'])==8 and len(fonts['all206_existing_actor_choices'])==206 and not fonts['findings']
    assert fonts['all8_whole_native_font_planes_and_complete_ordered_glyph_events_exact']
    assert len(fonts['invalid_compiler_inputs_rejected'])==14
    assert fonts['manuscript_sha256']==doc['reviewed_research_manuscript_sha256']
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies,escape])
    authored = {r['message_id']:compiled(r).hex() for r in doc['records']}
    assert all(case['compiled_hex']==authored[case['message_ID']] for case in fonts['cases'])
    visual = read(doc['visual_review'])
    assert visual['all8_native_victory_panels_actually_visually_reviewed']
    assert visual['all_native_fonts_margins_bounds_first_final_letters_and_blank_paper_pass']
    assert visual['entire188_byte_selector_and172_byte_gate_explicitly_exact']
    return c,a,proof
