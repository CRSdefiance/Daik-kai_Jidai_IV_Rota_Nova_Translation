"""Prepare source-locked complete Square labels and the cumulative test profile."""

import copy
import struct
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.plaza_distribution_label import transform
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import HEADER, POINT, STACK, STRING, call, machine
from scripts.verify_village_wrap_v608 import read, save


def main():
    source = NdsImage.open('out/all_routes_combined_v621_candidate.nds').read_file('/__arm9__.bin')
    target, proof = transform(source)
    root = Path('work/analysis/plaza_distribution_v623')
    root.mkdir(exist_ok=True)
    font = GameAsciiFont.from_arm9(target)
    palette = target[0x125A20:0x125A40]
    cases = []
    for text in ('Trends', 'Distribute Goods'):
        u = machine(target)
        image = struct.pack('<5I', 4, 64, 16, 20, 52) + palette + bytes(2048)
        u.mem_write(HEADER - 16, b'\xA5' * (len(image) + 32))
        u.mem_write(HEADER, image)
        u.mem_write(POINT, struct.pack('<2I', 0, 0))
        u.mem_write(STRING, text.encode('ascii') + b'\0')
        u.mem_write(STACK, struct.pack('<I', 1))
        call(u, 0xD1604, (0, HEADER, POINT, STRING))
        expected = bytearray(2048)
        ink = 0
        for i, char in enumerate(text):
            glyph = font.decode(char)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        px = i * 6 + x
                        expected[(y * 256 + px) // 2] |= 1 << (4 * (px % 2))
                        ink += 1
        assert bytes(u.mem_read(HEADER + 52, 2048)) == expected
        assert bytes(u.mem_read(HEADER - 16, 16)) == bytes(u.mem_read(HEADER + len(image), 16)) == b'\xA5' * 16
        cases.append({'text': text, 'source_native_font_ink': ink, 'complete_native_cells_width': len(text) * 6,
                      'whole_256x16_plane_and_guards_exact': True, 'actual_menu_GPU_not_inferred': True})
    proof['records'][0]['review']['formatting'] = True
    proof['native_label_fit_cases'] = cases
    save(root / 'native_label_fit_proof.json', proof)
    save('translations/plaza_distribution_label_v1.json', {'format': 'dk4-plaza-distribution-label-v1', 'proof': proof})
    path = Path('translations/release_stack.json')
    registry = read(path)
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v621'])
    profile.update({'plaza_distribution_label': 'translations/plaza_distribution_label_v1.json',
                    'description': 'Complete V621 plus full source-faithful Distribute Goods action in the Square menu.',
                    'note': 'Experimental. Original distribution availability rules and all prior layers retained; two exclusive strings repacked with no pool growth. Actual two-row menu and distribution gameplay require cold-boot verification.'})
    registry['profiles']['all-routes-unified-v623'] = profile
    save(path, registry)
    print('Registered experimental V623: complete Distribute Goods label,2 full native font rasters,zero pool growth.')


if __name__ == '__main__':
    main()
