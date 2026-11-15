"""One owned genre slot, exact inherited files and clean-input patch."""

import json
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_genre_card_v305 import BATCH, ROOT
from scripts.prepare_genre_card_v305 import ROM as PARENT

ROM = Path('out/all_routes_combined_v305_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent, current = NdsImage.open(PARENT), NdsImage.open(ROM)
    previous, manifest, prep = [read(p) for p in (PARENT.with_suffix('.manifest.json'), ROM.with_suffix('.manifest.json'), ROOT / 'preparation.json')]
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v305' and all(manifest['checks'].values())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['required_batches'] == previous['required_batches']
    assert manifest['batches'] == previous['batches'] + [str(BATCH)] and len(manifest['batches']) == 470
    a = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    b = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
    assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ['/FLS/logo.fls']
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(parent.rom, name) == getattr(current.rom, name)
    source, target = a['/FLS/logo.fls'], b['/FLS/logo.fls']
    assert sha(source) == prep['source_sha256'] and sha(target) == prep['target_sha256']
    before, after = FlsArchive(source), FlsArchive(target)
    assert len(source) == len(target) and before.records == after.records
    start, count = before.data_offset + before.records[3][4], before.records[3][5]
    assert all(x == y or start <= at < start + count for at, (x, y) in enumerate(zip(source, target, strict=True)))
    for index in range(before.count):
        x, y = before.texture(index), after.texture(index)
        assert (x.flags, x.width, x.height, x.palette) == (y.flags, y.width, y.height, y.palette)
        if index != 3:
            assert x.indices == y.indices
    assert (Path('work/analysis/root_fls_v304/v303_before_height_builder_change.nds')).read_bytes() == PARENT.read_bytes()
    assert (ROOT / 'v303_after_height_builder_change.nds').read_bytes() == PARENT.read_bytes()
    clean, patch, rebuilt = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    proof = {'format': 'dk4-genre-native-view-release-v305', 'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'profile': manifest['profile'],
             'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'],
             'all469_inherited_batches_and_accepted_requirements_retained': True, 'total_batches': 470,
             'changed_vs_V303': ['/FLS/logo.fls'], 'only_one_compressed_pixel_slot_changed': True,
             'all_metadata_palette_dimensions_other_logo_assets_code_routes_shared_text_and_other_graphics_exact': True,
             'before_after_full_V303_reproduction_exact': True, 'exact_clean_patch_reconstruction': True,
             'native_size_policy': 'header-size-v2', 'native_view': [256, 192], 'stored_view': [256, 256],
             'original_Japanese_ink_bounds': prep['original_Japanese_ink_bounds'],
             'old_English_ink_bounds': prep['old_English_ink_bounds'], 'new_English_ink_bounds': prep['new_English_ink_bounds'],
             'two_native_size_negatives_rejected': True, 'actual_startup_pixels_pending': True,
             'all18_plaques_and_legacy_display_gates_remain_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V305 onlyone logo slot; all470 batches; metadata and other files exact; reconstructed patch exact.')


if __name__ == '__main__':
    main()
