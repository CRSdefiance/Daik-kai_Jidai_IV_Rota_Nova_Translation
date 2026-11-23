"""Review the complete dolphin, Sirens, and mermaid encounters."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import checkpoint_sea_event_review_v1 as sea
from scripts import register_rafael_sailing_modes_20261119 as parent
from scripts import review_sailing_hazards_and_dolphins_v1 as hazards
from scripts import stage_sea_event_dialogue_followup_20261118 as workflow
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.stage_shared_notices_storage_v1 import relocate

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = workflow.ARM, workflow.COMMON, workflow.CLEAN
ROOT = Path("work/fleet_encounter_dialogue_20261119")
ROM, PROOF = ROOT / "Fleet_Encounter_Dialogue_RESEARCH_ONLY.nds", ROOT / "staged.json"
SEA_REVIEW = Path("releases/all_routes_editorial_20261110_sea_events_candidate/verification/registered_review.json")
HAZARD_REVIEW = Path("releases/all_routes_editorial_20261111_sailing_hazards_and_dolphins_candidate/verification/registered_review.json")
IDS = (*range(436, 457), *range(2366, 2391))
EDITS = {
    445: ("What the...? S-somebody's swimming out there!", ("What the...?", "swimming out there!")),
    449: ("Oh! Is that a mermaid, like in the legends?!", ("like in the legends?!",)),
    450: ("Oh! A mermaid from the legends?!", ()),
    451: ("Whoa! A mermaid, like in the stories?!", ("like in the stories?!",)),
    453: ("Could that really be a mermaid from the legends?!", ("a mermaid from the legends?!",)),
    456: ("Could that be a mermaid from the legends?", ("a mermaid from the legends?",)),
    2366: ("Dolphins! May I put this in the ship's log?", ("May I put this in the ship's log?",)),
    2369: ("Admiral, look! A pod of dolphins! May I put this in the ship's log?",
           ("Admiral, look!", "A pod of dolphins!", "May I put this in the ship's log?")),
    2372: ("Wow! So many dolphins! I want to put it in the ship's log. Can I, Admiral?",
           ("So many dolphins!", "I want to put it in the ship's log.", "Can I, Admiral?")),
    2382: ("So the dolphins are gone... I feel a bit calmer now.", ("I feel a bit calmer now.",)),
}
REASONS = {
    436: "Keep the stammer and puzzled reaction to singing before the voice does anything else.",
    437: "The short 'Huh?' stands in for the isolated question mark before the sailor asks about the song.",
    438: "The one-word question gives tentative recognition without identifying a singer.",
    439: "Keep the stammer on 'what' and the startled question about the song.",
    440: "The second question makes it clear the young sailor is unsure whether they hear singing at all.",
    441: "The two beats let the lookout first notice movement and then stammer that someone is swimming.",
    442: "'It looks like' preserves the lookout's uncertainty after the initial question.",
    443: "The broken question and the stammer give the identification its own beat.",
    444: "The soft surprise and question keep this voice tentative about the swimmer.",
    445: "The rough voice's startled aside and stammer fit the shift from noticing motion to seeing a swimmer.",
    446: "The more deliberate question and broken 'S-someone' retain both the hesitation and the report.",
    447: "Keep the brief question and youthful exclamation before the other speaker suggests a mermaid.",
    448: "The measured first question leads into genuine surprise that someone is swimming.",
    449: "The speaker wonders if the swimmer is a mermaid of the sort described in legends.",
    450: "The short exclamation preserves the excited recognition and the reference to legends.",
    451: "Use 'stories' in this casual exclamation and preserve the tentative comparison to the stories the sailor knows.",
    452: "The speaker recognizes a possibility and keeps the mermaid as a figure from legend.",
    453: "The rhetorical question sounds surprised and skeptical while leaving the swimmer's identity open.",
    454: "The broken question already gives the realization its pause. This source voice makes no reference to legends.",
    455: "Preserve the stammer and uncertainty in this young voice's short question.",
    456: "The more measured speaker still asks a full question and connects the swimmer to legends.",
    2366: "The lookout's exclamation and the entire request fit as separate spoken beats. The lookout asks permission to record it.",
    2367: "Keep the formal address, the pod in sight, and the polite request to use the ship's log.",
    2368: "The nearby sighting and the informal 'Can I' suit the excited reaction.",
    2369: "Keep the address, the pod, and a single polite question about recording the sighting.",
    2370: "The rough voice's short bursts of excitement and informal question already sound spoken.",
    2371: "The deliberate admiration and 'May I' suit the more measured lookout.",
    2372: "Keep the young lookout's unqualified excitement and eagerness to write it down before asking the admiral.",
    2373: "Rafael gives immediate permission in a casual voice.",
    2374: "Hodram's more formal assent contrasts with Rafael and Lil's brisk replies.",
    2375: "Lil follows her quick assent with a concise instruction to enter the sighting in the log.",
    2376: "Maria's direct request preserves the source's polite phrasing.",
    2377: "The lookout invites the admiral to share the calming feeling once the dolphins go.",
    2378: "The lookout observes the departure and then names the peaceful quality of the sight.",
    2379: "The short, informal appraisal after the pause suits this younger voice.",
    2380: "Keep the thought that a quiet moment is worth enjoying now and then.",
    2381: "The casual 'sure was' keeps this lookout's voice in the quiet closing beat.",
    2382: "The speaker reflects on how the sight left them calmer. Use everyday spoken English in the second beat.",
    2383: "The farewell is addressed to the dolphins. The understated comment keeps the childlike warmth.",
    2384: "The most measured farewell calls the encounter a brief, welcome respite.",
    2385: "Keep the stammer and the sailor's fear that the singing is affecting their mind.",
    2386: "The cry, question about the voice, and mounting distress each belong to this variant.",
    2387: "The scream and stammer preserve a separate anguished reaction before the sailor fears going mad.",
    2388: "Keep the plea for help as well as the interrupted complaint and fear that follows.",
    2389: "The childlike cry describes the voice as odd without importing the other speakers' fear of going mad.",
    2390: "The outcry and plain distress suit the fallback voice in the second Sirens beat.",
}


def source_groups(clean, current):
    result = {}
    for start, end, table, literal, load, call, consumer, role, _ in sea.GROUPS:
        if start not in (436, 441, 449):
            continue
        group, = (g for g in base.load(sea.OUTPUT)["exact_native_event_groups"] if g["first_ID"] == start)
        assert unpack_from("<8i", clean, table) == unpack_from("<8i", current, table)
        assert group["source_native_caller"] == sea.caller_binding(clean, current, load, call, literal, sea.BASE+table, consumer)
        assert group["original_role_argument"] == role
        result.update((n, (group | {"table": group["selector"], "consumer": sea.BASE+consumer}, group["original_actor_voice_choices"]))
                      for n in range(start, end))
    old_hazards = base.load(hazards.OUTPUT)
    for start, end, table, load, call, literal, consumer, role, _ in hazards.GROUPS[:4]:
        group, = (g for g in old_hazards["native_context"] if g["first_ID"] == start)
        slots = tuple(group["slots"])
        assert slots == unpack_from(f"<{len(slots)}i", clean, table) == unpack_from(f"<{len(slots)}i", current, table)
        assert group["native_callers"] == [sea.caller_binding(clean, current, load, call, literal, sea.BASE+table, consumer)]
        choices = group.get("original_voice_choices", [])
        native_group = group | {"consumer": sea.BASE+consumer, "original_role_argument": role}
        result.update((n, (native_group, choices)) for n in range(start, end+1))
    assert set(result) == set(IDS)
    return result


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    context = workflow.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(CLEAN)
    original_arm = clean.read_file(ARM)
    original = workflow.common_message_entries(clean.read_file(COMMON), original_arm)
    arm, common = context.arm, context.common
    assert native.digest(arm) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    installed = workflow.owned_entries(common, arm, directory)
    groups = source_groups(original_arm, arm)
    source = {r["message_ID"]: r for p in (SEA_REVIEW, HAZARD_REVIEW) for r in base.load(p)["records"]}
    assert set(IDS) == REASONS.keys()
    rows = {}
    for n in IDS:
        prior, jp, previous = source[n], original[n], installed[n]
        assert all(prior["review"].values()) and jp.text.hex() == prior["source_hex"]
        assert workflow.logical(previous.text) == prior["english"], n
        assert b"%" not in jp.text + previous.text
        english, phrases = EDITS.get(n, (prior["english"], ()))
        rows[n] = dict(id=f"COMMON_MESSAGE_{n}", message_ID=n, file_path=COMMON, speaker=prior["speaker"],
            context=prior["context"], clean_Japanese=jp.text.decode("cp932"), source_meaning=prior["source_meaning"],
            english=english, previous_English=prior["english"], localization_note=REASONS[n],
            decision="revision" if n in EDITS else "retention", source_reference=workflow.reference(jp),
            current_reference=workflow.reference(previous), source_hex=jp.text.hex(), current_hex=previous.text.hex(),
            protected_phrases=phrases, review=dict.fromkeys(workflow.parent.GATES, True) | {"formatting": False})
    wrap = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ |
                        {"PHRASES": {n: p for n, (_, p) in EDITS.items() if p}})
    storage = wrap({n: rows[n] for n in EDITS})
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    new_common, new_arm, entries, allocation = repack(common, arm, rows, storage)
    assert allocation["changed_visible_templates"] == list(EDITS)
    assert allocation["all_unselected_native_copy_spans_exact"] and allocation["all_41_blocks_fit_8KiB"]
    start, end = workflow.DIRECTORY_OFFSET, workflow.TABLE_OFFSET + len(installed)*4
    assert new_arm[:start] == arm[:start] and new_arm[end:] == arm[end:]
    ctx = with_components(context, new_arm, new_common)
    painter, _, font = workflow.font_tools(context.image)
    kanji = context.image.read_file("/GRP/KANJI.FNT")
    pages = []
    for n, row in rows.items():
        group, choices = groups[n]
        actor = group["slots"].index(n) if group["consumer"] == sea.BASE + 0x53BD8 else next(i for i, _, msg in choices if msg == n)
        payload = entries[n].text
        verify = portrait_case(ctx, row, group, payload, actor)
        display = verify.pop("display")
        lines = [line.strip() for line in display.decode("ascii").splitlines()]
        assert " ".join(lines) == row["english"] and 0 < len(lines) <= 4
        assert all(0 < len(line) <= 36 for line in lines)
        assert all(any(p in line for line in lines) for p in row["protected_phrases"])
        pixels, glyphs = render_portrait(painter, new_arm, kanji, display)
        assert [g["code"] for g in glyphs] == workflow.glyph_codes(display)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(row["english"][0]), ord(row["english"][-1]))
        if n in EDITS:
            pages.append((n, pixels))
        row.update(staged_reference=workflow.reference(entries[n]), staged_hex=payload.hex(), display_hex=display.hex(),
            visible_lines=lines, formatting_evidence=dict(native_dispatch=verify, glyph_count=len(glyphs),
                ink_sha256=native.digest(pixels), original_allocation_and_page_verified=True, pages=1))
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, new_arm)
    image.replace_file(COMMON, new_common)
    new_data = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(new_data)
    sheets = portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(new_arm),
        target_COMMON_sha256=native.digest(new_common), entire_parent_inverse=True,
        allocation=allocation, preservation=dict(directory_table_only=True, native_tables_unchanged=True),
        source_proofs={p.as_posix(): base.digest(p) for p in (SEA_REVIEW, HAZARD_REVIEW, sea.OUTPUT, hazards.OUTPUT)},
        font=font, sheets=sheets, translation_policy="natural-dialogue-v2",
        encoder="dialogue-relocatable-v1", target_locale="en-US", review_gates=workflow.parent.GATES,
        records=list(rows.values())))
    print(f"Verified {len(rows)} source-bound portraits and generated {len(pages)} revised pages.")


if __name__ == "__main__":
    main()
