"""Bound the actual dye picture and locate observed state differences at sampled phases only."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
import inspect
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Rafael_B50_actual_focus_v8160')
ACTUAL=Path('work/analysis/Rafael_B50_actual_v8156/paired_source_English_all28_pages_three_names_4821_departure_andreturn.json')
COMPARE=Path('work/analysis/Rafael_B50_actual_comparison_v8157/all_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
RUNS=Path('work/analysis/Rafael_B50_risk_runs_v8159')
FRAMES=[3970,5170,5770,10930,11890,15310,15550,16000]
SHOWN=[3970,5170,5770,10930,15310,16000]

def normalized_rows(trace):
    rows=deepcopy(trace['rows'])
    for r in rows:r['source'].pop('actual_payload_file',None)
    return rows

def regions(arm,raw):
    cpu,get=get_machine(arm,raw)
    values={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
    values['tasks']=dict(bytes=len(values['tasks']),sha256=sha(values['tasks']))
    actor=get(0xCB184);assert get(0x7F244)==0
    values['whole_actor_sha256']=sha(bytes(cpu.mem_read(actor,0x1A04)))
    values['PRNG_seed']=int.from_bytes(raw[0x168EB8:0x168EBC],'little')
    modelbytes=FunctionType(models.__code__,{**models.__globals__,'sha':lambda b:b})(arm,raw)
    persistentbytes={k:raw[v['address']-0x02000000:v['address']-0x02000000+v['bytes']] for k,v in values['persistent_objects'].items()}
    return values,{**modelbytes,**persistentbytes}

if __name__=='__main__':
    assert not ROOT.exists();actual,comparison=map(read,[ACTUAL,COMPARE]);assert not actual['unresolved']
    groups=[];states=[];references=[];sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
    for j,g in enumerate(actual['groups']):
        version=g['version'];folder=RUNS/f'route0_{version}';terminal=read(folder/'terminal.json');plan=read(folder/'run_plan.json')
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace=map(read,[rp,tp])
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        original=read(g['capture_report']);oldtrace=read(g['observer_report'])
        assert plan['inputs_sha256']==g['input_schedule_sha256'] and report['scripted_input_schedule']==original['scripted_input_schedule']
        assert normalized_rows(trace)==normalized_rows(oldtrace)
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        assert report['ROM_sha256']==original['ROM_sha256']==g['fixture']['research_ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        arm=NdsImage.open(g['fixture']['research_ROM']).read_file('/__arm9__.bin')
        assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
        snaps={s['frame']:s for s in report['read_only_capture_RAM_snapshots']};assert list(snaps)==FRAMES
        photos={p['frame']:p for p in report['frames_captured']};oldphotos={p['frame']:p for p in original['frames_captured']}
        samples={};rawregions={}
        for f in FRAMES:
            s=snaps[f];raw=Path(s['path']).read_bytes();assert s['read_only_export'] and len(raw)==4194304 and sha(raw)==s['sha256']
            assert photos[f]['PNG_sha256']==oldphotos[f]['PNG_sha256'] and photos[f]['framebuffer_sha256']==oldphotos[f]['framebuffer_sha256']
            assert sha(Path(photos[f]['path']).read_bytes())==photos[f]['PNG_sha256']
            samples[f],rawregions[f]=regions(arm,raw);samples[f]['snapshot']=s
        final=report['read_only_RAM_snapshot'];oldfinal=original['read_only_RAM_snapshot']
        assert final['sha256']==oldfinal['sha256']==sha(Path(final['path']).read_bytes())
        for i,f in enumerate(SHOWN):
            p=photos[f];draw.text((i*256+3,j*410+3),f'{version} frame{f}',fill='white')
            sheet.paste(Image.open(p['path']).convert('RGB'),(i*256,j*410+24))
        controls=[p for p in g['command_pairs'] if p['canonical_source_offset'] is not None and p['word'] in [0x4821,0xA000,0x4720,0x4681]]
        assert [(c['word'],c['decoded_length']) for c in controls]==[(0x4821,4),(0xA000,8),(0x4720,2),(0x4681,4)]
        assert [c['returned']-c['start'] for c in controls]==[60,240,0,88]
        assert all(c['native_result']==[3,0] for c in controls)
        assert sorted({s['source_selector'] for s in g['speech_observations']})==[0,2,9]
        groups.append(dict(version=version,controls=controls,sampled_native_values=samples,
            original_andrepeat_all_observer_rows_exact_except_output_paths=True,
            all_eight_capture_PNGs_framebuffers_andfinal_whole_RAM_exact_to_first_run=True,
            observer_rows=len(trace['rows']),terminal=str(folder/'terminal.json'),terminal_sha256=sha((folder/'terminal.json').read_bytes())))
        states.append(rawregions);references.extend([folder/'terminal.json',folder/'run_plan.json',rp,tp])
    comparisons=[]
    for f in FRAMES:
        a,b=[g['sampled_native_values'][f] for g in groups];difference={}
        for key in states[0][f]:
            x,y=states[0][f][key],states[1][f][key];assert len(x)==len(y)
            changed=[dict(offset=i,source=u,English=v) for i,(u,v) in enumerate(zip(x,y,strict=True)) if u!=v]
            difference[key]=dict(bytes=len(x),equal=not changed,all_byte_differences=changed)
        comparisons.append(dict(frame=f,component_equality={k:a[k]==b[k] for k in ['state','models','persistent_objects','tasks','calendar','whole_actor_sha256']},
            source_PRNG=a['PRNG_seed'],English_PRNG=b['PRNG_seed'],regions=difference))
    ROOT.mkdir(parents=True);path=ROOT/'paired_dye_picture_hide_return_tutorial_sailing_phases.png';sheet.save(path)
    save(ROOT/'focused_actual_picture_return_andbounded_later_state_risk.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),comparison=str(COMPARE),comparison_sha256=sha(COMPARE.read_bytes()),
        groups=groups,sampled_phase_comparisons=comparisons,sheet=str(path),sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,
        actual_dye_picture_appearance_hide_departure_andnormal_return_preserved=True,
        all28_speeches_three_complete_headers_FAsurname_FIgiven_andcomplete_thoughts_actually_observed=True,
        source_4821_A000_4720_4681_original_effect_bodies_executed_no_opaque_bridge=True,
        no_semantic_inventory_award_ororiginal_event_eligibility_inferred_from_entry_fixture=True,
        source_Japanese_ontranslated_UI_names_not_a_full_clean_ROM=True,
        bounded_comparison_not_every_frame_orcomplete_causal_trace=True,
        no_input_retiming_RAM_seed_roles_roster_funds_condition_orresult_forcing=True,
        later_differences_preserved_not_excused_as_broad_simulation_equivalence=True,
        original_run_frames=32002,additional_focused_risk_frames=32002,total_B50_actual_frames=64004,
        no_new_prose_orcompletion_credit=True,full_goal_complete=False,
        source_owned_native_getters={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar,get_machine]},
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,COMPARE,Path(__file__),*references]}))
    print([(r['frame'],r['component_equality']) for r in comparisons])
    print('Focused actual picture/departure andeight read-only phase snapshots measured;visual andrisk assessment pending.')
