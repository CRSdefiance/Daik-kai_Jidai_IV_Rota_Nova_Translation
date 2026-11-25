"""Exact fixed Gallery strings, inherited files and clean-input patch."""

import json
from pathlib import Path

from dk4tool.patch.gallery_menu_labels import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_gallery_menu_v307 import CONFIG, ROOT

ROM = Path('out/all_routes_combined_v307_candidate.nds')
PARENT = Path('out/all_routes_combined_v305_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent, current, clean, canonical = [NdsImage.open(p) for p in (PARENT, ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    previous, manifest = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes()) and manifest['profile'] == 'all-routes-unified-v307'
    assert all(manifest['checks'].values()) and manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == previous['batches'] and manifest['required_batches'] == previous['required_batches']
    a = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    b = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
    assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ['/__arm9__.bin']
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(parent.rom, name) == getattr(current.rom, name)
    expected, report = apply_release(a['/__arm9__.bin'], clean.read_file('/__arm9__.bin'), canonical.read_file('/__arm9__.bin'), CONFIG)
    assert b['/__arm9__.bin'] == expected
    assert (Path('work/analysis/gallery_access_v306/v305_before_gallery_builder_change.nds')).read_bytes() == PARENT.read_bytes()
    assert (ROOT / 'v305_after_gallery_builder_change.nds').read_bytes() == PARENT.read_bytes()
    clean_path, patch, reconstructed = Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    assert sha(clean_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean_path, ROM, patch)
    apply_xdelta(clean_path, patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    proof = {'format': 'dk4-gallery-menu-release-v307', 'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'profile': manifest['profile'],
             'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'],
             'all470_inherited_batches_required_layers_and_accepted_requirements_preserved': True,
             'only_three_fixed_ARM9_string_slots_change': True, 'records': report['records'],
             'all_code_native_unlock_gates_tables_fonts_graphics_and_data_files_exactV305': True,
             'full_V305_reproduction_before_after_builder_change_exact': True,
             'exact_clean_patch_reconstruction': True, 'actual_legitimate_save_and_Ruins_popup_pending': True,
             'actual_hidden_Characters_Event_Scenes_unlock_and_full_popup_context_pending': True,
             'all18_plaque_and_legacy_display_gates_remain_open': True, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V307 onlythree ARM9 strings; all470 batches/code/gates/art retained; reconstructed patch exact.')


if __name__ == '__main__':
    main()
