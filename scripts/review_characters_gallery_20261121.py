"""Review the current Gallery text against clean names and actual viewer output."""

from pathlib import Path
from struct import unpack_from

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.characters_gallery_text import BASE, TABLE, rows
from scripts import register_historic_sites_editorial_20261121 as current
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_characters_gallery_v525 import report
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base = current.base
ROOT = Path("work/characters_gallery_editorial_20261121")
PLAN = Path("work/analysis/characters_gallery_v525/run_plan.json")
OLDER = Path("E:/Rota Nova translations/Generated/work/emulation_v193/site_descriptions_v534_characters")
OLD_PROOF = Path("work/analysis/site_descriptions_v534/release_proof.json")
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
APPROVED = BOOK / "default_actor_names_current_20261120_v1.json"
BIANCA = Path("translations/maria310_integrated_final_review_v1.json")
OUTPUT = BOOK / "characters_gallery_editorial_20261121_v1.json"
COLOR = (230, 230, 230)


def c_string(data, start):
    return data[start:data.index(0, start) + 1]


def source(raw, row, arm, actual):
    clean_at = row["offset"]
    field = row.get("pointer_field")
    live_at = clean_at if field is None else unpack_from("<I", arm, field)[0] - BASE
    japanese = c_string(raw, clean_at)
    english = c_string(arm, live_at)
    assert japanese[:-1].decode("cp932") == row["Japanese"]
    assert english == row["English"].encode("ascii") + b"\0"
    assert c_string(actual, live_at) == english
    if field is not None:
        assert unpack_from("<I", actual, field)[0] == BASE + live_at
    refs = dict(source_reference=dict(offset=clean_at, pointer_field=field, exact_hex=japanese.hex()),
                current_reference=dict(offset=live_at, pointer_field=field, exact_hex=english.hex()))
    return refs


def actor_reference(index, clean_name, current_name, actors, clean_arm, ram, clean):
    if index == 41:
        prior = base.load(BIANCA)
        scene, = [r for r in prior["records"] if r["id"] == "DK4_MES_B55_R0133"]
        script = IlnkContainer.parse(clean.read_file(scene["file_path"])).blocks[scene["block"]]
        ref = scene["source_reference"]
        clean_text = bytes.fromhex(scene["source_hex"])
        start = ref["offset"]
        assert script[start:start + len(clean_text)] == clean_text
        assert f"＜{clean_name}＞" in scene["source_Japanese"] and scene["english"].startswith(current_name + ":")
        assert all(scene["review"].values()) and scene["actual_utterance_observed_in_disclosed_fixture"]
        return dict(story_review=str(BIANCA), record=scene["id"], file_path=scene["file_path"],
                    source_reference=ref, recorded_speaker=scene["speaker"],
                    reason="Bianca matches the clean named voice in Angelo's dream and the approved story spelling.")
    actor, field = actors[clean_name]
    assert field["current"]["text"] == current_name
    src, active = field["clean"], field["current"]
    assert c_string(clean_arm, src["offset"]) == bytes.fromhex(src["hex"]) + b"\0"
    assert unpack_from("<I", ram, field["offset"])[0] == active["pointer"]
    assert c_string(ram, active["pointer"] - BASE) == bytes.fromhex(active["hex"]) + b"\0"
    label_field = field["field"]
    scope = "given-name" if label_field == "primary" else "family-name"
    return dict(actor_ID=actor["actor_ID"], field=label_field, clean=src, current=active,
                reason=f"Retain {current_name}. The original card selects this {scope} form, which matches the approved actor field.")


def proof_mask(font, picture, text, x, y, region):
    ink, bounds = complete_mask(font, text, picture, x, y, COLOR)
    left, top, right, bottom = region
    assert left <= bounds[0] < bounds[2] <= right and top <= bounds[1] < bounds[3] <= bottom
    assert sum(pixel == COLOR for pixel in picture.crop(region).get_flattened_data()) == ink
    return dict(bounds=bounds, native_plane=region, complete_ink_pixels=ink)


def main():
    assert not OUTPUT.exists()
    release, ledger = map(base.load, (current.RELEASE, base.LEDGER))
    digest = base.digest(current.ROM)
    assert digest == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.stage.CLEAN) == release["clean_input_sha256"]
    clean, active = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    clean_arm, arm = (image.read_file(current.stage.ARM) for image in (clean, active))
    plan, actor_review, recorded = map(base.load, (PLAN, APPROVED, OLD_PROOF))
    old = base.load(OLDER / "capture_report.json")
    assert old["ROM_sha256"] == recorded["candidate_sha256"] and old["cold_boot"] and not old["savestate_loaded"]
    assert not old["callback_errors"]
    new = report(ROOT / "capture", digest)
    assert new["scripted_input_schedule"] == old["scripted_input_schedule"]
    assert new["frames"] == plan["final_frame"] and not new["earned_unlock_verified"]
    assert new["battery_save_preloaded"]["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    assert new["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    snapshot = new["read_only_RAM_snapshot"]
    snapshot_path = Path(snapshot["path"])
    assert snapshot["read_only_export"] and base.digest(snapshot_path) == snapshot["sha256"]
    ram = snapshot_path.read_bytes()
    assert len(ram) == 0x400000
    assert all(unpack_from("<I", data, TABLE + 42 * 4)[0] == 0 for data in (clean_arm, arm, ram))
    actors = {}
    candidates = {r["Japanese"][3:] for r in rows(clean_arm)[2:-1]}
    for row in actor_review["source_and_current_default_name_fields"]:
        for field in row["exact_fields"]:
            if field["clean"] and field["clean"]["text"] in candidates:
                japanese = field["clean"]["text"]
                assert japanese not in actors
                actors[japanese] = (row, field)
    assert set(actors) == candidates and len(actors) == 41

    a, b = map(shots, (old, new))
    font = GameAsciiFont.from_arm9(arm)
    title, description, *names = rows(clean_arm)
    records, headings, cases, crops = [], [], [], []
    for frame, row in zip(plan["frames"], names, strict=True):
        index, label = row["index"], row["English"]
        name = label[3:]
        affiliate = actor_reference(index, row["Japanese"][3:], name, actors, clean_arm, ram, clean)
        before, picture = captured(a[frame]), captured(b[frame])
        assert before.crop((0, 0, 256, 192)).tobytes() == picture.crop((0, 0, 256, 192)).tobytes()
        tm = proof_mask(font, picture, title["English"], 98, 195, (92, 194, 164, 207))
        dm = proof_mask(font, picture, description["English"], 16, 217, (16, 216, 152, 232))
        mask = proof_mask(font, picture, label, 128 - 3 * len(label), 263, (32, 262, 224, 276))
        headings.extend((tm, dm))
        cases.append(dict(frame=frame, exact_portrait_pixels=256 * 192, checked_masks=[tm, dm, mask],
                          before=a[frame], actual=b[frame]))
        crops.append(picture.crop((74, 256, 182, 281)))
        records.append(dict(id=row["id"], file_path=current.stage.ARM, speaker="Characters Gallery",
                            clean_Japanese=row["Japanese"], english=label, decision="retention",
                            context="The numbered character card uses the short name chosen in the original portrait viewer.",
                            source_meaning=f"Gallery entry {index:02d} with the character's selected short name.",
                            localization_note=affiliate["reason"], approved_name_reference=affiliate,
                            gameplay_frame=frame, review=dict.fromkeys(REQUIRED_REVIEW_GATES, True),
                            **source(clean_arm, row, arm, ram)))
    for row, reason in ((title, "Characters is the familiar menu heading for the cast."),
                        (description, "The story's main cast is a natural summary of the original description.")):
        records.insert(0, dict(id=row["id"], file_path=current.stage.ARM, speaker="Characters Gallery",
            clean_Japanese=row["Japanese"], english=row["English"], source_meaning=reason,
            context="The title and introduction stay in place as the numbered character cards advance.",
            localization_note=reason, decision="retention", review=dict.fromkeys(REQUIRED_REVIEW_GATES, True),
            **source(clean_arm, row, arm, ram)))
    screen = captured(b[plan["wrap"]])
    first = captured(b[plan["frames"][0]])
    assert screen.crop((0, 0, 256, 276)).tobytes() == first.crop((0, 0, 256, 276)).tobytes()
    for number in (plan["back"], plan["final_frame"]):
        previous, returned = captured(a[number]), captured(b[number])
        assert previous.crop((0, 0, 256, 192)).tobytes() == returned.crop((0, 0, 256, 192)).tobytes()
    sheet = Image.new("RGB", (1296, 350), "#20272b")
    for index, crop in enumerate(crops):
        sheet.paste(crop.resize((216, 50), Image.Resampling.NEAREST), (index % 6 * 216, index // 6 * 50))
    path = ROOT / "complete_numbered_names.png"
    sheet.save(path)
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES), records=records, registered_release=str(current.RELEASE),
        candidate_sha256=digest, emulator_cases=cases, complete_masks=len(headings) + len(cases),
        original_controls=True, wrapped_to_first_card=True, returned_frames=[plan["back"], plan["final_frame"]],
        initialized_collection=True, natural_unlock=False, hardware=False, new_credit=0, rom_changed=False,
        contact_sheet=dict(path=str(path), sha256=base.digest(path)),
        evidence={str(p): base.digest(p) for p in (ROOT/"capture/capture_report.json", ROOT/"fixture.json",
            OLDER/"capture_report.json", current.RELEASE, PLAN, APPROVED, BIANCA, snapshot_path)})
    validate_natural_dialogue_batch(batch)
    base.save(OUTPUT, batch)
    print(f"Reviewed {len(records)} exact retentions and {batch['complete_masks']} native text masks.")


if __name__ == "__main__":
    main()
