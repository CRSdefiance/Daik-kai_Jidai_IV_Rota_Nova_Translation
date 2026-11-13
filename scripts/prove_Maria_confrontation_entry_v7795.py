"""Bind original event chain and ten unchanged source/current predicate executions."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.prove_maria_B97_entry_v5002 import native_entry
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_entry_v7795')
SOURCE=Path('work/analysis/maria_next_clean_v7786/complete_clean_SC3_B36_EV3_andcoverage_before_current_English.json')
CURRENT=Path('work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json')
INPUT=Path('work/analysis/current_V7779_native_v7782/route3/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();source,current=map(read,[SOURCE,CURRENT]);im=NdsImage.open(current['current_ROM'])
    assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256']
    ev=im.read_file('/data/EV3.DK4');assert sha(ev)==source['EV3_sha256']
    selected=[r for r in parse_events(ev) if r['event_ID'] in [36]]
    assert {r['event_ID']:(r['action_index'],r['script_block'],tuple(r['must_be_completed'])) for r in selected}=={36:(37,36,(35,))}
    text=checked_text(inspect.getsource(native_entry),{
        'original_completion_flag_in_historical_opening':'original_completion_flag_in_own_current_opening_with_test_unlock',
        'not_current_eligibility_or_selected_B97_activation':'not_current_eligibility_or_selected_story_chain_activation'})
    ns=dict(native_entry.__globals__);exec(compile(text,__file__+'::original-EV3-getters','exec'),ns)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    native=ctx.execute(ns['native_entry'],ev,selected);ctx.machines.pop();cases=[]
    for sg,cg in zip(source['groups'],current['groups'],strict=True):
        assert sg['block']==cg['block']
        for label,hexkey,commands in [('clean-Japanese','clean_block_hex',sg['commands']),('current-English','current_block_hex',cg['all_current_commands'])]:
            block=bytes.fromhex((sg if label=='clean-Japanese' else cg)[hexkey])
            for command in commands:
                if command['word'] not in [0x8000,0x8100]:continue
                result=ctx.execute(predicate,block,command);ctx.machines.pop()
                cases.append(dict(block=sg['block'],version=label,**result))
    assert len(cases)==0 and not ctx.machines
    save(ROOT/'one_original_EV3_getter_no_inblock_predicates.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],selected_source_events=selected,
        source_completion_dependency_chain=[35,36],original_event_getters=native,source_owned_event_getter_adapter=text,
        native_predicate_cases=cases,source_owned_predicate_adapter=inspect.getsource(predicate),
        all_original_4MiB_ABI_input_owner_output_andsole_alignment_scratch_guards_preserved=True,
        no_predicate_completion_flag_actor_roster_orRNG_forcing=True,
        snapshot_results_not_all_possible_conditions_orwhole_VM_branch_playback=True,
        nested0100_relative0200_0300_andUI_setup_wait_A000_C200_full_control_proofs_pending=True,
        own_current_input=str(INPUT),own_current_input_sha256=sha(INPUT.read_bytes()),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,actual_optional_event_activation_not_claimed=True,
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CURRENT,INPUT,Path(__file__)]},full_goal_complete=False))
    print('One exact EV3 getter;no in-block predicate commands. Outer eligibility remains separate. No natural activation orfull branch claim.')
    print([(r['block'],r['version'],r['offset'],r['native_result']) for r in cases])
