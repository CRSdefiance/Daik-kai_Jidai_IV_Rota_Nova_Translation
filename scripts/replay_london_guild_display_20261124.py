"""Replay the ordinary Guild inputs on the staged ROM and compare the displays."""

import argparse
import sys

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import headless_desmume_v193 as harness
from scripts import stage_london_guild_display_20261124 as stage
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


BEFORE = stage.play.ROOT / "capture/capture_report.json"
REPLAY = stage.ROOT / "ordinary_replay"
AFTER = REPLAY / "capture_report.json"
OUT = stage.OUT.with_name("london_guild_paired_20261124.json")
CHANGED = {4800: (stage.PITCH_ID, None), 6400: (1073, 11000), 8400: (1073, 3000), 10800: (1084, None)}
RETAINS = {
    4000: (62, ("Need something?",), "A casual greeting from the Guildmaster leads into a short list of services."),
    5200: (3659, ("They say it's an ancient dagger", "with writing on it. I doubt anyone", "can still read it."),
           "Keep the report about the dagger and its inscription. The doubt that anyone can read it still sounds spoken."),
    5600: (1071, ("Which one would you like?",), "The short direct question introduces the item list, and works again when the player backs out."),
    8800: (1074, ("Thanks for your business!",), "The Guildmaster thanks Hodram after the purchase. The receipt still relies on the following balance and stock state."),
}


def replay():
    prior, staged = map(read, (BEFORE, stage.OUT))
    assert digest(stage.ROM) == staged["candidate"]["sha256"]
    assert prior["ROM_sha256"] == staged["predecessor"]["sha256"]
    donor = prior["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    assert not REPLAY.exists()
    inputs = stage.ROOT / "inputs.json"
    write(inputs, prior["scripted_input_schedule"])
    captures = stage.panels.shots(prior, "_navigation.png")
    argv = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(stage.ROM), "--out", str(REPLAY), "--frames", str(prior["frames"]),
                    "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                    "--battery-save", donor["source"], "--touchscreen", "--capture-at", *map(str, captures)]
        harness.main()
    finally:
        sys.argv = argv


def verify():
    panels = stage.panels
    before, after, preflight = map(read, (BEFORE, AFTER, stage.OUT))
    assert before["ROM_sha256"] == preflight["predecessor"]["sha256"]
    assert after["ROM_sha256"] == preflight["candidate"]["sha256"] == digest(stage.ROM)
    assert before["frames"] == after["frames"] and before["scripted_input_schedule"] == after["scripted_input_schedule"]
    for run in (before, after):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(v for k, v in run.items() if k.startswith("synthetic_"))
        donor = run["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert before["battery_save_preloaded"]["source_sha256"] == after["battery_save_preloaded"]["source_sha256"]
    assert before["core_DLL_sha256"] == after["core_DLL_sha256"] and before["core_options"] == after["core_options"]

    old, new = panels.shots(before, "_navigation.png"), panels.shots(after, "_cold_boot.png")
    assert old.keys() <= new.keys()
    target = NdsImage.open(stage.ROM)
    arm, common = (target.read_file(path) for path in (stage.ARM, stage.COMMON))
    assert preflight["target_ARM9_sha256"] == stage.sha256(arm).hexdigest()
    assert preflight["target_COMMON_sha256"] == stage.sha256(common).hexdigest()
    font = GameAsciiFont.from_arm9(arm)
    changed, unchanged, figures = [], [], []
    screens = {frame: panels.picture(new[frame]) for frame in old}
    for frame, capture in old.items():
        if frame not in CHANGED:
            assert capture["framebuffer_sha256"] == new[frame]["framebuffer_sha256"], frame
            unchanged.append(frame)
            continue
        key, amount = CHANGED[frame]
        if key == stage.PITCH_ID:
            record = preflight["pitch_after"]
        elif key == 1084:
            record = preflight["empty_sale_after"]
        else:
            record = preflight["quote_cases"][str(amount)]
        previous, installed = panels.picture(capture), screens[frame]
        bbox = ImageChops.difference(previous, installed).getbbox()
        assert bbox and 16 <= bbox[0] < bbox[2] <= 245 and 296 <= bbox[1] < bbox[3] < 360, (frame, bbox)
        full_mask = panels.exact_body(font, record["lines"], installed)
        nameplate = panels.nameplate(font, "Guildmaster", installed)
        changed.append(dict(frame=frame, message_ID=key if key != stage.PITCH_ID else None, amount=amount,
                            body_mask_pixels=full_mask, lines=record["lines"], nameplate=nameplate, changed_box=bbox,
                            previous=capture, installed=new[frame]))
        figures.extend(((f"{frame} / Before", previous), (f"{frame} / After", installed)))
    assert len(changed) == 4

    source = NdsImage.open(stage.CLEAN)
    clean = stage.common_message_entries(source.read_file(stage.COMMON), source.read_file(stage.ARM))
    current = stage.native.yard.common_rows(common, arm)
    trace_path = stage.play.ROOT / "trace/requests.json"
    trace = read(trace_path)
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    retentions = []
    for frame, (key, lines, reason) in RETAINS.items():
        requests = [r for r in trace["source_requests"] if r["message_ID"] == key and 0 < frame - r["frame"] < 400]
        getter, copier = requests
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert current[key].text.decode("ascii").split() == " ".join(lines).split()
        retentions.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=stage.COMMON, speaker="Guildmaster", context=stage.CONTEXT,
            english=" ".join(lines), clean_Japanese=clean[key].text.decode("cp932"), source_reference=stage.exact_row(clean[key]),
            current_reference=stage.exact_row(current[key]), staged_reference=stage.exact_row(current[key]), decision="retention",
            source_meaning=reason, localization_note=reason, review=dict.fromkeys(stage.GATES, True),
            complete_body_ink=panels.exact_body(font, lines, screens[frame]),
            nameplate=panels.nameplate(font, "Guildmaster", screens[frame]), requests=requests, capture=new[frame]))

    funds = [dict(frame=frame, **panels.find_mask(font, amount, screens[frame], (52, 344, 137, 367)))
             for frame, amount in ((4400, "40659"), (10000, "37659"), (11600, "37659"))]
    return_to_town = panels.find_mask(font, "London", screens[11600], (10, 13, 123, 31))
    sheets = panels.sheets_for("london_guild_paired", figures)
    write(OUT, dict(candidate_sha256=after["ROM_sha256"], predecessor_sha256=before["ROM_sha256"], ordinary_gameplay=True,
                    revised=changed, unchanged_frames=unchanged, retentions=retentions, balances=funds,
                    return_to_town=return_to_town, sheets=sheets,
                    exact_source_requests=trace["source_requests"], evidence=list(map(reference, (BEFORE, AFTER, stage.OUT, trace_path))),
                    unvisited="A successful sale or insufficient-funds response was not available in the observed sequence.",
                    new_editorial_credit=0, registered=False))
    print(f"Verified four revised Guild holds and {len(unchanged)} identical surrounding frames in ordinary play.")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--replay", action="store_true")
    args = cli.parse_args()
    if args.replay:
        replay()
    else:
        verify()
