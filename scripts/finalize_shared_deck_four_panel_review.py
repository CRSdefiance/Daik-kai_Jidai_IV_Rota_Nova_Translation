"""Seal four reviews with full native bodies and honestly scoped representative UI evidence."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

REVIEW=Path('work/analysis/Shared_Deck_tutorials_contextual_20261104/four_panel_contextual_review_v1.json')
NATIVE=Path('work/analysis/Shared_Deck_current_native_v5_20261104/native_andstorage_verification.json')
CONNECTED=Path('work/analysis/Shared_Deck_connected_current_20261104/connected_verification.json')
ACTUAL=Path('work/analysis/Shared_Deck_actual_UI_20261104/representative_UI_verification.json')
FINAL=Path('translations/shared_deck_four_panels_contextual_final_v1.json')
ROOT=Path('work/analysis/Shared_Deck_four_panel_checked_20261104')

if __name__=='__main__':
    assert not FINAL.exists() and not ROOT.exists()
    review,native,connected,actual=map(load,[REVIEW,NATIVE,CONNECTED,ACTUAL])
    assert (review['proposed_revisions'],review['wording_retentions'])==(1,3)
    assert len(native['cases'])==len(connected['cases'])==8 and len(native['plans'])==4
    assert connected['native_sha256']==sha(NATIVE.read_bytes()) and connected['all8_complete_current_native_constructor_selector_copy_raster_andfont_cases_pass']
    assert native['allocation_shortfall_bytes']==0 and native['all31_pointer_values_andallocation_starts_unchanged']
    assert native['complete_parent_inverse_andall_unowned_ARM9_bytes_exact']
    assert actual['actual_frames']==21400 and actual['complete_body_texture_andRGB_comparisons']==7
    assert actual['four_revised_special_static_paragraphs_not_activated_or_claimed_observed']
    assert actual['same_current168x108_native_Refit_constructor_palette_pitch_andglyph_consumer_observed']
    assert not any(actual[k] for k in ['natural_activation','full_route','hardware'])
    for sheet in [native['review_sheet'],*actual['review_sheets']]:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ledger=load('translations/editorial_review_current_v1.json')
    done={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not done & {('/__arm9__.bin',r['id']) for r in review['records']}
    plans={p['id']:p for p in native['plans']};final=deepcopy(review)
    for row in final['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        p=plans[row['id']];compiled=bytes.fromhex(p['compiled_hex'])
        assert compiled.endswith(b'\0') and len(compiled)<=p['allocation']
        assert ' '.join(p['lines'])==row['english'].removesuffix('{PAD}')
        assert all(len(line)<=27 for line in p['lines']) and 1<=len(p['lines'])<=5
        assert all(len(line)%2==0 for line in compiled[:-1].split(b'\n')[:-1])
        row['review']['formatting']=True
        row.update(planned_integrated_reference=dict(file_path='/__arm9__.bin',offset=p['current_offset'],capacity=p['allocation'],
            compiled_hex=p['compiled_hex'],padded_hex=compiled.ljust(p['allocation'],b'\0').hex()),
            formatting_preference_reason=p['phrase_preference_reason'],native_complete_body_checked=True,
            actual_target_paragraph_observed=False,representative_same_consumer_actual_evidence=str(ACTUAL),
            formatting_scope='Eight full native mode cases andeight source-connected cases;seven ordinary live bodies prove the unchanged consumer. Four special bodies remain unvisited.',
            registered_deployment_andcompletion_credit_pending=True)
    final.update(format='dk4-editorial-final-review-v1',file_path='/__arm9__.bin',all_four_prose_gates_pass=True,all_formatting_gates_false=False,
        all_five_individual_review_gates_pass_in_research=True,no_prose_shortening_for_storage=True,
        final_native_pages=4,ordinary_wrap_preferences=4,one_terminology_revision=1,justified_retentions=3,
        consumer='current-refit-help27-pair-safe-168x108',all31_pointer_values_andall_nonpanel_bytes_exact=True,
        no_font_runtime_heap_pagination_orlayout_code_change=True,four_target_paragraphs_live_unvisited=True,
        no_duplicate_credit_for_the_prior_single_First_Mate_draft=True,registered_deployment_andcompletion_credit_pending=True,
        new_credit=0,guide_photos=False,full_goal_complete=False,
        formatting_evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,CONNECTED,ACTUAL,Path('scripts/shared_deck_formatting_v1.py'),Path(__file__)]})
    validate_natural_dialogue_batch(final);ROOT.mkdir();save(FINAL,final)
    save(ROOT/'visual_andresearch_approval.json',dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        all_four_final_native_panels_andtwo_actual_QA_sheets_directly_viewed=True,findings=[],
        four_phrase_preferences_preserve_complete_prose_andnative_guards=True,
        complete_native_geometry_pitch_height_andaccepted_Yplus1_right_bounds_reconciled=True,
        special_target_bodies_unvisited_live=True,representative_live_consumer_bodies=7,actual_frames=21400,
        prior_legacy_pool_andnative_fixture_failures_preserved_not_ROM_defects=True,
        registered_deployment_andcompletion_credit_pending=True,new_credit=0,guide_photos=False))
    print('Four five-gate research reviews sealed:one revision/three retentions/four wrap fixes;four bodies offline-only,seven representative live consumer bodies;zero credit.')
