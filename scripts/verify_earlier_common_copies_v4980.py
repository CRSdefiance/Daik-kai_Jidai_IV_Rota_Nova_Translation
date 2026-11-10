"""Exercise every target COMMON selection in both original cache modes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/earlier_common_wraps_copies_v4980')
APPROVAL=Path('work/analysis/earlier_common_wraps_approval_v4979/four_retentions_one_reflow_source_native_approval.json')
if __name__=='__main__':
    assert not ROOT.exists();approval=read(APPROVAL);doc=read(approval['manuscript'])
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');target=Path(approval['target_COMMON']).read_bytes()
    assert sha(arm)==approval['source_ARM9_sha256'] and sha(target)==approval['target_COMMON_sha256']
    entries=owned_entries(target,arm,approval['directory_sha256']);assert len(entries)==3668
    loader=Loader(arm,target);cases=[]
    for mode in ['warm','cold']:
        for entry in entries:cases.append(loader.copy(entry.message_id,entry.text,mode))
        print(mode+'3668 native selections pass',flush=True)
    loader.reset();sequence=[loader.copy(n,entries[n].text,'sequence') for n in [774,779,766,775,780,766,682,764,3667,775]]
    assert len(cases)==7336 and [r.message_id for r in entries if r.text.hex()==doc['records'][-1]['target_hex']]==[775]
    ROOT.mkdir(parents=True);save(ROOT/'all7336_native_copies_and_letter_sequences.json',dict(source_ARM9_sha256=sha(arm),target_COMMON_sha256=sha(target),
        approval=str(APPROVAL),approval_sha256=sha(APPROVAL.read_bytes()),complete_native_copy_cases=7336,cases=cases,sequenced_cache_cases=sequence,
        original_ABI_complete_spans_NUL_canaries_cache_bounds_and_native_copy_guard_pass=True,
        native_file_open_read_are_explicit_host_contracts=True,not_actual_emulator_IO_or_earned_reward_eligibility=True,
        exact_original_runtime_no_code_or_table_change=True,new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,
        registered_integration_and_representative_transition_check_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
