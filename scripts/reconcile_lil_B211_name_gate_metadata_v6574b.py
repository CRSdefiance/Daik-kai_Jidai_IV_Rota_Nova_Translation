"""Keep the draft pending flag as history and make the approved name-gate state unambiguous."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_name_metadata_v6574b');INPUT=Path('translations/lil_B211_speaker_name_review_v2.json');OUTPUT=Path('translations/lil_B211_speaker_name_review_v3.json');KEY='native_complete_name_planes_actual_headers_and_full_catalogue_UI_scope_pending'
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();old=read(INPUT);assert old[KEY] and old['two_contextual_name_retentions_approved_no_asset_change'] and old['full_catalogue_UI_unvisited'];new=deepcopy(old);new.update(previous_name_review=str(INPUT),previous_name_review_sha256=sha(INPUT.read_bytes()))
    new['historical_pending_metadata']={KEY:old[KEY],'previous_name_review':old['previous_name_review'],'previous_name_review_sha256':old['previous_name_review_sha256']};new[KEY]=False;new['native_names_and_actual_headers_approved_full_catalogue_UI_scope_explicitly_unvisited']=True;assert new['records']==old['records'];save(OUTPUT,new);ROOT.mkdir(parents=True);save(ROOT/'name_review_metadata_reconciliation.json',dict(previous=str(INPUT),previous_sha256=sha(INPUT.read_bytes()),name_review=str(OUTPUT),name_review_sha256=sha(OUTPUT.read_bytes()),approved_name_records_and_all_native_actual_evidence_unchanged=True,stale_draft_pending_flag_preserved_as_history_cleared_in_approved_successor=True,no_UI_visit_new_asset_name_or_dialogue_credit_claim=True,full_goal_complete=False));print('B211 approved name gate metadata reconciled;full catalogue UI remains explicitly unvisited. No new prose,asset,test orcredit.')
