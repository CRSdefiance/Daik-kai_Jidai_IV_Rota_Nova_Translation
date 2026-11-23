"""Check the revised lines and both returns to the Square in ordinary play."""
from types import SimpleNamespace

from PIL import Image

from scripts import replay_athens_london_trends_20261121 as run
from scripts import verify_athens_london_trends_display_20261121 as offline


stage, original, base = run.stage, run.original, run.base
native, town, existing = stage.native, original.town, original.previous
PROOF = run.ROOT / "verified_trends.json"


def main():
    assert not PROOF.exists()
    stored, verified = map(base.load, (stage.PROOF, offline.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == verified["candidate_sha256"]
    assert stored["whole_parent_inverse"]
    target = base.NdsImage.open(stage.ROM)
    arm, font, events, archive = (target.read_file(path) for path in
        (native.ARM, "/GRP/KANJI.FNT", "/data/EV1.DK4", "/data/SC1.DK4"))
    context = SimpleNamespace(image=target, arm=arm)
    painter, system = town.clipped_renderer(context), town.current_fe_painter(context)
    names = existing.GameAsciiFont.from_arm9(arm)
    blocks = native.IlnkContainer.parse(archive).blocks
    event_map = {row["town"]: row for row in base.load(town.events.OUTPUT)["routes"][1]["entries"]}
    checks = {(row["file_path"], row["id"]): row for row in verified["records"]}
    observed, events_seen, sheets = [], {}, []
    evidence = {str(path):base.digest(path) for path in (offline.PROOF, original.OUTPUT, town.events.OUTPUT)}
    for city, plan in original.CASES.items():
        inputs, report_path = run.replay_paths(city)
        case, prior = run.source_run(city, stored)
        report = base.load(report_path)
        assert report["ROM_sha256"] == candidate and report["frames"] == plan["returned"]
        assert report["scripted_input_schedule"] == prior["scripted_input_schedule"] == base.load(inputs)
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
        donor = report["battery_save_preloaded"]
        for key in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
            assert donor[key] == prior["battery_save_preloaded"][key]
        assert base.digest(donor["source"]) == donor["source_sha256"]
        event = event_map[plan["town"]]
        assert event["script_block"] == plan["block"]
        events_seen[city] = existing.event_completion(arm, report, events, event, plan)
        path = "/data/SC1.DK4"
        group, = (g for g in stored["groups"] if g["file_path"] == path and g["block"] == plan["block"])
        block = blocks[plan["block"]]
        assert native.digest(block) == group["after"]
        before = {row["id"]: row for row in case["panels"]}
        frames = {row["frame"]: row for row in report["frames_captured"]}
        examples = []
        for command in group["commands"]:
            if not command["record_ids"]:
                continue
            ident, = command["record_ids"]
            old = before.pop(ident)
            raw, at = bytes.fromhex(command["stored"]), command["stored_offset"]
            assert block[at:at+len(raw)] == raw
            body = offline.prior.bytes_for(raw)
            if raw[5] == 254:
                surface = system(body)
                plane, width = surface["physical"], 228
            else:
                surface = painter(arm, font, body)
                page, = surface["pages"]
                assert page["native_independent_plane_equal"]
                plane, width = bytes.fromhex(page["native_plane_hex"]), 216
            assert surface["complete_consumed_bytes"] == len(body)
            shot, picture = town.read_frame(frames, old["observed"]["frame"])
            assert existing.mask_check(plane, width, picture), (city, ident)
            revised = command["stored"] != command["current"]
            if revised:
                assert checks[path,ident]["native_page_hashes"] == [native.digest(plane)]
                assert base.digest(old["observed"]["path"]) == old["observed"]["PNG_sha256"]
                with Image.open(old["observed"]["path"]) as old_image:
                    examples.extend([(ident + " before", old_image.convert("RGB")), (ident + " revised", picture)])
            else:
                assert old["observed_native_plane_sha256"] == native.digest(plane)
            if raw[5] != 254:
                assert raw[5] in (166,167,168)
                existing.complete_mask(names, "Lady", picture, 16, 277, town.INKS[1])
            observed.append(dict(city=city, file_path=path, id=ident, route=1, snapshot=shot, revised=revised,
                                 current_native_mask_sha256=native.digest(plane)))
        assert not before and len(examples) in (4, 8)
        for key, old in case["calendar_controls"].items():
            shot, _ = town.read_frame(frames, old["frame"])
            assert old["framebuffer_sha256"] == shot["framebuffer_sha256"], (city, key)
        for start in range(0, len(examples), 6):
            picture_path = run.ROOT / f"{city}_before_after_{start//6+1}.png"
            town.sheet(examples[start:start+6], picture_path)
            sheets.append(dict(path=str(picture_path), sha256=base.digest(picture_path)))
        evidence.update({str(p):base.digest(p) for p in (inputs, report_path)})
    assert len(observed) == 18 and sum(r["revised"] for r in observed) == 6 and len(sheets) == 3
    base.save(PROOF, dict(candidate_sha256=candidate, holds=observed, exact_native_glyph_matches=True,
        natural_activation=True, original_notice_dismissal_and_Square_return=True, hardware_verified=False,
        original_event_completion=events_seen, identical_saved_games_and_inputs=True, sheets=sheets, evidence=evidence))
    print("All 18 Athens and London panels match, including six revised lines and both Square returns.")


if __name__ == "__main__":
    main()
