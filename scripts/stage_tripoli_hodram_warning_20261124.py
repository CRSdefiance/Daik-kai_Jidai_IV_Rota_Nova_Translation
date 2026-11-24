"""Review and stage Hodram's first Tripoli warning from an ordinary voyage."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import observe_syracuse_westbound_20261124 as play
from scripts import stage_genoa_alternate_dialogue_20261123 as fixed
from scripts import stage_istanbul_tavern_rumor_20261124 as paired
from scripts import stage_tunis_shop_advice_20261124 as common_workflow
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_moonlit_violin_20261121 import bytes_for


ARM, COMMON, STORY, BLOCK = fixed.ARM, fixed.COMMON, fixed.STORY, 51
RELEASE, KEY, HOLD, END = play.RELEASE, "DK4_MES_B51_R0014", 8910, 12210
played = SimpleNamespace(RELEASE=RELEASE)
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_tripoli_hodram_warning")
ROM, STORED = ROOT / "Tripoli_Hodram_Warning_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
BEFORE, AFTER = play.ROOT / "capture/capture_report.json", ROOT / "replay/capture/capture_report.json"
PAIRED = ROOT / "paired_gameplay.json"
PREVIEW, SHEET = (ROOT / f"{name}_1_20261123.png" for name in ("tripoli_warning_native", "tripoli_warning_paired"))
PRIOR = Path("releases/all_routes_editorial_20261121_hodram_alexandria_tutorial_candidate")
OUT = panels.OUT.with_name("tripoli_hodram_warning_review_20261124.json")
ENGLISH = "There's someone around here who's bad news. Trust me. Head for safer waters."
CONTEXT = ("Hodram docks at newly discovered Tripoli. The port worker warns him off. Hodram asks why, "
           "Charles echoes the unnamed danger, and Gerhard privately wonders who the worker might mean.")
HOLD_FOR = dict(zip((6, 10, 14, 32, 39), (8470, 8690, HOLD, 9130, 9350), strict=True))
RETENTIONS = {
    6: "The blunt warning fits first contact with the fleet. Both the worker's uncertainty and the southern Mediterranean remain explicit.",
    10: "The brief question and hesitation fit Hodram's guarded reaction and leave the explanation to the worker.",
    32: "Charles repeats the worker's description with surprise while the person's identity remains open.",
    39: "Gerhard's parenthesized thought makes recognition possible, without turning it into a spoken identification.",
}
COMMON_HOLDS = (
    (7830, 1296, "Manuel Almeida", (), ("Admiral, we've spotted a port!",),
     "Manuel reports seeing a port and addresses the fleet commander.",
     "The exclamation fits the lookout's discovery and keeps the original address."),
    (8030, 297, "", ("Tripoli",), ("Discovered Tripoli.",),
     "The game announces discovery of the named port.",
     "The concise notice distinguishes the discovery from the confirmation that follows."),
    (8250, 65, "Charles Rochefort", ("Tripoli",), ("Dock at Tripoli?",),
     "Charles asks whether to call at the named port.",
     "The short question leaves the Yes or No choice to Hodram and preserves the port substitution."),
    (9790, 49, "Port Worker", ("282",), ("Want to resupply for 282 gold?",),
     "The worker offers resupply at the quoted price.",
     "The informal offer makes the charge and the decision explicit before money changes hands."),
    (10230, 85, "", ("38",), ("Sailing days left: about 38.",),
     "The provisions allow about 38 days at sea.",
     "About carries the source's estimate and the count precedes the departure-mode choice."),
    (11550, 637, "Charles Rochefort", (), ("There's no route to that port.",),
     "Charles says there is no route to the selected destination.",
     "The direct reply explains the refused Auto Move to Lisbon without implying the port is inaccessible by sailing."),
)


def sheet(name, figures):
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=STORED),
                        argdefs=panels.sheets_for.__defaults__)
    result, = draw(name, figures)
    return result


def source_command(block, row):
    source = row["source_reference"]
    payload = bytes.fromhex(source["exact_hex"])
    start = source["command_offset"]
    returned = block[start:start + 6 + len(payload)]
    assert returned[5:-1] == payload and returned[-1] == 0
    assert sha256(block).hexdigest() == source["block_sha256"]
    return returned, source | dict(exact_command_hex=returned.hex())


def anchor_rows(release, clean, image, frames, screenshots, arm, paint, font, kanji):
    historical = PRIOR / "verification/registered_review.json"
    assert digest(historical) == read(PRIOR / "checksums.json")["verification/registered_review.json"]
    reviewed = [row for row in read(historical)["records"] if row["block"] == BLOCK]
    assert {row["source_record_index"] for row in reviewed} == HOLD_FOR.keys()
    clean_archive, current_archive = (rom.read_file(STORY) for rom in (clean, image))
    a, b = (IlnkContainer.parse(archive).blocks[BLOCK] for archive in (clean_archive, current_archive))
    records = []
    for row in reviewed:
        ordinal, key, actor = (row[field] for field in ("source_record_index", "id", "speaker"))
        original, src = source_command(a, row)
        ref = row["registered_reference"]
        current = bytes.fromhex(ref["exact_command_hex"])
        at = ref["offset"]
        assert b[at:at + len(current)] == current and original[:6] == current[:6]
        assert sha256(b).hexdigest() == ref["block_sha256"]
        assert bytes_for(original).decode("cp932") == row["Japanese"]
        english = " ".join(bytes_for(current).decode("ascii").split())
        assert english == row["english"]
        layout = paint(arm, kanji, bytes_for(current))
        page, = layout["pages"]
        assert page["native_independent_plane_equal"] and layout["complete_consumed_bytes"] == len(bytes_for(current))
        frame = HOLD_FOR[ordinal]
        body = bytes.fromhex(page["native_plane_hex"])
        assert panels.mask_check(body, 216, screenshots[frame]), (key, frame)
        plate = panels.nameplate(font, actor, screenshots[frame])
        note = ("Head for safer waters gives the same protective advice in natural nautical English. "
                "Trust me keeps the worker's insistence and the person stays unnamed."
                if key == KEY else RETENTIONS[ordinal])
        records.append(dict(id=key, block=BLOCK, file_path=STORY, speaker=actor, context=CONTEXT,
            clean_Japanese=row["Japanese"], english=ENGLISH if key == KEY else english, previous_English=english,
            source_meaning=row["source_meaning"], localization_note=note, source_reference=src,
            current_reference=dict(file_path=STORY, block=BLOCK, command_offset=at, exact_command_hex=current.hex(),
                archive_sha256=sha256(current_archive).hexdigest(), block_sha256=sha256(b).hexdigest()),
            decision="revision" if key == KEY else "retention", review=dict.fromkeys(GATES, True),
            ordinary_hold=dict(capture=frames[frame], nameplate=plate, exact_body_plane_sha256=sha256(body).hexdigest())))
    return records


def common_rows(source, current, frames, screens, calls, font):
    out = []
    for frame, key, speaker, args, lines, meaning, reason in COMMON_HOLDS:
        a, b = [event for event in calls if event["message_ID"] == key and 0 < frame - event["frame"] < 950]
        assert a["PC"] == 0x0205528C and b == a | {"PC": 0x020534F4}
        ja, en = source[key], current[key]
        assert ja.text.count(b"%s") == len(args) == en.text.count(b"%s")
        assert (en.text.decode("ascii") % args).split() == " ".join(lines).split()
        make_ref = lambda row: panels.text_reference(row) | dict(exact_hex=row.text.hex())
        out.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker=speaker or "System",
            context=CONTEXT + " The voyage also includes resupply and the unavailable Auto Move to Lisbon.",
            clean_Japanese=ja.text.decode("cp932"), english=en.text.decode("ascii").strip(),
            source_reference=make_ref(ja), current_reference=make_ref(en), installed_reference=make_ref(en),
            source_meaning=meaning, localization_note=reason, decision="retention", review=dict.fromkeys(GATES, True),
            ordinary_hold=dict(capture=frames[frame], arguments=args, requests=[a, b],
                complete_body_ink=panels.exact_body(font, lines, screens[frame]),
                nameplate=panels.nameplate(font, speaker, screens[frame]))))
    return out


def stage():
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    capture = FunctionType(panels.capture.__code__, vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent)))
    frames, calls, evidence = capture(play.ROOT.name, release)
    assert max(frames) == END and {284, 318, 750, 751, 752}.isdisjoint(row["message_ID"] for row in calls)
    screenshots = {frame: panels.picture(shot) for frame, shot in frames.items()}
    clean, image = map(NdsImage.open, (CLEAN, release["candidate"]))
    original, before = map(fixed.previous.native.files, (clean, image))
    arm, kanji = before[ARM], image.read_file("/GRP/KANJI.FNT")
    font = GameAsciiFont.from_arm9(arm)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(before[COMMON]).hexdigest() == release["target_COMMON_sha256"]
    assert paired.continuity.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    paint = panels.town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    records = anchor_rows(release, clean, image, frames, screenshots, arm, paint, font, kanji)
    source_rows = panels.common_message_entries(original[COMMON], original[ARM])
    current_rows = panels.common_rows(before[COMMON], arm)
    companion = common_rows(source_rows, current_rows, frames, screenshots, calls, font)
    wallet = {frame: panels.find_mask(font, text, screenshots[frame], (55, 348, 139, 366))
              for frame, text in ((9570, "38371"), (10010, "38089"))}
    assert 38371 - 282 == 38089
    return_to_port = panels.find_mask(font, "Tripoli", screenshots[END], (25, 14, 130, 31))

    src, prior = (IlnkContainer.parse(data[STORY]) for data in (original, before))
    row, = [row for row in records if row["id"] == KEY]
    a = panels.exact_command(src.blocks[BLOCK], row["source_reference"])
    b = panels.exact_command(prior.blocks[BLOCK], row["current_reference"])
    proposal = dict(id=KEY, english=ENGLISH, protected_phrases=("who's bad news.", "Head for safer waters."))
    encoded, plan = panels.layout.plan_progressive(proposal, b[5], bytes_for(b), bytes_for(a))
    assert plan["expected_native_pages"] == 1 and len(encoded) <= len(bytes_for(b))
    assert any("Head for safer waters." in line for line in plan["lines"])
    display = paint(arm, kanji, encoded)
    page, = display["pages"]
    plane = bytes.fromhex(page["native_plane_hex"])
    assert page["native_independent_plane_equal"] and display["complete_consumed_bytes"] == len(encoded)
    draft = row | dict(installed_reference=row["current_reference"], proposed_English=ENGLISH,
        offline_preflight=dict(formatter_plan=plan, physical_source_and_installed_selectors=a[5],
                               native_plane_sha256=sha256(plane).hexdigest()))
    result, (edit,), extents = fixed.previous.apply_block(
        src.blocks[BLOCK], prior.blocks[BLOCK], arm, [draft], paint, kanji, fixed.explicit_walk())
    prior.blocks[BLOCK] = result
    updated = prior.to_bytes()
    directory_end = 8 + 4 * (len(prior.blocks) + 1)
    assert updated[:directory_end] == before[STORY][:directory_end]
    image.replace_file(STORY, updated)
    final = fixed.previous.native.files(image)
    assert final.keys() == before.keys() and {p for p in final if final[p] != before[p]} == {STORY}
    guard = bind_registered_story_percent_guard(paired.continuity.previous.guard_spec())(original, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    candidate = bytes(image.rom.save())
    image.replace_file(STORY, before[STORY])
    assert sha256(image.rom.save()).hexdigest() == release["candidate_sha256"]

    ROOT.mkdir(exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == candidate
    else:
        ROM.write_bytes(candidate)
    assert fixed.previous.native.files(NdsImage.open(ROM)) == final
    preview = Image.new("RGB", (256, 384), (250, 245, 226))
    preview.paste(Image.frombytes("L", (216, 64), bytes(12 if pix else 245 for pix in plane)), (16, 296))
    native = sheet("tripoli_warning_native", [("Proposed native layout", preview)])
    assert native == reference(PREVIEW)
    proof = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=records + companion, candidate_sha256=release["candidate_sha256"],
        ordinary_gameplay=True, evidence=evidence, controller=reference(play.ROOT / "controller.jsonl"),
        all_common_requests=calls, port_wallet=wallet, port_return=return_to_port,
        review_anchor=reference(PRIOR / "verification/registered_review.json"),
        mission_scope="Ordinary sailing from Syracuse to Tripoli, resupply and a refused Auto Move. No village reached.",
        native_preview=native, new_editorial_credit=0)
    validate_natural_dialogue_batch(proof)
    write(OUT, proof)
    write(STORED, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=release["target_COMMON_sha256"], target_SC1_sha256=sha256(updated).hexdigest(),
        target_block_sha256=sha256(result).hexdigest(), source_preflight=reference(OUT),
        edit=edit, native_command_extents=extents, whole_parent_inverse=True,
        unchanged_archive_directory=True, source25=guard, native_preview=native))
    print(f"Reviewed five Tripoli story turns and six surrounding shared records. Staged only Hodram B51 R14. {digest(ROM)}")


def replay(stored):
    old = read(BEFORE)
    assert old["ROM_sha256"] == stored["predecessor_sha256"] and digest(ROM) == stored["candidate_sha256"]
    frames = set(panels.shots(old, "_navigation.png")) | {6220, 6552, 6890}
    paired.capture(old, ROM, AFTER.parent, END, sorted(frames))


def verify(stored):
    before, after = map(read, (BEFORE, AFTER))
    assert before["ROM_sha256"] == stored["predecessor_sha256"] and after["ROM_sha256"] == stored["candidate_sha256"] == digest(ROM)
    assert before["scripted_input_schedule"] == after["scripted_input_schedule"]
    assert before["battery_save_preloaded"]["source_sha256"] == after["battery_save_preloaded"]["source_sha256"]
    assert before["core_DLL_sha256"] == after["core_DLL_sha256"] and before["core_options"] == after["core_options"]
    assert after["cold_boot"] and not after["savestate_loaded"] and not after["callback_errors"]
    assert not any(value for key, value in after.items() if key.startswith("synthetic_"))
    old, new = panels.shots(before, "_navigation.png"), panels.shots(after, "_cold_boot.png")
    assert old.keys() <= new.keys()
    unchanged = []
    for frame in old:
        if frame != HOLD:
            assert old[frame]["framebuffer_sha256"] == new[frame]["framebuffer_sha256"], frame
            unchanged.append(frame)
    image = NdsImage.open(ROM)
    arm, kanji = image.read_file(ARM), image.read_file("/GRP/KANJI.FNT")
    paint = panels.town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    command = bytes.fromhex(stored["edit"]["after_hex"])
    body = bytes_for(command)
    layout = paint(arm, kanji, body)
    page, = layout["pages"]
    plane = bytes.fromhex(page["native_plane_hex"])
    assert sha256(plane).hexdigest() == stored["edit"]["page_sha256"]
    a, b = panels.picture(old[HOLD]), panels.picture(new[HOLD])
    bounds = ImageChops.difference(a, b).getbbox()
    assert bounds and 16 <= bounds[0] < bounds[2] <= 245 and 296 <= bounds[1] < bounds[3] <= 360
    font = GameAsciiFont.from_arm9(arm)
    name = panels.nameplate(font, "Port Worker", b)
    assert name == panels.nameplate(font, "Port Worker", a) and panels.mask_check(plane, 216, b)
    assert END in unchanged and 9570 in unchanged and 11550 in unchanged
    visual = sheet("tripoli_warning_paired", [("Previous", a), ("Revised", b)])
    assert visual == reference(SHEET)
    write(PAIRED, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        source=reference(BEFORE), replay=reference(AFTER), stored=reference(STORED), ordinary_gameplay=True,
        changed_frame=dict(frame=HOLD, body_mask_sha256=sha256(plane).hexdigest(), nameplate=name, bounds=bounds),
        unchanged_frames=unchanged, visual=visual))
    print(f"The revised Tripoli warning and {len(unchanged)} matching companion frames passed.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "replay", "verify", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action in ("patch", "startup"):
        FunctionType(common_workflow.release_check.__code__, vars(common_workflow) | globals())(read(STORED), action)
    else:
        globals()[action](read(STORED))
