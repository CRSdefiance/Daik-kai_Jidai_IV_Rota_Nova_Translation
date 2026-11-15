"""Prove normal ends preserve the existing value word while flagged ends explicitly set zero."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B212_seeded_ends_v6634');PLAN=Path('work/analysis/lil_B212_relocation_v6622/all14_objects10_spans_three_exact_ends_full884_inverse_RESEARCH.json')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);adapter=checked_text(inspect.getsource(end_case),{'def end_case(arm,block,offset,previous):':'def end_case(arm,block,offset,previous,seed):','value=block[offset:offset+4];assert value==bytes(4)':"value=block[offset:offset+4];assert value in [bytes(4),bytes.fromhex('00000080')]",'cpu.mem_write(result,bytes(24))':"cpu.mem_write(result,struct.pack('<6I',0,seed,0,0,0,0))",'assert decoded==[0,0,0,0,0,0] and extent==4 and reads':"flagged=value==bytes.fromhex('00000080');assert decoded==[int(flagged),0 if flagged else seed,0,0,0,0] and extent==4 and reads",'source_operand_reads=reads,':'source_operand_reads=reads,initial_value_word=seed,flagged_terminal=flagged,'});env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::normal-residual-word-and-flagged-value','exec'),env);image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin');source=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[212];target=Path(plan['blocks'][0]['research_block']).read_bytes();assert sha(source)==plan['blocks'][0]['source_block_sha256'] and sha(target)==plan['blocks'][0]['research_block_sha256'];cases=[]
    for version,block in [('current-source',source),('relocated-target',target)]:
        for m in plan['blocks'][0]['complete_end_map']:
            at=m['source_offset' if version=='current-source' else 'target_offset'];assert block[at:at+4].hex()==m['source_hex']
            for previous in [0,1,2,3,0xFFFFFFFF]:
                for seed in [0,1,2,3,0xFFFFFFFF]:cases.append(dict(version=version,source_end_offset=m['source_offset'],**env['end_case'](arm,block,at,previous,seed)))
    assert len(cases)==150 and all(c['native_result'][1]==(0 if c['flagged_terminal'] else c['initial_value_word']) for c in cases);ROOT.mkdir(parents=True);save(ROOT/'150_native_terminal_seed_cases_normal_residual_and_flagged_zero.json',dict(relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),cases=cases,case_count=150,three_end_sites_two_versions_five_previous_results_five_value_seeds=True,normal_state0_leaves_existing_value_word_unchanged=True,flagged_00000080_sets_state1_value0=True,all_source_reads_within_four_bytes_and_full_ABI_owner_stream_main_memory_canaries_exact=True,actual_No_state0_residual1_is_expected_not_a_new_opcode_payload=True,no_result_word_normalization_or_source_flag_erasure=True,source_owned_adapter=adapter,no_new_ROM_emulator_run_or_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('150 native end cases pass: normal state0 preserves the existing value word; flagged state1 explicitly sets zero. Source/target four-byte reads and all guards exact.')
