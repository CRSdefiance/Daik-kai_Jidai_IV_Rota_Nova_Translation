"""Review all eight sea-inspection reactions and stage four fixed-slot improvements."""

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import replay_current_sea_targets_20261123 as live
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.stage_azores_wording_20261123 import ARM, BASE, COMMON, common_rows, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_lisbon_azores_voyage_20261123 import body_mask, town
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_special_target_labels_20261115 import captured, native_copy, shots, verify_label
from scripts.verify_stock_encounter_names_20261121 import read_ram


WORK = live.ROOT / "stage"
ROM, PROOF = WORK / "Sea_Inspection_Prose_STAGED.nds", WORK / "stored_proof.json"
OUT = Path("translations/editorial_checkpoints/shared_display_20261123")
PANEL_REPORT, SHEET = OUT / "sea_inspections_current_20261123.json", OUT / "sea_inspections_current_20261123.png"
SOURCE_HISTORY = Path("translations/sea_responses_editorial_manuscript_v1.json")
VOICE_HISTORY = Path("work/analysis/sea_responses_fonts_v1558/native_font_research.json")
TABLE, PARENT, CALL = 0x021186E0, 0x02053DB8, 0x0206F674
EDITS = {
    2209: "O-oh, no... Will we get home alive?",
    2210: "Incredible... I can't fathom it!",
    2211: "Whoa! Never seen anything like it!",
    2212: "A-amazing... Something like that, out at sea?",
}
NOTES = {
    2209: ("A stammer of alarm, then a question about whether they'll get back alive.",
           "The direct question gives Charles a quicker, frightened delivery and keeps the whole thought together."),
    2210: ("Express astonishment and say the sight is beyond comprehension.",
           "Can't fathom it keeps this officer's measured register and restores the force of the Japanese negative."),
    2211: ("React with surprise and say this is the first sight of anything like it.",
           "The spoken fragment keeps the exuberant voice. Never seen anything like it preserves the first sighting."),
    2212: ("Stammer in amazement at the sight of something like that at sea.",
           "The two fragments follow the original astonishment. The final question is about the sighting."),
    2213: ("Marvel at the sheer sight and recognize a monster.",
           "Keep the blunt recognition and the complete short exclamation."),
    2214: ("Express surprise and ask whether the creature can be beaten.",
           "Keep the vocal reaction, challenge and colloquial that thing."),
    2215: ("Cry out and admit fear.",
           "Keep the direct admission and the distinct fearful cry."),
    2216: ("Marvel at the mystery of the sea.",
           "The existing contemplative register and trailing wonder fit the source and the single row."),
    306: ("The player cannot view the requested information.",
          "The direct notice fits this unsuccessful inspection and the return to Info Mode."),
}
GATES = ("source", "context", "localization", "naturalness", "formatting")


def actual_replays(arm, release):
    font = GameAsciiFont.from_arm9(arm)
    evidence, panels = {}, []
    for case, (model, label) in live.CASES.items():
        source = live.ROOT / case / "capture/capture_report.json"
        run = read(source)
        assert run["ROM_sha256"] == release["candidate_sha256"] and run["frames"] == 6750
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert run["battery_save_preloaded"]["source_sha256"] == read(live.HISTORY)["battery_save_preloaded"]["source_sha256"]
        fixture, = run["synthetic_condition_fixtures"]
        assert fixture["original_existing_model_ID"] == model and fixture["all_other4MiB_bytes_exact"]
        assert fixture["original_class_ID"] == model - 115
        frames = shots(run)
        shown = {n: captured(frames[n]) for n in (5700, 5950, 6300, 6750)}
        for n in shown:
            assert digest(frames[n]["path"]) == frames[n]["PNG_sha256"]
        tooltip = {n: verify_label(font, shown[n], label) for n in (5700, 6750)}
        panel_text = ("O-oh, no... Are we going to make it", "home alive?")
        reaction = body_mask(font, shown[5950], panel_text)
        notice = body_mask(font, shown[6300], ("You can't view that information!",))
        data = native_copy(arm, run, label, model - 115)
        evidence[case] = dict(model=model, visible_class=label, capture=reference(source), tooltip=tooltip,
            original_tooltip_copy=data, reaction=dict(message_ID=2209, lines=panel_text, mask=reaction),
            unavailable_notice=dict(message_ID=306, mask=notice), frames={n: frames[n] for n in shown})
        panels.append((label, shown[5700].crop((83, 254, 234, 302))))
    panels += [("Charles's reaction", shown[5950].crop((0, 272, 256, 345))),
               ("Inspection notice", shown[6300].crop((0, 287, 256, 338)))]
    sheet = Image.new("RGB", (1050, 4 * 174), "#263238")
    ink = ImageDraw.Draw(sheet)
    for i, (label, panel) in enumerate(panels):
        x, y = i % 2 * 525 + 5, i // 2 * 174
        ink.text((x, y + 5), label, fill="white")
        sheet.paste(panel.resize((panel.width * 2, panel.height * 2), Image.Resampling.NEAREST), (x, y + 21))
    if SHEET.exists():
        encoded = BytesIO()
        sheet.save(encoded, format="PNG")
        assert encoded.getvalue() == SHEET.read_bytes()
    else:
        sheet.save(SHEET)
    return evidence


def alternate_raw(arm, raw, actor):
    cpu, get = get_machine(arm, raw)
    duty = get(0xCB1A8) + 0x2090
    assert get(0x82478, duty, 7) == get(0x82BC4, duty, 3) == 18
    get(0x82BB8, duty, 3, actor)
    assert get(0x82478, duty, 7) == get(0x82BC4, duty, 3) == actor
    candidate = bytes(cpu.mem_read(BASE, len(raw)))
    assert candidate[:duty + 9 - BASE] == raw[:duty + 9 - BASE]
    assert candidate[duty + 10 - BASE:] == raw[duty + 10 - BASE:]
    return candidate


def first_layout(arm, common, raw, entry):
    result = consumer(arm, common, raw, {"patches": []}, 0x53D44, 7, TABLE)
    assert result["parent"] == PARENT and result["selector"] == TABLE
    assert bytes.fromhex(result["input_hex"]).rstrip(b" ") == entry.text.rstrip(b" ")
    body = bytes.fromhex(result["formatted_hex"])
    lines = [row.strip().decode("ascii") for row in body.split(b"\n")]
    assert 1 <= len(lines) <= 4 and all(1 <= len(line) <= 35 for line in lines)
    assert " ".join(lines) == entry.text.decode("ascii").strip()
    return body, lines, result


def stage():
    assert not any(p.exists() for p in (ROM, PROOF, PANEL_REPORT))
    release, approved = map(read, (live.RELEASE, live.REGISTERED_NAMES))
    path = Path(release["candidate"])
    assert digest(path) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, path))
    clean_arm, arm = clean.read_file(ARM), image.read_file(ARM)
    common = image.read_file(COMMON)
    assert digest_bytes(arm) == release["target_ARM9_sha256"] and digest_bytes(common) == release["target_COMMON_sha256"]
    assert clean_arm[0x6F66C:0x6F678] == arm[0x6F66C:0x6F678]
    assert clean_arm[TABLE - BASE:TABLE - BASE + 32] == arm[TABLE - BASE:TABLE - BASE + 32]
    bindings = {}
    for row in approved["records"]:
        b = row["registered_reference"]
        assert b["exact_hex"] == (row["english"].encode("ascii") + b"\0").hex()
        assert int.from_bytes(arm[b["pointer_field"]:b["pointer_field"] + 4], "little") == b["address"]
        bindings[row["model_ID"]] = dict(clean=row["source_reference"], installed=b, english=row["english"],
                                          justified_retention=row["localization_note"])
    scope = actual_replays(arm, release)
    for model in bindings:
        case = next(key for key, data in scope.items() if data["model"] == model)
        raw = read_ram(scope[case]["original_tooltip_copy"]["capture_RAM"])
        cpu, get = get_machine(arm, raw)
        obj = get(0xCB148) + 4 + model * 140
        start = get(0x1A4E0, obj)
        assert start == obj + 8 and get(0x11DB0, obj) == model - 115
        value = bytes(cpu.mem_read(start, 19))
        assert value == bytes.fromhex(bindings[model]["installed"]["exact_hex"]).ljust(19, b"\0")
        bindings[model]["initialized_model_name"] = dict(address=start, exact_19_bytes=value.hex())
        bindings[model]["visible_class"] = scope[case]["visible_class"]
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    before = common_rows(common, arm)
    edits = {}
    for n, prose in EDITS.items():
        text = prose.encode("ascii")
        assert len(text) <= len(before[n].text) and before[n].block == 23
        edits[n] = text.ljust(len(before[n].text), b" ")
    deployed, after, slots = owned_deployment(common, arm, before, edits)
    assert {a.message_id for a, b in zip(before, after, strict=True) if a != b} == EDITS.keys()
    assert all(slot["new_null_fields"] == 0 for slot in slots.values())

    raw = read_ram(scope["fish"]["original_tooltip_copy"]["capture_RAM"])
    raster, _, _ = town.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, pages = [], []
    for old in read(VOICE_HISTORY)["cases"]:
        n = old["message_ID"]
        actor_raw = alternate_raw(arm, raw, old["existing_actor_ID"])
        prior_body, prior_lines, _ = first_layout(arm, common, actor_raw, before[n])
        body, lines, native = first_layout(arm, deployed, actor_raw, after[n])
        assert prior_lines == old["lines"]
        if n in EDITS:
            assert len(lines) == (2 if n == 2212 else 1)
            if n == 2212:
                assert lines == ["A-amazing... Something like that,", "out at sea?"]
        else:
            assert body == prior_body
        pixels, glyphs = render_portrait(raster, arm, kanji, body)
        # The reused portrait verifier compares the complete native plane
        # with the independent font and checks the guarded row origins.
        assert [g["code"] for g in glyphs] == town.glyph_codes(body)
        pages.append((str(n), pixels))
        meaning, note = NOTES[n]
        jp, current, installed = source[n], before[n], after[n]
        assert all(b"%" not in entry.text for entry in (jp, current, installed))
        rows.append(dict(id=f"COMMON_MESSAGE_{n}", message_ID=n, file_path=COMMON, speaker=f"Lookout voice {n-2209}",
            context="One of eight original lookout reactions. The player selects the sea target, sees the reaction and gets the information notice.",
            source_meaning=meaning, source_reference=town.reference(jp), source_Japanese=jp.text.decode("cp932"), source_hex=jp.text.hex(),
            previous_English=current.text.decode("ascii"), current_reference=town.reference(current),
            english=installed.text.decode("ascii").strip(), staged_reference=town.reference(installed),
            current_hex=current.text.hex(), staged_hex=installed.text.hex(), localization_note=note,
            decision="revision" if n in EDITS else "retention", review=dict.fromkeys(GATES, True), lines=lines,
            native=native, prior_lines=prior_lines, full_native_ink_sha256=digest_bytes(pixels),
            observed_on_parent=n == 2209, offline_role_counterfactual=n != 2209))
    assert len(rows) == len(pages) == 8
    n = 306
    entry, jp = before[n], source[n]
    rows.append(dict(id=f"COMMON_MESSAGE_{n}", message_ID=n, file_path=COMMON, speaker="System",
        context="The same inspection notice follows the lookout's reaction and leads back to Info Mode.",
        source_meaning=NOTES[n][0], localization_note=NOTES[n][1], decision="retention",
        source_reference=town.reference(jp), source_Japanese=jp.text.decode("cp932"), source_hex=jp.text.hex(),
        current_reference=town.reference(entry), current_hex=entry.text.hex(), staged_reference=town.reference(after[n]),
        staged_hex=entry.text.hex(), english=entry.text.decode("ascii"), review=dict.fromkeys(GATES, True),
        observed_on_parent=True))
    assert after[n] == entry
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
                 encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=rows)
    validate_natural_dialogue_batch(batch)
    image.replace_file(COMMON, deployed)
    result = bytes(image.rom.save())
    assert bytes(image.rom.iconBanner) == NdsImage.open(path).rom.iconBanner
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == path.read_bytes()
    WORK.mkdir()
    with ROM.open("xb") as output:
        output.write(result)
    assert digest(ROM) == digest_bytes(result)
    previews = portrait_sheets(WORK, pages)
    write(PANEL_REPORT, dict(candidate=reference(path), registered_names=reference(live.REGISTERED_NAMES),
        all_five_model_names_fit_initialized_fields=bindings, inspection_replays=scope,
        captured_emulator_controller_with_encounter_fixture=True, original_role_and_information_notice_exact=True,
        unverified=["natural encounter spawns", "played special-target victory", "other indirect model-name uses", "handheld"],
        visual_preview=reference(SHEET), source_credit_added=0))
    write(PROOF, batch | dict(predecessor=reference(path), candidate=reference(ROM), clean=reference(CLEAN),
        changed_internal_files=[COMMON], changed_ids=sorted(EDITS), exact_old_parent_inverse=True,
        target_COMMON_sha256=digest_bytes(deployed), target_ARM9_sha256=digest_bytes(arm), slots=slots,
        prior_source_meaning=reference(SOURCE_HISTORY), prior_native_voices=reference(VOICE_HISTORY),
        current_play=reference(PANEL_REPORT), sheets=previews, actual_revised_ROM_replay_pending=True, source_credit_added=0))
    print("Verified all five current encounters and staged four reactions in their original COMMON slots.")


if __name__ == "__main__":
    stage()
