"""Verify the actual toast/refusal, original gift selectors, and current item layouts."""

from pathlib import Path
from struct import unpack

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_tavern_conversations_v764 as tavern
from scripts import stage_tavern_toast_and_gift_20261114 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.observe_current_town_replays_20261114 import ROOT as OBSERVED
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.verify_personal_gameplay_v841 import get_machine

base,ROOT = stage.base,stage.ROOT
OUT = ROOT/"reviewed_display.json"
PREVIOUS = stage.parent.stage.ROOT/"istanbul/capture_report.json"
ORIGINAL_TRACE = OBSERVED/"istanbul/requests.json"
HISTORICAL = Path("work/analysis/tavern_context_v2184b/fresh_current_native_context.json")
BODY = (16,296,244,344)
COLOR = (0,8,0)
NAMES = (b"Rafael",b"Hodram",b"Lil",b"Maria")


def live(storage,font):
    paths = dict(before=PREVIOUS, paid=ROOT/"paid/capture_report.json", refused=ROOT/"declined/capture_report.json")
    reports = {label:base.load(path) for label,path in paths.items()}
    assert reports["before"]["ROM_sha256"]==storage["previous_sha256"]
    assert all(reports[label]["ROM_sha256"]==storage["candidate_sha256"] for label in ("paid","refused"))
    evidence = {str(path):base.digest(path) for path in paths.values()}
    for label,report in reports.items():
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
        save = report["battery_save_preloaded"]
        assert save["copied_byte_exact_before_cold_boot"]
        assert base.digest(save["source"])==save["source_sha256"]==reports["before"]["battery_save_preloaded"]["source_sha256"]
        assert all(report[k]==reports["before"][k] for k in ("core_DLL_sha256","core_options"))
    assert reports["before"]["scripted_input_schedule"]==reports["paid"]["scripted_input_schedule"]==base.load(ROOT/"paid_inputs.json")
    assert reports["refused"]["scripted_input_schedule"]==base.load(ROOT/"declined_inputs.json")
    original = base.load(ORIGINAL_TRACE)
    calls = [row for row in original["source_requests"] if row["message_ID"]==827]
    assert [(r["PC"],r["caller_LR"],r["frame"]) for r in calls]==[(0x0205528C,0x02053FF8,6819),(0x020534F4,0x02053FF8,6819)]
    evidence[str(ORIGINAL_TRACE)] = base.digest(ORIGINAL_TRACE)

    def captured(label,frame):
        [row] = [r for r in reports[label]["frames_captured"] if r["frame"]==frame and "_cold_boot.png" in r["path"]]
        assert base.digest(row["path"])==row["PNG_sha256"]
        evidence[row["path"]]=row["PNG_sha256"]
        return row,Image.open(row["path"]).convert("RGB")

    def panel(image,lines):
        masks=[]
        for i,text in enumerate(lines):
            y=296+i*16
            masks.append(font_mask(image,font,text,22,y+1,(16,y,244,y+16),COLOR))
        assert all(image.getpixel((x,y))!=COLOR for x in range(16,244) for y in range(296+len(lines)*16,344))
        return masks

    unchanged=[]
    for frame in (3751,4151,4551,4951,5351,5751,6151,6551,6951,7351,7751,8151,8551,8951):
        a,old = captured("before",frame)
        b,current = captured("paid",frame)
        if frame!=6951:
            assert a["framebuffer_sha256"]==b["framebuffer_sha256"]
            unchanged.append(frame)
            continue
        diff = ImageChops.difference(old,current).getbbox()
        assert diff and diff[0]>=BODY[0] and diff[1]>=BODY[1] and diff[2]<=BODY[2] and diff[3]<=BODY[3]
        lines = ("Ah, Hodram? Here's to meeting you!",)
        toast=dict(frame=b,lines=lines,ink=panel(current,lines))

    choice,_ = captured("refused",6151)
    yes,_ = captured("paid",6151)
    assert choice["framebuffer_sha256"]==yes["framebuffer_sha256"]
    refused,decline = captured("refused",6551)
    response=("Oh, I thought you could handle","another drink.")
    refusal=dict(frame=refused,lines=response,ink=panel(decline,response))
    returned,back = captured("refused",7351)
    assert back.getpixel((0,300))!=decline.getpixel((0,300))
    return dict(toast=toast,refusal=refusal,ordinary_town_return=returned,
        original_toast_selector_calls=calls,exact_same_frame_controls=unchanged,evidence=evidence,
        unmodified_gameplay_inputs=True,hardware=False,live_gift_scenes=False)


def domains(cpu,get,arm):
    def ptr(address):
        return unpack("<I",cpu.mem_read(address,4))[0]
    db = get(0xCB190)
    items=[]
    for i in range(218):
        obj=db+4+20*i
        at=get(ptr(ptr(obj)+8)-0x02000000,obj)
        value=bytes(cpu.mem_read(at,256)).split(b"\0",1)[0]
        assert value and b"\n" not in value
        items.append(value)
    old = base.load(HISTORICAL)
    old_items = [bytes.fromhex(row["name_hex"]) for row in old["current_items"]]
    differences = [(i,old_value.hex(),new_value.hex()) for i,(old_value,new_value) in enumerate(zip(old_items,items,strict=True)) if old_value!=new_value]
    selectors=[]
    route = unpack("<I",arm[0x5B0A0:0x5B0A4])[0]+0x48
    original=bytes(cpu.mem_read(route,4))
    for table,ids in ((0x021166E0,range(830,834)),(0x02116610,range(835,839))):
        assert unpack("<4I",cpu.mem_read(table,16))==tuple(ids)
        for index,number in enumerate(ids):
            cpu.mem_write(route,index.to_bytes(4,"little"))
            assert get(0x53C6C,table)==number
            selectors.append(dict(table=table,route=index,selected_id=number))
    cpu.mem_write(route,original)
    return items,differences,selectors


def offline(storage,rom,arm,actual):
    snapshot=ROOT/"paid/frame_006951_arm9_ram.bin"
    evidence=base.load(ROOT/"paid/capture_report.json")
    [bound] = [r for r in evidence["read_only_capture_RAM_snapshots"] if r["frame"]==6951]
    assert base.digest(snapshot)==bound["sha256"]
    raw=snapshot.read_bytes()
    assert len(raw)==0x400000
    clean=base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert all(arm[a:b]==clean[a:b] for a,b in ((0x5923C,0x59624),(0x59EDC,0x59F40)))
    cpu,get=get_machine(arm,raw)
    items,differences,selectors=domains(cpu,get,arm)
    assert len(items)==218
    rows={r["message_id"]:r for r in storage["records"]}
    cases=[]
    for number,values in ((827,NAMES),(831,items)):
        row=rows[number]
        for index,value in enumerate(values):
            case=tavern.format_case(cpu,row,(value,))
            raw_line=bytes.fromhex(case["formatted_hex"])
            lines=case["lines"]
            assert 1<=len(lines)<=3 and all(len(line.encode("cp932"))*6+6<=228 for line in lines)
            assert "%s" not in " ".join(lines) and b"\0" not in raw_line
            if number==827:
                assert len(lines)==1 and not case["findings"]
                if value==b"Hodram":
                    assert tuple(lines)==actual["toast"]["lines"]
            cases.append(case|dict(native_value_index=index))
    candidates=[]
    for number in (827,831):
        group=[row for row in cases if row["id"]==number]
        if number==827:
            candidates.extend(group)
            continue
        by_shape={}
        for row in group:
            word=bytes.fromhex(row["values_hex"][0])
            shape=(len(row["lines"]),len(word)%2,any(c>=128 for c in word))
            prior=by_shape.get(shape)
            if prior is None or len(word)>len(bytes.fromhex(prior["values_hex"][0])):
                by_shape[shape]=row
        candidates.extend(by_shape[key] for key in sorted(by_shape))
        shortest=min(group,key=lambda row:len(row["values_hex"][0]))
        if shortest not in candidates:
            candidates.append(shortest)

    raster, independent, geometry = font_tools(rom)
    kanji=rom.read_file("/GRP/KANJI.FNT")
    contact=Image.new("RGB",(3*468,127*((len(candidates)+2)//3)),"#242932")
    draw=ImageDraw.Draw(contact)
    pages=[]
    for i,row in enumerate(candidates):
        lines=row["lines"]
        body=bytes.fromhex(row["formatted_hex"])
        events=[]
        actual_plane=raster(arm,body,0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events)
        predicted=independent(arm,kanji,lines)
        assert predicted[-228:]==bytes(228) and actual_plane==bytes(228)+predicted[:-228]
        assert [ev["code"] for ev in events if ev["code"]!=32]==glyph_codes(body)
        assert all(0<=ev["x"] and ev["x"]+(12 if ev["code"]>255 else 6)<=228
            and 0<=ev["y"] and ev["y"]+12<=48 for ev in events)
        x,y=(i%3)*468,(i//3)*127
        page=Image.frombytes("L",(228,48),bytes(0 if v else 255 for v in actual_plane))
        contact.paste(page.convert("RGB").resize((456,96),Image.Resampling.NEAREST),(x+5,y+21))
        draw.text((x+5,y+3),f'{row["id"]} / '+bytes.fromhex(row["values_hex"][0]).decode("cp932"),fill="white")
        pages.append(dict(id=row["id"],index=row["native_value_index"],lines=lines,
            complete_ink_and_blank_mask_exact=True,glyphs_in_order=True))
    sheet=ROOT/"native_pages.png"
    contact.save(sheet)
    return dict(cases=cases,current_item_getters=len(items),item_name_changes_from_historical_context=differences,
        original_eight_gift_selectors=selectors,native_fonts=pages,current_snapshot=str(snapshot),
        snapshot_sha256=base.digest(snapshot),geometry=geometry,sheet=str(sheet),sheet_sha256=base.digest(sheet))


def main():
    assert not OUT.exists()
    stored=base.load(stage.STORED)
    assert base.digest(stage.ROM)==stored["candidate_sha256"]
    rom=base.NdsImage.open(stage.ROM)
    arm=rom.read_file(stage.ARM)
    observed=live(stored,GameAsciiFont.from_arm9(arm))
    native=offline(stored,rom,arm,observed)
    rows=stored["records"]
    for row in rows:
        row["review"]["formatting"]=True
        if row["message_id"]==827:
            row["speaker"]="Tavern attendant (Faticia in the observed exchange)"
    batch=dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=list(stage.GATES),records=rows,observed_gameplay=observed,native_layout=native,
        candidate_sha256=stored["candidate_sha256"],full_goal_complete=False)
    validate_natural_dialogue_batch(batch)
    base.save(OUT,batch)
    print(f'{len(native["cases"])} controlled substitutions and {len(native["native_fonts"])} full native glyph pages passed. Paid toast and drink refusal observed.')


if __name__ == "__main__":
    main()
