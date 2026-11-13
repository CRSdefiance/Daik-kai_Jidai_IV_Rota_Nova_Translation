"""Source/native-approved Search reports after the complete registered V1637 stack."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.search_reports_native_plan_v1661 import plan, compiled, IDS, PROFILE, SOURCE_COMMON, SOURCE_ARM
from scripts.verify_village_wrap_v608 import read

CONFIG='translations/search_reports_editorial_release_v1.json'


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-search-reports-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    doc=read(config['manuscript']);validate_natural_dialogue_batch(doc)
    assert doc['consumer_layout_profile']==PROFILE
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    assert proof['actual_changed_message_IDs']==list(IDS) and proof['all3657_unselected_texts_and_native_copy_spans_preserved']
    assert proof['all39_other_blocks_and_opaque_duel_prefix_exact']
    assert proof['shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    assert proof['runtime_plan']['encoded_table_bytes']==186 and proof['runtime_plan']['native_gate_bytes']==168
    fonts,copies,escape,runtime,visual=[read(doc[k]) for k in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']]
    assert len(fonts['cases'])==294 and not fonts['findings'] and len(fonts['invalid_compiler_inputs_rejected'])==17
    assert len(fonts['all414_existing_actor_selections'])==414 and fonts['all_original_one_to_four_digit_quantity_width_pairs_tested']
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13 and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies,escape])
    assert visual['all3_sheets38_panels_actually_viewed'] and visual['remaining_layout_findings']==0
    rows={r['message_id']:r for r in doc['records']}
    for case in fonts['cases']:
        assert case['compiled_hex']==compiled(rows[case['message_ID']]).hex()
        assert case['full228x64_native_and_independent_ink_shadow_planes_equal']
        assert case['complete_leading_trailing_letters_source_quantities_margins_bounds_and_blank_paper_verified']
    return c,a,proof
