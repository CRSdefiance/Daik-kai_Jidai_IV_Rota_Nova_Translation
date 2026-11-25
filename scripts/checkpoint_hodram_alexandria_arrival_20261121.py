"""Bind the naturally selected arrival story and ship lesson to exact frames."""
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_alexandria_square_20261121 as run
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel
from scripts.review_company_name_dialogue_20261121 import TOKEN


active, base, native, town = run.active, panel.base, panel.native, panel.town
ROOT = Path("work/hodram_alexandria_arrival_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "ordinary_arrival_coverage.json"
REPORT = run.ROOT / "capture/capture_report.json"
NAME_TOKENS = {"FI": b"Hodram", "FA": b"Bergstrom"}
FINDINGS = {
    "DK4_MES_B51_R0006": "The live line separates southern from Mediterranean.",
    "DK4_MES_B51_R0014": "The live line separates I'm telling from the rest of the warning.",
    "DK4_MES_B167_R0122": "The tutorial breaks signing contracts across rows.",
    "DK4_MES_B167_R0138": "Even when breaks after Even on the first row.",
    "DK4_MES_B167_R0163": "The first page ends after only two rows on a dependent clause.",
}


def main():
    assert not OUTPUT.exists()
    candidate = base.digest(active.ROM)
    packet, report, donor = map(base.load, (SOURCE, REPORT, run.ROOT / "source_save.json"))
    assert report["ROM_sha256"] == candidate == packet["candidate_sha256"] and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    battery = report["battery_save_preloaded"]
    assert battery["copied_byte_exact_before_cold_boot"]
    assert battery["source_sha256"] == donor["sha256"] == base.digest(donor["donor"])
    assert battery["source"] == donor["donor"]
    rom = base.NdsImage.open(active.ROM)
    arm, font = (rom.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    ctx = SimpleNamespace(image=rom, arm=arm)
    paint, fe = town.clipped_renderer(ctx), town.current_fe_painter(ctx)
    names = panel.GameAsciiFont.from_arm9(arm)
    frames = {row["frame"]: row for row in report["frames_captured"]
              if row["path"].endswith("_navigation.png") and 11620 <= row["frame"] <= 28120}
    pictures = {frame: town.read_frame(frames, frame)[1] for frame in frames}
    masks = {(width, frame): bytes(pixel == town.INKS[0] for pixel in image.crop((16, 296, 16 + width, 360)).get_flattened_data())
             for width in (216, 228) for frame, image in pictures.items()}
    clean = base.NdsImage.open(native.CLEAN)
    banks = [native.IlnkContainer.parse(image.read_file("/data/SC1.DK4")).blocks for image in (clean, rom)]
    matches, offline, captions = [], [], []
    for group in packet["groups"]:
        b = group["block"]
        refs = {r["source_reference"]["offset"]: r for r in base.load(Path(
            "translations/hodram_B51_contextual_final_review_v1.json" if b == 51 else
            "translations/hodram_B151_B170_contextual_final_review_v1.json"))["records"] if r["block"] == b}
        assert [native.digest(data[b]) for data in banks] == [group[f"{side}_block_sha256"] for side in ("source", "current")]
        for row in group["records"]:
            selector = row["selector"]
            prefix = bytes([selector]) if selector is not None else b""
            for bank, side in zip(banks, ("source", "current"), strict=True):
                value, at = prefix + bytes.fromhex(row[f"{side}_body_hex"]), row[f"{side}_offset"]
                assert bank[b][at:at+len(value)] == value
            prior = refs.pop(row["source_offset"])
            ident = prior["id"]
            if selector is None:
                captions.append(dict(id=ident, English=row["current_English"], source_offset=row["source_offset"],
                                     current_offset=row["current_offset"], current_hex=row["current_body_hex"],
                                     frame=frames[20640]))
                continue
            body = TOKEN.sub(lambda match: NAME_TOKENS[match[0]].decode("ascii"),
                             bytes.fromhex(row["current_body_hex"]).decode("ascii")).encode("ascii")
            if selector == 254:
                render, width = [fe(body)["physical"]], 228
            else:
                render, width = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]], 216
            visible = []
            first, last = (11620, 13440) if b == 51 else (13440, 28120)
            for plane in render:
                expected = bytes(bool(p) for p in plane)
                for frame, picture in sorted(pictures.items()):
                    if not (first <= frame < last) or masks[width, frame] != expected:
                        continue
                    if selector != 254:
                        try:
                            panel.complete_mask(names, prior["speaker"], picture, 16, 277, town.INKS[1])
                        except ValueError:
                            continue
                    assert panel.mask_check(plane, width, picture)
                    visible.append(frames[frame])
                    break
            evidence = dict(id=ident, file_path=group["file_path"], block=b, source_offset=row["source_offset"],
                            source_hex=(prefix + bytes.fromhex(row["source_body_hex"])).hex(),
                            current_offset=row["current_offset"], current_hex=(prefix + bytes.fromhex(row["current_body_hex"])).hex(),
                            actual_complete_pages=visible, stored_pages=len(render))
            if len(visible) == len(render):
                matches.append(evidence | {"finding": FINDINGS.get(ident)})
            else:
                offline.append(evidence)
        assert not refs
    assert [row["English"] for row in captions] == ["Listen.", "Skip"]
    assert set(FINDINGS) <= {row["id"] for row in matches}
    assert len(matches) + len(offline) + len(captions) == 48
    base.save(OUTPUT, dict(candidate_sha256=candidate, ordinary_sailing_and_story_activation=True,
        source_packet_sha256=base.digest(SOURCE), report_sha256=base.digest(REPORT), selected="Listen.",
        full_body_matches=matches, partially_sampled_or_unvisited=offline, displayed_captions=captions,
        closing_transition=frames[28120], hardware_verified=False, new_editorial_credit=0))
    print(f"Bound {len(matches)} complete speeches, both captions and {len(FINDINGS)} concrete wrap leads.")


if __name__ == "__main__":
    main()
