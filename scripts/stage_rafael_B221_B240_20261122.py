"""Stage Rafael B221–240 while retaining the original letter selectors and aliases."""

from collections import Counter
from types import FunctionType, SimpleNamespace

from scripts import pair_rafael_B221_B240_20261122 as paired
from scripts import review_rafael_B221_B224_20261122 as first
from scripts import review_rafael_B227_B239_20261122 as later
from scripts import stage_rafael_B181_B187_20261121 as modal_writer
from scripts import stage_rafael_B161_B169_20261121 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = paired.base, paired.native, paired.parent
ROOT = paired.ROOT / "staged_B221_B240_v2"
ROM, PROOF = ROOT / "Rafael_B221_B240_STAGED.nds", ROOT / "stored_proof.json"
MANUSCRIPT, SOURCE = paired.ROOT / "contextual_manuscript_B221_B240_v2.json", paired.PAIRED
DRAFTS = (first.OUTPUT, later.OUTPUT)
CARRIES = tuple(paired.ROOT / file for file in ("earlier_decisions_B225_B240.json", "earlier_decisions_B226.json"))
STYLE_PREFLIGHT = paired.ROOT / "format_preflight_B221_B224_v3.json"
BLOCKS = (tuple(range(221, 241)), (), (), ())
TOKEN = first.precedent.TOKEN


def combined_manuscript():
    packet = base.load(SOURCE)
    history = list(map(base.load, CARRIES))
    predecessor, source_hash = base.digest(parent.ROM), base.digest(SOURCE)
    assert packet["candidate_sha256"] == predecessor
    assert all(d["candidate_sha256"] == predecessor and d["source_packet_sha256"] == source_hash and not d["pending_records"]
               for d in history)
    reused = {row["id"]: row for proof in history for row in proof["reused_records"]}
    assert len(reused) == 48
    drafts = list(map(base.load, DRAFTS))
    assert all(d["previous_sha256"] == predecessor and d["source_packet_sha256"] == source_hash for d in drafts)
    fresh = {row["id"]: row for draft in drafts for row in draft["records"]}
    assert len(fresh) == 222 and not set(fresh) & set(reused)
    names = {row["actor_ID"]: row["progressive_nameplate"] for row in
             base.load(first.precedent.prior.CATALOGUE)["source_and_current_default_name_fields"]}
    names[208] = "Runtime-selected crew voice"
    normalize = FunctionType(first.precedent.normalize.__code__, first.precedent.normalize.__globals__ | {"WRAPS": {}})
    records = []
    for group in packet["groups"]:
        for pair in group["records"]:
            ident = pair["id"]
            if ident in fresh:
                row = fresh.pop(ident)
                assert all(row[key] == value for key, value in pair.items())
                records.append(row)
                continue
            evidence = reused.pop(ident)
            assert all(evidence[key] == pair[key] for key in ("source_reference", "current_reference"))
            assert all(evidence["prior_review_gates"].values()) and pair["block"] in (225, 226, 240)
            text = " ".join(pair["current_English"].split())
            entry = normalize(pair | dict(previous_English=text, english=text, protected_phrases=[],
                localization_note=evidence["localization_note"], decision="retention",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)), names)
            if pair["native_command_word"] == 0x4100:
                assert evidence["native_slots"] == pair["slots"]
                entry.update(kind="actor-style", source_hex=pair["source_reference"]["exact_body_hex"],
                             current_hex=pair["current_reference"]["exact_body_hex"])
            entry["earlier_contextual_decision"] = evidence
            records.append(entry)
    assert len(records) == 270 and not fresh and not reused
    counts = Counter(row["change_class"] for row in records)
    assert counts == {"retention": 208, "wording": 60, "glyph": 2}
    doc = drafts[0] | dict(records=records, findings=dict(counts), contextual_records_revisited=222,
        contextual_decisions_reused=48, component_drafts={str(path): base.digest(path) for path in DRAFTS},
        earlier_decisions={str(path): base.digest(path) for path in CARRIES})
    if MANUSCRIPT.exists():
        assert doc == base.load(MANUSCRIPT)
    else:
        base.save(MANUSCRIPT, doc)
    return doc


def rebuild_function():
    rebuild = modal_writer.rebuild_function({})
    env = rebuild.__globals__.copy()
    styles = env["changed_styles"]
    env["changed_styles"] = FunctionType(styles.__code__, styles.__globals__ | {"plan_progressive": previous.plan_progressive})
    return FunctionType(rebuild.__code__, env)


def main():
    manuscript = combined_manuscript()
    assert all(row["decision"] == "retention" for row in manuscript["records"] if row["source_selector"] in (None, 254))
    source = checked_text(previous.compiler.source, {
        "    assert groups.keys() == packet_groups.keys()":
            "    empty = [key for key, item in packet_groups.items() if not item['records']]\n"
            "    assert empty == [('/data/SC0.DK4', 231)]\n"
            "    groups[empty[0]] = []\n"
            "    assert groups.keys() == packet_groups.keys()",
        "    painter = stage.system.native_painter(ctx)": "    painter = None",
    })
    scope = previous.compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS),
    )
    exec(compile(source, __file__ + "::registered-story-objects", "exec"), scope)
    scope["main"]()
    plan = base.load(STYLE_PREFLIGHT)
    original_draft = paired.ROOT / "contextual_decisions_B221_B224_v3.json"
    assert plan["draft_sha256"] == base.digest(original_draft) and plan["candidate_sha256"] == manuscript["previous_sha256"]
    for draft in (base.load(original_draft), base.load(first.OUTPUT)):
        assert [r for r in draft["records"] if r["kind"] == "actor-style"] == [
            r for r in manuscript["records"] if r["block"] == 221 and r["kind"] == "actor-style"]
    objects = {command["source_offset"]: command for group in base.load(PROOF)["groups"]
               if group["block"] == 221 for command in group["commands"] if command["word"] == 0x4100}
    for row in plan["style_objects"]:
        assert objects[row["command_offset"]]["stored"] == row["compiled_hex"]


if __name__ == "__main__":
    main()
