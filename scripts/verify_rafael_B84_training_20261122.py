"""Verify the installed B84 text, exact font pixels and original typed choice."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import sys
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import check_rafael_two_choice_display_v2 as menu
from scripts import generic_name_macro_owned_v5886b as macro
from scripts import stage_rafael_B84_training_20261122 as stage
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts import verify_all_routes_next_phrase_wraps_20261118 as display
from scripts import verify_palace_london_glyphs_20261122 as glyphs
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
MENU_ROOT = stage.ROOT / "native_menu"
MENU_INPUT = stage.ROOT / "typed_choice_input.json"
MENU_PROOF = MENU_ROOT / "menu_provider_and_planes.json"
GLYPH_PROOF = stage.ROOT / "glyph_and_sheet_verification.json"
FE_PROOF = stage.ROOT / "unchanged_FE_pages.json"


def verify_text():
    stored, release = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(stage.ROM)
    assert stored["predecessor_sha256"] == base.digest(stage.parent.ROM) == release["candidate_sha256"]
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    font = image.read_file("/GRP/KANJI.FNT")
    paint = display.clipped_renderer(ctx)
    saved = base.load(display.build.parent.display.PROOF)["previous_initialized_rafael_context"]
    boot, identity = map(Path,(saved["path"],saved["identity"]))
    assert base.digest(boot)==saved["sha256"] and base.digest(identity)==saved["identity_sha256"]
    rafael = native.RegisteredRuntime(identity,boot,captain=0)
    sections = MainCodeFile(ctx.arm,0x02000000).sections
    macro_source = checked_text(getsource(macro.expand),{
        "assert identity==prefix and captain==2":"assert identity==prefix and captain==0",
        "current_executed_instruction_addresses=len(provider.executed_current)":
            "executed_addresses=sorted(provider.executed_current)",
    })
    words = vars(macro).copy()
    exec(compile(macro_source,__file__+"::original-company-substitution","exec"),words)
    fe = current_fe_painter(ctx)
    records = {r["id"]: r for r in stored["editorial_records"]}
    group, = stored["groups"]
    payload = native.IlnkContainer.parse(image.read_file(stage.PATH)).blocks[stage.BLOCK]
    assert native.digest(payload) == group["after"]
    checked, pictures, retained_fe, fe_pictures, choices = [], [], [], [], {}
    for command in group["commands"]:
        raw = bytes.fromhex(command["stored"])
        start = command["stored_offset"]
        assert payload[start:start + len(raw)] == raw
        if command["word"] in stage.forest.MENU:
            choices[command["word"]] = command
            continue
        if command["word"] != stage.forest.SPEECH:
            continue
        ids = command["record_ids"]
        body = raw[6:raw.index(0, 6)]
        if not ids or raw[5] == 254:
            assert command["current"] == command["stored"]
            continuation = command["retained_continuation_of"]
            if continuation or (ids and records[ids[0]].get("current_FE_continuation")):
                assert raw[:6] == bytes.fromhex("0040ffff00fe")
                page = fe(body)
                membership = stage.forest.system.check_FE_rows(body, page)
                assert page["complete_consumed_bytes"] == len(body)
                plane = page["physical"]
                assert all(not any(plane[y*228+216:(y+1)*228]) for y in range(64))
                cropped = b"".join(plane[y*228:y*228+216] for y in range(64))
                title = (continuation or ids[0]) + (" / second page" if continuation else " / first page")
                fe_pictures.append((title, cropped))
                retained_fe.append(dict(owner=continuation or ids[0],second_page=bool(continuation),
                   stored_offset=start,exact_command_hex=raw.hex(),row_membership=membership,
                   physical_plane_sha256=native.digest(plane),physical_plane_hex=plane.hex()))
            continue
        ident, = ids
        if ident not in group["plans"]:
            assert command["current"] == command["stored"]
            continue
        plan, row = group["plans"][ident], records[ident]
        assert " ".join(body.decode("ascii").split()) == row["english"]
        assert bytes.fromhex(command["current"])[:6] == raw[:6] and b"%" not in body
        layouts = [("no substitutions", {}, body)]
        extra = {}
        if b"FO" in body:
            assert ident.endswith("R0089") and body.count(b"FO") == 1
            actual = rafael.execute(words["expand"], body, raw[5])
            for address in actual["executed_addresses"]:
                earlier, = [s for s in rafael.sections if s.ramAddress<=address<s.ramAddress+len(s.data)]
                latest = [s for s in sections if s.ramAddress<=address<s.ramAddress+len(s.data)]
                if not latest:
                    latest=[s for s in ctx.sections if s.ramAddress<=address<s.ramAddress+len(s.data)]
                current_code, = latest
                a,b=address-earlier.ramAddress,address-current_code.ramAddress
                assert earlier.data[a:a+4]==current_code.data[b:b+4],hex(address)
            names = {"FO":"Castor Co."}
            completed = body.replace(b"FO", b"Castor Co.")
            assert len(actual["cases"]) == 4 and {c["output_hex"] for c in actual["cases"]} == {completed.hex()}
            extra = {"original_expansion": actual}
            layouts = [("default company", names, completed),
                       ("maximum company", {"FO":"W"*20}, body.replace(b"FO", b"W"*20))]
        current = dict(id=ident, route=0, command_offset=start, exact_command_hex=raw.hex(),
                       body_hex=(raw[5:6]+body).hex(), layouts=[], **extra)
        for title, names, value in layouts:
            lines = [display.display.expected(line,names) for line in plan["lines"]]
            page, = display.display.raster(ctx,font,paint,value,lines,1)
            assert page["native_independent_plane_equal"]
            pictures.append((ident+" / "+title,bytes.fromhex(page["native_plane_hex"])))
            current["layouts"].append(dict(scope=title,lines=lines,pages=[page],expanded_body_hex=value.hex()))
        checked.append(current)
    assert len(checked)==8 and len(pictures)==9 and len(retained_fe)==4
    assert set(choices)==set(stage.forest.MENU)
    assert choices[0x2200]["current"]==choices[0x2200]["stored"]
    contact = display.display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | dict(ROOT=stage.ROOT))(pictures)
    base.save(stage.NATIVE,dict(candidate_sha256=stored["candidate_sha256"],stage_sha256=base.digest(stage.PROOF),
        records=checked,sheets=sheets,pages=len(pictures),offline_native_only=True))
    FunctionType(glyphs.verify.__code__,vars(glyphs)|dict(stage=stage,OUTPUT=GLYPH_PROOF))()
    fe_root = stage.ROOT / "retained_FE"
    fe_root.mkdir()
    fe_sheets = FunctionType(contact.__code__,contact.__globals__|dict(ROOT=fe_root))(fe_pictures)
    base.save(FE_PROOF,dict(candidate_sha256=stored["candidate_sha256"],records=retained_fe,sheets=fe_sheets,
        original_modal_consumer=True,complete_stored_page_count=4))
    changed = choices[0x2100]
    a,b = (bytes.fromhex(changed[key]) for key in ("source","current"))
    manuscript = []
    for i,(j,e,ident) in enumerate(zip(labels(a),labels(b),changed["record_ids"],strict=True)):
        row = records[ident]
        manuscript.append(row | dict(kind="typed-choice-label",source_index=i,source_choice_object_hex=a.hex(),
            current_choice_object_hex=b.hex(),source_hex=j.hex(),current_hex=e.hex(),
            source_reference=dict(file_path=stage.PATH,block=84,command_offset=row["source_command_offset"]),
            current_reference=dict(file_path=stage.PATH,block=84,command_offset=row["current_command_offset"])))
    base.save(MENU_INPUT,dict(current_ROM_sha256=release["candidate_sha256"],typed_choice_objects=2,records=manuscript))
    print("Verified the eight installed speeches, nine layout variants and four unchanged FE panels.",flush=True)


def verify_menu():
    stored = base.load(stage.PROOF)
    checked = base.load(MENU_PROOF)
    group, = stored["groups"]
    command, = (c for c in group["commands"] if c["word"] == 0x2100)
    raw = bytes.fromhex(command["stored"])
    bank = native.IlnkContainer.parse(base.NdsImage.open(stage.ROM).read_file(stage.PATH)).blocks[84]
    at = command["stored_offset"]
    assert bank[at:at+len(raw)] == raw == (MENU_ROOT/"compiled_choice_object.bin").read_bytes()
    assert checked["native_choice_object_hex"]==raw.hex()
    assert checked["complete_caption_glyphs_centering_bounds_guards_andconsumption_pass"]
    assert checked["complete_English_caption_style_planes"]==8 and len(checked["compiler_negatives_rejected"])==7
    base.save(stage.ROOT/"installed_choice_verification.json",dict(candidate_sha256=stored["candidate_sha256"],
       installed_offset=at,exact_command_hex=raw.hex(),caption_labels=[x.decode("ascii") for x in labels(raw)],
       provider_proof_sha256=base.digest(MENU_PROOF),sheet=checked["review_sheet"],real_input_playback_separate=True))
    print("Verified original choice provider, both alignments, stored command and complete caption pixels.",flush=True)


def replay_provider():
    release = base.load(stage.parent.RELEASE)
    sys.argv=[menu.__file__,"--manuscript",str(MENU_INPUT),"--release",str(stage.parent.RELEASE),
        "--startup",release["own_registered_startup"],"--out",str(MENU_ROOT)]
    source = checked_text(menu.source,{"captain=0":"captain=3"})
    scope = menu.main.__globals__ | dict(__name__="b84_native_choice_provider")
    exec(compile(source,__file__+"::registered-runtime-typed-provider","exec"),scope)
    scope["main"]()
    verify_menu()


if __name__=="__main__":
    cli=ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("text","menu","provider"))
    action=cli.parse_args().action
    if action=="text":
        verify_text()
    elif action=="menu":
        verify_menu()
    else:
        replay_provider()
