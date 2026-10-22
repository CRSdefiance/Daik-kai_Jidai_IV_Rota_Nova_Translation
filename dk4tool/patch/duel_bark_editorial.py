"""Registered source-reviewed timed duel reactions and bounded static formatter."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_bark_native_plan_v1201 import plan,SOURCE_COMMON,SOURCE_ARM
from scripts.verify_village_wrap_v608 import read

CONFIG='translations/duel_bark_editorial_release_v1.json'


def current_entries(common,arm):
    config=read(CONFIG)
    assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    return owned_entries(common,arm,config['directory_sha256'])


def apply_release(common,arm,path):
    config=read(path);assert config['format']=='dk4-duel-bark-editorial-v1'
    assert sha(common)==config['source_common_sha256']==SOURCE_COMMON and sha(arm)==config['source_arm9_sha256']==SOURCE_ARM
    for name,digest in config['dependencies'].items():assert sha(Path(name).read_bytes())==digest,name
    doc=read(config['manuscript']);validate_natural_dialogue_batch(doc)
    assert all(all(row['review'].values()) for row in doc['records']) and not doc['formatting_review_pending']
    c,a,proof=plan(common,arm,doc)
    assert sha(c)==config['target_common_sha256'] and sha(a)==config['target_arm9_sha256']
    fonts=read(doc['native_font_proof']);copies=read(doc['native_copy_proof']);escape=read(doc['escape_regression_proof'])
    assert len(fonts['cases'])==36 and len(copies['complete_native_copies'])==92 and len(escape['all13_direct_pipeline_cases'])==13
    assert fonts['COMMON_sha256']==copies['COMMON_sha256']==escape['COMMON_sha256']==sha(c)
    assert fonts['ARM9_sha256']==copies['ARM9_sha256']==escape['ARM9_sha256']==sha(a)
    return c,a,proof
