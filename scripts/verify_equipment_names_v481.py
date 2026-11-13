"""All original item-name rasters and native tooltip placement contracts."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_inventory_fixture_v481 import transfer
from scripts.probe_button_prompt_native import STACK, STOP, call, machine
from scripts.verify_common_alignment_native_v257 import raster

ROOT = Path('work/analysis/equipment_names_v481')
ROM = Path('out/all_routes_combined_v474_candidate.nds')
SNAPSHOT = Path('work/emulation_v193/weapon_reload_v477/final_arm9_ram.bin')


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    # The inherited raster helper reads the V255 font; verify it is current.
    assert rom.read_file('/GRP/KANJI.FNT') == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    names = json.loads((ROOT / 'measured_names.json').read_text(encoding='utf-8'))
    assert [r['item'] for r in names] == list(range(218))
    font = GameAsciiFont.from_arm9(arm)
    raw = SNAPSHOT.read_bytes()
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    store = u.reg_read(UC_ARM_REG_R0)
    realframe = struct.unpack('<I', u.mem_read(0x02394780, 4))[0]
    template = bytes(u.mem_read(realframe, 128))
    frame, point, textptr, measured = 0x02460020, 0x02461020, 0x02462020, 0x02463020
    stop = u.hook_add(UC_HOOK_CODE, lambda cpu, address, size, data: cpu.emu_stop() if address == 0x0200761C else None)
    cases = []
    try:
        for row in names:
            call(u, 0x4A53C, (store + 4 + row['item'] * 20,))
            nameptr = u.reg_read(UC_ARM_REG_R0)
            text = bytes(u.mem_read(nameptr, 160)).split(b'\0')[0].decode('cp932')
            assert text == row['name'] and text.isascii()
            call(u, 0x77FC, (measured, realframe, nameptr))
            width, height = struct.unpack('<2I', u.mem_read(measured, 8))
            assert (width, height) == (row['width'], row['height'])
            pixels = raster(arm, text.encode('ascii'), 0xD5404, size=(240, 32))
            actual = {(i % 240, i // 240) for i, value in enumerate(pixels) if value}
            expected = {(n * 6 + x, y) for n, c in enumerate(text)
                        for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
            assert actual == expected
            placements = []
            for x in (16, 64, 112, 160, 208):
                u.mem_write(frame, template)
                u.mem_write(point, struct.pack('<2i', x, 32))
                u.mem_write(textptr, text.encode('ascii') + b'\0')
                u.mem_write(STACK, struct.pack('<4I', 0, 0, 1, 0xffffffff))
                u.reg_write(UC_ARM_REG_SP, STACK)
                u.reg_write(UC_ARM_REG_LR, STOP)
                for reg, val in ((UC_ARM_REG_R0, frame), (UC_ARM_REG_R1, textptr), (UC_ARM_REG_R2, point), (UC_ARM_REG_R3, 0)):
                    u.reg_write(reg, val)
                u.emu_start(0x02007430, STOP, count=20000)
                assert u.reg_read(UC_ARM_REG_PC) == 0x0200761C
                rect = list(struct.unpack('<4i', u.mem_read(u.reg_read(UC_ARM_REG_R2), 16)))
                assert rect[2] - rect[0] == width + 4 and rect[3] - rect[1] == 16
                assert 16 <= rect[0] < rect[2] <= 240 and 16 <= rect[1] < rect[3] <= 176
                placements.append({'anchor': [x, 32], 'paper_rect_local': rect})
            cases.append({**row, 'ink_pixels': len(actual), 'complete_native_raster_exact': True, 'placements': placements})
    finally:
        u.hook_del(stop)
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    for name, anchor, rect in (('Golden Cutlass',16,[16,16,104,32]),('Blue Oak Shield',64,[64,16,158,32]),('Travels of Marco Polo',112,[94,16,224,32])):
        sample = next(r for r in cases if r['name'] == name)
        assert next(p for p in sample['placements'] if p['anchor'][0] == anchor)['paper_rect_local'] == rect
    fixture, fixture_report = transfer(arm, raw, [40,71,83])
    assert fixture != raw and SNAPSHOT.read_bytes() == raw
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'snapshot_sha256': sha(raw),
             'name_count': len(cases), 'placement_contract_count': len(cases)*5, 'cases': cases,
             'native_inventory_fixture_trial': fixture_report, 'source_RAM_preserved': True,
             'limits': ['Placement contracts do not assert every item is eligible in every equipment slot.',
                        'Native rasters and geometry are isolated CPU evidence, not all-name GPU captures.',
                        'Synthetic inventory is not normal acquisition or unlock evidence.'], 'goal_complete': False}
    (ROOT / 'name_proof.json').write_text(json.dumps(proof, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'names':len(cases), 'placements':len(cases)*5, 'fixture_items':fixture_report['items']}))


if __name__ == '__main__':
    main()
