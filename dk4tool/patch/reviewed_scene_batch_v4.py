"""Qualify source-bound typed scenes with directly observed FE macros and scoped pixels."""
import ast
from pathlib import Path
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from scripts.source_locked_derivation_v5118 import checked_text

tree=ast.parse(Path('dk4tool/patch/reviewed_scene_batch_v3.py').read_text(encoding='utf-8'))
edits=ast.literal_eval(next(n.value.args[1] for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='source' for t in n.targets)))
source=checked_text(Path('dk4tool/patch/reviewed_scene_batch_v2.py').read_text(encoding='utf-8'),edits)
source=checked_text(source,{
    "'dk4-reviewed-scene-release-v3'":"'dk4-reviewed-scene-release-v4'",
    "    require(len(pixels['menu_samples'])==7 and len(pixels['name_headers'])==7 and len(pixels['rejection_pages'])==2, 'focused actual glyph comparisons')\n    for case in pixels['menu_samples']:\n        require(len(case['labels'])==2 and all(c['complete_caption_glyphs_andblank_guards_exact'] and c['background_andhighlight_exact'] for c in case['labels']), 'complete actual typed captions')\n    require({c['visible_selected_option'] for c in pixels['menu_samples']} >= {0,1}, 'both actual ordinary controller highlights')":
    """    require({k:len(pixels[k]) for k in conf['focused_pixel_counts']}==conf['focused_pixel_counts'], 'scoped actual glyph comparisons')
    for case in pixels['menu_samples']:
        require(len(case['labels'])==2 and case['both_complete_caption_glyphs_andblank_guards_exact'] and case['sampled_highlight_RGB_exact'], 'complete actual captions andhonest sampled highlight')
    require({c['selected_option'] for c in pixels['menu_samples']} >= {0,1}, 'both actual ordinary controller selections')
    require(all(p['complete_native_glyph_plane_andblank_guards_equal'] for p in pixels['body_pages']), 'complete actual page pixels')
    require({p['id'] for p in pixels['body_pages'] if p['kind']=='system-FE'}==set(conf['observed_FE_ids']), 'source-bound actual FE membership')
    require(all(next(r for r in speech_rows if r['id']==ident)['source_selector']==254 for ident in conf['observed_FE_ids']), 'actual FE source controls')
    macro_FE={r['id'] for r in speech_rows if r['kind']=='system-FE' and any(r['source_macros'].values())}
    require(macro_FE==set(conf['observed_macro_FE_ids']) and macro_FE<=set(conf['observed_FE_ids']), 'all new macro-bearing FE observed')""",
    "actual['representative_progressive_pagination_menu_name_andscene_transition_observed']":
    "actual['representative_progressive_FE_macros_pagination_menu_name_andscene_transition_observed']",
    "actual['no_new_blank_box_lost_glyph_orportrait_issue_seen_in_reviewed_samples']":
    "visual['no_clipping_orincomplete_glyphs']",
    "actual['no_natural_event_activation_original_location_earned_chronology_fullroute_orhardware_claim']":
    "actual['no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim']",
    "    require(actual['FE_new_batch_bodies_not_observed_in_gameplay'] and actual['FE_distinct_behavior_reference'], 'honest FE behavior reuse')\n    fe_reference=Path(actual['FE_distinct_behavior_reference'])\n    require(sha(fe_reference.read_bytes())==actual['FE_distinct_behavior_reference_sha256'] and load(fe_reference)['representative_progressive_FE_pagination_andscene_transition_observed'], 'bound completed FE gameplay precedent')":
    "    require(actual['all_four_conditional_B91_notices_observed_across_two_unforced_selection_paths'], 'honest observed conditional FE behavior')",
})
exec(compile(source,__file__+'::typed-scene-observed-FE-production','exec'),globals())
