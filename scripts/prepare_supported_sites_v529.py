"""Only unlock original Gallery entries with real image owners; copied save."""

import json
import struct
import subprocess
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

OUT = Path('work/analysis/site_descriptions_v529')


def main():
    source = json.loads((OUT / 'source_inventory.json').read_text(encoding='utf-8'))
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    rom = Path('out/all_routes_combined_v528_candidate.nds')
    current = NdsImage.open(rom).read_file('/__arm9__.bin')
    table = source['image_table']
    assert clean[table:table + 84] == current[table:table + 84]
    ram = Path('E:/Rota Nova translations/Generated/work/emulation_v193/site_image_probe_v529/final_arm9_ram.bin').read_bytes()
    supported, excluded = [], []
    for row in source['source_rows']:
        index = row['site_id']
        pointer = struct.unpack_from('<I', clean, table + index * 4)[0]
        assert pointer == row['image_owner_pointer']
        if not pointer:
            assert index in (1, 4) and row['japanese'] == '無い無い'
            excluded.append(index)
            continue
        string = struct.unpack_from('<I', ram, pointer - 0x02000000 + 12)[0]
        path = ram[string - 0x02000000:string - 0x02000000 + 128].split(b'\0')[0].decode('ascii')
        assert path == f'Iseki/Iseki{len(supported):02d}.pxl'
        supported.append(index)
    fixture = OUT / 'supported_fixture'
    subprocess.run([sys.executable, 'scripts/prepare_collection_gallery_v526.py',
                    '--site-ids', *(str(i) for i in supported), '--skip-items', '--out', str(fixture)], check=True)
    manifest = fixture / 'save_fixture_manifest.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['production_ROM'], data['production_ROM_sha256'] = str(rom), sha(rom.read_bytes())
    data['original_available_site_image_ids'] = supported
    data['excluded_original_null_image_placeholder_ids'] = excluded
    data['only_supported_source_Gallery_images_selected'] = True
    data['source_image_pointer_table'] = table
    manifest.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    events = json.loads(Path('work/analysis/collection_gallery_v526/ruins_inputs.json').read_text(encoding='utf-8'))
    events.append({'start': 2801, 'duration': 8, 'buttons': ['A']})
    frames = [3200 + i * 200 for i in range(19)]
    for frame in frames[1:]:
        events.append({'start': frame - 199, 'duration': 8, 'buttons': ['A']})
    wrap = frames[-1] + 200
    events.extend([{'start': wrap - 199, 'duration': 8, 'buttons': ['A']},
                   {'start': wrap + 1, 'duration': 8, 'buttons': ['B']}])
    (OUT / 'inputs.json').write_text(json.dumps(events, indent=2) + '\n', encoding='utf-8')
    (OUT / 'run_plan.json').write_text(json.dumps({'supported_site_ids': supported, 'image_frames': frames,
                                                 'wrap_frame': wrap, 'return_frame': wrap + 200,
                                                 'final_frame': wrap + 400, 'excluded_ids': excluded}, indent=2) + '\n', encoding='utf-8')
    print('19 real image owners selected; null/placeholder IDs1/4 excluded; normal original carousel scheduled.')


if __name__ == '__main__':
    main()
