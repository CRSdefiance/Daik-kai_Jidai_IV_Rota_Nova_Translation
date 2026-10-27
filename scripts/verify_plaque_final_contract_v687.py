"""Exercise the final material gate with real ROMs and isolated corruptions."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.graphics.plaque_contract import TILE_POINTER, verify_final_plaque_material
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import verify_golden_content
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/plaque_final_contract_v687')
ROM = Path('out/all_routes_combined_v685_candidate.nds')


class Overlay:
    """In-memory test inputs; never write an altered playable ROM."""

    def __init__(self, base, changes):
        self.base, self.changes = base, changes

    def read_file(self, path):
        return self.changes.get(path, self.base.read_file(path))

    def iter_files(self):
        for file_id, path, data in self.base.iter_files():
            yield file_id, path, self.changes.get(path, data)

    def iter_components(self):
        for path, data in self.base.iter_components():
            yield path, self.changes.get(path, data)


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    stack = read('translations/release_stack.json')
    profile = stack['profiles']['all-routes-unified-v685']
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    passed = verify_final_plaque_material(current, clean, profile)
    assert len(passed['static_files']) == 2
    assert sum(len(r['complete_glyph_masks']) for r in passed['static_files']) == 17
    assert passed['equipment_hint']['bytes'] == 1408
    grain = read(profile['source_plaque_grain'])
    mutations = []
    for group in grain['files']:
        path = group['file_path']
        image = PxlImage.from_bytes(current.read_file(path))
        l, t, r, b = group['records'][0]['plaque_box']
        point = next((x, y) for y in range(t + 2, b - 2) for x in range(l + 2, r - 2)
                     if image.indices[y * image.width + x] != 1)
        x, y = point
        old = image.indices[y * image.width + x]
        new = next(i for i, rgb in enumerate(image.palette)
                   if i != old and i != 1 and sum(rgb[:3]) > 320)
        image.indices[y * image.width + x] = new
        mutations.append(('wood_pixel_' + Path(path).stem, {path: image.to_bytes()}))
    group = grain['files'][0]
    path = group['file_path']
    image = PxlImage.from_bytes(current.read_file(path))
    l, t, r, b = group['records'][0]['plaque_box']
    x, y = min(((x, y) for y in range(t, b) for x in range(l, r)
                if image.indices[y * image.width + x] == 1), key=lambda p: (p[0], p[1]))
    image.indices[y * image.width + x] = 2
    mutations.append(('first_letter_ink_deleted', {path: image.to_bytes()}))
    raw = bytearray(current.read_file(path))
    raw[22] ^= 1  # A genuine palette word; preserve the entire indexed plane.
    mutations.append(('palette_word_changed', {path: bytes(raw)}))
    arm = current.read_file('/__arm9__.bin')
    code = MainCodeFile(arm, BASE)
    offset = TILE_POINTER - POOL
    code.sections[3].data[offset + (2 * 44 + 2) * 2] ^= 1
    mutations.append(('equipment_wood_word_changed', {'/__arm9__.bin': bytes(code.save())}))
    code = MainCodeFile(arm, BASE)
    old_code = MainCodeFile(NdsImage.open('out/all_routes_combined_v573_candidate.nds').read_file('/__arm9__.bin'), BASE)
    code.sections[3].data[offset:offset + 1408] = old_code.sections[3].data[offset:offset + 1408]
    mutations.append(('previous_pale_repeat_boundary_reintroduced', {'/__arm9__.bin': bytes(code.save())}))
    results = []
    for name, changes in mutations:
        altered = Overlay(current, changes)
        # Existing final menu/placeholder checks do not establish texture safety.
        verify_golden_content(baseline, altered)
        try:
            verify_final_plaque_material(altered, clean, profile)
        except ValueError as error:
            results.append({'case': name, 'existing_menu_placeholder_gate_passes': True,
                'new_final_material_gate_rejects': True, 'error': str(error),
                'in_memory_overrides_sha256': {p: sha(d) for p, d in changes.items()}})
        else:
            raise AssertionError('Material corruption escaped final check: ' + name)
    assert len(results) == 6
    unrelated = Overlay(current, {'/data/SC3.DK4': clean.read_file('/data/SC3.DK4')})
    assert verify_final_plaque_material(unrelated, clean, profile) == passed
    # Retain earlier profile behavior rather than claiming this gate reviewed it.
    assert not verify_final_plaque_material(clean, clean, {})['applicable']
    historical = verify_final_plaque_material(NdsImage.open('out/all_routes_combined_v555_candidate.nds'),
                                             clean, stack['profiles']['all-routes-unified-v555'])
    assert len(historical['static_files']) == 2 and 'equipment_hint' not in historical
    save(ROOT / 'contract_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'final_contract': passed,
        'six_isolated_material_letter_palette_and_repeat_boundary_corruptions_rejected': results,
        'unrelated_story_change_does_not_trigger_art_guard': True,
        'historical_V555_static_contract_passes_without_later_equipment_requirement': True,
        'profiles_without_these_material_stages_report_not_applicable': True,
        'all_mutations_in_memory_no_altered_ROM_or_fixture_published': True,
        'initial_live_POOL_vs_staged_section_assumption_rejected_and_retained': True,
        'actual_runtime_material_review_pending_not_closed_by_contract': True,
        'gate_sha256': sha(Path('dk4tool/graphics/plaque_contract.py').read_bytes()),
        'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V687: final 17-plaque/1408-byte hint contract passes; six regressions rejected; historical and unrelated controls pass.', flush=True)


if __name__ == '__main__':
    main()
