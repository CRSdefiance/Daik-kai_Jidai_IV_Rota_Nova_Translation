"""Exact four-record integration, native printf controls and reconstructable patch."""

from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.story_literal_percent import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.format_safety import reject_story_percent_commands, story_percent_findings
from scripts.prepare_story_percent_v685 import ROOT
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v685_candidate.nds')


def main():
    pre, registration = read(ROOT / 'preflight.json'), read(ROOT / 'registration.json')
    old, current = NdsImage.open(pre['source_candidate']), NdsImage.open(ROM)
    canonical, clean = [NdsImage.open(p) for p in (pre['canonical_baseline']['path'], 'work/clean.nds')]
    assert sha(Path(pre['source_candidate']).read_bytes()) == pre['source_candidate_sha256']
    assert sha(Path(pre['canonical_baseline']['path']).read_bytes()) == pre['canonical_baseline']['sha256']
    before = {p: d for _, p, d in old.iter_files()} | dict(old.iter_components())
    after = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert before.keys() == after.keys()
    changed = sorted(p for p in before if before[p] != after[p])
    assert changed == ['/data/SC0.DK4', '/data/SC2.DK4', '/data/SC3.DK4']
    expected, proof = apply_release({p: before[p] for p in changed},
        {p: canonical.read_file(p) for p in changed}, registration['config'])
    assert all(after[p] == expected[p] for p in changed) and proof == registration['four_record_proof']
    registry, manifest = read('translations/release_stack.json'), read(ROM.with_suffix('.manifest.json'))
    prior = read('translations/release_stack.json')
    del prior['profiles'][pre['profile']]
    assert prior == pre['source_registry'] and registry['accepted_layers'] == pre['accepted_layers']
    assert len(registry['accepted_layers']) == 114
    parent_manifest = read(Path(pre['source_candidate']).with_suffix('.manifest.json'))
    assert manifest['profile'] == pre['profile'] and manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == registration['registry_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == parent_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent_manifest['required_batches'] and all(manifest['checks'].values())
    assert manifest['checks']['source_bound_story_printf_contracts_enforced']
    paths = [f'/data/SC{i}.DK4' for i in range(4)]
    source_files = {p: clean.read_file(p) for p in paths}
    findings = {p: story_percent_findings(source_files[p], before[p]) for p in paths}
    assert sum(map(len, findings.values())) == 4
    try:
        reject_story_percent_commands(source_files, {p: before[p] for p in paths})
    except ValueError as error:
        assert 'Introduced or invalid story printf commands' in str(error)
    else:
        raise AssertionError('Old four-hazard candidate unexpectedly passes the final build gate')
    gate = reject_story_percent_commands(source_files, {p: after[p] for p in paths})
    assert gate == manifest['story_percent_contract']
    arm = after['/__arm9__.bin']
    assert arm == before['/__arm9__.bin'] and arm[0xD7720:0xD7790] == clean.read_file('/__arm9__.bin')[0xD7720:0xD7790]
    native = []
    for path, entry in proof.items():
        stage = manifest['relocations'][path]['story_literal_percent_safety']
        assert stage['proof'] == entry and stage['release_config_sha256'] == registration['config_sha256']
        for row in entry['records']:
            original = bytes.fromhex(row['before_hex'])[1:].rstrip(b' ')
            repaired = bytes.fromhex(row['after_hex'])[1:].rstrip(b' ')
            outcomes = []
            for kind, text in (('old', original), ('repaired', repaired)):
                for sentinel in (0x12345678, 0x87654321):
                    u = machine(arm)
                    u.mem_write(0x02462000, b'BOGUS\0')
                    arg = 0x02462000 if b'% s' in text else sentinel
                    u.mem_write(0x02460000, b'\xA5' * 544)
                    u.mem_write(0x02461000, text + b'\0')
                    call(u, 0xD7720, (0x02460020, 0x02461000, arg, sentinel), instruction_limit=400000)
                    actual = bytes(u.mem_read(0x02460020, 512)).split(b'\0')[0]
                    assert u.reg_read(UC_ARM_REG_R0) == len(actual)
                    assert bytes(u.mem_read(0x02460000, 32)) == b'\xA5' * 32
                    assert bytes(u.mem_read(0x02460020 + len(actual), 512 - len(actual))) == b'\0' + b'\xA5' * (511 - len(actual))
                    assert bytes(u.mem_read(0x02461000, len(text) + 1)) == text + b'\0'
                    if kind == 'repaired':
                        assert actual == text and b'BOGUS' not in actual
                    else:
                        assert actual != text
                        assert b'BOGUS' in actual if b'% s' in text else format(arg, 'o').encode() in actual
                    outcomes.append({'kind': kind, 'argument': arg, 'original_native_output_hex': actual.hex(),
                        'complete_native_return_ABI_NUL_input_and_destination_canaries_exact': True})
            native.append({'file': path, 'id': row['id'], 'calls': outcomes,
                           'legacy_corruption_reproduced_and_both_repaired_argument_controls_exact': True})
    graphics = [p for p in before if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(before[p] == after[p] for p in graphics)
    patch, rebuilt = ROM.with_suffix('.xdelta'), ROOT / 'all_routes_combined_v685_PATCH_RECONSTRUCTION.nds'
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    apply_xdelta(Path('work/clean.nds'), patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    save(ROOT / 'static_release_proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()), 'patch_sha256': sha(patch.read_bytes()),
        'registry_sha256': manifest['release_stack_sha256'], 'four_record_proof': proof,
        'source_bound_format_gate_rejects_old_four_and_accepts_current': True,
        'all_graphics_ARM9_other_files_and_components_exact_V678': True,
        'all470_prior_batches114_accepted_layers_and_prior_profiles_unchanged': True,
        'sixteen_complete_original_native_printf_controls': native,
        'exact_clean_patch_reconstruction': True, 'reconstructed_ROM': str(rebuilt),
        'canonical_promoted': False, 'cold_boot_verification_pending': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V685 four exact record repairs, final source-contract guard,16 native printf controls and exact patch reconstruction pass.', flush=True)


if __name__ == '__main__':
    main()
