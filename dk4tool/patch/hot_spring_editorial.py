"""Source/native-approved hot-spring13 after all current screenshot corrections."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.hot_spring_native_plan_v1615 import plan,compiled,IDS,SOURCE_COMMON,SOURCE_ARM
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/hot_spring_editorial_release_v1.json'

def current_entries(common,arm):
    config=read(CONFIG);assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])

def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-hot-spring-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    doc=read(config['manuscript']);validate_natural_dialogue_batch(doc)
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    assert proof['actual_changed_message_IDs']==[n for n in IDS if n!=2282]
    assert proof['all3656_unselected_or_retained_texts_and_native_copy_spans_preserved'] and proof['all40_other_blocks_and_opaque_duel_prefix_exact']
    assert proof['shared_balance_literal_status_fonts_sections_BSS_cache_arena_ITCM_staged123040_exact']
    fonts,copies,escape,runtime,visual=[read(doc[k]) for k in ['native_font_proof','native_copy_proof','escape_regression_proof','native_runtime_proof','visual_review']]
    assert len(fonts['cases'])==16 and not fonts['findings'] and len(fonts['invalid_compiler_inputs_rejected'])==16
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert len(escape['all13_original_direct_pipeline_cases'])==13 and runtime['native_exact_dispatch_ABI_memory_and_external_reference_proven']
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies,escape])
    assert {c['message_ID'] for c in fonts['cases']}==set(IDS)
    rows={r['message_id']:r for r in doc['records']}
    for case in fonts['cases']:
        assert case['compiled_hex']==compiled(rows[case['message_ID']]).hex()
        assert case['full228x64_native_and_independent_font_exact'] and case['complete_first_final_letters_uniform6px_margins_bounds_and_blank_paper_pass']
    assert visual['all16_native_panels_actually_viewed'] and visual['remaining_layout_findings']==0
    return c,a,proof
