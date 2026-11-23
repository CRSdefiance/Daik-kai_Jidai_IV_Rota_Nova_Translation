"""Stage Hodram's opening exchanges with the registered story compiler."""

from dataclasses import replace
from inspect import getsource
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts import review_hodram_opening_20261122 as author
from scripts import stage_hodram_alexandria_tutorial_20261121 as precedent
from scripts import stage_rafael_early_wraps_20261111 as layout
from scripts.source_locked_derivation_v5118 import checked_text


paired = author.paired
base, native, parent = paired.base, paired.native, paired.parent
compiler = precedent.compiler
SOURCE, ROOT = paired.PACKET, paired.ROOT / "staged"
ROM, PROOF = ROOT / "Hodram_B24_B53_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = paired.ROOT / "scoped_manuscript_v4.json"
BLOCKS = ((), tuple(author.DECISIONS), (), ())
TOKEN = author.precedent.TOKEN
logical_end = compiler.logical_end


def route_profile(name):
    base_profile = get_dialogue_profile(name)
    hodram = get_dialogue_profile("hodram-story-live")
    return replace(base_profile,
        macro_ascii_lengths=base_profile.macro_ascii_lengths | hodram.macro_ascii_lengths,
        macro_widths=base_profile.macro_widths | hodram.macro_widths)


def hodram_planner():
    original = layout.prior.layout

    def source(function):
        assert function is original.plan
        return checked_text(getsource(function), {
            "profile.macro_ascii_lengths['FA']==5 and profile.macro_widths['FA']==30":
            "profile.macro_ascii_lengths['FA']==9 and profile.macro_widths['FA']==54",
        })

    settings = SimpleNamespace(**(vars(original) | {"get_dialogue_profile": route_profile}))
    bind = FunctionType(layout.bind_planner.__code__, layout.bind_planner.__globals__ |
                        {"getsource": source, "prior": SimpleNamespace(layout=settings)})
    return bind()


PLANNER = hodram_planner()
plan_progressive = FunctionType(precedent.plan_progressive.__code__,
    precedent.plan_progressive.__globals__ | {"PLANNER": PLANNER})


def manuscript():
    draft, carry, source, release = map(base.load, (author.OUTPUT, paired.CARRY, SOURCE, parent.RELEASE))
    assert draft["source_packet_sha256"] == carry["source_packet_sha256"] == base.digest(SOURCE)
    assert draft["previous_sha256"] == carry["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    fresh = {row["id"]: row for row in draft["records"]}
    reused = {row["id"]: row for row in carry["reused_records"] if row["block"] in BLOCKS[1]}
    assert len(reused) == 2 and not fresh.keys() & reused.keys()
    rows = []
    for group in source["groups"]:
        if group["block"] not in BLOCKS[1]:
            continue
        for pair in group["records"]:
            ident = pair["id"]
            if ident in fresh:
                row = fresh.pop(ident)
                assert all(row[k] == v for k, v in pair.items())
            else:
                old = reused.pop(ident)
                assert all(old[k] == v for k, v in pair.items()) and all(old["prior_review_gates"].values())
                selector = pair["selector"]
                text = " ".join(pair["current_English"].split())
                row = pair | dict(kind="progressive", source_selector=selector, native_slots=[],
                    source_hex=f"{selector:02x}" + pair["source_reference"]["exact_body_hex"],
                    current_hex=f"{selector:02x}" + pair["current_reference"]["exact_body_hex"],
                    speaker=old["speaker"], english=text, previous_English=text, protected_phrases=[],
                    context=author.CONTEXTS[pair["block"]], localization_note=old["localization_note"],
                    source_meaning=old["source_meaning"], decision="retention", change_class="retention",
                    review=old["prior_review_gates"], earlier_contextual_decision=old)
            rows.append(row | {"route": 1})
    assert len(rows) == 120 and not fresh and not reused
    result = draft | dict(previous_registry_sha256=release["registry_sha256"], records=rows,
        contextual_records_revisited=118, contextual_decisions_reused=2,
        findings=draft["findings"] | {"retention": draft["findings"]["retention"] + 2})
    if OUTPUT.exists():
        assert base.load(OUTPUT) == result
    else:
        base.save(OUTPUT, result)
    return result


def main():
    draft = manuscript()
    program = checked_text(compiler.source, {
        '    painter = stage.system.native_painter(ctx)': '    painter = None',
        'for g in packet["groups"]}': 'for g in packet["groups"] if g["block"] in paired.BLOCKS[1]}',
    })
    rebuild = checked_text(getsource(compiler.rebuild_function), {
        "workflow.plan_progressive": "plan_progressive",
    })
    scope = compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=OUTPUT, SOURCE=SOURCE), paired=SimpleNamespace(BLOCKS=BLOCKS))
    exec(compile(rebuild, __file__ + "::writer", "exec"), scope)
    exec(compile(program, __file__ + "::store", "exec"), scope)
    scope["main"]()
    expected = sorted({row["block"] for row in draft["records"] if row["decision"] == "revision"})
    assert base.load(PROOF)["changed_blocks"] == {paired.ARCHIVE: expected}


if __name__ == "__main__":
    main()
