"""Keep all mixed-scene release guards; qualify this batch's documented source layouts."""
import inspect
from dk4tool.patch import reviewed_scene_batch_v5 as previous
from scripts.check_editorial_compiled_pages_v5 import validate_documented_layouts
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_layouts(doc, layout):
    validate_documented_layouts(doc, layout)
    manuals = []
    for row in doc['records']:
        english = row['english']
        previous.require(not any(t in english for t in ['{LB@', '{ALIGN', '{PAD}', '\n']), 'no byte-positioned or raw layout markup')
        if '{LB}' not in english:
            continue
        raw = bytes.fromhex(row['source_hex'])
        previous.require(raw[1:].decode('cp932') == row['source_Japanese'], 'exact clean structural/dramatic body')
        previous.require(bool(row['manual_break_reason'].strip()) and bool(row['qa_waiver_reason'].strip()), 'individual source-layout reason')
        if row['id'] == 'DK4_MES_B143_R0033':
            previous.require(row['english'] == '...{LB}...{LB}...' and row['source_Japanese'].count('\n') == 2, 'three source waiting beats')
        else:
            previous.require(row['block'] == 142 and row['source_selector'] == 254
                and row['source_Japanese'].startswith('＜異国の少女＞\n')
                and english.startswith('<Foreign Girl>{LB}') and english.count('{LB}') == 1,
                'complete source FE heading, not ordinary manual wrapping')
        manuals.append(row['id'])
    previous.require(len(manuals) == 13, 'exact twelve structural headings and one dramatic wait')
    row = next(r for r in doc['records'] if r['id'] == 'DK4_MES_B142_R0159')
    plan = next(r for r in layout['records'] if r['id'] == row['id'])
    previous.require(row['qa_waivers'] == ['weak-line-ending'] and bool(row['qa_waiver_reason'].strip())
        and plan['lines'][3] == 'with no one to turn to...', 'individual grammatical ending retention')
    warnings = [i for i in plan['unmodified_base_QA']['issues'] if i['severity'] == 'warning']
    previous.require(len(warnings) == 1 and warnings[0]['code'] == 'weak-line-ending', 'unchanged original narrow QA finding')
    resolved = [i for i in plan['base_QA']['issues'] if i.get('reviewed_retention_reason')]
    previous.require(len(resolved) == 1 and resolved[0]['reviewed_retention_reason'] == row['qa_waiver_reason'], 'same recorded retention reason')


source = checked_text(inspect.getsource(previous.plan_release), {
    "'dk4-reviewed-scene-release-v5'": "'dk4-reviewed-scene-release-v6'",
    "    require(all(not any(t in r['english'] for t in ['{LB','{ALIGN','{PAD}','\\n']) for r in doc['records']),'logical prose only')":
    '    qualify_layouts(doc,layout)',
    "actual['representative_progressive_FE_actor0_style_three_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andnormal_F_headers_complete']":
    "actual['representative_progressive_FE_actor0_style_two_choice_pagination_andscene_transition_observed'] and actual['all_required_distinct_display_cases_match']",
    "{p['selected_option'] for p in pixels['menu_samples']}=={0,1,2}": "{p['selected_option'] for p in pixels['menu_samples']}=={0,1}",
    "p['all_three_complete_caption_glyphs_andblank_guards_exact']": "p['all_two_complete_caption_glyphs_andblank_guards_exact']",
    "'three complete controller highlights'": "'both complete controller highlights'",
    "    path=doc['file_path'];":
    """    control=load(conf['source_control'])
    require(control['Japanese_core_message_exactly_same'] and control['final_framebuffers_identical'] and control['no_translation_or_runtime_workaround_applied'],'source-controlled B133 initialized battle limitation')
    require(actual['source_control_sha256']==sha(Path(conf['source_control']).read_bytes()) and actual['source_control_runs']==1 and actual['source_control_extra_frames']==5001,'honest separate Japanese control scope')
    path=doc['file_path'];""",
})
env = {**previous.plan_release.__globals__, 'qualify_layouts': qualify_layouts}
exec(compile(source, __file__ + '::same-scene-guards-source-qualified-layouts-and-two-choice-scope', 'exec'), env)
plan_release = env['plan_release']
