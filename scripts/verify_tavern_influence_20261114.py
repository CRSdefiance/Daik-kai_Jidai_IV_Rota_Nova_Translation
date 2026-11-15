"""Check the revised Tavern rumor against live and controlled native display."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_tavern_conversations_v764 as tavern
from scripts import stage_tavern_influence_20261114 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.observe_current_town_replays_20261114 import ROOT as OBSERVED
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.verify_personal_gameplay_v841 import get_machine

base = stage.base
ROOT = stage.ROOT
OUT = ROOT / "reviewed_display.json"
MATRIX = Path("work/analysis/tavern_coordinates_v766/actual_leader_layout_matrix.json")
SAMPLE = (b"Hayreddin", b"Alexandria", b"pirate")


def live(stage_record, font):
    source = OBSERVED / "istanbul"
    before = source / "capture/capture_report.json"
    after = ROOT / "istanbul/capture_report.json"
    reports = [base.load(path) for path in (before, after)]
    assert [r["ROM_sha256"] for r in reports] == [stage_record["previous_sha256"], stage_record["candidate_sha256"]]
    controls = ("scripted_input_schedule", "core_DLL_sha256", "core_options")
    assert all(reports[0][k] == reports[1][k] for k in controls)
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] for r in reports)
    for report in reports:
        source_save = report["battery_save_preloaded"]
        assert source_save["copied_byte_exact_before_cold_boot"]
        assert base.digest(source_save["source"]) == source_save["source_sha256"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
    assert reports[0]["battery_save_preloaded"]["source_sha256"] == reports[1]["battery_save_preloaded"]["source_sha256"]
    requests = base.load(source/"requests.json")
    matching = [row for row in requests["source_requests"] if row["message_ID"] == 821]
    assert [row["PC"] for row in matching] == [0x0205528C,0x020534F4]
    assert all(row["frame"] == 4823 and row["caller_LR"] == 0x02053FF8 for row in matching)
    maps = [{r["frame"]:r for r in report["frames_captured"] if r["frame"] >= 3751} for report in reports]
    holds = (3751,4151,4551,4951,5351,5751,6151,6551,6951,7351,7751,8151,8551,8951)
    evidence = {str(p):base.digest(p) for p in (before,after,source/"requests.json")}
    revised = None
    for frame in holds:
        left,right = [mapping[frame] for mapping in maps]
        for row in (left,right):
            assert base.digest(row["path"]) == row["PNG_sha256"]
            evidence[row["path"]] = row["PNG_sha256"]
        if frame != 4951:
            assert left["framebuffer_sha256"] == right["framebuffer_sha256"]
        else:
            old,new = [Image.open(item["path"]).convert("RGB") for item in (left,right)]
            change = ImageChops.difference(old,new).getbbox()
            assert change and 16 <= change[0] < change[2] <= 244 and 296 <= change[1] < change[3] <= 344
            lines = ("Hayreddin from Alexandria is", "a pirate with real pull here.")
            masks = []
            for i,text in enumerate(lines):
                y = 296+16*i
                masks.append(font_mask(new,font,text,22,y+1,(16,y,244,y+16),(0,8,0)))
            assert all(new.getpixel((x,y)) != (0,8,0) for x in range(16,244) for y in range(328,344))
            revised = dict(frame=frame,lines=lines,masks=masks,image=right)
    return dict(revised=revised,unmodified_holds=[f for f in holds if f != 4951],source_request=matching,evidence=evidence)


def layout(rom, arm, report):
    matrix = base.load(MATRIX)
    assert len(matrix["cases"]) == 14400
    variants = [tuple(bytes.fromhex(b) for b in c["values_hex"]) for c in matrix["cases"] if c["id"] == 821]
    assert len(variants) == 7200
    all_roles = {c[2] for c in variants}
    assert all_roles == {b"pirate",b"trader",b"soldier",b"conqueror"}
    selected = {SAMPLE}
    for role in all_roles:
        group = [c for c in variants if c[2]==role]
        selected.add(min(group,key=lambda c: (len(c[0])+len(c[1]),c)))
        selected.add(max(group,key=lambda c: (len(c[0])+len(c[1]),c)))
        selected.add(max(group,key=lambda c: (len(c[0]),-len(c[1]),c)))
        selected.add(max(group,key=lambda c: (len(c[1]),-len(c[0]),c)))
    assert 12 <= len(selected) <= 17
    maximum = max(len(stage.DRAFT.encode("ascii") % c) for c in variants)
    assert maximum < 236
    snapshot = ROOT/"istanbul/frame_004951_arm9_ram.bin"
    raw = snapshot.read_bytes()
    assert len(raw)==0x400000
    cpu,_ = get_machine(arm,raw)
    raster, independent, geometry = font_tools(rom)
    cases = []
    contact = Image.new("RGB",(3*468,131*((len(selected)+2)//3)),"#263238")
    labels = ImageDraw.Draw(contact)
    for i,values in enumerate([SAMPLE,*sorted(selected-{SAMPLE})]):
        row = {"message_id":821,"english":stage.DRAFT}
        case = tavern.format_case(cpu,row,values)
        assert all(f in {"weak_line_end","short_final_row"} for f in case["findings"])
        text = bytes.fromhex(case["formatted_hex"])
        lines = case["lines"]
        assert len(lines)<=3 and all(len(line.encode("cp932"))*6<=228 for line in lines)
        if values == SAMPLE:
            assert tuple(lines) == tuple(report["revised"]["lines"])
        events = []
        plane = raster(arm,text,0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000,glyph_events=events)
        expected = independent(arm,rom.read_file("/GRP/KANJI.FNT"),lines)
        # The registered renderer starts the 11-pixel ink one pixel below
        # the row origin, as observed on the 296/297 live anchor.
        assert expected[-228:] == bytes(228)
        assert plane == bytes(228) + expected[:-228]
        assert [ev["code"] for ev in events if ev["code"]!=32]==glyph_codes(text)
        assert all(0<=ev["x"] and ev["x"]+(12 if ev["code"]>255 else 6)<=228
            and 0<=ev["y"] and ev["y"]+12<=48 for ev in events)
        x,y = (i%3)*468,(i//3)*131
        page = Image.frombytes("L",(228,48),bytes(0 if v else 255 for v in plane))
        contact.paste(page.convert("RGB").resize((456,96),Image.Resampling.NEAREST),(x+4,y+22))
        labels.text((x+4,y+4)," / ".join(v.decode("cp932") for v in values),fill="white")
        cases.append(case | dict(complete_three_row_native_mask=True,plane_sha256=stage.parent.source.current.assets.edit.digest(plane)))
    sheet = ROOT/"revised_native_pages.png"
    contact.save(sheet)
    return dict(cases=cases,all_source_domain_role_values=sorted(role.decode() for role in all_roles),
        maximum_provider_expansion_bytes=maximum,prior_provider_combination_count=len(variants),
        distinct_tested_cases=len(cases),source_matrix_sha256=base.digest(MATRIX),
        snapshot_sha256=base.digest(snapshot),geometry=geometry,sheet=str(sheet),sheet_sha256=base.digest(sheet))


def main():
    assert not OUT.exists()
    storage = base.load(stage.STORED)
    assert base.digest(stage.ROM) == storage["candidate_sha256"]
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.ARM)
    actual = live(storage,GameAsciiFont.from_arm9(arm))
    layouts = layout(rom,arm,actual)
    review, = storage["records"]
    assert review["english"].removesuffix("{PAD}") == stage.DRAFT
    review.update(english=stage.DRAFT,review=dict.fromkeys(stage.GATES,True))
    report = dict(translation_policy="natural-dialogue-v2",target_locale="en-US",
        encoder="dialogue-relocatable-v1",review_gates=list(stage.GATES),
        records=[review],native_layout=layouts,observed_gameplay=actual,
        candidate_sha256=storage["candidate_sha256"],full_goal_complete=False)
    validate_natural_dialogue_batch(report)
    base.save(OUT,report)
    print(f"{layouts['distinct_tested_cases']} controlled pages and one observed page; thirteen other hold frames exact.")


if __name__ == "__main__":
    main()
