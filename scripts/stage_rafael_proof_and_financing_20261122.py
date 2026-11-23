"""Stage the complete Proof briefing and Lisbon financing dialogue."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_athens_and_maria_crew_20261122 as checkpoint
from scripts import pair_rafael_proof_and_financing_20261122 as paired
from scripts import stage_rafael_athens_and_maria_crew_20261122 as template


base, native, established = paired.base, paired.native, template.established
registered = paired.release
parent = SimpleNamespace(
    ROM=registered.ROM, MANIFEST=registered.MANIFEST, RELEASE=registered.RELEASE,
    STARTUP_CAPTURE=registered.STARTUP_CAPTURE,
    guard_spec=registered.scope["guard_spec"],
    bind_registered_story_percent_guard=registered.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/rafael_proof_and_financing_20261122/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Proof_And_Lisbon_Financing_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_money_panel.json"
CHOICE_PROOF = ROOT / "unchanged_choice.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
MANUSCRIPTS = {41: paired.BRIEFING, 44: Path(__file__).with_name("rafael_lisbon_financing_20261122.md")}
CHOICE = (
    ("Choose to have Julio teach the preparations.", "Ask him. answers Janus's question directly and selects Julio's lesson."),
    ("State that Rafael can prepare independently.", "Prepare alone. identifies the independent option and leaves Julio's response in its original branch."),
)


def contextual_review():
    assert not REVIEW.exists()
    paired_source, active = map(base.load, (paired.OUTPUT, parent.RELEASE))
    candidate = base.digest(parent.ROM)
    assert paired_source["candidate_sha256"] == active["candidate_sha256"] == candidate
    assert paired_source["clean_sha256"] == active["clean_input_sha256"] == base.digest(native.CLEAN)
    assert paired_source["current_archive_sha256"] == active["target_SC0_sha256"]
    catalogue = base.load(template.review_scope["established"].CATALOGUE)["source_and_current_default_name_fields"]
    names = {r["actor_ID"]: r["progressive_nameplate"] for r in catalogue}
    records, groups, choices = [], [], []
    for block in paired_source["groups"]:
        number = block["block"]
        _, context, table = MANUSCRIPTS[number].read_text(encoding="utf-8").strip().split("\n\n", 2)
        rows = {}
        for line in table.splitlines():
            index, *values = line.split("|", 4)
            rows[int(index)] = values
        ids = []
        for reference in block["records"]:
            ident, selector = reference["id"], reference["source_selector"]
            source, current = [reference[side + "_reference"] | dict(
                file_path=paired.ARCHIVE, block=number, archive_sha256=paired_source[f"{side}_archive_sha256"],
                block_sha256=block[f"{side}_block_sha256"]) for side in ("source", "current")]
            current["candidate_sha256"] = candidate
            before = " ".join(reference["English"].split())
            if reference["opcode"] == 0x2100:
                slot, = reference["slots"]
                meaning, reason = CHOICE[slot]
                assert before == ("Ask him.", "Prepare alone.")[slot]
                choices.append(dict(id=ident, slot=slot, Japanese=reference["Japanese"], english=before,
                    context=context, source_meaning=meaning, localization_note=reason, source_reference=source,
                    current_reference=current, decision="retention",
                    review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
                continue
            assert reference["opcode"] == 0x4000 and selector <= 254
            meaning, replacement, protected, reason = rows.pop(int(ident.rsplit("R", 1)[-1]))
            english = replacement or before
            phrases = protected.split(";") if protected else []
            assert all(phrase in english and len(phrase) <= 36 for phrase in phrases), (ident, english, phrases)
            if not before.isascii():
                assert not replacement and before == " ".join(reference["Japanese"].split())
            change = "prose" if english != before else "wrap_only" if phrases else "retention"
            assert selector != 254 or change == "retention"
            prefix = bytes([selector]).hex()
            records.append(dict(id=ident, route=0, file_path=paired.ARCHIVE, block=number, source_selector=selector,
                kind="system" if selector == 254 else "progressive", speaker=names[selector] if selector != 254 else "System",
                context=context, source_meaning=meaning, Japanese=reference["Japanese"], previous_English=before,
                english=english, protected_phrases=phrases, source_reference=source, current_reference=current,
                source_hex=prefix+source["exact_body_hex"], current_hex=prefix+current["exact_body_hex"],
                change_class=change, decision="retention" if change == "retention" else "revision", localization_note=reason,
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=change=="retention")))
            ids.append(ident)
        assert not rows
        groups.append(dict(route=0, block=number, file_path=paired.ARCHIVE, context=context, record_ids=ids,
            source_block_sha256=block["source_block_sha256"], current_block_sha256=block["current_block_sha256"]))
    assert len(records) == 142 and len(choices) == 2
    found = {row["id"] for row in records if row["decision"] == "revision"}
    assert set(paired_source["known_wrap_leads"]) <= found
    counts = dict(Counter(row["change_class"] for row in records))
    BATCH.mkdir(parents=True, exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=candidate, clean_sha256=paired_source["clean_sha256"], groups=groups,
        records=records, retained_choice_labels=choices, counts=counts, translation_policy="natural-dialogue-v2",
        target_locale="en-US", source_pair_sha256=base.digest(paired.OUTPUT),
        wrap_queue_sha256=base.digest(checkpoint.QUEUE), stored_and_native_verification_of_changes_pending=True))
    print(f"Reviewed 142 spoken and system texts and both financing captions. {counts}", flush=True)


preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))
compiler_scope = template.compiler_scope | globals()
exec(compile(template.renderer_source, __file__ + "::Rafael-native-layouts", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        contextual_review()
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope[action]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
