"""Original HELP parser and font pixels; link child creation is observed only."""

import json
import struct

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R5,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.prepare_help_pages_v281 import ROOT
from scripts.probe_button_prompt_native import STACK, machine
from scripts.research_online_loader_v190 import resource_call as call

WIDTH, HEIGHT = 252, 120
HEADER, VIEW, PARENT = 0x02450000, 0x02456000, 0x02460000


def verify(arm, page):
    cpu = machine(arm)
    cpu.mem_write(POOL, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    size = WIDTH * HEIGHT // 2
    header = struct.pack("<5I", 4, WIDTH // 4, HEIGHT, 0x02452000 - HEADER, 20)
    cpu.mem_write(HEADER - 16, b"\xA5" * (size + 52))
    cpu.mem_write(HEADER, header + bytes(size))
    call(cpu, 0xD3D80, (VIEW,))
    cpu.mem_write(STACK, struct.pack("<4I", WIDTH, HEIGHT, 0, 0))
    call(cpu, 0xD3AFC, (VIEW, HEADER, 0, 0))
    metrics = struct.unpack_from("<I", arm, 0xD5088)[0]
    cpu.mem_write(metrics + 4, struct.pack("<2I", 6, 12))
    call(cpu, 0xAC378, (STACK + 0x78, VIEW, 1))
    raw = bytes.fromhex(page["encoded_hex"])
    buffer = struct.unpack_from("<I", arm, 0x7D06C)[0]
    cpu.mem_write(buffer - 16, b"\xA5" * (len(raw) + 32))
    cpu.mem_write(buffer, raw)
    cpu.mem_write(STACK + 4, struct.pack("<I", PARENT))
    cpu.mem_write(PARENT + 0x660, bytes(4))
    for register in (UC_ARM_REG_R5, UC_ARM_REG_R8, UC_ARM_REG_R9):
        cpu.reg_write(register, 0)
    cpu.reg_write(UC_ARM_REG_R10, buffer)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    events, links = [], []

    def observe(uc, address, size, _):
        stack = uc.reg_read(UC_ARM_REG_SP)
        if address == BASE + 0xD16B4:
            code, style = struct.unpack("<2I", uc.mem_read(stack, 8))
            events.append({"code": code, "style": style, "x": uc.reg_read(UC_ARM_REG_R2), "y": uc.reg_read(UC_ARM_REG_R3)})
        elif address == BASE + 0x7CBE4:
            assert uc.reg_read(UC_ARM_REG_R0) == PARENT
            link = {"column": uc.reg_read(UC_ARM_REG_R1), "label_cells": uc.reg_read(UC_ARM_REG_R2),
                    "row": uc.reg_read(UC_ARM_REG_R3), "id": struct.unpack("<I", uc.mem_read(stack, 4))[0]}
            assert link["row"] < 10 and link["column"] + link["label_cells"] <= 42
            links.append(link)
            # The native parser is intact; UI child allocation/registration is
            # an explicitly deferred contract, not a verified clickable widget.
            uc.mem_write(PARENT + 0x660, struct.pack("<I", len(links)))
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
    cpu.hook_add(UC_HOOK_CODE, observe)
    cpu.emu_start(BASE + 0x7CE88, BASE + 0x7D050, count=max(200000, len(raw) * 5000))
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + 0x7D050
    assert cpu.reg_read(UC_ARM_REG_R10) == buffer + len(raw) - 1
    assert bytes(cpu.mem_read(buffer, len(raw))) == raw
    assert bytes(cpu.mem_read(buffer - 16, 16)) == bytes(cpu.mem_read(buffer + len(raw), 16)) == b"\xA5" * 16
    assert bytes(cpu.mem_read(HEADER, 20)) == header
    assert bytes(cpu.mem_read(HEADER - 16, 16)) == bytes(cpu.mem_read(HEADER + 20 + size, 16)) == b"\xA5" * 16
    assert [(r["id"], r["row"]) for r in links] == [(r["id"], r["row"]) for r in page["links"]]
    font = GameAsciiFont.from_arm9(arm)
    expected = bytearray(WIDTH * HEIGHT)
    visible = [e for e in events if e["code"] != 32]
    assert [e["code"] for e in visible] == [ord(c) for line in page["visible_lines"] for c in line if c != " "]
    assert len({(e["x"], e["y"]) for e in visible}) == len(visible)
    for event in events:
        glyph = font.decode(chr(event["code"]))
        x, y = event["x"], event["y"]
        if event["code"] != 32:
            assert 0 <= x <= WIDTH - 6 and 0 <= y <= HEIGHT - 11
        for yy in range(11):
            for xx in range(6):
                if 0 <= x + xx < WIDTH and 0 <= y + yy < HEIGHT:
                    expected[(y + yy) * WIDTH + x + xx] = event["style"] if glyph.getpixel((xx, yy)) else 0
    actual = bytes(n for b in cpu.mem_read(HEADER + 20, size) for n in (b & 15, b >> 4))
    assert actual == expected, [(i % WIDTH, i // WIDTH, a, b) for i, (a, b) in enumerate(zip(actual, expected)) if a != b][:8]
    for row, line in enumerate(page["visible_lines"]):
        positioned = [e for e in events if e["y"] == row * 12 and e["code"] != 32]
        assert [(e["x"], chr(e["code"])) for e in positioned] == [(i * 6, c) for i, c in enumerate(line) if c != " "]
    picture = Image.new("RGB", (WIDTH, HEIGHT))
    colors = {0: (32, 54, 65), 12: (100, 218, 255), 14: (210, 210, 210), 15: (255, 255, 255)}
    picture.putdata([colors[p] for p in actual])
    return {"topic_id": page["topic_id"], "complete_glyphs": len(visible), "native_link_requests": links,
            "all_visible_lines_coordinates_complete_pixels_and_first_final_glyphs_exact": True,
            "input_header_pixel_guards_pass": True}, picture


def main():
    arm = NdsImage.open("out/all_routes_combined_v275_candidate.nds").read_file("/__arm9__.bin")
    plan = json.loads((ROOT / "page_proposal.json").read_text(encoding="utf-8"))
    cases, failures, images = [], [], []
    for page in plan["pages"]:
        try:
            proof, picture = verify(arm, page)
            cases.append(proof)
            images.append((page["topic_id"], picture))
        except (ValueError, AssertionError) as error:
            failures.append({"topic_id": page["topic_id"], "error": str(error)})
    sheet = Image.new("RGB", (WIDTH * 4, 3 * (HEIGHT * 2 + 24)), "#333333")
    draw = ImageDraw.Draw(sheet)
    for n, (topic, image) in enumerate(images):
        x, y = n % 2 * WIDTH * 2, n // 2 * (HEIGHT * 2 + 24)
        draw.text((x + 4, y + 4), f"HELP topic{topic}", fill="white")
        sheet.paste(image.resize((WIDTH * 2, HEIGHT * 2), Image.Resampling.NEAREST), (x, y + 24))
    sheet.save(ROOT / "native_help_pages.png")
    proof = {"format": "dk4-help-native-parser-pages-v281", "cases": cases, "failures": failures,
             "actual_native_parser_pairing_and_font_painting_executed": True,
             "link_UI_child_creation_is_observed_contract_not_actual_navigation_proof": True,
             "native_archive_load_full_widgets_gameplay_and_registered_integration_pending": True,
             "playable_ROM_modified": False, "full_goal_complete": False}
    (ROOT / "native_parser_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(cases), "failures": failures}))


if __name__ == "__main__":
    main()
