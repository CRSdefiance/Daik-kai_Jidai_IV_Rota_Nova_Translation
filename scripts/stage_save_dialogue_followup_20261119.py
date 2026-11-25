"""Stage the native save confirmations and cartridge read and write warnings."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import register_mutiny_dialogue_followup_20261119 as parent
from scripts.plan_literal_static_layout_v1 import HEIGHT, WIDTH, render
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN
ROOT = Path("work/save_dialogue_followup_20261119_v2")
ROM = ROOT / "Save_Dialogue_RESEARCH_ONLY.nds"
PROOF = ROOT / "staged.json"
SHEET = ROOT / "save_native_pages.png"
SOURCE = Path("translations/common_submenus_arm9_v1.json")
GATES = list(parent.stage.source.GATES)
FIXED = (
    ("DK4_SAVE_OVERWRITE_CONFIRM", 0xEEC28, 0xEEA14, 1, 1, ("Overwrite this save?",),
     "The existing data will be lost. The player must approve replacing it.",
     "Selected save slot is occupied.",
     "A direct overwrite question conveys that the current save will be replaced and fits as one complete line."),
    ("DK4_SAVE_CREATE_CONFIRM", 0xEEC2C, 0xEEA14, 2, 1, ("Create a new save?",),
     "The game will create new save data if the player confirms.",
     "Selected save slot is empty.",
     "Say what will happen in the confirmation itself. The question fits as one complete line."),
    ("DK4_LOAD_READ_ERROR", 0xEEF54, 0xEEF24, 0, 0,
     ("Couldn't read the data.", "Power off. Reinsert the game card."),
     "The read failed. The player should power off the system and then reinsert the game card.",
     "Native cartridge read error.",
     "Keep the read failure distinct. Keep the two recovery instructions together and in the original order."),
    ("DK4_SAVE_WRITE_ERROR", 0xEEF50, 0xEEF24, 1, 0,
     ("Couldn't write the data.", "Power off. Reinsert the game card."),
     "The write failed. The player should power off the system and then reinsert the game card.",
     "Native cartridge write error.",
     "Keep the write failure distinct. Keep the two recovery instructions together and in the original order."),
)


def digest(value):
    return sha256(value).hexdigest()


def literal(raw, offset):
    return raw[offset:raw.index(0, offset)]


def probe(runtime, entry, mode, kind, offset, text):
    cpu, _, provider = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    cpu.mem_write(STACK, bytes(0x88))
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, mode)
    seen = []

    def watch(u, pc, size, _):
        pointer = u.reg_read(UC_ARM_REG_R1)
        assert bytes(u.mem_read(pointer, len(text) + 1)) == text + b"\0"
        assert u.reg_read(UC_ARM_REG_R0) == kind and u.reg_read(UC_ARM_REG_R3) == 0
        if kind == 0:
            assert pointer == BASE + offset
        else:
            assert STACK - 0x88 < pointer < STACK
        seen.append(pointer)

    cpu.hook_add(UC_HOOK_CODE, watch, begin=BASE + 0x54774, end=BASE + 0x54774)
    stop = BASE + 0x5479C
    cpu.emu_start(BASE + entry, stop, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == stop and len(seen) == 1
    expanded, output = unpack_from("<2I", runtime.arm, 0x54890)
    assert bytes(cpu.mem_read(expanded, 256)).split(b"\0", 1)[0] == text
    display = bytes(cpu.mem_read(output, 256)).split(b"\0", 1)[0]
    assert b" ".join(display.split()) == b" ".join(text.split())
    assert not provider.opens and not provider.reads
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return display


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    arm = runtime.arm
    clean = base.NdsImage.open(CLEAN).read_file(ARM)
    for lo, hi in ((0xEEA14, 0xEEA60), (0xEEF24, 0xEEF58), (0x546F8, 0x54798)):
        assert arm[lo:hi] == clean[lo:hi]
    known = {row["id"]: row for row in base.load(SOURCE)["records"]}
    output = bytearray(arm)
    plan = []
    for label, pointer, entry, mode, kind, lines, meaning, context, note in FIXED:
        offset = known[label]["offset"]
        assert unpack_from("<I", clean, pointer)[0] == unpack_from("<I", arm, pointer)[0] == BASE + offset
        allocation = bytes.fromhex(known[label]["source_hex"])
        assert clean[offset:offset + len(allocation)] == allocation
        before = literal(arm, offset)
        assert before.decode("ascii") == known[label]["english"]
        span = len(before) + 1  # Later builds use portions of the original padding for other code.
        assert arm[offset:offset + span] == before + b"\0"
        body = "\n ".join(lines).encode("ascii")
        assert b"%" not in allocation and b"%" not in body and len(body) < span
        output[offset:offset + span] = body.ljust(span, b"\0")
        plan.append((offset, span, label, pointer, entry, mode, kind, lines, meaning, context, note, allocation,
                     before, body))
    changed = bytes(output)
    deployed = with_components(runtime, changed, runtime.common)
    snapshot = bytearray(deployed.raw)
    for offset, span, *_ in plan:
        assert snapshot[offset:offset + span] == arm[offset:offset + span]
        snapshot[offset:offset + span] = changed[offset:offset + span]
    deployed.raw = bytes(snapshot)
    raster, _, _ = font_tools(runtime.image)
    font = GameAsciiFont.from_arm9(arm)
    records, panels = [], []
    for offset, span, label, pointer, entry, mode, kind, lines, meaning, context, note, allocation, before, body in plan:
        original_display = probe(runtime, entry, mode, kind, offset, before)
        display = probe(deployed, entry, mode, kind, offset, body)
        before_pixels, old_lines, _, _ = render(raster, font, arm, original_display)
        pixels, visible, origins, glyphs = render(raster, font, changed, display)
        assert tuple(visible) == lines and display != original_display
        assert all(0 <= start and start + len(row) * 6 <= 216 for start, row in zip(origins, visible, strict=True))
        logical = " ".join(lines)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(logical[0]), ord(logical[-1]))
        panels.extend((before_pixels, pixels))
        location = dict(offset=offset, allocation=span, pointer_field=BASE + pointer, runtime_pointer=BASE + offset)
        records.append(dict(id=label, file_path=ARM, speaker="System", context=context, source_meaning=meaning,
            localization_note=note, decision="revision", source_Japanese=allocation.split(b"\0", 1)[0].decode("cp932"),
            source_reference=location | {"ARM9_sha256": digest(clean), "allocation": len(allocation)}, current_reference=location | {"ARM9_sha256": digest(arm)},
            source_hex=allocation.hex(), current_hex=arm[offset:offset+span].hex(), staged_hex=changed[offset:offset+span].hex(),
            previous_English=before.decode("ascii"), previous_native_lines=old_lines, english=logical,
            display_hex=display.hex(), visible_lines=visible, native_ink_sha256=digest(pixels),
            original_selector=BASE + entry, supplied_selector_mode=mode, native_modal_mode=kind,
            glyphs=len(glyphs), native_pages=1, runtime_substitutions=[],
            review=dict.fromkeys(GATES, True) | {"formatting": False}))
        output[offset:offset + span] = arm[offset:offset + span]
    assert bytes(output) == arm
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, changed)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)

    sheet = Image.new("RGB", (936, 4 * 118), "#253444")
    draw = ImageDraw.Draw(sheet)
    for i, (row, plane) in enumerate(zip((r for r in records for _ in range(2)), panels, strict=True)):
        x, y = i % 2 * 468, i // 2 * 118
        side = "after" if i % 2 else "before"
        draw.text((x + 4, y + 2), f'{row["id"]}  {side}', fill="white")
        img = Image.frombytes("L", (WIDTH, HEIGHT), bytes(0 if p else 255 for p in plane))
        sheet.paste(img.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 18))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate=str(ROM), candidate_sha256=digest(candidate), parent_sha256=release["candidate_sha256"],
        target_ARM9_sha256=digest(changed), target_COMMON_sha256=release["target_COMMON_sha256"], clean_input_sha256=release["clean_input_sha256"],
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=GATES, records=records, entire_parent_inverse=True, original_source_manifest_sha256=base.digest(SOURCE),
        native_sheet_sha256=base.digest(SHEET)))
    print("Four exact ARM9 templates staged through their native selectors and modal formatter.")


if __name__ == "__main__":
    main()

