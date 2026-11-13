"""Two faithful inspection system statuses after the full V1563 stack."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspection_status_native_plan_v1573 import plan,compiled,IDS,SOURCE_COMMON,SOURCE_ARM
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/inspection_status_editorial_release_v1.json'

def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])

def apply_release(common,arm,path):
    config=read(path)
    assert config['format']=='dk4-inspection-status-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    doc=read(config['manuscript']);validate_natural_dialogue_batch(doc)
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    assert proof['actual_changed_message_IDs']==[306,307]
    assert proof['all3666_unselected_texts_and_native_copy_spans_preserved'] and proof['all40_other_blocks_and_opaque_duel_prefix_exact']
    assert not proof['runtime_plan']['patches'] and proof['runtime_plan']['no_native_code_or_selector_membership_change']
    assert proof['shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    fonts,copies,visual=[read(doc[k]) for k in ['native_font_proof','native_copy_proof','visual_review']]
    assert fonts['manuscript_sha256']==doc['reviewed_research_manuscript_sha256'] and len(fonts['cases'])==2
    assert len(fonts['invalid_compiler_inputs_rejected'])==12 and copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies])
    assert [r['message_ID'] for r in fonts['cases']]==list(IDS)
    for case,row in zip(fonts['cases'],doc['records'],strict=True):
        assert case['compiled_hex']==compiled(row).hex()==case['native_pipeline']['formatted_hex']==case['native_pipeline']['loaded_template_hex']
        assert case['full228x64_native_and_independent_font_equal'] and case['complete_first_final_letters_single_line_bounds_and_blank_paper_pass']
    assert visual['both_native_panels_actually_viewed'] and visual['remaining_layout_findings']==0
    return c,a,proof
