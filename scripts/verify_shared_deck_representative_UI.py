"""Bind seven ordinary live Refit bodies to the same current native consumer and complete pixels."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_Deck_actual_UI_20261104')
CAP=Path('work/emulation_v193/Shared_Deck_actual_UI_20261104')
SELECTED={13000:1286,13300:1281,13600:1248,13900:1278,14500:1247,14800:1277,15100:1282}
REFIT=Path('translations/refit_contextual_editorial_manuscript_v1.json')

if __name__=='__main__':
    output=ROOT/'representative_UI_verification.json';assert not output.exists()
    plan=load(ROOT/'run_plan.json');report_path=CAP/'capture_report.json';report=load(report_path)
    assert report['frames']==21400 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==plan['research_ROM_sha256']==sha(Path(plan['research_ROM']).read_bytes())
    assert report['battery_save_preloaded']['source_sha256']==plan['original_battery_sha256']==sha(Path(plan['original_battery']).read_bytes())
    assert not any(k.startswith('synthetic_') for k in report)
    arm=NdsImage.open(plan['research_ROM']).read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    records={r['message_id']:r for r in load(REFIT)['records'] if r.get('consumer')=='refit-help27-pair-safe-v1'}
    assert len(records)==31
    captures={r['frame']:r for r in report['frames_captured']}
    snapshots={r['frame']:r for r in report['read_only_pause_RAM_snapshots']}
    results=[]
    for frame,ident in SELECTED.items():
        cap,snapshot=captures[frame],snapshots[frame];path=Path(cap['path']);raw=Path(snapshot['path']).read_bytes()
        assert sha(path.read_bytes())==cap['PNG_sha256'] and sha(raw)==snapshot['sha256'] and snapshot['read_only_export']
        found=[];at=raw.find(struct.pack('<3I',4,42,108))
        while at>=0:
            parent=at-0x1c38
            if parent>=0 and struct.unpack_from('<2I',raw,parent+0x38)==(168,108):
                vtable=struct.unpack_from('<I',raw,parent)[0]
                if 0x02000000<=vtable<0x02400000:
                    typeinfo=struct.unpack_from('<I',raw,vtable-0x02000000-4)[0]
                    name=struct.unpack_from('<I',raw,typeinfo-0x02000000+4)[0]-0x02000000
                    if raw[name:raw.index(0,name)]==b'21CRemodelCabinInfoView':found.append((parent,at))
            at=raw.find(struct.pack('<3I',4,42,108),at+1)
        assert len(found)==1
        parent,header=found[0];relative=struct.unpack_from('<I',raw,header+16)[0]
        pointer=(0x02000000+header+relative)&0xffffffff;packed=raw[pointer-0x02000000:pointer-0x02000000+9072];assert len(packed)==9072
        indices=bytes(v for n in packed for v in (n&15,n>>4))
        text=records[ident]['english'];_,lines=compile_paragraph(text);expected=bytearray(168*60)
        for j,line in enumerate(lines):
            for k,char in enumerate(line):
                glyph=font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x,y)):expected[(j*12+y+1)*168+k*6+x]=1
        assert indices[:168*60]==expected
        image=Image.open(path).convert('RGB');crop=image.crop((64,80,232,140))
        assert bytes(pixel==(230,230,230) for pixel in crop.getdata())==bytes(bool(v) for v in expected)
        results.append(dict(frame=frame,message_id=ident,logical_English=text,lines=lines,capture=cap,snapshot=snapshot,
            source_bounded_actual_RTTI='21CRemodelCabinInfoView',parent_address=0x02000000+parent,resource_header=0x02000000+header,
            native_pixel_pointer=pointer,actual_resource_format_pitch_height=[4,42,108],
            all168x60_body_indices_andactual_RGB_ink_blank_mask_exact=True,complete_first_internal_final_glyphs_andblank_guards_exact=True,
            independent_body_plane_sha256=sha(expected)))
    sheets=[];font_caption=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for first in range(0,len(results),6):
        group=results[first:first+6];sheet=Image.new('RGB',(1536,1600),'#eee');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(group):
            x,y=i%3*512,i//3*800;draw.text((x+4,y+4),'Refit COMMON '+str(row['message_id'])+' @'+str(row['frame']),font=font_caption,fill='black')
            sheet.paste(Image.open(row['capture']['path']).convert('RGB').resize((512,768),Image.Resampling.NEAREST),(x,y+28))
        path=ROOT/f'ordinary_Refit_QA_{len(sheets)+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),captures=len(group)))
    save(output,dict(run_plan=str(ROOT/'run_plan.json'),run_plan_sha256=sha((ROOT/'run_plan.json').read_bytes()),capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),
        actual_frames=21400,ordinary_live_Refit_bodies=results,complete_body_texture_andRGB_comparisons=7,review_sheets=sheets,direct_visual_review_pending=True,
        same_current168x108_native_Refit_constructor_palette_pitch_andglyph_consumer_observed=True,
        four_revised_special_static_paragraphs_not_activated_or_claimed_observed=True,
        new_four_paragraphs_have_native_offline_stored_andconnected_checks_only=True,
        ordinary_cancel_ship_selection_return_to_port_andDeck_Navigator_class_UI_observed=True,
        incidental_Manuel_Almeida_Helm_comment_andSailor_Info_seen_not_new_editorial_credit=True,
        one_invalid_touch_rejected_before_input_orstate_change=True,original_donor_save_unchanged=True,
        inherited_five_ship_test_save_not_earned_progress=True,no_new_RAM_orcondition_override=True,natural_activation=False,full_route=False,hardware=False,
        actual_gameplay=True,not_registered_release=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [ROOT/'run_plan.json',report_path,REFIT,Path(__file__)]}))
    print('Seven ordinary live bodies:source-bounded actual168x108 resources,all168x60 texture andRGB masks exact;four special paragraphs remain offline-only.')
