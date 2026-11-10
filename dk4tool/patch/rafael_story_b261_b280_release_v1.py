"""Qualify the next Rafael archive over the complete verified nine-stage release."""
from dk4tool.patch import rafael_story_b241_b260_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


evidence_source = checked_text(previous.evidence_source, {
    '(292, 244, 48)': '(135, 118, 17)',
    "len(names['records']) == 20": "len(names['records']) == 18",
    'all 20 public name and role decisions': 'all 18 public name and role decisions',
    "conf['native_pages'] == 294": "conf['native_pages'] == 131",
    "conf['relative_cases'] == 120": "conf['relative_cases'] == 390",
    "conf['speech_count'] == 286": "conf['speech_count'] == 130",
    "conf['style_count'] == 14": "conf['style_count'] == 16",
    "sum(row['kind']=='system-FE' for row in speech) == 7": "sum(row['kind']=='system-FE' for row in speech) == 17",
    '(343,36,650)': '(343,40,646)',
    "conf['menu_count'] == 3": "conf['menu_count'] == 2",
    "menu['typed_labels']": "sum(len(item['record_IDs']) for item in menu['menus'])",
    "conf['typed_choice_count'] == 6": "conf['typed_choice_count'] == 5",
    "item['versions'][-1]['object_hex']":
        "(proof['versions'] if count==2 else proof['menus'][0]['versions'])[-1]['object_hex']",
    '(48003,3,132,135,6,154)': '(15761,1,42,43,5,88)',
    'all_three_menu_instances_default_cursor_and_following_fixture_speech_observed':
        'all_two_menu_instances_default_cursor_and_following_fixture_speech_observed',
})
evidence_env = {**previous.evidence_env, '__file__': __file__}
exec(compile(evidence_source, __file__ + '::exact-135-record-evidence', 'exec'), evidence_env)
qualify_evidence = evidence_env['qualify_evidence']
env = {**previous.env, 'qualify_evidence': qualify_evidence, '__file__': __file__}
exec(compile(previous.source, __file__ + '::same-native-archive-transaction', 'exec'), env)
plan_release = env['plan_release']
