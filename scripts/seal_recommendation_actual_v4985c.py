"""Seal ten viewed full screens and exact declared fixture/display/return scope."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/recommendation_actual_verification_v4985')
INPUT=ROOT/'paired775_780_766_actual_planes_fixtures_and_return.json'
OUTPUT=ROOT/'viewed_original_reward_transition_approval.json'
DOC=Path('translations/earlier_common_wraps_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not OUTPUT.exists() and not DOC.exists();d=read(INPUT)
    assert d['all_jobs_terminal'] and d['actual_original_reward_sequence']==[775,780,766] and d['actual_panel_observations']==6
    assert len(d['captured_comparisons'])==d['nontext_equal_samples']==74 and not d['nontext_differences']
    assert all(r['whole_RGB_equal'] for r in d['sampled_after_original_farewell']) and d['whole_final_RGB_equal']
    assert all(d['native_final_component_equality'].values()) and d['whole_actor_and_actual_captain_equal']
    assert d['actual_donor_captain_IDs']==[1,1] and d['PRNG_equal'] and d['PRNG_seeds']==[260148687,260148687]
    assert d['versions'][0]['all_font_rows']==d['versions'][1]['all_font_rows']
    assert [r['font_frame'] for r in d['versions'][0]['holds']]==[6023,6424,6827]
    for p,h in d['evidence'].items():assert sha(Path(p).read_bytes())==h
    assert sha(Path(d['review_sheet']).read_bytes())==d['review_sheet_sha256']
    d.update(visual_review_pending=False,ten_full_screens_viewed=True,
        visual_review='Viewed all10 full paired screens at6100,6500,6900,7300 and12001.775 is four rows before and three complete rows after;all words,apostrophes,punctuation,leading/final glyphs and margins survive. Trader portrait/name and the Deal/Istanbul UI are preserved.780 retains any town and should;766 remains Come back any time.7300 shows the original Power+16 result and12001 normal Istanbul town/Port return;neither following output adds editorial credit. All74 paired nontext samples,source font timings,post-farewell whole images,five final state groups,whole actor,captain1 and PRNG260148687 agree. This does not prove future-world or full-RAM equality. The cargo IDs/demand/share80 and source qualification2/reward quantity16/bonus1 inputs are disclosed counterfactual fixtures;only two actual cargo holds were sold,and no earned recommendation or qualification is claimed.',
        no_open_translation_specific_display_or_transition_finding=True,representative_original_reward_transition_sufficient=True,
        no_extra_focus_run_without_concrete_unresolved_risk=True,new_editorial_credit=0,
        previous_analysis=str(INPUT),previous_analysis_sha256=sha(INPUT.read_bytes()),view_producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUTPUT,d)
    oldpath=Path('translations/earlier_common_wraps_editorial_manuscript_v1.json');old=read(oldpath);doc=deepcopy(old)
    doc.update(previous_manuscript=str(oldpath),previous_manuscript_sha256=sha(oldpath.read_bytes()),postscene_native_state_proof=str(OUTPUT),
        postscene_native_state_proof_sha256=sha(OUTPUT.read_bytes()),actual_new_emulator_runs=2,total_frames=24002,
        registered_integration_pending=True,source_prose_or_completion_credit_added=0,status='source-context-wording-native-and-representative-approved;registered-integration-pending')
    for r in doc['records']:
        r['status']=doc['status'];r['actual_recommendation_branch_observed']=r['message_id']==775
        r['actual_new_display_coverage']=r['message_id']==775
        r['native_display_scope']='Full current/reviewed native planes for all four leads. Actual paired fixture-driven775->780->766 and normal return are verified;682/764/774 remain offline in this revisit. No earned recommendation or natural large-sale eligibility claim.'
    assert [r['english'] for r in doc['records']]==[r['english'] for r in old['records']]
    validate_natural_dialogue_batch(doc);save(DOC,doc)
    save(ROOT/'sealed_manuscript_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),actual_approval=str(OUTPUT),actual_approval_sha256=sha(OUTPUT.read_bytes()),
        actual_display_IDs=[775,780,766],reflow_IDs=[775],exact_layout_retentions=[682,764,774],registered_integration_pending=True,new_editorial_credit=0,full_goal_complete=False))
    print('Viewed and sealed10 screens;775->780->766,three-row reflow and town return pass. Fixture inputs disclosed;no duplicate credit.')
