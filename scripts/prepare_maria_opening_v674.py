"""Pin the omitted Maria introduction and the authorized system-unlock save."""

from copy import deepcopy
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_graphic_paints_v669 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/maria_opening_v674')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'preflight.json').exists()
    source = read('work/analysis/gallery_v521/save_fixture_manifest.json')
    manifest = deepcopy(source)
    manifest.update(production_ROM=str(ROM), production_ROM_sha256=sha(ROM.read_bytes()),
        current_test_scope='Maria original New Game introduction, isolated source system unlock, no earned-unlock claim')
    save(ROOT / 'unlock_manifest.json', manifest)
    donor = Path(manifest['fixture_save'])
    assert sha(donor.read_bytes()) == manifest['fixture_save_sha256']
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    movie = current.read_file('/FLS/M26.fls')
    assert movie == clean.read_file('/FLS/M26.fls') and FlsArchive(movie).count == 2
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    save(ROOT / 'pilot_inputs.json', [{'start': 1601, 'duration': 8, 'buttons': ['START']}])
    save(ROOT / 'preflight.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
            ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
            Path('out/raphael_natural_v2_accepted_base.nds'))},
        'movie': '/FLS/M26.fls', 'movie_sha256': sha(movie), 'two_source_textures_exact_clean': True,
        'donor': str(donor), 'donor_sha256': manifest['fixture_save_sha256'],
        'manifest': str(ROOT / 'unlock_manifest.json'),
        'manifest_sha256': sha((ROOT / 'unlock_manifest.json').read_bytes()),
        'original_manifest': 'work/analysis/gallery_v521/save_fixture_manifest.json',
        'original_manifest_sha256': sha(Path('work/analysis/gallery_v521/save_fixture_manifest.json').read_bytes()),
        'previous_goal_turn_classification': 'progress: V673 actual battle/victory image calls,164 current/retained pairs, exact coordinate-only fixtures and archive',
        'requirement_review_next_action': 'V647 covers only three route introductions. Add actual Maria M26 selection/playback/source composition with authorized original system-unlock save.',
        'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
        'full_goal_complete': False})
    print('V674 missing Maria opening coverage/source M26 and existing unlock-save provenance locked.')


if __name__ == '__main__':
    main()
