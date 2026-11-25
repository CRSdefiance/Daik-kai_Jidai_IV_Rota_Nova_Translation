"""Verify the exact stored dialogue in the focused Hodram and Lil replays."""
from types import SimpleNamespace

from scripts import replay_fernando_parallel_routes_20261121 as replay
from scripts import verify_fernando_parallel_routes_20261121 as display
from scripts import verify_parallel_ship_lessons_gameplay_20261121 as bodies
from scripts.verify_rafael_refit_sailing_gameplay_20261121 import caption_bounds


stage, base, native = replay.stage, replay.base, replay.native
panel, town = bodies.panel, bodies.town
PROOF = replay.ROOT / "verified_gameplay.json"
HEADERS = {1: "Hodram Bergstrom", 9: "Camille Overijssel", 20: "Fernando Dias",
           92: "Barkeep", 95: "Patron", 164: "Man", 165: "Woman"}


def main():
    assert not PROOF.exists()
    draft, checked = map(base.load, (stage.review.OUTPUT, display.PROOF))
    candidate = base.digest(stage.ROM)
    assert checked["candidate_sha256"] == candidate == base.digest(stage.ROOT / "clean_rebuilt.nds")
    image = base.NdsImage.open(stage.ROM)
    arm, font = (image.read_file(asset) for asset in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    header = panel.GameAsciiFont.from_arm9(arm)
    rows = {(r["route"], r["id"]): r for r in draft["records"]}
    native_rows = {(r["route"], r["id"]): r for r in checked["records"]}
    evidence = {str(display.PROOF): base.digest(display.PROOF)}
    holds, kept, menus, sheets = [], [], [], []
    for route, case in replay.CASES.items():
        path = f"/data/SC{route}.DK4"
        folder = replay.ROOT / f"route{route}"
        fixture_path, inputs, report_path = [folder / n for n in ("fixture.json", "inputs.json", "capture/capture_report.json")]
        fixture, report = map(base.load, (fixture_path, report_path))
        assert fixture["candidate_sha256"] == candidate and fixture["route"] == route
        assert fixture["exact_candidate_inverse"] and not fixture["natural_activation"]
        assert report["ROM_sha256"] == fixture["fixture_sha256"] == base.digest(fixture["fixture"])
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not report.get("battery_save_preloaded") and not any(v for k, v in report.items() if k.startswith("synthetic_"))
        assert report["frames"] == case["end"] and report["scripted_input_schedule"] == base.load(inputs)
        for file in (fixture_path, inputs, report_path, fixture["fixture"]):
            evidence[str(file)] = base.digest(file)
        block = native.IlnkContainer.parse(image.read_file(path)).blocks[case["block"]]
        frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
        shots = {frame: town.read_frame(frames, frame)[1] for frame in sorted(frames)}
        foreground = {frame: bodies.foreground(shot) for frame, shot in shots.items()}
        previews = []
        last = 3899
        for span in fixture["copied_native_commands"]:
            ident = span["ids"][0]
            data = native_rows[route, ident]
            raw = bytes.fromhex(data["stored_command_hex"])
            pos = span["original_offset"]
            assert data["block"] == span["block"] and block[pos:pos+len(raw)] == raw and native.digest(raw) == span["command_sha256"]
            if data.get("native_caption"):
                labels = [rows[route, name]["english"] for name in span["ids"]]
                for frame, shot in shots.items():
                    if frame <= last or shot.getpixel((112, 270)) != (0, 165, 172):
                        continue
                    bounds = [caption_bounds(header, shot, label, top) for label, top in zip(labels, (267, 287), strict=True)]
                    if all(bounds):
                        menus.append(dict(route=route, ids=span["ids"], labels=labels, bounds=bounds,
                                          selected=0, observed=frames[frame]))
                        previews.append(("Play / Pass", shot))
                        last = frame
                        break
                else:
                    raise AssertionError((route, "no full choice menu"))
                continue
            changed = data["decision"] == "revision" and ident != display.BYTE_EXACT
            layout = data.get("layouts", [None])[0]
            if layout:
                text = bytes.fromhex(layout["expanded_hex"])
            else:
                text = raw[6:raw.index(0, 6)]
                assert not stage.review.TOKEN.findall(text.decode("ascii"))
            page, = paint(arm, font, text)["pages"]
            mask = bytes.fromhex(page["native_plane_hex"])
            if layout:
                assert [native.digest(mask)] == layout["pages"]
            expected = bytes(bool(value) for value in mask)
            for frame, actual in foreground.items():
                if frame <= last or actual != expected:
                    continue
                shot = shots[frame]
                assert panel.mask_check(mask, 216, shot)
                speaker = HEADERS[rows[route, ident]["source_selector"]]
                panel.complete_mask(header, speaker, shot, 16, 277, town.INKS[1])
                item = dict(id=ident, route=route, file_path=path, block=case["block"], frame=frame,
                            speaker=speaker, observed=frames[frame])
                (holds if changed else kept).append(item)
                previews.append((ident, shot))
                last = frame
                break
            else:
                raise AssertionError((route, ident, "no complete ordered live page"))
        for start in range(0, len(previews), 6):
            file = folder / f"fernando_SC{route}_actual_{start//6+1}.png"
            town.sheet(previews[start:start+6], file)
            sheets.append(dict(path=str(file), sha256=base.digest(file)))
    assert len(holds) == 30 and len(kept) == 4 and len(menus) == 1
    assert {r["speaker"] for r in holds}.issuperset({"Man", "Woman", "Camille Overijssel", "Fernando Dias"})
    assert menus[0]["route"] == 1 and set(menus[0]["labels"]) == {"Play", "Pass"}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, unchanged_sample_panels=kept,
        captions=menus, sheets=sheets, evidence=evidence))
    print("Matched 30 revised pages, four retained speeches and Hodram's complete choice menu.")


if __name__ == "__main__":
    main()
