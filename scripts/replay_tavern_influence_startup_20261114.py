"""Run the registered predecessor's startup and protected-getter checks."""

from inspect import getsource
from types import FunctionType

from scripts import replay_visible_gallery_captions_v1 as boot
from scripts import stage_tavern_influence_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    root = stage.ROOT
    proof = root / "startup_input.json"
    stopped = stage.base.load(stage.STORED)
    assert stage.base.digest(stage.ROM) == stopped["candidate_sha256"]
    expected = dict(research_ROM_sha256=stopped["candidate_sha256"],
        registered_input=dict(candidate_sha256=stopped["previous_sha256"]))
    if proof.exists():
        assert stage.base.load(proof) == expected
    else:
        stage.base.save(proof, expected)
    prior = stage.parent.stage.ROOT / "own_startup"
    if not (root / "startup_retry" / "terminal.json").exists():
        FunctionType(boot.startup_replay.main.__code__, vars(boot.startup_replay) | dict(
            EVIDENCE=proof, ROM=stage.ROM, STARTUP=root / "startup_retry", PRIOR=prior))()
    code = checked_text(getsource(boot.startup_check.verify_startup), {
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PARENT_CAPTURE / 'capture/capture_report.json'",
        "ROOT / 'own_startup/capture/capture_report.json'": "ROOT / 'startup_retry/capture/capture_report.json'",
        "ROOT / 'own_startup/terminal.json'": "ROOT / 'startup_retry/terminal.json'",
    })
    env = vars(boot.startup_check) | dict(ROOT=root, ROM=stage.ROM, PROOF=proof,
        BOOT=root / "own_startup_verification.json", PARENT_CAPTURE=prior, BIOGRAPHIES=prior.parent)
    exec(compile(code, __file__ + "::startup-contract", "exec"), env)
    env["verify_startup"]()


if __name__ == "__main__":
    main()
