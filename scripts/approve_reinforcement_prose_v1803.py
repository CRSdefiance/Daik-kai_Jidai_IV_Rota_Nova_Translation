"""Record visual/source review of current20 andsix unintegrated successors."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_review_v1803')
OLD=Path('translations/reinforcement_sniping_editorial_manuscript_v3.json')
NEW=Path('translations/reinforcement_sniping_editorial_manuscript_v4.json')
CURRENT=Path('work/analysis/current_reinforcement_matrix_v1801d/current694_native_wrap_and_font_reconciliation.json')
DRAFT=Path('work/analysis/reinforcement_faction_prose_v1802/six_paragraphs120_complete_native_cases.json')

if __name__=='__main__':
    assert not ROOT.exists()and not NEW.exists();ROOT.mkdir(parents=True)
    current,draft=read(CURRENT),read(DRAFT);assert len(current['cases'])==694 and len(draft['all120_cases'])==120
    assert len(current['fresh_current_complete_native_font_samples'])==34 and not draft['boundary_findings']
    all_previews=current['fresh_current_complete_native_font_samples']+draft['all120_cases']
    for row in all_previews:assert sha(Path(row['preview']).read_bytes())==row['preview_sha256']
    assert len({r['preview']for r in all_previews})==154
    sheets=current['review_sheets']+draft['review_sheets'];assert len(sheets)==6
    for row in sheets:assert sha(Path(row['path']).read_bytes())==row['sha256']
    proof=ROOT/'visual_and_source_review.json'
    save(proof,{'current_native_proof':str(CURRENT),'current_native_proof_sha256':sha(CURRENT.read_bytes()),
        'successor_six_paragraph_proof':str(DRAFT),'successor_six_paragraph_proof_sha256':sha(DRAFT.read_bytes()),
        'six_review_sheets_viewed':sheets,'every_reference_preview_hash_and_unique_variant_path_verified':True,
        'current20_exact_clean_Japanese_meanings_tones_and_speaker_alternatives_reread':True,
        'six_faction_lines_improved_to_ships_from_full_faction_label':True,
        'source_collective_fleet_assistance_and_uncertainty_preserved_without_duplicate_fleet_from_Fleet_wording':True,
        'no_faction_names_shortened_and_no_added_fleet_size_identity_or_event_fact':True,
        'all120_new_native_printf_wraps_ABI_guards_full_font_planes_and_bounds_pass':True,
        'all694_current_layouts_and_masks_plus34_current_native_rasters_pass':True,
        'CP932_fullwidth_F_intact_with_palette15_and_ascii_intact_with_palette1':True,
        'no_dropped_leading_trailing_letters_clipped_rows_blank_pages_or_unexplained_indentation_in_reviewed_sheets':True,
        'initial_failures_preserved':['1798 wrong terminal snapshot key','1801 historical-only entry guard',
            '1801b binary-mask versus palette15 comparison','1801c duplicate variant preview filenames'],
        'those_verifier_problems_did_not_change_any_ROM_or_target_gameplay':True,
        'six_revisions_remain_unregistered_and_not_gameplay_verified':True,'completed_entries_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    doc=deepcopy(read(OLD));assert doc['registered_integration_pending']
    for row in doc['records']:
        if row['message_id']in range(1911,1917):row['review']['formatting']=True
    doc['formatting_review_pending']=False
    doc['status']='six-faction-successors-source-prose-native-and-visual-reviewed-not-integrated'
    doc['successor_visual_review_proof']=str(proof);doc['successor_visual_review_proof_sha256']=sha(proof.read_bytes())
    doc['unchanged14_current_format_proof']=str(CURRENT);doc['unchanged14_current_format_proof_sha256']=sha(CURRENT.read_bytes())
    doc['predecessor_draft']=str(OLD);doc['predecessor_draft_sha256']=sha(OLD.read_bytes())
    validate_natural_dialogue_batch(doc);save(NEW,doc)
    print('Six successor faction paragraphs source/native/visual approved;20-record v2 manuscript valid. Integration/gameplay still pending.',flush=True)
