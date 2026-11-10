"""Bind the measured town difference to the two original selected A000 effects."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_effect_focus_v4814b')
FIXTURE=Path('work/analysis/lil_B180_display_fixture_v4808/complete_B180_B22_fixtures.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

def delta(a,b):
    assert len(a)==len(b)
    return [dict(offset=i,before=x,after=y) for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]

if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)
    arm=NdsImage.open(fixture['parent']).read_file('/__arm9__.bin')
    rows=[];spans=[];finals=[];paths=[FIXTURE,Path(__file__)]
    for f in fixture['fixtures']:
        case=f['case'];focus=BASE/('lil_B180_effect_focus_v4813_'+case);first=BASE/('lil_B180_display_v4810_'+case)
        proofpaths=[focus/'capture_report.json',focus/'observer/commands.json',first/'capture_report.json',first/'observer/commands.json',
            Path('work/analysis/lil_B180_effect_focus_run_v4813_'+case)/'terminal.json']
        report,trace,prior,oldtrace,terminal=map(read,proofpaths);paths.extend(proofpaths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and report['frames']==6001
        assert report['ROM_sha256']==prior['ROM_sha256']==f['research_ROM_sha256'] and sha(Path(f['research_ROM']).read_bytes())==f['research_ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and all(not v for k,v in report.items() if k.startswith('synthetic_'))
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        # The additional observer exports reproduce the original full run exactly
        # through every common command boundary, including the WRAM hash.
        assert len(trace['rows'])<=len(oldtrace['rows'])
        for a,b in zip(trace['rows'],oldtrace['rows'],strict=False):
            stripped={k:v for k,v in a.items() if k!='targeted_readonly_RAM'}
            for current in [stripped,b]:
                source=current['source'];payload=Path(source['actual_payload_file']);assert sha(payload.read_bytes())==source['actual_sha256'];paths.append(payload)
            stripped['source']={**stripped['source'],'actual_payload_file':b['source']['actual_payload_file']}
            assert stripped==b
        selected=[r for r in trace['rows'] if r['kind']=='after_command' and r['source'].get('block')==22
            and r['source']['first_word']==0xA000 and r['source']['instruction_offset']>=56]
        assert len(selected)==1;after=selected[0];before=trace['rows'][after['entry_row']]
        exports=[]
        for r in [before,after]:
            snap=r['targeted_readonly_RAM'];p=Path(snap['path']);raw=p.read_bytes();paths.append(p)
            assert snap['read_only_export'] and len(raw)==snap['bytes']==0x400000 and sha(raw)==snap['sha256']==r['WRAM_sha256']
            exports.append(raw)
        a,b=exports;objects=persistent_objects(arm,a);post=persistent_objects(arm,b);changes={};bounded={}
        for name,obj in objects.items():
            assert obj['address']==post[name]['address'] and obj['bytes']==post[name]['bytes']
            at=obj['address']-0x02000000;n=obj['bytes'];old,new=a[at:at+n],b[at:at+n]
            changes[name]=delta(old,new);bounded[name]=(old,new)
        expected_value=0x013B if case=='clean_Japanese' else 0x013D
        assert changes['all90_towns']==[dict(offset=1294,before=125,after=expected_value&255),dict(offset=1295,before=0,after=1)]
        assert all(not v for k,v in changes.items() if k!='all90_towns')
        source=next(c for c in f['selected_original_objects'] if c['fixture_offset']==before['source']['instruction_offset'])
        assert source['source_offset']==(504 if case=='clean_Japanese' else 472)
        expected_hex='00a0ffff013b0ba1' if case=='clean_Japanese' else '00a0ffff013d0ba1'
        assert source['whole_command_hex']==expected_hex and before['source']['packet_prefix_hex'].startswith(expected_hex)
        assert before['frame']==after['frame'] and before['original_RNG_seed']==after['original_RNG_seed']==985555256
        spans.append(bounded)
        end_snapshot=prior['read_only_RAM_snapshot'];p=Path(end_snapshot['path']);raw=p.read_bytes();paths.append(p)
        assert sha(raw)==end_snapshot['sha256'];finals.append((raw,persistent_objects(arm,raw)))
        rows.append(dict(case=case,source_effect_offset=source['source_offset'],source_effect_hex=expected_hex,
            actual_fixture_offset=before['source']['instruction_offset'],frame=before['frame'],entry=before,returned=after,
            all_four_native_persistent_object_deltas=changes,actual_town_array_word_offset=1294,
            original_town_slot_index=11,original_town_object_field_offset=102,before_word=125,after_word=expected_value,
            packed_effect_bytes_and_original_execution_bound_without_plot_semantics=True,
            all_common_command_boundaries_exact_to_first9001_frame_run=True))
    assert spans[0].keys()==spans[1].keys()
    assert all(spans[0][name][0]==spans[1][name][0] for name in spans[0])
    final_delta={}
    for name,obj in finals[0][1].items():
        other=finals[1][1][name];assert obj['address']==other['address'] and obj['bytes']==other['bytes']
        at=obj['address']-0x02000000;n=obj['bytes']
        final_delta[name]=delta(finals[0][0][at:at+n],finals[1][0][at:at+n])
    assert final_delta['all90_towns']==[dict(offset=1294,before=59,after=61)]
    assert all(not v for k,v in final_delta.items() if k!='all90_towns')
    ROOT.mkdir(parents=True)
    save(ROOT/'two_actual_original_effects_and_exact_one_byte_final_town_difference.json',dict(
        versions=rows,both_pre_effect_all_four_persistent_arrays_byte_identical=True,
        source_effects_write_only_the_two_observed_town_field_bytes_within_four_arrays=True,
        final9001_four_array_differences=final_delta,final_town_difference_is_exact_observed_original_effect_value=True,
        no_full_WRAM_write_ownership_claim=True,no_town_field_plot_or_market_mechanics_inferred=True,
        original_RNG_paths_and_future_world_equivalence_not_forced_or_assumed=True,
        focus_runs=2,frames_each=6001,focus_reason='Resolve concrete persistent-town difference after distinct original random paths.',
        content_sessions_terminal=[41140,20129],focus_sessions_terminal=[29528,42686],
        all_emulator_sessions_exit0=True,no_unresolved_translation_specific_state_difference_within_checked_arrays=True,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Original effects bound:town11 field102 changes125 to315/317;the final persistent difference is exactly that one byte. Other actor/item/goods arrays exact. No forced RNG or plot inference.')
