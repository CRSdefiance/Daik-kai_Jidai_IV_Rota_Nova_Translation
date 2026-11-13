"""Bind original live FE typed descriptors, palette and full held bitmap to exact native models."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.trace_file_ids_v683 import mapped_read
from scripts.actual_Hodram_FE_VRAM_v8338b import read_bitmap
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_FE_binding_v8420')
RUNS=Path('work/analysis/Hodram_B49_FE_runs_v8419')
MODELS=Path('work/analysis/Hodram_B49_models_v8408/native_models.json')
BASE=0x02000000

def rgb(value):
    red=value&31;green=(value>>5)&31;blue=(value>>10)&31
    green6=(green<<1)|(green>>4)
    return red*255//31,green6*255//63,blue*255//31

if __name__=='__main__':
    assert not ROOT.exists();models=read(MODELS);groups=[];evidence={str(MODELS):sha(MODELS.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for version in ['clean_Japanese','revised_English']:
        folder=RUNS/version;terminal=read(folder/'terminal.json');plan=read(folder/'run_plan.json');rp,op=Path(terminal['report']),Path(terminal['observer']);report,observer=map(read,[rp,op])
        assert terminal['terminal'] and terminal['frames']==4931 and terminal['exactly_one_complete_original_FE_paint_CPU_WRAM_DTCM_ITCM_snapshot'] and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==terminal['observer_sha256'] and sha((folder/'run_plan.json').read_bytes())==terminal['run_plan_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
        captured=[r for r in observer['rows'] if 'complete_readonly_snapshots' in r];assert len(captured)==1;row=captured[0]
        assert row['kind']=='modal_paint' and row['text_hex']==plan['exact_expanded_FE_body_hex'] and row['CPU_all4MiB_DTCM_ITCM_and_configuration_unchanged_by_callback']
        data={}
        for name,ref in row['complete_readonly_snapshots'].items():
            raw=Path(ref['path']).read_bytes();assert len(raw)==ref['bytes'] and sha(raw)==ref['sha256'];data[name]=raw
        assert len(data['WRAM'])==0x400000 and len(data['DTCM'])==0x4000 and len(data['ITCM'])==0x8000 and len(data['CPU'])==128
        memory=lambda address,length:mapped_read(data['WRAM'],data['DTCM'],row['DTCM_base'],address,length)
        context=list(struct.unpack('<19I',bytes.fromhex(row['context_76_hex'])));view=list(struct.unpack('<25I',bytes.fromhex(row['bitmap_100_hex'])));font=list(struct.unpack('<6I',bytes.fromhex(row['font_object_24_hex'])))
        assert memory(row['context'],76).hex()==row['context_76_hex'] and memory(row['bitmap'],100).hex()==row['bitmap_100_hex'] and memory(row['font_metrics_object'],24).hex()==row['font_object_24_hex']
        assert context[1:6]==[0,0,228,48,1] and context[11]==row['bitmap'] and view[10:16]==[228,48,0,0,228,48] and view[18:20]==[0,0] and font[1:3]==[6,12]
        header=list(struct.unpack('<5I',memory(view[4],20)));assert header[:3]==[4,72,48]
        palette_address=(view[4]+header[3])&0xFFFFFFFF;palette=memory(palette_address,32);colors=[rgb(v) for v in struct.unpack('<16H',palette)];assert colors[15]==(0,8,0) and colors[14]==(197,198,197)
        image=NdsImage.open(plan['research_ROM']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==models['ARM9_sha256'] and sha(Path(plan['research_ROM']).read_bytes())==plan['research_ROM_sha256']==report['ROM_sha256']
        vtables=[]
        for pointer in [context[0],view[0],view[20],font[0],font[5]]:
            assert BASE<=pointer<BASE+len(arm)-32 and memory(pointer,32)==arm[pointer-BASE:pointer-BASE+32];vtables.append(dict(address=pointer,bytes=32,sha256=sha(memory(pointer,32))))
        model=next(m for m in models['native_models'][version] if m['source_selector']==254);page=model['pages'][0];wanted=Path(page['native_plane']).read_bytes();assert len(wanted)==228*48 and sha(wanted)==page['native_plane_sha256']
        full=Path('work/analysis/Hodram_B49_tail_runs_v8416')/f'route1_{version}_accept';fullterminal=read(full/'terminal.json');fullreport=read(fullterminal['report']);photos={p['frame']:p for p in report['frames_captured']};otherphotos={p['frame']:p for p in fullreport['frames_captured']};holds=[]
        assert report['scripted_input_schedule']==[e for e in fullreport['scripted_input_schedule'] if e['start']<=4930]
        for snap in report['read_only_capture_RAM_snapshots']:
            frame=snap['frame'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==0x400000 and sha(raw)==snap['sha256'] and frame in [4870,4930]
            def readram(address,length):
                at=address-BASE;assert 0<=at and at+length<=len(raw);return raw[at:at+length]
            # The original context is a paint-call stack object; its storage is
            # reused after the call. The held view, bitmap and palette persist.
            paint_context_storage_reused=readram(row['context'],76).hex()!=row['context_76_hex']
            assert readram(row['bitmap'],100).hex()==row['bitmap_100_hex'] and readram(view[4],20)==struct.pack('<5I',*header) and readram(palette_address,32)==palette
            stored,vram_binding=read_bitmap(fullreport,frame,header,view[4]);pixels=bytes(v for b in stored for v in [b&15,b>>4]);logical=bytes(pixels[y*288+x] for y in range(48) for x in range(228));assert logical==wanted
            photo=photos[frame];assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'] and Path(photo['path']).read_bytes()==Path(otherphotos[frame]['path']).read_bytes()
            rgbimage=Image.open(photo['path']).convert('RGB');physical=Path(page['physical_plane']).read_bytes();assert sha(physical)==page['physical_plane_sha256'];matches=0
            for i,index in enumerate(physical):
                if index:assert rgbimage.getpixel((16+i%228,296+i//228))==colors[index];matches+=1
            holds.append(dict(frame=frame,RAM_snapshot=snap,capture=photo,whole_PNG_equal_to_completed_original_command_trace_run=True,complete_actual_bitmap_228x48_equals_independent_native_plane=True,all_native_ink_indices_match_actual_palette_andRGB=True,matched_ink_pixels=matches,original_paint_context_stack_storage_reused_after_paint=paint_context_storage_reused,persistent_view_bitmap_header_andpalette_exact=True,actual_bitmap_VRAM_binding=vram_binding))
        assert len(holds)==2
        groups.append(dict(version=version,actual_FE_paint_frame=row['frame'],captured_original_context=row['context_76_hex'],captured_original_bitmap_view=row['bitmap_100_hex'],captured_original_header=header,captured_original_font_metrics=row['font_object_24_hex'],original_typed_geometry_228x48_stride288_logical6x12_physical16pitch=True,
            palette_address=palette_address,palette_hex=palette.hex(),palette15_RGB=colors[15],palette14_RGB=colors[14],exact_current_source_vtables=vtables,complete_paint_snapshot=row['complete_readonly_snapshots'],complete_actual_holds=holds,
            original_native_source_consumer_not_geometry_inferred_from_incidental_r1=True))
        for p in [folder/'terminal.json',folder/'run_plan.json',rp,op,full/'terminal.json']:evidence[str(p)]=sha(p.read_bytes())
    assert groups[0]['palette_hex']==groups[1]['palette_hex'] and groups[0]['captured_original_font_metrics']==groups[1]['captured_original_font_metrics']
    ROOT.mkdir(parents=True);save(ROOT/'two_original_FE_paint_snapshots_four_exact_bitmap_palette_RGB_holds.json',dict(groups=groups,focused_actual_frames=9862,whole_scene_tests_not_repeated=True,
        full_native_scene_runs_40004_frames_referenced_separately=True,all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model=True,
        no_gameplay_state_save_conditions_roles_roster_funds_RNG_results_orcontroller_retiming=True,read_only_callbacks_host_slots_andcore_restored=True,
        not_natural_optional_activation_original_location_customnames_fullroute_hardware_oreveryframe_causality=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Actual FE:two originalpaint snapshots/four complete held nativebitmaps/palettes/RGB;228x48/288stride/6x12/16pitch andcurrent vtables exact;9862focusedframes/no repeatedwholeflow tests.')
