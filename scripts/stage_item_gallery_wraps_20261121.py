"""Reflow eight complete item descriptions inside their original slots."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
import sys
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan
from dk4tool.patch.source_item_cards_and_coin_v1 import PROTECTED_PHRASES, compile_item
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import audit_item_gallery_editorial_20261121 as audit
from scripts import headless_desmume_v193 as emulator
from scripts.verify_characters_gallery_v525 import report


base, parent = audit.base, audit.current
ARM, COMMON, CLEAN = audit.stage.ARM, audit.stage.COMMON, audit.stage.CLEAN
ROOT = Path("work/item_gallery_wraps_20261121")
ROM, PROOF = ROOT / "Items_Gallery_Wraps_STAGED.nds", ROOT / "staged.json"
LIVE = ROOT / "gallery_wraps_playback.json"
PHRASES = {
    3: ("It is packed with nourishing nectar", "they gather from flowers."),
    18: ("An Eastern medical text of unknown authorship.", "from herbs and bark."),
    44: ("a black handle and twisted tip.",),
    108: ("this miraculous cross resurfaced", "after over a thousand years underground."),
    120: ("with its delicate beauty.",),
    132: ("when she went back.",),
    154: ("remains a mystery.",),
    174: ("Its purpose is a mystery.",),
}


def read_native(arm):
    code = MainCodeFile(arm, BASE)
    deployed, = (s.data for s in code.sections if s.ramAddress == STAGE)
    resident, = (s.data for s in code.sections if s.ramAddress == 0x01FFD000)
    return code, deployed, resident


def transform(arm, coverage):
    code, copied, resident = read_native(arm)
    assert bytes(code.save()) == arm
    records, inverse = [], []
    pointers = [row["current_projection"]["pointer"] for row in coverage["records"]]
    assert len(pointers) == 218
    for row in coverage["records"]:
        draft = row.get("open_wrap")
        if not draft:
            continue
        index, pointer = row["item_ID"], pointers[row["item_ID"]]
        reference = row["current_projection"]
        assert pointers.count(pointer) == 1
        assert unpack_from("<I", copied, reference["pointer_field"] - POOL)[0] == pointer
        original = bytes.fromhex(reference["stored_hex"])
        assert all(other == pointer or other < pointer or other >= pointer + len(original) for other in pointers)
        phrases = PHRASES[index]
        compiler = FunctionType(compile_item.__code__, compile_item.__globals__ | {
            "PROTECTED_PHRASES": PROTECTED_PHRASES + phrases,
        })
        rows, formatted = compiler(row["English"])
        assert all(any(phrase in line for line in rows) for phrase in phrases)
        assert len(formatted) == len(original) and original != formatted
        assert " ".join(rows) == row["English"] and 2 <= len(rows) <= 3 and all(0 < len(line) <= 47 for line in rows)
        region, start = (copied, POOL) if pointer >= POOL else (resident, 0x01FFD000)
        at = pointer - start
        assert region[at:at + len(original)] == original
        region[at:at + len(original)] = formatted
        inverse.append((region, at, original))
        records.append(dict(id=f"ITEM_GALLERY_WRAP_{index:03d}", item_ID=index, message_ID=row["message_ID"],
            file_path=ARM, speaker="Item description", clean_Japanese=bytes.fromhex(row["source_hex"]).decode("cp932"),
            english=row["English"], previous_English=row["English"], decision="retention", finding="wrap",
            context="Items Gallery and inventory display the same small catalogue card from the original item table.",
            source_meaning="The complete original item description recorded in the linked source review.",
            localization_note=draft["reason"], protected_phrases=list(phrases),
            source_reference=row["source_reference"], current_reference=reference,
            related_common_reference=row["current_reference"], related_common_hex=row["current_hex"],
            prior_review=row["previous_review"],
            staged_reference=reference | dict(lines=list(rows), stored_hex=formatted.hex()),
            review=dict.fromkeys(REQUIRED_REVIEW_GATES, True) | {"formatting": False}))
    assert len(records) == 8
    target = bytes(code.save())
    assert cache_plan(target) == cache_plan(arm)
    for region, at, original in inverse:
        region[at:at + len(original)] = original
    assert bytes(code.save()) == arm
    return target, records


def stage():
    assert not ROOT.exists()
    release, coverage = map(base.load, (parent.RELEASE, audit.OUTPUT))
    assert base.digest(parent.ROM) == release["candidate_sha256"] == coverage["candidate_sha256"]
    assert base.load(base.LEDGER)["current_integrated_candidate"]["sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    image = base.NdsImage.open(parent.ROM)
    arm = image.read_file(ARM)
    target, records = transform(arm, coverage)
    image.replace_file(ARM, target)
    output = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(output)
    patch, rebuilt = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
    make_xdelta(CLEAN, ROM, patch)
    apply_xdelta(CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=audit.stage.native.digest(target),
        coverage_sha256=base.digest(audit.OUTPUT), records=records,
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES)))
    print("Staged eight exact-length wraps and verified the clean-input patch.", flush=True)


def replay():
    proof = base.load(PROOF)
    digest = base.digest(ROM)
    assert proof["candidate_sha256"] == digest
    fixture = base.load(audit.DONOR / "fixture/save_fixture_manifest.json")
    fixture.update(production_ROM=str(ROM), production_ROM_sha256=digest)
    path = ROOT / "fixture.json"
    base.save(path, fixture)
    plan = base.load(audit.DONOR / "all_plan.json")
    ids = {0, *(r["item_ID"] for r in proof["records"])}
    cases = [r for r in plan["cases"] if r["item_id"] in ids]
    frames = [*(r["frame"] for r in cases), plan["wrap_frame"], plan["back_frame"]]
    base.save(ROOT / "sample.json", dict(cases=cases, frames=frames, wrap=plan["wrap_frame"], back=plan["back_frame"]))
    sys.argv = [emulator.__file__, "--rom", str(ROM), "--out", str(ROOT / "capture"), "--frames", "23000",
        "--capture-every", "99999", "--capture-at", *map(str, frames), "--dump-ram", "--touchscreen",
        "--allow-gallery-fixtures", "--battery-save", fixture["fixture_save"],
        "--gallery-save-fixture-manifest", str(path), "--inputs-json", str(audit.DONOR / "all_inputs.json")]
    emulator.main()


def verify():
    assert not LIVE.exists()
    proof, coverage = map(base.load, (PROOF, audit.OUTPUT))
    image = base.NdsImage.open(ROM)
    arm = image.read_file(ARM)
    digest = base.digest(ROM)
    assert proof["candidate_sha256"] == digest
    observed = report(ROOT / "capture", digest)
    assert observed["frames"] == 23000 and not observed["earned_unlock_verified"]
    assert observed["scripted_input_schedule"] == base.load(audit.DONOR / "all_inputs.json")
    snapshot = observed["read_only_RAM_snapshot"]
    path = Path(snapshot["path"])
    assert snapshot["read_only_export"] and base.digest(path) == snapshot["sha256"]
    records = coverage["records"]
    for row in proof["records"]:
        records[row["item_ID"]]["current_projection"] = row["staged_reference"]
    cards, sheets = audit.verify_cards(image, path.read_bytes(), records, arm, observed, workspace=ROOT)
    assert {r["item_ID"] for r in proof["records"]} | {0} == {r["item_id"] for r in cards}
    snapshot_paths = [path, ROOT / "capture/capture_report.json", ROOT / "fixture.json", ROOT / "sample.json"]
    evidence = {str(p): base.digest(p) for p in snapshot_paths} | {r["capture"]["path"]: r["capture"]["PNG_sha256"] for r in cards}
    base.save(LIVE, dict(candidate_sha256=digest, cards=cards, sheets=sheets, evidence=evidence,
        original_gallery_controls=True, initialized_collection=True, full_original_carousel_return=True,
        natural_acquisition=False, hardware=False))
    print("Verified eight revised item cards and one unchanged control in the original Gallery.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "replay", "verify"))
    action = parser.parse_args().action
    {"stage": stage, "replay": replay, "verify": verify}[action]()
