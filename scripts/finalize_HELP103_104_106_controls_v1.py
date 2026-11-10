"""Bind actual DS controls and finish the remaining three prose gates for Deck Help30."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT=Path('work/analysis/HELP103_104_106_current_controls_20261104')
ARTICLES=Path('work/analysis/Shared_HELP_T103_T132_clean_20261104')

if __name__=='__main__':
    out=ROOT/'control_binding_v1.json'
    target=ARTICLES/'whole_article_comparisons_v3.json'
    assert not out.exists() and not target.exists()
    plan_path=ROOT/'run_plan_v1.json';report_path=ROOT/'capture_v1/capture_report.json'
    plan,report=map(load,[plan_path,report_path])
    assert report['ROM_sha256']==plan['ROM_sha256']==sha(Path(plan['ROM']).read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==9600
    assert not any(v for k,v in report.items()if k.startswith('synthetic_'))
    assert sha(Path(plan['battery']).read_bytes())==plan['battery_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    initial=load(ROOT/'inputs_v1.json');events=report['scripted_input_schedule']
    assert events[:len(initial)]==initial
    assert events[len(initial):]==[
        dict(start=7801,duration=8,buttons=['A']),dict(start=8001,duration=8,buttons=['Y']),
        dict(start=8201,duration=1,buttons=['DOWN']),dict(start=8401,duration=8,buttons=['A']),
        dict(start=8601,duration=8,buttons=['B']),dict(start=8801,duration=8,buttons=[],touch=[98,103]),
        dict(start=9001,duration=8,buttons=['A']),dict(start=9201,duration=8,buttons=['Y']),
        dict(start=9401,duration=8,buttons=['A'])]
    pauses=report['read_only_pause_RAM_snapshots']
    assert [r['frame']for r in pauses]==list(range(7800,9601,200))
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    for row in pauses:
        assert len(Path(row['path']).read_bytes())==4194304 and sha(Path(row['path']).read_bytes())==row['sha256']
    native=load(ARTICLES/'native_roles_rooms_andskills_v1.json')
    arm=NdsImage.open(plan['ROM']).read_file('/__arm9__.bin')
    assert sha(arm)==native['current_ARM9_sha256']
    observations={7800:'X opened the shared command menu at sea; Route Map selected.',
        8000:'A opened the current sea-region route map with selected fleet information.',
        8200:'Y opened World Map / Sea Areas with N.Sea selected.',
        8400:'DOWN selected Med. on the world map.',8600:'A opened the Mediterranean map; no travel occurred.',
        8800:'B returned to the shared command menu.',9000:'Ordinary stylus selection moved the menu to Deck View.',
        9200:'A opened Deck; footer explicitly shows X Finish and Y Crew.',
        9400:'Y opened Crew Setup with Explore, Trade and Battle choices.',
        9600:'A selected Explore and returned to Deck with changed assignments; no save was written to the donor.'}
    save(out,dict(ROM=plan['ROM'],ROM_sha256=plan['ROM_sha256'],current_ARM9_sha256=sha(arm),
        report=str(report_path),report_sha256=sha(report_path.read_bytes()),run_plan=str(plan_path),run_plan_sha256=sha(plan_path.read_bytes()),
        direct_individual_frame_visual_review=[dict(frame=f,finding=observations[f],capture=next(r for r in report['frames_captured']if r['frame']==f))for f in observations],
        observed_controls=dict(shared_menu_at_sea='X',map_to_world='Y',Deck_automatic_assignments='Y',Deck_finish='X'),
        observed_assignment_policy_labels=['Explore','Trade','Battle'],source106_triangle_maps_to_DS_Y_in_this_consumer=True,
        no_global_PlayStation_to_DS_button_substitution=True,ordinary_inputs_andisolated_inherited_battery_only=True,
        original_battery_unchanged=True,no_new_RAM_code_location_unlock_fixture_or_savestate=True,
        shared_town_X_not_freshly_activated=True,not_new_Rafael_progress_orfull_story_orhardware=True,new_credit=0))
    prior_path=ARTICLES/'whole_article_comparisons_v2.json';doc=deepcopy(load(prior_path))
    for row in doc['records']:
        n=row['topic_id']
        if n==103:
            row['finding']='Retain the full town-and-sea scope and native destinations. X opens the shared menu in the observed current sailing consumer; the town instruction is clean-source/current-bound, not a newly activated town case.'
        elif n==104:
            row['finding']='Restore the omitted Y zoom-out instruction. Actual current Y opened World Map, DOWN selected Med., and A opened that region, confirming the full source navigation sequence without claiming travel.'
        elif n==106:
            row['heading']='Crew Setup'
            row['english']='You can assign officers to jobs automatically. Press Y in Deck View, then choose [[107|Explore]], [[108|Trade]] or [[109|Battle]].'
            row['finding']='Use the actually observed DS Y Crew control and Explore/Trade/Battle choices. Source triangle is Y here; X finishes Deck changes. The older Choose Auto instruction and provisional X draft did not match this current consumer.'
        elif n in [107,109]:
            row['heading']={107:'Explore',109:'Battle'}[n]
            row['heading_localization_reason']='Use the actual Crew Setup policy caption, retaining the accurate body explanation word for word.'
        if n in [103,104,106]:
            row['localization_note']=row['finding'];row['review']['localization']=True
            row['native_term_orcontrol_binding_pending']=False;row['native_terms_andcontrols_binding_pending']=False
            row['provisional_decision_may_change_after_binding']=False
            row['native_control_binding']=str(out);row['native_control_binding_sha256']=sha(out.read_bytes())
    assert len(doc['records'])==30 and all(all(r['review'][g]for g in ['source','context','localization','naturalness'])and not r['review']['formatting']for r in doc['records'])
    doc.update(first_four_gates_passed=30,pending_localization_binding_topic_IDs=[],all_fifth_gates_pending=True,
        previous_comparisons=str(prior_path),previous_comparisons_sha256=sha(prior_path.read_bytes()),
        native_controls=str(out),native_controls_sha256=sha(out.read_bytes()),proposed_revisions=12,justified_retentions=18,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(target,doc)
    print('All30 four-prose-gate reviews pass:12 revisions/18 exact-body retentions. Actual Y Crew correction bound; fresh display/integration remain.')
