"""Bind all three source choice indices and cancellation with original modal VM code."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_choice_source_v5655')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);group=packet['blocks'][0]
    source=inspect.getsource(prior.choice_vm)
    adapter=checked_text(source,{'== 2':'== 3','for index in (0, 1):':'for index in range(3):',
        'for selected in (0, 1, -1):':'for selected in (0, 1, 2, -1):','(rect, provider, maximum, 2)':'(rect, provider, maximum, 3)',
        'pointer, 32':'pointer, len(object_bytes)','96':'VM_GUARD_BYTES','p.decode()':"p.decode('cp932')"})
    env={**prior.__dict__,'VM_GUARD_BYTES':256};exec(compile(adapter,__file__+'::three-original-options','exec'),env)
    versions=[]
    for label,commands,path in [('clean',group['all_clean_native_commands'],'work/clean.nds'),('current',group['all_current_native_commands'],packet['current_ROM'])]:
        command=next(c for c in commands if c['word']==0x2200);value=bytes.fromhex(command['whole_command_hex']);assert len(value)+32<=256
        image=NdsImage.open(path);proof=env['choice_vm'](image.read_file('/__arm9__.bin'),value)
        assert [c['modal_selection'] for c in proof['VM_cases']]==[0,1,2,-1]
        assert [c['VM_state'] for c in proof['VM_cases']]==[2,2,2,0]
        assert all(c['next_command_delta']==len(value) and c['original_dispatch_ABI_and_guards_pass'] for c in proof['VM_cases'])
        versions.append(dict(version=label,source_offset=230,object_hex=value.hex(),**proof))
    assert versions[0]['labels']==['買おう','買わない','任せる']
    ROOT.mkdir(parents=True);save(ROOT/'all_three_indices_and_cancel_original_VM_geometry_without_live_input.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        versions=versions,source_derived_three_option_VM_adapter=adapter,native_selection_cancel_cases=8,
        first_buying_proposal_index0_no_buy_index1_delegation_index2_preserved=True,
        all_six_relative_sites_original_last_results0_1_2_3_and_unsigned_minus1_separately_bound=True,
        exact_menu_bodies_consumed_and_native_state2_selected_index_or_state0_cancel_bound=True,
        modal_input_loop_bridged_not_actual_selected_gameplay=True,
        no_new_text_font_plane_or_English_wording_approval=True,
        financial_queries_delegation_decision_and_gift_conditions_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(prior.__file__),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B1972200:source/current indices0/1/2 and cancel pass8 VM cases;native geometry retained.Third option delegates the decision.Original modal input loop bridged;financial/delegation outcome conditions still pending.')
