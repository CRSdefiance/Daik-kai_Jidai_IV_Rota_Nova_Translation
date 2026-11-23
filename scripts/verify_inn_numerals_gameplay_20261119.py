"""Verify complete stay and dated rumor text in the original Inn UI."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from scripts import replay_inn_numerals_context_20261119 as game
from scripts import replay_inn_raid_numerals_20261119 as raid
from scripts import verify_inn_numerals_native_20261119 as oracle
from scripts.finish_refit_display_v712 import load as load_capture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring

stage = game.stage
base,inn = stage.base,stage.parent.stage


def visible(image, rom, arm, case, raster, independent):
    raw = bytes.fromhex(case["formatted_hex"])
    plane,used = raster(arm,raw,0x01FFCE40-stage.patch.BASE,size=(228,64),complete=False,instruction_limit=2000000)
    assert used==len(raw) and plane==independent(arm,rom.read_file("/GRP/KANJI.FNT"),case["lines"])
    wanted = {(16+i%228,296+i//228) for i,v in enumerate(plane) if v==1}
    actual = {(x,y) for y in range(294,360) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
    assert wanted==actual
    return len(wanted)


def verify_stay(rom,arm,candidate,records,raster,independent,evidence):
    paths = [game.CAPTURE/p for p in ("capture/capture_report.json","requests.json","terminal.json")]
    previous_paths = [stage.parent.game.CAPTURE/p for p in ("capture/capture_report.json","requests.json","terminal.json")]
    current,trace,terminal = map(base.load,paths)
    before,prior_trace,prior_end = map(base.load,previous_paths)
    events,_,end,_,donor = game.inn.schedule("istanbul")
    assert current["ROM_sha256"]==terminal["ROM_sha256"]==candidate
    assert before["ROM_sha256"]==prior_end["ROM_sha256"]==base.digest(stage.parent.ROM)
    for report,receipt in ((current,trace),(before,prior_trace)):
        assert report["frames"]==end and report["scripted_input_schedule"]==events
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
        assert receipt["all_host_slots_restored_and_core_file_exact"] and not receipt["errors"] and not receipt["mismatches"]
        assert report["battery_save_preloaded"]["source_sha256"]==donor["source_sha256"]==base.digest(donor["source"])
    assert current["core_options"]==before["core_options"]
    assert trace["source_requests"]==prior_trace["source_requests"]
    now,old = ({r["frame"]:r for r in page["frames_captured"]} for page in (current,before))
    assert now.keys()==old.keys()
    assert {f for f in now if now[f]["framebuffer_sha256"]!=old[f]["framebuffer_sha256"]}=={7000}
    evidence.update({str(p):base.digest(p) for p in (*paths,*previous_paths)})

    def screen(row):
        path = row["path"]
        assert base.digest(path)==row["PNG_sha256"]
        evidence[path] = row["PNG_sha256"]
        with Image.open(path) as opened:
            return opened.convert("RGB")

    earlier,corrected,returned = screen(old[7000]),screen(now[7000]),screen(now[8600])
    x,y,right,lower = ImageChops.difference(earlier,corrected).getbbox()
    assert 16<=x<right<=244 and 294<=y<lower<=344
    case, = (c for c in records[1180]["layout_cases"] if c["source_values_hex"]==[b"3".hex()])
    pixels = visible(corrected,rom,arm,case,raster,independent)
    return dict(message_ID=1180,frame=7000,lines=case["lines"],complete_visible_ink=pixels,
        actual_numeric_argument="3",normal_return_frame=8600,exact_other_frames=sorted(set(now)-{7000}),
        changed_pixels_only_in_dialogue=[x,y,right,lower]), (earlier,corrected,returned)


def verify_raid(rom,arm,candidate,records,raster,independent,evidence):
    report,images,receipt = load_capture(raid.ROOT,candidate,6400)
    evidence[receipt["report"]] = receipt["sha256"]
    journal = raid.ROOT/"navigation_command_journal.json"
    assert [row["command"] for row in base.load(journal)["commands_received"]]==raid.schedule()
    evidence[str(journal)] = base.digest(journal)
    fixture, = report["synthetic_condition_fixtures"]
    assert fixture["frame"]==3200 and fixture["request"]==raid.REQUEST
    assert fixture["no_code_text_dialogue_selection_menu_flags_or_result_replacement"]
    assert fixture["all_other4MiB_RAM_bytes_exact"]
    observed, = fixture["original_dispatcher_preflight"]
    assert observed["message"]==1197
    values = tuple(bytes.fromhex(value) for value in observed["values_hex"])
    assert values[0]==b"10 months ago"
    raw = {}
    for r in report["read_only_capture_RAM_snapshots"]+report["read_only_pause_RAM_snapshots"]:
        path = r["path"]
        region = Path(path).read_bytes()
        assert len(region)==0x400000 and base.digest(path)==r["sha256"] and r["read_only_export"]
        assert raw.setdefault(r["frame"],region)==region
        evidence[path] = r["sha256"]
    _,proof = raid.fixture(arm,raw[3200],raid.REQUEST)
    assert proof=={k:v for k,v in fixture.items() if k!="frame"}
    history = fixture["history_record"]-stage.patch.BASE
    original_input = bytes.fromhex(fixture["fixture_history_hex"])
    assert raw[5600][history:history+12]==original_input
    assert raw[6400][history:history+12]==original_input[:4]+b"\x15"+original_input[5:]
    owner,formatted,expanded = (unpack_from("<I",arm,p)[0] for p in (0x552A0,0x54450,0x5444C))
    target = records[1197]
    paragraph = bytes.fromhex(target["staged_hex"])
    assert cstring(raw[5600],owner+0x2030)==paragraph
    for value in values:
        paragraph = paragraph.replace(b"%s",value,1)
    assert cstring(raw[5600],expanded)==paragraph
    scope = vars(oracle.formatting).copy()
    exec(compile(inn.FORMATTER.read_text(encoding="utf-8"),str(inn.FORMATTER),"exec"),scope)
    template = next(r for r in base.load(inn.HISTORY)["records"] if r["message_ID"]==1197)
    cpu,_ = get_machine(arm,raw[5600])
    case = scope["format_case"](cpu,template|{"english":target["english"]},values)
    assert bytes.fromhex(case["formatted_hex"])==cstring(raw[5600],formatted) and not case["findings"]
    pixels = visible(images[5600],rom,arm,case,raster,independent)
    assert images[3200].crop((0,0,256,192)).tobytes()==images[6400].crop((0,0,256,192)).tobytes()
    evidence.update({r["path"]:r["PNG_sha256"] for r in report["frames_captured"] if r["frame"] in (3200,5600,6400)})
    return dict(message_ID=1197,frame=5600,lines=case["lines"],complete_visible_ink=pixels,
        native_argument_bytes=[v.hex() for v in values],fixture_disclosed=fixture,history_consumed=True,
        return_frame=6400,natural_activation=False), (images[5600],images[6400])


def main():
    assert not game.PLAYBACK.exists()
    candidate = base.digest(stage.ROM)
    proof = base.load(stage.NATIVE_PROOF)
    assert proof["candidate_sha256"]==candidate
    records = {r["message_ID"]:r for r in proof["records"]}
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.ARM)
    raster,independent,_ = inn.physical_renderers(rom)
    evidence = {str(Path(__file__)):base.digest(__file__)}
    stay,screens = verify_stay(rom,arm,candidate,records,raster,independent,evidence)
    rumor,more = verify_raid(rom,arm,candidate,records,raster,independent,evidence)
    labels = ("3-night confirmation before", "3-night confirmation revised", "Normal town return", "Seeded 10-month raid rumor", "Return after the rumor")
    sheet = Image.new("RGB",(768,420),"#263238")
    draw = ImageDraw.Draw(sheet)
    for i,(label,image) in enumerate(zip(labels,(*screens,*more),strict=True)):
        x,y = i%3*256,i//3*210
        draw.text((x+4,y+3),label,fill="white")
        sheet.paste(image.crop((0,192,256,384)),(x,y+16))
    path = stage.ROOT/"inn_confirmation_and_raid_rumor.png"
    sheet.save(path)
    evidence[str(path)] = base.digest(path)
    base.save(game.PLAYBACK,dict(candidate_sha256=candidate,ordinary_stay=stay,initialized_raid=rumor,
        hardware=False,sheets=[dict(path=str(path),sha256=base.digest(path))],evidence=evidence))
    print("Verified the normal stay and initialized raid rumor with regular numerals and complete text.")


if __name__=="__main__":
    main()
