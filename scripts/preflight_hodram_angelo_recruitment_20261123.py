"""Check Angelo's dialogue proposals with the registered progressive renderer."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import pair_hodram_angelo_recruitment_20261123 as paired
from scripts import review_current_story_wraps_20261122 as established
from scripts import stage_hodram_and_lil_followups_20261122 as review

base, parent = paired.base, paired.release
ROOT = paired.OUTPUT.parent / "angelo_preflight"
REVIEW, PREFLIGHT = (ROOT / name for name in ("contextual_review.json", "native_preflight.json"))
MANUSCRIPT = Path(__file__).with_name("hodram_angelo_recruitment_20261123.md")


def prepare():
    packet = base.load(paired.OUTPUT)
    release = base.load(parent.RELEASE)
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["clean_sha256"] == release["clean_input_sha256"]
    load = FunctionType(review.load_sections.__code__,
        review.load_sections.__globals__ | dict(MANUSCRIPTS=(MANUSCRIPT,)))
    sections = load()
    context, decisions = sections.pop((1, 158))
    assert not sections
    group = packet["group"]
    records = []
    for row in group["records"]:
        ordinal, selector = row["source_record_index"], row["selector"]
        assert row["native_command_word"] == 0x4000 and selector < 207
        before = " ".join(row["current_English"].split())
        fields = decisions.pop(ordinal)
        if len(fields) == 2:
            meaning, note = fields
            text, phrases = before, []
        else:
            meaning, text, protection, note = fields
            phrases = protection.split(";")
            assert text.isascii() and text != before
            assert all(phrase in text and len(phrase) <= 36 for phrase in phrases)
        change = "prose" if text != before else "retention"
        source, current = (review.reference(group, row, side) for side in ("source", "current"))
        current["candidate_sha256"] = packet["candidate_sha256"]
        control = bytes([selector]).hex()
        records.append(dict(id=row["id"], route=1, block=158, file_path=group["file_path"],
            source_selector=selector, kind="progressive", speaker=row["speaker"], context=context,
            source_meaning=meaning, Japanese=row["Japanese"], previous_English=before, english=text,
            protected_phrases=phrases, source_reference=source, current_reference=current,
            source_hex=control + source["exact_body_hex"], current_hex=control + current["exact_body_hex"],
            change_class=change, decision="revision" if change == "prose" else "retention",
            localization_note=note, review=dict(source=True, context=True, localization=True, naturalness=True,
                formatting=False)))
    assert not decisions and len(records) == 44
    revised = {row["id"] for row in records if row["decision"] == "revision"}
    assert {row["id"] for row in packet["ordinary_Istanbul_display_leads"]} <= revised
    ROOT.mkdir(parents=True, exist_ok=True)
    scope = dict(route=1, block=158, file_path=group["file_path"], context=context,
        record_ids=[row["id"] for row in records], source_block_sha256=group["source_block_sha256"],
        current_block_sha256=group["current_block_sha256"])
    base.save(REVIEW, dict(candidate_sha256=packet["candidate_sha256"], clean_sha256=packet["clean_sha256"],
        groups=[scope], records=records, counts=Counter(row["change_class"] for row in records),
        manuscripts_sha256={str(MANUSCRIPT): base.digest(MANUSCRIPT)},
        source_packet_sha256=base.digest(paired.OUTPUT), translation_policy="natural-dialogue-v2",
        target_locale="en-US", stored_and_native_verification_of_changes_pending=True))


def main():
    assert not PREFLIGHT.exists()
    prepare()
    renderer = FunctionType(established.preflight.__code__,
        established.preflight.__globals__ | dict(parent=parent, REVIEW=REVIEW, PREFLIGHT=PREFLIGHT, ROOT=ROOT))
    renderer()


if __name__ == "__main__":
    main()
