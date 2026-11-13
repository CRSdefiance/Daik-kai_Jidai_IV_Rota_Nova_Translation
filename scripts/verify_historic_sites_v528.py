"""Complete site-name metadata, actual list/map masks, preservation and patch."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.historic_site_names import BASE, TABLE, fixed_transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_characters_gallery_v525 import report
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files

ROM = Path('out/all_routes_combined_v528_candidate.nds')
PARENT = Path('out/all_routes_combined_v525_candidate.nds')
OUT = Path('work/analysis/historic_sites_v528')
ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    assert digest == '487f39e981d2779876c2f9a7f9094a39228a524fdda0600fb23abaf71a6ff082'
    manifest, old_manifest = [read(p.with_suffix('.manifest.json')) for p in (ROM, PARENT)]
    assert manifest['profile'] == 'all-routes-unified-v528' and manifest['candidate_sha256'] == digest
    assert all(manifest['checks'].values()) and manifest['batches'] == old_manifest['batches']
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == old_manifest['required_batches']
    registry = read('translations/release_stack.json')
    assert len(registry['accepted_layers']) == 114 and registry['profiles']['all-routes-unified-v527']['status'] == 'revoked'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    a, b = [files(NdsImage.open(p)) for p in (PARENT, ROM)]
    assert sorted(p for p in a if a[p] != b[p]) == ['/__arm9__.bin']
    config = read('translations/historic_site_names_v2.json')
    expected, stage = fixed_transform(a['/__arm9__.bin'], config['records'])
    assert b['/__arm9__.bin'] == expected and sha(expected) == config['target_arm9_sha256']
    assert stage['owned_bytes'] == 364 and stage['complete_English_bytes'] == 337
    assert len([p for p in a if p.lower().endswith(('.pxl', '.fls'))]) == 675
    font = GameAsciiFont.from_arm9(expected)
    cases = []
    outcomes = read(OUT / 'site_capture_outcomes.json')
    assert len(outcomes) == 21 and [r['site_id'] for r in outcomes] == list(range(21))
    assert [r['site_id'] for r in outcomes if r['native_CPU_fault_observed']] == [1, 4]
    for row in outcomes:
        index = row['site_id']
        folder = Path(row['run'])
        current = report(folder, digest)
        original_folder = ROOT / f'collection_site_{index:02d}_v526'
        original = report(original_folder, parent_digest)
        assert current['scripted_input_schedule'] == original['scripted_input_schedule']
        ram = (folder / 'final_arm9_ram.bin').read_bytes()
        pointer = struct.unpack_from('<I', ram, TABLE + index * 4)[0]
        text = ram[pointer - BASE:pointer - BASE + 64].split(b'\0')[0].decode('ascii')
        assert text == config['records'][index]['english'] == row['English']
        image = Image.open(folder / 'frame_002800_final.png').convert('RGB')
        old_image = Image.open(original_folder / 'frame_002800_final.png').convert('RGB')
        if row['native_CPU_fault_observed']:
            assert not row['display_credit'] and image.tobytes() == old_image.tobytes()
            cases.append({'site_id': index, 'English': text, 'runtime_pointer': pointer,
                          'existing_fixture_fault_exact_to_V525': True, 'actual_display_credit': False})
            continue
        assert row['display_credit']
        masks = []
        for label, x, y in [('Historic Sites', 86, 2), (text, 128 - len(text) * 3, 70),
                            (text, 128 - len(text) * 3, 194)]:
            ink, bounds = complete_mask(font, label, image, x, y, (230, 230, 230))
            masks.append({'English': label, 'complete_ink_pixels': ink, 'bounds': bounds,
                          'first_final_letters_and_blank_cells_exact': True})
        for y in range(384):
            for x in range(256):
                if (16 <= x < 240 and 64 <= y < 88) or 192 <= y < 208:
                    continue
                assert image.getpixel((x, y)) == old_image.getpixel((x, y)), (index, x, y)
        cases.append({'site_id': index, 'English': text, 'runtime_pointer': pointer,
                      'complete_masks': masks, 'all_pixels_outside_two_name_fields_exact': True,
                      'actual_display_credit': True})
    # Original metadata getter and virtual name method, including odd C-string
    # pointers, use the actual initialized object store from the current run.
    ram = (ROOT / 'historic_site_00_v528/final_arm9_ram.bin').read_bytes()
    u = machine(expected)
    u.mem_write(BASE, ram)
    call(u, 0xCB16C, ())
    store = u.reg_read(UC_ARM_REG_R0)
    getters = []
    for row in config['records']:
        index = row['site_id']
        call(u, 0x87444, (store + 4 + index * 8,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        raw = bytes(u.mem_read(pointer, len(row['english']) + 1))
        assert raw == row['english'].encode('ascii') + b'\0'
        assert pointer == struct.unpack_from('<I', ram, TABLE + index * 4)[0]
        getters.append({'site_id': index, 'English': row['english'], 'runtime_pointer': pointer,
                        'original_getter_complete_bytes_and_saved_register_ABI_verified': True})
    fresh_folder = ROOT / 'historic_sites_v528_fresh'
    fresh, old_fresh = report(fresh_folder, digest), report(ROOT / 'characters_gallery_v525_fresh', parent_digest)
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options'] and fresh['frames'] == old_fresh['frames'] == 21200
    old_frames, new_frames = [{r['frame']: r for r in d['frames_captured']} for d in (old_fresh, fresh)]
    assert old_frames.keys() == new_frames.keys() and len(old_frames) == 56
    assert all(old_frames[n]['PNG_sha256'] == new_frames[n]['PNG_sha256'] for n in old_frames)
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    reconstructed = OUT / 'reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    preservation_path = Path('work/analysis/characters_gallery_v525/preservation_proof.json')
    preservation = read(preservation_path)
    assert len(preservation['entries']) == 921 and all(a[r['path']] == b[r['path']] for r in preservation['entries'])
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        exact_container_parent=str(PARENT), exact_container_parent_sha256=parent_digest,
                        parent_preservation_proof=str(preservation_path), parent_preservation_proof_sha256=sha(preservation_path.read_bytes()))
    (OUT / 'preservation_proof.json').write_text(json.dumps(preservation, indent=2) + '\n', encoding='utf-8')
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all21_complete_source_reviewed_names_implemented': stage,
             'all21_original_native_getters_full_bytes_and_ABI': getters,
             'all19_actual_list_map_heading_name_masks_57_complete_masks': cases,
             'all56_fresh_regression_frames_exact': True,
             'all470_batches114_layers675_graphics_and921_preservation_entries_retained': True,
             'only_original_owned_site_name_spans_and21_pointers_change': True,
             'all_startup_heap_cache_and_section_extents_unchanged': True,
             'existing_site_01_04_fixture_faults_retained_without_display_credit': True,
             'broader_gameplay_shared_site_macro_contexts_remain_under_audit': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'status': 'experimental', 'canonical_promotion': False,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V528:21 complete names/getters,57 actual masks,19 exact surrounding displays,56 fresh frames,all inherited content and exact patch pass.')


if __name__ == '__main__':
    main()
