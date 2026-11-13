"""Direct visual receipt for four complete native name input planes; no current-ROM claim."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Gerhard_name_view_v8211')
PROOF=Path('work/analysis/Gerhard_target_name_v8210c/owned12byte_input8_getters4_complete_name_planes_Blades_protected.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=read(PROOF);sheet=proof['review_sheet']
    assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'] and len(proof['planes'])==4
    assert [r['text'] for r in proof['planes']]==['Gerhard Ardelknatts','Gerhard Adernkatz','Adernkatz','Gerhard']
    assert all(r['all_complete_leading_internal_final_glyphs_one_row_in_bounds'] and r['independent_current_font_pixels_equal'] for r in proof['planes'])
    assert len(proof['native_eight_getters']['rows'])==8 and proof['protected_Blades_bytes_andall_other_RAM_exact']
    ROOT.mkdir(parents=True);save(ROOT/'four_name_planes_directly_viewed_research_input_only.json',dict(
        name_proof=str(PROOF),name_proof_sha256=sha(PROOF.read_bytes()),directly_viewed_sheet=sheet,viewed=True,
        all4_current_proposed_full_surname_andgiven_planes_read_completely=True,
        complete_first_internal_final_letters_punctuation_andspacing_visually_confirmed=True,
        selected_family_form_Adernkatz_preserves_clean_identity_without_official_Latin_canonical_claim=True,
        given_Gerhard_retained=True,approved_Hodram_Joakim_Camille_andLil_fields_unchanged=True,
        only_owned12byte_CPU_input_not_current_nameasset_actual_catalogue_UI_or_scene_gameplay=True,
        actual_name_scenes_registered_correction_frozen_policy_atomic_andrelease_pending=True,
        all_final_formatting_gates_still_false=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PROOF,Path(__file__)]}))
    print('All4 name input planes directly viewed;full/given/surname letters complete;asset/gameplay/release pending.')
