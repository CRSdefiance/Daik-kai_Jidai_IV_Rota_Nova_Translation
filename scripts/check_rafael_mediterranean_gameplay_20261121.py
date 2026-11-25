"""Match focused emulator captures to the final native dialogue masks."""
from types import SimpleNamespace

from scripts import replay_rafael_mediterranean_dialogue_20261121 as replay
from scripts import verify_rafael_mediterranean_dialogue_20261121 as display
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel


stage, base, native, town = replay.stage, replay.base, replay.native, panel.town
PROOF = replay.ROOT / "verified_gameplay_v2.json"
NAMES = {0: "Rafael Castor", 2: "Lil Argot", 4: "Janus Pasar", 5: "Claudio Manaus", 6: "Julio Erneco",
         8: "Arcadius Eudoxios", 9: "Camille Overijssel", 75: "Hans Letzel"}
REQUIRED = {"DK4_MES_B47_R0053", "DK4_MES_B48_R0071", "DK4_MES_B48_R0406",
            "DK4_MES_B49_R0020", "DK4_MES_B50_R0037"}


def main():
    assert not PROOF.exists()
    candidate = base.digest(stage.ROM)
    proof, draft = map(base.load, (display.PROOF, stage.review.OUTPUT))
    assert proof["candidate_sha256"] == candidate and base.digest(stage.ROOT / "clean_rebuilt.nds") == candidate
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    name_font = panel.GameAsciiFont.from_arm9(arm)
    rows = {row["id"]: row for row in draft["records"]}
    archive = native.IlnkContainer.parse(rom.read_file(replay.PATH))
    viewed, offline, cases, sheets, evidence = [], [], [], [], {}
    for number, (_, end) in replay.CASES.items():
        folder = replay.ROOT / f"B{number}"
        fixture_path, report_path = folder / "fixture.json", folder / "capture/capture_report.json"
        fixture, report = map(base.load, (fixture_path, report_path))
        assert fixture["candidate_sha256"] == candidate and fixture["preserved_block"] == number
        assert fixture["exact_candidate_inverse"] and fixture["source_controls_exact_under_constant_shift"]
        block = archive.blocks[number]
        assert native.digest(block[8:stage.logical_end(block)]) == fixture["preserved_command_bytes_sha256"]
        assert report["ROM_sha256"] == fixture["research_ROM_sha256"] == base.digest(fixture["research_ROM"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["frames"] == end and report["scripted_input_schedule"] == base.load(folder / "inputs.json")
        assert not report.get("battery_save_preloaded")
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
        evidence.update({str(p): base.digest(p) for p in (fixture_path, report_path, folder / "inputs.json")})
        captures = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
        pictures = {frame: town.read_frame(captures, frame)[1] for frame in captures}
        masks = {frame: bytes(value == town.INKS[0] for value in pic.crop((16, 296, 232, 360)).get_flattened_data())
                 for frame, pic in pictures.items()}
        matches = []
        for record in proof["records"]:
            if record["block"] != number or record["decision"] != "revision":
                continue
            row = rows[record["id"]]
            draw = paint(arm, font, bytes.fromhex(record["expanded_hex"]))
            page, = draw["pages"]
            raw = bytes.fromhex(page["native_plane_hex"])
            assert native.digest(raw) == record["plane_sha256"]
            expected = bytes(bool(value) for value in raw)
            for frame, pixels in sorted(masks.items()):
                if expected != pixels:
                    continue
                pic = pictures[frame]
                assert panel.mask_check(raw, 216, pic)
                speaker = NAMES[row["source_selector"]]
                panel.complete_mask(name_font, speaker, pic, 16, 277, town.INKS[1])
                matches.append(dict(id=row["id"], file_path=replay.PATH, block=number, frame=frame,
                                    speaker=speaker, observed=captures[frame]))
                break
            else:
                offline.append(row["id"])
        matches.sort(key=lambda row: row["frame"])
        assert matches, number
        viewed.extend(matches)
        final = captures[end - 1]
        cases.append(dict(block=number, observed_panels=len(matches), final_hold=final, initialized=True))
        samples = [(row["id"], pictures[row["frame"]]) for row in matches]
        samples.append((f"B{number} final hold", pictures[end - 1]))
        for start in range(0, len(samples), 6):
            target = folder / f"rafael_B{number}_gameplay_{start // 6 + 1}.png"
            town.sheet(samples[start:start + 6], target)
            sheets.append(dict(path=str(target), sha256=base.digest(target)))
    ids = {row["id"] for row in viewed}
    assert len(ids) == len(viewed) and len(offline) + len(viewed) == 40
    assert REQUIRED <= ids, (REQUIRED - ids, sorted(ids))
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=viewed, offline_only=offline,
        cases=cases, sheets=sheets, evidence=evidence | {str(display.PROOF): base.digest(display.PROOF)}))
    print(f"Observed {len(viewed)} revised panels across all four initialized exchanges. {len(offline)} are verified offline.")


if __name__ == "__main__":
    main()
