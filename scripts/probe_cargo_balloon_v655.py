"""Run the actual banner and balloon callbacks in their original scene order."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call
from scripts.research_town_scene_v644 import setup
from scripts.verify_dialogue_palette_v628 import captured_rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/cargo_tooltip_v655')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_victory_v654_replay')
ROM = Path('out/all_routes_combined_v653_candidate.nds')
LOWER, UPPER, FRAME_BYTES = 0x022E1794, 0x022F9794, 98304


def main():
    frame = 23200
    rom = NdsImage.open(ROM)
    raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
    state = read(CAP / f'native_state_{frame:06d}/native_state.json')
    blobs = {}
    for key in ('ITCM', 'DTCM', '9REG', 'LCDM'):
        row = state['regions'][key]
        blobs[key] = Path(row['path']).read_bytes()
        assert sha(blobs[key]) == row['sha256']
    u, mapping = setup(rom, raw, blobs['9REG'], blobs['LCDM'], blobs['DTCM'])
    u.mem_write(0x01FF0000, blobs['ITCM'])
    u.mem_write(0x01FF8000, blobs['ITCM'])
    parent = 0x0218A7B0
    vt = struct.unpack_from('<I', raw, parent - BASE)[0]
    base_offset = struct.unpack_from('<I', raw, vt - BASE - 16)[0]
    assert base_offset == 0x31F8
    owner = struct.unpack_from('<I', raw, parent - BASE + base_offset + 20)[0]
    context = owner - 12
    assert context == 0x023117C4
    node, nodes = struct.unpack_from('<I', raw, context - BASE + 16)[0], []
    while node:
        assert node not in {r['node'] for r in nodes} and len(nodes) < 100
        vtable = struct.unpack_from('<I', raw, node - BASE)[0]
        nodes.append({'node': node, 'draw': struct.unpack_from('<I', raw, vtable - BASE + 12)[0]})
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    banner_node = parent + 0x3070 + 0x44
    assert next(r['draw'] for r in nodes if r['node'] == banner_node) == 0x0200CAF8
    balloon = next(r['node'] for r in nodes if r['draw'] == 0x020068AC)
    assert nodes.index(next(r for r in nodes if r['node'] == banner_node)) < nodes.index(next(r for r in nodes if r['node'] == balloon))
    u.mem_write(LOWER, b'\xA5' * (FRAME_BYTES * 2))
    trace = []

    def hook(cpu, address, size, unused):
        if address in (0x020CFC14, 0x020D3338, 0x020D5404, 0x020D5A18, 0x020D5A2C):
            trace.append({'PC': address, 'R0': cpu.reg_read(UC_ARM_REG_R0), 'R1': cpu.reg_read(UC_ARM_REG_R1)})

    h = u.hook_add(UC_HOOK_CODE, hook)
    try:
        call(u, 0xCAF8, (banner_node, context), instruction_limit=1000000)
        before = bytes(u.mem_read(LOWER, FRAME_BYTES))
        executed = call(u, 0x68AC, (balloon, context), instruction_limit=1000000)
    finally:
        u.hook_del(h)
    out = bytes(u.mem_read(LOWER, FRAME_BYTES))
    actual = Image.open(CAP / f'frame_{frame:06d}_navigation.png').convert('RGB')
    def image(data):
        result = Image.new('RGB', (256, 192))
        result.putdata([captured_rgb(w) for w in struct.unpack('<49152H', data)])
        return result
    im = image(out)
    crop, expected = im.crop((0, 69, 256, 85)), actual.crop((0, 261, 256, 277))
    diff = sum(a != b for a, b in zip(crop.get_flattened_data(), expected.get_flattened_data(), strict=True))
    crop.save(ROOT / 'native_banner_balloon_composition.png')
    image(before).crop((0, 69, 256, 85)).save(ROOT / 'native_banner_before_balloon.png')
    (ROOT / 'native_balloon_output.bin').write_bytes(out)
    save(ROOT / 'balloon_probe.json', {'frame': frame, 'parent': parent, 'parent_base_offset': base_offset,
        'actual_context': context, 'original_owner_link': owner,
        'banner_node': banner_node, 'balloon_node': balloon,
        'balloon_declared_rect': list(struct.unpack_from('<4I', raw, balloon - BASE + 32)),
        'executed_original_addresses': sorted(executed), 'trace': trace, 'mapping': mapping,
        'complete4096_banner_RGB_difference_count': diff,
        'two_original_native_callbacks_complete_and_ABI_pass': True,
        'whole_scene_not_claimed': True, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('Original balloon', hex(balloon), 'rect', struct.unpack_from('<4I', raw, balloon - BASE + 32), '4096 banner differences', diff)


if __name__ == '__main__':
    main()
