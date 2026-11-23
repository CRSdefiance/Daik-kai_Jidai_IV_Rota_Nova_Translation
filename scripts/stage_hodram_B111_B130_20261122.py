"""Compile the reviewed Hodram scenes with original menu and actor-style structure."""

from collections import Counter
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import compact_hodram_wraps_20261122 as compact
from scripts import pair_hodram_B111_B130_20261122 as paired
from scripts import register_hodram_B91_B110_20261122 as parent
from scripts import stage_hodram_B91_B110_20261122 as previous
from scripts import verify_hodram_B91_B110_20261122 as proof
from scripts.source_locked_derivation_v5118 import checked_text


base, native, compiler, TOKEN = previous.base, previous.native, previous.scope["compiler"], previous.TOKEN
SOURCE, ROOT = paired.PACKET, paired.ROOT / "B111_B130_staged_v3"
ROM, PROOF = ROOT / "Hodram_B111_B130_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = paired.ROOT / "B111_B130_scoped_manuscript_v3.json"
BLOCKS = ((), tuple(b for b in paired.BLOCKS if b != 128), (), ())
ARCHIVE = paired.pairing.ARCHIVE
logical_end = previous.logical_end
modal = proof.scope["modal"]
DRAFTS = [paired.ROOT / f"B{span}_contextual_v1.json" for span in (
    "111_B114", "115_B116", "117_B119", "120_B122", "123_B125", "126_B130")]
WRAPS = {
    "114_R0136": (["have a total of 32", "hands and feet", "How many are babies?"],
                  "Keep the puzzle's final question together after presenting the information."),
    "127_R0057": (["the best angle.", "Tap your flagship to stop."],
                  "Keep the stop instruction together after the explanation of automatic trim."),
    "127_R0061": (["on-screen speed meter.", "as long as possible."],
                  "Keep the meter's name and the visual cue for maximum speed intact."),
}
FE_WORDING = {
    "127_R0049": ("Use L and R to adjust the sails. Trim them for more speed.",
                  ["adjust the sails.", "Trim them for more speed."],
                  "Name both controls and explain why sail trim matters in two complete sentences."),
    "127_R0053": ("Press L to turn the sails left. Press R to turn them right.",
                  ["Press L to turn the sails left.", "Press R to turn them right."],
                  "Give each button and direction a full instruction of its own."),
}
REFINEMENTS = {
    "112_R0005": ("You're pilgrims, I take it? Please take a cross to remember your visit.",
                  ["You're pilgrims, I take it?", "to remember your visit."]),
    "114_R0197": (None, ["hands and feet", "The canes don't matter.", "Older people"]),
    "115_R0050": (None, ["the villagers", "to safety. Now!"]),
    "120_R0015": ("You're after that treasure, the Proof of Conquest, aren't you?", ["the Proof of Conquest, aren't you?"]),
    "120_R0036": (None, ["on the mainland.", "the divine winds."]),
    "120_R0039": (None, ["as his army,", "conquered the world."]),
    "122_R0042": (None, ["as an offering.", "meant a great deal"]),
    "123_R0092": ("If you hate every European and strike at random, you're no better than the people who hurt you. You're just as guilty.",
                  ["strike at random,", "people who hurt you.", "just as guilty."]),
    "123_R0124": (None, ["I wouldn't bluff about this.", "extended our reach", "to Africa.", "even beat them."]),
    "129_R0077": ("The new empire will rule the whole New World and hold all its trading rights. No one will trade here without our permission.",
                  ["the whole New World", "all its trading rights.", "without our permission."]),
}


def contents():
    a = base.load(SOURCE)
    carry = base.load(paired.CARRY)
    registered = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == a["candidate_sha256"] == carry["candidate_sha256"] == registered["candidate_sha256"]
    assert registered["registry_sha256"] == base.digest(base.REGISTRY)
    assert not carry["reused_records"] and carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(d["source_packet_sha256"] == base.digest(SOURCE) for d in drafts)
    by_id = {r["id"]: r for d in drafts for r in d["records"]}
    assert len(by_id) == sum(len(d["records"]) for d in drafts) == 323
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image,arm=image.read_file(native.ARM)))
    records, wraps, considered = [], {}, set()
    for group in a["groups"]:
        for pair in group["records"]:
            ident = pair["id"]
            row = by_id.pop(ident)
            assert all(row[k] == v for k,v in pair.items())
            if row["kind"] == "actor-style":
                row["speaker"] = "Runtime-selected crew member"
            short = ident.partition("_B")[2]
            if short in WRAPS or short in FE_WORDING:
                considered.add(short)
                wording, phrases, reason = FE_WORDING[short] if short in FE_WORDING else (None, *WRAPS[short])
                change = "wording" if wording else "wrap-only"
                assert row["decision"] == "retention" and row["source_selector"] == 254
                raw = bytes.fromhex(row["current_hex"])[1:]
                template = row | {"source_record_index": -1, "protected_phrases": phrases,
                                  "english": wording or row["english"]}
                compiled, final, rows, raster = modal.plan(template, raw, painter)
                if final != raw:
                    row.update(decision="revision", change_class=change, english=template["english"],
                               protected_phrases=phrases, previous_wrap_reason=row["localization_note"],
                               localization_note=reason)
                    wraps[ident] = dict(compiled_hex=compiled.hex(), expected_hex=(b"\xfe" + final).hex(),
                                       rows=rows, plane_sha256=native.digest(raster))
                else:
                    row["formatting_retention_reason"] = reason + " The native layout already does this."
            if short in REFINEMENTS:
                wording, phrases = REFINEMENTS[short]
                assert row["decision"] == "revision"
                if wording:
                    row["english"] = wording
                assert all(phrase.casefold() in row["english"].casefold() for phrase in phrases)
                row["protected_phrases"] = phrases
                row["layout_refinement"] = "Refined phrase boundaries after the first width check."
            records.append(row | {"route": 1})
    assert not by_id and considered == WRAPS.keys() | FE_WORDING.keys()
    findings = dict(Counter(row["change_class"] for row in records))
    assert findings == {"retention": 253, "wording": 65, "glyph": 2, "wrap-only": 3}
    doc = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
               review_gates=drafts[0]["review_gates"], previous_sha256=registered["candidate_sha256"],
               previous_registry_sha256=registered["registry_sha256"], source_packet=str(SOURCE),
               source_packet_sha256=base.digest(SOURCE), records=records, findings=findings, planned_FE=wraps,
               source_and_draft_evidence={str(path): base.digest(path) for path in DRAFTS},
               contextual_records_revisited=323, contextual_decisions_reused=0, new_editorial_credit=0,
               status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")
    if OUTPUT.exists():
        assert base.load(OUTPUT) == doc
    else:
        base.save(OUTPUT, doc)
    return doc


def assemble(wraps):
    builder = compiler.rebuild_function()
    env = builder.__globals__.copy()

    def plan_progressive(row, selector, old, original):
        picker = previous.scope["plan_progressive"] if "FO" in TOKEN.findall(row["english"]) else compact.qualified_plan
        return picker(row, selector, old, original)

    def plan_fe(row, painter):
        fit = wraps[row["id"]]
        body = bytes.fromhex(fit["compiled_hex"])
        stored = fit["expected_hex"]
        return body, dict(encoded_hex="fe" + body.hex(), expected_native_pages=1,
                         planned_visible_rows=fit["rows"], expected_stored_hex=stored)

    env.update(plan_progressive=plan_progressive, plan_fe=plan_fe)
    for name in ("changed_speech", "changed_styles"):
        env[name] = FunctionType(env[name].__code__, env)
    return FunctionType(builder.__code__, env)


def main():
    assert not PROOF.exists()
    draft = contents()
    program = checked_text(compiler.source, {
        '    painter = stage.system.native_painter(ctx)': '    painter = None',
        '    rebuild = rebuild_function()': '    rebuild = assemble(draft["planned_FE"])',
        'for g in packet["groups"]}': 'for g in packet["groups"] if g["block"] in paired.BLOCKS[1]}',
    })
    scope = compiler.env | globals() | dict(review=SimpleNamespace(OUTPUT=OUTPUT,SOURCE=SOURCE),
                                           paired=SimpleNamespace(BLOCKS=BLOCKS),draft=draft)
    exec(compile(program, __file__ + "::stored-script-and-inverse", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == len(BLOCKS[1])
    assert stored["changed_blocks"] == {ARCHIVE: sorted({r["block"] for r in draft["records"] if r["decision"]=="revision"})}
    print(draft["findings"])


if __name__ == "__main__":
    main()

