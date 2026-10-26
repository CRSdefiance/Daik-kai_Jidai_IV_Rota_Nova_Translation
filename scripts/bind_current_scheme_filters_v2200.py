"""Bind inherited target-exclusion cases to exact current source filter code."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/current_scheme_filter_binding_v2200')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 source=Path('work/analysis/tavern_scheme_targets_v775/source_contract.json')
 prior=read(source);current=Path('work/analysis/current_scheme_input_contract_v2199/input_contract.json');bound=read(current)
 a=NdsImage.open('out/all_routes_combined_v2171_candidate.nds').read_file('/__arm9__.bin');b=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=[]
 for lo,hi in prior['source_current_spans_exact']:
  assert a[lo:hi]==b[lo:hi];spans.append(dict(start=lo,end=hi,clean_current_sha256=sha(a[lo:hi])))
 assert len(prior['all400_first_target_exclusions'])==400 and len(prior['all8000_second_target_exclusions'])==8000
 assert bound['scheme_targets_exclude_current_faction_at_both_selections']and bound['editable_company_name_does_not_reach_these_original_scheme_consumers']
 assert a[0x9145C:0x91464]==bytes.fromhex('1800a0e31eff2fe1')
 save(ROOT/'source_filter_and_current_name_contract.json',dict(ARM9_sha256=sha(a),inherited_exclusion_proof=str(source),inherited_exclusion_proof_sha256=sha(source.read_bytes()),exact_filter_code_bindings=spans,inherited_first_target_cases=400,inherited_second_target_cases=8000,current_private_call_closure_and20_initializers=str(current),current_contract_sha256=sha(current.read_bytes()),editable_player_company_names_excluded=True,original_23_byte_synthetic_faction_stress_not_an_eligible_target_contract=True,no_general_waiver_of_custom_name_or_other_selector_risks=True,current_scheme_class_width_getter_cells=24,actual_CScheme_GUI_not_claimed_here=True,not_a_general_older_record_technical_reaudit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
