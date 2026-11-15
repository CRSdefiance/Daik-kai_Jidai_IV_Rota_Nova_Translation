"""Verify cumulative V378 integration, exact patch, and final emulator captures."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text

ROOT = Path('work/analysis/alignment_release_v378')
ROM = Path('out/all_routes_combined_v378_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def files(image):
    return {n: d for _, n, d in image.iter_files()} | dict(image.iter_components())


def compare(old_name, new_name, digest, font, allow_alignment=False):
    directory = Path('work/emulation_v193')
    old = read(directory / old_name / 'capture_report.json')
    new = read(directory / new_name / 'capture_report.json')
    assert new['ROM_sha256'] == digest and new['cold_boot']
    assert not new['savestate_loaded'] and not new['callback_errors']
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    before = {r['frame']: r for r in old['frames_captured']}
    after = {r['frame']: r for r in new['frames_captured']}
    assert before.keys() == after.keys()
    changes = []
    for frame, record in after.items():
        a = Image.open(before[frame]['path']).convert('RGB')
        b = Image.open(record['path']).convert('RGB')
        assert a.size == b.size == (256, 384)
        assert sha(Path(record['path']).read_bytes()) == record['PNG_sha256']
        if a.tobytes() == b.tobytes():
            continue
        assert allow_alignment and frame == 9200, (new_name, frame)
        differences = [(x, y) for y in range(384) for x in range(256)
                       if a.getpixel((x, y)) != b.getpixel((x, y))]
        assert all(16 <= x < 124 and 296 <= y < 307 for x, y in differences)
        first = dark_text(font, 'Admiral, sailors', b, (10, 292, 252, 317))
        continuation = dark_text(font, 'have scurvy!', b, (10, 308, 252, 340))
        assert first['bounds'][0] == continuation['bounds'][0] == 22
        assert first['ink_pixels'] == 166 and continuation['ink_pixels'] == 126
        assert a.crop((0, 308, 256, 384)).tobytes() == b.crop((0, 308, 256, 384)).tobytes()
        changes.append({'frame': frame, 'first': first, 'continuation': continuation})
    return {'frames': len(after), 'aligned_changes': changes}


def main():
    manifest = read(ROM.with_suffix('.manifest.json'))
    parent = read('out/all_routes_combined_v375_candidate.manifest.json')
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest
    assert manifest['profile'] == 'all-routes-unified-v378'
    assert manifest['base_sha256'] == parent['base_sha256'] == (
        '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe')
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    stack_path = Path('translations/release_stack.json')
    stack = read(stack_path)
    assert manifest['release_stack_sha256'] == sha(stack_path.read_bytes())
    old = stack['profiles']['all-routes-unified-v375']
    new = stack['profiles']['all-routes-unified-v378']
    assert all(new[k] == v for k, v in old.items() if k not in ('note', 'description'))
    assert set(new) - set(old) == {'unguarded_dialogue_alignment'}
    a = files(NdsImage.open('out/all_routes_combined_v375_candidate.nds'))
    b = files(NdsImage.open(ROM))
    assert a.keys() == b.keys()
    assert [n for n in a if a[n] != b[n]] == ['/__arm9__.bin']
    assert b['/__arm9__.bin'] == Path('work/analysis/unguarded_alignment_v377/research_arm9.bin').read_bytes()
    for label in ('Continue', 'New Game', 'Options', 'Grand Race', 'Extras', 'Gallery'):
        assert label.encode() in b['/__arm9__.bin']
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    assert sha(Path('work/clean.nds').read_bytes()) == (
        'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d')
    font = GameAsciiFont.from_arm9(b['/__arm9__.bin'])
    cases = [
        ('unguarded_alignment_v377', 'alignment_fleet_v378', False),
        ('fleet_sort_v375', 'alignment_sort_v378', True),
        ('fleet_new_game_v375', 'alignment_new_game_v378', False),
        ('fleet_equipment_v375', 'alignment_equipment_v378', False),
    ]
    captures = {new_name: compare(old_name, new_name, digest, font, allow)
                for old_name, new_name, allow in cases}
    plaques = read('translations/graphics_completion_campaign_v1.json')[
        'plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {
        'candidate': str(ROM), 'candidate_sha256': digest,
        'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
        'profile': manifest['profile'], 'all470_batches_and_all_V375_stages_retained': True,
        'only_ARM9_changed_all_graphics_files_and_other_components_exact': True,
        'exact_clean_patch_reconstruction': True, 'actual_final_ROM_replays': captures,
        'native_boundary_proof': 'work/analysis/unguarded_alignment_v377/native_proof.json',
        'stored_string_census_proof': 'work/analysis/unguarded_alignment_v377/census_native_proof.json',
        'all18_plaques_incomplete': True, 'status': 'experimental',
        'canonical_promotion': False, 'full_goal_complete': False,
        'hardware_device_verification': False,
    }
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'V378: exact patch, full inherited stack, {sum(c["frames"] for c in captures.values())} final-ROM frames pass.')


if __name__ == '__main__':
    main()
