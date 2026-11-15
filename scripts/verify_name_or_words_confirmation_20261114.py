"""Verify current COMMON 296 at all three original input owners."""

from pathlib import Path
from struct import pack,unpack_from

from capstone import CS_ARCH_ARM,CS_MODE_ARM,Cs
from PIL import Image,ImageChops,ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,
    UC_ARM_REG_R5,UC_ARM_REG_R8,UC_ARM_REG_R10,UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont,SJIS_GLYPH_COUNT,SJIS_MAP_OFFSET,decode_glyph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_ship_name_confirmation_20261114 as before
from scripts import stage_name_or_words_literal_20261114 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.probe_button_prompt_native import BASE,STACK,STOP
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shared_crew_selector_v1 import dispatch,ARGS
from scripts.native_machine_scoped_v764 import machine

base,ROOT=stage.base,stage.ROOT
OUT=ROOT/"reviewed_display_v2.json"
INVENTORY=Path("work/analysis/native_common_extended_calls_clean.json")
PANEL=(16,296,244,344)
WRAPPER=0x0205466C
CALLERS=(
    ("Name a purchased ship",0x635E0,0x6361C,UC_ARM_REG_R8),
    ("Enter Promised Words",0xAE990,0xAEA00,UC_ARM_REG_R10),
    ("Rename an existing ship",0xAEA90,0xAEB44,UC_ARM_REG_R8),
)
LIVE={
    "buy":("Latina",(9550,),9405),
    "rename":("Vestaros",(13850,14650),13703),
}
INPUTS=(b"Latina",b"Vestaros",b"FIONA",b"FALCON",b"FORTUNE",b"FURY",b"ICARUS",b"INCREDIBLE",b"Blue Oak",
        b"ABCDEFGHIJKLMNOPQR","アカサタナハマヤラ".encode("cp932"),b"HMS "+ "船影".encode("cp932"),
        b"100% Gale")


def actual(stored,font):
    observations={}
    evidence={}
    for case,(name,targets,first_call_frame) in LIVE.items():
        old,new=([root/case/"capture/capture_report.json" for root in (before.ROOT,ROOT)])
        read=[base.load(path) for path in (old,new)]
        assert [data["ROM_sha256"] for data in read]==[stored["previous_sha256"],stored["candidate_sha256"]]
        expect,frames,last,_,donor=before.schedule(case)
        assert all(data["cold_boot"] and not data["savestate_loaded"] and not data["callback_errors"] for data in read)
        assert all(data["scripted_input_schedule"]==expect and data["frames"]==last for data in read)
        assert all(not any(v for k,v in data.items() if k.startswith("synthetic_")) for data in read)
        assert all(read[0][key]==read[1][key] for key in ("core_options","core_DLL_sha256"))
        assert all(data["battery_save_preloaded"]["source_sha256"]==donor["source_sha256"] for data in read)
        assert base.digest(donor["source"])==donor["source_sha256"]
        paths=[root/case/"requests.json" for root in (before.ROOT,ROOT)]
        original,revised=map(base.load,paths)
        assert all(not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
                   for trace in (original,revised))
        assert [r for r in revised["source_requests"] if r["PC"]!=WRAPPER]==original["source_requests"]
        selected=[row for row in revised["source_requests"] if row["PC"]==WRAPPER and row["message_ID"]==296]
        assert len(selected)==len(targets) and selected[0]["frame"]==first_call_frame
        chosen_caller=0x6361C if case=="buy" else 0xAEB44
        assert {row["caller_LR"] for row in selected}=={BASE+chosen_caller+4}
        masks=[]
        exact=[]
        for frame in frames:
            rows=[next(r for r in data["frames_captured"] if r["frame"]==frame) for data in read]
            for row in rows:
                assert row["PNG_sha256"]==base.digest(row["path"])
                evidence[row["path"]]=row["PNG_sha256"]
            if frame in targets:
                left,right=(Image.open(row["path"]).convert("RGB") for row in rows)
                diff=ImageChops.difference(left,right).getbbox()
                x,y,w,h=diff
                assert PANEL[0]<=x<w<=PANEL[2] and PANEL[1]<=y<h<=PANEL[3]
                mask=font_mask(right,font,stage.DRAFT%name,16,297,PANEL,(0,8,0))
                masks.append(dict(frame=frame,display=stage.DRAFT%name,complete_ink=mask,changed_bounds=diff,path=rows[1]["path"]))
            else:
                assert rows[0]["framebuffer_sha256"]==rows[1]["framebuffer_sha256"]
                exact.append(frame)
        evidence.update({str(p):base.digest(p) for p in (old,new,*paths)})
        branch=next(r for r in read[1]["read_only_capture_RAM_snapshots"] if r["frame"]==targets[0])
        assert branch["read_only_export"] and base.digest(branch["path"])==branch["sha256"]
        observations[case]=dict(confirmations=masks,byte_exact_other_holds=exact,
            native_original_caller_observed=selected,snapshot=branch,ordinary_inputs=True)
    return observations,evidence


def native_origins(arm,clean,snapshot):
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    relocated = {
        0x636E0:(0x021447D0,0x01FFC7B4),
        0xAEA3C:(0x02156074,0x023885B4),
        0xAEA40:(0x02156058,0x02388598),
        0xAEB90:(0x02156080,0x01FFC7B4),
    }
    restored=bytearray(arm)
    for offset,(old,new) in relocated.items():
        assert unpack_from("<I",clean,offset)[0]==old and unpack_from("<I",arm,offset)[0]==new
        restored[offset:offset+4]=clean[offset:offset+4]
    for lo,hi in ((0x6354C,0x636F4),(0xAE960,0xAEA44),(0xAEA44,0xAEB98),(0x5466C,0x546B8)):
        assert restored[lo:hi]==clean[lo:hi]
    calls=[]
    old=base.load(INVENTORY)
    assert not any(row["native_id_constant"]==296 for row in old["candidates"])
    # The three keyboard loops store the constant in preserved r5.
    for label,entry,branch,_ in CALLERS:
        rows=list(decoder.disasm(arm[entry:branch+4],BASE+entry))
        assert rows[0].mnemonic=="mov" and rows[0].op_str=="r5, #0x128"
        assert rows[-3].op_str=="r0, r5" and rows[-1].op_str=="#0x205466c"
        assert not any(r.mnemonic.startswith(("ldr","mov","add","sub")) and r.op_str.startswith("r5,") for r in rows[1:])
        calls.append(dict(context=label,original_message_assignment=BASE+entry,original_call=BASE+branch,
            span_sha256=stage.parent.parent.parent.source.current.assets.edit.digest(arm[entry:branch+4]),
            old_local_resolver_missed_preserved_r5=True))
    descriptor=unpack_from("<I",clean,0xAEA3C)[0]
    assert clean[descriptor-BASE:].split(b"\0",1)[0].decode("cp932")=="約束の言葉"
    shown=unpack_from("<I",arm,0xAEA3C)[0]
    cpu,_=get_machine(arm,Path(snapshot["path"]).read_bytes())
    assert bytes(cpu.mem_read(shown,15))==b"Promised Words\0"
    assert bytes(cpu.mem_read(0x01FFC7B4,10))==b"Ship Name\0"
    return calls


def port_text(cpu,arm,branch,arg_reg,value,template=stage.DRAFT.encode("ascii"),preserve=True):
    scratch=0x02668000
    cpu.mem_write(scratch-16,b"\xa5"*16+value+b"\0"+b"\xa5"*16)
    for reg,num in ((UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP),(UC_ARM_REG_R5,296),(arg_reg,scratch)):
        cpu.reg_write(reg,num)
    reached=[]
    def modal(u,pc,size,unused):
        assert u.reg_read(UC_ARM_REG_R0)==1
        ptr=u.reg_read(UC_ARM_REG_R1)
        assert bytes(u.mem_read(ptr,len(template)+1))==template+b"\0"
        va=u.reg_read(UC_ARM_REG_R2)
        assert bytes(u.mem_read(va,4))==pack("<I",scratch)
        reached.append(True)
    hook=cpu.hook_add(UC_HOOK_CODE,modal,begin=0x02054774,end=0x02054774)
    try:
        cpu.emu_start(BASE+branch-8,0x0205479C,count=3000000)
    finally:
        cpu.hook_del(hook)
    assert reached==[True] and cpu.reg_read(UC_ARM_REG_PC)==0x0205479C
    assert bytes(cpu.mem_read(scratch-16,len(value)+33))==b"\xa5"*16+value+b"\0"+b"\xa5"*16
    fmt,display=unpack_from("<2I",arm,0x54890)
    expanded=bytes(cpu.mem_read(fmt,256)).split(b"\0",1)[0]
    rendered=bytes(cpu.mem_read(display,256)).split(b"\0",1)[0]
    assert expanded==template%value
    if preserve:
        assert b" ".join(rendered.split())==expanded and b"\n" not in rendered,(value,expanded,rendered)
    return rendered


def independent(rom,arm,font,display):
    # The compact one-line prompt starts at the left interior margin; buffers
    # may contain a zero-width logical phase space before the text.
    kanji=rom.read_file("/GRP/KANJI.FNT")
    mapping=unpack_from(f"<{SJIS_GLYPH_COUNT}H",arm,SJIS_MAP_OFFSET)
    text=display.decode("cp932").strip()
    expected=bytearray(228*48)
    x=0
    for char in text:
        raw=char.encode("cp932")
        width=len(raw)*6
        glyph=font.decode(char) if width==6 else decode_glyph(kanji,mapping.index(int.from_bytes(raw,"big")))
        if width==12:
            for y in range(11):
                for dx in range(glyph.width):
                    if glyph.getpixel((dx,y)):
                        expected[(y+1)*228+x+dx+1]=15
        for y in range(11):
            for dx in range(glyph.width):
                if glyph.getpixel((dx,y)):
                    expected[(y+(width==6))*228+x+dx]=1
        x+=width
    assert x<=216
    return bytes(expected)


def offline(rom,arm,font,observations):
    cases=[]
    raster,_,_=font_tools(rom)
    snapshot=observations["buy"]["snapshot"]
    raw=Path(snapshot["path"]).read_bytes()
    split=7
    sheets=[Image.new("RGB",(3*468,118*n),"#242932") for n in (split,len(INPUTS)-split)]
    labels=[ImageDraw.Draw(sheet) for sheet in sheets]
    for i,(context,_,branch,reg) in enumerate(CALLERS):
        cpu,_=get_machine(arm,raw)
        for j,value in enumerate(INPUTS):
            assert len(value)<=18
            display=port_text(cpu,arm,branch,reg,value)
            expected=independent(rom,arm,font,display)
            events=[]
            plane=raster(arm,display,0x01FFCE40-BASE,size=(228,48),instruction_limit=2000000,glyph_events=events)
            assert plane==expected,(context,value,display)
            visible=[e for e in events if e["code"]!=32]
            assert [e["code"] for e in visible]==glyph_codes(display)
            assert visible[0]["code"]==ord("I") and visible[-1]["code"]==ord("?")
            assert all(0<=e["x"] and e["x"]+(12 if e["code"]>255 else 6)<=216 and e["y"]==0 for e in visible)
            panel=Image.frombytes("L",(228,48),bytes({0:255,1:0,15:192}[px] for px in plane))
            which=0 if j<split else 1
            x,y=(468*i,118*(j if which==0 else j-split))
            sheets[which].paste(panel.convert("RGB").resize((456,96),Image.Resampling.NEAREST),(x+4,y+20))
            labels[which].text((x+4,y+3),f'{context} | input {j+1}',fill="white")
            cases.append(dict(context=context,value_hex=value.hex(),display_hex=display.hex(),
                expanded_visible_text=display.decode("cp932").strip(),exact_complete_mask=True,
                ordinary_latin_and_wide_input_bytes_unmodified=True,actual_gameplay=False))
    reports=[]
    for i,sheet in enumerate(sheets,1):
        path=ROOT/f"native_confirmation_readable_{i}.png"
        sheet.save(path)
        reports.append(dict(path=str(path),sha256=base.digest(path)))
    return dict(cases=cases,sheets=reports)


def selector_scope(arm):
    old_arm=base.NdsImage.open(stage.parent.ROM).read_file(stage.ARM)
    original,revised=map(machine,(old_arm,arm))
    comparisons=0
    for parent in (stage.OLD_PARENT,stage.YES_NO_PARENT,0x0205466C):
        for number in (*range(3668),0x80000000,0xFFFFFFFF):
            stack={0xC4:parent,0xD0:number}
            targets=(stage.PARAGRAPH,stage.LITERAL,stage.FALLBACK)
            left,right=(dispatch(cpu,stage.START,stack,targets) for cpu in (original,revised))
            if (parent,number)==(stage.YES_NO_PARENT,296):
                assert left[0]==stage.FALLBACK and right[0]==stage.LITERAL
            else:
                expected=stage.PARAGRAPH if parent==stage.OLD_PARENT and number in stage.EXISTING_IDS else stage.FALLBACK
                assert left[0]==right[0]==expected
            assert left[1][:3]==right[1][:3]==ARGS[:3]
            comparisons+=1
    return comparisons


def historical_macro_example():
    index=before.ROOT/"buy/capture/capture_report.json"
    data=base.load(index)
    original=base.load(stage.parent.RELEASE)
    assert data["ROM_sha256"]==original["candidate_sha256"]
    snapshot=next(row for row in data["read_only_capture_RAM_snapshots"] if row["frame"]==9550)
    raw=Path(snapshot["path"]).read_bytes()
    assert base.digest(snapshot["path"])==snapshot["sha256"]
    arm=base.NdsImage.open(stage.parent.ROM).read_file(stage.ARM)
    cpu,_=get_machine(arm,raw)
    value=b"FIONA"
    output=port_text(cpu,arm,0x6361C,UC_ARM_REG_R8,value,b"\x82hs %s all right?",False)
    assert b"HodramONA" in output and value not in output
    return dict(input=value.decode("ascii"),earlier_display=output.decode("cp932").strip(),
        earlier_candidate_sha256=original["candidate_sha256"],snapshot=snapshot,captured_representative_only=True)


def main():
    assert not OUT.exists()
    proof=base.load(stage.STORED)
    assert base.digest(stage.ROM)==proof["candidate_sha256"]
    rom=base.NdsImage.open(stage.ROM)
    clean=base.NdsImage.open(stage.CLEAN)
    arm=rom.read_file(stage.ARM)
    font=GameAsciiFont.from_arm9(arm)
    observations,evidence=actual(proof,font)
    owners=native_origins(arm,clean.read_file(stage.ARM),observations["buy"]["snapshot"])
    checks=offline(rom,arm,font,observations)
    row,=proof["records"]
    row.update(review=dict.fromkeys(stage.GATES,True),original_callers=owners)
    receipt=dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=list(stage.GATES),records=[row],candidate_sha256=proof["candidate_sha256"],
        observed_gameplay=observations,native_layout=checks,evidence=evidence,hardware=False,
        earlier_macro_corruption=historical_macro_example(),selector_scope_comparisons=selector_scope(arm),
        full_goal_complete=False)
    validate_natural_dialogue_batch(receipt)
    base.save(OUT,receipt)
    print(f'Three ordinary ship-name panels and {len(checks["cases"])} complete native previews across all input owners passed.')


if __name__=="__main__":
    main()
