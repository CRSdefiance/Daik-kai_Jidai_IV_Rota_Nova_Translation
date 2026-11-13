"""Qualify the reviewed Rafael archive over the registered Rafael3649 release."""
from dk4tool.patch import rafael_story_b261_b280_release_v1 as previous
from dk4tool.patch import rafael_story_b241_b260_release_v1 as contract
from scripts.source_locked_derivation_v5118 import checked_text


evidence_source = checked_text(previous.evidence_source, {
    '(135, 118, 17)': '(245, 202, 43)',
    "len(names['records']) == 18": "len(names['records']) == 17",
    'all 18 public name and role decisions': 'all 17 public name and role decisions',
    "conf['native_pages'] == 131": "conf['native_pages'] == 248",
    "conf['relative_cases'] == 390": "conf['relative_cases'] == 800",
    "conf['speech_count'] == 130": "conf['speech_count'] == 240",
    "conf['style_count'] == 16": "conf['style_count'] == 76",
    "len(styles['objects']) == 2 and styles['native_target_slot_cases'] == 16":
        "len(styles['objects']) == 11 and styles['native_target_slot_cases'] == 88",
    "for row in styles['compiler_negatives']) == 18": "for row in styles['compiler_negatives']) == 99",
    '(15761,1,42,43,5,88)': '(12881,1,27,31,5,213)',
    'both_complete_style_commands_observed_under_unmodified_default_roles':
        'nine_complete_style_commands_observed_under_unmodified_default_roles',
})
evidence_env = {**previous.evidence_env, '__file__': __file__}
exec(compile(evidence_source, __file__ + '::exact-245-record-evidence', 'exec'), evidence_env)
qualify_evidence = evidence_env['qualify_evidence']
source = checked_text(contract.source, {"len(styles['objects']) == 2": "len(styles['objects']) == 11"})
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__ + '::same-native-archive-transaction', 'exec'), env)
plan_release = env['plan_release']
