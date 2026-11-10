"""Add12 relocated predicate cases to24 exactly source-bound predecessor cases."""
from pathlib import Path
import struct
from scripts.prove_lil_B191_predicates_v5362 import probe_mixed
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_predicates_v5379')
SOURCE=Path('work/analysis/lil_B191_source_v5356/all13_clean_current_complete_context.json')
OLD=Path('work/analysis/lil_B191_predicates_v5362/all24_original_mixed_predicate_RNG_ownership_cases.json')
PLAN=Path('work/analysis/lil_B191_relocation_v5377b/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,prior,plan=map(read,[SOURCE,OLD,PLAN]);b=plan['blocks'][0]
    assert prior['source_context_sha256']==sha(SOURCE.read_bytes()) and prior['candidate_sha256']==packet['current_ROM_sha256']==plan['candidate_sha256']
    assert len(prior['cases'])==24 and prior['all24_original_seed_result_and_unowned4MiB_checks_pass']
    block=Path(b['research_block']).read_bytes();assert sha(block)==b['research_block_sha256']
    mapping={c['old_offset']:c['new_offset'] for c in b['command_map']};assert all(mapping[at]==at for at in [8,28,76])
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B191_voices_v5357/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    commands=[c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0x8000];inverse=pow(0x41C64E6D,-1,1<<32);fresh=[]
    for command in commands:
        threshold=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[4:8],'little')
        fixtures={roll:(((roll<<16)-0x3039)*inverse)&0xFFFFFFFF for roll in [threshold-1,threshold,threshold+1]}
        for target,seed in [(None,None),*fixtures.items()]:
            row=ctx.execute(probe_mixed,block,{**command,'offset':mapping[command['offset']]},seed);ctx.machines.pop()
            if target is not None:assert row['roll']==target
            parent=next(r for r in prior['cases'] if r['version']=='current' and r['offset']==command['offset'] and r['supplied_CPU_only_seed_fixture']==seed)
            for key in ['native_result','after_seed','roll','threshold','all_original_native_writes','operand_pointer_unaligned']:assert row[key]==parent[key]
            fresh.append(dict(version='relocated',**row))
    cases=[*prior['cases'],*fresh];assert len(fresh)==12 and len(cases)==36 and not ctx.machines
    assert sum(r['unforced_current_snapshot'] for r in cases)==9 and not any(r['operand_pointer_unaligned'] for r in cases)
    save(ROOT/'all36_original_mixed_predicate_ownership_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,unforced_cases=9,CPU_only_boundary_fixture_cases=27,
        fresh_relocated_cases=12,exact_source_current_reused_cases=24,prior_proof=str(OLD),prior_proof_sha256=sha(OLD.read_bytes()),
        relocation_plan=str(PLAN),relocation_plan_sha256=sha(PLAN.read_bytes()),all_actual_operands_aligned=True,
        source_thresholds_by_offset={'8':500,'28':700,'76':500},actual_emulator_seed_writes=0,
        all36_exact_native_results_seed_writes_and_unowned4MiB_checks_pass=True,
        no_global_RNG_scratch_state_or_ABI_waiver=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('36 exact mixed-predicate cases:12fresh relocated/24source-current hash-bound reuse;9unforced/27CPU boundaries. All three aligned sites and native state guards pass.')
