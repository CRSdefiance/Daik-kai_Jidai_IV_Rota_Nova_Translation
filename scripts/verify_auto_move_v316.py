"""Exact inherited release, patch and actual Auto Move confirmation pixels."""

import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.auto_move_caption import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_auto_move_v316 import CONFIG, ROOT

ROM = Path('out/all_routes_combined_v316_candidate.nds')
PARENT = Path('out/all_routes_combined_v309_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    current, parent, clean, canonical = [NdsImage.open(p) for p in
                                        (ROM, PARENT, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    a = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    b = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
    assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ['/__arm9__.bin']
    expected, plan = apply_release(a['/__arm9__.bin'], clean.read_file('/__arm9__.bin'), canonical.read_file('/__arm9__.bin'), CONFIG)
    assert expected == b['/__arm9__.bin']
    old, new = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
    assert new['candidate_sha256'] == sha(ROM.read_bytes()) and new['profile'] == 'all-routes-unified-v316'
    assert new['batches'] == old['batches'] and len(new['batches']) == 470
    assert new['required_batches'] == old['required_batches'] and all(new['checks'].values())
    assert new['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    for path, records in old['changed_records'].items():
        assert set(records) <= set(new['changed_records'][path])
    for name in ('v309_before_builder.nds', 'v309_after_builder.nds'):
        assert (ROOT / name).read_bytes() == PARENT.read_bytes()
    patch, restored = ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    apply_xdelta(Path('work/clean.nds'), patch, restored)
    assert restored.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'profile': new['profile'],
             'canonical_base': new['base_rom'], 'canonical_sha256': new['base_sha256'],
             'all470_inherited_batches_and_data_art_routes_ARM7_overlays_preserved': True,
             'only_original12_byte_ARM9_caption_slot_changes': True,
             'all_native_code_pointers_descriptors_gates_and_other_bytes_preserved': True,
             'full_V309_before_after_builder_reproduction_exact': True,
             'exact_clean_patch_reconstruction': True, 'label': plan, 'actual_confirmation_pending': True,
             'full_goal_complete': False}
    if args.live:
        directory = Path('work/emulation_v193/auto_move_caption_v316')
        report = read(directory / 'capture_report.json')
        source = read('work/emulation_v193/ordinary_voyage_v315/capture_report.json')
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == 6000 and report['ROM_sha256'] == proof['candidate_sha256']
        assert report['battery_save_preloaded']['source_sha256'] == source['battery_save_preloaded']['source_sha256']
        assert report['scripted_input_schedule'] == read(ROOT / 'replay_inputs.json')
        frames = {}
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            frames[row['frame']] = row
        image = Image.open(frames[6000]['path']).convert('RGB')
        font = GameAsciiFont.from_arm9(b['/__arm9__.bin'])
        matches = []
        for advance in (5, 6):
            for x0 in range(94, 111):
                for y0 in range(275, 295):
                    wanted = {(x0 + n * advance + x, y0 + y) for n, c in enumerate('Auto Move')
                              for y in range(11) for x in range(6) if font.decode(c).getpixel((x, y))}
                    for color in ((0, 8, 0), (0, 0, 0), (8, 8, 8)):
                        actual = {(x, y) for y in range(y0, y0 + 11) for x in range(x0, x0 + 9 * advance)
                                  if image.getpixel((x, y)) == color}
                        if actual == wanted:
                            matches.append({'origin': [x0, y0], 'advance': advance, 'color': color,
                                            'all_first_internal_final_letter_ink_pixels': len(wanted)})
        assert len(matches) == 1, matches
        unchanged, changed = [], []
        seen = set()
        for row in source['frames_captured']:
            number = row['frame']
            if number > 6000 or number not in frames or number in seen:
                continue
            seen.add(number)
            before = Image.open(row['path']).convert('RGB')
            after = Image.open(frames[number]['path']).convert('RGB')
            delta = [(x, y) for y in range(384) for x in range(256) if before.getpixel((x, y)) != after.getpixel((x, y))]
            if delta:
                assert number == 6000 and all(85 <= x < 175 and 265 <= y < 310 for x, y in delta)
                changed.append({'frame': number, 'only_confirmation_rectangle_pixels_change': len(delta)})
            else:
                unchanged.append(number)
        assert len(changed) == 1
        proof.update({'actual_confirmation_pending': False, 'actual_label_glyph_case': matches[0],
                      'unchanged_comparable_whole_frames': unchanged, 'changed_comparable_frames': changed,
                      'genuine_cartridge_save_cold_boot_Continue_to_Auto_Move_Ceuta_confirmation': True,
                      'capture_report': str(directory / 'capture_report.json'),
                      'source_discovery_run_no_surveryor_no_voyage_or_equipment_credit': True})
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in proof.items() if k in ('candidate_sha256', 'patch_sha256', 'actual_confirmation_pending', 'actual_label_glyph_case', 'changed_comparable_frames')}))


if __name__ == '__main__':
    main()
