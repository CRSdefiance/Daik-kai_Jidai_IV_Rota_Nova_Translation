"""Verify a source-bound Deck View clarification in its existing text allocation."""

import sys
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.deck_filter_help import BASE, POOL, cache_plan, compiled
from scripts import observe_riga_trade_20261124 as play
from scripts import stage_deck_view_guidance_20261119 as historical
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts import verify_deck_filter_native_v263 as native
from scripts import verify_palace_investment_replay_20261124 as playback
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write

parent = play.current
ARM, COMMON = parent.ARM, parent.COMMON
ROOT = play.ROOT.with_name("editorial_20261124_deck_skill_guidance")
ROM = ROOT / "Deck_Skill_Guidance_STAGED.nds"
OUT, SHEET = ROOT / "deck_skill_guidance_native.json", ROOT / "deck_skill_guidance_native.png"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
played = SimpleNamespace(RELEASE=parent.RELEASE)
HISTORY = Path("releases/all_routes_editorial_20261119_deck_view_guidance_candidate/verification/registered_review.json")
BASELINE = play.ROOT / "capture/capture_report.json"
FIELD = 0x1559C
DRAFT = "Each duty has skill requirements. Navigators must meet them to qualify. Higher skill improves performance."
ORIGINS = (33, 49, 81)
HOLDS = (12000, 12400, 12800, 13200, 13600)
EXTRA = (14480, 17420)
panels = playback.panels


def help_pixels(font, lines):
    expected = set()
    for paragraph, y in zip(lines, ORIGINS, strict=True):
        for row, text in enumerate(paragraph.split("\n")):
            expected.update(historical.ink(font, text[1:] if row else text, 0, y + row * 16))
    return expected


def actual_help_pixels(screen):
    return {(x, y) for y in range(30, 128) for x in range(256) if screen.getpixel((x, y)) == (230, 230, 230)}


def stage():
    release, baseline = map(read, (parent.RELEASE, BASELINE))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] == baseline["ROM_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, parent.ROM))
    before, arm = clean.read_file(ARM), image.read_file(ARM)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    layout = cache_plan(arm)
    code = MainCodeFile(arm, BASE)
    pool = code.sections[3].data
    rows, patches = [], []
    for row in read(HISTORY)["records"]:
        field = row["field"]
        raw_japanese = row["source_Japanese"].encode("cp932") + b"\0"
        old = row["compiled"].encode("ascii") + b"\0"
        assert unpack_from("<I", before, field) == (row["source_pointer"],)
        assert unpack_from("<I", arm, field) == (row["target_pointer"],)
        source = row["source_pointer"] - BASE
        at = row["target_pointer"] - POOL
        assert before[source:source + len(raw_japanese)] == raw_japanese and bytes(pool[at:at + len(old)]) == old
        assert 0 <= at < at + len(old) < len(pool) - 112 and b"%" not in raw_japanese + old
        english = DRAFT if field == FIELD else row["english"]
        target_text = compiled(field, english, 2)
        assert len(row["compiled"].split("\n")) == len(target_text.split("\n"))
        if field != FIELD:
            assert row["compiled"] == target_text
        raw_new = (target_text.encode("ascii") + b"\0").ljust(len(old), b"\0")
        assert len(raw_new) == len(old)
        if field == FIELD:
            assert target_text.split("\n") == ["Each duty has skill requirements.",
                "  Navigators must meet them to qualify.", "  Higher skill improves performance."]
            patches.append((at, old, raw_new))
            pool[at:at + len(old)] = raw_new
        rows.append(row | dict(
            english=english, English=english, compiled=target_text, predecessor_compiled=row["compiled"],
            decision="revision" if field == FIELD else "retention",
            localization_note=("Name the skill requirements explicitly so 'meet them' has a clear antecedent. Preserve the threshold and the benefit of higher skill."
                               if field == FIELD else row["localization_note"]),
            current_reference=dict(pointer_field=BASE + field, runtime_pointer=row["target_pointer"], exact_hex=old.hex()),
            installed_reference=dict(pointer_field=BASE + field, runtime_pointer=row["target_pointer"], exact_hex=raw_new.hex()),
            review=dict.fromkeys(GATES, True) | {"formatting": field != FIELD},
        ))
    assert len(patches) == 1
    changed = bytes(code.save())
    at, old, new = patches[0]
    pool[at:at + len(old)] = old
    assert bytes(code.save()) == arm and cache_plan(changed) == layout
    spans = [(i, a, b) for i, (a, b) in enumerate(zip(arm, changed, strict=True)) if a != b]
    assert spans and arm.count(old) == 1
    raw_at = arm.index(old)
    assert changed[raw_at:raw_at + len(new)] == new
    assert all(raw_at <= i < raw_at + len(new) for i, _, _ in spans)

    font = historical.GameAsciiFont.from_arm9(arm)
    old_help = [row["predecessor_compiled"] for row in rows[2:]]
    frames = panels.shots(baseline, "_navigation.png")
    reference_screen = panels.picture(frames[12000])
    assert actual_help_pixels(reference_screen) == help_pixels(font, old_help)
    right_bound = release["right_bound_configuration"]
    assert parent.template.right_bound(changed, right_bound) == parent.template.right_bound(arm, right_bound)
    assert parent.template.right_bound(changed, right_bound)["matched_repair_spans"] == 8
    ROOT.mkdir(exist_ok=True)
    (ROOT / "research_arm9.bin").write_bytes(changed)
    write(ROOT / "runtime_plan.json", dict(records=rows, cache=layout))
    recipe = checked_text(getsource(native.main), {
        'e["y"] + 11 <= 128': 'e["y"] + 12 <= 128',
        'expected[(e["y"] + y) * width + e["x"] + x]': 'expected[(e["y"] + y + 1) * width + e["x"] + x]',
        'boot_rom = NdsImage.open("out/all_routes_combined_v261_candidate.nds")': 'boot_rom = NdsImage.open(parent_rom)',
        '    (ROOT / "native_proof.json").write_text': '    save_preview(expected)\n    (ROOT / "native_proof.json").write_text',
    })

    def save_preview(expected):
        sheet = Image.new("RGB", (1024, 276), "#263238")
        labels = ImageDraw.Draw(sheet)
        labels.text((6, 5), "Current / ordinary Riga Deck View", fill="white")
        labels.text((518, 5), "Proposed / native Deck View", fill="white")
        sheet.paste(reference_screen.crop((0, 0, 256, 128)).resize((512, 256), Image.Resampling.NEAREST), (0, 20))
        preview = Image.frombytes("L", (256, 128), bytes(232 if pixel else 46 for pixel in expected))
        sheet.paste(preview.resize((512, 256), Image.Resampling.NEAREST), (512, 20))
        sheet.save(SHEET)

    scope = vars(native) | dict(ROOT=ROOT, parent_rom=parent.ROM, save_preview=save_preview)
    exec(compile(recipe, str(Path(__file__)) + "::native-deck-width", "exec"), scope)
    scope["main"]()

    image.replace_file(ARM, changed)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert sha256(image.rom.save()).hexdigest() == release["candidate_sha256"]
    if ROM.exists():
        assert ROM.read_bytes() == candidate
    else:
        with ROM.open("xb") as stream:
            stream.write(candidate)
    write(OUT, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=sha256(changed).hexdigest(),
        target_COMMON_sha256=release["target_COMMON_sha256"], exact_parent_reserialize=True,
        exact_arm_span=dict(offset=raw_at, current_hex=old.hex(), installed_hex=new.hex(), resident_address=POOL + at),
        records=rows, sheets=[reference(SHEET)], native_proof=reference(ROOT / "native_proof.json"),
        previous_gameplay=reference(BASELINE), translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=list(GATES), native_pages=1, visual_review_complete=False,
        paired_gameplay_complete=False, registered=False))


def replay(candidate):
    edit, baseline = map(read, (OUT, BASELINE))
    donor = baseline["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    rom = ROM if candidate else parent.ROM
    assert digest(rom) == edit["candidate_sha256" if candidate else "predecessor_sha256"]
    target = ROOT / ("riga" if candidate else "riga_parent")
    target.mkdir()
    inputs = target / "inputs.json"
    write(inputs, baseline["scripted_input_schedule"])
    frames = set(panels.shots(baseline, "_navigation.png")) | set(EXTRA)
    original = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(rom), "--out", str(target), "--frames", str(baseline["frames"]),
                    "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen", "--press-start", "-1",
                    "--capture-every", "999999", "--capture-at", *map(str, sorted(frames))]
        playback.harness.main()
    finally:
        sys.argv = original


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "replay", "parent-replay", "patch", "startup"))
    action = cli.parse_args().action
    if action in ("patch", "startup"):
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(OUT), action)
    elif action == "stage":
        stage()
    else:
        replay(action == "replay")
