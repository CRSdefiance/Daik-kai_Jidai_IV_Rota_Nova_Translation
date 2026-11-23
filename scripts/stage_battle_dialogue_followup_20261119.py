"""Review the ram, attack confirmation, defeat and special-target portraits."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import register_sea_hazard_dialogue_20261119 as parent
from scripts import review_battle_commands_and_outcomes_v1 as battle
from scripts import stage_battle_commands_and_outcomes_v1 as original
from scripts import stage_sea_hazard_dialogue_20261119 as hazard
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.stage_shared_notices_storage_v1 import relocate

base, native, workflow = parent.base, parent.native, hazard.workflow
ARM, COMMON, CLEAN = hazard.ARM, hazard.COMMON, hazard.CLEAN
ROOT = Path("work/battle_dialogue_followup_20261119_v4")
ROM, PROOF = ROOT / "Battle_Dialogue_Followup_RESEARCH_ONLY.nds", ROOT / "staged.json"
PREVIOUS = Path("releases/all_routes_editorial_20261111_battle_commands_and_outcomes_candidate/verification/registered_review.json")
ATTACK_PATHS = Path("releases/all_routes_editorial_20261118_sailing_mode_prose_candidate/verification/verified_display_ownership.json")
EDITS = {
    2110: ("We rammed their ship right in the side!", ("We rammed their ship", "right in the side!")),
    2129: ("May we strike %s?", ()),
    2179: ("%s's flagship was knocked out. We've lost!", ()),
    2186: ("%s's flagship fell. We've lost the battle.", ()),
}
REASONS = {
    2106: "The direct report identifies where the ram hit and leaves the outcome to what follows.",
    2107: "Keep the terse acknowledgment in this voice. The subject is implicit in the quick report.",
    2108: "'Our ram' keeps the crew's excited ownership of the hit.",
    2109: "'Struck' gives this voice its emphasis and names the enemy ship.",
    2110: "Keep the rough sailor's emphasis on hitting the ship in the side and give that phrase its own line.",
    2111: "The confident older voice calls the successful maneuver in a short exclamation.",
    2112: "The youthful sailor makes a simple, excited report and names the ram.",
    2113: "The more measured 'has struck' suits the formal voice even during the action.",
    2122: "The fallback asks for agreement in one complete question. The selected town is the target.",
    2123: "The clipped question is a natural way for this First Mate to confirm the selected target.",
    2124: "'Should we' keeps the familiar speaker checking the order.",
    2125: "'May we' retains the more courteous request and fits the town name into the question.",
    2126: "'Going after' reflects the rough voice while still asking for assent.",
    2127: "'Are we to' sounds measured and keeps the order pending.",
    2128: "'So we're attacking' sounds like the young speaker confirming instructions already heard.",
    2129: "Give the especially courteous voice a distinct request to proceed with the attack before the choice.",
    2179: "Say the flagship was knocked out, then give the defeat report. The source leaves the ship's fate open.",
    2180: "Only this speaker explicitly reports a sinking. Keep the two emphatic announcements.",
    2181: "'They took out' keeps the immediate, informal report before the collective admission of defeat.",
    2182: "Give the first beat a subdued cadence and the result a burst of dismay.",
    2183: "'They got' and 'lost the fight' suit the rough sailor's blunt delivery.",
    2184: "'Looks like' preserves the older voice's uncertainty about what happened to the flagship.",
    2185: "The two short exclamations fit the younger sailor's reaction.",
    2186: "Use a measured announcement of the flagship's defeat. 'Disabled' implies a more specific condition than the Japanese gives.",
    2187: "Keep the collective victory announcement. The encounter getter supplies the creature or vessel.",
    2188: "'Down' is a terse battle report and leaves the target's precise fate open.",
    2189: "Preserve the brisk declaration of defeat and the complete target name.",
    2190: "The Japanese is identical to the nearby alternative and suits the same brief battle cry.",
    2191: "Keep the younger voice's plain, emphatic victory announcement.",
}


def original_groups(ja, en):
    result = {}
    for g in base.load(battle.OUTPUT)["native_context"]:
        start = g["table"] - battle.BASE
        assert tuple(g["slots"]) == unpack_from("<8i", ja, start) == unpack_from("<8i", en, start)
        caller, = g["native_callers"]
        prefix = g["argument_prefix"]
        pos = prefix["start"] - battle.BASE
        body = bytes.fromhex(prefix["exact_hex"])
        if g["argument_kind"] == "special":
            # The registered alias changes the call after the original model name is obtained.
            assert ja[pos:pos+len(body)] == body and en[pos:pos+len(body)-4] == body[:-4]
            assert en[pos+len(body)-4:pos+len(body)] != body[-4:]
            prior_arm = base.NdsImage.open(parent.ROM).read_file(ARM)
            assert prior_arm[pos:pos+len(body)] == en[pos:pos+len(body)]
            original.alias_controls(en)
        else:
            assert ja[pos:pos+len(body)] == en[pos:pos+len(body)] == body
        field = caller["literal_address"] - battle.BASE
        assert unpack_from("<I", ja, field) == unpack_from("<I", en, field) == (g["table"],)
        for n in range(g["first_ID"], g["last_ID"]+1):
            result[n] = g | {"consumer": caller["consumer"]}
    assert result.keys() == REASONS.keys()
    return result


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    runtime = workflow.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(CLEAN)
    ja, arm, common = clean.read_file(ARM), runtime.arm, runtime.common
    source = workflow.common_message_entries(clean.read_file(COMMON), ja)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    current = workflow.owned_entries(common, arm, directory)
    groups = original_groups(ja, arm)
    prior = {r["message_ID"]: r for r in base.load(PREVIOUS)["records"]}
    assert prior.keys() == REASONS.keys()
    rows, prepared = {}, {}
    for n, old in prior.items():
        jp, installed = source[n], current[n]
        assert all(old["review"].values()) and jp.text.hex() == old["source_hex"]
        assert workflow.logical(installed.text) == old["english"]
        english, phrases = EDITS[n] if n in EDITS else (old["english"], ())
        assert jp.text.count(b"%s") == installed.text.count(b"%s") == english.count("%s")
        rows[n] = dict(id=old["id"], message_ID=n, file_path=COMMON, speaker=old["speaker"],
            context=old["context"], clean_Japanese=jp.text.decode("cp932"), source_meaning=old["source_meaning"],
            english=english, previous_English=old["english"], localization_note=REASONS[n],
            decision="revision" if n in EDITS else "retention", source_reference=workflow.reference(jp),
            current_reference=workflow.reference(installed), source_hex=jp.text.hex(), current_hex=installed.text.hex(),
            original_substitution_count=old["original_substitution_count"],
            protected_phrases=phrases, review=dict.fromkeys(workflow.parent.GATES, True) | {"formatting": False})
        if n in EDITS and not phrases:
            prepared[n] = english.encode("ascii")
    wrap = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ |
                        {"PHRASES": {n: p for n, (_, p) in EDITS.items() if p}})
    prepared.update(wrap({n: rows[n] for n, (_, p) in EDITS.items() if p}))
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    new_common, new_arm, entries, allocation = repack(common, arm, rows, dict(sorted(prepared.items())))
    assert allocation["changed_visible_templates"] == list(EDITS)
    start, end = workflow.DIRECTORY_OFFSET, workflow.TABLE_OFFSET + len(current)*4
    assert new_arm[:start] == arm[:start] and new_arm[end:] == arm[end:]
    for stored in base.load(parent.parent.PENDING)["records"]:
        entry = entries[stored["message_ID"]]
        assert workflow.reference(entry) == stored["current_reference"] and entry.text.hex() == stored["current_hex"]

    context = with_components(runtime, new_arm, new_common)
    painter, _, font = workflow.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    select = original.original_portraits()
    arguments = battle.argument_samples(runtime, ja)
    pages = []
    for n, row in rows.items():
        group = groups[n]
        actor = next(i for i, _, msg in group["original_voice_choices"] if msg == n)
        template = entries[n].text
        row.update(staged_reference=workflow.reference(entries[n]), staged_hex=template.hex(), native_displays=[])
        choices = original.samples(group["argument_kind"], arguments, n)
        if n in EDITS and group["argument_kind"] == "town":
            choices.append(next(sample for sample in arguments["town"] if sample["arguments"] == [b"Madeira".hex()]))
        for i, sample in enumerate(choices):
            args = tuple(bytes.fromhex(a) for a in sample["arguments"]) if sample else ()
            result = select(context, row, group, template, actor, args, sample)
            display = result.pop("display")
            expected = row["english"].encode("ascii") % args if args else row["english"].encode("ascii")
            lines = [line.strip() for line in display.decode("ascii").splitlines()]
            assert b" ".join(display.split()) == expected and 0 < len(lines) <= 4, (n, lines)
            assert all(0 < len(line) <= 36 for line in lines), (n, lines)
            for phrase in (*row["protected_phrases"], *(name.decode("ascii") for name in args)):
                assert any(phrase in line for line in lines), (n, phrase, lines)
            pixels, glyphs = render_portrait(painter, new_arm, kanji, display)
            assert [g["code"] for g in glyphs] == workflow.glyph_codes(display)
            assert (glyphs[0]["code"], glyphs[-1]["code"]) == (expected[0], expected[-1])
            row["native_displays"].append(dict(native_dispatch=result, sample=sample, expansion_hex=expected.hex(),
                display_hex=display.hex(), visible_lines=lines, glyph_count=len(glyphs), ink_sha256=native.digest(pixels)))
            if n in EDITS:
                pages.append((f"{n}/{i+1}", pixels))
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, new_arm)
    image.replace_file(COMMON, new_common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=base.digest(parent.ROM),
        clean_input_sha256=base.digest(CLEAN), target_ARM9_sha256=native.digest(new_arm),
        target_COMMON_sha256=native.digest(new_common), entire_parent_inverse=True, allocation=allocation,
        source_proofs={p.as_posix(): base.digest(p) for p in (PREVIOUS, battle.OUTPUT, ATTACK_PATHS)},
        font=font, sheets=portrait_sheets(ROOT, pages), translation_policy="natural-dialogue-v2",
        encoder="dialogue-relocatable-v1", target_locale="en-US", review_gates=workflow.parent.GATES,
        records=list(rows.values())))
    print(f"Verified {len(rows)} source-bound portraits and generated {len(pages)} revised pages.")


if __name__ == "__main__":
    main()
