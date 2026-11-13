"""Prepare disposable actual/blank atlas crop controls; no playable release.

Only research ARM9 crop-selection words and, in blank controls, the five source
cells' foreground indices differ. The actual atlas always remains production art.
"""

import json
import struct
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import rom_files
from scripts.probe_button_prompt_native import machine
from scripts.verify_marker_ownership_v569 import PATCHES

ROOT = Path('work/analysis/miniature_crops_v579')
PARENT = Path('out/all_routes_combined_v573_candidate.nds')
PARENT_SHA = 'f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77'
FILE = '/_pxl/__frame.pxl'
OWNER = 0x02313F60
RECTANGLE = (184, 32, 256, 56)


def main():
    assert sha(PARENT.read_bytes()) == PARENT_SHA
    manifest = json.loads(PARENT.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256'] == PARENT_SHA and manifest['profile'] == 'all-routes-unified-v573'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and len(registry['accepted_layers']) == 114
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    original = NdsImage.open(PARENT)
    files = rom_files(original)
    arm = files['/__arm9__.bin']
    mapped = machine(arm)
    assert int.from_bytes(mapped.mem_read(0x020854DC, 4), 'little') == 0x02313C7C
    image = PxlImage.from_bytes(files[FILE])
    blank = PxlImage.from_bytes(files[FILE])
    batch = json.loads(Path('translations/frame_action_buttons_graphics_v7.json').read_text(encoding='utf-8'))
    records = [row for row in batch['records'][15:] if row['text'] not in ('M', 'D')]
    ink = []
    for row in records:
        left, top, right, bottom = row['box']
        assert 184 <= left < right <= 256 and 32 <= top < bottom <= 56
        for y in range(top, bottom):
            for x in range(left, right):
                index = y * 256 + x
                assert image.indices[index] in (0, 9)
                if image.indices[index] == 9:
                    ink.append([x, y])
                    blank.indices[index] = 0
    assert len(ink) == 307 and len(set(map(tuple, ink))) == 307
    assert blank.source[:blank.pixels_offset] == image.source[:image.pixels_offset]
    assert sum(a != b for a, b in zip(blank.indices, image.indices, strict=True)) == 307
    control = blank.to_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    fixtures = []
    for bank in (0, 9):
        patches = dict(PATCHES)
        patches.update({0x020852BC: 0xE3A00048, 0x020852C0: 0xE3A01018,
                        0x020852C4: 0xE3A02000 | bank,
                        0x020852D8: 0xE3A020B8, 0x020852DC: 0xE3A03020,
                        0x020854DC: OWNER})
        modified = bytearray(arm)
        changes = []
        for address, word in patches.items():
            pattern = bytes(mapped.mem_read(address - 16, 32))
            assert arm.count(pattern) == 1
            offset = arm.find(pattern) + 16
            modified[offset:offset + 4] = struct.pack('<I', word)
            changes.append({'RAM': address, 'file_offset': offset,
                            'before': arm[offset:offset + 4].hex(), 'after': struct.pack('<I', word).hex()})
        assert len(changes) == 10 and len(modified) == len(arm)
        for kind in ('actual', 'blank'):
            rom = NdsImage.open(PARENT)
            rom.replace_file('/__arm9__.bin', bytes(modified))
            if kind == 'blank':
                rom.replace_file(FILE, control)
            path = ROOT / f'MINIATURES_palette{bank}_{kind.upper()}_RESEARCH_ONLY.nds'
            rom.save(path)
            saved = rom_files(NdsImage.open(path))
            changed = sorted(p for p in files if files[p] != saved[p])
            assert changed == (['/__arm9__.bin'] if kind == 'actual' else ['/__arm9__.bin', FILE])
            fixtures.append({'kind': kind, 'palette_bank': bank, 'parent': str(PARENT),
                             'parent_sha256': PARENT_SHA, 'ROM': str(path), 'ROM_sha256': sha(path.read_bytes()),
                             'changes': changes, 'changed_internal_files': changed,
                             'source_rectangle': list(RECTANGLE), 'resource_owner': OWNER,
                             'research_only_not_for_handoff': True, 'manual_crop_not_ordinary_parent': True,
                             'actual_production_atlas_preserved': kind == 'actual',
                             'blank_control_only_307_glyph_indices_replaced_by_zero': kind == 'blank'})
    previous_report = json.loads(Path('E:/Rota Nova translations/Generated/work/emulation_v193/confirm_material_v573_actual/capture_report.json').read_text(encoding='utf-8'))
    save = previous_report['battery_save_preloaded']
    assert sha(Path(save['source']).read_bytes()) == save['source_sha256']
    (ROOT / 'inputs.json').write_text(json.dumps(previous_report['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    result = {'parent': str(PARENT), 'parent_sha256': PARENT_SHA, 'fixtures': fixtures,
              'resource': FILE, 'resource_sha256': sha(image.source),
              'control_resource_sha256': sha(control), 'source_rectangle': list(RECTANGLE),
              'five_caption_records': [{'id': row['id'], 'text': row['text'], 'box': row['box']} for row in records],
              'all307_changed_source_points': ink, 'source_save': save['source'],
              'source_save_sha256': save['source_sha256'], 'production_changed': False,
              'five_ordinary_consumers_remain_unresolved': True, 'full_goal_complete': False}
    (ROOT / 'fixture_manifest.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Four research fixtures: exact actual atlas plus307-point blank controls, source crop72x24, banks0/9; production unchanged.')


if __name__ == '__main__':
    main()
