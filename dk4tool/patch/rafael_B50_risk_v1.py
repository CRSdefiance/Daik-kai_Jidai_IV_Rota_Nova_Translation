"""Independently recompute B50 bounded risk values from captured read-only RAM and frames."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.focus_Rafael_B50_picture_risk_v8160 import regions,normalized_rows,FRAMES
from scripts.verify_village_wrap_v608 import read

def require(value,label):
    if not value:raise ValueError('Rafael B50 editorial contract: bounded risk '+label)

def check_bounded_risk(focus,actual,later):
    require(focus['original_run_frames']==32002 and focus['additional_focused_risk_frames']==32002 and focus['total_B50_actual_frames']==64004,'capture scopes')
    require(focus['source_4821_A000_4720_4681_original_effect_bodies_executed_no_opaque_bridge'] and focus['bounded_comparison_not_every_frame_orcomplete_causal_trace'] and focus['later_differences_preserved_not_excused_as_broad_simulation_equivalence'],'scope limitations')
    require(focus['no_input_retiming_RAM_seed_roles_roster_funds_condition_orresult_forcing'] and focus['no_semantic_inventory_award_ororiginal_event_eligibility_inferred_from_entry_fixture'],'unforced entry limits')
    require(len(focus['groups'])==2 and [g['version'] for g in focus['groups']]==['clean_Japanese','English'],'source English groups')
    computed=[]
    for group in focus['groups']:
        original=next(g for g in actual['groups'] if g['version']==group['version'])
        terminal=read(group['terminal']);require(sha(Path(group['terminal']).read_bytes())==group['terminal_sha256'],'terminal digest')
        require(terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored'],'terminal limits')
        report,trace=read(terminal['report']),read(terminal['observer'])
        require(sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'] and sha(Path(terminal['observer']).read_bytes())==terminal['observer_sha256'],'repeat capture digests')
        oldreport,oldtrace=read(original['capture_report']),read(original['observer_report'])
        require(normalized_rows(trace)==normalized_rows(oldtrace) and group['observer_rows']==len(trace['rows']),'whole original/repeat trace equality')
        require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'readonly trace integrity')
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'],'coldboot limits')
        require(report['ROM_sha256']==oldreport['ROM_sha256']==original['fixture']['research_ROM_sha256'],'same fixture identity')
        require(report['scripted_input_schedule']==oldreport['scripted_input_schedule'] and not any(v for k,v in report.items() if k.startswith('synthetic_')),'identical inputs/no synthetic state')
        arm=NdsImage.open(original['fixture']['research_ROM']).read_file('/__arm9__.bin')
        photos={p['frame']:p for p in report['frames_captured']};oldphotos={p['frame']:p for p in oldreport['frames_captured']}
        snapshots={s['frame']:s for s in report['read_only_capture_RAM_snapshots']}
        require(list(snapshots)==FRAMES and set(map(int,group['sampled_native_values']))==set(FRAMES),'eight exact phases')
        sample={}
        for frame in FRAMES:
            snapshot=snapshots[frame];raw=Path(snapshot['path']).read_bytes()
            require(snapshot['read_only_export'] and len(raw)==snapshot['bytes'] and sha(raw)==snapshot['sha256'],'sample export hash')
            require(photos[frame]['PNG_sha256']==oldphotos[frame]['PNG_sha256']==sha(Path(photos[frame]['path']).read_bytes()) and photos[frame]['framebuffer_sha256']==oldphotos[frame]['framebuffer_sha256'],'same phase framebuffer')
            values,ownedregions=regions(arm,raw);values['snapshot']=snapshot
            require(values==group['sampled_native_values'][str(frame)],'independently recomputed native values')
            sample[frame]=(values,ownedregions)
        require(report['read_only_RAM_snapshot']['sha256']==oldreport['read_only_RAM_snapshot']['sha256']==sha(Path(report['read_only_RAM_snapshot']['path']).read_bytes()),'deterministic final whole RAM')
        computed.append(sample)
    require(len(focus['sampled_phase_comparisons'])==8,'all comparison rows')
    for index,frame in enumerate(FRAMES):
        row=focus['sampled_phase_comparisons'][index];require(row['frame']==frame,'comparison phase ordering')
        (a,ar),(b,br)=[c[frame] for c in computed]
        equality={key:a[key]==b[key] for key in ['state','models','persistent_objects','tasks','calendar','whole_actor_sha256']}
        require(row['component_equality']==equality and row['source_PRNG']==a['PRNG_seed'] and row['English_PRNG']==b['PRNG_seed'],'sampled component/PRNG equality metadata')
        require(set(row['regions'])==set(ar)==set(br),'all sampled regions')
        for key,x in ar.items():
            y=br[key];require(len(x)==len(y),'region sizes')
            changes=[dict(offset=i,source=u,English=v) for i,(u,v) in enumerate(zip(x,y,strict=True)) if u!=v]
            require(row['regions'][key]==dict(bytes=len(x),equal=not changes,all_byte_differences=changes),'all recomputed region byte differences')
        if index<7:require(all(equality.values()),'seven equal early/postreturn/tutorial/departure samples')
        else:
            require(equality==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True,whole_actor_sha256=False),'later underway differences retained')
            require({k:len(v['all_byte_differences']) for k,v in row['regions'].items() if not v['equal']}==dict(fleet=2,ship_0=1,all207_actors_and_current_captain=105,all90_towns=2),'all later exact changed-byte counts')
    require(later['groups'][0]['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True) and not later['groups'][0]['whole_actors_equal'],'later final comparison limits')
