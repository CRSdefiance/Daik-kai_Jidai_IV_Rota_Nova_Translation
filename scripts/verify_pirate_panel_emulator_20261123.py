"""Compare the registered label and English fixture across complete emulator frames."""

from argparse import ArgumentParser
import json

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage
from scripts.probe_pirate_panel_emulator_20261123 import CAPTURES, FRAMES, RELEASE, ROOT, STAGED
from scripts.probe_pirate_affiliation_20261123 import ENGLISH, JAPANESE, REPORT as NATIVE, SLOT
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, OUT, digest, read, reference


REPORT = OUT.with_name("pirate_affiliation_panel_20261123.json")
SHEET = REPORT.with_suffix(".png")
STORED = STAGED / "staged_panel_replay.json"
PLATE = (0, 208, 120, 232)
CHANGE = (6, 214, 40, 226)
PALETTE = {(131, 133, 32), (230, 230, 230)}


def evidence(case, candidate_sha256):
    folder = ROOT / case
    fixture_path = folder / "fixture.json"
    fixture = read(fixture_path)
    entry = fixture["capture"]
    assert digest(entry["path"]) == entry["sha256"]
    capture = read(entry["path"])
    assert fixture["actor"] == 27 and fixture["name"].startswith("Aziza")
    assert fixture["assigned_crew"] == [16, 23, 18, 1] and not fixture["ordinary_gameplay"]
    assert fixture["candidate_sha256"] == capture["ROM_sha256"] == candidate_sha256
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert capture["frames"] == FRAMES
    assert digest(fixture["inputs"]["path"]) == fixture["inputs"]["sha256"]
    frames = {row["frame"]: row for row in capture["frames_captured"] if not row["path"].endswith("_final.png")}
    assert set(CAPTURES) <= frames.keys()
    picks = {k: frames[k] for k in CAPTURES}
    assert all(digest(row["path"]) == row["PNG_sha256"] for row in picks.values())
    return fixture, capture, picks, reference(fixture_path)


def screen(row):
    with Image.open(row["path"]) as image:
        rgb = image.convert("RGB")
    assert rgb.size == (256, 384)
    return rgb


def main():
    assert not REPORT.exists() and not SHEET.exists()
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    jp, en = (evidence(case, release["candidate_sha256"]) for case in ("installed", "english"))
    assert jp[0]["label_slot_hex"] == JAPANESE.hex() and en[0]["label_slot_hex"] == ENGLISH.hex()
    assert jp[0]["state_transitions"] == en[0]["state_transitions"]
    assert jp[0]["state_transitions"][-1]["state"] == 2
    assert jp[1]["scripted_input_schedule"] == en[1]["scripted_input_schedule"]
    assert jp[1]["battery_save_preloaded"]["source_sha256"] == en[1]["battery_save_preloaded"]["source_sha256"]
    arm = NdsImage.open(release["candidate"]).read_file(ARM)
    native = read(NATIVE)
    assert native["candidate_sha256"] == release["candidate_sha256"] and native["proposed_text"] == "Pirate"
    assert arm[SLOT:SLOT + len(JAPANESE)] == JAPANESE
    font = GameAsciiFont.from_arm9(arm)
    expected = {(6 + i * 6 + x, 215 + y) for i, char in enumerate("Pirate")
                for glyph in (font.decode(char),) for x in range(6) for y in range(11) if glyph.getpixel((x, y))}
    assert len(expected) == native["proposed_exact_native_font_pixels"] == 70
    holds = []
    for number in CAPTURES:
        old, new = screen(jp[2][number]), screen(en[2][number])
        bounds = ImageChops.difference(old, new).getbbox()
        if number <= 4801:
            assert bounds is None
        else:
            assert bounds == CHANGE
            positions = {(x, y) for y in range(PLATE[1], PLATE[3]) for x in range(PLATE[0], PLATE[2])
                         if new.getpixel((x, y)) == (230, 230, 230)}
            assert positions == expected
            assert set(new.crop(PLATE).get_flattened_data()) == PALETTE
        holds.append({"frame": number, "only_pixel_changes_within": bounds,
                      "installed": jp[2][number], "english": en[2][number]})

    show = 5300
    sheet = Image.new("RGB", (560, 450), "#242a34")
    labels = ImageDraw.Draw(sheet)
    for x, data, heading in ((12, jp, "Current ROM · Japanese label"), (292, en, "Fixture · proposed English")):
        labels.text((x, 8), heading, fill="white")
        image = screen(data[2][show])
        sheet.paste(image, (x, 24))
        sheet.paste(image.crop(PLATE).resize((240, 40), Image.Resampling.NEAREST), (x, 409))
    sheet.save(SHEET)
    row = {"id": "ARM9_ALTERNATE_BATTLE_PIRATE_AFFILIATION", "file_path": ARM,
           "speaker": "Opponent affiliation nameplate", "source_Japanese": "海賊", "english": "Pirate",
           "context": "The alternate battle draws the opponent affiliation beside the player's named fleet. "
                      "The same branch accepts the original faction-name getter for other affiliations.",
           "source_meaning": "The affiliation field identifies the opponent as a pirate.",
           "localization_note": "The singular role reads naturally under the opponent and stays distinct from a fleet name. "
                                "It preserves the source role without assigning a new faction or rank.",
           "decision": "revision", "review": dict.fromkeys(("source", "context", "localization", "naturalness", "formatting"), True),
           "source_reference": {"offset": SLOT, "bytes": JAPANESE.hex(), "clean_ROM_sha256": release["clean_input_sha256"]},
           "current_reference": {"offset": SLOT, "bytes": JAPANESE.hex(), "candidate_sha256": release["candidate_sha256"]},
           "proposed_reference": {"offset": SLOT, "bytes": ENGLISH.hex(), "exclusive_end": SLOT + len(ENGLISH)},
           "original_painter_call": BASE + 0xBC44, "substitutions": [], "pages_in_field": 1}
    result = {"candidate_sha256": release["candidate_sha256"], "translation_policy": "natural-dialogue-v2",
              "encoder": "dialogue-relocatable-v1", "target_locale": "en-US", "review_gates": list(row["review"]),
              "records": [row], "native_comparison": reference(NATIVE), "fixtures": [jp[3], en[3]],
              "emulator_comparisons": holds, "complete_English_pixels_per_hold": len(expected),
              "sheet": reference(SHEET), "ordinary_gameplay": False, "tested_full_nameplate": True,
              "observed_battle_exit": False, "registered_ROM_changed": False}
    validate_natural_dialogue_batch(result)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified nine exact full emulator comparisons with every English nameplate glyph.")


def verify_staged():
    proof_path = STAGED / "stored_proof.json"
    proof, accepted = read(proof_path), read(REPORT)
    candidate = proof["candidate_sha256"]
    fixture, capture, frames, receipt = evidence("staged", candidate)
    assert not fixture["label_overridden_in_memory"] and fixture["label_slot_hex"] == ENGLISH.hex()
    assert proof["exact_parent_inverse"] and proof["predecessor_sha256"] == accepted["candidate_sha256"]
    assert digest(capture["ROM"]) == candidate
    arm = NdsImage.open(capture["ROM"]).read_file(ARM)
    assert arm[SLOT:SLOT + len(ENGLISH)] == ENGLISH
    checks = []
    for old in accepted["emulator_comparisons"]:
        row = frames[old["frame"]]
        assert row["framebuffer_sha256"] == old["english"]["framebuffer_sha256"]
        checks.append({"frame": row["frame"], "framebuffer_sha256": row["framebuffer_sha256"]})
    assert len(checks) == len(CAPTURES)
    result = {"candidate_sha256": candidate, "stored_proof": reference(proof_path), "display_receipt": reference(REPORT),
              "staged_fixture_receipt": receipt, "exact_English_frame_matches": checks,
              "label_overridden_in_memory": False, "ordinary_battle_activation_or_exit_observed": False}
    assert not STORED.exists()
    STORED.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("The staged ROM's stored Pirate label matches all eleven tested English frames.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true")
    (verify_staged if parser.parse_args().staged else main)()
