"""Complete inherited ROM, owned label-only delta and exact patch reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sailing_condition_names import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_sailing_conditions_v309 import CONFIG, ROOT

ROM = Path('out/all_routes_combined_v309_candidate.nds')
PARENT = Path('out/all_routes_combined_v307_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent, current, clean, canonical = [NdsImage.open(p) for p in
                                        (PARENT, ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    previous, manifest = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes()) and manifest['profile'] == 'all-routes-unified-v309'
    assert all(manifest['checks'].values()) and manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == previous['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == previous['required_batches']
    for path, identifiers in previous['changed_records'].items():
        assert set(identifiers) <= set(manifest['changed_records'][path])
    a = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    b = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
    assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ['/__arm9__.bin']
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(parent.rom, name) == getattr(current.rom, name)
    expected, report = apply_release(a['/__arm9__.bin'], clean.read_file('/__arm9__.bin'), canonical.read_file('/__arm9__.bin'), CONFIG)
    assert b['/__arm9__.bin'] == expected == (ROOT / 'research_arm9.bin').read_bytes()
    for name in ('v307_before_builder.nds', 'v307_after_builder.nds'):
        assert (ROOT / name).read_bytes() == PARENT.read_bytes()
    clean_path, patch = Path('work/clean.nds'), ROM.with_suffix('.xdelta')
    assert sha(clean_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean_path, ROM, patch)
    recovered = ROOT / 'exact_patch_reconstruction.nds'
    apply_xdelta(clean_path, patch, recovered)
    assert recovered.read_bytes() == ROM.read_bytes()
    proof = {'format': 'dk4-sailing-condition-names-release-v309', 'candidate': str(ROM),
             'candidate_sha256': sha(ROM.read_bytes()), 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
             'profile': manifest['profile'], 'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'],
             'all470_inherited_batches_required_layers_and_changed_records_preserved': True,
             'all_files_art_routes_COMMON_HELP_ARM7_overlays_and_banner_exactV307': True,
             'only26_label_pointers_owned_appended_text_and_required_boot_extent_fields_change': True,
             'original_condition_strings_table_order_and_selector_code_preserved': True,
             'full_V307_reproduction_before_after_builder_change_exact': True,
             'exact_clean_patch_reconstruction': True, 'records': report['records'],
             'actual_English_reef_warning_pending': True, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ROM_sha256': proof['candidate_sha256'], 'patch_sha256': proof['patch_sha256'],
                      'names': len(report['records']), 'only_changed_component': '/__arm9__.bin'}))


if __name__ == '__main__':
    main()
