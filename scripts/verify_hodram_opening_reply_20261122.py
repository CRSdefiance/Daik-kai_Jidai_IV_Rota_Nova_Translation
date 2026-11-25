"""Verify all revised pages against the native renderer and the original Hodram opening."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_hodram_opening_reply_20261122 as stage
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as screenshot
from scripts import verify_story_literal_names_20261122 as prior
from scripts.audit_captain_name_latin_20261119 import LABEL_COLOR, glyphs


base, native, parent = stage.base, stage.native, stage.parent
NATIVE = stage.ROOT/"native_display.json"
LIVE = stage.ROOT/"ordinary_dialogue.json"
SHEET = stage.ROOT/"ordinary_exchange.png"
PAGES = {24670:116,25020:120,26420:135}
TITLE = (prior.captured.MAX+b" "+prior.captured.EXPECTED_FIELDS[1]).decode("ascii")


def native_display():
    assert not NATIVE.exists()
    stored, preceding = map(base.load,(stage.PROOF,parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] and base.digest(parent.ROM) == preceding["candidate_sha256"]
    assert stored["predecessor_sha256"] == preceding["candidate_sha256"] and stored["whole_parent_inverse"]
    ctx = native.RegisteredRuntime(parent.RELEASE,preceding["own_registered_startup"],captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    block = native.IlnkContainer.parse(image.read_file(stage.PATH)).blocks[stage.BLOCK]
    assert native.digest(block) == stored["after_block_sha256"]
    font = image.read_file("/GRP/KANJI.FNT")
    paint = display.clipped_renderer(ctx)
    rows = {row["id"]:row for row in stored["records"]}
    checked, pictures = [], []
    for command in stored["commands"]:
        ids = command["record_ids"]
        if not ids:
            continue
        ident, = ids
        row = rows.pop(ident)
        compiled = bytes.fromhex(command["stored"])
        before, source = [bytes.fromhex(command[key]) for key in ("current","source")]
        at = command["stored_offset"]
        assert block[at:at+len(compiled)] == compiled
        assert source[:6] == before[:6] == compiled[:6] == b"\0\x40\xff\xff\0"+bytes([row["source_selector"]])
        stop = compiled.index(0,6)
        assert not any(compiled[stop:]) and " ".join(compiled[6:stop].decode("cp932").split()) == row["english"]
        recorded = dict(id=ident,file_path=stage.PATH,block=stage.BLOCK,candidate_sha256=candidate,
            archive_sha256=stored["archive_sha256"],block_sha256=stored["after_block_sha256"],
            command_offset=at,offset=at+5,exact_stored_hex=compiled[5:stop].hex(),exact_command_hex=compiled.hex())
        if ident in stage.CHANGED:
            plan = stored["plans"][ident]
            encoded = bytes.fromhex(plan["encoded_hex"])
            assert compiled[5:stop] in (encoded,encoded+b" ") and plan["expected_native_pages"] == 1
            assert not any(d["severity"]=="error" for d in plan["diagnostics"])
            body = compiled[6:stop]
            # None of the three authored replacements adds a runtime token or a printf directive.
            assert not any(token in body or token in before[6:] for token in (b"FI",b"FA",b"FO",b"FU",b"%"))
            pages = display.display.raster(ctx,font,paint,body,plan["lines"],1)
            page, = pages
            assert page["native_independent_plane_equal"]
            pixels = bytes.fromhex(page["native_plane_hex"])
            pictures.append((ident,pixels))
            checked.append(dict(id=ident,reference=recorded,fresh_native_page=page))
        else:
            assert compiled == before
            checked.append(dict(id=ident,reference=recorded,earlier_layout_reused=True))
    assert not rows and len(checked)==15 and len(pictures)==3
    sheet_maker = display.display.inherited.early.contact_sheets
    sheets = FunctionType(sheet_maker.__code__,sheet_maker.__globals__ | {
        "ROOT":stage.ROOT, "PREFIX":"hodram_reply_native"})(pictures)
    base.save(NATIVE,dict(candidate_sha256=candidate,stage_proof_sha256=base.digest(stage.PROOF),
        records=checked,sheets={str(p["path"]):p["sha256"] for p in sheets},offline_native_only=True,
        complete_bounds_and_consumed_bytes=True,stored_references_and_padding_checked=True))
    print("Three changed pages matched the independent native glyph planes; 12 retentions are byte-exact.",flush=True)


def gameplay():
    assert not LIVE.exists()
    native_report, report = map(base.load,(NATIVE,stage.REPORT))
    candidate = base.digest(stage.ROM)
    assert report["ROM_sha256"] == native_report["candidate_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and not any(v for k,v in report.items() if k.startswith("synthetic_"))
    old_capture_path = prior.REPORTS["fixed"]
    old = base.load(old_capture_path)
    assert old["ROM_sha256"] == base.load(parent.RELEASE)["candidate_sha256"]
    control_path = stage.baseline.stage.parent.stage.BASELINE
    controls = base.load(control_path)
    assert report["scripted_input_schedule"] == [e for e in controls["scripted_input_schedule"] if e["start"]<report["frames"]]
    arm = base.NdsImage.open(stage.ROM).read_file(native.ARM)
    font = GameAsciiFont.from_arm9(arm)
    native_rows = {r["id"]:r for r in native_report["records"]}
    holds, pictures = [], []
    for number in stage.FRAMES:
        shot, = [r for r in report["frames_captured"] if r["frame"]==number]
        assert base.digest(shot["path"])==shot["PNG_sha256"]
        with Image.open(shot["path"]) as opened:
            image = opened.convert("RGB")
        if number in PAGES:
            ident = f"DK4_MES_B42_R{PAGES[number]:04d}"
            page = native_rows[ident]["fresh_native_page"]
            assert screenshot.mask_check(bytes.fromhex(page["native_plane_hex"]),216,image), (ident,number)
            heading = glyphs(font,image,TITLE,(16,277),LABEL_COLOR,226)
            holds.append(dict(id=ident,frame=shot,nameplate=heading,mask_exact=True))
            pictures.append((f"Revised / {ident}",image))
        else:
            if number in (24320,25370):
                earlier, = [r for r in old["frames_captured"] if r["frame"]==number]
                assert base.digest(earlier["path"])==earlier["PNG_sha256"]
                with Image.open(earlier["path"]) as view:
                    assert view.convert("RGB").crop((0,192,256,357)).tobytes() == image.crop((0,192,256,357)).tobytes()
            holds.append(dict(frame=shot,transition_context=True))
            pictures.append((f"Story sequence / frame {number}",image))
    assert {r.get("id") for r in holds if r.get("mask_exact")} == stage.CHANGED
    key,sha = prior.make_sheet(SHEET,pictures)
    paths = (stage.REPORT,stage.PROOF,NATIVE,old_capture_path,control_path)
    base.save(LIVE,dict(candidate_sha256=candidate,predecessor_sha256=old["ROM_sha256"], actual_original_opening=True,
        observed=holds,sheets={key:sha},exact_changed_body_masks=3,retained_Charles_surname_panel=True,
        ordinary_controls_only=True,hardware=False,evidence={str(p):base.digest(p) for p in paths}))
    print("All three revised pages and their ordinary transitions matched the staged text.",flush=True)


if __name__=="__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("native_display","gameplay"))
    globals()[cli.parse_args().action]()
