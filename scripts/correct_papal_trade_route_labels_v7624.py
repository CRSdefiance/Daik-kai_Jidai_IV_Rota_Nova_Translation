"""Correct route-name metadata while preserving all earlier bytes, references and findings."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_route_identity_v7624')
OLD=Path('work/analysis/papal_trade_SC0_SC1_findings_v7621/all36_whole_exchange_raw_findings_andcandidate_retentions_native_consumers_pending.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(OLD);references=[Path('translations')/p for p in ['raphael_deep_route_v63.json','hodram_deep_route_v1.json','maria_deep_route_v24.json']]
    assert [read(p)['file_path'] for p in references]==['/data/SC0.DK4','/data/SC1.DK4','/data/SC3.DK4']
    oldkey='Rafael_Filippo_address_erased_Maria_full_width_initial_is_source_bound_alias_lead_not_shared_role_relabel'
    assert d[oldkey] is True and len(d['records'])==36
    corrected=deepcopy(d);corrected['historical_route_label_finding']=dict(original_path=str(OLD),original_sha256=sha(OLD.read_bytes()),incorrect_key=oldkey,incorrect_value=corrected.pop(oldkey),reason='SC1 was mislabeled Maria in progress wording andthis finding key;the actual SC0B246/SC1B237 file/block/record references andJapanese/current bytes were always correct.')
    corrected['Rafael_Filippo_address_erased_Hodram_full_width_initial_is_source_bound_alias_lead_not_shared_role_relabel']=True
    for r in corrected['records']:r['route_identity']={'/data/SC0.DK4':'Rafael','/data/SC1.DK4':'Hodram'}[r['file_path']]
    for before,after in zip(d['records'],corrected['records'],strict=True):
        restored=deepcopy(after);restored.pop('route_identity');assert restored==before
    ROOT.mkdir(parents=True);out=ROOT/'corrected_SC0_Rafael_SC1_Hodram36_raw_findings_no_body_changes.json';save(out,corrected)
    save(ROOT/'route_identity_correction_no_ROM_prose_reference_orcredit_change.json',dict(incorrect_prior_SC1_Maria_label_acknowledged=True,correct_route_names={'SC0':'Rafael','SC1':'Hodram','SC2':'Lil','SC3':'Maria'},current_scope=[dict(file_path='/data/SC0.DK4',block=246,route_identity='Rafael',expected_original_captain_ID=0),dict(file_path='/data/SC1.DK4',block=237,route_identity='Hodram',expected_original_captain_ID=1)],source_identity_metadata={str(p):dict(file_path=read(p)['file_path'],sha256=sha(p.read_bytes())) for p in references},corrected_findings=str(out),corrected_findings_sha256=sha(out.read_bytes()),all_original36_source_current_refs_andtexts_andfindings_unchanged=True,all_prior_incorrect_labels_preserved_as_history_andexplicitly_superseded=True,Maria_SC3_remains_in_full_goal_not_part_of_this_SC1_scope=True,fresh_route_specific_native_contexts_not_yet_captured=True,no_ROM_or_new_prose_orcredit_mutation=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Route labels corrected:SC0 Rafael/SC1 Hodram;Maria SC3 remains separate.All36 source/current references andbodies unchanged;historical incorrect labels preserved;zero credit.')
