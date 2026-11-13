"""Rebind eight historical Livestock/Chapel holds to the current complete payloads."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/rebind_work_history_v2312.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'dk4tool.patch.work_comments_editorial':'dk4tool.patch.livestock_prayer_editorial',
 'work_history_v2312':'livestock_prayer_history_v2329',
 'work/analysis/work_comments_v846/actual_gameplay_verification.json':'work/analysis/livestock_prayer_v856/actual_gameplay_verification.json',
 'translations/work_contextual_editorial_manuscript_v1.json':'translations/livestock_prayer_contextual_editorial_manuscript_v1.json',
 'scripts.work_comments_layout_v843 import compiled,layout':'scripts.livestock_prayer_layout_v854 import compiled,layout',
 'synthetic_work_room_occupant_fixtures':'synthetic_livestock_prayer_assignment_fixtures',
 'not_new_current_fixture_or_earned_refit_assignment':'not_new_current_fixture_or_earned_family_assignment',
 'V845':'V855',
 '{1387,1395,1398,1405}':'{1428,1435,1441,1444}',
 '[1387,1395,1398,1405]':'[1428,1435,1441,1444]',
 'historical_work8_sheet.png':'historical_livestock_prayer8_sheet.png',
 'Janus_foreign_faction21_preserved_not_a_recruitment_claim':'Julio_Janus_Emilio_foreign_faction21_preserved_not_a_recruitment_claim',
 'full36_cell1405_period_and_odd19_character1398_continuation_bound':'full_three_row1435_invocation_odd15_middle_row_and_third_continuation_bound',
 'no_new_current_Doctor_Hodram_or_Janus_visit_claim':'no_new_current_Livestock_or_Chapel_visit_claim',
 'current_ordinary_Gerhard_capture_is_separate':'current_shared_Cook_consumer_control_is_separate_not_a_family_visit',
 'work/analysis/work_current_verification_v2311/ordinary_current_Shipwright_actual.json':'work/analysis/cooking_current_verification_v2321/ordinary_current_Cook_actual.json',
 'work/analysis/work_fonts_v2309/all24_current_native_fonts.json':'work/analysis/livestock_prayer_fonts_v2328/all24_current_native_fonts.json'}
 for old,new in changes.items():assert old in source,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 proofpath=Path('work/analysis/livestock_prayer_history_v2329/historical8_current_binding.json');proof=read(proofpath)
 for scope in proof['historical_reports_and_fixture_scopes']:
  fix=scope['historical_room_occupant_fixture'];assert fix['role_type']in(17,18)and fix['actual_captain_ID_preserved']==1
  if fix['actor_ID']in(4,6,14):assert fix['original_actor_faction']==21 and fix['foreign_actor_not_claimed_as_normally_recruited']
 save(proofpath.parent/'historical_scope_and_labels.json',dict(binding=str(proofpath),binding_sha256=sha(proofpath.read_bytes()),historical_case_label_preserved='JoakimFleet',current_actor1_given_name='Hodram',approved_full_name='Hodram Joakim Bergstrom',metadata_evidence='work/analysis/cooking_context_v2316/captain1_speaker_metadata.json',four_historical_normal_return_controls_inherited_only=True,all_original_historical_fixtures_remain_disclosed=True,no_new_current_family_visits_or_earned_recruitment_claim=True,producer_sha256=sha(Path(__file__).read_bytes()),effective_source_sha256=sha(source.encode()),full_goal_complete=False))
