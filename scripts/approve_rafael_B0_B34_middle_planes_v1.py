"""Record direct visual review of all 18 current/proposed native name planes."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT


PROOF=ROOT/'owned_middle_fields_native_v1/native_name_fields_verification.json'
OUT=ROOT/'owned_middle_fields_visual_v1.json'


def main():
    assert not OUT.exists()
    proof=load(PROOF)
    assert len(proof['planes'])==18 and len(proof['consumer_plane_bindings'])==24
    assert len(proof['negative_cases_rejected'])==8 and proof['original_progressive_andfull_name_getters_pass']
    assert proof['name_data_plan']['complete_parent_inverse_exact']
    assert proof['name_data_plan']['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    assert all(p['complete_glyphs_bounds_andindependent_pixels_pass'] for p in proof['planes'])
    assert digest(proof['review_sheet']['path'])==proof['review_sheet']['sha256']
    save(OUT,{**proof,'native_proof':str(PROOF),'native_proof_sha256':digest(PROOF),
        'direct_view_pending':False,'offline_visual_approved':True,
        'visual_findings':'Viewed all 18 current/proposed planes. Full-width F and untranslated de particles are visible in the old catalogue forms; the three proposed full names use consistent complete ASCII glyphs. Progressive forms retain their existing spelling. First/final characters, spacing and bounds are intact.',
        'style1_is_a_second_native_plane_not_observed_catalogue_UI':True,
        'actual_header_catalogue_UI_startup_andregistered_deployment_pending':True,
        'evidence':{**proof['evidence'],str(PROOF):digest(PROOF),str(Path(__file__)):digest(__file__)}})
    print('Approved the 18 directly viewed native name planes; gameplay and deployment remain pending.')


if __name__=='__main__':
    main()
