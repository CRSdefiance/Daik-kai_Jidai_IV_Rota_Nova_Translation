"""Verify the edited Lisbon scene in the ordinary unmodified event flow."""
from types import SimpleNamespace

from PIL import Image

from scripts import replay_lisbon_fragrance_wraps_20261121 as run
from scripts import verify_lisbon_fragrance_wraps_20261121 as offline


stage, original, base = run.stage, run.original, run.base
native, town = stage.native, original.town
PROOF = run.ROOT / "verified_lisbon.json"


def main():
    assert not PROOF.exists()
    staged, verified, report, before = map(base.load, (stage.PROOF, offline.PROOF, run.REPORT, original.OUTPUT))
    assert report["ROM_sha256"] == staged["candidate_sha256"] == verified["candidate_sha256"] == base.digest(stage.ROM)
    assert staged["predecessor_sha256"] == before["candidate_sha256"] and staged["whole_parent_inverse"]
    case, = [r for r in before["town_runs"] if r["city"] == "lisbon"]
    source = original.runs.ROOT / "lisbon/capture/capture_report.json"
    assert base.digest(source) == case["evidence"][str(source)]
    prior = base.load(source)
    assert report["scripted_input_schedule"] == prior["scripted_input_schedule"] == base.load(run.PLAN)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    for k in ("source", "source_sha256", "copied_byte_exact_before_cold_boot"):
        assert report["battery_save_preloaded"][k] == prior["battery_save_preloaded"][k]
    assert base.digest(report["battery_save_preloaded"]["source"]) == prior["battery_save_preloaded"]["source_sha256"]
    image = base.NdsImage.open(stage.ROM)
    arm, font = (image.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT"))
    context = SimpleNamespace(image=image, arm=arm)
    painter, system = town.clipped_renderer(context), town.current_fe_painter(context)
    group, = staged["groups"]
    assert (group["file_path"], group["block"]) == ("/data/SC1.DK4", 184)
    active = native.IlnkContainer.parse(image.read_file(group["file_path"])).blocks[group["block"]]
    assert native.digest(active) == group["after"]
    observed = original.event_completion(arm, report, image.read_file("/data/EV1.DK4"),
        case["event"]["original_event"], original.ROUTES["lisbon"])
    previous_hold = {r["id"]: r for r in case["records"]}
    checks = {r["id"]: r for r in verified["records"]}
    frames = {r["frame"]: r for r in report["frames_captured"]}
    names = original.GameAsciiFont.from_arm9(arm)
    proofs, examples = [], []
    for c in group["commands"]:
        if not c["record_ids"]:
            continue
        name, = c["record_ids"]
        raw = bytes.fromhex(c["stored"])
        at = c["stored_offset"]
        assert active[at:at+len(raw)] == raw
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
        old = previous_hold[name]
        shot, picture = town.read_frame(frames, old["observed"]["frame"])
        assert original.mask_check(plane, width, picture)
        revised = c["stored"] != c["current"]
        if revised:
            assert checks[name]["native_page_hashes"] == [native.digest(plane)]
            assert base.digest(old["observed"]["path"]) == old["observed"]["PNG_sha256"]
            with Image.open(old["observed"]["path"]) as old_image:
                examples.extend([(name + " before", old_image.convert("RGB")), (name + " revised", picture)])
        else:
            assert old["complete_native_body_sha256"] == native.digest(plane)
        if raw[5] in (166, 167):
            original.complete_mask(names, "Lady", picture, 16, 277, town.INKS[1])
        proofs.append(dict(id=name, route=1, current_native_mask_sha256=native.digest(plane),
            snapshot=shot, observed_on_changed_ROM=True, revised=revised))
    assert len(proofs) == 11 and sum(r["revised"] for r in proofs) == 2
    for key in ("opened_existing_save", "after_rest", "Square_after_notice"):
        old = case[key]
        shot, _ = town.read_frame(frames, old["frame"])
        assert old["framebuffer_sha256"] == shot["framebuffer_sha256"], key
    picture_path = run.ROOT / "lisbon_before_after_gameplay.png"
    town.sheet(examples, picture_path)
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], holds=proofs, event=observed,
        natural_activation=True, identical_saved_game_and_inputs=True, exact_native_glyph_matches=True,
        hardware_verified=False, two_revised_panels=True, original_notice_dismissal_and_Square_return=True,
        sheets=[dict(path=str(picture_path), sha256=base.digest(picture_path))],
        evidence={str(p):base.digest(p) for p in (run.REPORT, run.PLAN, offline.PROOF, original.OUTPUT)}))
    print("All 11 staged Lisbon panels match the original event flow, including both revised lines.")


if __name__ == "__main__":
    main()

