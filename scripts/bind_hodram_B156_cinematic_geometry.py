"""Bind every selected source body to actual typed geometry and readable QA holds."""
import math
import struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.trace_file_ids_v683 import mapped_read

ROOT=Path('work/analysis/Hodram_B156_cinematic_geometry_20261102')
RUN=Path('work/analysis/Hodram_B156_cinematic_geometry_run_20261102')
FIXTURE=Path('work/analysis/Hodram_B156_cinematic_source_probe_20261102/fixture.json')


if __name__=='__main__':
    assert not ROOT.exists()
    fixture=load(FIXTURE);terminal=load(RUN/'terminal.json')
    reportpath=Path(terminal['report']);observerpath=Path(terminal['observer'])
    assert sha(reportpath.read_bytes())==terminal['report_sha256'] and sha(observerpath.read_bytes())==terminal['observer_sha256']
    report,observer=load(reportpath),load(observerpath)
    assert terminal['terminal'] and report['cold_boot'] and report['frames']==15001 and not report['savestate_loaded'] and not report['callback_errors']
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    packet=load(fixture['source_packet']);source={r['id']:r for g in packet['groups'] if g['block']==156 for r in g['records']}
    expected=[source[r['id']] for r in fixture['selected_source_commands'] if r['id'] is not None]
    paints=[r for r in observer['rows'] if r['kind']=='modal_paint']
    arm=NdsImage.open(fixture['research_ROM']).read_file('/__arm9__.bin')
    captures=report['frames_captured'];rows=[];start=0
    for record in expected:
        body=record['source_Japanese'].replace('FI','Hodram').encode('cp932').hex()
        index=next(i for i in range(start,len(paints)) if paints[i]['text_hex']==body)
        row=paints[index];start=index+1
        assert 'complete_readonly_snapshots' in row and row['CPU_all4MiB_DTCM_ITCM_and_configuration_unchanged_by_callback']
        data={}
        for kind,ref in row['complete_readonly_snapshots'].items():
            value=Path(ref['path']).read_bytes();assert len(value)==ref['bytes'] and sha(value)==ref['sha256'];data[kind]=value
        memory=lambda address,size:mapped_read(data['WRAM'],data['DTCM'],row['DTCM_base'],address,size)
        context=list(struct.unpack('<19I',memory(row['context'],76)));view=list(struct.unpack('<25I',memory(row['bitmap'],100)))
        font=list(struct.unpack('<6I',memory(row['font_metrics_object'],24)));header=list(struct.unpack('<5I',memory(view[4],20)))
        assert context[1:6]==[0,0,228,48,1] and context[11]==row['bitmap']
        assert view[10:16]==[228,48,0,0,228,48] and view[18:20]==[0,0] and font[1:3]==[6,12] and header[:3]==[4,72,48]
        vtables=[context[0],view[0],view[20],font[0],font[5]]
        assert all(memory(p,32)==arm[p-0x02000000:p-0x02000000+32] for p in vtables)
        palette_address=(view[4]+header[3])&0xffffffff;palette=memory(palette_address,32)
        next_frame=paints[index+1]['frame'] if index+1<len(paints) else report['frames']
        # FE paints are synchronous; retain a settled hold. Progressive bodies
        # can advance before the next 120-frame capture and are matched by RAM,
        # not approved as complete visual text from these incidental captures.
        minimum_hold=60 if record['source_selector']==254 else 20
        candidates=[c for c in captures if row['frame']+minimum_hold<=c['frame']<next_frame]
        assert candidates,(record['id'],row['frame'],next_frame)
        capture=candidates[0];assert sha(Path(capture['path']).read_bytes())==capture['PNG_sha256']
        rows.append(dict(id=record['id'],source_selector=record['source_selector'],source_reference=record['source_reference'],
            actual_paint_frame=row['frame'],actual_expanded_body_hex=body,original_source_preamble_hex=record['source_complete_preamble_hex'],
            capture=capture,capture_minimum_hold_frames=minimum_hold,progressive_capture_not_complete_text_approval=record['source_selector']!=254,
            context=context,view=view,font=font,header=header,palette_address=palette_address,palette_hex=palette.hex(),
            snapshots=row['complete_readonly_snapshots'],actual_geometry_228x48_stride288_font6x12=True,
            actual_current_typed_vtables_exact=True,source_body_andmacro_expansion_match=True,visual_approval_pending=True))
    assert len(rows)==31 and sum(r['source_selector']==254 for r in rows)==23
    ROOT.mkdir(parents=True);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',12);sheets=[]
    fe=[r for r in rows if r['source_selector']==254]
    for offset in range(0,len(fe),12):
        selected=fe[offset:offset+12];sheet=Image.new('RGB',(3*256,math.ceil(len(selected)/3)*216),'#eeeeee');draw=ImageDraw.Draw(sheet)
        for j,row in enumerate(selected):
            x=(j%3)*256;y=(j//3)*216
            picture=Image.open(row['capture']['path']).convert('RGB');assert picture.size==(256,384)
            sheet.paste(picture.crop((0,192,256,384)),(x,y+24));draw.text((x+3,y+2),row['id'].replace('DK4_MES_','')+' @'+str(row['capture']['frame']),fill='black',font=font)
        path=ROOT/f'cinematic_source_holds_{offset//12+1:02d}.png';sheet.resize((sheet.width*2,sheet.height*2),Image.Resampling.NEAREST).save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),record_ids=[r['id'] for r in selected]))
    save(ROOT/'observed_cinematic_geometry.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),terminal=str(RUN/'terminal.json'),
        report=str(reportpath),report_sha256=sha(reportpath.read_bytes()),observer=str(observerpath),observer_sha256=sha(observerpath.read_bytes()),
        selected_source_records=31,cinematic_FE_records=23,matched_source_records=rows,review_sheets=sheets,
        all23_source_FE_typed_geometry_228x48_288stride_6x12_current_vtables_exact=True,
        visual_review_pending=True,new_English_native_planes_andgeometry_bound_formatting_pending=True,
        no_natural_endgame_orplot_completion_claim=True,source_conditional_wrapper_not_executed=True,
        later_unrelated_opening_panels_not_editorial_coverage=True,new_credit=0,new_registered_ROM=False,
        evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,RUN/'terminal.json',reportpath,observerpath,Path(__file__)]}))
    print('31 exact source bodies/23 cinematic FE displays bound:228x48,288stride,6x12 andcurrent vtables. Two readable sheets need direct review;English formatting still pending.')
