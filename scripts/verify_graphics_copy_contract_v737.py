"""Exercise the final copy gate against actual late-stage graphics corruption."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.copy_contract import verify_final_graphics_copies
from dk4tool.graphics.plaque_contract import verify_final_plaque_material
from dk4tool.graphics.pxl import PxlImage
from dk4tool.graphics.raw_art_contract import verify_final_raw_art
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import verify_golden_content
from scripts.verify_plaque_final_contract_v687 import Overlay
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/graphics_copy_contract_v737')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
REBUILT = Path('out/all_routes_combined_v712_copy_contract_rebuild.nds')


def archive_pixel(rom, path, index, width, header, x, y, value=None):
    archive = IlnkContainer.parse(rom.read_file(path))
    block = bytearray(archive.blocks[index])
    at, shift = header + (y * width + x) // 2, (x % 2) * 4
    before = (block[at] >> shift) & 15
    value = (before ^ 1) if value is None else value
    assert value != before and 0 <= value < 16
    block[at] = (block[at] & ~(15 << shift)) | value << shift
    archive.blocks[index] = bytes(block)
    return archive.to_bytes()


def main():
    assert not (ROOT / 'proof.json').exists()
    pre = read('work/analysis/village_request_sweep_v735/preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    registry = read('translations/release_stack.json')
    profile = registry['profiles']['all-routes-unified-v712']
    paths = [Path(p) for p in profile['batches']]
    current, baseline, clean = [NdsImage.open(p) for p in
        (ROM, 'out/raphael_natural_v2_accepted_base.nds', 'work/clean.nds')]
    passed = verify_final_graphics_copies(current, baseline, paths, profile)
    assert len(passed['families']) == 3
    assert sum(len(f.get('copies', [f])) for f in passed['families']) == 5
    frame = PxlImage.from_bytes(current.read_file('/_pxl/__frame.pxl'))
    ink = [(x, y) for y in range(32, 40) for x in range(208, 256)
           if frame.indices[y * frame.width + x] == 9]
    first = min(ink)
    last = max(ink)
    changes = []
    for label, (x, y) in (('embedded_first_Pick_Cargo_glyph_pixel_deleted', first),
                          ('embedded_final_Pick_Cargo_glyph_pixel_deleted', last)):
        changes.append((label, {'/GRP/CMMNIMG.DK4': archive_pixel(
            current, '/GRP/CMMNIMG.DK4', 5, 512, 20, x + 256, y, 0)}))
    changes.append(('embedded_gender_cell_pixel_changed', {'/GRP/CMMNIMG.DK4': archive_pixel(
        current, '/GRP/CMMNIMG.DK4', 5, 512, 20, 236, 100)}))
    for filename, index in (('slackimg12', 12), ('slackimg20', 20)):
        image = PxlImage.from_bytes(current.read_file('/_pxl/' + filename + '.pxl'))
        changes.append((filename + '_embedded_pixel_changed', {'/GRP/SLACKIMG.DK4': archive_pixel(
            current, '/GRP/SLACKIMG.DK4', index, image.width, 64, 4, 4)}))
    a = IlnkContainer.parse(current.read_file('/GRP/CMMNIMG.DK4'))
    b = bytearray(a.blocks[4])
    b[20] ^= 1
    a.blocks[4] = bytes(b)
    changes.append(('original_external_palette_changed', {'/GRP/CMMNIMG.DK4': a.to_bytes()}))
    a = IlnkContainer.parse(current.read_file('/GRP/CMMNIMG.DK4'))
    b = bytearray(a.blocks[5])
    b[0] ^= 1
    a.blocks[5] = bytes(b)
    changes.append(('original_pixel_header_changed', {'/GRP/CMMNIMG.DK4': a.to_bytes()}))
    a = IlnkContainer.parse(current.read_file('/GRP/CMMNIMG.DK4'))
    a.blocks[5] = IlnkContainer.parse(baseline.read_file('/GRP/CMMNIMG.DK4')).blocks[5]
    changes.append(('whole_shared_copy_reverted_to_original_Japanese', {'/GRP/CMMNIMG.DK4': a.to_bytes()}))
    obj = current.read_file('/GRP/DSOBJR.DK4')
    for label, at in (('banked_start_prompt_pixel_changed', 5920),
                      ('banked_start_prompt_padding_changed', 5920 + 3 * 1024 + 3 * 8 * 32 + 7 * 4),
                      ('unowned_OBJ_prefix_changed', 0)):
        changed = bytearray(obj)
        changed[at] ^= 1
        changes.append((label, {'/GRP/DSOBJR.DK4': bytes(changed)}))
    image = PxlImage.from_bytes(current.read_file('/_pxl/__frame.pxl'))
    image.indices[first[1] * image.width + first[0]] = 0
    changes.append(('both_loose_and_embedded_glyph_erased', {
        '/_pxl/__frame.pxl': image.to_bytes(),
        '/GRP/CMMNIMG.DK4': archive_pixel(current, '/GRP/CMMNIMG.DK4', 5, 512, 20,
                                           first[0] + 256, first[1], 0)}))
    outcomes = []
    for label, changed in changes:
        candidate = Overlay(current, changed)
        verify_golden_content(baseline, candidate)
        verify_final_plaque_material(candidate, clean, profile)
        verify_final_raw_art(candidate, baseline, clean, paths)
        try:
            verify_final_graphics_copies(candidate, baseline, paths, profile)
        except ValueError as error:
            outcomes.append({'mutation': label, 'previous_final_gates_accept': True,
                             'new_copy_gate_rejects': True, 'error': str(error)})
        else:
            raise AssertionError('Final copy guard accepted corruption: ' + label)
    # Ownership controls: another story file is outside the copy gate. Raw19
    # is explicitly delegated to the adjacent final raw-art gate, which rejects it.
    unrelated = bytearray(current.read_file('/data/SC0.DK4'))
    unrelated[-1] ^= 1
    assert verify_final_graphics_copies(Overlay(current, {'/data/SC0.DK4': bytes(unrelated)}), baseline, paths, profile) == passed
    a = IlnkContainer.parse(current.read_file('/GRP/SLACKIMG.DK4'))
    b = bytearray(a.blocks[19])
    b[0] ^= 1
    a.blocks[19] = bytes(b)
    delegated = Overlay(current, {'/GRP/SLACKIMG.DK4': a.to_bytes()})
    delegated_result = verify_final_graphics_copies(delegated, baseline, paths, profile)
    assert delegated_result['applicable']
    try:
        verify_final_raw_art(delegated, baseline, clean, paths)
    except ValueError:
        pass
    else:
        raise AssertionError('Delegated raw-art corruption was not rejected by its own final gate')
    assert not verify_final_graphics_copies(None, None, [])['applicable']
    manifest = read(REBUILT.with_suffix('.manifest.json'))
    old = read(ROM.with_suffix('.manifest.json'))
    assert sha(REBUILT.read_bytes()) == sha(ROM.read_bytes()) == pre['candidate_sha256']
    assert manifest['checks']['final_registered_graphics_copy_contract_enforced']
    for k, v in old['checks'].items():
        assert manifest['checks'][k] == v
    extra = {'created_at', 'candidate_rom', 'checks', 'final_graphics_copy_contract'}
    assert {k: v for k, v in manifest.items() if k not in extra} == {
        k: v for k, v in old.items() if k not in extra}
    assert manifest['final_graphics_copy_contract'] == passed
    assert len(manifest['batches']) == 470 and len(registry['accepted_layers']) == 114
    assert all(layer.get('baked_into_baseline') for layer in registry['accepted_layers'])
    assert not manifest['required_batches'], 'All114 accepted layers are already baked into the immutable base'
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', {
        'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'final_contract': passed, 'all12_meaningful_corruption_controls': outcomes,
        'unrelated_story_file_outside_contract_control_pass': True,
        'raw19_delegation_and_separate_final_raw_gate_rejection_pass': True,
        'not_applicable_control_pass': True, 'no_corrupted_ROM_written': True,
        'rebuild': str(REBUILT), 'rebuild_sha256': sha(REBUILT.read_bytes()),
        'complete_rebuild_byte_exact_current_V712': True,
        'rebuild_manifest': str(REBUILT.with_suffix('.manifest.json')),
        'rebuild_manifest_sha256': sha(REBUILT.with_suffix('.manifest.json').read_bytes()),
        'all470_batches114_layers_previous_checks_paths_records_and_relocations_exact': True,
        'registered_later_Marker_and_name_gradient_transitions_carried_by_source_target_config_locks': True,
        'prototype_initial_sync_reference_hash_assumption_corrected_to_registered_stage_chain_no_ROM_change': True,
        'prototype_required_batches_count_corrected_all114_accepted_layers_baked_in_base_not_reapplied': True,
        'module_sha256': sha(Path('dk4tool/graphics/copy_contract.py').read_bytes()),
        'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': pre['release_hashes'],
        'original_consumers_native_readability_and_full_goal_not_proven': True,
        'full_goal_complete': False})
    print(f'V737: all{len(outcomes)} late-corruption controls rejected; complete470-batch rebuild exact V712.', flush=True)


if __name__ == '__main__':
    main()
