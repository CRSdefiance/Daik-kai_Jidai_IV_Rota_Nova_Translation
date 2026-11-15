"""Inspect original cargo scene callbacks and reproduce the captured composition."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_INVALID, UcError
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.research_town_scene_v644 import setup
from scripts.verify_dialogue_palette_v628 import captured_rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/cargo_tooltip_v655')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/full_fleet_victory_v654_replay')
ROM = Path('out/all_routes_combined_v653_candidate.nds')
CONTEXT, LOWER, UPPER, FRAME_BYTES = 0x023117C4, 0x022E1794, 0x022F9794, 98304


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
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
    nodes, node = [], struct.unpack_from('<I', raw, CONTEXT - BASE + 16)[0]
    while node:
        assert node not in {n['node'] for n in nodes} and len(nodes) < 100
        vt = struct.unpack_from('<I', raw, node - BASE)[0]
        predicate, draw = struct.unpack_from('<2I', raw, vt - BASE + 8)
        nodes.append({'node': node, 'vtable': vt, 'predicate': predicate, 'draw': draw})
        node = struct.unpack_from('<I', raw, node - BASE + 8)[0]
    methods = {n['draw'] for n in nodes}
    calls = []

    def hook(cpu, address, size, unused):
        if address in methods:
            calls.append({'draw': address, 'node': cpu.reg_read(UC_ARM_REG_R0),
                          'context': cpu.reg_read(UC_ARM_REG_R1)})

    h = u.hook_add(UC_HOOK_CODE, hook)
    invalid = []

    def unmapped(cpu, kind, address, size, value, unused):
        invalid.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address, 'size': size, 'kind': kind})
        return False

    h2 = u.hook_add(UC_HOOK_MEM_INVALID, unmapped)
    u.mem_write(LOWER, b'\xA5' * (FRAME_BYTES * 2))
    u.reg_write(UC_ARM_REG_R4, CONTEXT)
    u.reg_write(UC_ARM_REG_R5, CONTEXT + 12)
    u.reg_write(UC_ARM_REG_SP, STACK)
    error = None
    try:
        u.emu_start(0x020D32B8, 0x020D3314, count=50000000)
        assert u.reg_read(UC_ARM_REG_PC) == 0x020D3314
    except (AssertionError, ValueError, UcError) as exc:
        error = repr(exc)
    finally:
        u.hook_del(h)
        u.hook_del(h2)
    out = bytes(u.mem_read(LOWER, FRAME_BYTES * 2))
    (ROOT / 'diagnostic_whole_scene.bin').write_bytes(out)
    actual = Image.open(CAP / f'frame_{frame:06d}_navigation.png').convert('RGB')
    images, differences = [], []
    # Main compositor stores lower then upper. Presentation puts upper first.
    for offset, y0 in ((FRAME_BYTES, 0), (0, 192)):
        words = struct.unpack('<49152H', out[offset:offset + FRAME_BYTES])
        image = Image.new('RGB', (256, 192))
        image.putdata([captured_rgb(w) for w in words])
        images.append(image)
        crop = actual.crop((0, y0, 256, y0 + 192))
        differences.append(sum(a != b for a, b in zip(image.get_flattened_data(), crop.get_flattened_data(), strict=True)))
    combined = Image.new('RGB', (256, 384))
    combined.paste(images[0], (0, 0))
    combined.paste(images[1], (0, 192))
    combined.save(ROOT / 'diagnostic_whole_scene.png')
    save(ROOT / 'diagnostic.json', {'frame': frame, 'RAM_sha256': sha(raw), 'mapping': mapping,
         'nodes': nodes, 'executed_draws': calls, 'error': error,
         'unmapped_accesses': invalid,
         'whole_upper_lower_RGB_difference_counts': differences,
         'not_yet_final_verification': True, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('Cargo callbacks', calls, 'error', error, 'upper/lower differences', differences)


if __name__ == '__main__':
    main()
