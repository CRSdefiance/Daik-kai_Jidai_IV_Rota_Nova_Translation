"""Score the focused Rafael excerpts against the final native glyph proofs."""

from types import SimpleNamespace

from scripts import check_rafael_mediterranean_gameplay_20261121 as template
from scripts import replay_rafael_north_sea_africa_20261121 as replay
from scripts import verify_rafael_north_sea_africa_20261121 as display


stage, base, native, town = replay.stage, replay.base, replay.native, template.town
ROOT, PROOF = replay.ROOT, replay.ROOT / "verified_gameplay.json"
REQUIRED = {"DK4_MES_B55_R0044", "DK4_MES_B58_R0045", "DK4_MES_B58_R0068"}


def main():
    assert not PROOF.exists()
    native_review, draft = map(base.load, (display.PROOF, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == native_review["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    name_font = template.panel.GameAsciiFont.from_arm9(arm)
    path = replay.prior.PATH
    archive = native.IlnkContainer.parse(rom.read_file(path))
    rows = {row["id"]: row for row in draft["records"]}
    holds, cases, sheets, evidence = [], [], [], {}
    first = stage.ROOT.with_name("staged_v1")
    for block, (_, end) in replay.CASES.items():
        reference_rom = first / stage.ROM.name if block == 55 else stage.ROM
        folder = (first / ROOT.name if block == 55 else ROOT) / f"B{block}"
        fixture_path, report_path = folder / "fixture.json", folder / "capture/capture_report.json"
        fixture, report = map(base.load, (fixture_path, report_path))
        assert fixture["candidate_sha256"] == base.digest(reference_rom) and fixture["preserved_block"] == block
        assert fixture["exact_candidate_inverse"] and fixture["source_controls_exact_under_constant_shift"]
        prior_rom = base.NdsImage.open(reference_rom)
        assert all(prior_rom.read_file(asset) == rom.read_file(asset) for asset in display.display.ASSETS)
        prior_bank = native.IlnkContainer.parse(prior_rom.read_file(path))
        payload = archive.blocks[block]
        assert prior_bank.blocks[block] == payload
        assert native.digest(payload[8:stage.logical_end(payload)]) == fixture["preserved_command_bytes_sha256"]
        assert report["ROM_sha256"] == fixture["research_ROM_sha256"] == base.digest(fixture["research_ROM"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["frames"] == end and report["scripted_input_schedule"] == base.load(folder / "inputs.json")
        assert not report.get("battery_save_preloaded")
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
        evidence.update({str(p): base.digest(p) for p in (fixture_path, report_path, folder / "inputs.json")})
        captures = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
        pictures = {frame: town.read_frame(captures, frame)[1] for frame in captures}
        matches = []
        for record in native_review["records"]:
            if record["block"] != block or record["decision"] != "revision":
                continue
            row = rows[record["id"]]
            layout = record["layouts"][0]
            assert layout["scope"] == "registered default"
            page, = paint(arm, font, bytes.fromhex(layout["expanded_hex"]))["pages"]
            raw = bytes.fromhex(page["native_plane_hex"])
            assert native.digest(raw) == layout["plane_sha256"]
            for frame, picture in sorted(pictures.items()):
                if not template.panel.mask_check(raw, 216, picture):
                    continue
                template.panel.complete_mask(name_font, row["speaker"], picture, 16, 277, town.INKS[1])
                matches.append(dict(id=row["id"], file_path=path, block=block, frame=frame,
                                    speaker=row["speaker"], observed=captures[frame]))
                break
        matches.sort(key=lambda row: row["frame"])
        assert matches, block
        holds.extend(matches)
        final = captures[end - 1]
        cases.append(dict(block=block, observed_panels=len(matches), final_hold=final,
                          focused_excerpt=True, earlier_fixture_block_byte_exact=block == 55))
        samples = [(r["id"], pictures[r["frame"]]) for r in matches]
        samples.append((f"B{block} final hold", pictures[end - 1]))
        for start in range(0, len(samples), 6):
            output = ROOT / f"rafael_B{block}_gameplay_{start // 6 + 1}.png"
            town.sheet(samples[start:start + 6], output)
            sheets.append(dict(path=str(output), sha256=base.digest(output)))
    observed = {r["id"] for r in holds}
    assert len(observed) == len(holds) and REQUIRED <= observed, (REQUIRED - observed, sorted(observed))
    offline = [r["id"] for r in draft["records"] if r["decision"] == "revision" and r["id"] not in observed]
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, offline_only=offline,
        cases=cases, sheets=sheets, evidence=evidence | {str(display.PROOF): base.digest(display.PROOF)} |
        {str(folder / f"B{block}" / f"Rafael_B{block}_RESEARCH_ONLY.nds"):
         base.digest(folder / f"B{block}" / f"Rafael_B{block}_RESEARCH_ONLY.nds")
         for block, folder in ((55, first / ROOT.name), (58, ROOT))}))
    print(f"Observed {len(holds)} revised panels across both initialized excerpts. {len(offline)} are verified offline.")


if __name__ == "__main__":
    main()
