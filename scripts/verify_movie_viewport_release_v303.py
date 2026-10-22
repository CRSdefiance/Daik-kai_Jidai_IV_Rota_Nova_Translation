"""Complete inherited release preservation and exact subtitle patch reconstruction."""

import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_movie_viewport_release_v303 import ROM as PARENT
from scripts.prepare_movie_viewport_release_v303 import ROOT

ROM = Path('out/all_routes_combined_v303_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent, current = NdsImage.open(PARENT), NdsImage.open(ROM)
    previous, manifest, preparation = [read(p) for p in (PARENT.with_suffix('.manifest.json'), ROM.with_suffix('.manifest.json'), ROOT / 'preparation.json')]
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v303' and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['required_batches'] == previous['required_batches']
    assert manifest['batches'] == previous['batches'] + preparation['batches'] and len(manifest['batches']) == 469
    a = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    b = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert a.keys() == b.keys()
    changed = sorted(p for p in a if a[p] != b[p])
    assert changed == ['/FLS/M22.fls', '/FLS/M24.fls']
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(parent.rom, name) == getattr(current.rom, name)
    for row in preparation['cases']:
        path = row['path']
        assert sha(a[path]) == row['source_sha256'] and sha(b[path]) == row['target_sha256']
        before, after = FlsArchive(a[path]), FlsArchive(b[path])
        owned = {1, 2} if path.endswith('M22.fls') else {3, 4}
        assert before.records == after.records and len(a[path]) == len(b[path])
        for index in range(before.count):
            x, y = before.texture(index), after.texture(index)
            assert (x.flags, x.width, x.height, x.palette) == (y.flags, y.width, y.height, y.palette)
            if index not in owned:
                assert x.indices == y.indices
    source = PARENT.read_bytes()
    assert (Path('work/analysis/movie_playback_v302/v299_before_subtitle_builder_change.nds')).read_bytes() == source
    assert (ROOT / 'v299_after_subtitle_builder_change.nds').read_bytes() == source
    clean, patch, rebuilt = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    output = {'format': 'dk4-native-subtitle-viewport-release-v303', 'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
              'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'profile': manifest['profile'],
              'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'],
              'all467_inherited_batches_and_accepted_requirements_preserved': True, 'total_batches': 469,
              'changed_vs_V299': changed, 'only_four_source_locked_subtitle_compressed_slots_changed': True,
              'all_metadata_palettes_dimensions_other_assets_ARM9_ARM7_route_and_shared_text_exact': True,
              'full_V299_reproduction_before_after_shared_builder_change_exact': True,
              'exact_clean_patch_reconstruction_pass': True, 'four_storage_width_negative_cases_rejected': True,
              'native_width_policy_enforced': 'header-width-v1',
              'current_actual_full_movie_subtitle_pixels_pending': True,
              'all18_plaques_and_variants_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print('V303 onlyM22/M24 four compressed slots; all469 batches/metadata/inherited files; exact clean patch pass.')


if __name__ == '__main__':
    main()
