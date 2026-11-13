"""Verify the integrated ship correction and complete observed screen composites."""
import argparse
import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_plaque_texture import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_source_plaque_grain_v542 import capture_report

ROM = Path('out/all_routes_combined_v557_candidate.nds')
PARENT = Path('out/all_routes_combined_v555_candidate.nds')
ROOT = Path('work/analysis/ship_plaque_release_v557')
CAPTURE = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--static-only', action='store_true')
    args = parser.parse_args()
    current, parent, clean = [NdsImage.open(p) for p in (ROM, PARENT, Path('work/clean.nds'))]
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    stack = read('translations/release_stack.json')
    assert manifest['profile'] == 'all-routes-unified-v557' and manifest['candidate_sha256'] == digest
    assert manifest['base_sha256'] == stack['canonical_baseline']['sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert len(stack['accepted_layers']) == 114
    old = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new = {p: d for _, p, d in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys()
    assert [p for p in old if old[p] != new[p]] == ['/_pxl/shipinfo.pxl']
    path, expected, stage = apply_release(parent, clean, 'translations/ship_plaque_texture_v1.json')
    assert expected == new[path]
    a, b = PxlImage.from_bytes(old[path]), PxlImage.from_bytes(new[path])
    assert a.source[:a.pixels_offset] == b.source[:b.pixels_offset]
    config = read('translations/ship_plaque_texture_v1.json')
    font = GameAsciiFont.from_arm9(new['/__arm9__.bin'])
    masks = []
    for row in config['records']:
        l, t, r, bottom = row['draw_box']
        tx, ty = l + (r - l - len(row['english']) * 5) // 2, t + (bottom - t - 11) // 2
        mask = {(tx + n * 5 + x, ty + y) for n, ch in enumerate(row['english'])
                for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        assert mask == {tuple(p) for p in row['expected_ink']}
        assert all(b.indices[y * b.width + x] == 1 for x, y in mask)
        masks.append({'id': row['id'], 'english': row['english'], 'complete_font_points': len(mask)})
    assert len(masks) == 11
    prior_proof = read('work/analysis/local_plaque_release_v555/release_proof.json')
    assert prior_proof['candidate_sha256'] == parent_digest
    preservation = read('work/analysis/plaque_borders_v546/preservation_proof.json')
    assert len(preservation['entries']) == 921
    assert all(old[e['path']] == new[e['path']] for e in preservation['entries'] if e['path'] != path)
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), ROOT / 'reconstructed.nds')
    assert (ROOT / 'reconstructed.nds').read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'only_ship_atlas_changes_from_V555': True, 'all_code_and_other_translations_exact_V555': True,
             'all470_batches114_layers921_preservation_entries_retained': True,
             'stage': stage, 'independent_complete_font_masks': masks,
             'experimental': True, 'canonical_promoted': False, 'full_goal_complete': False}
    if args.static_only:
        (ROOT / 'static_release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
        print('V557 static:11 complete masks; only ship atlas changed; inherited stack and exact patch pass.')
        return
    control = capture_report(CAPTURE / 'ship_texture_v557_control_r2', parent_digest)
    actual = capture_report(CAPTURE / 'ship_texture_v557_actual_r2', digest)
    assert actual['scripted_input_schedule'] == control['scripted_input_schedule']
    assert actual['core_options'] == control['core_options']
    assert actual['battery_save_preloaded']['source_sha256'] == control['battery_save_preloaded']['source_sha256']
    source_save = Path(actual['battery_save_preloaded']['source'])
    assert sha(source_save.read_bytes()) == actual['battery_save_preloaded']['source_sha256']
    old_shots, new_shots = [{s['frame']: s for s in report['frames_captured']} for report in (control, actual)]
    cargo_path = '/_pxl/itemtrade16.pxl'
    cargo_data = new[cargo_path]
    assert cargo_data == clean.read_file(cargo_path)
    cargo = PxlImage.from_bytes(cargo_data)
    # Full observed row correspondence: row7 repeats at the8-row boundary;
    # destination rows8..15 use source rows7..14. Producer cause is untraced.
    cargo_rows = list(range(8)) + list(range(7, 15))
    cargo_pixels = {(dx+x, 64+y): native5(cargo.palette[cargo.indices[(1440+sy)*16+x]])
                    for dx in (166, 182) for y, sy in enumerate(cargo_rows) for x in range(16)}
    assert len(cargo_pixels) == 512
    raw = (CAPTURE / 'ship_texture_v557_actual_r2/frame_003700_arm9_ram.bin').read_bytes()
    u = machine(new['/__arm9__.bin'])
    u.mem_write(0x02000000, raw)
    cargo_bindings = []
    for view in (0x0218E164, 0x0218E1D8):
        fields = struct.unpack_from('<12I', raw, view - 0x02000000)
        assert fields[3] == 0x02313BB4 and fields[7:12] == (0, 1440, 0, 16, 16)
        executed = call(u, 0xD4170, (view,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(pointer, len(cargo_data))) == cargo_data
        assert pointer == raw.find(cargo_data) + 0x02000000
        assert 0x020DED50 not in executed and 0x020DEBDC not in executed
        cargo_bindings.append({'view': view, 'owner': fields[3], 'resident_pointer': pointer,
                               'full_original_resource_resolution_without_bridge': True})
    changed_colours = {(x, y) for y in range(192) for x in range(256)
                       if native5(a.palette[a.indices[y*256+x]]) != native5(b.palette[b.indices[y*256+x]])}
    cases = []
    for frame in (3700, 3800, 3900, 4600, 4700, 4800):
        before, after = [Image.open(shots[frame]['path']).convert('RGB') for shots in (old_shots, new_shots)]
        assert before.size == after.size == (256, 384)
        frame_raw = (CAPTURE / f'ship_texture_v557_actual_r2/frame_{frame:06d}_arm9_ram.bin').read_bytes()
        assert frame_raw.find(cargo_data) >= 0
        for binding in cargo_bindings:
            fields = struct.unpack_from('<12I', frame_raw, binding['view'] - 0x02000000)
            assert fields[3] == binding['owner'] and fields[7:12] == (0, 1440, 0, 16, 16)
        assert all(native5(before.getpixel(p)) == c == native5(after.getpixel(p))
                   for p, c in cargo_pixels.items()), (frame, 'complete cargo source pixels')
        mismatches, new_background, visible_overlays = [], 0, 0
        for y in range(384):
            for x in range(256):
                observed = native5(before.getpixel((x, y)))
                expected_colour = observed
                if (x, y) in changed_colours:
                    if observed == native5(a.palette[a.indices[y*256+x]]):
                        expected_colour = native5(b.palette[b.indices[y*256+x]])
                        new_background += 1
                    else:
                        visible_overlays += 1
                if (x, y) in cargo_pixels:
                    expected_colour = cargo_pixels[x, y]
                if native5(after.getpixel((x, y))) != expected_colour:
                    mismatches.append([x, y])
        assert not mismatches, (frame, len(mismatches), mismatches[:12])
        ink = native5(b.palette[1])
        for row in config['records']:
            assert all(native5(after.getpixel(tuple(p))) == ink for p in row['expected_ink']), (frame, row['id'])
        cases.append({'frame': frame, 'complete_both_screen_pixels_exact': 98304,
                      'visible_revised_background_points': new_background,
                      'occluding_foreground_points_preserved': visible_overlays,
                      'all11_complete_English_masks_visible': True, 'no_excluded_screen_pixels': True})
    # Back returns to the same Info menu as the unchanged control.
    assert new_shots[4200]['PNG_sha256'] == old_shots[4200]['PNG_sha256']
    fresh = capture_report(CAPTURE / 'ship_texture_v557_fresh', digest)
    old_fresh = capture_report(CAPTURE / 'local_plaque_v555_fresh', parent_digest)
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options']
    assert [s['PNG_sha256'] for s in fresh['frames_captured']] == [s['PNG_sha256'] for s in old_fresh['frames_captured']]
    assert len(fresh['frames_captured']) == 57
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(e['fully_completed'] is False for e in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof.update(actual_ship_screen_cases=cases, observed_complete_composite_pixels=589824,
                 actual_original_cargo_bindings=cargo_bindings, cargo_source_path=cargo_path,
                 complete_cargo_source_pixels_per_frame=512, cargo_observed_source_rows=cargo_rows,
                 cargo_row_repeat_producer_cause_not_claimed=True,
                 control_foreground_classification_is_empirical_not_icon_consumer_proof=True,
                 original_icon_sources_and_unobserved_ship_states_not_claimed=True,
                 Back_and_reentry_verified=True, unique_unchanged_startup_frames=56,
                 source_save_unchanged=True, all18_plaques_remain_incomplete=True,
                 all22_requirements_retained=True, full_route_or_hardware_verified=False)
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V557:6 complete Ships composites,66 full labels,Back/re-entry,56 unchanged startup frames and exact patch pass.')


if __name__ == '__main__':
    main()
