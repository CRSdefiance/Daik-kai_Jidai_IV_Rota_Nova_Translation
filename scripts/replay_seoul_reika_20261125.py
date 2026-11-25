"""Replay the ordinary Seoul Tavern sequence against one staged COMMON edit."""

from inspect import getsource
from types import SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from scripts import observe_seoul_tavern_accept_20261125 as play
from scripts import preflight_seoul_reika_20261125 as draft
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, sha256, write


ROOT = play.ROOT.with_name("editorial_20261125_seoul_reika")
ROM = ROOT / "Seoul_Reika_STAGED.nds"
STAGED = ROOT / "unregistered_replay_manifest.json"
CAPTURE = ROOT / "paired"


def main():
    parent, proposal = map(read, (play.current.RELEASE, draft.OUT))
    assert proposal["parent_candidate_sha256"] == parent["candidate_sha256"] == digest(play.current.ROM)
    original = NdsImage.open(play.current.ROM)
    common = original.read_file(play.current.COMMON)
    assert sha256(common).hexdigest() == parent["target_COMMON_sha256"]
    slot = proposal["allocation"]
    block, lo, hi = (slot[k] for k in ("block", "start", "end"))
    blocks = list(IlnkContainer.parse(common).blocks)
    assert blocks[block][lo:hi].hex() == slot["before"]
    blocks[block] = blocks[block][:lo] + bytes.fromhex(slot["after"]) + blocks[block][hi:]
    proposed = IlnkContainer(blocks).to_bytes()
    assert sha256(proposed).hexdigest() == proposal["proposed_COMMON_sha256"]
    original.replace_file(play.current.COMMON, proposed)
    ROOT.mkdir()
    original.save(ROM)
    original.replace_file(play.current.COMMON, common)
    assert sha256(original.rom.save()).hexdigest() == parent["candidate_sha256"]
    write(STAGED, parent | dict(candidate=str(ROM), candidate_sha256=digest(ROM), unregistered_staged_replay=True,
        target_COMMON_sha256=proposal["proposed_COMMON_sha256"], exact_parent_inverse=True,
        parent_release=reference(play.current.RELEASE), proposal=reference(draft.OUT)))

    baseline = read(draft.review.OUT)
    assert baseline["candidate_sha256"] == parent["candidate_sha256"]
    terminal = read(baseline["evidence"]["terminal"]["path"])
    assert terminal["evidence"][str(play.CONTROLLER)] == digest(play.CONTROLLER)
    current = SimpleNamespace(ROM=ROM, RELEASE=STAGED)
    source = checked_text(getsource(play.main), {
        'stream.write(json.dumps(OPENING) + "\\n")': 'stream.write(BASELINE_CONTROLLER.read_text("utf-8"))',
    })
    scope = vars(play) | dict(ROOT=CAPTURE, CONTROLLER=CAPTURE / "controller.jsonl", current=current,
                             BASELINE_CONTROLLER=play.CONTROLLER, __file__=__file__)
    exec(compile(source, __file__ + "::same-Seoul-inputs", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()
