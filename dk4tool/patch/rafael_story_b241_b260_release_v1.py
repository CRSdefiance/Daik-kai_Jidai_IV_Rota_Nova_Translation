"""Qualify the reviewed B241–B260 dialogue append over Rafael3222."""
import inspect

from dk4tool.patch import rafael_story_b221_b240_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


evidence_source = checked_text(inspect.getsource(previous.qualify_evidence), {
    '(270, 221, 49)': '(292, 244, 48)',
    "len(names['records']) == 26": "len(names['records']) == 20",
    'all 26 public name and role decisions': 'all 20 public name and role decisions',
    "conf['native_pages'] == 279": "conf['native_pages'] == 294",
    "conf['relative_cases'] == 170": "conf['relative_cases'] == 120",
    "conf['speech_count'] == 263": "conf['speech_count'] == 286",
    "conf['style_count'] == 29": "conf['style_count'] == 14",
    "len(styles['objects']) == 4 and styles['native_target_slot_cases'] == 32":
        "len(styles['objects']) == 2 and styles['native_target_slot_cases'] == 16",
    "for row in styles['compiler_negatives']) == 36": "for row in styles['compiler_negatives']) == 18",
    "sum(row['kind']=='system-FE' for row in speech) == 3": "sum(row['kind']=='system-FE' for row in speech) == 7",
    '(343,38,648)': '(343,36,650)',
    "conf['typed_choice_count'] == 7": "conf['typed_choice_count'] == 6",
    '(33202,2,86,94,7,177)': '(48003,3,132,135,6,154)',
    'all_four_complete_style_commands_observed_under_unmodified_default_roles':
        'both_complete_style_commands_observed_under_unmodified_default_roles',
})
source = checked_text(previous.source, {"len(styles['objects']) == 4": "len(styles['objects']) == 2"})
evidence_env = {**vars(previous), '__file__': __file__}
exec(compile(evidence_source, __file__ + '::current-sealed-research-scope', 'exec'), evidence_env)
qualify_evidence = evidence_env['qualify_evidence']
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(source, __file__ + '::complete-source-owned-dialogue-transaction', 'exec'), env)
plan_release = env['plan_release']
