"""Recompute original live FE typed objects/palette and held VRAM pixels; no producer/capture replay."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.trace_file_ids_v683 import mapped_read
from scripts.actual_Hodram_FE_VRAM_v8338b import read_bitmap
BASE=0x02000000

def color(word):
    r=word&31;g=(word>>5)&31;b=(word>>10)&31;g6=(g<<1)|(g>>4)
    return r*255//31,g6*255//63,b*255//31

def check_FE_geometry(data,parent,native,load,require):
    declared=data['FE_geometry'];require(len(declared['groups'])==2 and declared['focused_actual_frames']==8002,'two focused FE language groups/8002 frames')
    arm=parent.read_file('/__arm9__.bin');groups=[]
    for version in ['clean_Japanese','revised_English']:
        root=Path('work/analysis/Hodram_outcome_FE_geometry_runs_v8336')/version;terminal,plan=map(load,[root/'terminal.json',root/'run_plan.json']);rp,op=Path(terminal['report']),Path(terminal['observer']);report,observer=map(load,[rp,op])
        require(terminal['terminal'] and terminal['frames']==report['frames']==plan['frames']==4001 and terminal['all_callbacks_readonly_andhost_slots_restored'] and terminal['exactly_one_complete_original_FE_paint_CPU_WRAM_DTCM_ITCM_snapshot'],'terminal readonly original FE paint capture')
        require(sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==terminal['observer_sha256'] and sha((root/'run_plan.json').read_bytes())==terminal['run_plan_sha256'],'exact focused FE report/observer/plan files')
        fixture=next(f for f in data['fixtures']['fixtures'] if f['source_block']==48 and f['version']==version)
        require(plan['research_ROM']==fixture['research_ROM'] and plan['research_ROM_sha256']==report['ROM_sha256']==fixture['research_ROM_sha256'],'focused FE exact whole-scene fixture association')
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not any(v for k,v in report.items() if k.startswith('synthetic_')),'focused ordinary coldboot/no forced state')
        require(not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact'],'focused FE callback/core guards')
        candidates=[r for r in observer['rows'] if 'complete_readonly_snapshots' in r];require(len(candidates)==1,'one complete original modal paint snapshot');row=candidates[0]
        body=native['bodies'][version]['DK4_MES_B48_R0006']['expanded_body'];require(row['kind']=='modal_paint' and row['text_hex']==body.hex()==plan['exact_expanded_FE_body_hex'] and row['CPU_all4MiB_DTCM_ITCM_and_configuration_unchanged_by_callback'],'exact original FE body andreadonly paint boundary')
        snapshots={}
        for name,ref in row['complete_readonly_snapshots'].items():
            raw=Path(ref['path']).read_bytes();require(len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'whole FE boundary snapshot:'+name);snapshots[name]=raw
        require(len(snapshots['WRAM'])==0x400000 and len(snapshots['DTCM'])==0x4000 and len(snapshots['ITCM'])==0x8000 and len(snapshots['CPU'])==128,'complete typed FE CPU/RAM/TCM extents')
        memory=lambda address,length:mapped_read(snapshots['WRAM'],snapshots['DTCM'],row['DTCM_base'],address,length)
        registers=struct.unpack('<32I',snapshots['CPU']);require(row['PC']==registers[2]==0x02054924 and row['context']==registers[4] and row['R1']==registers[5] and memory(row['R1'],len(body)+1)==body+b'\0','original modal paint PC/arguments/full input andNUL')
        context=list(struct.unpack('<19I',memory(row['context'],76)));view=list(struct.unpack('<25I',memory(row['bitmap'],100)));font=list(struct.unpack('<6I',memory(row['font_metrics_object'],24)))
        require(memory(row['context'],76).hex()==row['context_76_hex'] and memory(row['bitmap'],100).hex()==row['bitmap_100_hex'] and memory(row['font_metrics_object'],24).hex()==row['font_object_24_hex'],'captured descriptors match original raw snapshots')
        require(context[1:6]==[0,0,228,48,1] and context[11]==row['bitmap'] and view[10:16]==[228,48,0,0,228,48] and view[18:20]==[0,0] and font[1:3]==[6,12],'actual original FE geometry/clip/metrics')
        header=list(struct.unpack('<5I',memory(view[4],20)));require(header[:3]==[4,72,48],'original fourbit bitmap descriptor/288stride')
        palette_address=(view[4]+header[3])&0xFFFFFFFF;palette=memory(palette_address,32);colors=[color(v) for v in struct.unpack('<16H',palette)];require(colors[15]==(0,8,0) and colors[14]==(197,198,197),'actual FE ink/CP932-shadow palette')
        vtables=[]
        for address in [context[0],view[0],view[20],font[0],font[5]]:
            require(BASE<=address<BASE+len(arm)-32 and memory(address,32)==arm[address-BASE:address-BASE+32],'actual typed FE vtable matches exact current runtime');vtables.append(dict(address=address,bytes=32,sha256=sha(memory(address,32))))
        fullroot=Path('work/analysis/Hodram_outcome_FE_scene_runs_v8333b')/f'route1_B48_{version}';fullterminal=load(fullroot/'terminal.json');fullreport=load(fullterminal['report'])
        require(report['scripted_input_schedule']==[e for e in fullreport['scripted_input_schedule'] if e['start']<=4000],'exact unretimed focused/fullrun input prefix')
        photos={p['frame']:p for p in report['frames_captured']};fullphotos={p['frame']:p for p in fullreport['frames_captured']};expected=native['bodies'][version]['DK4_MES_B48_R0006']['pages'][0];holds=[]
        for snap in report['read_only_capture_RAM_snapshots']:
            raw=Path(snap['path']).read_bytes();frame=snap['frame'];require(snap['read_only_export'] and len(raw)==0x400000 and sha(raw)==snap['sha256'] and frame in [3490,3910],'complete focused FE hold RAM')
            def readram(address,length):
                at=address-BASE;require(0<=at and at+length<=len(raw),'held persistent FE descriptor bounds');return raw[at:at+length]
            reused=readram(row['context'],76).hex()!=row['context_76_hex']
            require(readram(row['bitmap'],100).hex()==row['bitmap_100_hex'] and readram(view[4],20)==struct.pack('<5I',*header) and readram(palette_address,32)==palette,'held persistent view/descriptor/palette,not temporary paint stack')
            try:packed,binding=read_bitmap(fullreport,frame,header,view[4])
            except AssertionError as error:raise ValueError('Hodram original FE bankD/source/VRAM guard') from error
            pixels=bytes(v for b in packed for v in [b&15,b>>4]);logical=bytes(pixels[y*288+x] for y in range(48) for x in range(228));require(logical==expected['native_plane_bytes'],'independent actual held original VRAM bitmap equals native glyph plane')
            photo=photos[frame];require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'] and Path(photo['path']).read_bytes()==Path(fullphotos[frame]['path']).read_bytes(),'focused/fulltrace complete held PNG equality')
            picture=Image.open(photo['path']).convert('RGB');matches=0
            for i,index in enumerate(expected['physical_plane_bytes']):
                if index:require(picture.getpixel((16+i%228,296+i//228))==colors[index],'every actual FE native ink pixel/palette/RGB');matches+=1
            holds.append(dict(frame=frame,RAM_snapshot=snap,capture=photo,whole_PNG_equal_to_completed_original_command_trace_run=True,complete_actual_bitmap_228x48_equals_independent_native_plane=True,all_native_ink_indices_match_actual_palette_andRGB=True,matched_ink_pixels=matches,original_paint_context_stack_storage_reused_after_paint=reused,persistent_view_bitmap_header_andpalette_exact=True,actual_bitmap_VRAM_binding=binding))
        require(len(holds)==2,'two complete held bitmaps perFE language')
        groups.append(dict(version=version,actual_FE_paint_frame=row['frame'],captured_original_context=row['context_76_hex'],captured_original_bitmap_view=row['bitmap_100_hex'],captured_original_header=header,captured_original_font_metrics=row['font_object_24_hex'],original_typed_geometry_228x48_stride288_logical6x12_physical16pitch=True,palette_address=palette_address,palette_hex=palette.hex(),palette15_RGB=list(colors[15]),palette14_RGB=list(colors[14]),exact_current_source_vtables=vtables,complete_paint_snapshot=row['complete_readonly_snapshots'],complete_actual_holds=holds,original_native_source_consumer_not_geometry_inferred_from_incidental_r1=True))
    require(declared['groups']==groups,'every independently recomputed original FE descriptor/palette/VRAM/hold/scope field')
    for key in ['whole_scene_tests_not_repeated','full_native_scene_runs_40004_frames_referenced_separately','all_actual_FE_typed_descriptors_palette_complete_bitmap_andphysical_RGB_match_independent_model','no_gameplay_state_save_conditions_roles_roster_funds_RNG_results_orcontroller_retiming','read_only_callbacks_host_slots_andcore_restored','not_natural_optional_activation_original_location_customnames_fullroute_hardware_oreveryframe_causality']:
        require(declared[key] is True,'honest original FE scope:'+key)
    return dict(original_FE_paint_snapshots_recomputed=2,complete_actual_VRAM_bitmap_palette_RGB_holds_recomputed=4,focused_actual_frames_bound=8002,temporary_context_persistent_view_andlive_VRAM_not_synthetic_RAM_distinction_preserved=True,new_emulator_runs=0)
