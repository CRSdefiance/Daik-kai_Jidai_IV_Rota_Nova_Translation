"""Bound the focused introduction's measured timing/RNG difference with exact same-input replay and eight RAM phases."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.focus_Rafael_B50_picture_risk_v8160 import normalized_rows,regions as prior_regions
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_intro_actual_focus_v8232')
ACTUAL=Path('work/analysis/Gerhard_actual_v8229/six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json')
COMPARE=Path('work/analysis/Gerhard_actual_comparison_v8230b/three_actual_pairs_scene_timing_RNG_final_components_later_RGB_scope.json')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
RUNS=Path('work/analysis/Gerhard_intro_risk_runs_v8231')
FRAMES=[3970,4330,4810,5770,6310,9730,10510,12000]
SHOWN=[3970,4810,5770,6310,10510,12000]
if __name__=='__main__':
    assert not ROOT.exists();actual,comparison,reference=map(read,[ACTUAL,COMPARE,REFERENCE]);assert not actual['unresolved']
    adapter=checked_text(inspect.getsource(prior_regions),{'assert get(0x7F244)==0':'assert get(0x7F244)==2'})
    env=dict(prior_regions.__globals__);exec(compile(adapter,__file__+'::own-Lil-disposable-native-components','exec'),env)
    originals=[next(g for g in actual['groups'] if g['scope']=='intro-display' and g['version']==v) for v in ['parent_English','revised_English']]
    groups=[];rawgroups=[];proofpaths=[];sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
    for row,g in enumerate(originals):
        version=g['version'];folder=RUNS/f'route2_B27_{version}';terminal,plan=map(read,[folder/'terminal.json',folder/'run_plan.json'])
        assert terminal['terminal'] and terminal['frames']==12001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace=map(read,[rp,tp]);old=read(g['capture_report']);oldterminal=read(g['terminal']);oldtrace=read(oldterminal['observer'])
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['scripted_input_schedule']==old['scripted_input_schedule'] and report['frames']==old['frames']==12001
        assert normalized_rows(trace)==normalized_rows(oldtrace) and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        assert report['ROM_sha256']==old['ROM_sha256']==g['fixture']['research_ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        arm=NdsImage.open(g['fixture']['research_ROM']).read_file('/__arm9__.bin');assert sha(arm)==reference['current_ARM9_sha256' if version=='parent_English' else 'research_ARM9_sha256']
        snaps={s['frame']:s for s in report['read_only_capture_RAM_snapshots']};assert list(snaps)==FRAMES
        photos={p['frame']:p for p in report['frames_captured']};oldphotos={p['frame']:p for p in old['frames_captured']}
        samples={};rawregions={}
        for frame in FRAMES:
            snap=snaps[frame];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
            assert photos[frame]['PNG_sha256']==oldphotos[frame]['PNG_sha256'] and photos[frame]['framebuffer_sha256']==oldphotos[frame]['framebuffer_sha256']
            assert sha(Path(photos[frame]['path']).read_bytes())==photos[frame]['PNG_sha256']
            samples[frame],rawregions[frame]=env['regions'](arm,raw);samples[frame]['snapshot']=snap
        final=report['read_only_RAM_snapshot'];oldfinal=old['read_only_RAM_snapshot'];assert final['sha256']==oldfinal['sha256']==sha(Path(final['path']).read_bytes())
        for n,frame in enumerate(SHOWN):
            p=photos[frame];draw.text((n*256+3,row*410+3),f'{version} frame{frame}',fill='white');sheet.paste(Image.open(p['path']).convert('RGB'),(n*256,row*410+24))
        groups.append(dict(version=version,sampled_native_values=samples,original_andrepeat_all_observer_rows_exact_except_output_paths=True,
            all8_capture_PNGs_framebuffers_andfinal_whole_RAM_exact_to_initial_run=True,observer_rows=len(trace['rows']),
            terminal=str(folder/'terminal.json'),terminal_sha256=sha((folder/'terminal.json').read_bytes())))
        rawgroups.append(rawregions);proofpaths.extend([folder/'terminal.json',folder/'run_plan.json',rp,tp])
    phasepairs=[]
    for frame in FRAMES:
        a,b=[g['sampled_native_values'][frame] for g in groups];differences={}
        for key in rawgroups[0][frame]:
            x,y=rawgroups[0][frame][key],rawgroups[1][frame][key];assert len(x)==len(y)
            changed=[dict(offset=i,parent=p,revised=q) for i,(p,q) in enumerate(zip(x,y,strict=True)) if p!=q]
            differences[key]=dict(bytes=len(x),changed_bytes=len(changed),changes=changed,parent_sha256=sha(x),revised_sha256=sha(y))
        equality={k:a[k]==b[k] for k in ['state','models','persistent_objects','tasks','calendar','whole_actor_sha256']}
        phasepairs.append(dict(frame=frame,component_equality=equality,parent_PRNG_seed=a['PRNG_seed'],revised_PRNG_seed=b['PRNG_seed'],
            bounded_native_model_andpersistent_byte_differences=differences,raw_calendar_values=[a['calendar'],b['calendar']],
            raw_calendar_date_values_not_interpreted_as_real_dates=True))
        print('PHASE',frame,'equal',equality,'RNG',a['PRNG_seed'],b['PRNG_seed'],'changed',{k:v['changed_bytes'] for k,v in differences.items() if v['changed_bytes']},flush=True)
    ROOT.mkdir(parents=True);path=ROOT/'eight_RAM_phases_six_unmasked_parent_revised_frames.png';sheet.save(path)
    save(ROOT/'exact_intro_replay8_RAM_phases_bounded_later_state_andRNG_differences.json',dict(
        actual=str(ACTUAL),actual_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),groups=groups,sampled_comparisons=phasepairs,
        all_same_ROM_input_horizon_observer_rows_selected_framebuffers_andfinal_RAM_reproduce_exactly_perversion=True,
        original_andrepeat_intro_normal_returns=[g['normal_return'] for g in originals],
        all8_RAM_samples_readonly_without_flag_result_seed_roster_role_funds_orinput_forcing=True,
        source_owned_native_regions_adapter=adapter,declared_RAM_sample_frames=FRAMES,
        measured_later_differences_retained_without_everyframe_causality_futureoutcome_orbroad_simulation_claim=True,
        original_full_B27_production_branch_conditions_NOT_executed_bythis_focused_display_fixture=True,
        full_Hamburg_primary_fixture_has_equal_final5components_actors_seed_and164_later_RGB_samples=True,
        full_B27_initialized_tail_captain0_andSC0_B44_is_a_separate_fixture_limit_not_natural_Lilcontinuity=True,
        later_older_record_technical_reaudit_keeps_all_timing_RNG_component_byte_andfixture_limits=True,
        review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),visual_review_pending=True,
        new_credit=0,new_emulator_runs=2,new_actual_frames=24002,total_Gerhard_scene_frames_including_replay=176008,
        full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,COMPARE,REFERENCE,Path(__file__),*proofpaths]}))
    print('Exact focused replay/8RAMphase proof complete;bounded differences retained,not broad simulation equivalence;directview pending.')
