"""Review shared weather and the protected and unprotected sea hazards."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import checkpoint_sea_event_review_v1 as sea
from scripts import register_fleet_encounter_dialogue_20261119 as parent
from scripts import review_sailing_hazards_and_dolphins_v1 as hazards
from scripts import review_sailing_reactions_v1 as protection
from scripts import stage_sea_event_dialogue_followup_20261118 as workflow
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.stage_shared_notices_storage_v1 import relocate

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = workflow.ARM, workflow.COMMON, workflow.CLEAN
ROOT = Path("work/sea_hazard_dialogue_20261119_v2")
ROM, PROOF = ROOT / "Sea_Hazard_Dialogue_RESEARCH_ONLY.nds", ROOT / "staged.json"
SEA_REVIEW = Path("releases/all_routes_editorial_20261110_sea_events_candidate/verification/registered_review.json")
HAZARD_REVIEW = Path("releases/all_routes_editorial_20261111_sailing_hazards_and_dolphins_candidate/verification/registered_review.json")
PROTECTION_REVIEW = Path("releases/all_routes_editorial_20261111_sailing_reactions_candidate/verification/registered_review.json")
IDS = (*range(383, 394), *range(2391, 2425), *range(2476, 2492))
EDITS = {
    392: ("Admiral! A blizzard just blew in!", ()),
    2393: ("These bubbles will swallow our ship!", ()),
    2404: ("Damn! We're caught!", ()),
    2409: ("Whoa! We're caught in the whirlpool!", ()),
    2410: ("Oh no! The whirlpool's pulling us in!", ("The whirlpool's pulling us in!",)),
    2420: ("Too late! We can't turn fast enough!", ()),
    2477: ("Admiral, the extra armor saved us. We took no damage.",
           ("Admiral, the extra armor saved us.", "We took no damage.")),
    2478: ("We fitted that extra armor, Admiral. Not a scratch on the ship!",
           ("We fitted that extra armor, Admiral.", "Not a scratch on the ship!")),
    2480: ("Reef damage? Our extra armor can handle that!", ("Our extra armor can handle that!",)),
    2485: ("The ram broke up the drift ice, Admiral. We took no damage!",
           ("The ram broke up the drift ice,", "We took no damage!")),
    2489: ("The ram broke up the drift ice. No need to worry about the ship.",
           ("The ram broke up the drift ice.", "No need to worry about the ship.")),
    2491: ("The ram shattered the drift ice, Admiral. The ship took no damage.",
           ("The ram shattered the drift ice,", "The ship took no damage.")),
}
REASONS = {
    383: "The measured report names the storm and addresses the admiral as it arrives.",
    384: "The separate call for the admiral's attention suits this informal warning.",
    385: "The two emphatic beats convey alarm first and identify the storm second.",
    386: "'Just hit' captures the rough voice reporting the storm's arrival.",
    387: "'Come up' fits the older sailor's description of the weather turning.",
    388: "The youthful alarm and the name of the hazard can come out in two quick bursts.",
    389: "The matter-of-fact report describes the onset and preserves the address.",
    390: "'We've hit' conveys that the ship is already in the blizzard.",
    391: "The clipped report fits the direct tone and places the weather immediately in view.",
    392: "'Blew in' lets the older voice announce the blizzard in a complete, one-line thought.",
    393: "The shiver and broken address preserve the sequence of the child's reaction.",
    2391: "Keep the direct warning that the bubbles are already engulfing the ship.",
    2392: "The demonstrative points at the visible bubbles and the full verb phrase stays together after the break.",
    2393: "Keep the impending threat to our ship in a single urgent spoken beat.",
    2394: "The rough sailor says 'our ship' as they see it being engulfed.",
    2395: "'Those bubbles' brings the older voice into the ongoing emergency, with the action on an intact second line.",
    2396: "'Eating our ship' preserves the child's way of describing what they see.",
    2397: "Keep the groan and stammer as the cold interrupts the speaker.",
    2398: "The shiver comes first, followed by the younger voice's plain complaint.",
    2399: "Keep the startled interjection and the repeated start on 'lightning'.",
    2400: "The clipped recognition suits a warning delivered as the lightning strikes.",
    2401: "The stammer itself carries the startle, followed by the name of the hazard.",
    2402: "This sailor also stammers. The same short English cry conveys the emphasis of the original.",
    2403: "The drawn-out cry precedes the child's recognition of lightning.",
    2404: "The blunt first beat fits the rough speaker's dismay, then the sailor reports being caught.",
    2405: "The two beats separate the sailor's first alarm from the explicit tornado warning.",
    2406: "Keep the scream on its own beat before the sailor identifies the tornado trapping the ship.",
    2407: "The older sailor reports the ship still being pulled after the opening alarm.",
    2408: "'Swallowing us' preserves the child's image and names the tornado.",
    2409: "The startled sailor reports that the ship and crew are already caught in the whirlpool.",
    2410: "The immediate alarm leads into the whirlpool's ongoing pull, with each beat on one line.",
    2411: "Keep the older sailor's alarm and the vivid description of ongoing movement into the whirlpool.",
    2412: "Keep the child's image of the whirlpool eating the ship.",
    2413: "'Hidden reef' conveys the sudden realization that there's a submerged hazard.",
    2414: "The sailor reports contact, leaving the damage for what follows.",
    2415: "Keep the sharp alarm and the reef warning as two short beats.",
    2416: "'Look out' delivers the sailor's urgent warning that a reef is in view.",
    2417: "The older sailor voices immediate concern and identifies the submerged reef.",
    2418: "The child's scream comes before the simple identification.",
    2419: "Keep the interrupted reference to the rudder and the urgent conclusion.",
    2420: "The first exclamation conveys dismay, followed by a sailor's plain description of the turn coming too late.",
    2421: "Keep the interrupted thought and the different verb in this voice's conclusion.",
    2422: "The older sailor's clipped 'No good!' suits the effort to steer clear.",
    2423: "Keep the child's report that they cannot steer, which differs from turning too late.",
    2424: "The speaker voices dismay and gives a firm judgment that the ship will fail to turn in time.",
    2476: "The report leads with the absence of reef damage and then credits the extra armor.",
    2477: "Keep the respectful address and explain naturally that the extra armor prevented all damage.",
    2478: "Express the relief that the crew fitted the armor and that the ship escaped without a scratch.",
    2479: "The admiral hears the specific reef outcome first, followed by the sailor's relief.",
    2480: "The question and answer keep the boast brisk and tie it specifically to reef damage.",
    2481: "The first sentence explains the unscathed ship, and the familiar proverb suits the older voice.",
    2482: "The rough sailor's 'no big deal' conveys confidence grounded in the extra armor.",
    2483: "Keep the deferential, specific report that extra armor prevented all reef damage.",
    2484: "The clipped report credits the ram, then confirms the ship escaped harm.",
    2485: "Keep the admiral's address, place 'broke up' with its object, and complete the report with the outcome.",
    2486: "The exclamation about their luck is explicit in Japanese and comes before the explanation.",
    2487: "The sailor reports what the ram did and takes a distinct second beat to express relief.",
    2488: "'Smashed' conveys the rough voice's forceful description of the floating ice breaking.",
    2489: "The older sailor reassures the crew about the ship's condition after the ram breaks the ice.",
    2490: "The exclamation keeps this young sailor's delight at seeing the ice break.",
    2491: "Put the cause and outcome in two spoken beats and keep the formal address to the admiral.",
}


def source_groups(clean, current):
    weather = {g["first_ID"]: g for g in base.load(sea.OUTPUT)["exact_native_event_groups"]}
    encounters = {g["first_ID"]: g for g in base.load(hazards.OUTPUT)["native_context"]}
    protected = {g["first_ID"]: g for g in base.load(protection.OUTPUT)["native_context"]}
    result = {}
    for start, end, table, literal, load, call, consumer, role, _ in sea.GROUPS[:2]:
        group = weather[start]
        binding = sea.caller_binding(clean, current, load, call, literal, sea.BASE + table, consumer)
        assert group["source_native_caller"] == binding
        slots = tuple(group["table_slots"])
        assert slots == unpack_from("<8i", clean, table) == unpack_from("<8i", current, table)
        source = group | {"table": group["selector"], "consumer": sea.BASE + consumer}
        result.update((n, (source, group["original_actor_voice_choices"])) for n in range(start, end))

    selectors = list(hazards.GROUPS[4:]) + [
        (start, end, table, load, call, literal, consumer, role, description)
        for start, end, table, literal, load, call, consumer, role, description in protection.GROUPS
        if start in (2476, 2484)
    ]
    for start, end, table, load, call, literal, consumer, role, _ in selectors:
        group = (protected if start >= 2476 else encounters)[start]
        slots = tuple(group["slots"])
        assert slots == unpack_from("<8i", clean, table) == unpack_from("<8i", current, table)
        binding = sea.caller_binding(clean, current, load, call, literal, sea.BASE + table, consumer)
        assert group.get("native_callers", [group.get("original_source_caller")]) == [binding]
        source = group | {"consumer": sea.BASE + consumer, "original_role_argument": role}
        result.update((n, (source, group["original_voice_choices"])) for n in range(start, end + 1))
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
    source = {r["message_ID"]: r for p in (SEA_REVIEW, HAZARD_REVIEW, PROTECTION_REVIEW) for r in base.load(p)["records"]}
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
        actor = next(i for i, _, msg in choices if msg == n)
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
        source_proofs={p.as_posix(): base.digest(p) for p in (SEA_REVIEW, HAZARD_REVIEW, PROTECTION_REVIEW, sea.OUTPUT, hazards.OUTPUT, protection.OUTPUT)},
        font=font, sheets=sheets, translation_policy="natural-dialogue-v2",
        encoder="dialogue-relocatable-v1", target_locale="en-US", review_gates=workflow.parent.GATES,
        records=list(rows.values())))
    print(f"Verified {len(rows)} source-bound portraits and generated {len(pages)} revised pages.")


if __name__ == "__main__":
    main()
