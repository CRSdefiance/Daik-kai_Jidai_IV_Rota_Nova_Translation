"""Measure the real one-step RNG phase difference; bind unchanged original discarded-yield semantics."""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_random_waits_v7897')
ACTUAL=Path('work/analysis/Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json')
COMPARISON=Path('work/analysis/Rafael_B45_actual_comparison_v7896b/12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
PRIOR=Path('work/analysis/ceremony_rand_v822/source_random_yield_cause_v824.json')
SEMANTICS=Path('work/analysis/ceremony_rand_v822/native_yield_control_semantics.json')
def step(value):return (value*1103515245+12345)&0xFFFFFFFF
def distance(before,after,limit=4096):
    value=before
    for n in range(limit+1):
        if value==after:return n
        value=step(value)
    return None
if __name__=='__main__':
    assert not ROOT.exists();actual,comparison,prior,semantics=map(read,[ACTUAL,COMPARISON,PRIOR,SEMANTICS])
    assert not actual['unresolved'] and comparison['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    source,english=[next(g for g in actual['groups'] if g['version']==v) for v in ['clean_Japanese','English']]
    current=NdsImage.open(source['fixture']['research_ROM']).read_file('/__arm9__.bin')
    other=NdsImage.open(english['fixture']['research_ROM']).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    historical=NdsImage.open('out/all_routes_combined_v809_candidate.nds').read_file('/__arm9__.bin')
    assert current==other and sha(current)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    spans=prior['source_clean_spans']
    assert all(current[a:b]==clean[a:b]==historical[a:b] for a,b in spans)
    assert semantics['count']==len(semantics['cases'])==6
    instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(current[0xC9D98:0xC9DF0],0x020C9D98)]
    by={i['address']:i for i in instructions}
    assert (by[0x020C9DA0]['mnemonic'],by[0x020C9DA0]['operands'])==('bl','#0x20d9834')
    assert (by[0x020C9DA8]['mnemonic'],by[0x020C9DA8]['operands'])==('mov','r0, #0')
    seed_address=struct.unpack_from('<I',current,0xD9858)[0]
    assert seed_address==struct.unpack_from('<I',current,0xD9830)[0]==0x02168EB8
    assert struct.unpack_from('<3I',current,0xD985C)==(1103515245,12345,32767)
    rows=[]
    for index,(a,b) in enumerate(zip(source['command_pairs'],english['command_pairs'],strict=True)):
        if a['exchange_command_ordinal'] is None:continue
        assert a['exchange_command_ordinal']==b['exchange_command_ordinal'] and a['word']==b['word']
        counts=[distance(r['before_RNG'],r['after_RNG']) for r in [a,b]]
        assert None not in counts
        if a['word']!=0x4000:assert counts==[0,0]
        phase=distance(a['after_RNG'],b['after_RNG'])
        assert phase in [0,1]
        rows.append(dict(actual_command_index=index,canonical_source_offset=a['canonical_source_offset'],
            original_exchange_command_ordinal=a['exchange_command_ordinal'],word=a['word'],
            source_duration=a['returned']-a['start'],English_duration=b['returned']-b['start'],
            source_LCG_steps=counts[0],English_LCG_steps=counts[1],English_minus_source_step_count=counts[1]-counts[0],
            source_before_seed=a['before_RNG'],English_before_seed=b['before_RNG'],
            source_after_seed=a['after_RNG'],English_after_seed=b['after_RNG'],
            English_ahead_by_exact_original_LCG_steps=phase))
    first=next(r for r in rows if r['English_ahead_by_exact_original_LCG_steps'])
    assert first['canonical_source_offset']==58 and first['word']==0x4000
    assert first['source_before_seed']==first['English_before_seed'] and (first['source_duration'],first['English_duration'])==(237,240)
    assert (first['source_LCG_steps'],first['English_LCG_steps'])==(57,58)
    assert len(rows)==22 and sum(r['English_minus_source_step_count'] for r in rows)==1
    cg=comparison['groups'][0];source_final,English_final=cg['final_PRNG_seeds']
    assert (source_final,English_final)==(2420418440,1937175841) and step(source_final)==English_final
    end_source,end_English=[g['command_pairs'][-1]['after_RNG'] for g in [source,english]]
    post_counts=[distance(a,b) for a,b in [(end_source,source_final),(end_English,English_final)]]
    assert post_counts[0]==post_counts[1] and post_counts[0] is not None
    assert all(cg['five_native_component_equality'].values()) and cg['whole_actors_equal'] and not cg['later_RGB_differences']
    ROOT.mkdir(parents=True);save(ROOT/'actual_one_step_RNG_phase_andunchanged_source_discarded_wait_contract.json',dict(
        actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARISON),comparison_sha256=sha(COMPARISON.read_bytes()),
        current_ARM9_sha256=sha(current),source_bound_spans=[dict(start=a,end=b,sha256=sha(current[a:b])) for a,b in spans],
        native_generator=0x020D9834,original_positive_modulus_wrapper=0x020519D4,seed_word=seed_address,
        original_discarded_yield_callsite=0x020C9DA0,original_overwrite_random_return_with_zero=0x020C9DA8,
        source_current_yield_disassembly=instructions,
        prior_isolated_six_case_discarded_yield_semantics=str(SEMANTICS),prior_isolated_six_case_discarded_yield_semantics_sha256=sha(SEMANTICS.read_bytes()),
        prior_semantics_reused_only_byexact_current_clean_andoriginal_V809_code_equality=True,
        prior_modified_ceremony_probes_not_current_B45_gameplay_ornew_executions=True,
        actual_original_exchange_LCG_intervals=rows,first_measured_phase_difference=first,
        source_andEnglish_final_seeds=[source_final,English_final],English_exactly_one_LCG_step_ahead_at_end_andfinal=True,
        original_exchange_net_additional_English_LCG_steps=1,post_return_equal_LCG_step_counts=post_counts,
        all_non_speech_B45_commands_observed_zero_LCG_steps=True,
        observed_extra_step_consistent_with_original_cooperative_wait_timing=True,
        no_fresh_every_RNG_call_caller_trace_orcomplete_causal_equivalence_claim=True,
        exact_random_state_andfuture_random_outcome_equality_NOT_verified=True,
        source_English_seed_difference_preserved_not_forced_or_hidden=True,
        full_five_measured_components_actor_and157_later_RGB_equal_not_whole_gameplay_equivalence=True,
        later_older_record_technical_reaudit_andthis_measured_limit_retained=True,
        no_ROM_game_code_RAM_seed_input_orcontroller_retiming_change=True,new_emulator_runs=0,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,COMPARISON,PRIOR,SEMANTICS,Path(__file__)]},full_goal_complete=False))
    print('First difference:R9 source237frames/57LCGsteps,English240frames/58steps. One net additional step remains atnormal end/final;later step counts equal. Original discarded-yield code unchanged;future random outcome equality isnot claimed.')
