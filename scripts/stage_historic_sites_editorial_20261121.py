"""Rereview the nineteen reachable Historic Sites captions and descriptions."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into, unpack_from
import sys

from PIL import Image, ImageDraw
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.gallery_caption_bounds import validate as event_captions
from dk4tool.patch.historic_site_names import TABLE as NAME_TABLE
from dk4tool.patch.site_descriptions import BASE, DESCRIPTION_TABLE, IMAGE_TABLE, formatted
from scripts import headless_desmume_v193 as emulator
from scripts import register_hangzhou_veracruz_trends_20261121 as parent
from scripts.compile_scene_caption_allocation import pack
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_site_descriptions_v534 import paragraph


base, native = parent.base, parent.native
ARM, CLEAN = native.ARM, native.CLEAN
PREVIEW = Path("work/historic_sites_editorial_20261121")
LAYOUT_TRIALS = tuple(Path(f"work/historic_sites_editorial_20261121_v{n}") for n in (2, 3))
ROOT = Path("work/historic_sites_editorial_20261121_v4")
ROM, PROOF = ROOT / "Historic_Sites_STAGED.nds", ROOT / "staged.json"
LIVE = ROOT / "gallery_verified.json"
GALLERY = Path("work/analysis/site_descriptions_v534")
PLAN = Path("work/analysis/site_descriptions_v529")
MANUSCRIPT = Path("translations/historic_site_description_manuscript_v3.json")
NAMES = Path("translations/historic_site_names_v2.json")
ALLOCATION = GALLERY / "prepared_stage.json"
REVISIONS = {
    3: ("A wooden church in Stockholm with imagery from Christianity and Norse myth. Discover it to gain 1 influence.",
        "Restore the explicit Norse mythology behind the decorations while keeping the Christian imagery and reward."),
    6: ("An oval arena begun by Roman emperor Vespasian in the 1st century. It holds large crowds. Explore from Genoa to find it and gain 5 influence.",
        "Restore the emperor's Roman title and the arena's large capacity as a fact about its use."),
    7: ("A marble temple built in Athens in the late 5th century BC. Its main chamber holds a statue of Athena, the city's patron goddess. Find it to gain 3 influence.",
        "The Japanese specifies a statue of Athena in the chamber. Keep the complete influence amount together.",
        ("gain 3 influence.",)),
    10: ("A grand mud mosque in Djenne, a West African city that flourished south of the Sahara. Explore from Sao Jorge to discover it and gain 10 influence.",
         "Use the source's past tense for Djenne's prosperity and name the material plainly."),
    15: ("Built in the late 8th century, Borobudur has Buddhist reliefs in its galleries on every level. Explore from Batavia to find it and gain 15 influence.",
         "Give the introductory phrase an explicit subject. Keep the galleries, reliefs and all levels."),
    17: ("The tomb of King Muryeong, who ruled Baekje in its middle period, stands in the hills of Ungjin, then the capital. It reflects burial customs of China's Southern Dynasties. Explore from Seoul to find it and gain 20 influence.",
         "Specify Ungjin's role at the time and keep the broader burial customs that influenced the tomb."),
}
RETENTIONS = {
    0: "The ring of standing stones and the central circle both remain clear. The London expedition and five influence points are explicit.",
    2: "The belief about St. Martin's dedication is qualified. The saint's century and one-point reward are clear.",
    5: "The crypt, its dedication to James and his connection to the twelve apostles all read clearly in the two sentences.",
    8: "Central Anatolia identifies the source region. The wording gives the underground city's estimated age and Istanbul expedition naturally.",
    9: "The compact opening fits the descriptive caption. The next sentence distinguishes the mythological Sphinx, and the final one gives the exploration route.",
    11: "Retain the Rozwi attribution, the source's translation of Zimbabwe and the Sofala expedition as distinct statements.",
    12: "The text gives the royal role, Safavid attribution and date without interrupting the Basra instruction.",
    13: "The caption establishes the subject. The text clearly names both Shah Jahan and Mumtaz Mahal and gives the Calicut expedition.",
    14: "Five-towered describes the temple's five pointed towers concisely. The ruler, era and Malacca reward remain explicit.",
    16: "The description preserves both dynastic periods and the sequence from Yongle's move to building on the old Yuan palace site.",
    18: "The gold-leaf pavilion and Kyoto setting are clear. The text keeps the shogun's title and the Osaka discovery requirement.",
    19: "The caption and description clearly identify the surviving stone warrior figures and the former Toltec capital.",
    20: "The dating remains attributed and approximate. The Teotihuacan identification, Veracruz expedition and influence are all present.",
}
WRAP_FIXES = {
    2: ("4th century.", "gain 1 influence."),
    5: ("11th century.",),
    12: ("late 16th century.",),
    14: ("12th century", "gain 20 influence."),
    16: ("gain 20 influence.",),
    18: ("gain 20 influence.",),
    20: ("2nd century AD.",),
}


def c_string(arm, offset):
    return arm[offset:arm.index(0, offset) + 1]


def transform(clean, current):
    old_layout, source, names = map(base.load, (ALLOCATION, MANUSCRIPT, NAMES))
    spans = old_layout["owned_ranges"]
    bindings = {row["field"]: row for row in old_layout["pointer_bindings"]}
    refs = byte_pointer_references(current, spans)
    rejected = {
        row["byte_offset"]: row["apparent_relative_pointer"]
        for row in old_layout["unaligned_cross_instruction_patterns_classified"]
    }
    assert refs == rejected | {field: row["offset"] for field, row in bindings.items()}
    for row in old_layout["unaligned_cross_instruction_patterns_classified"]:
        offset = row["instruction_offset"]
        assert current[offset:offset + 8].hex() == row["exact_instruction_hex"]
    assert current[IMAGE_TABLE:IMAGE_TABLE + 84] == clean[IMAGE_TABLE:IMAGE_TABLE + 84]
    existing = {row["id"]: c_string(current, row["offset"]) for row in bindings.values()}
    checkpoint = bytearray(current)
    for lo, hi in spans:
        checkpoint[lo:hi] = bytes(hi - lo)
    for row in bindings.values():
        offset, raw = row["offset"], existing[row["id"]]
        assert any(lo <= offset < offset + len(raw) <= hi for lo, hi in spans)
        checkpoint[offset:offset + len(raw)] = raw
    assert checkpoint == current

    target_text = existing.copy()
    records = []
    for row in source["records"]:
        ident, index, field = (row[k] for k in ("id", "site_id", "pointer_field"))
        start = unpack_from("<I", clean, field)[0] - BASE
        source_raw = c_string(clean, start)
        assert start == row["source_offset"] and source_raw[:-1].hex() == row["source_hex"]
        assert source_raw[:-1].decode("cp932") == row["japanese"]
        assert field == DESCRIPTION_TABLE + index * 4 and ident == bindings[field]["id"]
        old = row["english"]
        assert existing[ident] == formatted(old)[0]
        retained = index not in REVISIONS
        english, rationale, *keep = (old, RETENTIONS[index]) if retained else REVISIONS[index]
        phrases = keep[0] if keep else WRAP_FIXES.get(index, ())
        raw, lines = formatted(english, keep_together=phrases)
        assert b"%" not in raw and b"%" not in source_raw and "\r" not in english
        assert lines[-1] != "influence."
        target_text[ident] = raw
        title = names["records"][index]
        name_field = NAME_TABLE + index * 4
        name_offset = unpack_from("<I", clean, name_field)[0] - BASE
        source_name = c_string(clean, name_offset)
        assert existing[title["id"]] == title["english"].encode("ascii") + b"\0"
        records.append(dict(
            id=ident, site_id=index, file_path=ARM, speaker="Historic Sites Gallery",
            clean_Japanese=row["japanese"], source_meaning=row["source_meaning"],
            context=row["context"], previous_English=old, english=english,
            decision="retention" if retained else "revision", localization_note=rationale,
            finding="prose" if not retained else "wrap" if index in WRAP_FIXES else "exact retention",
            display_changed=raw != existing[ident], layout_phrases=list(phrases),
            source_reference=dict(offset=start, pointer_field=field, exact_hex=source_raw.hex()),
            current_reference=dict(offset=bindings[field]["offset"], pointer_field=field, exact_hex=existing[ident].hex()),
            caption=dict(english=title["english"], source_hex=source_name.hex(), source_offset=name_offset,
                         current_offset=bindings[name_field]["offset"], pointer_field=name_field,
                         decision="retention", reason="The complete established Gallery title identifies the pictured site."),
            native_lines=lines, review=dict.fromkeys(REQUIRED_REVIEW_GATES, True) | {"formatting": False},
        ))
    assert len(records) == len(REVISIONS) + len(RETENTIONS) == 19
    allocations, unused = pack(target_text, spans)
    for lo, hi in spans:
        checkpoint[lo:hi] = bytes(hi - lo)
    for field, entry in bindings.items():
        key = entry["id"]
        target = allocations[key]
        raw = target_text[key]
        checkpoint[target:target + len(raw)] = raw
        pack_into("<I", checkpoint, field, BASE + target)
    for field, entry in bindings.items():
        start = unpack_from("<I", checkpoint, field)[0] - BASE
        assert c_string(checkpoint, start) == target_text[entry["id"]]
    result = bytes(checkpoint)
    for lo, hi in spans:
        checkpoint[lo:hi] = current[lo:hi]
    for field in bindings:
        checkpoint[field:field + 4] = current[field:field + 4]
    assert checkpoint == current and event_captions(result) == event_captions(current)
    for row in records:
        row["staged_reference"] = dict(
            offset=allocations[row["id"]], pointer_field=row["source_reference"]["pointer_field"],
            exact_hex=target_text[row["id"]].hex(),
        )
    return result, records, unused


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"] == base.load(base.LEDGER)["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    original, active = map(base.NdsImage.open, (CLEAN, parent.ROM))
    raw = active.read_file(ARM)
    after, records, unused = transform(original.read_file(ARM), raw)
    active.replace_file(ARM, after)
    binary = bytes(active.rom.save())
    active.replace_file(ARM, raw)
    assert bytes(active.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(binary)
    base.save(PROOF, dict(
        candidate_sha256=base.digest(ROM), target_ARM9_sha256=native.digest(after),
        parent_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="static-site-gallery-pending-flush-v3",
        review_gates=list(REQUIRED_REVIEW_GATES), records=records, unused_ranges=unused,
        source_proofs={str(path): base.digest(path) for path in (ALLOCATION, MANUSCRIPT, NAMES)},
    ))
    print(f"Staged {len(REVISIONS)} prose corrections and {len(WRAP_FIXES)} wrap fixes in the original Gallery pool.")


def replay(version):
    rom = parent.ROM if version == "before" else ROM
    root = (PREVIEW if version == "before" else ROOT) / version
    root.mkdir(parents=True)
    manifest = base.load(GALLERY / "sites_fixture_manifest.json")
    manifest.update(production_ROM=str(rom), production_ROM_sha256=base.digest(rom))
    path = root / "fixture.json"
    base.save(path, manifest)
    frames = [2800, *base.load(PLAN / "run_plan.json")["image_frames"], 7000, 7200, 7400]
    sys.argv = [emulator.__file__, "--rom", str(rom), "--out", str(root / "capture"), "--frames", "7400",
                "--capture-every", "99999", "--capture-at", *map(str, frames), "--touchscreen",
                "--allow-gallery-fixtures", "--battery-save", manifest["fixture_save"],
                "--gallery-save-fixture-manifest", str(path), "--inputs-json", str(PLAN / "inputs.json")]
    emulator.main()


def verify():
    assert not LIVE.exists()
    draft = base.load(PROOF)
    reports = [folder / side / "capture/capture_report.json"
               for folder, side in ((PREVIEW, "before"), (ROOT, "after"))]
    before, after = map(base.load, reports)
    assert [before["ROM_sha256"], after["ROM_sha256"]] == [draft["parent_sha256"], draft["candidate_sha256"]]
    expected_save = base.load(GALLERY / "sites_fixture_manifest.json")["fixture_save_sha256"]
    for report in (before, after):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["frames"] == 7400 and not report["earned_unlock_verified"]
        assert report["battery_save_preloaded"]["source_sha256"] == expected_save
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    for key in ("core_DLL_sha256", "scripted_input_schedule", "core_options"):
        assert before[key] == after[key]
    old_frames, new_frames = map(shots, (before, after))
    assert old_frames.keys() == new_frames.keys()
    plan = base.load(PLAN / "run_plan.json")
    font = GameAsciiFont.from_arm9(base.NdsImage.open(ROM).read_file(ARM))
    evidence = {str(path): base.digest(path) for path in reports}
    images, pages = [], []
    for row, frame, index in zip(draft["records"], plan["image_frames"], plan["supported_site_ids"], strict=True):
        assert row["site_id"] == index
        old, new = captured(old_frames[frame]), captured(new_frames[frame])
        for scope in ((0, 0, 256, 212), (0, 356, 256, 384)):
            assert old.crop(scope).tobytes() == new.crop(scope).tobytes(), (index, scope)
        title = row["caption"]["english"]
        complete_mask(font, title, new, 128 - len(title) * 3, 195, (230, 230, 230))
        old_lines = formatted(row["previous_English"])[1]
        paragraph(font, old, old_lines, ink_y=213)
        masks = paragraph(font, new, row["native_lines"], ink_y=213)
        assert (old.tobytes() != new.tobytes()) == row["display_changed"]
        evidence.update({frame_row[frame]["path"]: frame_row[frame]["PNG_sha256"] for frame_row in (old_frames, new_frames)})
        images.append((title, new.crop((0, 192, 256, 356))))
        pages.append(dict(site_id=index, frame=frame, complete_title=True, native_page=masks,
                          before=old_frames[frame]["path"], after=new_frames[frame]["path"]))
    unchanged = [frame for frame in old_frames if frame not in plan["image_frames"] and frame != plan["wrap_frame"]]
    for frame in unchanged:
        assert captured(old_frames[frame]).tobytes() == captured(new_frames[frame]).tobytes(), frame
    wrap = captured(new_frames[plan["wrap_frame"]])
    first = captured(new_frames[plan["image_frames"][0]])
    assert wrap.tobytes() == first.tobytes()

    sheets = {}
    for start in range(0, len(images), 6):
        group = images[start:start + 6]
        sheet = Image.new("RGB", (1024, ((len(group) + 1) // 2) * 352), "#1d2630")
        labels = ImageDraw.Draw(sheet)
        for i, (title, image) in enumerate(group):
            x, y = (i % 2) * 512, (i // 2) * 352
            labels.text((x + 8, y + 3), title, fill="white")
            sheet.paste(image.resize((512, 328), Image.Resampling.NEAREST), (x, y + 20))
        path = ROOT / f"historic_sites_pages_{start // 6 + 1}.png"
        assert not path.exists()
        sheet.save(path)
        sheets[str(path)] = base.digest(path)
    base.save(LIVE, dict(candidate_sha256=draft["candidate_sha256"], pages=pages, carousel_wrap=True,
        unchanged_menu_and_return_frames=unchanged, actual_original_viewer=True, initialized_collection=True,
        natural_site_discoveries_observed=False, hardware=False, evidence=evidence, sheets=sheets))
    print(f"Verified {len(pages)} complete captions and paragraph masks, carousel wrap and Back.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("task", choices=("stage", "verify", "before", "after"))
    task = parser.parse_args().task
    if task == "stage":
        stage()
    elif task == "verify":
        verify()
    else:
        replay(task)
