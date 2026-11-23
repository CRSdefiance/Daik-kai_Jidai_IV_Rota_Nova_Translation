"""Stage four complete Hodram and Lil exchanges over the registered ROM."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import re
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_six_followup_exchanges_20261122 as checkpoint
from scripts import rebind_hodram_and_lil_followups_20261122 as paired
from scripts import stage_rafael_six_followup_exchanges_20261122 as template


base, native, established = paired.base, paired.native, template.established
active = paired.active
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path("work/analysis/hodram_and_lil_followups_20261122/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_And_Lil_Followups_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF, CHOICE_PROOF = ROOT / "unchanged_FE_pages.json", ROOT / "unchanged_choice.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
typed = template.typed
MANUSCRIPTS = tuple(Path(__file__).with_name(f"{stem}_20261122.md") for stem in (
    "hodram_aziza_and_cristina_followups", "lil_clifford_and_rafael_followups"))
CAPTIONS = (
    ("Hmm... fine, then.", "Lil reluctantly accepts the negotiated offer.", "Her hesitation and brief acceptance fit the branch."),
    ("Are you nuts?", "Lil rejects the proposed exchange with indignation.", "The sharp refusal matches her next line and preserves the second branch."),
)


def load_sections():
    sections = {}
    for manuscript in MANUSCRIPTS:
        parts = re.split(r"^## SC([12]) B(\d+)\s*$", manuscript.read_text(encoding="utf-8"), flags=re.M)
        assert not parts[0].strip()
        for route, block, section in zip(parts[1::3], parts[2::3], parts[3::3], strict=True):
            context, table = section.strip().split("\n\n", 1)
            rows = {}
            for text in table.splitlines():
                key, *fields = text.split("|", 4)
                assert int(key) not in rows
                rows[int(key)] = fields
            sections[int(route), int(block)] = context, rows
    return sections


def reference(group, row, label):
    return dict(file_path=group["file_path"], block=group["block"],
        archive_sha256=group[f"{label}_archive_sha256"], block_sha256=group[f"{label}_block_sha256"],
        command_offset=row[f"{label}_command_offset"], offset=row[f"{label}_offset"],
        exact_body_hex=row[f"{label}_body_hex"], exact_command_hex=row[f"{label}_command_hex"])


def contextual_review():
    assert not REVIEW.exists()
    packet, release = map(base.load, (paired.OUTPUT, parent.RELEASE))
    candidate = base.digest(parent.ROM)
    assert packet["candidate_sha256"] == release["candidate_sha256"] == candidate
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    catalogue = template.review_scope["established"].CATALOGUE
    names = {row["actor_ID"]:row["progressive_nameplate"]
             for row in base.load(catalogue)["source_and_current_default_name_fields"]}
    sections, records, groups, captions, leads = load_sections(), [], [], [], []
    for group in packet["groups"]:
        route, block, path = (group[k] for k in ("route","block","file_path"))
        context, decisions = sections.pop((route, block))
        ids = []
        for row in group["records"]:
            ordinal, selector = row["source_record_index"], row["selector"]
            ident = f"DK4_MES_B{block}_R{ordinal:04d}"
            source, current = [reference(group,row,label) for label in ("source","current")]
            current["candidate_sha256"] = candidate
            before = " ".join(row["current_English"].split())
            if row["native_command_word"] == 0x2100:
                slot, = row["slots"]
                english, meaning, note = CAPTIONS[slot]
                assert (route,block) == (2,133) and english == before
                captions.append(dict(id=ident, slot=slot, Japanese=row["Japanese"], english=english, context=context,
                    source_meaning=meaning, localization_note=note, source_reference=source, current_reference=current,
                    decision="retention",
                    review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
                continue
            assert row["native_command_word"] == 0x4000 and selector <= 254
            meaning, replacement, protection, note = decisions.pop(ordinal)
            english = replacement or before
            phrases = protection.split(";") if protection else []
            assert all(part in english and len(part) <= 36 for part in phrases), (ident, phrases)
            change = "prose" if english != before else "wrap_only" if phrases else "retention"
            if selector == 254:
                assert change == "retention"
            if change != "retention":
                assert english.isascii()
            control = bytes([selector]).hex()
            records.append(dict(id=ident, route=route, file_path=path, block=block, source_selector=selector,
                kind="system" if selector == 254 else "progressive", speaker=names[selector] if selector != 254 else "System",
                context=context, source_meaning=meaning, Japanese=row["Japanese"], previous_English=before, english=english,
                protected_phrases=phrases, source_reference=source, current_reference=current,
                source_hex=control+source["exact_body_hex"], current_hex=control+current["exact_body_hex"],
                change_class=change, decision="revision" if change!="retention" else "retention", localization_note=note,
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=change=="retention")))
            ids.append(ident)
        assert not decisions
        groups.append(dict(route=route, block=block, file_path=path, context=context, record_ids=ids,
            source_block_sha256=group["source_block_sha256"], current_block_sha256=group["current_block_sha256"]))
        leads.extend((path,block,r["offset"]) for r in group["open_wrap_leads"])
    assert not sections and len(records)==288 and len(captions)==2 and len(leads)==8
    changed = {(r["file_path"],r["block"],r["current_reference"]["offset"]):r for r in records if r["decision"]=="revision"}
    assert all(lead in changed for lead in leads)
    counts = dict(Counter(r["change_class"] for r in records))
    BATCH.mkdir(parents=True, exist_ok=True)
    base.save(REVIEW, dict(candidate_sha256=candidate, clean_sha256=packet["clean_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", groups=groups, records=records,
        retained_choice_labels=captions, counts=counts, wrap_leads_covered=[changed[k]["id"] for k in leads],
        source_packet_sha256=base.digest(paired.OUTPUT), wrap_queue_sha256=base.digest(checkpoint.QUEUE),
        manuscripts_sha256={str(path):base.digest(path) for path in MANUSCRIPTS},
        stored_and_native_verification_of_changes_pending=True))
    print(f"Reviewed all 288 spoken and system texts and two choice captions. {counts}", flush=True)


preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))
compiler_scope = template.compiler_scope | globals()
exec(compile(template.template.renderer_source, __file__ + "::native-layouts", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review","preflight","stage","native_display","patch","startup"))
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
