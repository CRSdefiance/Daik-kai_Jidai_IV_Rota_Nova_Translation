"""Retain all original pixel/VM safeguards for only the two changed English captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_final_actual_tools_v7765');assert not root.exists()
    original="""    for number in [34,108,35]:
        a,b=[next(g for g in groups if g['block']==number and g['version']==v) for v in ['clean_Japanese','English']]
        assert a['input_schedule_sha256']==b['input_schedule_sha256']"""
    replacement="""    previous=read('work/analysis/maria_story_actual_v7752c/six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json')
    assert not previous['unresolved']
    for b in groups:
        a=next(g for g in previous['groups'] if g['block']==b['block'] and g['version']=='clean_Japanese')
        assert a['input_schedule_sha256']==b['input_schedule_sha256']
        assert sha(Path(a['capture_report']).read_bytes())==a['capture_report_sha256']
        assert sha(Path(a['observer_report']).read_bytes())==a['observer_report_sha256']"""
    a=derive('scripts/audit_Maria_story_scenes_v7752c.py','scripts/audit_Maria_story_final_v7765.py',{
        'maria_story_actual_v7752c':'maria_story_final_actual_v7765',
        'maria_story_scene_fixtures_v7749/six_complete_source_English_original_prelude_fixtures':'maria_story_scene_fixtures_v7763/two_final_English_original_prelude_fixtures',
        'maria_story_scene_runs_v7750':'maria_story_scene_runs_v7764',
        'work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json':'work/analysis/maria_story_final_stored_v7759/67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json',
        original:replacement,
        'six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json':'two_final_English_captures_actual_pages_headers_branches_returns.json',
        'all_six_jobs_terminal_andreaped':'both_final_English_jobs_terminal_andreaped',
    })
    # The replacement embeds the prior evidence path; simultaneous replacements do not alter it.
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=a,
        all_original_native_numbers_pixel_masks_complete_headers_branch_extents_returns_andunowned_guards_preserved=True,
        source_captures_reused_byexact_report_andtrace_hashes_not_rerun=True,
        old_type0_carry_andsource_R65_rightcell_findings_preserved=True,new_credit=0,full_goal_complete=False))
    print('Final two English actual-audit adapter frozen;original source captures retained byexact hashes.')
