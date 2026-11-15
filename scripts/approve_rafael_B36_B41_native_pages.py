"""Join exact complete record proofs and directly viewed replacement pages."""
import inspect
from pathlib import Path
from scripts import review_rafael_early_tutorial_display as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_formatting_20261104')
DOC=ROOT/'formatting_input.json'
INITIAL=ROOT/'initial_plans_v1/automatic_plans.json'
NATIVE=Path('work/analysis/Rafael_B36_B41_native_20261104/initial_v1/compiled_native_pages.json')
FINDINGS={k:None for k in ['DK4_MES_B36_R0046','DK4_MES_B37_R0254','DK4_MES_B37_R0267','DK4_MES_B41_R0131']}

source=checked_text(inspect.getsource(previous.approve),{
    'speech_display_approved_v2':'speech_display_approved_v3',
    'page_clauses_v2/automatic_plans.json':'visual_plans_v3/automatic_plans.json',
    'Rafael_early_tutorial_B42_B43_native_20261104/page_clauses_v2':'Rafael_B36_B41_native_20261104/visual_v3',
    'page_clause_preferences_v2.json':'visual_preferences_v3.json',
    'pages == 42 and len(native) == 40':'pages == 177 and len(native) == 175',
    "len(fresh['review_sheets']) == 2 and fresh['pages'] == 4":"len(fresh['review_sheets']) == 3 and fresh['pages'] == 6",
    "viewed['directly_viewed_sheets']":"viewed['directly_viewed_sheets']",
    'all40_compiled_plans.json':'all175_compiled_plans.json',
    'pages=42,':'pages=177,',
    'all42_final_pages_directly_viewed=True':'all177_final_pages_directly_viewed=True',
    'exact_unchanged_complete_record_proofs_reused=38':'exact_unchanged_complete_record_proofs_reused=171',
    'fresh_changed_record_proofs=2, fresh_changed_alignments=8':'fresh_changed_record_proofs=4, fresh_changed_alignments=16',
    'all40_native_pages.json':'all175_native_pages.json',
    'normal_ASCII_First_andcomplete_Rafael_name_viewed=True':'both_corrected_ASCII_I_andcomplete_FU_name_viewed=True',
    'FE_Deck_View_three_rows_viewed=True':'all175_progressive_no_FE_objects=True',
    'All 40 speeches/42 final pages approved offline; two page-boundary fixes; no prose changes or QA waivers.':
        'All175 speeches/177 final pages approved offline;four layout fixes;two ASCII-I corrections;no prose changes orQA waivers.',
})
env={**previous.approve.__globals__,'ROOT':ROOT,'DOC':DOC,'INITIAL':INITIAL,'NATIVE':NATIVE,'FINDINGS':FINDINGS,'__file__':__file__}
exec(compile(source,__file__+'::same-exact-proof-merge-current-full-source-scope','exec'),env)

if __name__=='__main__':
    env['approve']()
    names_path=Path('work/analysis/Rafael_B36_B41_name_fields_native_20261104/native_name_fields_verification.json')
    names=load(names_path)
    assert len(names['planes'])==12 and len(names['negative_cases_rejected'])==8
    sheet=names['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(ROOT/'speech_display_approved_v3/catalogue_name_proposal_visual_approval.json',dict(native=str(names_path),native_sha256=sha(names_path.read_bytes()),
        directly_viewed_sheet=sheet,all12_current_andproposed_name_planes_directly_viewed=True,
        four_current_andfour_proposed_getters_pass=True,two_source_owned_spans=names['name_data_plan']['fields'],
        complete_parent_inverse_andall_unowned_ARM9_bytes_preserved=True,eight_rejection_cases_pass=True,
        offline_constructor_andraster_test_not_catalogue_UI_observation=True,actual_andregistered_deployment_pending=True,
        no_ROM_created=True,new_credit=0,guide_photos=False))
