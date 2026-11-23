"""Review the Deck's personal, Shipwright and Doctor dialogue and stage the revised text."""

from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import register_lil_red_dye_20261119 as parent
from scripts import work_comments_layout_v843 as formatter
from scripts.prepare_work_comments_v842 import snapshot
from scripts.probe_work_fonts_v843 import execute, expected_pixels, prepare_model
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.stage_square_shop_followup_20261119 import ARM, CLEAN, COMMON, PENDING, precedent as workflow

base, native = parent.base, parent.native
ROOT = Path("work/deck_comments_20261119/staged_v2")
ROM = ROOT / "Deck_Comments_STAGED.nds"
PROOF = ROOT / "staged.json"
HISTORY = (
    Path("translations/personal_chatter_editorial_final_review_v1.json"),
    Path("translations/work_comments_editorial_final_review_v1.json"),
)
NUMBERS = tuple(range(1361, 1410))
ACTORS = {1373: 12, 1374: 13, 1387: 16, 1406: 0}
EDITS = {
    1373: ("My blade shines beautifully, as always...",
           "Yukihisa admires his blade's familiar shine. Keep the original measured diction and the compliment together."),
    1374: ("There! Turned out well, didn't it?",
           "Cesare's proud little flourish leads straight into a conversational tag, as if inviting agreement."),
    1387: ("Might as well make spare parts...",
           "Gerhard is thinking aloud about making spares in advance. The casual omitted subject suits the unhurried decision."),
    1406: ("Guys like Clau get hurt so easily...",
           "Rafael uses the familiar Clau from the source and the opening. His aside explains why he keeps medicine ready."),
}
RETENTIONS = {
    1361: "Rafael's pleased hum and warm appraisal suit a moment of enjoying the sound.",
    1362: "Hodram's pauses and restrained approval carry the quiet satisfaction of judging his own work.",
    1363: "Lil's sleepy exasperation uses Camille's approved name and sits between two snores.",
    1364: "Maria's brief, appreciative comment has the same understated delivery as the Japanese.",
    1365: "Janus's acknowledgment and appreciation sound like someone listening to a story.",
    1366: "Claudio's interrupted count and effort preserve the joke in his strenuous exercise.",
    1367: "Julio's drawn-out reaction and familiar expression carry the relish in the Japanese.",
    1368: "Cristina's sung opening and cheerful explanation preserve the two beats of her dancing comment.",
    1369: "Arcadius's pauses convey reading and coming to an understanding as the thought unfolds.",
    1370: "Camille's first thought sets up the quiet admission. The existing pause leaves the full reaction on the next row.",
    1371: "Xien's concise maxim carries both the warrior and continual practice.",
    1372: "Jam's admiration of the rod leads naturally to his eagerness for a sizable catch.",
    1375: "Emilio's delighted reaction leads into the joke about sneaking food. Both lines are complete spoken beats.",
    1376: "Angelo's annoyed click and complaint preserve the specific effect of sea air on his hair.",
    1377: "Gerhard's solitary sword practice and the calming effect read naturally in one quiet thought.",
    1378: "Al's boast about fists and decision to keep training land as separate beats in his rough register.",
    1379: "Charles trails off as he mixes the medicine, then voices his sudden realization.",
    1380: "Carlo's mumble and brief nodding action preserve the rhythm of the sleep gag.",
    1381: "Fernando's casual 'wanna' preserves the blunt, familiar way he voices the urge to gamble.",
    1382: "Ian's initial repeated 'Stronger' is emphatic. The full second row resolves the thought.",
    1383: "Samwell praises the taste in his sleep. The pauses and return to snoring mark the joke.",
    1384: "Manuel's three observations read as a complete list before his satisfied verdict.",
    1385: "Sera's gentle fragments sound like speaking to her flowers. The watering and reaction are distinct thoughts.",
    1386: "The voice leaves the thought hanging after a natural reminder to prepare the spare parts in advance.",
    1388: "The quick wear and the problem of keeping up read as cause and reaction.",
    1389: "The repetition and immediate breakage come through in an exasperated contrast across two rows.",
    1390: "The abrupt cry and 'whacked' fit the comic accident without specifying a tool.",
    1391: "The thoughtful pause and quiet approval preserve the understated evaluation.",
    1392: "The bright announcement and eagerness to make more are two short, complete beats.",
    1393: "The speaker's small discovery grows into admiring praise, with the source's reflective finish.",
    1394: "Rafael's conversational self-reminder preserves the need to keep making parts.",
    1395: "Hodram's practical preparation remains firm and unhurried. 'Spare parts' and 'while I can' each stay together.",
    1396: "Lil's quick hesitation and direct question express uncertainty about her work.",
    1397: "Maria's matter-of-fact confidence sounds natural in this role.",
    1398: "The salve shortage and decision form two complete thoughts. 'Salve' preserves the wound remedy.",
    1399: "The repeated ingredients stay clear. The existing break keeps 'this herb' and 'into the medicine' intact.",
    1400: "The smell and the pragmatic defense preserve the source's comic contrast.",
    1401: "The full first sentence supplies the reason, and the second states the need to make medicine.",
    1402: "The shout is a separate exclamation. The complete announcement fills the next row and keeps the remedy together.",
    1403: "The quiet pause and 'should' keep the speaker's tentative judgment.",
    1404: "The pause before 'Yuck!' lands the tasting joke in one line.",
    1405: "The tentative 'seems' and measured opening fit the original voice. The period fits the verified 36th cell.",
    1407: "Hodram's first-person resolve sounds natural. The continuation keeps 'medicinal herbs' together.",
    1408: "Lil's trailing observation and full question preserve the shift from surprise to concern.",
    1409: "Maria credits Xien and the usable knowledge he taught her. 'Chinese medicine' and the final verb phrase stay intact.",
}


def native_lines(text):
    # Keep Yukihisa's complete observation together before the trailing aside.
    protect = {("blade", "shines"), ("shines", "beautifully")}
    layout = FunctionType(formatter.layout.__code__, formatter.layout.__globals__ | {
        "KEEP_TOGETHER": formatter.KEEP_TOGETHER | protect,
    })
    return layout(text)


def current_pixels(arm, font, events, mode, *, background=0):
    # The registered right-bound painter retains the current one-pixel Y offset.
    shifted = [g | {"y": g["y"] + 1} if g["kind"] == "ascii" else g for g in events]
    return expected_pixels(arm, font, shifted, mode, background=background)


def main():
    assert not PROOF.exists()
    release, ledger, pending = map(base.load, (parent.RELEASE, base.LEDGER, PENDING))
    assert base.digest(CLEAN) == release["clean_input_sha256"] == pending["clean_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    clean, previous = map(base.NdsImage.open, (CLEAN, parent.ROM))
    clean_arm, arm, common = clean.read_file(ARM), previous.read_file(ARM), previous.read_file(COMMON)
    source = workflow.common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    entries = workflow.owned_entries(common, arm, directory)
    historical = {row["message_id"]: row for path in HISTORY for row in base.load(path)["records"]}
    assert sorted(historical) == list(NUMBERS) == sorted(EDITS.keys() | RETENTIONS.keys())
    assert EDITS.keys().isdisjoint(RETENTIONS)
    credited = {(row["file_path"], row["id"]) for row in ledger[base.CONTEXT]["integrated_record_keys"]}

    rows, storage = {}, {}
    for n in NUMBERS:
        original, installed, prior = source[n], entries[n], historical[n]
        assert (COMMON, prior["id"]) in credited
        assert all(prior["review"].values()) and prior["source_hex"] == original.text.hex()
        assert prior["native_argument_count"] == 0 and all(b"%" not in text for text in (original.text, installed.text))
        raw = installed.text.decode("ascii")
        old_lines = [line.rstrip(" ") for line in raw.split("\n")]
        previous_english = " ".join(old_lines)
        assert previous_english == prior["english"] and old_lines == prior["generated_native_lines"]
        assert all(0 < len(line) <= formatter.WIDTH for line in old_lines) and len(old_lines) <= formatter.MAX_LINES
        english, note = EDITS[n] if n in EDITS else (previous_english, RETENTIONS[n])
        lines = native_lines(english) if n in EDITS else old_lines
        if n in EDITS:
            storage[n] = formatter.serialize(lines)
        rows[n] = {key: prior[key] for key in ("id", "speaker", "context", "source_meaning")}
        rows[n].update(message_ID=n, file_path=COMMON, clean_Japanese=original.text.decode("cp932"),
            previous_English=previous_english, english=english, localization_note=note,
            decision="revision" if n in EDITS else "retention",
            finding="wrap" if n in EDITS and english == previous_english else "prose" if n in EDITS else "retention",
            source_reference=workflow.reference(original), current_reference=workflow.reference(installed),
            source_hex=original.text.hex(), current_hex=installed.text.hex(), original_substitution_count=0,
            previous_visible_lines=old_lines, visible_lines=lines, review=dict.fromkeys(REQUIRED_REVIEW_GATES, True))

    repack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    target_common, target_arm, rebound, allocation = repack(common, arm, rows, storage)
    assert allocation["all_41_blocks_fit_8KiB"] and allocation["changed_visible_templates"] == list(EDITS)
    for row in pending["records"]:
        entry = rebound[row["message_ID"]]
        assert row["current_reference"] == workflow.reference(entry) and row["current_hex"] == entry.text.hex()
    for n, row in rows.items():
        row.update(staged_reference=workflow.reference(rebound[n]), staged_hex=rebound[n].text.hex())

    previous.replace_file(ARM, target_arm)
    previous.replace_file(COMMON, target_common)
    target = bytes(previous.rom.save())
    previous.replace_file(ARM, arm)
    previous.replace_file(COMMON, common)
    assert bytes(previous.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == target
    else:
        ROM.write_bytes(target)
    rom = base.NdsImage.open(ROM)
    assert rom.read_file(COMMON) == target_common and rom.read_file(ARM) == target_arm
    runtime = workflow.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    current = workflow.with_components(runtime, target_arm, target_common)
    cpu, get, provider = current.machine(target_arm, target_common, current.raw, current.plan)
    for n, row in rows.items():
        text = rebound[n].text + b"\0"
        assert bytes(cpu.mem_read(get(0x5528C, n), len(text))) == text
        assert bytes(cpu.mem_read(get(0x5528C, n), len(text))) == text
    assert provider.reads

    # The archived room snapshot has the right widget and actor data but predates
    # the current ASCII font and renderer. Bind them to this parent's own startup.
    draw_ranges = ((0xD16B4, 0xD1898), (0x125A20, 0x126000))
    assert all(current.raw[a:b] == target_arm[a:b] for a, b in draw_ranges)
    ui, ui_receipt = snapshot("personal_cabin_v840_838_Charles_after", 4600)
    npc, npc_receipt = snapshot("personal_cabin_v840_838_Charles_after", 3200)
    rafael, rafael_receipt = snapshot("personal_activity_v839_838_Rafael_later", 3200)
    cases = []
    sheet = Image.new("RGB", (452, len(EDITS) * 103), "#293340")
    draw = ImageDraw.Draw(sheet)
    paint = FunctionType(execute.__code__, execute.__globals__ | {"expected_pixels": current_pixels})
    for index, n in enumerate(EDITS):
        actor, role = ACTORS[n], 12 if n < 1386 else 13 if n < 1398 else 14
        raw = rafael if n == 1406 else npc
        fixture, fixture_proof = prepare_model(target_arm, raw, actor, role, ui)
        display = bytearray(fixture)
        for start, end in draw_ranges:
            display[start:end] = current.raw[start:end]
        case, plane = paint(rom, bytes(display), actor, role, n, rebound[n].text, rows[n]["visible_lines"])
        assert case["complete_native_copy_macro_draw_and_ABI"]
        assert case["independent_authored_words_at_x0_12px_rows_match_every_pixel"]
        assert not any(plane[y*252+x] for y in range(60, 96) for x in range(216, 252))
        case.update(fixture=fixture_proof, all_body_ink_inside_216x36=True)
        cases.append(case)
        image = Image.frombytes("L", (252, 96), bytes(0 if v else 255 for v in plane)).crop((0, 60, 216, 96))
        y = index * 103
        draw.text((10, y+3), f"COMMON {n}   {rows[n]['speaker']}", fill="white")
        sheet.paste(image.resize((432, 72), Image.Resampling.NEAREST), (10, y+21))

    preview = ROOT / "revised_deck_pages.png"
    sheet.save(preview)
    review = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES), candidate_sha256=base.digest(ROM), records=list(rows.values()))
    validate_natural_dialogue_batch(review)
    base.save(PROOF, review | dict(parent_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        entire_parent_inverse=True, target_COMMON_sha256=native.digest(target_common), target_ARM9_sha256=native.digest(target_arm),
        allocation=allocation, native_display=cases, initialized_offline_snapshots=[ui_receipt, npc_receipt, rafael_receipt],
        parent_runtime=runtime.receipt(), current_font_and_draw_ranges=draw_ranges, warm_and_cold_actual_loader_checks=2*len(rows),
        sheets=[dict(path=str(preview), sha256=base.digest(preview))], pending_references_exact=True,
        source_proofs={str(p): base.digest(p) for p in (*HISTORY, parent.RELEASE, PENDING)}))
    print(f"Reviewed {len(rows)} Deck lines and rendered {len(cases)} revisions in the native panel.", flush=True)


if __name__ == "__main__":
    main()
