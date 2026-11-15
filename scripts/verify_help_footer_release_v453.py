"""Exact release ancestry and actual full-English copied Help footer/actions."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.help_footer_release_v2 import transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/help_footer_release_v453')
ROM = Path('out/all_routes_combined_v453_candidate.nds')
PARENT = Path('out/all_routes_combined_v449_candidate.nds')
CAPTURE = Path('work/emulation_v193/help_footer_v453')
LABELS = ('Prev', 'Next', 'Index', 'First', 'Quit', 'Select')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def caption(font, text, image, x, advance):
    mask = Image.new('1', (len(text) * advance + 1, 11))
    for i, char in enumerate(text):
        mask.paste(font.decode(char), (i * advance, 0))
    ink = 0
    for y in range(11):
        for col in range(mask.width):
            expected = bool(mask.getpixel((col, y)))
            assert (image.getpixel((x + col, 370 + y)) == (230, 230, 230)) == expected, (text, col, y)
            ink += expected
    return {'text': text, 'origin': [x, 370], 'advance': advance, 'full_ink_pixels': ink,
            'all_first_interior_final_glyphs_and_blank_cells_exact': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    m, pm = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert m['candidate_sha256'] == digest and m['profile'] == 'all-routes-unified-v453'
    assert m['base_sha256'] == pm['base_sha256'] and m['batches'] == pm['batches'] and len(m['batches']) == 470
    assert m['required_batches'] == pm['required_batches'] and all(m['checks'].values())
    rp = Path('translations/release_stack.json')
    assert m['release_stack_sha256'] == sha(rp.read_bytes())
    profiles = read(rp)['profiles']
    assert all(profiles[m['profile']][k] == v for k, v in profiles['all-routes-unified-v449'].items() if k not in ('description', 'note'))
    a, b = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ['/__arm9__.bin']
    arm, changes = transform(a['/__arm9__.bin'])
    assert arm == b['/__arm9__.bin'] == Path('work/analysis/help_footer_v452/research_arm9.bin').read_bytes()
    native_path = Path('work/analysis/help_footer_v452/native_proof.json')
    native = read(native_path)
    assert native['target_arm9_sha256'] == sha(arm)
    assert len(native['all256_original_and_copied_Help_footer_native_cases']) == 256
    config = read(Path('translations/help_footer_release_v2.json'))
    assert config['native_proof_sha256'] == sha(native_path.read_bytes())
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstruction = ROOT / 'patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    report_path = CAPTURE / 'capture_report.json'
    r = read(report_path)
    assert r['ROM_sha256'] == digest and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
    assert r['frames'] == 23200
    for row in r['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    font = GameAsciiFont.from_arm9(arm)
    actions, footers = [], []
    for frame, heading in ((21600, 'Data Guide'), (22000, 'Sea Info'), (22200, 'Coordinates'),
                           (22400, 'Sea Info'), (22600, 'Coordinates'), (22800, 'Shared Commands'), (23000, 'Help Index')):
        image = Image.open(CAPTURE / f'frame_{frame:06d}_navigation.png').convert('RGB')
        count, bounds = complete_mask(font, heading, image, 0, 192, (123, 246, 123))
        actions.append({'frame': frame, 'heading': heading, 'full_glyph_pixels': count, 'bounds': bounds})
        snapshot = CAPTURE / f'frame_{frame:06d}_arm9_ram.bin'
        raw = snapshot.read_bytes()
        recorded = next(x for x in r['read_only_pause_RAM_snapshots'] if x['frame'] == frame)
        assert sha(raw) == recorded['sha256']
        pointers = list(struct.unpack_from('<6I', raw, 0x2CF7DC + 0x14))
        metadata = list(struct.unpack_from('<18h', raw, 0x2CF7DC + 0x2C))
        complete = []
        for i, pointer in enumerate(pointers):
            left, width, _ = metadata[i * 3:i * 3 + 3]
            if not pointer:
                assert left == -1
                continue
            text = raw[pointer - 0x02000000:].split(b'\0', 1)[0].decode('ascii')
            assert text == LABELS[i]
            advance = width // len(text)
            assert advance in (5, 6) and width == advance * len(text)
            assert 0 <= left and left + 14 + width + 2 <= 256
            complete.append(caption(font, text, image, left + 14, advance))
        footers.append({'frame': frame, 'actual_cached_descriptor': pointers,
                        'actual_native_metadata': metadata, 'complete_labels': complete})
    all_six = next(f for f in footers if f['frame'] == 22400)
    assert [x['text'] for x in all_six['complete_labels']] == list(LABELS)
    assert all(x['advance'] == 5 for x in all_six['complete_labels'])
    assert Image.open(CAPTURE / 'frame_022200_navigation.png').tobytes() == Image.open(CAPTURE / 'frame_022600_navigation.png').tobytes()
    parent = read(Path('work/emulation_v193/crew_help_v449/capture_report.json'))
    old = {x['frame']: x for x in parent['frames_captured'] if 'cold_boot' in x['path']}
    exact, footer_only = [], []
    for row in r['frames_captured']:
        f = row['frame']
        if 'cold_boot' not in row['path'] or f > 21200:
            continue
        x, y = Image.open(row['path']), Image.open(old[f]['path'])
        assert x.crop((0, 0, 256, 368)).tobytes() == y.crop((0, 0, 256, 368)).tobytes()
        (exact if x.tobytes() == y.tobytes() else footer_only).append(f)
    assert len(exact) + len(footer_only) == 56
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'exact_clean_patch_reconstruction': True, 'parent': str(PARENT), 'parent_sha256': sha(PARENT.read_bytes()),
             'profile': m['profile'], 'base': m['base_rom'], 'base_sha256': m['base_sha256'],
             'only_ARM9_changed_from_V449': True, 'all470_inherited_batches_stages_artwork_HELP_and_routes_exact': True,
             'native256_direct_and_copied_descriptor_cases_pass': True, 'actual_complete_footer_cases': footers,
             'actual_Prev_Next_First_Index_actions': actions, 'actual_all_six_complete_labels_fit': True,
             'actual_Prev_Next_full_page_return_exact': True,
             'pre_Help_whole_frames_exact': exact, 'pre_Help_frames_only_footer_changed': footer_only,
             'all56_non_footer_regions_exact': True, 'transform': changes,
             'Help_footer_Japanese_labels_resolved': True, 'V451_rejected_and_not_parent': True,
             'hardware_device_verification': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False,
             'release_status': 'experimental'}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V453 actual full-English footer:all6 captions complete,actions/history pass;56 unchanged non-footer regions;exact full-stack patch.')


if __name__ == '__main__':
    main()
