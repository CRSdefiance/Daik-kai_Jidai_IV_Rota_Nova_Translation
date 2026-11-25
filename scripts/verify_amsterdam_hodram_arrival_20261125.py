"""Check both of Hodram's complete ordinary Amsterdam story exchanges."""

from argparse import ArgumentParser
from pathlib import Path
from types import SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts import observe_amsterdam_london_gift_20261125 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


SOURCE_PACKET = Path("releases/all_routes_editorial_20261122_hodram_B24_B53_candidate/verification/registered_review.json")
OUT = panels.OUT.with_name("amsterdam_hodram_arrival_current_20261125.json")
PATH = "/data/SC1.DK4"
HOLD_FRAMES = (11600, 11900, *range(12600, 21001, 350))
WRAP_FINDINGS = {
    29: ("You can't", "barge in"),
    49: ("Now", "everyone from soldiers to explorers"),
    53: ("Then they strut", "around like they own the place."),
}
APOLOGY_PACKET = Path("releases/all_routes_editorial_20261123_hodram_midroute_followups_candidate/verification/registered_review.json")
APOLOGY_OUT = panels.OUT.with_name("amsterdam_camille_apology_current_20261125.json")
APOLOGY_FINDINGS = {
    89: ("Many countries around the", "Mediterranean live by sea trade. We"),
}


def capture_ref(frame):
    path = play.ROOT / "capture" / f"frame_{frame:06d}_navigation.png"
    return dict(frame=frame, path=str(path), PNG_sha256=digest(path))


def main(block):
    packet, output, holds, findings = {
        44: (SOURCE_PACKET, OUT, HOLD_FRAMES, WRAP_FINDINGS),
        137: (APOLOGY_PACKET, APOLOGY_OUT, tuple(range(26750, 33751, 350)), APOLOGY_FINDINGS),
    }[block]
    release = read(play.current.RELEASE)
    assert release["registry_sha256"] == digest(REGISTRY) and release["candidate_sha256"] == digest(play.current.ROM)
    assert release["clean_input_sha256"] == digest(CLEAN)
    relative = packet.relative_to(packet.parent.parent).as_posix()
    assert digest(packet) == read(packet.parent.parent / "checksums.json")[relative]
    original, current = map(NdsImage.open, (CLEAN, play.current.ROM))
    clean_archive, installed_archive = (rom.read_file(PATH) for rom in (original, current))
    clean, installed = (IlnkContainer.parse(data).blocks[block] for data in (clean_archive, installed_archive))
    arm = current.read_file(play.current.ARM)
    kanji = current.read_file("/GRP/KANJI.FNT")
    context = SimpleNamespace(image=current, arm=arm)
    font = GameAsciiFont.from_arm9(arm)
    paint, fe = panels.town.clipped_renderer(context), panels.town.current_fe_painter(context)
    earlier = [r for r in read(packet)["records"] if r.get("file_path") == PATH and r.get("block") == block]
    assert len(earlier) == len(holds)
    decisions, figures = [], []
    for row, frame in zip(earlier, holds, strict=True):
        source, stored = row["source_reference"], row["registered_reference"]
        installed_cmd = bytes.fromhex(stored["exact_command_hex"])
        cursor = installed.find(installed_cmd)
        assert cursor >= 0 and installed.find(installed_cmd, cursor + 1) < 0
        source_body = bytes.fromhex(source["exact_body_hex"])
        offset = source["command_offset"]
        assert sha256(clean).hexdigest() == source["block_sha256"]
        clean_cmd = clean[offset:offset + 6 + len(source_body) + 1]
        assert clean_cmd[:6] == installed_cmd[:6] and clean_cmd[6:] == source_body + b"\0"
        raw = panels.bytes_for(installed_cmd)
        assert raw.isascii()
        number = int(row["id"].rsplit("_R", 1)[1])
        substitutions = {}
        paint_raw = raw
        if block == 44 and number == 111:
            assert raw.startswith(b"FI,") and source_body.startswith(b"FI")
            substitutions["FI"] = "Hodram"
            paint_raw = b"Hodram" + raw[2:]
        shot = capture_ref(frame)
        screen = panels.picture(shot)
        if installed_cmd[5] == 0xFE:
            display = fe(paint_raw)
            plane, width = display["physical"], 228
            nameplate = None
        else:
            display = paint(arm, kanji, paint_raw)
            page, = display["pages"]
            assert page["native_independent_plane_equal"]
            plane, width = bytes.fromhex(page["native_plane_hex"]), 216
            nameplate = panels.nameplate(font, row["speaker"], screen)
        assert display["complete_consumed_bytes"] == len(paint_raw)
        assert panels.mask_check(plane, width, screen), (row["id"], frame)
        assert set(row["review"]) == set(GATES) and all(row["review"].values())
        reference_now = dict(file_path=PATH, block=block, archive_sha256=sha256(installed_archive).hexdigest(),
            block_sha256=sha256(installed).hexdigest(), command_offset=cursor, exact_command_hex=installed_cmd.hex())
        finding = findings.get(number)
        if finding:
            assert finding[0].encode("ascii") in paint_raw and finding[1].encode("ascii") in paint_raw
        decisions.append(dict(id=row["id"], file_path=PATH, block=block, speaker=row["speaker"], context=row["context"],
            clean_Japanese=row["Japanese"], source_meaning=row["source_meaning"], english=" ".join(raw.decode("ascii").split()),
            localization_note=row["localization_note"], source_reference=source | dict(exact_command_hex=clean_cmd.hex()),
            current_reference=reference_now, installed_reference=reference_now, capture=shot,
            complete_nameplate=nameplate, display_plane_sha256=sha256(plane).hexdigest(), substitutions=substitutions,
            line_break_finding=finding, decision="wrap revision needed" if finding else "retention",
            review=row["review"] | {"formatting": finding is None}))
        figures.append((row["id"], screen))
    assert sum(row["decision"] == "wrap revision needed" for row in decisions) == len(findings)
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"],
        prior_contextual_review=reference(packet), records=decisions, new_editorial_credit=0)
    validate_natural_dialogue_batch(batch | {"records": [row for row in decisions if row["decision"] == "retention"]})
    sheets = panels.sheets_for(f"amsterdam_hodram_B{block}_20261125", figures)
    transitions = {"unvoiced_scene_transition": capture_ref(12250)} if block == 44 else {}
    write(output, batch | dict(sheets=sheets, held_panels=len(decisions), **transitions,
        gameplay_coverage="ordinary story panels; bind terminal capture before registration"))
    print(f"All {len(decisions)} Amsterdam B{block} story panels matched the current native renderer.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("block", choices=(44, 137), type=int)
    main(parser.parse_args().block)
