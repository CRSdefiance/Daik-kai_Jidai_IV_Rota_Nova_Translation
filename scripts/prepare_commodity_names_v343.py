"""Verify all commodity metadata/getters and complete English name rasters."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.commodity_names_research import COUNT, TABLE, transform
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.execute_sailing_footer_v317 import execute
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_scene_caption_raster import expected_pixels

ROOT = Path('work/analysis/commodity_names_v343')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean = [NdsImage.open(p).read_file('/__arm9__.bin') for p in
                      ('out/all_routes_combined_v342_candidate.nds', 'work/clean.nds')]
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    target, plan = transform(current, clean, manuscript)
    u = machine(target)
    u.mem_write(POOL, bytes(MainCodeFile(target, BASE).sections[3].data[:-48]))
    getters, rasters = [], []
    for row in plan['names']:
        call(u, 0xCD1AC, (row['index'],))
        address = u.reg_read(UC_ARM_REG_R0)
        assert address == BASE + TABLE + row['index'] * 12
        record = bytes(u.mem_read(address, 12))
        pointer = struct.unpack_from('<I', record)[0]
        assert pointer == row['pointer']
        value = bytes(u.mem_read(pointer, 64)).split(b'\0', 1)[0]
        assert value.decode('ascii') == row['English']
        assert record[4:] == current[TABLE + row['index'] * 12 + 4:TABLE + row['index'] * 12 + 12]
        getters.append({'index': row['index'], 'complete_name': row['English'], 'metadata_exact': True})
        if row['changed']:
            for mode in (4, 16):
                text = row['English']
                reference = text + (' ' if mode == 4 and len(text) % 2 else '')
                r = execute(target, text, x=0, y=0, tracking=0, mode=mode, buffered_context=True)
                assert r['pixels'] == expected_pixels(target, reference, 0, 0, mode, advance=6)
                rasters.append({'index': row['index'], 'text': text, 'mode': mode,
                                'complete_native_ink_and_blank_cells': True, 'width': len(text) * 6})
    assert len(getters) == COUNT and len(rasters) == 98
    (ROOT / 'research_arm9.bin').write_bytes(target)
    (ROOT / 'native_proof.json').write_text(json.dumps({'transform': plan, 'native_getters': getters,
                                                     'native_rasters': rasters,
                                                     'supplied_unclipped_raster_geometry_not_all_UI_parents': True,
                                                     'registration_insertion_actual_contexts_and_layout_pending': True}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'all124_native_getters': True, 'fresh49_names': True, 'complete_native_rasters': len(rasters),
                      'UI_bounds_and_actual_playback_still_pending': True}))


if __name__ == '__main__':
    main()
