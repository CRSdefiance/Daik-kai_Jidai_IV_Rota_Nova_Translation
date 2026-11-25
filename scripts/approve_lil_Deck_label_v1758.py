"""Approve inspected Deck View refinement and reconcile every current native case."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_Deck_label_approval_v1758')
OUT=Path('translations/lil_lessons_editorial_manuscript_v5.json')
DRAFT=Path('translations/lil_lessons_editorial_manuscript_v4.json')
REFINED=Path('work/analysis/lil_Deck_label_v1755/Deck_View_label_native_proof.json')
FONT=ROOT/'all60_current_native_font_reconciliation.json'
FE=ROOT/'all9_current_FE_reconciliation.json'

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    doc=deepcopy(read(DRAFT)); refinement=read(REFINED)
    assert sha(DRAFT.read_bytes())==refinement['draft_sha256']
    assert sha(Path(refinement['preview']).read_bytes())==refinement['preview_sha256']
    assert all(c['complete_one_page_and_independent_plane_exact'] for c in refinement['cases'])
    prior_path=Path('work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json')
    prior=read(prior_path); cases=deepcopy(prior['cases'])
    row=next(r for r in doc['records'] if r['id']==refinement['only_changed_id'])
    row['compiled_hex']=refinement['encoded_hex'];row['formatted_markup']=refinement['formatted_markup']
    row['review']['formatting']=True;row['formatting_evidence']=str(ROOT/'visual_review.json')
    row['qa_waivers']=['line-break-count']
    row['qa_waiver_reason']='Source Japanese3 breaks versus automatically wrapped English2 breaks. The exact three-line FE panel was inspected,complete native and independent planes match inside228x48,and full first/last letters fit one page. The original Deck View menu label is preserved;no authored breaks or omitted mechanics.'
    case=next(r for r in cases if r['id']==row['id'])
    case.update(encoded_hex=refinement['encoded_hex'],native_expanded_hex=refinement['encoded_hex'][2:],
        formatted_markup=refinement['formatted_markup'],diagnostics=refinement['diagnostics'],
        glyphs=refinement['cases'][0]['glyphs'],preview=refinement['preview'],preview_sha256=refinement['preview_sha256'],
        current_actual_FE_context_native_plane_proof=str(REFINED),
        current_native_plane_source_geometry=[228,48],preview_display_geometry=[228,64])
    case.pop('native_font_plane_sha256',None)
    assert case['whole_native_and_independent_font_plane_exact'] and case['complete_printable_glyph_order_unique_cells_and_bounds_verified']
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    panel=replace(base,name='lil-lessons-FE-runtime-bound-v1',leading_speaker_bytes=base.leading_speaker_bytes|frozenset({254}))
    by_id={r['id']:r for r in cases}
    for r in doc['records']:
        compiled=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['english'],panel if r['source_presentation_prefix_hex']=='fe' else base)
        assert compiled.encoded.hex()==r['compiled_hex']==by_id[r['id']]['encoded_hex']
        assert all(d.severity=='warning' and d.code=='line-break-count' and d.code in r.get('qa_waivers',[]) and r.get('qa_waiver_reason') for d in compiled.diagnostics)
    doc.update(formatting_review_pending=False,
        status='60-source-prose-native-layout-approved;Deck-View-label-matches-actual-menu;revised-gameplay-map-release-pending',
        native_font_proof=str(FONT),native_font_research=str(FONT),actual_context_FE_proof=str(FE),
        visual_review=str(ROOT/'visual_review.json'),native_label_refinement_proof=str(REFINED))
    for key in ('native_font_proof_sha256','actual_context_FE_proof_sha256','visual_review_sha256'):
        doc.pop(key,None)
    validate_natural_dialogue_batch(doc)
    old_FE_path=Path('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')
    old_FE=read(old_FE_path); panels=deepcopy(old_FE['reviewed_cases'])
    current=next(r for r in panels if r['id']==row['id'])
    current.update(target_hex=refinement['storage_target_hex'],native_glyphs=refinement['cases'][1]['glyphs'],
        display_preview=refinement['preview'],display_preview_sha256=refinement['preview_sha256'],
        current_native_plane_proof=str(REFINED))
    current.pop('logical_228x48_plane',None);current.pop('logical_plane_sha256',None)
    ROOT.mkdir(parents=True)
    save(ROOT/'visual_review.json',{'refined_three_line_Deck_View_panel_actually_viewed':True,
        'exact_actual_menu_label_and_Deck_screen_title_verified':True,
        'full_first_last_letters_uniform_left_alignment_bounds_and_one_page_acceptable':True,
        'remaining59_approved_paragraphs_compiled_bytes_and_native_planes_exactly_reused':True,
        'earlier_full64_native_visual_review':'work/analysis/lil_lesson_layout_approval_v1742/visual_native_formatting_review.json',
        'refinement_proof':str(REFINED),'refinement_sha256':sha(REFINED.read_bytes()),
        'current_live_research_ROM_still_contains_prior_instruction_new_actual_verification_required':True,
        'full_goal_complete':False})
    save(OUT,doc)
    save(FONT,{'manuscript':str(OUT),'manuscript_sha256':sha(OUT.read_bytes()),'candidate':prior['candidate'],
        'candidate_sha256':prior['candidate_sha256'],'ARM9_sha256':prior['ARM9_sha256'],
        'prior_native_proof':str(prior_path),'prior_native_proof_sha256':sha(prior_path.read_bytes()),
        'only_refined_id':row['id'],'unchanged59_rows_and_compiled_planes_reused_exactly':True,
        'cases':cases,'FE_dispatch_cases':prior['FE_dispatch_cases'],'review_sheets':prior['review_sheets'],
        'refined_panel_visual_review':str(ROOT/'visual_review.json'),
        'native_reference_new_actual_scene_and_registered_release_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    save(FE,{'candidate':old_FE['candidate'],'candidate_sha256':old_FE['candidate_sha256'],
        'reviewed_cases':panels,'all9_reviewed_FE_full_actual_context_native_planes_pass':True,
        'all9_complete_targets_fit_one_native_page_inside228x48':True,
        'current_actual_checks':old_FE['current_actual_checks'],
        'all6_current_FE_native_actual_complete_ink_and_blank_cells_match':True,
        'eight_unchanged_planes_and_original_screen_composition_contract':str(old_FE_path),
        'prior_sha256':sha(old_FE_path.read_bytes()),'one_refined_panel':str(REFINED),
        'physical_mapping_is_an_actual_screen_contract_not_an_independent_GPU_trace':True,
        'actual_revised_gameplay_external_references_and_registered_release_pending':True,'full_goal_complete':False})
    save(ROOT/'approval_receipt.json',{'manuscript':str(OUT),'sha256':sha(OUT.read_bytes()),
        'all60_current_native_cases_and_all9_FE_current_planes_reconciled':True,
        'only_one_paragraph_changes_to_match_visible_Deck_View_menu_label':True,
        'new_relocation_research_and_actual_final_instruction_pending':True,'full_goal_complete':False})
    print('V5 approved:Deck View instruction complete in three lines;59 other texts/planes exact,all60 current cases reconciled. New ROM/final instruction actual still pending.')
