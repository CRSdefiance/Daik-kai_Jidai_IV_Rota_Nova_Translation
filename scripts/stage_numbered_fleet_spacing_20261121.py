"""Fix the missing space between faction names and numbered fleets."""
from pathlib import Path
import re
from struct import pack, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from scripts import register_athens_london_trends_20261121 as active
from scripts import replay_stockholm_december_20261121 as play
from scripts import verify_amsterdam_bread_gameplay_20261121 as display
from scripts.checkpoint_pending_shared_native_20261115 import components


base, native = active.base, active.native
ROOT = Path("out/numbered_fleet_spacing_20261121")
ROM, PROOF = ROOT / "Numbered_Fleet_Spacing_STAGED.nds", ROOT / "stored_proof.json"
OFFSET, CAPACITY, LITERAL, FLEET_GETTER = 0x135250, 8, 0x36B50, 0x36A6C
SOURCE, ENGLISH = b"%s%s\0\0\0\0", b"%s %s\0\0\0"


def get_names(arm, ram):
    cpu, get = display.get_machine(arm, ram)
    root = get(0xCB1A8)
    results = []
    for index in range(50):
        pointer = get(FLEET_GETTER, root + 4 + index * 132)
        text, terminator, _ = bytes(cpu.mem_read(pointer, 64)).partition(b"\0")
        assert text and terminator
        results.append(text)
    return results


def main():
    assert not ROOT.exists()
    release = base.load(active.RELEASE)
    assert base.digest(active.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    predecessor, original = (base.NdsImage.open(path) for path in (active.ROM, native.CLEAN))
    arm, clean = (image.read_file(native.ARM) for image in (predecessor, original))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    for image, code in ((original, clean), (predecessor, arm)):
        assert code[OFFSET:OFFSET + CAPACITY] == SOURCE
        assert unpack_from("<I", code, LITERAL)[0] == display.B + OFFSET
        aliases = []
        for name, address, data in components(image.rom):
            for i in range(CAPACITY):
                for match in re.finditer(re.escape(pack("<I", display.B + OFFSET + i)), data):
                    if match.start() % 4 == 0:
                        aliases.append((name, address + match.start(), i))
        assert aliases == [("ARM9 section 0", display.B + LITERAL, 0)], aliases

    captures = play.ROOT / "capture"
    report_path = captures / "capture_report.json"
    report = base.load(report_path)
    assert report["ROM_sha256"] == release["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    shot, = [f for f in report["frames_captured"] if f["frame"] == 5960 and "_navigation" in f["path"]]
    assert base.digest(shot["path"]) == shot["PNG_sha256"]
    snap = report["read_only_RAM_snapshot"]
    assert snap["read_only_export"] and base.digest(snap["path"]) == snap["sha256"]
    ram = Path(snap["path"]).read_bytes()
    assert len(ram) == 0x400000 and ram[OFFSET:OFFSET + CAPACITY] == SOURCE
    assert b"CliffordFleet \x82\x51\0" in ram
    new_arm = arm[:OFFSET] + ENGLISH + arm[OFFSET + CAPACITY:]
    assert bytes(MainCodeFile(new_arm, display.B).save()) == new_arm
    new_ram = ram[:OFFSET] + ENGLISH + ram[OFFSET + CAPACITY:]
    old, new = get_names(arm, ram), get_names(new_arm, new_ram)
    assert old[20] == b"CliffordFleet \x82\x51" and new[20] == b"Clifford Fleet \x82\x51"
    out = []
    for i, (before, after) in enumerate(zip(old, new, strict=True)):
        expected = re.sub(rb"(?<=\S)(Fleet \x82[\x4f-\x58])$", rb" \1", before) if i < 39 else before
        assert after == expected and len(after) * 6 <= 192, (i, before, after)
        out.append(dict(index=i, before=before.decode("cp932"), after=after.decode("cp932"), changed=before!=after))
    assert sum(row["changed"] for row in out) == 38

    before = native.files(predecessor)
    predecessor.replace_file(native.ARM, new_arm)
    after = native.files(predecessor)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {native.ARM}
    output = bytes(predecessor.rom.save())
    predecessor.replace_file(native.ARM, arm)
    assert bytes(predecessor.rom.save()) == active.ROM.read_bytes()
    record = dict(id="FLEET_NAME_135250", file_path=native.ARM, speaker="Numbered fleet label",
        context="The Route Map shows a fleet in the header and shows its name beside its marker. Numbered fleets identify their faction plus their ordinal.",
        source_meaning="Join the owning faction name and the original numbered fleet label in that order.",
        previous_English="%s%s", english="%s %s{PAD}",
        localization_note="Insert a single word space between the two independent names. Keep the order, internal spaces, ordinal and native full-width digits.",
        source_reference=dict(offset=OFFSET, command_offset=LITERAL, exact_hex=SOURCE.hex()),
        current_reference=dict(offset=OFFSET, command_offset=LITERAL, exact_hex=SOURCE.hex()),
        staged_reference=dict(offset=OFFSET, command_offset=LITERAL, exact_hex=ENGLISH.hex()),
        review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True) | {"formatting": False})
    ROOT.mkdir()
    ROM.write_bytes(output)
    base.save(PROOF, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-fixed-v1",
        target_locale="en-US", review_gates=sorted(REQUIRED_REVIEW_GATES), records=[record],
        predecessor_sha256=release["candidate_sha256"], candidate_sha256=base.digest(ROM),
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(new_arm),
        complete_parent_inverse=True, affected_snapshot_labels=38, existing_getter_results=out,
        proof_uses_ordinary_read_only_replay_snapshot=True, original_screenshot=shot,
        evidence={str(report_path):base.digest(report_path), snap["path"]:snap["sha256"]},
        gameplay_of_revised_candidate_pending=True))
    print("Staged the private fleet label separator. 38 numbered fleets gained one space in the native getter.")


if __name__ == "__main__":
    main()
