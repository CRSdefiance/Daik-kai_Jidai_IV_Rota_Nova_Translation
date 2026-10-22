"""Exact footer release delta and reconstructable inherited ROM."""

import json
from pathlib import Path

from dk4tool.patch.footer_measurement import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_footer_v318 import CONFIG, ROOT

ROM = Path('out/all_routes_combined_v318_candidate.nds')
PARENT = Path('out/all_routes_combined_v316_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent, current, clean, canonical = [NdsImage.open(p) for p in
                                        (PARENT, ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    a = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    b = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
    assert a.keys() == b.keys() and [p for p in a if a[p] != b[p]] == ['/__arm9__.bin']
    target, plan = apply_release(a['/__arm9__.bin'], clean.read_file('/__arm9__.bin'), canonical.read_file('/__arm9__.bin'), CONFIG)
    assert target == b['/__arm9__.bin'] == (ROOT / 'research_arm9.bin').read_bytes()
    old, new = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
    assert new['candidate_sha256'] == sha(ROM.read_bytes()) and new['profile'] == 'all-routes-unified-v318'
    assert new['batches'] == old['batches'] and len(new['batches']) == 470
    assert new['required_batches'] == old['required_batches'] and all(new['checks'].values())
    assert new['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    for path, records in old['changed_records'].items():
        assert set(records) <= set(new['changed_records'][path])
    for path in ('v316_before_builder.nds', 'v316_after_builder.nds'):
        assert (ROOT / path).read_bytes() == PARENT.read_bytes()
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(parent.rom, name) == getattr(current.rom, name)
    patch, restored = ROM.with_suffix('.xdelta'), ROOT / 'exact_patch_reconstruction.nds'
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    apply_xdelta(Path('work/clean.nds'), patch, restored)
    assert restored.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
             'canonical_base': new['base_rom'], 'canonical_sha256': new['base_sha256'], 'profile': new['profile'],
             'all470_inherited_batches_and_accepted_requirements_retained': True,
             'all_data_art_routes_COMMON_HELP_ARM7_overlays_banner_exactV316': True,
             'only_two_footer_width_instructions_and16_byte_Stop_slot_change': True,
             'all_other_code_pointers_staged_helpers_arenas_and_fonts_preserved': True,
             'full_V316_before_after_builder_reproduction_exact': True, 'exact_clean_patch_reconstruction': True,
             'change': plan, 'actual_complete_sailing_footer_pending': True,
             'actual_Auto_Move_Stop_context_still_pending': True, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: proof[key] for key in ('candidate_sha256', 'patch_sha256', 'profile')}))


if __name__ == '__main__':
    main()
