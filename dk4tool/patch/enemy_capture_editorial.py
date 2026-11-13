"""Source-locked capture prose and exact caller name protection after V1404."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.enemy_capture_native_plan_v1423 import plan,compiled,IDS,SOURCE_COMMON,SOURCE_ARM
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/enemy_capture_editorial_release_v1.json'

def current_entries(common,arm):
    config = read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])

def apply_release(common,arm,path):
    config = read(path)
    assert config['format']=='dk4-enemy-capture-editorial-v1'
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
    assert proof['actual_changed_message_IDs']==list(IDS) and proof['all3660_unselected_texts_and_native_copy_spans_preserved']
    assert proof['all_other_code_fonts_sections_BSS_cache_arena_ITCM_and123040_staged_bytes_exact']
    assert proof['runtime_plan']['owned_table_bytes']==188 and proof['runtime_plan']['owned_gate_bytes']==172
    fonts,copies,escape,runtime,visual = [read(doc[k]) for k in
        ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']]
    assert len(fonts['cases'])==208 and len(fonts['all206_source_existing_actor_choices'])==206 and not fonts['findings']
    assert fonts['all208_original_selection_printf_macro_wrap_full_font_planes_verified']
    assert len(fonts['invalid_compiler_inputs_rejected'])==15
    assert fonts['manuscript_sha256']==doc['reviewed_research_manuscript_sha256']
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies,escape])
    assert runtime['source_ARM9_sha256']==SOURCE_ARM and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    runtime_plan = read('work/analysis/enemy_capture_runtime_v1418/runtime_plan.json')
    assert runtime_plan['patches']==proof['runtime_plan']['patches']
    assert read('work/analysis/enemy_capture_runtime_v1418/scope_proof.json')['total_cases']==529325
    authored = {r['message_id']:compiled(r).hex() for r in doc['records']}
    assert all(case['compiled_hex']==authored[case['message_ID']] for case in fonts['cases'])
    assert visual['all8_sheets_and64_native_panels_actually_visually_reviewed']
    assert visual['all208_native_fonts_margins_bounds_first_final_letters_and_blank_paper_pass']
    assert visual['no_shared_BALANCE_or_literal_or_live_status_tail_change']
    assert visual['only_source_owned188_byte_selector_and172_byte_gate_runtime_spans_changed']
    return c,a,proof
