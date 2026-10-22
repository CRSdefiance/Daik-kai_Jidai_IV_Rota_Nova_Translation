"""Prove exact integrated-caption delta, inherited stack and patch reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sea_inspect_caption import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_sea_inspect_v322 import CONFIG, ROOT

ROM = Path('out/all_routes_combined_v322_candidate.nds')
PARENT = Path('out/all_routes_combined_v318_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parent, current, clean, canonical = [NdsImage.open(p) for p in (
        PARENT, ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    before = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
    after = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys()
    assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
    target, plan = apply_release(before['/__arm9__.bin'], clean.read_file('/__arm9__.bin'),
                                 canonical.read_file('/__arm9__.bin'), CONFIG)
    assert target == after['/__arm9__.bin'] == (ROOT / 'research_arm9.bin').read_bytes()
    assert (ROOT / 'v318_reproduction.nds').read_bytes() == PARENT.read_bytes()
    old, new = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
    assert new['candidate_sha256'] == sha(ROM.read_bytes())
    assert new['profile'] == 'all-routes-unified-v322' and all(new['checks'].values())
    assert old['batches'] == new['batches'] and len(new['batches']) == 470
    assert old['required_batches'] == new['required_batches']
    assert new['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    for path, records in old['changed_records'].items():
        assert set(records) <= set(new['changed_records'][path])
    for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                 'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
        assert getattr(parent.rom, name) == getattr(current.rom, name)
    patch = ROM.with_suffix('.xdelta')
    reconstructed = ROOT / 'exact_patch_reconstruction.nds'
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    apply_xdelta(Path('work/clean.nds'), patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
             'canonical_base': new['base_rom'], 'canonical_sha256': new['base_sha256'],
             'profile': new['profile'], 'all470_inherited_batches_retained': True,
             'accepted_requirements_and_all_inherited_changed_records_retained': True,
             'full_V318_reproduction_byte_exact': True,
             'only_original8_byte_caption_slot_changes': True,
             'all_graphics_routes_COMMON_HELP_code_fonts_pointers_and_other_components_preserved': True,
             'exact_clean_patch_reconstruction': True, 'change': plan,
             'actual_display_verification_pending': True, 'goal_complete': False,
             'experimental_user_acceptance_pending': True}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    parent_report = read('work/emulation_v193/footer_measurement_v318/capture_report.json')
    assert max(row['start'] for row in parent_report['scripted_input_schedule']) == 30801
    inputs = [row for row in parent_report['scripted_input_schedule'] if row['start'] < 30801]
    inputs.append({'start': 30801, 'duration': 8, 'buttons': ['Y']})
    (ROOT / 'cold_boot_inputs.json').write_text(json.dumps(inputs, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: proof[k] for k in ('candidate_sha256', 'patch_sha256', 'profile')}))


if __name__ == '__main__':
    main()
