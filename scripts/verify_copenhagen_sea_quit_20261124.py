"""Bind the at-sea System Quit branches to the original session fields."""

import json
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_copenhagen_sea_quit_20261124 as play
from scripts import reconcile_exhibition_quit_scene_gate_20261124 as gate
from scripts import verify_riga_trade_deck_20261124 as earlier
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_crew_policy_matrix_v657 import find_complete


OUT = gate.OUT.with_name("copenhagen_sea_quit_current_20261124.json")
panels = earlier.panels
HOLDS, END = (5600, 6800), 7400


def capture(release):
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    commands = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert commands[0] == play.OPENING and commands[-2]["until"] == max(frames) == END
    past = read(play.PRIOR)["replay"]
    assert reference(past["path"]) == past
    old = read(past["path"])
    start = panels.shots(old, "_cold_boot.png")[play.FIRST_PAUSE]
    assert start["framebuffer_sha256"] == frames[play.FIRST_PAUSE]["framebuffer_sha256"]
    assert refs["donor"]["sha256"] == old["battery_save_preloaded"]["source_sha256"]
    report = read(refs["capture"]["path"])
    prefix = [row for row in old["scripted_input_schedule"] if row["start"] <= play.FIRST_PAUSE]
    assert report["scripted_input_schedule"][:len(prefix)] == prefix
    return report, frames, calls, refs, commands


def live_session(report, arm, frames):
    snapshots = {row["frame"]: row for row in report["read_only_pause_RAM_snapshots"]}
    output = {}
    for frame in (3200, 4400, 5600, 6000, 6800, END):
        snap = snapshots[frame]
        raw = Path(snap["path"]).read_bytes()
        assert snap["read_only_export"] and sha256(raw).hexdigest() == snap["sha256"]
        for name in ("System popup and Quit helper", "Session getter and literal"):
            lo, hi = (address - gate.BASE for address in gate.SPANS[name])
            assert raw[lo:hi] == arm[lo:hi]
        kind, value = unpack_from("<2I", raw, gate.SESSION + 8 - gate.BASE)
        phase, = unpack_from("<I", raw, gate.SESSION + 0x54 - gate.BASE)
        assert (kind, value, phase) == (0, 0, int(frame != END))
        output[frame] = dict(scene_type=kind, scene_argument=value, system_phase=phase, snapshot=snap, capture=frames[frame])
    return output


def sheets(screens):
    labels = ((3200, "Ordinary approach at sea"), (4400, "Functions menu before quitting"), (5600, "First Quit question"),
              (6000, "No restores the menu"), (6800, "Second Quit question"), (END, "Yes returns to the title"))
    sheet = Image.new("RGB", (768, 808), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(labels):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 4, y + 4), label, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    dest = OUT.with_suffix(".png")
    sheet.save(dest)
    return reference(dest)


def main():
    current = play.current
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"] == read(gate.OUT)["candidate_sha256"]
    report, frames, calls, refs, commands = capture(release)
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    source_arm, arm = (rom.read_file(current.ARM) for rom in (clean, image))
    original, installed = (rom.read_file(current.COMMON) for rom in (clean, image))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(installed).hexdigest() == release["target_COMMON_sha256"]
    ja = earlier.base.common_message_entries(original, source_arm)[319]
    en = earlier.base.common_rows(installed, arm)[319]
    font = GameAsciiFont.from_arm9(arm)
    screens = {n: panels.picture(row) for n, row in frames.items()}
    assert screens[4400].tobytes() == screens[6000].tobytes()
    assert screens[5600].tobytes() == screens[6800].tobytes()
    match = [row for row in calls if row["frame"] > play.FIRST_PAUSE]
    assert len(match) == 4 and {row["message_ID"] for row in match} == {319}
    assert not {284, 318, 750, 751, 752} & {row["message_ID"] for row in calls}
    title = find_complete(font, "Continue", screens[END], (96, 223, 158, 249))
    save = find_complete(font, "Save", screens[4400], (96, 248, 158, 267))
    english = en.text.decode("ascii").strip()
    assert english == "Quit the game?" and b"%" not in ja.text + en.text
    holds = []
    for n, (get, copy) in zip(HOLDS, zip(match[::2], match[1::2], strict=True), strict=True):
        assert get["PC"] == 0x0205528C and copy == get | {"PC": 0x020534F4}
        assert get["caller_LR"] == 0x02054680 and 0 < n - get["frame"] < 400
        choices = [panels.find_mask(font, label, screens[n], rect) for label, rect in
                   (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
        holds.append(dict(capture=frames[n], complete_body=panels.exact_body(font, (english,), screens[n]),
                          choices=choices, native_requests=[get, copy]))
    row = dict(id="COMMON_MESSAGE_319", message_ID=319, file_path=current.COMMON,
        context="The player selects Quit Game in the Functions menu while at sea.",
        english=english, clean_Japanese=ja.text.decode("cp932"), source_meaning="The system asks whether to stop playing.",
        localization_note="The brief direct question fits the Yes/No control and identifies the action before returning to the title.",
        decision="retention", review=dict.fromkeys(GATES, True), speaker="System",
        source_reference=earlier.source_ref(ja), current_reference=earlier.source_ref(en),
        installed_reference=earlier.source_ref(en), holds=holds)
    packet = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        records=[row], ordinary_gameplay=True, ordinary_session_words=live_session(report, arm, frames), earlier_quit_matrix=reference(gate.OUT),
        exact_no_returns_to_functions=True, yes_returns_to_title=title, save_label=save, controller=commands, evidence=refs,
        unvisited=["Natural scene type 0 with argument 1", "Other consumers of the archived exhibition warning", "Physical hardware"],
        new_editorial_credit=0, ROM_changed=False)
    validate_natural_dialogue_batch(packet)
    packet["contact_sheet"] = sheets(screens)
    write(OUT, packet)
    print("Verified both at-sea Quit prompts, exact cancellation, and title return on the registered candidate.")


if __name__ == "__main__":
    main()
