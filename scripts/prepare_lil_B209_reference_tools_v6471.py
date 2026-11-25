"""Prepare source-bound B209 event entry, current whole loaders and four-site shipped census."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_reference_tools_v6471')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/prove_lil_B208_entry_v6395.py','scripts/prove_lil_B209_entry_v6471.py',{
        'B208':'B209','entry_v6395':'entry_v6471','source_v6390/all24_clean_current_complete_context.json':'source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json',
        "and sha(ev)==packet['original_EV2_sha256']":"and sha(ev)==sha(clean.read_file('/data/EV2.DK4'))",
        "packet['historical_snapshot_ROM']":"'unused-no-historical-ROM'",
        'current_V6380_native_v6389':'current_V6439_native_v6449',"r['script_block'] in [208]":"r['script_block'] in [209]",
    }))
    rows.append(derive('scripts/verify_lil_B208_loader_v6425.py','scripts/verify_lil_B209_loader_v6472.py',{
        'B208':'B209','loader_v6425':'loader_v6472','create_lil_B208_reference_v6424':'create_lil_B209_reference_v6468','lil_B208_research_v6424':'lil_B209_reference_v6468','V6380':'V6439',
    }))
    rows.append(derive('scripts/verify_lil_B208_references_v6426.py','scripts/verify_lil_B209_references_v6473.py',{
        'B208':'B209','reference_census_v6426':'reference_census_v6473','loader_v6425':'loader_v6472','create_lil_B208_reference_v6424':'create_lil_B209_reference_v6468',
        'if n not in [208]':'if n not in [209]',
        '==29':'==18','native_commands_each=29':'native_commands_each=18',
        "sum(r['typed_relative_span_count']for r in result)==0":"sum(r['typed_relative_span_count']for r in result)==4",
        "sum(r['target_native_skip_cases']for r in result)==0":"sum(r['target_native_skip_cases']for r in result)==20",
        'all29_commands_no_relative_sites_and_shipped_entry_census':'all18_commands_four_relative_sites_and_shipped_entry_census',
        'all29_clean_current_target_commands_and_no_relative_sites_reexecuted':'all18_clean_current_target_commands_and_four_relative_sites_reexecuted',
        'relative_sites=0,target_native_skip_cases=0':'relative_sites=4,target_native_skip_cases=20',
        'census and29-command/no-relative-site':'census and18-command/four-relative-site',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,source_event_conditions_and_actual_eligibility_not_assumed=True,all336_blocks_two_parent_modes_and_three_shipped_call_censuses_required=True,all18_commands_two_typed_objects_four_relative_sites20_target_cases_bound=True,no_registered_or_ledger_mutation=True,full_goal_complete=False))
