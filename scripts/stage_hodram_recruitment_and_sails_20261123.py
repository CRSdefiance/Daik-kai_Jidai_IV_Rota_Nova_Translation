"""Review and stage the six paired exchanges with the existing native compiler."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import pair_hodram_recruitment_and_sails_20261123 as paired
from scripts import preflight_hodram_angelo_recruitment_20261123 as angelo
from scripts import review_current_story_wraps_20261122 as layout
from scripts import stage_current_story_wraps_20261122 as compiler
from scripts import stage_hodram_and_lil_followups_20261122 as editorial
from scripts import stage_rafael_fleet_and_crew_exchanges_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

base, native, established, parent = paired.base, paired.native, compiler, paired.release
typed = precedent.typed
BATCH = Path(".codex-release-work/hodram_recruitment_and_sails_20261123/final")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_Recruitment_And_Sails_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
MANUSCRIPT = Path(__file__).with_name("hodram_recruitment_and_sails_20261123.md")
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)


def author():
    packet = base.load(paired.OUTPUT)
    registered = base.load(parent.RELEASE)
    assert packet["candidate_sha256"] == registered["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["clean_sha256"] == registered["clean_input_sha256"]
    reusable, earlier_plans = map(base.load, (angelo.REVIEW, angelo.PREFLIGHT))
    assert earlier_plans["draft_sha256"] == base.digest(angelo.REVIEW) and not earlier_plans["pending"]
    assert reusable["source_packet_sha256"] == base.digest(angelo.paired.OUTPUT)
    assert reusable["candidate_sha256"] == packet["candidate_sha256"]
    assert all(base.digest(path) == digest for path, digest in reusable["manuscripts_sha256"].items())
    parser_source = checked_text(getsource(editorial.load_sections), {
        "                assert int(key) not in rows\n                rows[int(key)] = fields":
            "                key = int(key) if key.isdecimal() else key\n"
            "                assert key not in rows\n                rows[key] = fields",
    })
    parser_scope = dict(MANUSCRIPTS=(MANUSCRIPT,), re=editorial.re)
    exec(compile(parser_source, __file__ + "::manuscript", "exec"), parser_scope)
    sections = parser_scope["load_sections"]()
    groups, records, captions = list(reusable["groups"]), list(reusable["records"]), []
    for group in packet["groups"]:
        block = group["block"]
        if block == 158:
            assert [row["id"] for row in group["records"]] == groups[0]["record_ids"]
            continue
        context, decisions = sections.pop((1, block))
        record_ids = []
        for row in group["records"]:
            ident, selector, ordinal = (row[key] for key in ("id", "selector", "source_record_index"))
            before = " ".join(row["current_English"].split())
            source, current = (editorial.reference(group, row, key) for key in ("source", "current"))
            current["candidate_sha256"] = packet["candidate_sha256"]
            gates = dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
            shared = dict(id=ident, Japanese=row["Japanese"], context=context, source_reference=source,
                          current_reference=current, review=gates)
            if row["native_command_word"] == 0x2100:
                slot, = row["slots"]
                meaning, note = decisions.pop(f'{row["source_command_offset"]}.{slot}')
                captions.append(shared | dict(slot=slot, english=before, decision="retention",
                    source_meaning=meaning, localization_note=note))
                continue
            assert row["native_command_word"] == 0x4000
            fields = decisions.pop(ordinal)
            if len(fields) == 2:
                meaning, note = fields
                text, phrases = before, []
            else:
                meaning, text, protection, note = fields
                phrases = protection.split(";")
                assert text.isascii() and selector != 254
                assert all(phrase in text and len(phrase) <= 36 for phrase in phrases)
            change = "prose" if text != before else "wrap_only" if phrases else "retention"
            record_ids.append(ident)
            control = bytes([selector]).hex()
            records.append(shared | dict(route=1, block=block, file_path=group["file_path"], source_selector=selector,
                kind="system" if selector == 254 else "progressive", speaker=row["speaker"], source_meaning=meaning,
                previous_English=before, english=text, protected_phrases=phrases, source_hex=control + source["exact_body_hex"],
                current_hex=control + current["exact_body_hex"], change_class=change,
                decision="retention" if change == "retention" else "revision", localization_note=note))
        assert not decisions
        groups.append(dict(route=1, block=block, file_path=group["file_path"], context=context, record_ids=record_ids,
            source_block_sha256=group["source_block_sha256"], current_block_sha256=group["current_block_sha256"]))
    assert not sections and len(records) == 194 and len(captions) == 2
    assert sum(row["source_selector"] == 254 for row in records) == 4
    leads = {row["id"] for group in packet["groups"] for row in group["open_wrap_leads"]}
    leads |= {row["id"] for key in ("ordinary_display_leads", "focused_display_leads") for row in packet[key]}
    assert leads <= {row["id"] for row in records if row["decision"] == "revision"}
    counts = Counter(row["change_class"] for row in records)
    BATCH.mkdir(parents=True, exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=packet["candidate_sha256"], clean_sha256=packet["clean_sha256"],
        groups=sorted(groups, key=lambda item: item["block"]), records=sorted(records, key=lambda row: (row["block"],
            row["source_reference"]["offset"])), retained_choice_labels=captions, counts=counts,
        wrap_leads_covered=sorted(leads), source_packet_sha256=base.digest(paired.OUTPUT),
        manuscripts_sha256=reusable["manuscripts_sha256"] | {str(MANUSCRIPT): base.digest(MANUSCRIPT)},
        reviewed_angelo_preflight_sha256=base.digest(angelo.PREFLIGHT),
        translation_policy="natural-dialogue-v2", target_locale="en-US",
        stored_and_native_verification_of_changes_pending=True))
    print(f"Reviewed 196 texts in six exchanges. {dict(counts)} and two retained choice labels.", flush=True)


def preflight():
    source = checked_text(precedent.preflight_source, {
        "    plans,pictures,open_cases={},[],[]":
            "    previous = base.load(angelo.PREFLIGHT)\n"
            "    assert previous['candidate_sha256'] == draft['candidate_sha256']\n"
            "    plans,pictures,open_cases=previous['plans'].copy(),[],[]",
        'for row in (r for r in draft["records"] if r["decision"]=="revision"):':
            'for row in (r for r in draft["records"] if r["decision"]=="revision" and r["block"]!=158):',
        'plans=plans,pending=open_cases,sheets=sheets,offline_native_only=True,':
            'plans=plans,pending=open_cases,sheets=sheets + previous["sheets"],offline_native_only=True,',
    })
    scope = layout.preflight.__globals__ | globals() | dict(ROOT=BATCH, layout=layout.layout)
    exec(compile(source, __file__ + "::native-preflight", "exec"), scope)
    scope["preflight"]()


compiler_scope = vars(compiler) | globals() | dict(
    layout=compiler.layout, guard_spec=parent.scope["guard_spec"],
    bind_registered_story_percent_guard=parent.scope["bind_registered_story_percent_guard"])
compiler_scope["parent"] = SimpleNamespace(ROM=parent.ROM, MANIFEST=parent.MANIFEST, RELEASE=parent.RELEASE,
    guard_spec=parent.scope["guard_spec"], bind_registered_story_percent_guard=parent.scope["bind_registered_story_percent_guard"])
compiler_scope["compilers"] = FunctionType(compiler.compilers.__code__, compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        author()
    elif action == "preflight":
        preflight()
    elif action in ("stage", "native_display"):
        FunctionType(getattr(compiler, action).__code__, compiler_scope)()
    else:
        inherited = getattr(compiler.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
