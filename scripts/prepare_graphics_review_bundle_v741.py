"""Package the unchanged registered V712 candidate for concrete user review."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.build_integrated_release import load_release_stack, resolve_release_batches
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/graphics_review_bundle_v741')
BUNDLE = Path('E:/Rota Nova translations/Review candidates/V741 Graphics review (V712 ROM)')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
DOC = Path('docs/graphics_review_bundle_v741.md')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    assert not BUNDLE.exists()
    prior = read('work/analysis/palette_domains_v740/proof.json')
    for path, digest in prior['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    manifest = read(ROM.with_suffix('.manifest.json'))
    registry = load_release_stack()
    batches = resolve_release_batches(manifest['profile'], [], registry)
    assert manifest['profile'] == 'all-routes-unified-v712'
    assert [Path(p).as_posix() for p in manifest['batches']] == [p.as_posix() for p in batches]
    assert len(batches) == 470 and len(registry['accepted_layers']) == 114
    assert all(row['baked_into_baseline'] for row in registry['accepted_layers'])
    assert manifest['required_batches'] == [] and all(manifest['checks'].values())
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert registry['profiles'][manifest['profile']]['status'] == 'experimental'
    reconstruction = Path('work/analysis/graphics_audit_v721/V712_patch_reconstruction_RESEARCH_ONLY.nds')
    assert reconstruction.read_bytes() == ROM.read_bytes()
    copy_proof = read('work/analysis/graphics_copy_contract_v737/proof.json')
    assert copy_proof['complete_rebuild_byte_exact_current_V712']
    assert copy_proof['all470_batches114_layers_previous_checks_paths_records_and_relocations_exact']
    assert sha(Path(copy_proof['rebuild']).read_bytes()) == manifest['candidate_sha256']
    assert sha(Path(copy_proof['rebuild_manifest']).read_bytes()) == copy_proof['rebuild_manifest_sha256']
    clean_sha = sha(Path('work/clean.nds').read_bytes())
    assert clean_sha == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    for source in (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta')):
        copy(source, BUNDLE / source.name)
    for source in ('translations/release_stack.json', 'translations/graphics_current_work_v1.json',
                   'translations/graphics_current_requirements_v1.json',
                   'work/analysis/graphics_copy_contract_v737/proof.json',
                   'docs/graphics_remaining_work.md', 'docs/context_reconciliation_v736_checkpoint.md',
                   'docs/graphics_copy_contract_v737_checkpoint.md'):
        path = Path(source)
        copy(path, BUNDLE / 'audit_at_packaging' / path.parent.name / path.name)
    copy(Path(copy_proof['rebuild_manifest']), BUNDLE / 'audit_at_packaging' / 'V737_reproduction.manifest.json')
    save(BUNDLE / 'applied_layers.json', {
        'canonical_baseline': registry['canonical_baseline'],
        'accepted_layers_baked_in_baseline': registry['accepted_layers'],
        'experimental_profile': manifest['profile'],
        'experimental_batches_in_build_order': manifest['batches'],
        'changed_internal_files': manifest['changed_paths'],
        'changed_records': manifest['changed_records'],
    })
    remaining = read('translations/graphics_current_work_v1.json')
    assert remaining['completed_scope_count'] == 29 and len(remaining['active_remaining_tasks']) == 5
    text = (
        '# V741 graphics review bundle — existing V712 ROM\n\n'
        'This bundle contains the current experimental combined candidate. V741 is the '
        'packaging checkpoint; the playable ROM remains V712 with exactly the same bytes. '
        'The graphics goal remains open for the unresolved display contexts and final review.\n\n'
        '## Open and test\n\n'
        f'Folder: `{BUNDLE.as_posix()}`\n\n'
        f'1. Open `{ROM.name}` in your emulator from a power-off state. Start without a savestate.\n'
        '2. Check the opening logo, Press START screen and main menu. Advance into New Game.\n'
        '3. Select Lil and check the captain confirmation and first dialogue for complete '
        'leading/trailing letters and readable layout.\n'
        '4. When available, open Assign Sailors and Sailor Info. Check plaque wording, '
        'texture/borders, stat labels/bars and equipment hint paper. Existing saves may be '
        'tested using a separate copy.\n'
        '5. Report the emulator/version, the last successful screen and any defects. '
        'These short checks provide user cold-boot evidence for these contexts; the '
        'remaining original comic/control/card/legacy contexts are listed in the audit snapshot.\n\n'
        '## Exact identities\n\n'
        f'- Candidate: `{ROM.name}`\n'
        f'- Candidate SHA-256: `{manifest["candidate_sha256"]}`\n'
        f'- Registered build base: `{Path(manifest["base_rom"]).name}`\n'
        f'- Build-base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Profile: `{manifest["profile"]}` (experimental)\n'
        '- 114 accepted layers are already baked into the canonical base; 470 registered '
        'experimental batches are applied in manifest order. `applied_layers.json` lists '
        'every layer, changed internal file and changed record.\n'
        f'- {len(manifest["changed_paths"])} changed internal files relative to the registered base.\n\n'
        '## Reconstruct from the exact patch\n\n'
        'The build base and patch input are different: the supplied xdelta patches the '
        'clean Japanese ROM. Supply your exact clean source with SHA-256 '
        f'`{clean_sha}`. With xdelta3 available, run in this folder:\n\n'
        '```powershell\n'
        f'xdelta3 -d -s "path/to/clean.nds" "{ROM.with_suffix(".xdelta").name}" "reconstructed.nds"\n'
        'Get-FileHash -Algorithm SHA256 -LiteralPath "reconstructed.nds"\n'
        '```\n\n'
        f'The reconstructed hash must equal `{manifest["candidate_sha256"]}`. The prior '
        'V721 reconstruction is still byte-exact to this packaged ROM; the unchanged '
        'patch and ROM are verified on copy.\n\n'
        '## Verification carried forward\n\n'
        'The original neighboring manifest records its passing build guards. The V737 '
        'reproduction manifest and proof record the added final graphics-copy gate, its '
        '12 corruption controls and a complete registered rebuild byte-exact to V712. '
        'V736 records current plaque contexts; V740 records the stored palette-domain '
        'inspection. Testing includes targeted emulator runs and declared fixtures, '
        'with their limits retained in the audit.\n\n'
        'Four low-resolution Online bodies remain excluded. Approved brown marks remain '
        'preserved. All 18 original plaque/hint audit objects retain final sign-off pending. '
        'The canonical base and original saves are unchanged.\n')
    DOC.write_text(text, encoding='utf-8')
    copy(DOC, BUNDLE / 'README.md')
    files = {str(p.relative_to(BUNDLE)).replace('\\', '/'): sha(p.read_bytes())
             for p in BUNDLE.rglob('*') if p.is_file()}
    save(BUNDLE / 'bundle_manifest.json', {
        'format': 'dk4-experimental-graphics-review-bundle-v741',
        'files': files, 'ROM_version': 'V712', 'packaging_checkpoint': 'V741',
        'candidate_sha256': manifest['candidate_sha256'], 'patch_clean_input_sha256': clean_sha,
        'canonical_promotion': False, 'full_goal_complete': False})
    for path, digest in files.items():
        assert sha((BUNDLE / path).read_bytes()) == digest
    save(ROOT / 'proof.json', {
        'bundle': str(BUNDLE), 'bundle_manifest_sha256': sha((BUNDLE / 'bundle_manifest.json').read_bytes()),
        'all_packaged_files_hash_verified': files, 'candidate_sha256': manifest['candidate_sha256'],
        'profile': manifest['profile'], 'accepted_baked_layers': 114, 'experimental_batches': 470,
        'source_V721_reconstruction_still_whole_byte_exact': True,
        'source_V737_registered_rebuild_still_same_candidate_hash': True,
        'new_patch_application_or_gameplay_not_claimed': True,
        'release_hashes_unchanged': prior['release_hashes_unchanged'],
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'previous_goal_turn_classification': 'progress: V740 alternate-palette source inspection completed',
        'full_goal_complete': False})
    print(f'Prepared {BUNDLE}: {len(files)} checked files, unchanged V712 ROM.', flush=True)


if __name__ == '__main__':
    main()
