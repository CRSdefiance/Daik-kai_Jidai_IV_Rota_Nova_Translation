"""Original packet accessors and four player-card setters in isolated captured RAM."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.research_town_scene_v644 import setup
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/race_roster_v661')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/race_roster_v661_controlled_ring')


def main():
    rom = NdsImage.open('out/all_routes_combined_v653_candidate.nds')
    raw = (CAP / 'frame_004590_arm9_ram.bin').read_bytes()
    state = read(CAP / 'capture_native_state_004590/native_state.json')
    region = lambda key: Path(state['regions'][key]['path']).read_bytes()
    u, mapping = setup(rom, raw, region('9REG'), region('LCDM'), region('DTCM'))
    u.mem_write(0x01FF0000, region('ITCM'))
    u.mem_write(0x01FF8000, region('ITCM'))
    executed, rows = set(), []
    lower_base = 0x022E1794
    boxes = [(4, 6, 68, 78), (188, 6, 252, 78), (4, 84, 68, 156), (188, 84, 252, 156),
             (68, 6, 184, 40), (72, 44, 188, 78), (68, 84, 184, 118), (72, 122, 188, 156)]
    output_bytes = {lower_base + (y * 256 + x) * 2 + byte
                    for x1, y1, x2, y2 in boxes for y in range(y1, y2)
                    for x in range(x1, x2) for byte in range(2)}
    for x1, y1, x2, y2 in boxes:
        for y in range(y1, y2):
            u.mem_write(lower_base + (y * 256 + x1) * 2, b'\xA5' * ((x2 - x1) * 2))
    written = set()

    def write(cpu, kind, address, size, value, data):
        if lower_base <= address < lower_base + 98304:
            assert all(p in output_bytes for p in range(address, address + size))
            written.update(range(address, address + size))

    def memory_read(cpu, kind, address, size, value, data):
        if lower_base <= address < lower_base + 98304:
            assert all(p in written for p in range(address, address + size))

    handle = u.hook_add(UC_HOOK_CODE, lambda cpu, a, size, data: executed.add(a))
    h2 = u.hook_add(UC_HOOK_MEM_WRITE, write)
    h3 = u.hook_add(UC_HOOK_MEM_READ, memory_read)
    root, packet_base, mask, sdk = 0x021929B4, 0x0237B644, 0x0237B640, 0x0237BBC0
    arm = rom.read_file('/__arm9__.bin')
    try:
        own = raw[packet_base - BASE:packet_base - BASE + 52]
        u.mem_write(mask, struct.pack('<2H', 15, 15))
        for index in range(4):
            pointer = packet_base + index * 52
            character = (3, 0, 1, 2)[index]
            packet = bytearray(own)
            name_pointer = struct.unpack_from('<I', arm, 0x120B80 + character * 32)[0] - BASE
            name = arm[name_pointer:name_pointer + 17].split(b'\0')[0]
            ship = b'Chun' if index == 0 else f'Test Ship {index + 1}'.encode('ascii')
            struct.pack_into('<I', packet, 8, character)
            packet[16:33] = name.ljust(17, b'\0')
            packet[33:52] = ship.ljust(19, b'\0')
            u.mem_write(pointer, bytes(packet))
            call(u, 0x10C524, (sdk, mask, index))
            selected = u.reg_read(UC_ARM_REG_R0)
            assert selected == pointer
            call(u, 0xFA5B0, (root, index, selected))
            assert bytes(u.mem_read(root + 0xD0 + index * 17, 17)) == packet[16:33]
            assert bytes(u.mem_read(root + 0x114 + index * 19, 19)) == packet[33:52]
            card = 0x02192820 + index * 0x4C
            call(u, 0xFAD38, (card, character, root + 0xD0 + index * 17, root + 0x114 + index * 19),
                 instruction_limit=1000000)
            assert struct.unpack('<I', u.mem_read(card + 0x10, 4))[0] == character
            call(u, 0xFABB0, (card, root), instruction_limit=3000000)
            rows.append({'index': index, 'character': character, 'name': name.decode('ascii'),
                         'ship': ship.decode('ascii'), 'packet': pointer, 'card': card})
            print('Native card complete:', rows[-1], flush=True)
    finally:
        u.hook_del(handle)
        u.hook_del(h2)
        u.hook_del(h3)
        save(ROOT / 'native_roster_research.json', {'completed_cards': rows,
            'executed_instruction_addresses': sorted(executed), 'bank_mapping': mapping,
            'isolated_fixture_not_wireless': True})
    lower = bytes(u.mem_read(0x022E1794, 98304))
    assert written == output_bytes and len(output_bytes) == 68416
    assert lower == raw[lower_base - BASE:lower_base - BASE + 98304]
    registered = machine(arm)
    clean_rom = NdsImage.open('work/clean.nds')
    clean = machine(clean_rom.read_file('/__arm9__.bin'))
    for image, cpu in ((rom, registered), (clean_rom, clean)):
        overlay = loadOverlayTable(image.rom.arm9OverlayTable, lambda i, f, image=image: image.files[f])[0]
        cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    for address in executed:
        word = bytes(u.mem_read(address, 4))
        assert word == bytes(registered.mem_read(address, 4)), hex(address)
        assert word == bytes(clean.mem_read(address, 4)), hex(address)
    (ROOT / 'native_four_cards_lower.bin').write_bytes(lower)
    save(ROOT / 'native_roster_research.json', {'completed_cards': rows,
        'executed_instruction_addresses': sorted(executed), 'bank_mapping': mapping,
        'isolated_fixture_not_wireless': True, 'lower_sha256': sha(lower),
        'source_card_boxes': boxes, 'all34208_card_pixels_assigned_over_poison': True,
        'no_card_output_read_before_write': True, 'all_other_lower_bytes_unchanged': True,
        'every_executed_instruction_exact_registered_and_clean_ROM': True,
        'complete98304_lower_bytes_match_capture': True})


if __name__ == '__main__':
    main()
