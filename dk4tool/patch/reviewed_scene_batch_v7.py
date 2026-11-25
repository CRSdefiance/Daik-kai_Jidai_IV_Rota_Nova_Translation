"""Retain complete scene guards with B151–B170 source-owned cinematic formatting."""
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import reviewed_scene_batch_v5 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_source_plans(conf, doc, layout):
    original = load(conf['qualified_compiled_plans'])
    expected = deepcopy(original)
    staged = []
    by_id = {r['id']: r for r in doc['records']}
    for row in expected['records']:
        if row.get('individually_documented_automatic_source_staging'):
            record = by_id[row['id']]
            previous.require(row['block'] == 156 and row['source_selector'] == 254
                and bool(row['cinematic_layout_reason'].strip()), 'individual cinematic staging reason')
            previous.require(bytes.fromhex(row['source_hex'])[1:].decode('cp932') == record['source_Japanese'],
                'complete clean cinematic body')
            previous.require(row['logical_English'] == record['english'], 'unchanged cinematic prose')
            row['English'] = '{SPEAKER:FE}' + row['logical_English']
            staged.append(row['id'])
    previous.require(len(staged) == 23 and staged == conf['source_qualified_cinematic_records'], 'exact cinematic source scope')
    previous.require(layout == expected, 'exact qualified compiled layout; only schema binding added')
    previous.require(len(layout['records']) == 634 and not layout['failures'], 'all speech plans retained')
    previous.require(all(not any(token in r['english'] for token in ['{LB', '{ALIGN', '{PAD}', '\n'])
        for r in doc['records']), 'logical prose remains free of authored formatting')


source = checked_text(inspect.getsource(previous.plan_release), {
    "'dk4-reviewed-scene-release-v5'": "'dk4-reviewed-scene-release-v7'",
    "    require(all(not any(t in r['english'] for t in ['{LB','{ALIGN','{PAD}','\\n']) for r in doc['records']),'logical prose only')":
        '    qualify_source_plans(conf,doc,layout)',
    "actual['representative_progressive_FE_actor0_style_three_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andnormal_F_headers_complete']":
        "actual['representative_progressive_FE_actor0_two_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andheaders_complete']",
    "{p['selected_option'] for p in pixels['menu_samples']}=={0,1,2}": "{p['selected_option'] for p in pixels['menu_samples']}=={0,1}",
    "p['all_three_complete_caption_glyphs_andblank_guards_exact']": "p['all_two_complete_caption_glyphs_andblank_guards_exact']",
    "'three complete controller highlights'": "'both complete controller highlights'",
})
env = {**previous.plan_release.__globals__, 'qualify_source_plans': qualify_source_plans}
exec(compile(source, __file__ + '::unchanged-scene-guards-qualified-source-layout-and-two-choice-scope', 'exec'), env)
plan_release = env['plan_release']
