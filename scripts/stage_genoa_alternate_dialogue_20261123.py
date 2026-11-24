"""Stage the reviewed alternate Genoa dialogue in four original text slots."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack
from types import FunctionType, SimpleNamespace

from scripts import register_genoa_dialogue_20261123 as parent
from scripts import stage_genoa_dialogue_20261123 as previous
from scripts import verify_genoa_alternate_choices_20261123 as review
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/genoa_alternate_dialogue_20261123")
ROM = ROOT / "Genoa_Alternate_Dialogue_STAGED.nds"
STORED = ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
IDS = tuple(f"DK4_MES_B170_R{ordinal:04d}" for ordinal in sorted(review.PROPOSALS))
ARM, COMMON, STORY = previous.ARM, previous.COMMON, previous.STORY
gameplay = SimpleNamespace(OUT=review.OUT, town=review.gameplay.town)


def explicit_walk():
    original = previous.explicit_walk()

    def branch_rows(arm, block, lo, hi):
        window = block[:4] + pack("<2H", hi - lo, 0) + block[lo:hi]
        native = original(arm, window)
        assert native["error"] is None, (lo, hi, native["error"])
        for row in native["rows"]:
            offset = lo + row["offset"] - 8
            limit = offset + row["native_extent"]
            assert lo <= offset < limit <= hi
            yield row | {"offset": offset}
            if row["word"] == 0x0100:
                yield from branch_rows(arm, block, offset + 4, limit)

    def walk(arm, block):
        limit = 8 + int.from_bytes(block[4:6], "little")
        assert limit <= len(block) and not any(block[limit:])
        return dict(error=None, rows=list(branch_rows(arm, block, 8, limit)))

    return walk


source = checked_text(getsource(previous.stage), {
    '    genoa = packet["ordinary_gameplay"]["genoa"]\n'
    '    assert packet["draft_findings"] == 3\n'
    '    assert len(genoa["proposed_native_sheets"]) == 1\n'
    '    assert all(reference(row["path"]) == row for row in genoa["proposed_native_sheets"])\n'
    '    proposals = defaultdict(list)\n'
    '    for row in genoa["story"]:\n'
    '        if row["proposed_English"]:\n'
    '            proposals[row["block"]].append(row)':
        '''    assert packet["verified_story_holds"] == 20 and packet["fresh_ordinary_input_runs"] == 2
    assert len(packet["offline_proposed_pages"]) == 1
    assert all(reference(row["path"]) == row for row in packet["offline_proposed_pages"])
    proposals = defaultdict(list)
    for branch in packet["choice_paths"].values():
        assert branch["ordinary_tavern_return"]
        for row in branch["story"]:
            if row["decision"] == "revision proposed":
                proposals[row["block"]].append(row)
    assert set(proposals) == {170}''',
})
scope = vars(previous) | globals()
exec(compile(source, __file__ + "::registered-fixed-allocations", "exec"), scope)
stage = scope["stage"]
check = FunctionType(previous.check.__code__, scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    stage() if action == "stage" else check(action)
