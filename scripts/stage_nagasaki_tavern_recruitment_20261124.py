"""Stage and replay the reviewed Nagasaki spare-berth prompt."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import preflight_nagasaki_tavern_recruitment_20261124 as preflight
from scripts import stage_nagasaki_contract_wrap_20261124 as earlier
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


tavern, capacity, KEY = preflight.tavern, preflight.capacity, preflight.KEY
parent, panels = tavern.play.current, tavern.panels
ARM, COMMON = parent.ARM, parent.COMMON
ROOT = Path(".codex-release-work/nagasaki_tavern_recruitment_20261124")
ROM, STORED = ROOT / "Nagasaki_Tavern_Recruitment_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPLAY = ROOT / "replay/capture/capture_report.json"
BEFORE = tavern.play.ROOT / "capture/capture_report.json"
SHEET, PAIRED = ROOT / "nagasaki_tavern_recruitment_paired.png", ROOT / "paired_gameplay.json"
HOLD = 12920


def stage():
    release, draft, gameplay = map(read, (parent.RELEASE, preflight.OUT, tavern.OUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] == draft["candidate_sha256"] == gameplay["candidate_sha256"]
    assert draft["source_review"] == reference(tavern.OUT) and gameplay["ordinary_gameplay"]
    assert all(digest(row["path"]) == row["sha256"] for row in draft["sheets"])
    clean, image = map(NdsImage.open, (CLEAN, parent.ROM))
    arm, prior = (image.read_file(path) for path in (ARM, COMMON))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(prior).hexdigest() == release["target_COMMON_sha256"]
    assert earlier.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    source = tavern.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))[KEY]
    before = tavern.common_rows(prior, arm)
    assert panels.text_reference(source) == draft["source"] and panels.text_reference(before[KEY]) == draft["installed"]
    revised = bytes.fromhex(draft["proposed_stored_hex"])
    assert len(revised) == len(before[KEY].text) and revised.decode("ascii").strip() == tavern.PROPOSED
    assert all(text.count(b"%s") == text.count(b"%") == 1 for text in (source.text, before[KEY].text, revised))
    assert revised.startswith(b" ") and b"\n" not in revised and b"\r" not in revised
    common, entries, allocations = capacity.owned_deployment(prior, arm, before, {KEY: revised})
    assert [new.message_id for old, new in zip(before, entries, strict=True) if old != new] == [KEY]
    assert allocations[KEY] == draft["allocation"] and not allocations[KEY]["new_null_fields"]
    image.replace_file(COMMON, common)
    data = bytes(image.rom.save())
    image.replace_file(COMMON, prior)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(data)
    installed = NdsImage.open(ROM)
    assert installed.read_file(COMMON) == common and installed.read_file(ARM) == arm
    final = tavern.common_rows(common, arm)[KEY]
    assert final.text == revised
    observed, = [case["after"] for case in draft["native_cases"] if case["count"] == 29]
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN),
        target_COMMON_sha256=sha256(common).hexdigest(), target_ARM9_sha256=release["target_ARM9_sha256"],
        changed_message=KEY, exact_clean_source=draft["source"], exact_predecessor=draft["installed"],
        exact_installed=panels.text_reference(final), whole_parent_inverse=True, allocation=allocations[KEY],
        preflight=reference(preflight.OUT), candidate_layout=observed))
    print(f"Staged only COMMON {KEY}. {digest(ROM)}", flush=True)


def run_native_step(action, stored):
    scope = vars(earlier) | globals()
    if action == "verify":
        source = checked_text(getsource(earlier.verify), {
            '"Daimyo"': '"Sailor"',
            '(set(market.GOODS) | {8520, 8920, 9720, 12520, 12920})': '{8120, 9720, 12520, 13320, 14920, 15720, 16520}',
            'revised Palace question': 'revised spare-berth question',
        })
        exec(compile(source, __file__ + "::paired-tavern", "exec"), scope)
        scope["verify"](stored)
    else:
        name = "replay" if action == "replay" else "release_check"
        function = FunctionType(getattr(earlier, name).__code__, scope)
        function(stored, *(() if action == "replay" else (action,)))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup", "replay", "verify"))
    selected = cli.parse_args().action
    if selected == "stage":
        stage()
    else:
        run_native_step(selected, read(STORED))
