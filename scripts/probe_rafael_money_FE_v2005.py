"""Unchanged B44 money notice in the established original228x48 mode1 consumer.

Borrowed actual FE context establishes renderer behavior only; B44's actual money
panel is reconciled separately from this reusable offline native proof.
"""
from pathlib import Path
import struct
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.verify_lil_FE_display_v1737 import snapshots,OBS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_money_FE_v2005')
PLAN=Path('work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json')
DOC=Path('translations/rafael_opening_contextual_editorial_manuscript_v2.json')
INPUT=0x02660000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc=map(read,(PLAN,DOC));im=NdsImage.open(plan['research_ROM']);arm=im.read_file('/__arm9__.bin')
    assert sha(arm)=='500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    row=next(r for r in doc['records']if r['source_presentation_prefix_hex']=='fe')
    record=next(r for r in plan['text_records']if r['id']==row['id'])
    assert record['unchanged_FE_separate_display_pending']
    body=bytes.fromhex(row['current_text_hex'])[1:]
    assert body.rstrip()==b'Received 30,000 gold!'
    observed=read(OBS);captured=next(r for r in observed['rows']if r.get('complete_readonly_snapshots'))
    data=snapshots(captured);ctx=captured['context'];bitmap=struct.unpack('<25I',bytes.fromhex(captured['bitmap_100_hex']))
    assert bitmap[10:12]==(228,48)and bitmap[12:16]==(0,0,228,48)
    descriptor=bitmap[4];header=struct.unpack_from('<5I',data['WRAM'],descriptor-0x02000000)
    assert header[0]&255==4 and header[1:3]==(72,48)
    pixels_address=(descriptor+header[4])&0xffffffff;width=288
    cpu=machine(arm);cpu.mem_write(0x02000000,data['WRAM']);cpu.mem_write(0x01FF8000,data['ITCM'])
    cpu.mem_write(captured['DTCM_base'],data['DTCM']);cpu.mem_map(0x06000000,0x800000)
    cpu.mem_write(INPUT-16,b'\xa5'*(len(body)+33));cpu.mem_write(INPUT,body+b'\0');events=[]
    def glyph(u,address,size,_):
        code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
        events.append(dict(code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
    hook=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4)
    try:call(cpu,0x01FFCE40-0x02000000,(ctx,INPUT),instruction_limit=1000000)
    finally:cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_R0)==INPUT+len(body)
    assert bytes(cpu.mem_read(INPUT,len(body)+1))==body+b'\0'
    assert bytes(cpu.mem_read(INPUT-16,16))==bytes(cpu.mem_read(INPUT+len(body)+1,16))==b'\xa5'*16
    visible=[e for e in events if e['code']!=32]
    assert [e['code']for e in visible]==[c for c in body if c not in(32,10)]
    assert len(visible)==len({(e['x'],e['y'])for e in visible})
    assert all(0<=e['x']<=222 and e['y']%12==0 and 0<=e['y']<=36 for e in visible)
    font=GameAsciiFont.from_arm9(arm);expected=bytearray(width*48);physical=bytearray(228*64)
    for e in visible:
        g=font.decode(chr(e['code']))
        for y in range(11):
            for x in range(6):
                if g.getpixel((x,y)):
                    expected[(e['y']+y)*width+e['x']+x]=e['style']
                    physical[(e['y']//12*16+y)*228+e['x']+x]=1
    native=bytes(n for b in cpu.mem_read(pixels_address,72*2*48)for n in(b&15,b>>4))
    assert native==bytes(expected)
    ROOT.mkdir(parents=True);logical=bytes(native[y*width+x]for y in range(48)for x in range(228))
    (ROOT/'complete_native_228x48.bin').write_bytes(logical);(ROOT/'physical_228x64_mask.bin').write_bytes(physical)
    preview=Image.new('RGB',(228,64));preview.putdata([(0,8,0)if p else(239,232,201)for p in physical]);path=ROOT/'money_notice_FE.png';preview.save(path)
    save(ROOT/'unchanged_money_notice_native_modal_proof.json',dict(id=row['id'],plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),ARM9_sha256=sha(arm),body_hex=body.hex(),
        separate_original_FE_mode1_consumer=True,not_progressive_actor_fallback=True,logical_geometry=[228,48],physical_geometry=[228,64],
        one_page_full_target_and_terminal_pointer_exact=True,complete_native_independent_plane_and_all_glyphs_bounds=True,
        native_plane_sha256=sha(logical),physical_mask_sha256=sha(physical),glyphs=events,
        borrowed_actual_FE_context=str(OBS),borrowed_actual_context_sha256=sha(Path(OBS).read_bytes()),
        no_new_B44_actual_panel_claim=True,B44_actual_reconciliation_pending=True,
        preview=str(path),preview_sha256=sha(path.read_bytes()),visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(id=row['id'],unchanged=True,complete_native_modal_plane=True,actual_B44_pending=True))
