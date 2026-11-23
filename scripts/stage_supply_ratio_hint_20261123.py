"""Make an isolated native display probe for the L/R Supply Ratio hint."""

import json
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.rom.nds import NdsImage
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, digest, read, reference, right_bound


RELEASE = Path("releases/all_routes_editorial_20261123_sound_play_stop_candidate/verification/registered_release_verification.json")
BEFORE = Path(".codex-release-work/supply_ratio_selector_20261123_v5/observer/requests.json")
SLOT = 0x14A110
SOURCE = bytes.fromhex("8A848D8700000000")
ENGLISH = b"Mix".ljust(len(SOURCE), b"\0")


def stage(folder):
    target = folder / "Translation_DS_Supply_Ratio_Mix_STAGED.nds"
    proof = folder / "stored_proof.json"
    assert not target.exists() and not proof.exists()
    current = read(RELEASE)
    trace = read(BEFORE)
    capture = read(BEFORE.parent.parent / "mix/capture/capture_report.json")
    assert capture["ROM_sha256"] == current["candidate_sha256"] and not trace["errors"] and not trace["mismatches"]
    assert [(row["PC"], row["text_pointer"], row["text_hex"]) for row in trace["rows"]] == [
        (0x02060500, None, ""),
        (0x020D5404, 0x0214A44C, b"Supply Ratio".hex()),
        (0x02086390, BASE + SLOT, SOURCE[:4].hex()),
        (0x020D5404, BASE + SLOT, SOURCE[:4].hex()),
    ]
    assert trace["rows"][2]["descriptor_address"] == 0x02119808

    clean_path, parent = Path("work/clean.nds"), Path(current["candidate"])
    assert digest(clean_path) == current["clean_input_sha256"]
    assert digest(parent) == current["candidate_sha256"]
    assert digest("translations/release_stack.json") == current["registry_sha256"]
    clean, original = [NdsImage.open(p).read_file(ARM) for p in (clean_path, parent)]
    assert sha256(original).hexdigest() == current["target_ARM9_sha256"]
    for low, high in ((0x60500, 0x6050C), (0x86354, 0x863A8), (0xD5404, 0xD5410), (0x119808, 0x119810)):
        assert clean[low:high] == original[low:high]
    assert clean[SLOT:SLOT + len(SOURCE)] == original[SLOT:SLOT + len(SOURCE)] == SOURCE
    assert unpack_from("<I", original, 0x11980C)[0] == BASE + SLOT

    parent_raw = parent.read_bytes()
    arm_start = unpack_from("<I", parent_raw, 0x20)[0]
    assert parent_raw[arm_start:arm_start + len(original)] == original
    low = arm_start + SLOT
    high = low + len(SOURCE)
    proposed = parent_raw[:low] + ENGLISH + parent_raw[high:]
    assert len(proposed) == len(parent_raw)
    assert proposed[:low] + SOURCE + proposed[high:] == parent_raw
    arm = proposed[arm_start:arm_start + len(original)]
    assert right_bound(arm, current["right_bound_configuration"])["matched_repair_spans"] == 8
    folder.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(".partial")
    output = partial.open("xb")
    try:
        with output as stream:
            for start in range(0, len(proposed), 1 << 20):
                stream.write(proposed[start:start + (1 << 20)])
        assert digest(partial) == sha256(proposed).hexdigest()
        partial.rename(target)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    candidate = digest(target)
    assert sha256(proposed).hexdigest() == candidate
    record = dict(id="ARM9_SUPPLY_RATIO_BUTTON_HINT", file_path=ARM, speaker="Supply Ratio L/R button hint",
        context="After the Port Worker asks whether to change the mix of water and food, the Supply Ratio panel shows both percentages and the L/R adjustment.",
        source_Japanese="割合", english="Mix", source_meaning="The relative shares of water and food.",
        localization_note="Mix names the setting in the same words the Port Worker uses. The existing Supply Ratio heading already identifies the percentage panel.",
        source_reference=dict(offset=SLOT, bytes=SOURCE.hex(), clean_ROM_sha256=current["clean_input_sha256"]),
        current_reference=dict(offset=SLOT, bytes=SOURCE.hex(), candidate_sha256=current["candidate_sha256"]),
        installed_reference=dict(offset=SLOT, exclusive_end=SLOT + len(SOURCE), bytes=ENGLISH.hex(), candidate_sha256=candidate),
        substitutions=[], pages_in_field=1, decision="revision",
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
    result = dict(candidate=str(target), candidate_sha256=candidate, predecessor_sha256=current["candidate_sha256"],
        clean_input_sha256=current["clean_input_sha256"], target_ARM9_sha256=sha256(arm).hexdigest(),
        target_COMMON_sha256=current["target_COMMON_sha256"], changed_file=ARM, ROM_byte_offset=low,
        exact_parent_inverse=True, source_trace=reference(BEFORE), research_stage=True, record=record)
    proof.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Staged the L/R hint for emulator verification. SHA-256 {candidate}")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    stage(parser.parse_args().folder)
