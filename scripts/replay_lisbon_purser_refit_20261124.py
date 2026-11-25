"""Reproduce the Purser help hold on a one-record staged candidate."""

import json
from types import FunctionType, SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from scripts import observe_lisbon_stock_quota_20261124 as play
from scripts import preflight_lisbon_purser_refit_20261124 as draft
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


ROOT = play.ROOT.with_name("editorial_20261124_lisbon_purser_refit")
ROM = ROOT / "Lisbon_Purser_Refit_STAGED.nds"
STAGED = ROOT / "unregistered_replay_manifest.json"
CAPTURE = ROOT / "paired"
STOP_AT = 43700


def prepare():
    current = play.current
    parent, proposal = map(read, (current.RELEASE, draft.OUT))
    assert proposal["candidate_sha256"] == parent["candidate_sha256"] == digest(current.ROM)
    rom = NdsImage.open(current.ROM)
    original = rom.read_file(current.COMMON)
    assert sha256(original).hexdigest() == parent["target_COMMON_sha256"]
    owner = proposal["owned_allocation"]
    block, lo, hi = (owner[key] for key in ("block", "start", "end"))
    blocks = list(IlnkContainer.parse(original).blocks)
    assert blocks[block][lo:hi].hex() == owner["before"]
    blocks[block] = blocks[block][:lo] + bytes.fromhex(owner["proposed"]) + blocks[block][hi:]
    deployed = IlnkContainer(blocks).to_bytes()
    assert sha256(deployed).hexdigest() == proposal["proposed_COMMON_sha256"]
    rom.replace_file(current.COMMON, deployed)
    ROOT.mkdir()
    rom.save(ROM)
    rom.replace_file(current.COMMON, original)
    assert sha256(rom.rom.save()).hexdigest() == parent["candidate_sha256"]
    write(STAGED, parent | dict(candidate=str(ROM), candidate_sha256=digest(ROM), unregistered_staged_replay=True,
        target_COMMON_sha256=proposal["proposed_COMMON_sha256"], exact_parent_inverse=True,
        parent_release=reference(current.RELEASE), proposal=reference(draft.OUT)))


def main():
    prepare()
    earlier = read(play.ROOT / "stock_quota_runner.json")
    assert earlier["controller"] == reference(play.CONTROLLER)
    actions = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    prefix = [action for action in actions if action.get("until", STOP_AT + 1) <= STOP_AT]
    assert prefix[-1]["until"] == STOP_AT and prefix[:len(play.OPENING)] == list(play.OPENING)
    temp = SimpleNamespace(**(vars(play.current) | dict(RELEASE=STAGED, ROM=ROM)))
    prior = SimpleNamespace(**(vars(play.stock.prior) | {"current": temp}))
    scope = vars(play.stock) | dict(prior=prior, ROOT=CAPTURE, CONTROLLER=CAPTURE / "controller.jsonl",
                                    ACTIONS=prefix + [{"stop": True}], __file__=__file__)
    scope["finance_prerequisite"] = FunctionType(play.stock.finance_prerequisite.__code__, scope)
    FunctionType(play.stock.main.__code__, scope)()
    write(ROOT / "paired_terminal.json", dict(candidate=reference(ROM), parent=reference(play.current.RELEASE),
        original_capture=reference(play.ROOT / "capture/capture_report.json"),
        candidate_capture=reference(CAPTURE / "capture/capture_report.json"),
        controller=reference(CAPTURE / "controller.jsonl"), frames=STOP_AT, source=reference(__file__)))


if __name__ == "__main__":
    main()
