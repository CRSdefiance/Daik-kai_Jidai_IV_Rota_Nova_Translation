"""Check the ordinary Alexandria Auto Move refusal and return to Athens."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_athens_auto_move_20261124 as run
from scripts import verify_additional_voyages_20261123 as earlier
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = panels.OUT.with_name("athens_alexandria_auto_move_20261124.json")
ARM, COMMON = run.current.ARM, run.current.COMMON
ROUTE_REVIEW = Path("releases/all_routes_editorial_20261123_cabin_square_wrap_candidate")
CASES = {
    85: (4150, ("38",), None, "The estimate gives about 38 sailing days with the loaded supplies. It precedes the choice of sailing mode."),
    637: (6410, (), "Charles Rochefort", "Charles reports the missing route after the player picks Alexandria. The direct sentence gives the reason for the refusal and leaves the player at the map."),
}


def route_review(jp, en):
    relative = "verification/registered_review.json"
    path = ROUTE_REVIEW / relative
    assert digest(path) == read(ROUTE_REVIEW / "checksums.json")[relative]
    row, = [r for r in read(path)["records"] if r["id"] == "COMMON_MESSAGE_637"]
    assert row["source_hex"] == jp.text.hex()
    assert row["english"] == " ".join(en.text.decode("ascii").split())
    return row, reference(path)


def native_town_names(cpu, call):
    source = read(panels.CATALOGUE)["town_table"]
    result = []
    root = call(0xCB178)
    for name in ("Athens", "Alexandria"):
        installed, = [row for row in source["installed"] if row["name"] == name]
        town = installed["town"]
        original, = [row for row in source["clean"] if row["town"] == town]
        pointer = call(installed["original_name_getter"] - 0x02000000, root + 4 + 108 * town)
        body = bytes.fromhex(installed["exact_hex"])
        assert bytes(cpu.mem_read(pointer, len(body))) == body == name.encode("ascii") + b"\0"
        result.append(dict(town=town, clean=original, native_installed=installed | {"string_address": pointer}))
    return result


def main():
    release = read(run.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(run.current.ROM) == release["candidate_sha256"]
    capture = FunctionType(panels.capture.__code__, vars(panels) | {"observed": SimpleNamespace(ROOT=run.ROOT.parent)})
    shots, calls, evidence = capture(run.ROOT.name, release)
    assert list(sorted({r["message_ID"] for r in calls})) == [0, 85, 637]
    assert max(shots) == 7800
    images = {k: panels.picture(v) for k, v in shots.items()}
    ctx = RegisteredRuntime(run.current.RELEASE, release["own_registered_startup"], captain=3)
    cpu, call, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    clean = NdsImage.open(CLEAN)
    source = panels.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    en = common_rows(ctx.common, ctx.arm)
    font = GameAsciiFont.from_arm9(ctx.arm)
    system = earlier.font_tools(ctx.image)[0]
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")

    records, figures = [], []
    for key, (frame, args, speaker, note) in CASES.items():
        a, b = [r for r in calls if r["message_ID"] == key]
        assert (a["PC"], b["PC"]) == (0x0205528C, 0x020534F4) and b == a | {"PC": 0x020534F4}
        assert 0 < frame - a["frame"] < 300
        jp, current = source[key], en[key]
        assert jp.text.count(b"%s") == current.text.count(b"%s") == len(args)
        old, contract = earlier.review_for(key, jp, current) if key == 85 else route_review(jp, current)
        assert old["review"] == dict.fromkeys(GATES, True)
        text = current.text % tuple(value.encode("ascii") for value in args)
        if speaker:
            assert panels.exact_body(font, [text.decode("ascii").strip()], images[frame])
            text_stats = panels.nameplate(font, speaker, images[frame])
        else:
            _, plane = earlier.system_plane(system, ctx.arm, kanji, text.rstrip(b" "), images[frame])
            text_stats = dict(complete_system_plane_sha256=plane)
        records.append(dict(id=old["id"], clean_Japanese=jp.text.decode("cp932"), english=old["english"],
            context=old["context"], source_meaning=old["source_meaning"], localization_note=note, decision="retention",
            source_reference=panels.text_reference(jp) | dict(exact_hex=jp.text.hex()),
            installed_reference=panels.text_reference(current) | dict(exact_hex=current.text.hex()),
            earlier_review=contract, review=old["review"], arguments=args, speaker=speaker, complete_glyphs=text_stats,
            command_request=a, capture=shots[frame]))
        figures.append((f"COMMON {key} / frame {frame}", images[frame]))

    names = native_town_names(cpu, call)
    labels = {5830: panels.find_mask(font, "Alexandria", images[5830], (55, 0, 133, 16)),
              7800: panels.find_mask(font, "Athens", images[7800], (45, 10, 115, 35))}
    auto_menu = panels.find_line(font, "Auto Move", images[6120], range(80, 129), range(260, 305), (8, 8, 8))
    before, after = images[3570], images[7800]
    for region in ((0, 0, 256, 192), (48, 330, 242, 366)):
        assert ImageChops.difference(before.crop(region), after.crop(region)).getbbox() is None
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_existing_save=True, records=records, evidence=evidence,
        observed_Auto_Move_choice=shots[6120], complete_Auto_Move_caption=auto_menu,
        actual_selected_port=shots[5830], returned_to_picker=shots[6990], returned_to_departure_menu=shots[7260],
        returned_to_Athens=shots[7800], town_names=names, town_header_glyphs=labels, unchanged_date_and_funds=True,
        sheets=sheets("athens_alexandria_auto_move", figures, (0, 272, 256, 380)),
        finished_auto_voyage_observed=False, offline_fleet_writer_evidence_is_separate=True,
        new_editorial_credit=0, ROM_changed=False))
    print("Verified the sailing estimate, the complete Alexandria refusal, and normal return to Athens.")


if __name__ == "__main__":
    main()
