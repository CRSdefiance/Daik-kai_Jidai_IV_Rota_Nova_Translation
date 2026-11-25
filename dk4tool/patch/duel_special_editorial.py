"""Source-reviewed special calls in the original static duel widget."""
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_special_native_plan_v1218 import plan, SOURCE_COMMON, SOURCE_ARM
from scripts.verify_village_wrap_v608 import read

CONFIG = 'translations/duel_special_editorial_release_v1.json'


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return owned_entries(common, arm, config['directory_sha256'])


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-duel-special-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    doc = read(config['manuscript'])
    validate_natural_dialogue_batch(doc)
    assert all(all(r['review'].values()) for r in doc['records']) and not doc['formatting_review_pending']
    c, a, proof = plan(common, arm, doc)
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    fonts, copies, escape = (read(doc[k]) for k in ('native_font_proof', 'native_copy_proof', 'escape_regression_proof'))
    assert len(fonts['cases']) == 51 and len(fonts['excluded_cases']) == 49
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert len(escape['all13_direct_pipeline_cases']) == 13
    assert fonts['COMMON_sha256'] == copies['COMMON_sha256'] == escape['COMMON_sha256'] == sha(c)
    assert fonts['ARM9_sha256'] == copies['ARM9_sha256'] == escape['ARM9_sha256'] == sha(a)
    assert read(doc['visual_review'])['all15_special_call_previews_visually_inspected']
    return c, a, proof
