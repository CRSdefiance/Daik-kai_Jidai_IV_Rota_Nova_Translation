"""Review and stage the source-bound Hodram exchanges with native wrapping."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import re
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_late_midroute_wraps_20261123 as paired
from scripts import register_rafael_remaining_wraps_20261123 as registered
from scripts import review_current_story_wraps_20261122 as native_review
from scripts import stage_current_story_wraps_20261122 as compiler
from scripts.stage_hodram_and_lil_followups_20261122 import reference


base, native = paired.base, paired.native
BATCH = Path(".codex-release-work/hodram_late_midroute_wraps_20261123/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_Late_Midroute_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
MANUSCRIPT = paired.OUTPUT.with_name("working_review.md")
ARCHIVE = paired.ARCHIVE
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
parent = SimpleNamespace(ROM=registered.ROM, MANIFEST=registered.MANIFEST, RELEASE=registered.RELEASE,
    STARTUP_CAPTURE=registered.STARTUP_CAPTURE, guard_spec=registered.guard_spec,
    bind_registered_story_percent_guard=registered.bind_registered_story_percent_guard)
PROTECTION = {
    (141, 44): ["who's in charge", "threatened and shaken down"],
    (142, 8): ["safe in town", "slave traders", "in front of a crowd"],
    (142, 126): ["Maybe there's a reason you met.", "Why not let her stay with you?"],
    (142, 165): ["I'd better finish", "ready to sail"],
    (145, 29): ["your money ran out", "You see that now, don't you?"],
    (145, 36): ["start fresh"],
    (147, 8): ["I hadn't heard that before."],
    (148, 54): ["without a plan"],
    (150, 17): ["Tang Bamboo Craft"],
    (150, 72): ["on the back of the bamboo"],
    (156, 59): ["Your Majesty", "I know it's selfish", "I'd like to retire from the navy."],
    (160, 230): ["people's health"],
    (166, 17): ["It's so wide!"],
    (166, 46): ["lie around at sea", "It's scientifically impossible!"],
    (167, 145): ["two masts, others three", "A third mast", "more sail handlers"],
    (176, 42): ["the shops don't sell it", "Supposedly it's in Seoul."],
    (177, 39): ["'Your lips are like rose petals.'", "He knows how to flirt."],
    (178, 14): ["I kept my promise!", "Here's your Silla Gold Crown."],
    (178, 90): ["up to the work", "you can come aboard."],
}


def proposals():
    pattern = re.compile(r"\| B(\d+) R(\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|")
    rows = {}
    for line in MANUSCRIPT.read_text(encoding="utf-8").splitlines():
        if match := pattern.fullmatch(line):
            block, ordinal = map(int, match.group(1, 2))
            key = block, ordinal
            assert key not in rows
            rows[key] = tuple(field.strip() for field in match.group(3, 4, 5))
    assert len(rows) == 25 and PROTECTION.keys() <= rows.keys()
    return rows


def author():
    packet, release = map(base.load, (paired.OUTPUT, parent.RELEASE))
    candidate = packet["candidate_sha256"]
    assert candidate == release["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    for path, digest in packet["earlier_reviews"].items():
        assert base.digest(Path(path)) == digest

    edits = proposals()
    records, groups, captions, leads = [], [], [], set()
    for group in packet["groups"]:
        block, path = group["block"], group["file_path"]
        context = group["records"][0]["prior_context"]
        leads.update(row["id"] for row in group["open_wrap_leads"])
        ids = []
        for row in group["records"]:
            ident, selector = row["id"], row["selector"]
            before = " ".join(row["current_English"].split())
            source, current = [reference(group, row, key) for key in ("source", "current")]
            current["candidate_sha256"] = candidate
            key = block, row["source_record_index"]
            edit = edits.pop(key, None)
            meaning, english, note = edit or (row["prior_source_meaning"], before, row["prior_localization_note"])
            assert meaning and note and row["prior_context"] == context
            phrases = PROTECTION.get(key, [])
            gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
            entry = dict(id=ident, route=1, block=block, file_path=path, Japanese=row["Japanese"],
                speaker=row["speaker"], context=context, source_meaning=meaning, localization_note=note,
                source_reference=source, current_reference=current, prior_registered_review=row["prior_registered_review"],
                english=english, review=gates)
            if row["native_command_word"] == 0x2100:
                assert edit is None and block == 167
                slot, = row["slots"]
                captions.append(entry | dict(slot=slot, decision="retention"))
                continue
            assert row["native_command_word"] == 0x4000
            if edit is not None:
                assert selector != 254 and english.isascii()
                assert all(phrase in english and len(phrase) <= 36 for phrase in phrases)
            change = "retention" if edit is None else "wrap_only" if before == english else "prose"
            prefix = bytes([selector]).hex()
            records.append(entry | dict(source_selector=selector, kind="system" if selector == 254 else "progressive",
                previous_English=before, source_hex=prefix + source["exact_body_hex"],
                current_hex=prefix + current["exact_body_hex"], protected_phrases=phrases, change_class=change,
                decision="retention" if change == "retention" else "revision"))
            ids.append(ident)
        groups.append(dict(route=1, block=block, file_path=path, context=context, record_ids=ids,
            source_block_sha256=group["source_block_sha256"], current_block_sha256=group["current_block_sha256"]))
    counts = Counter(row["change_class"] for row in records)
    assert not edits and len(records) == 494 and len(captions) == 2 and len(groups) == 15
    assert sum(row["kind"] == "system" for row in records) == 50
    assert counts == {"retention":469, "wrap_only":1, "prose":24}
    assert len(leads) == 20 and leads <= {r["id"] for r in records if r["decision"] == "revision"}
    BATCH.mkdir(parents=True, exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=candidate, clean_sha256=packet["clean_sha256"], groups=groups,
        records=records, retained_choice_labels=captions, counts=counts, wrap_leads_covered=sorted(leads),
        source_packet_sha256=base.digest(paired.OUTPUT), manuscripts_sha256={str(MANUSCRIPT):base.digest(MANUSCRIPT)},
        exact_prior_registered_reviews=packet["earlier_reviews"], translation_policy="natural-dialogue-v2",
        target_locale="en-US", stored_and_native_verification_of_changes_pending=True))
    print(f"Reviewed {len(records)+len(captions)} texts across {len(groups)} exchanges. {dict(counts)}.")


def run(action):
    if action == "review":
        author()
    elif action == "preflight":
        settings = dict(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT, ROOT=BATCH, parent=parent)
        FunctionType(native_review.preflight.__code__, native_review.preflight.__globals__ | settings)()
    elif action in ("stage", "native_display"):
        scope = vars(compiler) | globals()
        scope["compilers"] = FunctionType(compiler.compilers.__code__, scope)
        FunctionType(getattr(compiler, action).__code__, scope)()
    else:
        inherited = getattr(compiler.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    run(cli.parse_args().action)
