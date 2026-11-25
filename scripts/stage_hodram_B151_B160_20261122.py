"""Stage Hodram's retirement, farewell and four recruitment scenes."""

from collections import Counter
from types import SimpleNamespace

from scripts import preflight_hodram_B156_farewell_20261122 as farewell
from scripts import register_hodram_B131_B150_20261122 as parent
from scripts import review_hodram_B151_B155_20261122 as first
from scripts import review_hodram_B157_B158_20261122 as recruits
from scripts import review_hodram_B159_B160_20261122 as previous
from scripts import stage_hodram_B131_B150_20261122 as staging


base, native, compiler, TOKEN = staging.base, staging.native, staging.compiler, staging.TOKEN
modal, ARCHIVE, logical_end = staging.modal, staging.ARCHIVE, staging.logical_end
paired = previous.paired
ROOT = paired.ROOT / "B151_B160_staged_v3"
SOURCE, OUTPUT = paired.PACKET, paired.ROOT / "B151_B160_scoped_manuscript_v4.json"
ROM, PROOF = ROOT / "Hodram_B151_B160_STAGED.nds", ROOT / "stored_proof.json"
BLOCKS = ((), tuple(paired.BLOCKS), (), ())
DEFAULT_NAMES = staging.DEFAULT_NAMES
DRAFTS = [first.OUTPUT, farewell.REFINED, recruits.OUTPUT, previous.OUTPUT]
REFINEMENTS = {
    "151_R0013": (None, ["knife fits", "the sheath..."]),
    "153_R0034": (None, ["find the Proof", "without delay."]),
    "155_R0033": ("Sure. Do you know anything about it?", []),
    "156_R0014": (
        "You're now supreme naval commander. I expect our navy to grow even stronger under your command.",
        ["You're now supreme naval commander.", "under your command."],
    ),
    "156_R0157": (None, ["made to live", "at sea."]),
    "157_R0034": (None, ["perfect bodyguard,", "with a crew.", "with others."]),
    "157_R0086": (None, ["you've got?", "just fired you?"]),
    "158_R0022": ("Hold on. I'm this ship's captain. FI FA.", ["FI FA."]),
    "158_R0086": ("No way... I've never lost before.", []),
    "158_R0181": (None, ["picked it up"]),
    "159_R0044": (None, ["table over there."]),
    "159_R0058": ("A pretty one, aren't you? Huh?", ["A pretty one, aren't you?"]),
    "160_R0013": ("Here you go. That's how much.", []),
    "160_R0123": ("That man never listens to me. If you hadn't spoken up yesterday...", ["never listens to me."]),
    "160_R0219": (
        "My daughter got sick first, during an outbreak. I was so caught up in work... I didn't take proper care of her.",
        ["My daughter got sick first,", "during an outbreak.", "proper care of her."],
    ),
    "160_R0230": (
        "...I'd put work ahead of my family. It felt hollow in the end. Now I'm more concerned with people's health than with business.",
        [],
    ),
    "160_R0237": (None, ["going home?"]),
}
WRAPS = {
    "158_R0195": (
        "More cargo holds won't help much in Europe. It's hard to get market share there, and you can't trade in bulk without it.",
        ["market share", "trade in bulk"],
        "Julio explains why extra capacity cannot overcome limited access to Europe's market. Put the quantity restriction with its cause in one readable page.",
    ),
}


def apply_wraps(row):
    short = row["id"].partition("_B")[2]
    if short in REFINEMENTS:
        wording, phrases = REFINEMENTS[short]
        assert row["decision"] == "revision"
        row["english"] = wording or row["english"]
        row["protected_phrases"] = phrases
        row["layout_refinement"] = "Adjusted phrase protection after the width check."
    if short in WRAPS:
        wording, phrases, reason = WRAPS[short]
        assert row["decision"] == "retention"
        row.update(decision="revision", change_class="wording", english=wording, protected_phrases=phrases,
                   prior_retention_note=row["localization_note"], localization_note=reason)


def collect():
    packet, carry, release = map(base.load, (SOURCE, paired.CARRY, parent.RELEASE))
    assert base.digest(parent.ROM) == packet["candidate_sha256"] == release["candidate_sha256"] == carry["candidate_sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert not carry["reused_records"] and carry["source_packet_sha256"] == base.digest(SOURCE)
    drafts = list(map(base.load, DRAFTS))
    assert all(doc["source_packet_sha256"] == base.digest(SOURCE) for doc in drafts)
    rows = {row["id"]: row for doc in drafts for row in doc["records"]}
    assert len(rows) == sum(len(doc["records"]) for doc in drafts) == 331

    placement = base.load(farewell.OUT)
    assert placement["candidate_sha256"] == release["candidate_sha256"]
    assert placement["manuscript_sha256"] == base.digest(farewell.REFINED)
    fe = placement["records"]
    image = base.NdsImage.open(parent.ROM)
    painter = modal.prior.town.current_fe_painter(SimpleNamespace(image=image, arm=image.read_file(native.ARM)))
    ordered = []
    for group in packet["groups"]:
        for original in group["records"]:
            row = rows.pop(original["id"])
            assert all(row[key] == value for key, value in original.items())
            apply_wraps(row)
            if row["source_selector"] == 254 and row["block"] == 156 and row["decision"] == "retention":
                row["formatting_retention_reason"] = (
                    "Keep the authored lead rows, speaker markers and offsets in the farewell and ending. "
                    "They distinguish staged turns and asides from the ordinary portrait dialogue."
                )
            if row["source_selector"] == 254 and row["decision"] == "revision" and row["id"] not in fe:
                assert row["block"] == 160
                raw = bytes.fromhex(row["current_hex"])[1:]
                body, expected, cells, raster = modal.plan(row | {"source_record_index": -1}, raw, painter)
                fe[row["id"]] = dict(compiled_hex=body.hex(), expected_hex=(b"\xfe" + expected).hex(),
                                     rows=cells, plane_sha256=native.digest(raster))
            ordered.append(row | {"route": 1})
    assert not rows and len(fe) == 6
    findings = dict(Counter(row["change_class"] for row in ordered))
    doc = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
               target_locale="en-US", review_gates=drafts[0]["review_gates"],
               previous_sha256=release["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
               source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE), records=ordered,
               findings=findings, planned_FE=fe,
               source_and_draft_evidence={str(path): base.digest(path) for path in [*DRAFTS, farewell.OUT]},
               contextual_records_revisited=len(ordered), contextual_decisions_reused=0, new_editorial_credit=0,
               status="Prose reviewed. Stored native, visual and focused gameplay gates pending.")
    return doc


def main():
    assert not PROOF.exists()
    draft = collect()
    if OUTPUT.exists():
        assert base.load(OUTPUT) == draft
    else:
        base.save(OUTPUT, draft)
    print(draft["findings"], flush=True)
    scope = compiler.env | globals() | dict(
        review=SimpleNamespace(OUTPUT=OUTPUT, SOURCE=SOURCE),
        paired=SimpleNamespace(BLOCKS=BLOCKS), draft=draft, assemble=staging.assemble,
    )
    exec(compile(staging.program, __file__ + "::stored-script-and-inverse", "exec"), scope)
    scope["main"]()
    stored = base.load(PROOF)
    assert stored["whole_parent_inverse"] and len(stored["groups"]) == len(BLOCKS[1])
    assert stored["changed_blocks"] == {ARCHIVE: sorted({r["block"] for r in draft["records"] if r["decision"] == "revision"})}


if __name__ == "__main__":
    main()

