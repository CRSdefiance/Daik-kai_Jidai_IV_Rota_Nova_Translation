"""Receipt for directly viewed five-page native sheet; no gameplay or final formatting credit."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Gerhard_native_review_v8207')
PAGES=Path('work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json')
PLAN=Path('work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json')
if __name__=='__main__':
    assert not ROOT.exists();pages,plan=map(read,[PAGES,PLAN]);assert pages['plan_sha256']==sha(PLAN.read_bytes())
    assert len(pages['records'])==5 and pages['complete_progressive_pages']==5 and len(pages['review_sheets'])==1
    assert not pages['unapproved_exact_ordinary_boundary_warnings'] and not plan['failures']
    for sheet in pages['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    issues=[dict(id=r['id'],issue=i) for r in plan['records'] for i in r['base_QA']['issues']]
    assert issues==[dict(id='DK4_MES_B74_R0260',issue=dict(severity='info',code='line-break-count',message='source has 2 line breaks; target has 1'))]
    ROOT.mkdir(parents=True);save(ROOT/'five_native_pages_directly_viewed_one_info_zero_warnings.json',dict(
        pages=str(PAGES),pages_sha256=sha(PAGES.read_bytes()),plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        directly_viewed_sheets=pages['review_sheets'],all_five_complete_bodies_visually_read=True,
        all_first_internal_final_letters_andpunctuation_visible=True,
        individual_wrap_review={
            'DK4_MES_B27_R0091':'Courteous acknowledgment leads into an intact Gerhard Adernkatz name on row2.',
            'DK4_MES_B27_R0094':'Complete address on row1; pirate-hunter identification remains together on row2.',
            'DK4_MES_B74_R0060':'Two short complete exclamations; It\'s been is no longer split.',
            'DK4_MES_B74_R0185':'Lil macro expands intact; Gerhard Adernkatz remains together. Admiral naturally introduces the next-row full name.',
            'DK4_MES_B74_R0260':'Exclamation/address and complete thanks/request fit two readable rows without dropping words.'},
        all_original_QA_diagnostics_preserved=issues,no_warning_waivers=True,
        offline_native_rendering_not_actual_scene_or_final_stored_layout=True,
        all5_final_formatting_gates_still_false=True,stored_controls_nameasset_actual_andregistered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PAGES,PLAN,Path(__file__)]}))
    print('Viewed all5 native pages;one info retained,zero warnings;actual/stored/name/release still pending.')
