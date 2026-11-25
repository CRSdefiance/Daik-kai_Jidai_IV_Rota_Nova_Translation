"""Preserve complete mixed-scene guards for ordinary two-choice scene batches."""
import inspect
from dk4tool.patch import reviewed_scene_batch_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_scoped_display(conf, doc, stored):
    names = previous.load(conf['scoped_names'])
    previous.validate_natural_dialogue_batch(names)
    previous.require(names['all_five_gates_pass_in_scoped_context'] and len(names['records']) == conf['scoped_name_count'], 'individual scoped name/term reviews')
    rows = [r for r in stored['records'] if r['complete_stored_native_display'].get('planned_native_row_comparison', {}).get('exact_owned_terminal_alignment_space_andzeroink_flush_row_qualified')]
    previous.require(len(rows) == 1 and rows[0]['id'] == 'DK4_MES_B179_R0047', 'exact qualified terminal alignment case')
    proof = rows[0]['complete_stored_native_display']['planned_native_row_comparison']
    previous.require(proof['qualified_events'] == [dict(kind='ascii', code=32, style=15, x=x, y=24) for x in [0, 6]]
        and proof['complete_reviewed_pixel_plane_exact'] and proof['complete_glyph_row_membership_exact'], 'only two zero-ink terminal events')
    previous.require(proof['diagnostic_sha256'] == previous.sha(previous.Path(proof['diagnostic']).read_bytes()), 'exact terminal event diagnostic')


source = checked_text(inspect.getsource(previous.plan_release), {
    "'dk4-reviewed-scene-release-v5'": "'dk4-reviewed-scene-release-v8'",
    "    require(stored['complete_stored_pages']==visual['pages']==conf['native_pages']":
        "    qualify_scoped_display(conf,doc,stored)\n    require(stored['complete_stored_pages']==visual['pages']==conf['native_pages']",
    "actual['representative_progressive_FE_actor0_style_three_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andnormal_F_headers_complete']":
        "actual['representative_progressive_FE_two_choice_name_pagination_andscene_transition_observed'] and actual['all_target_sampled_paragraphs_andheaders_complete']",
    "{p['selected_option'] for p in pixels['menu_samples']}=={0,1,2}": "{p['selected_option'] for p in pixels['menu_samples']}=={0,1}",
    "p['all_three_complete_caption_glyphs_andblank_guards_exact']": "p['all_two_complete_caption_glyphs_andblank_guards_exact']",
    "'three complete controller highlights'": "'both complete controller highlights'",
})
env = {**previous.plan_release.__globals__, 'qualify_scoped_display': qualify_scoped_display}
exec(compile(source, __file__ + '::same-scene-guards-two-choice-and-exact-terminal-events', 'exec'), env)
plan_release = env['plan_release']
