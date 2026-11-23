"""Bind the Stockholm manuscript to the fleet successor and stage its three repairs."""
from pathlib import Path
from types import SimpleNamespace

from scripts import register_numbered_fleet_spacing_20261121 as parent
from scripts import review_stockholm_dialogue_followup_20261121 as author
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage = compiler.base, compiler.native, compiler.stage
WORK = Path("out/stockholm_dialogue_followup_20261121")
ROOT = WORK / "staged"
ROM, PROOF = ROOT / "Stockholm_Dialogue_STAGED.nds", ROOT / "stored_proof.json"
logical_end = compiler.logical_end
REBOUND = WORK / "review_with_registered_fleet_parent.json"
PACKET = WORK / "paired_source_with_registered_fleet_parent.json"


def rebind():
    manuscript, packet = map(base.load,(author.OUTPUT,author.SOURCE))
    release, previous = map(base.load,(parent.RELEASE,author.parent.RELEASE))
    assert manuscript["previous_sha256"] == packet["candidate_sha256"] == previous["candidate_sha256"]
    assert release["predecessor"]["candidate_sha256"] == previous["candidate_sha256"]
    assert release["changed_internal_files"] == [native.ARM]
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    images = [base.NdsImage.open(p) for p in (author.parent.ROM,parent.ROM)]
    a,b = [image.read_file(native.ARM) for image in images]
    lo, hi = parent.stage.OFFSET,parent.stage.OFFSET+parent.stage.CAPACITY
    assert a[:lo] == b[:lo] and a[hi:] == b[hi:]
    for path in sorted({g["file_path"] for g in packet["groups"]} | {"/GRP/KANJI.FNT"}):
        assert images[0].read_file(path) == images[1].read_file(path)
    packet.update(candidate_sha256=release["candidate_sha256"],profile=release["profile"])
    WORK.mkdir()
    base.save(PACKET,packet)
    manuscript.update(previous_sha256=release["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],
        source_packet=str(PACKET),source_packet_sha256=base.digest(PACKET),prior_editorial_sha256=base.digest(author.OUTPUT),
        retained_screen_dependencies_equal=True)
    base.save(REBOUND,manuscript)


def main():
    if not WORK.exists():
        rebind()
    script = checked_text(compiler.source,{
        "Staged all revised story phrases": "Staged the Stockholm Square and Tavern edits",
        "painter = stage.system.native_painter(ctx)": "painter = author.live.town.current_fe_painter(ctx)",
    })
    scope = compiler.env | globals() | {"review":SimpleNamespace(OUTPUT=REBOUND,SOURCE=PACKET),"paired":author}
    exec(compile(script,__file__+"::stage-stockholm","exec"),scope)
    scope["main"]()
    proof = base.load(PROOF)
    assert proof["changed_blocks"] == {"/data/SC1.DK4":[134,189]} and proof["whole_parent_inverse"]


if __name__ == "__main__":
    main()
