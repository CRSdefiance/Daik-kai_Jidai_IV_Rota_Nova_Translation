"""Stage the source-bound Yard numeral correction and replay Nagasaki."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch import yard_numerals_20261124 as patch
from scripts import register_nagasaki_shipyard_20261124 as parent
from scripts import stage_nagasaki_contract_wrap_20261124 as earlier
from scripts import stage_nagasaki_shipyard_20261124 as yard_baseline
from scripts import verify_nagasaki_shipyard_20261124 as yard
from scripts.checkpoint_pending_shared_native_20261115 import branch_hits
from scripts.inventory_arm9_text import loaded_components
from scripts.reconcile_archived_message_reader_20261124 import linked_immediates
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ARM, COMMON = parent.ARM, parent.COMMON
ROOT = Path(".codex-release-work/yard_numerals_20261124")
ROM, STORED = ROOT / "Yard_Numerals_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
REPLAY = ROOT / "replay/capture/capture_report.json"
BEFORE = yard_baseline.REPLAY
SHEET, PAIRED = ROOT / "yard_numerals_paired.png", ROOT / "paired_gameplay.json"
BASE = patch.BASE
panels = yard.panels
LIVE = {7320: (786, "Masts: 1. Durability: 30."), 12120: (789, "How about 7500 gold coins?")}


def incoming(image, target):
    return [(area, pc, dst, kind) for area, base, data in loaded_components(image)
            for pc, dst, kind in (*branch_hits(data, base, {target, target | 1}), *linked_immediates(data, base, {target}))]


def stage():
    release = read(parent.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] and digest(BEFORE) == read(yard_baseline.PAIRED)["after"]["sha256"]
    original, active = map(NdsImage.open, (CLEAN, parent.ROM))
    clean_arm, arm = (image.read_file(ARM) for image in (original, active))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    common = active.read_file(COMMON)
    assert sha256(common).hexdigest() == release["target_COMMON_sha256"]
    target, changes, suffix = patch.propose(arm, clean_arm)
    links = incoming(active, patch.QUANTITY)
    assert set(links) == {("arm9_section_0", call, patch.QUANTITY, "arm_bl") for call in patch.QUANTITY_CALLS}, links
    helper_before = incoming(active, patch.HELPER)
    before_bounds = earlier.template.right_bound(arm, release["right_bound_configuration"])
    assert before_bounds["matched_repair_spans"] == 8
    assert earlier.template.right_bound(target, release["right_bound_configuration"]) == before_bounds
    active.replace_file(ARM, target)
    helper_after = incoming(active, patch.HELPER)
    added = {("arm9_section_0", call, patch.HELPER, "arm_bl") for call in patch.BARE_CALLS}
    added.add(("arm9_section_0", patch.QUANTITY_DIGITS, patch.HELPER, "thumb_blx_immediate"))
    assert set(helper_before) <= set(helper_after) and set(helper_after) - set(helper_before) == added, helper_after
    image = bytes(active.rom.save())
    active.replace_file(ARM, arm)
    assert bytes(active.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(image)
    reopened = NdsImage.open(ROM)
    assert reopened.read_file(ARM) == target and reopened.read_file(COMMON) == common
    write(STORED, dict(candidate=reference(ROM), previous=reference(parent.ROM), clean=reference(CLEAN), whole_parent_inverse=True,
        instruction_changes=changes, suffix_callers=suffix, bare_numeric_callers=patch.BARE_CALLS, affected_ordinary=LIVE,
        compact_helper_unchanged=patch.compact_helper().hex(), quantity_references=links, compact_helper_predecessor_references=helper_before,
        compact_helper_candidate_references=helper_after, target_ARM9_sha256=sha256(target).hexdigest(), target_COMMON_sha256=release["target_COMMON_sha256"],
        install_scope="Nine width-only branches in the native ARM9. Shared strings and control templates retain exact bytes.",
        prior_release=reference(parent.RELEASE), prior_gameplay=reference(yard_baseline.PAIRED)))
    print(f"Staged Yard numeral corrections. {digest(ROM)}", flush=True)


def verify(stored):
    old, new = map(read, (BEFORE, REPLAY))
    assert old["ROM_sha256"] == stored["previous"]["sha256"] and new["ROM_sha256"] == stored["candidate"]["sha256"] == digest(ROM)
    assert new["cold_boot"] and not new["callback_errors"] and not new["savestate_loaded"]
    assert not any(value for key, value in new.items() if key.startswith("synthetic_"))
    assert new["frames"] == old["frames"] and new["scripted_input_schedule"] == old["scripted_input_schedule"]
    donor = new["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    before, after = (panels.shots(run, "_cold_boot.png") for run in (old, new))
    expected = set(range(3720, yard.END + 1, 400))
    assert expected <= before.keys() and expected <= after.keys()
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ARM))
    matches, revisions, blinks = [], [], []
    sheet = Image.new("RGB", (1024, 496), "#263238")
    draw = ImageDraw.Draw(sheet)
    for frame in sorted(expected):
        a, b = (panels.picture(group[frame]) for group in (before, after))
        bbox = ImageChops.difference(a, b).getbbox()
        if bbox is None:
            assert frame not in LIVE
            matches.append(frame)
            continue
        if frame not in LIVE:
            assert bbox[1] >= 192
            changes = Counter((s, t) for s, t in zip(a.crop(bbox).get_flattened_data(), b.crop(bbox).get_flattened_data(), strict=True) if s != t)
            colors = {yard_baseline.PAPER, (24, 40, 49), (24, 48, 57), (41, 48, 57), (41, 48, 65)}
            assert all(yard_baseline.HIGHLIGHT in pair and any(color in colors for color in pair) for pair in changes), (frame, bbox, changes)
            blinks.append(dict(frame=frame, background_only=True, box=bbox,
                changed_colors=[dict(previous=s, current=t, pixels=count) for (s, t), count in sorted(changes.items())]))
            continue
        key, line = LIVE[frame]
        assert 16 <= bbox[0] < bbox[2] <= 245 and 296 <= bbox[1] < bbox[3] <= 360, (frame, bbox)
        ink = panels.exact_body(font, [line], b)
        assert panels.nameplate(font, "Shipwright", a) == panels.nameplate(font, "Shipwright", b)
        revisions.append(dict(frame=frame, message_ID=key, line=line, complete_foreground_pixels=ink,
            previous=before[frame], revised=after[frame], validated_change_box=bbox))
        y = 248 * (len(revisions) - 1)
        for index, (label, screen) in enumerate((("Previous", a), ("Revised", b))):
            x = 512 * index
            draw.text((x + 6, y + 4), f"COMMON {key} / {label}", fill="white")
            sheet.paste(screen.crop((0, 272, 256, 384)).resize((512, 224), Image.Resampling.NEAREST), (x, y + 19))
    assert len(revisions) == len(LIVE) and yard.END in matches
    sheet.save(SHEET)
    write(PAIRED, dict(candidate_sha256=new["ROM_sha256"], previous_sha256=old["ROM_sha256"], before=reference(BEFORE), after=reference(REPLAY),
        stored=reference(STORED), sheet=reference(SHEET), unchanged_frames=matches, revised=revisions, menu_highlight_only=blinks,
        ordinary_saved_game=True, research_fixtures=False))
    print(f"Verified both revised numeric panels, {len(matches)} exact controls, and {len(blinks)} highlight-only frames.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup", "replay", "verify"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    elif action == "verify":
        verify(read(STORED))
    elif action == "replay":
        scope = vars(earlier) | globals()
        source = checked_text(getsource(earlier.replay), {'shots(old, "_navigation.png")': 'shots(old, "_cold_boot.png")'})
        exec(compile(source, __file__ + "::current-Yard-replay", "exec"), scope)
        scope["replay"](read(STORED))
    else:
        scope = vars(earlier) | globals()
        FunctionType(earlier.release_check.__code__, scope)(read(STORED), action)
