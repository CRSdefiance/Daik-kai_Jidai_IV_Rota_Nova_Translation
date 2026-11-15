"""Replay the cumulative release's preserved startup controls."""

from inspect import getsource
from types import FunctionType

from scripts import replay_visible_gallery_captions_v1 as boot
from scripts import stage_tavern_toast_and_gift_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    root,base = stage.ROOT,stage.base
    prior = stage.parent.stage.ROOT/"startup_retry"
    output = root/"own_startup"
    proof = root/"startup_input.json"
    stored = base.load(stage.STORED)
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    data = dict(research_ROM_sha256=stored["candidate_sha256"],
        registered_input=dict(candidate_sha256=stored["previous_sha256"]))
    if proof.exists():
        assert base.load(proof)==data
    else:
        base.save(proof,data)
    if not (output/"terminal.json").exists():
        FunctionType(boot.startup_replay.main.__code__,vars(boot.startup_replay)|dict(
            EVIDENCE=proof,ROM=stage.ROM,STARTUP=output,PRIOR=prior))()
    original = getsource(boot.startup_check.verify_startup)
    source = checked_text(original,{
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'":"PARENT_CAPTURE / 'capture/capture_report.json'",
    })
    env = vars(boot.startup_check)|dict(ROOT=root,ROM=stage.ROM,PROOF=proof,BOOT=root/"own_startup_verification.json",
        PARENT_CAPTURE=prior,BIOGRAPHIES=prior.parent)
    exec(compile(source,__file__+"::registered-startup-contract","exec"),env)
    env["verify_startup"]()


if __name__ == "__main__":
    main()
