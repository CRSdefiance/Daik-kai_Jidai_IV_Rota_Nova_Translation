"""Retain strict frame failures and verify explicitly matching update phases.

Translation can change when a cooperative wait yields. Source C9D98 calls RAND
and discards its return on every yield. An all-frame bitwise equality rule is
therefore distinct from faithful source effects at matching native completion.
Neither original strict assertion is deleted or waived by this audit.
"""

import struct
import traceback
from pathlib import Path

from PIL import Image,ImageChops

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ceremony_rand_trace_v822 import ROOT,decode
from scripts.verify_ceremony_random_cause_v823 import native,traces,controlled,load,ram,fingerprint
from scripts.verify_village_wrap_v608 import read,save


def step(seed,n):
    for _ in range(n):seed=(seed*1103515245+12345)&0xFFFFFFFF
    return seed


def main():
    native()
    failures=[]
    for fn in (traces,controlled):
        try:fn()
        except AssertionError as error:
            failures.append(dict(check=fn.__name__,error=repr(error),traceback=traceback.format_exc(),
                original_assertions_unchanged=True))
        else:raise AssertionError('Expected broad strict gate changed; re-audit its scope')
    assert "18233" in failures[0]['error'] and "18220" in failures[1]['error']
    save(ROOT/'retained_strict_frame_gate_failures_v824.json',dict(failures=failures,
        source_checker='scripts/verify_ceremony_random_cause_v823.py',
        source_checker_sha256=sha(Path('scripts/verify_ceremony_random_cause_v823.py').read_bytes()),
        neither_original_assertion_removed_or_waived=True))
    trace_rows=[];differences=[];samples=[]
    for version in (803,809):
        old,of,orr=load(f'ceremony_v{version}_Athens_climb_frame_probe')
        new,nf,nrr=load(f'ceremony_v{version}_post_climb_rand_trace_v822')
        assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
        arm=NdsImage.open(old['ROM']).read_file('/__arm9__.bin')
        seed=struct.unpack_from('<I',ram(orr[18200]),0x168EB8)[0]
        for f in sorted(nrr):
            a,b=ram(orr[f]),ram(nrr[f]);x,y=fingerprint(arm,a),fingerprint(arm,b)
            rng_equal=a[0x168EB8:0x168EBC]==b[0x168EB8:0x168EBC]
            state_equal=x==y
            pixels_equal=None
            if f in of and f in nf:
                pixels_equal=ImageChops.difference(Image.open(of[f]['path']).convert('RGB'),Image.open(nf[f]['path']).convert('RGB')).getbbox() is None
            row=dict(version=version,frame=f,original_PRNG_equal=rng_equal,
                original_full_state_equal=state_equal,complete_screen_equal=pixels_equal,
                original_ticks=x['calendar']['ticks'],traced_ticks=y['calendar']['ticks'])
            trace_rows.append(row)
            if not rng_equal or not state_equal or pixels_equal is False:differences.append(row)
            if f<=18224 or f>=18600:
                assert rng_equal and state_equal and pixels_equal is not False,(version,f,'early or settled trace control failed')
            if f>18200:
                tr=decode(b);assert not tr['unexpected_alternate_header_return']
                assert struct.unpack_from('<I',b,0x168EB8)[0]==step(seed,tr['total_generator_calls'])
                assert all(r['seed_before_generator']==step(seed,r['sequence']-1) for r in tr['last_four_calls'])
                samples.append(dict(version=version,frame=f,**tr))
    assert differences and all(18224<r['frame']<18600 for r in differences)
    indexed={(r['version'],r['frame']):r for r in samples}
    first=indexed[803,18203]['last_four_calls'][0]
    assert indexed[803,18203]['total_generator_calls']==1 and indexed[809,18203]['total_generator_calls']==0
    assert first['callsite']==0x020C9DA0 and first['caller_stack_word']==0x020C9CB0
    assert indexed[803,18600]['total_generator_calls']==860 and indexed[809,18600]['total_generator_calls']==870
    save(ROOT/'phase_scoped_generator_trace_v824.json',dict(controls=trace_rows,transient_observer_differences=differences,
        samples=samples,first_difference=dict(frame=18203,**first),
        all_pre_first_growth_and_settled_controls_equal_uninstrumented=True,
        tracing_is_not_transparent_at_every_intermediate_frame=True,
        first_difference_source_attribution_only_uses_matching_early_controls=True,
        every_counter_and_ring_seed_matches_original_LCG_chain=True,
        four_record_ring_not_a_complete_ordered_every_call_log=True,
        original_strict_frame_failure_retained=True))
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');spans=((0x519D4,0x51A28),(0xD9824,0xD9868),
        (0xC9C8C,0xC9CF8),(0xC9D98,0xC9DF0),(0xB6FAC,0xB7010),(0x610FC,0x61C18))
    for version in (803,809,820):
        arm=NdsImage.open(f'out/all_routes_combined_v{version}_candidate.nds').read_file('/__arm9__.bin')
        assert all(arm[a:b]==clean[a:b] for a,b in spans)
    # All static ARM BL references in the initial source code go through the
    # positive-modulus wrapper or the discarded scheduler call. This is not
    # an assertion about arbitrary indirect calls/overlays.
    calls=read(ROOT/'source_direct_generator_callsites.json')['direct_ARM_BL_callsites']
    assert calls==[0x02051A0C,0x020C9DA0]
    save(ROOT/'source_random_yield_cause_v824.json',dict(source_clean_spans=[list(p) for p in spans],
        all_spans_byte_exact_in_V803_V809_V820=True,
        original_generator=0x020D9834,positive_modulus_wrapper=0x020519D4,
        discarded_generator_callsite=0x020C9DA0,
        source_overwrites_generator_return_with_zero_at=0x020C9DA8,
        observed_parent_input_mask_and_event_wait_yield_callsite=0x020C9CAC,
        observed_post_return_town_wait_yield_callsite=0x020B6FE0,
        first_ordinary_random_divergence_explained_by_discarded_source_wait_yield=True,
        ordinary_exact_random_outcome_equality_not_claimed=True))
    runs={v:load(f'ceremony_v{v}_yield_control_v823') for v in (803,809,820)}
    arms={v:NdsImage.open(runs[v][0]['ROM']).read_file('/__arm9__.bin') for v in runs}
    reference=runs[803][0];equal=[];in_progress=[]
    for v,(d,_,_) in runs.items():
        assert d['scripted_input_schedule']==reference['scripted_input_schedule'] and d['core_options']==reference['core_options']
        selected=[r for r in d['synthetic_condition_fixtures'] if r.get('synthetic_discarded_yield_RAND_control')]
        assert len(selected)==1 and selected[0]['frame']==18200
        assert selected[0]['only4_instruction_bytes_change_no_seed_or_persistent_data_supplied']
    common=set.intersection(*(set(r[2]) for r in runs.values()))
    start=33214;end=start+192
    for f in sorted(common):
        raw={v:ram(runs[v][2][f]) for v in runs};states={v:fingerprint(arms[v],raw[v]) for v in runs}
        same=states[803]==states[809]==states[820]
        rng_same=len({raw[v][0x168EB8:0x168EBC] for v in raw})==1
        ticks={v:states[v]['calendar']['ticks'] for v in states}
        if f<=18200 or f>=18600:
            assert same and rng_same,(f,'matching input/settled phase differs')
            equal.append(dict(frame=f,all_three_complete_state_families_and_PRNG_equal=True,ticks=ticks[820]))
        else:
            # These two deliberately sampled points are at different original
            # calendar-update progress, so no same-phase equality is claimed.
            assert len(set(ticks.values()))>1 and all(start<=t<end for t in ticks.values())
            in_progress.append(dict(frame=f,ticks=ticks,complete_states_equal=same,PRNG_equal=rng_same,
                all_versions_inside_original_four_day_update=True,not_same_native_update_phase=True))
    assert {r['frame'] for r in in_progress}=={18220,18240}
    post={r['frame']:r for r in equal}
    assert post[18600]['ticks']-post[18200]['ticks']==192 and 20000 in post
    save(ROOT/'matching_phase_yield_control_v824.json',dict(matching_phase_cases=equal,count=len(equal),
        explicitly_different_in_progress_phases=in_progress,versions=[803,809,820],
        full_actor_town_item_goods_models_tasks_funds_calendar_and_PRNG_equal_after_completion=True,
        original_four_day192_tick_advance_and_return_verified=True,
        only_discarded_scheduler_RAND_advance_omitted_no_seed_or_outcome_supplied=True,
        no_production_ROM_patch_or_registry_change=True,
        original_unmodified_ROM_strict_gate_still_fails_because_source_random_inputs_differ=True,
        causal_control_does_not_claim_identical_uncontrolled_random_outcomes=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'{len(trace_rows)} trace points audited;{len(differences)} transient observer differences retained. '
          f'{len(equal)} matching-phase3-version complete-state/PRNG controls pass;source RNG cause mapped.',flush=True)


if __name__=='__main__':main()
