"""Cook historical holds rebound to current complete text and pixels; no new visits."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/rebind_work_history_v2312.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'dk4tool.patch.work_comments_editorial':'dk4tool.patch.cooking_comments_editorial',
 'work_history_v2312':'cooking_history_v2322',
 'work/analysis/work_comments_v846/actual_gameplay_verification.json':'work/analysis/cooking_comments_v851/actual_gameplay_verification.json',
 'translations/work_contextual_editorial_manuscript_v1.json':'translations/cooking_contextual_editorial_manuscript_v1.json',
 'synthetic_work_room_occupant_fixtures':'synthetic_cook_room_assignment_fixtures',
 'not_new_current_fixture_or_earned_refit_assignment':'not_new_current_fixture_or_earned_Cook_assignment',
 'V845':'V850',
 '{1387,1395,1398,1405}':'{1411,1416,1419,1422}',
 '[1387,1395,1398,1405]':'[1411,1416,1419,1422]',
 'historical_work8_sheet.png':'historical_cooking8_sheet.png',
 'all24_complete_stored_payloads_exact_to_V850':'all13_complete_stored_payloads_exact_to_V850',
 'Janus_foreign_faction21_preserved_not_a_recruitment_claim':'Emilio_and_Sera_foreign_faction21_preserved_not_a_recruitment_claim',
 'full36_cell1405_period_and_odd19_character1398_continuation_bound':'odd19_character1416_and1419_first_rows_and_complete_continuations_bound',
 'no_new_current_Doctor_Hodram_or_Janus_visit_claim':'no_new_current_Emilio_Hodram_or_Sera_visit_claim',
 'work/analysis/work_current_verification_v2311/ordinary_current_Shipwright_actual.json':'work/analysis/cooking_current_verification_v2321/ordinary_current_Cook_actual.json',
 'current_all24_native_proof_is_separate':'current_all13_native_proof_is_separate',
 'work/analysis/work_fonts_v2309/all24_current_native_fonts.json':'work/analysis/cooking_fonts_v2318/all13_current_native_fonts.json'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
 save(env['ROOT']/'historical_label_metadata.json',dict(historical_case_label_preserved='JoakimCook',current_source_bound_actor1_given_name='Hodram',approved_full_name='Hodram Joakim Bergstrom',metadata_evidence='work/analysis/cooking_context_v2316/captain1_speaker_metadata.json',historical_label_is_not_a_new_character_or_current_visit=True,all4_historical_normal_return_controls_remain_historical=True,no_new_ROM_or_live_RAM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),effective_source_sha256=sha(source.encode()),full_goal_complete=False))
