"""Validate source-bound traces and the separate discarded-RAND causal control.

Original unmodified-ROM exact-world-state failures remain recorded. This probe
can establish equal simulation under controlled scheduler entropy; it cannot
claim that distinct unmodified text schedules produce identical random results.
"""

import argparse
import itertools
import struct
from pathlib import Path

from PIL import Image,ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.native_ceremony_rand_trace_v822 import assembled,decode,BASE,ROOT
from scripts.native_ceremony_yield_control_v823 import AT
from scripts.verify_ceremony_families_gameplay_v815 import state,models,persistent_objects,tasks,calendar
from scripts.verify_village_wrap_v608 import read,save

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
DONOR='a9e58e5b96a86d98ca23eacd9da4ac9572052d400dad7e1ffc4e34bc0e719db4'


def native():
    arm=NdsImage.open('out/all_routes_combined_v809_candidate.nds').read_file('/__arm9__.bin')
    new=bytearray(arm)
    for at,code in assembled().items():new[at-BASE:at-BASE+len(code)]=code
    cases=[]
    for entry,seed,n in itertools.product((0xD9834,0x519D4),(0,3946971496,0xFFFFFFFF),(-1,0,1,2,100,0x7FFFFFFF)):
        outputs=[]
        for data in (arm,bytes(new)):
            u=machine(data);u.mem_write(0x02168EB8,struct.pack('<I',seed))
            call(u,entry,(n&0xFFFFFFFF,))
            outputs.append((u.reg_read(UC_ARM_REG_R0),bytes(u.mem_read(BASE,0x800000))))
        a,b=outputs;assert a[0]==b[0]
        restored=bytearray(b[1])
        for at,code in assembled().items():restored[at-BASE:at-BASE+len(code)]=a[1][at-BASE:at-BASE+len(code)]
        restored[0x7EFF00:0x7F0000]=a[1][0x7EFF00:0x7F0000]
        assert bytes(restored)==a[1]
        trace=decode(b[1]);assert trace['total_generator_calls']==int(entry==0xD9834 or n>0)
        assert not trace['unexpected_alternate_header_return']
        cases.append(dict(entry=entry,seed=seed,modulus=n,output=a[0],
            ABI_PRNG_and_entire8MiB_outside_owned_code_and_stack_equal=True))
    save(ROOT/'native_trace_equivalence.json',dict(count=len(cases),cases=cases,
        source_ARM9_sha256=sha(arm),fixture_sha256=sha(Path('scripts/native_ceremony_rand_trace_v822.py').read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),actual_trace_timing_controls_required=True))
    controlled=bytearray(arm);controlled[AT-BASE:AT-BASE+4]=bytes.fromhex('0000a0e1')
    manager=struct.unpack_from('<I',arm,0xC9DE4)[0];object_at=0x02430000;cases=[]
    for mode,seed in itertools.product((1,5),(0,3946971496,0xFFFFFFFF)):
        outputs=[]
        for data in (arm,bytes(controlled)):
            u=machine(data);u.mem_write(manager+0x54,struct.pack('<I',mode))
            u.mem_write(object_at,bytes(0x100));u.mem_write(object_at+0x48,struct.pack('<I',1))
            u.mem_write(0x02168EB8,struct.pack('<I',seed));call(u,0xC9D98,(object_at,))
            outputs.append((u.reg_read(UC_ARM_REG_R0),bytes(u.mem_read(BASE,0x800000))))
        a,b=outputs;assert a[0]==b[0]==0
        assert struct.unpack_from('<I',a[1],0x168EB8)[0]==(seed*1103515245+12345)&0xFFFFFFFF
        assert struct.unpack_from('<I',b[1],0x168EB8)[0]==seed
        restored=bytearray(b[1]);restored[AT-BASE:AT-BASE+4]=a[1][AT-BASE:AT-BASE+4]
        restored[0x168EB8:0x168EBC]=a[1][0x168EB8:0x168EBC]
        assert bytes(restored)==a[1]
        cases.append(dict(manager_state=mode,seed=seed,source_return_and_ABI_preserved=True,
            only_instruction_and_discarded_PRNG_step_differ_entire8MiB=True))
    save(ROOT/'native_yield_control_semantics.json',dict(cases=cases,count=len(cases),
        source_return_value_zero_and_callee_saved_registers_exact=True,
        actual_cooperative_scheduling_not_exercised_by_this_unit_probe=True))
    print('36 direct RAND/wrapper contracts and6 discarded-step semantics controls pass.',flush=True)


def load(name):
    folder=CAP/name;report=read(folder/'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames']==20000 and report['core_DLL_sha256']=='42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    donor=report['battery_save_preloaded'];assert donor['source_sha256']==DONOR==sha(Path(donor['source']).read_bytes())
    assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    pictures={r['frame']:r for r in report['frames_captured']}
    for row in pictures.values():assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    records={r['frame']:r for k in ('read_only_capture_RAM_snapshots','read_only_pause_RAM_snapshots') for r in report.get(k,[])}
    return report,pictures,records


def ram(record):
    raw=Path(record['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==record['sha256']
    return raw


def fingerprint(arm,raw):
    return {fn.__name__:fn(arm,raw) for fn in (state,models,persistent_objects,tasks,calendar)}


def traces():
    controls=[];samples=[]
    def step(seed,n):
        for _ in range(n):seed=(seed*1103515245+12345)&0xFFFFFFFF
        return seed
    for version in (803,809):
        old,of,orr=load(f'ceremony_v{version}_Athens_climb_frame_probe')
        new,nf,nrr=load(f'ceremony_v{version}_post_climb_rand_trace_v822')
        assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
        arm=NdsImage.open(old['ROM']).read_file('/__arm9__.bin')
        initial_seed=struct.unpack_from('<I',ram(orr[18200]),0x168EB8)[0]
        for f in sorted(nrr):
            a,b=ram(orr[f]),ram(nrr[f])
            assert a[0x168EB8:0x168EBC]==b[0x168EB8:0x168EBC],(version,f,'trace changes original PRNG')
            assert fingerprint(arm,a)==fingerprint(arm,b),(version,f,'trace changes original persistent state')
            if f in of and f in nf:
                assert ImageChops.difference(Image.open(of[f]['path']).convert('RGB'),Image.open(nf[f]['path']).convert('RGB')).getbbox() is None
            if f>18200:
                trace=decode(b);assert not trace['unexpected_alternate_header_return']
                assert struct.unpack_from('<I',b,0x168EB8)[0]==step(initial_seed,trace['total_generator_calls'])
                for r in trace['last_four_calls']:
                    assert r['seed_before_generator']==step(initial_seed,r['sequence']-1)
                samples.append(dict(version=version,frame=f,**trace))
            controls.append(dict(version=version,frame=f,original_PRNG_all_persistent_objects_and_available_complete_screens_equal=True))
    indexed={(r['version'],r['frame']):r for r in samples}
    assert indexed[803,18203]['total_generator_calls']==1 and indexed[809,18203]['total_generator_calls']==0
    first=indexed[803,18203]['last_four_calls'][0]
    assert first['callsite']==0x020C9DA0 and first['caller_stack_word']==0x020C9CB0
    assert indexed[803,18600]['total_generator_calls']==860 and indexed[809,18600]['total_generator_calls']==870
    save(ROOT/'validated_actual_generator_traces.json',dict(controls=controls,count=len(controls),samples=samples,
        first_divergence_frame=18203,first_caller=first,
        exact_original_generator_counts_at18600={'803':860,'809':870},
        all_observed_PRNG_states_and_persistent_states_preserve_uninstrumented_runs=True,
        every_observed_generator_counter_and_ring_seed_matches_original_LCG_chain=True,
        four_record_ring_is_not_a_complete_every_call_log=True,
        no_unexpected_use_of_repurposed_alternate_header=True,
        production_ROMs_and_saves_unmodified=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print(f'{len(controls)} actual trace controls preserve original PRNG/state;first difference is discarded scheduler RAND in the input-release loop.',flush=True)


def controlled():
    runs={v:load(f'ceremony_v{v}_yield_control_v823') for v in (803,809,820)}
    arms={v:NdsImage.open(runs[v][0]['ROM']).read_file('/__arm9__.bin') for v in runs}
    reference=runs[803][0];rows=[]
    common=set.intersection(*(set(r[2]) for r in runs.values()))
    for v,(d,_,_) in runs.items():
        assert d['scripted_input_schedule']==reference['scripted_input_schedule'] and d['core_options']==reference['core_options']
        fixes=d['synthetic_condition_fixtures'];assert sum(r.get('synthetic_discarded_yield_RAND_control',False) for r in fixes)==1
        assert next(r for r in fixes if r.get('synthetic_discarded_yield_RAND_control'))['frame']==18200
    for f in sorted(common):
        raw={v:ram(runs[v][2][f]) for v in runs}
        states={v:fingerprint(arms[v],raw[v]) for v in runs}
        assert states[803]==states[809]==states[820],(f,'controlled actor/town/etc state differs')
        assert len({raw[v][0x168EB8:0x168EBC] for v in raw})==1,(f,'controlled PRNG differs')
        rows.append(dict(frame=f,all_three_versions_persistent_objects_models_tasks_funds_calendar_and_PRNG_equal=True,
            ticks=states[820]['calendar']['ticks']))
    indexed={r['frame']:r for r in rows}
    assert indexed[18600]['ticks']-indexed[18200]['ticks']==192
    assert all(r['frame'] in indexed for r in (dict(frame=18200),dict(frame=18600),dict(frame=20000)))
    save(ROOT/'controlled_yield_world_state_v823.json',dict(cases=rows,count=len(rows),versions=[803,809,820],
        only_source_discarded_scheduler_RAND_call_omitted_after18200=True,
        no_seed_actor_town_or_outcome_values_supplied=True,
        four_day192_tick_native_advance_and_all_original_state_updates_equal=True,
        original_uncontrolled_exact_state_gate_retained_failed_not_waived=True,
        controlled_causal_evidence_not_ordinary_random_outcome_equivalence=True,
        no_production_patch_registry_or_source_ROM_changes=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'{len(rows)} controlled3-version state/PRNG pairs pass,including the original4-day advance.',flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--phase',choices=('native','captures','all'),default='all');args=p.parse_args()
    if args.phase in ('native','all'):native()
    if args.phase in ('captures','all'):
        traces()
        controlled()


if __name__=='__main__':main()
