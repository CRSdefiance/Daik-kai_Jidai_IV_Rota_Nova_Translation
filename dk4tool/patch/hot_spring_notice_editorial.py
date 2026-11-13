"""One source/native-approved no-argument Experience notice after full V1622."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.hot_spring_notice_plan_v1632 import plan,compiled,SOURCE_COMMON,SOURCE_ARM
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/hot_spring_notice_editorial_release_v1.json'
def current_entries(common,arm):
    config=read(CONFIG);assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])
def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-hot-spring-notice-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    doc=read(config['manuscript']);validate_natural_dialogue_batch(doc)
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    assert proof['actual_changed_message_IDs']==[310] and proof['all3667_unselected_texts_and_native_copy_spans_preserved']
    assert not proof['runtime_plan']['patches'] and proof['runtime_plan']['no_native_code_or_selector_membership_change']
    fonts,copies,visual=[read(doc[k]) for k in ['native_font_proof','native_copy_proof','visual_review']]
    assert len(fonts['cases'])==1 and len(fonts['invalid_compiler_inputs_rejected'])==12
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
    assert all(p['ARM9_sha256']==sha(a) and p['COMMON_sha256']==sha(c) for p in [fonts,copies])
    assert fonts['cases'][0]['compiled_hex']==compiled(doc['records'][0]).hex() and visual['notice_native_panel_actually_viewed'] and visual['remaining_layout_findings']==0
    return c,a,proof
