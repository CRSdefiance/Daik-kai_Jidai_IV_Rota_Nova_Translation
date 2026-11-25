"""Stage the Sound Setup Stop label in its verified native slot."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import register_pirate_affiliation_20261123 as parent
from scripts import stage_pirate_affiliation_20261123 as release_tools
from scripts.observe_sound_play_stop_20261123 import PLAY, ROOT as CAPTURES, STOP
from scripts.reconcile_editorial_acceptance_20261123 import ARM, right_bound


base, native = parent.base, parent.native
ROOT = CAPTURES / "staged_rom"
ROM, PROOF = ROOT / "Translation_DS_Sound_Stop_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
SLOT, SIZE = 0x170280, 8
STOP_JAPANESE = bytes.fromhex("92e28e7e00000000")
PLAY_JAPANESE = bytes.fromhex("8dc490b600000000")
STOP_ENGLISH, PLAY_ENGLISH = b"Stop".ljust(SIZE, b"\0"), b"Play".ljust(SIZE, b"\0")


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    previous = base.digest(parent.ROM)
    assert previous == release["candidate_sha256"] and base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    evidence = CAPTURES / "current/terminal.json"
    trace = base.load(evidence)
    assert trace["ROM_sha256"] == previous and len(trace["caption_calls"]) == 5
    assert [row["PC"] for row in trace["caption_calls"]] == [PLAY, STOP, PLAY, STOP, PLAY]
    assert {row["text_hex"] for row in trace["caption_calls"]} == {STOP_JAPANESE[:4].hex(), PLAY_ENGLISH[:4].hex()}

    clean, image = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    source, before = map(native.files, (clean, image))
    assert native.digest(before[ARM]) == release["target_ARM9_sha256"]
    context = (0x107DE0, 0x108068)
    assert before[ARM][slice(*context)] == source[ARM][slice(*context)]
    assert source[ARM][SLOT:SLOT + 2 * SIZE] == STOP_JAPANESE + PLAY_JAPANESE
    assert before[ARM][SLOT:SLOT + 2 * SIZE] == STOP_JAPANESE + PLAY_ENGLISH
    final_arm = before[ARM][:SLOT] + STOP_ENGLISH + before[ARM][SLOT + SIZE:]
    assert len(final_arm) == len(before[ARM])
    assert right_bound(final_arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    image.replace_file(ARM, final_arm)
    after = native.files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    guard = parent.parent.parent.bind_registered_story_percent_guard(parent.guard_spec())(source, after)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    target = bytes(image.rom.save())
    image.replace_file(ARM, before[ARM])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(target)
    candidate = base.digest(ROM)
    records = []
    for i, (jp, english, clean_bytes, current_bytes, final_bytes, call, meaning, note) in enumerate((
            ("停止", "Stop", STOP_JAPANESE, STOP_JAPANESE, STOP_ENGLISH, STOP, "Stop the playing music.",
             "Stop names the action on A when the selected music is playing and pairs with the existing Play label."),
            ("再生", "Play", PLAY_JAPANESE, PLAY_ENGLISH, PLAY_ENGLISH, PLAY, "Play the selected music or effect.",
             "Play is the established short action for starting a track or previewing the selected sound effect."))):
        loc = SLOT + i * SIZE
        row = dict(id=f"ARM9_SOUND_SETUP_{english.upper()}", file_path=ARM, speaker="Sound Setup A-button prompt",
            context="The same footer prompt follows the selected BGM or SFX controls and exposes the next action.",
            source_Japanese=jp, english=english, source_meaning=meaning,
            localization_note=note, decision="revision" if i == 0 else "retention", native_call=call,
            source_reference=dict(offset=loc, bytes=clean_bytes.hex(), clean_ROM_sha256=release["clean_input_sha256"]),
            current_reference=dict(offset=loc, bytes=current_bytes.hex(), candidate_sha256=previous),
            installed_reference=dict(offset=loc, bytes=final_bytes.hex(), candidate_sha256=candidate,
                exclusive_end=loc + SIZE, ARM9_sha256=native.digest(final_arm)),
            substitutions=[], pages_in_field=1,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
        records.append(row)
    proof = dict(candidate=str(ROM), candidate_sha256=candidate, predecessor_sha256=previous,
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(final_arm),
        target_COMMON_sha256=release["target_COMMON_sha256"], changed_files=[ARM], exact_parent_inverse=True,
        source25=guard, records=records, translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=list(records[0]["review"]), current_replay_sha256=base.digest(evidence))
    base.save(PROOF, proof)
    print(f"Staged {candidate} with only four Sound Setup text bytes changed.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    else:
        step = release_tools.patch if action == "patch" else release_tools.parent.playback.release_tools.startup
        FunctionType(step.__code__, step.__globals__ | globals())()
