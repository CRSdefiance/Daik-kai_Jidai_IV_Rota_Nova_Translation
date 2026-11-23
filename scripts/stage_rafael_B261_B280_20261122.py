"""Stage the reviewed ruins scene and preserve the audited surrounding encounters."""

from inspect import getsource
from types import SimpleNamespace

from scripts import review_rafael_B261_20261122 as review
from scripts import stage_rafael_B221_B240_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


paired, first, previous = review.paired, prior.first, prior.previous
base, native, parent, TOKEN = paired.base, paired.native, paired.parent, prior.TOKEN
ROOT = paired.ROOT / "staged_B261_B280"
ROM, PROOF = ROOT / "Rafael_B261_B280_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = paired.ROOT / "contextual_manuscript_B261_B280.json", paired.PAIRED
DRAFTS, CARRIES = (review.OUTPUT,), (review.CARRY,)
BLOCKS = (tuple(range(261, 281)), (), (), ())
PREFLIGHT = paired.ROOT / "preflight_B261_native_objects.json"
rebuild_function = prior.rebuild_function

compose = checked_text(getsource(prior.combined_manuscript), {
    'and not d["pending_records"]': '',
    '    names[208] = "Runtime-selected crew voice"':
        '    names.update({207: "Rafael Castor", 208: "Runtime-selected crew voice"})',
    'len(reused) == 48': 'len(reused) == 114',
    'len(fresh) == 222': 'len(fresh) == 21',
    ' and pair["block"] in (225, 226, 240)': '',
    'len(records) == 270': 'len(records) == 135',
    '{"retention": 208, "wording": 60, "glyph": 2}': '{"retention": 129, "wording": 2, "wrap-only": 4}',
    'contextual_records_revisited=222': 'contextual_records_revisited=21',
    'contextual_decisions_reused=48': 'contextual_decisions_reused=114',
})
scope = vars(prior) | globals()
exec(compile(compose, __file__ + "::source-bound-manuscript", "exec"), scope)


def main():
    manuscript = scope["combined_manuscript"]()
    assert sum(item["decision"] == "revision" for item in manuscript["records"]) == 6
    source = checked_text(previous.compiler.source, {"    painter = stage.system.native_painter(ctx)": "    painter = None"})
    compiler = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE), paired=SimpleNamespace(BLOCKS=BLOCKS))
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), compiler)
    compiler["main"]()
    plan = base.load(PREFLIGHT)
    assert plan["draft_sha256"] == base.digest(review.OUTPUT) and plan["candidate_sha256"] == manuscript["previous_sha256"]
    stored = base.load(PROOF)
    assert stored["changed_blocks"] == {"/data/SC0.DK4": [261]}
    commands = {command["source_offset"]: command for group in stored["groups"]
                if group["block"] == 261 for command in group["commands"]}
    for item in plan["objects"]:
        command = commands[item["source_offset"]]
        assert all(command[key] == item[other] for key, other in (
            ("source", "original_hex"), ("current", "current_hex"), ("stored", "proposed_hex")))


if __name__ == "__main__":
    main()
