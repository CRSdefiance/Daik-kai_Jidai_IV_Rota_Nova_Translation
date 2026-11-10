"""Reuse complete scene integration with explicitly scoped mixed-menu gameplay gates."""
import inspect
from dk4tool.patch import reviewed_scene_batch_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_scoped_display(conf, doc, stored):
    names = previous.load(conf['scoped_names'])
    previous.validate_natural_dialogue_batch(names)
    previous.require(names['all_five_gates_pass_in_scoped_context'] and len(names['records']) == conf['scoped_name_count'], 'individual scoped name/term reviews')
    previous.require(not any(r['complete_stored_native_display'].get('planned_native_row_comparison', {}).get('exact_owned_terminal_alignment_space_andzeroink_flush_row_qualified') for r in stored['records']), 'strict FE checks without inherited terminal exceptions')


def qualify_actual(conf, pixels):
    previous.require(pixels['all_required_distinct_display_cases_match'] and not pixels['missing_required_cases'] and not pixels['header_findings'], 'all required native display cases')
    previous.require({k:v['calls'] for k,v in pixels['ordered_linear_scene_sequences'].items()} == conf['required_ordered_calls'], 'exact ordered linear scene calls')
    cases = {(p['block'], p['source_command_offset'], p['selected_option']) for p in pixels['menu_samples']}
    previous.require(cases == {tuple(p) for p in conf['required_actual_menu_cases']}, 'declared complete mixed-menu controller samples')
    previous.require(all(p['all_complete_caption_glyphs_blank_guards_andhighlight_RGB_exact'] for p in pixels['menu_samples']), 'all sampled complete caption planes and highlights')
    branches = pixels['branch_responses']
    previous.require(len(branches) == 2 and branches[0]['responses'] != branches[1]['responses'], 'distinct ordinary three-choice responses')


source = checked_text(inspect.getsource(previous.plan_release), {
    "'dk4-reviewed-scene-release-v5'": "'dk4-reviewed-scene-release-v9'",
    "    require(stored['complete_stored_pages']==visual['pages']==conf['native_pages']":
        "    qualify_scoped_display(conf,doc,stored)\n    require(stored['complete_stored_pages']==visual['pages']==conf['native_pages']",
    "actual['representative_progressive_FE_actor0_style_three_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andnormal_F_headers_complete']":
        "actual['representative_progressive_FE_mixed_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andheaders_complete']",
    "    require({p['selected_option'] for p in pixels['menu_samples']}=={0,1,2} and all(p['all_three_complete_caption_glyphs_andblank_guards_exact'] and p['all_highlight_background_RGB_exact'] for p in pixels['menu_samples']),'three complete controller highlights')":
        "    qualify_actual(conf,pixels)",
})
env = {**previous.plan_release.__globals__, 'qualify_scoped_display':qualify_scoped_display, 'qualify_actual':qualify_actual}
exec(compile(source, __file__ + '::unchanged-complete-scene-guards-scoped-mixed-menu-tests', 'exec'), env)
plan_release = env['plan_release']
