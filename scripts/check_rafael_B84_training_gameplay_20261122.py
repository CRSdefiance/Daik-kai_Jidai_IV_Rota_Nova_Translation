"""Verify every B84 excerpt hold and the real controller choices against stored text."""

from PIL import Image

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts.audit_captain_name_latin_20261119 import LABEL_COLOR, GameAsciiFont, glyphs
from scripts import replay_rafael_B84_training_20261122 as replay
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_rafael_B84_training_20261122 as verify
from scripts.verify_all_items_gallery_v535 import glyph_pixels
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check
from scripts.verify_story_literal_names_20261122 import make_sheet


base, native, stage = replay.base, replay.native, replay.stage
OUTPUT = replay.ROOT / "verified_gameplay.json"
MENU_INK = (8,8,8)
MENU_HIGHLIGHT = [0,165,172]


def screen(report, frame):
    picture, = (r for r in report["frames_captured"] if r["frame"] == frame)
    assert base.digest(picture["path"]) == picture["PNG_sha256"]
    with Image.open(picture["path"]) as image:
        return picture,image.convert("RGB")


def capture(name,kind,candidate):
    root = replay.run_root(name)
    path = root/"capture/capture_report.json"
    config = base.load(replay.ROOT/kind/"fixture.json")
    report = base.load(path)
    assert report["ROM_sha256"]==config["rom_sha256"]==base.digest(config["path"])
    assert config["candidate_sha256"]==candidate and config["exact_inverse"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded")
    assert report["scripted_input_schedule"]==base.load(root/"inputs.json")
    return report,path,config


def captions(font,image,texts):
    matches = []
    for text in texts:
        x=128-3*len(text)
        raw=glyph_pixels(font,b"",(),text,x,0,6)
        positions=[]
        for y in range(235,332):
            ink={(i,j-y) for i in range(x,x+6*len(text)) for j in range(y,y+11)
                 if image.getpixel((i,j))==MENU_INK}
            if ink==raw:
                positions.append(y)
        y,=positions
        matches.append(dict(text=text,origin=[x,y],background=list(image.getpixel((128,y-2)))))
    assert [r["origin"][1] for r in matches]==sorted({r["origin"][1] for r in matches})
    return matches


def main():
    assert not OUTPUT.exists()
    stored, commands = replay.commands_for()
    candidate = stored["candidate_sha256"]
    active = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE,active["own_registered_startup"],captain=3)
    paint = display.clipped_renderer(ctx)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    names = GameAsciiFont.from_arm9(ctx.arm)
    rows = {r["id"]:r for r in stored["editorial_records"]}
    stored_pages = {r["id"]:r for r in base.load(stage.NATIVE)["records"]}
    system = {r["stored_offset"]:r for r in base.load(verify.FE_PROOF)["records"]}
    screenshots, observations, menus, report_hashes = [], [], [], {}

    def body_panel(command, frame, report, script):
        hold, image = screen(report, frame)
        at = command["stored_offset"]
        ids=command["record_ids"]
        ident=ids[0] if ids else command["retained_continuation_of"]
        row=rows[ident]
        if at in system:
            exact=system[at]
            assert exact["exact_command_hex"]==command["stored"]
            title=row["id"]+(" / second FE page" if exact["second_page"] else " / first FE page")
            hex_plane=exact["physical_plane_hex"]
            assert mask_check(bytes.fromhex(hex_plane),228,image),(script,title,frame)
        else:
            if ident in stored_pages:
                layout=stored_pages[ident]["layouts"][0]
                page,=layout["pages"]
            else:
                raw=bytes.fromhex(command["stored"])
                body=raw[6:raw.index(0,6)]
                assert not any(token in body for token in (b"FI",b"FA",b"FO",b"FU"))
                rendered=paint(ctx.arm,font,body)
                assert rendered["complete_consumed_bytes"]==len(body)
                page,=rendered["pages"]
            hex_plane=page["native_plane_hex"]
            title=row["id"]+" / "+row["speaker"]
            assert mask_check(bytes.fromhex(hex_plane),216,image),(script,title,frame)
            glyphs(names,image,row["speaker"],(16,277),LABEL_COLOR,226)
        observations.append(dict(script=script,id=ident,stored_offset=at,capture=hold,caption=title,
                                 exact_complete_body_mask=True))
        screenshots.append((title,image))

    report,path,sequence=capture("speech","speech",candidate)
    report_hashes[str(path)]=base.digest(path)
    assert not sequence["contiguous_B84_suffix_with_original_branches"]
    frames=(3900,*(4300+370*i for i in range(11)))
    for command, frame in zip(sequence["original_commands"][:-1],frames,strict=True):
        body_panel(command,frame,report,"speech")
    exit_shot,image=screen(report,8370)
    screenshots.append(("Return to the original host town",image))

    for name,kind,menu_frames,response_frame,response in (
        ("defeat","pact_entry",(4650,4900),5410,"R0234"),
        ("alternative","pact_entry",(4650,4900),5410,"R0327"),
        ("lesson_only","lesson_entry",(4260,4540),5050,"R0511"),
    ):
        report,path,config=capture(name,kind,candidate)
        report_hashes[str(path)]=base.digest(path)
        assert config["contiguous_B84_suffix_with_original_branches"]
        opcode=0x2200 if name=="lesson_only" else 0x2100
        command,=(c for c in config["original_commands"] if c["word"]==opcode)
        strings=[v.decode("ascii") for v in labels(bytes.fromhex(command["stored"]))]
        parsed=[]
        for i,frame in enumerate(menu_frames):
            hold,image=screen(report,frame)
            visible=captions(names,image,strings)
            parsed.append(dict(capture=hold,labels=visible))
            screenshots.append((name+" menu / "+("initial" if i==0 else "after input"),image))
        before=[r["background"] for r in parsed[0]["labels"]]
        after=[r["background"] for r in parsed[1]["labels"]]
        assert before[0]==MENU_HIGHLIGHT and MENU_HIGHLIGHT not in before[1:]
        assert len(before)==len(after)
        if name=="defeat":
            assert before==after
        else:
            assert after==[before[1],before[0],*before[2:]],(name,before,after)
        target,=(c for c in commands if replay.is_id(c,response))
        body_panel(target,response_frame,report,name)
        menus.append(dict(script=name,stored_offset=command["stored_offset"],opcode=opcode,
                         captions=strings,observations=parsed,selected=0 if name=="defeat" else 1,
                         response=response,executed_original_branch=True))
    assert len(observations)==15 and len(menus)==3
    sheets=[]
    for i in range(0,len(screenshots),6):
        path,sha=make_sheet(replay.ROOT/f"gameplay_{i//6+1}.png",screenshots[i:i+6])
        sheets.append(dict(path=path,sha256=sha))
    base.save(OUTPUT,dict(candidate_sha256=candidate,focused_original_excerpts=True,natural_trigger_unvisited=True,
        original_menu_choices=menus,observations=observations,observed_speech_pages=len(observations),
        return_frame=exit_shot,native_FE_panels_observed=4,report_sha256=report_hashes,sheets=sheets,hardware=False))
    print("Verified 15 exact text panels, both retained FE sequences and three original menu selections.",flush=True)


if __name__=="__main__":
    main()
