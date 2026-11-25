"""Original mixed500/700 predicates with exact RNG/operand ownership at each site."""
from pathlib import Path
import inspect,struct
from scripts.prove_lil_B190_predicate500_v5330 import probe500
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B191_predicates_v5362')
SOURCE=Path('work/analysis/lil_B191_source_v5356/all13_clean_current_complete_context.json')

def adapter_source():
    return checked_text(inspect.getsource(probe500),{
        'def probe500(':'def probe_mixed(',
        "assert command['word']==0x8000 and command['whole_command_hex']=='0080fffff4010000' and command['native_extent']==8":
        "assert command['word']==0x8000 and command['whole_command_hex'][:8]=='0080ffff' and command['native_extent']==8\n    threshold=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[4:8],'little');assert threshold in [500,700]\n    assert block[command['offset']:command['offset']+8].hex()==command['whole_command_hex']",
        'roll<500':'roll<threshold','roll==500':'roll==threshold','value=500':'value=threshold',
        "scratch_address-BASE,500":"scratch_address-BASE,threshold",'threshold=500':'threshold=threshold',
        "result_classes='0 when roll<500;1 when equal500;2 when roll>500'":"result_classes='0 below the source threshold;1 equal;2 above'",
    })

_namespace=dict(probe500.__globals__)
exec(compile(adapter_source(),__file__+'::mixed-source-operands','exec'),_namespace)
probe_mixed=_namespace['probe_mixed']

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B191_voices_v5357/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    commands=[c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0x8000]
    assert [(c['offset'],int.from_bytes(bytes.fromhex(c['whole_command_hex'])[4:8],'little')) for c in commands]==[(8,500),(28,700),(76,500)]
    inverse=pow(0x41C64E6D,-1,1<<32);cases=[]
    for version,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        block=IlnkContainer.parse(NdsImage.open(path).read_file('/data/SC2.DK4')).blocks[191]
        for command in commands:
            threshold=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[4:8],'little')
            fixtures={roll:(((roll<<16)-0x3039)*inverse)&0xFFFFFFFF for roll in [threshold-1,threshold,threshold+1]}
            for target,seed in [(None,None),*fixtures.items()]:
                row=ctx.execute(probe_mixed,block,command,seed);ctx.machines.pop()
                if target is not None:assert row['roll']==target
                assert not row['operand_pointer_unaligned'] and not row['unaligned_operand_scratch_writes']
                cases.append(dict(version=version,**row))
    assert len(cases)==24 and sum(r['unforced_current_snapshot'] for r in cases)==6 and not ctx.machines
    for at in [8,28,76]:
        first=[r for r in cases if r['version']=='clean' and r['offset']==at]
        second=[r for r in cases if r['version']=='current' and r['offset']==at]
        assert [(r['native_result'],r['after_seed']) for r in first]==[(r['native_result'],r['after_seed']) for r in second]
    save(ROOT/'all24_original_mixed_predicate_RNG_ownership_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,unforced_cases=6,CPU_only_boundary_fixture_cases=18,
        source_thresholds_by_offset={'8':500,'28':700,'76':500},actual_emulator_seed_writes=0,
        all24_original_seed_result_and_unowned4MiB_checks_pass=True,all_actual_operands_aligned=True,
        source_owned_adapter=adapter_source(),no_source_scheduler_activation_or_gameplay_outcome_claim=True,
        producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('24 original mixed-predicate cases:6unforced/18CPU-only boundary fixtures;all native result classes,exact seed writes and unowned4MiB pass.')
