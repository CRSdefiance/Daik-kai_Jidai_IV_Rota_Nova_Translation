"""Check the seven encounter pages and the subsequent port sighting."""

import json
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import replay_fleet_encounter_dialogue_20261119 as play
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold

base, build = play.base, play.build
PROOF = build.ROOT / "verified_encounters.json"
OBSERVATIONS = {
    "dolphins": ({8750: 2366, 8950: 2374, 10450: 2384}, 12500),
    "sirens": ({9627: 436, 9827: 2385}, 10227),
    "mermaid": ({9627: 448, 9827: 449}, 10027),
}


def snapshot(item):
    assert item["read_only_export"]
    raw = Path(item["path"]).read_bytes()
    assert len(raw) == 0x400000 and build.native.digest(raw) == item["sha256"]
    return raw


def page(image, raw):
    path = raw["path"]
    assert base.digest(path) == raw["PNG_sha256"]
    with Image.open(path) as photo:
        return photo.convert("RGB")


def record_frame(draw, sheet, panel, index, label):
    x, y = 520 * (index % 2), 208 * (index // 2)
    draw.text((x+4, y+3), label, fill="white")
    cut = panel.crop((0, 288, 256, 384)).resize((512, 192), Image.Resampling.NEAREST)
    sheet.paste(cut, (x+4, y+17))


def main():
    assert not PROOF.exists()
    stored = base.load(build.PROOF)
    sha = base.digest(build.ROM)
    assert sha == stored["candidate_sha256"]
    image = base.NdsImage.open(build.ROM)
    arm, kanji = image.read_file(build.ARM), image.read_file("/GRP/KANJI.FNT")
    raster, _, _ = build.workflow.font_tools(image)
    plain_pointer, display_pointer, owner = (unpack_from("<I", arm, offset)[0]-play.earlier.BASE
                                           for offset in (0x5444C, 0x54450, 0x552A0))
    rows = {r["message_ID"]: r for r in stored["records"]}
    evidence = {str(build.PROOF): base.digest(build.PROOF)}
    outcomes, sheets = [], []
    for event, (holds, return_frame) in OBSERVATIONS.items():
        terminal_path = play.ROOT/event/"terminal.json"
        terminal = base.load(terminal_path)
        assert terminal["candidate_sha256"] == sha
        for k in ("report", "commands"):
            assert base.digest(terminal[k]) == terminal[k+"_sha256"]
            evidence[terminal[k]] = terminal[k+"_sha256"]
        evidence[str(terminal_path)] = base.digest(terminal_path)
        report = base.load(terminal["report"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        donor = report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
        assert {k for k, v in report.items() if k.startswith("synthetic_") and v} == {"synthetic_condition_fixtures"}
        frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
        snapshots = {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
        journal = Path(terminal["report"]).with_name("navigation_command_journal.json")
        received = base.load(journal)["commands_received"]
        assert all(r["validation_passed"] for r in received)
        assert [r["command"] for r in received] == [json.loads(line) for line in Path(terminal["commands"]).read_text(encoding="utf-8").splitlines()]
        evidence[str(journal)] = base.digest(journal)
        fixture_receipts = []
        for command in received:
            request = command["command"].get("condition_fixture")
            if request:
                n = command["frame"]
                _, replayed = play.set_condition(arm, snapshot(snapshots[n]), request)
                fixture_receipts.append(replayed | {"frame": n})
                evidence[snapshots[n]["path"]] = snapshots[n]["sha256"]
        assert report["synthetic_condition_fixtures"] == fixture_receipts
        sheet = Image.new("RGB", (1040, 208*((len(holds)+2)//2)), "#263238")
        draw = ImageDraw.Draw(sheet)
        observed = []
        for i, (n, ident) in enumerate(holds.items()):
            raw = snapshot(snapshots[n])
            row = rows[ident]
            plain = owner + 0x2030 if event == "dolphins" else plain_pointer
            assert raw[plain:plain+256].split(b"\0", 1)[0].hex() == row["staged_hex"], (event, n, "stored")
            display = raw[display_pointer:display_pointer+256].split(b"\0", 1)[0]
            assert display.hex() == row["display_hex"], (event, n, "wrapped")
            pixels, glyphs = build.render_portrait(raster, arm, kanji, display)
            assert len(glyphs) == row["formatting_evidence"]["glyph_count"]
            assert build.native.digest(pixels) == row["formatting_evidence"]["ink_sha256"]
            photographed = page(image, frames[n])
            ink = native_hold(photographed, pixels)
            record_frame(draw, sheet, photographed, i, f"{event} COMMON {ident} at {n}")
            evidence[frames[n]["path"]] = frames[n]["PNG_sha256"]
            evidence[snapshots[n]["path"]] = snapshots[n]["sha256"]
            observed.append(dict(message_ID=ident, frame=n, complete_visible_ink_pixels=ink,
                exact_original_body=True, original_display_hex=display.hex(), capture=frames[n]))
        raw = snapshot(snapshots[return_frame])
        resumed = raw[display_pointer:display_pointer+256].split(b"\0", 1)[0]
        assert b" ".join(resumed.split()) == b"Admiral, we've spotted a port!"
        at = play.earlier.FIELD-play.earlier.BASE
        assert raw[at:at+4] == play.earlier.ORIGINAL
        pane = page(image, frames[return_frame])
        record_frame(draw, sheet, pane, len(holds), f"Next port sighting at {return_frame}")
        evidence[frames[return_frame]["path"]] = frames[return_frame]["PNG_sha256"]
        evidence[snapshots[return_frame]["path"]] = snapshots[return_frame]["sha256"]
        file = play.ROOT/event/f"{event}_replay.png"
        sheet.save(file)
        content = dict(path=str(file), sha256=base.digest(file))
        sheets.append(content)
        evidence[str(file)] = content["sha256"]
        outcomes.append(dict(event=event, observed=observed, following_port_sighting=frames[return_frame],
                             selector_restored=True, fixture_receipts=fixture_receipts))
    assert sum(len(x["observed"]) for x in outcomes) == 7
    base.save(PROOF, dict(candidate_sha256=sha, outcomes=outcomes, sheets=sheets, evidence=evidence,
        original_sequences_initialized=True, natural_random_selection_verified=False, hardware=False))
    print("Verified seven complete encounter pages, with a port sighting after each replay.")


if __name__ == "__main__":
    main()
