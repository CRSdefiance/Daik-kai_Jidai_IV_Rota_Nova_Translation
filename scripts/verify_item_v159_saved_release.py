"""Audit the saved integrated item candidate and reconstruct its clean-ROM patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_interface_release import SOURCE, TARGET, apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)

PREVIOUS = Path('out/all_routes_combined_v158_candidate.nds')
CANDIDATE = Path('out/all_routes_combined_v159_candidate.nds')
PROFILE = 'all-routes-unified-v159'
CONFIG = 'translations/item_interface_release_v1.json'
PATHS = ['/COMMON/HELP.DK4', '/COMMON/MESFILE.DK4', '/__arm9__.bin', '/_pxl/dividecrewinfo.pxl',
         '/_pxl/personinfo.pxl', '/data/SC0.DK4', '/data/SC1.DK4', '/data/SC2.DK4', '/data/SC3.DK4']


def main():
    clean_path = Path('work/clean.nds')
    if sha(clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Wrong clean patch base')
    clean, previous, saved = [NdsImage.open(p) for p in (clean_path, PREVIOUS, CANDIDATE)]
    if sha(PREVIOUS.read_bytes()) != '9a197373ba448718f3c0d887fdd27f01ce19b75dae11bb22515fed36981a7f5f':
        raise ValueError('Wrong V158 comparison source')
    manifest = json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    old_manifest = json.loads(PREVIOUS.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    baseline_path = Path(manifest['base_rom'])
    if (sha(baseline_path.read_bytes()) != CANONICAL_BASELINE_SHA256
            or manifest['base_sha256'] != CANONICAL_BASELINE_SHA256
            or manifest['candidate_sha256'] != sha(CANDIDATE.read_bytes())
            or manifest['profile'] != PROFILE or manifest['release_stack_sha256'] != sha(RELEASE_STACK_PATH.read_bytes())
            or manifest['changed_paths'] != PATHS or not all(manifest['checks'].values())):
        raise ValueError('Saved item candidate manifest/identity/checks incomplete')
    stack = load_release_stack()
    if (manifest['batches'] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
            or manifest['batches'] != old_manifest['batches'] or len(manifest['batches']) != 435
            or manifest['required_batches'] != [str(p) for p in accepted_batch_paths(stack)]):
        raise ValueError('Saved item candidate omits inherited/accepted layers')
    expected, report = apply_release(previous, clean, CONFIG)
    if sha(previous.read_file('/__arm9__.bin')) != SOURCE or sha(saved.read_file('/__arm9__.bin')) != TARGET:
        raise ValueError('Saved item ARM9 differs from source-locked research')
    if saved.read_file('/__arm9__.bin') != expected:
        raise ValueError('Saved item bytes differ from complete verified transform')
    before, after = rom_files(previous), rom_files(saved)
    differences = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if differences != ['/__arm9__.bin']:
        raise ValueError('Unrelated file/component changed from V158')
    baseline = NdsImage.open(baseline_path)
    baseline_files = rom_files(baseline)
    if sorted(p for p in baseline_files.keys() | after.keys() if baseline_files.get(p) != after.get(p)) != PATHS:
        raise ValueError('Saved canonical path set differs')
    verify_golden_content(baseline, saved)
    for path, stages in old_manifest['relocations'].items():
        for name, stage in stages.items():
            if manifest['relocations'][path][name] != stage:
                raise ValueError('Saved item manifest changes inherited terminal stage: ' + name)
    report['release_config'] = CONFIG
    report['release_config_sha256'] = sha(Path(CONFIG).read_bytes())
    # Manifest JSON stores integer cache-op addresses as string object keys.
    report = json.loads(json.dumps(report))
    if manifest['relocations']['/__arm9__.bin']['item_interface'] != report:
        raise ValueError('Saved item stage metadata differs')
    for path, records in old_manifest['changed_records'].items():
        expected_records = records + (report['changed_records'] if path == '/__arm9__.bin' else [])
        if manifest['changed_records'][path] != expected_records:
            raise ValueError('Saved item changed-record lineage differs')
    patch = CANDIDATE.with_suffix('.xdelta')
    reconstruction = Path('work/analysis/item_v159_patch_reconstruction.nds')
    make_xdelta(clean_path, CANDIDATE, patch)
    apply_xdelta(clean_path, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError('Item patch fails exact clean-ROM reconstruction')
    proof = {'status': 'pass-saved-integrated-v159-item-candidate-and-exact-clean-patch',
             'candidate': str(CANDIDATE), 'candidate_sha256': sha(CANDIDATE.read_bytes()),
             'candidate_arm9_sha256': TARGET, 'canonical_base': str(baseline_path),
             'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
             'previous_rom_sha256': sha(PREVIOUS.read_bytes()), 'previous_arm9_sha256': SOURCE,
             'release_stack_sha256': manifest['release_stack_sha256'], 'profile': PROFILE,
             'profile_status': stack['profiles'][PROFILE]['status'], 'batch_count': len(manifest['batches']),
             'required_accepted_batches': manifest['required_batches'], 'changed_paths_vs_canonical': PATHS,
             'changed_paths_vs_v158': differences, 'all_inherited_terminal_stage_metadata_preserved': True,
             'all_inherited_changed_records_preserved': True, 'exact_research_target_bytes': True,
             'canonical_menu_and_graphic_invariants_pass': True,
             'item_release_report': report, 'clean_patch_base_sha256': sha(clean_path.read_bytes()),
             'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'patch_bytes': patch.stat().st_size,
             'patch_exact_reconstruction_pass': True, 'physical_cold_boot_and_gameplay_verified': False}
    Path('work/analysis/item_v159_saved_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'Pass: V159 {proof["candidate_sha256"]}; 435 batches, inherited stages/records, only ARM9 differs from V158.')
    print(f'Exact clean-ROM patch: {proof["patch_bytes"]} bytes; {proof["patch_sha256"]}. Physical cold boot pending.')


if __name__ == '__main__':
    main()
