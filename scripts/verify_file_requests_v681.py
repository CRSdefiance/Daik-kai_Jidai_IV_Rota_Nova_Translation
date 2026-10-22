"""Actual file requests, complete raw returns, all Event Scenes and paired baselines."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.prepare_file_requests_v681 import ROM, ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_resource_dispatch_v668 import validate_caller
from scripts.verify_village_wrap_v608 import read, save


def main():
    pre, contract = read(ROOT / 'preflight.json'), read(ROOT / 'source_contract.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert sha(Path(contract['MMU_source']).read_bytes()) == contract['MMU_source_sha256']
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    assert controls['observer_sha256'] == sha(Path('scripts/observe_file_requests_v681.py').read_bytes())
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    paths = rom.path_map()
    blocks = IlnkContainer.parse(rom.read_file('/GRP/SLACKIMG.DK4')).blocks
    canonical_paths = {p.casefold(): p for p in paths}
    target_by_pc = {t['PC']: t for t in contract['targets']}
    configs = read(ROOT / 'run_cases.json')
    reports, shotmaps, refs, results = {}, {}, [], []
    for case in ('ordinary', 'gallery'):
        pairs = {}
        for mode in ('observed', 'baseline'):
            folder = CAP / f'file_requests_v681_{case}_{mode}'
            rp = folder / 'capture_report.json'
            report = read(rp)
            assert report['frames'] == configs[case]['frames'] and report['cold_boot']
            assert not report['savestate_loaded'] and not report['callback_errors']
            assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
            assert report['scripted_input_schedule'] == read(configs[case]['inputs'])
            run = read(folder / 'run_contract.json')
            assert run['runner_sha256'] == sha(Path('scripts/run_file_requests_v681.py').read_bytes())
            assert run['observer_sha256'] == controls['observer_sha256']
            assert run['inputs_sha256'] == sha(Path(configs[case]['inputs']).read_bytes())
            if case == 'ordinary':
                assert not report.get('battery_save_preloaded')
                assert not any(k.startswith('synthetic_') and v for k, v in report.items())
            else:
                fixture = read(ROOT / 'gallery_save_fixture_manifest.json')
                assert report['battery_save_preloaded']['source_sha256'] == fixture['fixture_save_sha256']
                assert report['earned_unlock_verified'] is False and len(report['synthetic_gallery_fixtures']) == 1
                assert sha(Path(fixture['fixture_save']).read_bytes()) == fixture['fixture_save_sha256']
                assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
            shots = {}
            for row in report['frames_captured']:
                assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
                pixels = Image.open(row['path']).convert('RGB').tobytes()
                if row['frame'] in shots:
                    assert shots[row['frame']] == pixels
                shots[row['frame']] = pixels
            reports[(case, mode)], shotmaps[(case, mode)] = report, {r['frame']: r for r in report['frames_captured']}
            pairs[mode] = shots
            refs.append({'path': str(rp), 'sha256': sha(rp.read_bytes())})
        assert pairs['observed'] == pairs['baseline']
        assert (CAP / f'file_requests_v681_{case}_observed/final_arm9_ram.bin').read_bytes() == (
            CAP / f'file_requests_v681_{case}_baseline/final_arm9_ram.bin').read_bytes()
        meta_path = CAP / f'file_requests_v681_{case}_observed/observer/requests.json'
        meta = read(meta_path)
        assert meta['all_three_opcode_slots_restored_before_free_and_core_file_exact']
        assert meta['observer_sha256'] == controls['observer_sha256'] and not meta['errors'] and not meta['mismatches']
        assert meta['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
        assert len(meta['rows']) == meta['callbacks'] and not meta['unreturned_raw_requests']
        names, callers, opens, entries, returns = Counter(), {}, [], [], []
        for i, row in enumerate(meta['rows']):
            values = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
            target = target_by_pc[row['PC']]
            assert values[1] == target['word'] and values[2] == row['PC'] and values[19] == row['PC'] + 8
            assert not values[20] & 32 and values[4:8] == tuple(row['args']) and values[18] == row['LR']
            assert row['entire_CPU_prefix_and4MiB_WRAM_unchanged_by_observation']
            if row['PC'] == 0x020DED50:
                name = row['filename']
                assert bytes.fromhex(row['filename128_hex']).split(b'\0')[0].decode('ascii') == name
                normalized = '/' + name.replace('\\', '/').lstrip('/')
                path = canonical_paths[normalized.casefold()]
                names[path] += 1
                opens.append({'frame': row['frame'], 'requested_name': name, 'ROM_path': path,
                    'ROM_file_sha256': sha(rom.read_file(path)), 'LR': row['LR']})
                callers[row['LR']] = validate_caller(arm, row['LR'], row['PC'])
                offset = row['LR'] - 0x02000000 - 4
                assert arm[offset:offset + 4] == original[offset:offset + 4]
            elif row['PC'] == 0x0204704C:
                assert row['LR'] == 0x0209EDEC
                assert row['original_raw_read']['entry_index'] == i
                entries.append(row)
            else:
                request = row['original_raw_read']
                assert meta['rows'][request['entry_index']]['original_raw_read'] == request
                payload = Path(row['complete_actual_loaded_payload']).read_bytes()
                assert sha(payload) == row['actual_loaded_payload_sha256']
                assert payload == blocks[request['block']][request['offset']:request['offset'] + request['length']]
                assert row['complete_source_bytes_exact']
                returns.append(row)
        if case == 'ordinary':
            assert len(meta['rows']) == 47 and len(opens) == 39
            assert [e['original_raw_read']['block'] for e in entries] == [14, 15, 16, 17]
            assert [e['original_raw_read']['block'] for e in returns] == [14, 15, 16, 17]
            assert all(e['original_raw_read']['length'] == 14144 for e in returns)
        else:
            assert len(meta['rows']) == len(opens) == 195 and not entries and not returns
            gallery = read(ROOT / 'all_gallery_positions_proof.json')
            assert gallery['candidate_sha256'] == pre['candidate_sha256']
            assert gallery['all164_captions_headings_and_route_descriptions_complete']
            assert gallery['full_source_pixel_comparisons'] == 8060928
            source_photos = {c['source'] for r in gallery['all164_original_Gallery_positions_and_four_wraps'] for c in r['cases']}
            assert len(source_photos) == gallery['distinct_source_images'] == 159
            assert source_photos == {p for p in names if p.startswith('/evstill/')}
            for route in gallery['all164_original_Gallery_positions_and_four_wraps']:
                for photo in route['cases']:
                    frame = next(f for f, s in shotmaps[('gallery', 'observed')].items() if s['path'] == photo['image'])
                    assert any(o['ROM_path'] == photo['source'] and o['frame'] <= frame for o in opens)
        negatives = ('/GRP/CMMNIMG.DK4', '/_pxl/copyright.pxl', '/_pxl/logo.pxl', '/_pxl/ship_eurL.pxl',
                     '/_pxl/startmenu0.pxl', '/_pxl/kakutei.pxl')
        assert all(path not in names for path in negatives)
        results.append({'case': case, 'frames': configs[case]['frames'], 'whole_two_screen_baseline_pairs': len(pairs['observed']),
            'request_log': str(meta_path), 'request_log_sha256': sha(meta_path.read_bytes()),
            'actual_SDK_filename_entries': opens,
            'original_direct_callers': list(callers.values()),
            'original_raw_entries': entries, 'original_raw_full_payload_returns': returns,
            'selected_unresolved_files_not_requested_through_this_interface_in_this_schedule': list(negatives),
            'no_other_interface_or_global_nonuse_claim': True})
    plan = read('work/analysis/gallery_v522/run_plan.json')
    selected = [f for route in plan['routes'] for f in (route['frames'][0], route['frames'][len(route['frames']) // 2], route['frames'][-1])]
    sheet = Image.new('RGB', (1024, 3 * 410), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, frame in enumerate(selected):
        x, y = i % 4 * 256, i // 4 * 410
        draw.text((x + 3, y + 4), f'V678 Event Scenes {frame}', fill='white')
        sheet.paste(Image.open(shotmaps[('gallery', 'observed')][frame]['path']).convert('RGB'), (x, y + 24))
    target = ROOT / 'actual_Event_Scenes_review.png'
    sheet.save(target)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'reports': refs, 'cases': results, 'four_terminal_cold_boots_two_observed_two_baseline': True,
        'all164_current_Gallery_photos_captions_descriptions_and_wraps_verified': True,
        'all159_actual_Gallery_source_photo_filenames_requested_before_display': True,
        'ordinary_four_actual_raw14_to17_payloads_complete_no_IO_stubs': True,
        'all_actual_callback_CPU_prefix_and4MiB_WRAM_unchanged': True,
        'all242_callback_entries234_SDK_filename_requests_and8_raw_entry_return_events': True,
        'gallery_authorized_system_unlock_not_earned_access': True,
        'source_Gallery_verifier': 'scripts/verify_gallery_carousels_v522.py',
        'source_Gallery_verifier_sha256': sha(Path('scripts/verify_gallery_carousels_v522.py').read_bytes()),
        'review_sheet': str(target), 'review_sheet_sha256': sha(target.read_bytes()),
        'actual_legacy_comic_controls_cards_and_other_contexts_still_open': True,
        'ROM_patch_registry_and_all18_plaques22_original_requirements_preserved': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'current_goal_turn_classification': 'progress',
        'full_goal_complete': False})
    print('V681:234 actual SDK requests,4 complete raw returns,all164 Gallery positions and paired screens verified.', flush=True)


if __name__ == '__main__':
    main()
