"""Actual FE context,independent prior paper contract,and all9 reviewed panels."""
import struct
from pathlib import Path
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_FE_display_v1737')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_modal_context_v1734_1711/modal_observer/actual_modal_contexts.json')
CAP=OBS.parent.parent
PRIOR=Path('work/analysis/equipment_release_v366/research_live_proof.json')
GEOMETRY=Path('work/analysis/equipment_confirmation_v362/actual_geometry.json')
INPUT=0x02660000


def snapshots(row):
    result={}
    for name,ref in row['complete_readonly_snapshots'].items():
        data=Path(ref['path']).read_bytes();assert sha(data)==ref['sha256'] and len(data)==ref['bytes'];result[name]=data
    return result


if __name__=='__main__':
    assert not ROOT.exists()
    prior,geometry,observed=map(read,(PRIOR,GEOMETRY,OBS))
    assert prior['physical_paper_origin_contract']==[16,296] and prior['physical_paper_row_advance_contract']==16
    assert prior['physical_composition_is_an_actual_screen_contract_not_an_independent_native_trace']
    assert geometry['declared_source_size']==[228,48] and geometry['actual_clip']==[0,0,228,48]
    assert geometry['actual_dialog_spacing_words']==[0,0] and geometry['font_metric_words'][1:]==[6,12]
    assert geometry['modal_mode']==1
    assert not observed['errors'] and observed['mismatches']==0 and observed['all_host_slots_restored_and_core_file_exact']
    report=read(CAP/'capture_report.json');assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames']==29930 and 'battery_save_preloaded' not in report
    plan=read('work/analysis/lil_modal_context_v1734/run_plan.json')
    assert report['ROM_sha256']==plan['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())
    assert report['scripted_input_schedule']==read(plan['input'])
    image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    rows=[r for r in observed['rows'] if r.get('complete_readonly_snapshots')];assert len(rows)==6
    baseline=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711')
    before=read(baseline/'capture_report.json');by_frame={r['frame']:r for r in before['frames_captured']}
    pairs=[]
    for frame in report['frames_captured']:
        p=Path(frame['path']);assert sha(p.read_bytes())==frame['PNG_sha256']
        if frame['frame'] in by_frame:
            old=Path(by_frame[frame['frame']]['path'])
            assert Image.open(p).convert('RGB').tobytes()==Image.open(old).convert('RGB').tobytes()
            pairs.append(frame['frame'])
    actual_replay=read('work/analysis/lil_actual_modal_replay_v1736/captured_context_native_glyph_metrics.json')
    current=[]
    frames={25047:25330,25347:25630,27249:27530,27549:27830,27849:28130,29050:29330}
    for row in rows:
        data=snapshots(row);raw=data['WRAM'];ctx=struct.unpack('<19I',bytes.fromhex(row['context_76_hex']))
        bitmap=struct.unpack('<25I',bytes.fromhex(row['bitmap_100_hex']))
        assert list(bitmap[10:12])==[228,48] and list(bitmap[12:16])==[0,0,228,48]
        assert list(bitmap[18:20])==[0,0] and list(ctx[1:5])==[0,0,228,48] and list(ctx[7:11])==[0,0,0,0]
        assert list(struct.unpack('<6I',bytes.fromhex(row['font_object_24_hex'])))[1:3]==[6,12]
        state=struct.unpack_from('<I',arm,0x54984)[0]
        assert struct.unpack_from('<I',raw,state-0x02000000+0x54)[0]==1
        native=next(r for r in actual_replay['cases'] if r['frame']==row['frame'])
        wanted=set();cells={}
        for e in native['glyphs']:
            assert e['y']%12==0
            glyph=font.decode(chr(e['code']))
            for y in range(11):
                for x in range(6):
                    point=(16+e['x']+x,296+e['y']//12*16+y)
                    ink=bool(glyph.getpixel((x,y)));cells[point]=ink
                    if ink:wanted.add(point)
        frame=frames[row['frame']];p=CAP/f'frame_{frame:06d}_cold_boot.png'
        if not p.exists():p=next(CAP.glob(f'frame_{frame:06d}_*.png'))
        actual=Image.open(p).convert('RGB')
        ink={(x,y) for y in range(296,360) for x in range(16,244) if actual.getpixel((x,y))==(0,8,0)}
        assert wanted==ink,(row['frame'],len(wanted-ink),len(ink-wanted))
        assert all((actual.getpixel(point)==(0,8,0))==ink for point,ink in cells.items())
        current.append({'source_frame':row['frame'],'capture_frame':frame,'complete_native_actual_ink_and_blank_cells_exact':True,
            'capture':str(p),'capture_sha256':sha(p.read_bytes()),'ink_pixels':len(ink),'source_context':row['context'],
            'logical_row_advance':12,'physical_row_advance':16,'source_geometry':[228,48]})
    # Use one exact actual FE paint state for the same generic native consumer.
    captured=rows[0];data=snapshots(captured);actual_ctx=captured['context'];bitmap=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))
    descriptor=bitmap[4];header=struct.unpack_from('<5I',data['WRAM'],descriptor-0x02000000)
    assert header[0]&255==4 and header[1]==72 and header[2]==48
    pixels_address=(descriptor+header[4])&0xFFFFFFFF;assert 0x06000000<=pixels_address<0x06800000
    width=header[1]*4;assert width==288
    text_proof=read('work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json')
    relocation=read('work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json')
    target_bytes={r['id']:bytes.fromhex(r['target_hex']) for b in relocation['blocks'] for r in b['text_records']}
    cases=[];ROOT.mkdir(parents=True)
    for case in text_proof['cases']:
        if case['consumer']!='original_FE_modal_548A8':continue
        body=target_bytes[case['id']][1:];assert b'FI' not in body
        cpu=machine(arm);cpu.mem_write(0x02000000,data['WRAM']);cpu.mem_write(0x01FF8000,data['ITCM'])
        cpu.mem_write(captured['DTCM_base'],data['DTCM']);cpu.mem_map(0x06000000,0x800000)
        cpu.mem_write(INPUT-16,b'\xA5'*(len(body)+33));cpu.mem_write(INPUT,body+b'\0');events=[]
        def glyph(u,address,size,_):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append({'code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})
        h=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4)
        try:call(cpu,0x01FFCE40-0x02000000,(actual_ctx,INPUT),instruction_limit=1000000)
        finally:cpu.hook_del(h)
        assert cpu.reg_read(UC_ARM_REG_R0)==INPUT+len(body)
        assert bytes(cpu.mem_read(INPUT,len(body)+1))==body+b'\0'
        assert bytes(cpu.mem_read(INPUT-16,16))==bytes(cpu.mem_read(INPUT+len(body)+1,16))==b'\xA5'*16
        visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[c for c in body if c not in (32,10)]
        assert len(visible)==len({(e['x'],e['y']) for e in visible})
        assert all(0<=e['x']<=222 and e['y']%12==0 and 0<=e['y']<=36 for e in visible)
        raw_pixels=bytes(n for b in cpu.mem_read(pixels_address,header[1]*2*48) for n in (b&15,b>>4))
        expected=bytearray(width*48);physical=bytearray(228*64)
        for e in visible:
            glyph=font.decode(chr(e['code']))
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x,y)):
                        expected[(e['y']+y)*width+e['x']+x]=e['style']
                        physical[(e['y']//12*16+y)*228+e['x']+x]=1
        assert raw_pixels==bytes(expected)
        native_path=ROOT/(case['id']+'_native_228x48.bin')
        logical=bytes(raw_pixels[y*width+x] for y in range(48) for x in range(228));native_path.write_bytes(logical)
        preview=Image.new('RGB',(228,64));preview.putdata([(0,8,0) if v else (239,232,201) for v in physical])
        path=ROOT/(case['id']+'_display.png');preview.save(path)
        cases.append({'id':case['id'],'target_hex':target_bytes[case['id']].hex(),'native_glyphs':events,
            'actual_captured_FE_context_and_4bit_descriptor_replayed':True,'one_native_page_consumes_complete_target':True,
            'complete_first_last_letters_full_native_independent_plane_bounds_and_input_guards':True,
            'logical_228x48_plane':str(native_path),'logical_plane_sha256':sha(logical),
            'display_preview':str(path),'display_preview_sha256':sha(path.read_bytes()),
            'physical_row_composition_inherits_prior_independent_V365_actual_screen_contract':True})
    assert len(cases)==9
    save(ROOT/'actual_paper_contract_and_all9_reviewed_FE_panels.json',{'candidate':plan['candidate'],'candidate_sha256':plan['candidate_sha256'],
        'current_actual_checks':current,'all6_current_FE_native_actual_complete_ink_and_blank_cells_match':True,
        'reviewed_cases':cases,'all9_reviewed_FE_full_actual_context_native_planes_pass':True,
        'all9_complete_targets_fit_one_native_page_inside228x48':True,
        'prior_independent_screen_contract':str(PRIOR),'prior_contract_sha256':sha(PRIOR.read_bytes()),
        'prior_actual_geometry':str(GEOMETRY),'prior_geometry_sha256':sha(GEOMETRY.read_bytes()),
        'same_mode1_context_geometry_clip_spacing_and_font_metrics_confirmed_by_readonly_capture':True,
        'physical_mapping_is_an_actual_screen_contract_not_an_independent_GPU_trace':True,
        'all_common_replay_frames_pixel_exact_to_prior_original_wind_test':pairs,
        'observer':str(OBS),'observer_sha256':sha(OBS.read_bytes()),'readonly_callbacks':observed['callbacks'],
        'actual_revised_gameplay_external_references_and_registered_release_pending':True,
        'visual_review_of_new_actual_context_previews_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All6 current FE captures match native letters and blank cells through the prior12-to16 paper contract. All9 reviewed FE targets fit one real228x48 native page with exact complete pixels.',flush=True)
