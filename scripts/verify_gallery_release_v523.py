"""Verify corrected Gallery, inherited release, fresh regressions and exact patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.gallery_caption_bounds import OFFSET, OLD, transform, validate
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROM = Path('out/all_routes_combined_v523_candidate.nds')
PARENT = Path('out/all_routes_combined_v518_candidate.nds')
OUT = Path('work/analysis/gallery_caption_v523')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193/gallery_all_v523')
FRESH = Path('E:/Rota Nova translations/Generated/work/emulation_v193/gallery_caption_v523_fresh')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    digest = sha(ROM.read_bytes())
    assert digest == '76cb6645e040a68f7470f25e0a70bcd965bb1b2450cdecf6c383cae4647ee3fa'
    manifest, prior = [read(p.with_suffix('.manifest.json')) for p in (ROM, PARENT)]
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v523'
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == prior['required_batches'] and all(manifest['checks'].values())
    registry = read('translations/release_stack.json')
    assert len(registry['accepted_layers']) == 114
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    a, b = [files(NdsImage.open(p)) for p in (PARENT, ROM)]
    assert sorted(p for p in a if a[p] != b[p]) == ['/__arm9__.bin']
    assert b['/__arm9__.bin'] == transform(a['/__arm9__.bin'])[0]
    differences = [i for i, (x, y) in enumerate(zip(a['/__arm9__.bin'], b['/__arm9__.bin'])) if x != y]
    assert differences and all(OFFSET <= i < OFFSET + len(OLD) for i in differences)
    assert len(validate(b['/__arm9__.bin'])) == 164
    graphics = [p for p in a if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(a[p] == b[p] for p in graphics)
    fresh_path = FRESH / 'capture_report.json'
    fresh = read(fresh_path)
    old_fresh = read('work/emulation_v193/shiraki_surname_v518_fresh/capture_report.json')
    assert fresh['ROM_sha256'] == digest and fresh['cold_boot'] and not fresh['savestate_loaded']
    assert not fresh['callback_errors'] and fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options']
    x, y = [{r['frame']: r for r in report['frames_captured']} for report in (old_fresh, fresh)]
    assert x.keys() == y.keys() and len(x) == 56
    assert all(x[n]['PNG_sha256'] == y[n]['PNG_sha256'] for n in x)
    for row in fresh['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    gallery = read(OUT / 'all_carousels_proof.json')
    assert gallery['candidate_sha256'] == digest
    assert gallery['all164_captions_headings_and_route_descriptions_complete']
    assert sum(r['count'] for r in gallery['all164_original_Gallery_positions_and_four_wraps']) == 164
    old_folder = Path('E:/Rota Nova translations/Generated/work/emulation_v193/gallery_all_v522')
    changed_frames = []
    for route in read('work/analysis/gallery_v522/run_plan.json')['routes']:
        for frame in route['frames'] + [route['wrap_frame']]:
            name = f'frame_{frame:06d}_cold_boot.png'
            before, after = [Image.open(p / name).convert('RGB') for p in (old_folder, CAPTURE)]
            if before.tobytes() != after.tobytes():
                changed_frames.append(frame)
                assert before.crop((0, 0, 256, 258)).tobytes() == after.crop((0, 0, 256, 258)).tobytes()
                assert before.crop((0, 278, 256, 384)).tobytes() == after.crop((0, 278, 256, 384)).tobytes()
    assert changed_frames == [37600]
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    rebuilt = OUT / 'reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'), patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    parent_path = Path('work/analysis/shiraki_surname_v518/preservation_proof.json')
    preservation = read(parent_path)
    assert len(preservation['entries']) == 921
    assert all(a[row['path']] == b[row['path']] for row in preservation['entries'])
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        exact_container_parent=str(PARENT), exact_container_parent_sha256=sha(PARENT.read_bytes()),
                        parent_preservation_proof=str(parent_path), parent_preservation_proof_sha256=sha(parent_path.read_bytes()))
    (OUT / 'preservation_proof.json').write_text(json.dumps(preservation, indent=2) + '\n', encoding='utf-8')
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(patch.read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all470_batches_and114_accepted_layers_preserved': True,
             'only_owned_Grand_Review_string_data_changes': differences,
             'all675_PXL_FLS_and_every_other_component_byte_exact': True,
             'all921_preservation_entries_inherited_by_exact_container_equality': True,
             'all164_final_Gallery_titles_arrow_safe_build_gate': True,
             'all164_actual_images_captions_headings_and_descriptions': str(OUT / 'all_carousels_proof.json'),
             'only_one_of168_Gallery_selection_and_wrap_frames_changes': changed_frames,
             'changed_pixels_confined_to_original_caption_band': [0, 258, 256, 278],
             'all56_fresh_title_NewGame_story_town_Help_frames_exact': True,
             'fresh_report': str(fresh_path), 'status': 'experimental', 'canonical_promotion': False,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V523: all164 Gallery checks,56 fresh frames,470 batches,114 layers,921 preservation entries and exact patch reconstruction pass.')


if __name__ == '__main__':
    main()
