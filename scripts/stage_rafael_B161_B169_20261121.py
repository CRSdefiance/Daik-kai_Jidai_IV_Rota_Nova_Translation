"""Compile Rafael's reviewed B161–169 exchanges with the existing story writer."""

from collections import Counter
from dataclasses import replace
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_B161_B169_FE_20261121 as panels
from scripts import review_rafael_east_asia_followup_20261121 as width
from scripts import stage_rafael_followup_encounters_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = panels.base, panels.native, panels.parent
compiler = precedent.compiler
SOURCE = panels.PAIRS
MANUSCRIPT = panels.ROOT / "contextual_manuscript_B161_B169_v4.json"
ROOT = panels.ROOT / "staged_B161_B169_v3"
ROM, PROOF = ROOT / "Rafael_B161_B169_STAGED.nds", ROOT / "stored_proof.json"
FE_PROOF = panels.OUT / "native_speakerless_preflight.json"
EARLIER = Path("translations/rafael_B161_B165_integrated_final_review_v1.json")
DRAFTS = [panels.ROOT / f"B{i}_contextual_decisions_final_candidate.json" for i in range(161, 166)]
DRAFTS += [panels.DRAFTS[1], panels.ROOT / "B167_B169_contextual_decisions_v2_final_candidate.json"]
BLOCKS = (tuple(range(161, 170)), (), (), ())
TOKEN = width.TOKEN
MAX_FU_CELLS = 33
review = SimpleNamespace(OUTPUT=MANUSCRIPT, SOURCE=SOURCE)

WRAP_FIXES = {
    "DK4_MES_B161_R0062": (["with FI, would I?", "teamed up"],
        "Keep Claudio's question tag with the named person and use three rows in place of four."),
    "DK4_MES_B163_R0051": (["from the Brass Lamp", "reveal the markings."],
        "Use the opening row for the complete thought about heat and keep the reveal together."),
    "DK4_MES_B165_R0016": (["seven Proofs of Conquest", "scattered across the world.",
        "we can ask him to recognize", "the Portuguese Crown again."],
        "End the first page on the full condition and start the second page with its consequence."),
    "DK4_MES_B168_R0037": (["What's got you so mad?", "trouble with muscleheads."],
        "Use two rows and keep the punch line together."),
    "DK4_MES_B169_R0110": (["ways to deal with a customer", "without drawing a sword.", "There are"],
        "Bring the customer phrase onto the same line and keep the contrast with drawing a sword."),
}


def full_name_planner():
    source = checked_text(width.company_source, {
        '.replace("{MACRO:FO}", "W" * MAX_COMPANY_CELLS))':
            '.replace("{MACRO:FO}", "W" * MAX_COMPANY_CELLS)\n'
            '                    .replace("{MACRO:FU}", "W" * 16 + " " + "W" * 16))',
    })
    scope = width.company_scope.copy()
    default_planner = scope["PLANNER"]
    get_profile = default_planner.__globals__["get_dialogue_profile"]

    def profile(name):
        original = get_profile(name)
        # Match the registered default Rafael Castor expansion for pair phase.
        return replace(original, macro_ascii_lengths=original.macro_ascii_lengths | {"FU": 13},
            macro_widths=original.macro_widths | {"FU": 13 * 6})

    scope["PLANNER"] = FunctionType(default_planner.__code__,
        default_planner.__globals__ | {"get_dialogue_profile": profile})
    exec(compile(source, __file__ + "::full-name-width", "exec"), scope)
    return scope["plan_progressive"]


def plan_progressive(row, selector, old, original):
    tokens = TOKEN.findall(row["english"])
    planner = full_name_planner() if "FU" in tokens else width.plan_progressive
    body, plan = planner(row, selector, old, original)
    assert TOKEN.findall(body.decode("ascii")) == tokens
    assert len(plan["lines"]) <= 4 * (1 + old.count(b"\n") // 4)
    if "FU" in tokens:
        assert plan["lines"][0] == "{MACRO:FU}."
        plan["maximum_expanded_FU_length"] = MAX_FU_CELLS
    return body, plan


def qualified_panels():
    data = base.load(FE_PROOF)
    assert data["parent_sha256"] == base.digest(parent.ROM)
    assert all(base.digest(path) == digest for path, digest in data["evidence"].items())
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in data["sheets"])
    return {r["id"]: r for r in data["records"]}


def exact_body(member, group, pair, side):
    reference = member[side + "_reference"]
    assert reference["offset"] == pair[side + "_offset"]
    assert reference["command_offset"] == pair[side + "_command_offset"]
    assert reference["block_sha256"] == group[side + "_block_sha256"]
    assert reference["archive_sha256"] == group[side + "_archive_sha256"]
    assert reference["exact_body_hex"] == pair[side + "_body_hex"]
    return bytes([pair["selector"]]).hex() + reference["exact_body_hex"]


def prepare(fe):
    packet, release, earlier = map(base.load, (SOURCE, parent.RELEASE, EARLIER))
    source_sha = base.digest(SOURCE)
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert tuple(g["block"] for g in packet["groups"]) == BLOCKS[0]
    glossary = {r["id"]: r for r in earlier["records"]}
    rows = {}
    for group in packet["groups"]:
        for pair in group["records"]:
            ident = f'DK4_MES_B{group["block"]}_R{pair["source_record_index"]:04d}'
            assert pair["native_command_word"] == 0x4000 and not pair["slots"] and ident not in rows
            rows[ident] = (group, pair)
    prepared = []
    for path in DRAFTS:
        draft = base.load(path)
        assert draft["paired_source_sha256"] == source_sha and draft["candidate_sha256"] == packet["candidate_sha256"]
        assert draft["translation_policy"] == "natural-dialogue-v2" and draft["target_locale"] == "en-US"
        for member in draft["records"]:
            ident = member["id"]
            group, pair = rows.pop(ident)
            assert member["Japanese"] == pair["Japanese"]
            assert member["source_selector"] == pair["selector"]
            assert member["block"] == pair["block"] and member["file_path"] == pair["file_path"]
            assert {key for key, value in member["review"].items() if value} == {
                "source", "context", "localization", "naturalness"}
            source, current = [exact_body(member, group, pair, side) for side in ("source", "current")]
            panel = pair["selector"] == 254
            row = member | dict(route=0, source_hex=source, current_hex=current,
                native_command_word=pair["native_command_word"], native_slots=pair["slots"],
                kind="system-FE" if panel else "progressive", protected_phrases=member.get("protected_phrases", []),
                finding=member["localization_note"])
            if ident in glossary:
                old = glossary.pop(ident)
                assert old["source_hex"] == source
                row["source_meaning"] = old["source_meaning"]
            if ident == "DK4_MES_B166_R0072":
                assert row["english"] == "I'm FU, and I've returned to my homeland, Portugal."
                row.update(english="FU. I've returned to my homeland, Portugal.",
                    protected_phrases=["I've returned", "my homeland, Portugal."],
                    finding="Rafael states his full name on its own as in the Japanese, then formally announces his return to Portugal.")
                row["localization_note"] = row["finding"]
            if ident == "DK4_MES_B166_R0085":
                row.update(english="I hear the Pope will press for Portugal's Crown to be recognized again if we show him the seven Proofs of Conquest you found.",
                    protected_phrases=["seven Proofs of Conquest", "recognized again"],
                    finding="The King reports what he has heard about the Pope pressing for renewed recognition of the Portuguese Crown, conditional on showing him the seven Proofs Rafael gathered.")
                row["localization_note"] = row["finding"]
            if ident in WRAP_FIXES:
                assert row["decision"] == "retention" and row["english"] == row["previous_English"]
                phrases, finding = WRAP_FIXES[ident]
                row.update(decision="revision", change_class="wrap-only", protected_phrases=phrases,
                           finding=finding, prose_retention_reason=row["localization_note"])
            if ident == "DK4_MES_B167_R0005":
                row["formatting_retention_reason"] = "The established four rows give Al two complete opening statements and keep each of his paired objections intact. Compiling with both phrases protected gives the same stored bytes."
            if ident == "DK4_MES_B167_R0180":
                row.update(decision="revision", english="He looks so strong! I'd want someone like him on our side. I'd hate to be up against him.",
                    protected_phrases=["on our side.", "I'd hate to be up against him."],
                    finding="Rafael's enthusiasm makes a blunt distinction between an ally and an enemy. Keep the last thought together before Claudio calls him simple.")
                row["localization_note"] = row["finding"]
            if ident == "DK4_MES_B168_R0214":
                row.update(decision="revision", english="Buying a ship gives you more cargo space. But market share is hard to come by in Europe, so you can't trade in bulk.",
                    protected_phrases=["more cargo space", "market share", "trade in bulk."],
                    finding="Julio distinguishes spare cargo capacity from the market share needed to trade goods in bulk. The revision also removes the sparse rows from the old layout.")
                row["localization_note"] = row["finding"]
            assert row["source_meaning"] and row["finding"]
            source_tokens = TOKEN.findall(row["Japanese"])
            assert TOKEN.findall(row["english"]) == TOKEN.findall(row["previous_English"]) == source_tokens
            if panel:
                proof = fe[ident]
                assert (proof["decision"], proof["english"], proof["source_reference"], proof["current_reference"]) == (
                    row["decision"], row["english"], row["source_reference"], row["current_reference"])
                row["panel_preflight"] = proof["compiled_hex"]
            prepared.append(row)
    assert not rows and not glossary
    counts = Counter(row["decision"] for row in prepared)
    assert counts == {"revision": 102, "retention": 266}
    assert sum(row.get("change_class") == "wrap-only" for row in prepared) == len(WRAP_FIXES)
    data = dict(translation_policy="natural-dialogue-v2", encoder="registered-native-story-objects", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"],
        status="contextual review complete, with stored and gameplay display checks pending",
        previous_sha256=packet["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE), source_packet_sha256=source_sha, records=prepared,
        source_and_draft_evidence={str(p): base.digest(p) for p in [EARLIER, FE_PROOF, *DRAFTS]},
        findings=dict(counts, wrap_only=len(WRAP_FIXES)), new_editorial_credit=0)
    if MANUSCRIPT.exists():
        assert base.load(MANUSCRIPT) == data
    else:
        base.save(MANUSCRIPT, data)


def rebuild_function(fe):
    rebuild = compiler.rebuild_function()
    env = rebuild.__globals__ | {"plan_progressive": plan_progressive}

    def plan_fe(row, _):
        proof = fe[row["id"]]
        assert row["panel_preflight"] == proof["compiled_hex"]
        raw = bytes.fromhex(proof["compiled_hex"])
        assert raw[0] == 254
        return raw[1:], dict(encoded_hex=raw.hex(), expected_native_pages=1,
            planned_visible_rows=proof["rows"], expected_stored_hex=proof["expected_stored_hex"])

    env["plan_fe"] = plan_fe
    env["changed_speech"] = FunctionType(env["changed_speech"].__code__, env)
    return FunctionType(rebuild.__code__, env)


def main():
    fe = qualified_panels()
    prepare(fe)
    source = checked_text(compiler.source, {
        "    painter = stage.system.native_painter(ctx)": "    painter = None  # qualified speakerless renders are checked in rebuild",
        "    rebuild = rebuild_function()": "    rebuild = rebuild_function(fe)",
    })
    scope = compiler.env | globals() | dict(paired=SimpleNamespace(BLOCKS=BLOCKS), fe=fe)
    exec(compile(source, __file__ + "::stored-script-and-inverse", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    for group in stored["groups"]:
        for cmd in group["commands"]:
            for ident in cmd["record_ids"]:
                if ident in fe:
                    raw = bytes.fromhex(fe[ident]["expected_stored_hex"])
                    whole = bytes.fromhex(cmd["stored"])
                    assert whole[5:5 + len(raw)] == raw and not any(whole[5 + len(raw):])


if __name__ == "__main__":
    main()
