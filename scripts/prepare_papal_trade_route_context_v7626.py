"""Preserve every strict current-code guard and bind only fresh actual captain0/1 snapshots."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/papal_trade_route_context_tools_v7626')
if __name__=='__main__':
    assert not ROOT.exists()
    replacement="""assert self.doc['expected_original_captain_ID'] in [0,1] and context['route']==self.doc['expected_original_captain_ID']
        assert get(0x7F244)==self.doc['expected_original_captain_ID']"""
    tool=derive('scripts/square_shopkeeper_exact_native_context_v7020.py','scripts/papal_trade_route_native_context_v7626.py',{'class CurrentContext:':'class RouteCurrentContext:','assert get(0x7F244)==2':replacement})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_route_context_class.json',dict(tool=tool,original_captain2_context_unchanged=True,new_separate_class_requires_actual_own_current_capture_andexpected_original_captain0_or1=True,all2b6_COMMON_directory123264_payload_executed_instruction_andactor_guards_unchanged=True,no_historical_RAM_overlay_orrole_roster_RNG_event_mutation=True,all_high_native_numbers_andmultiplicity_preserved=True,new_credit=0,full_goal_complete=False))
