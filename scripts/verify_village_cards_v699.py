"""Verify full actual card displays from declared original-parent argument fixtures."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.run_village_cards_v699 import BASE, CAP, CARDS, FRAMES, ROM, ROOT, plan
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_raw_portrait_tail_v689 import pictures
from scripts.verify_village_wrap_v608 import read, save


def checked(row):
    value = Path(row['path']).read_bytes()
    assert sha(value) == row['sha256']
    return value


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, field in ((Path('scripts/run_village_cards_v699.py'), 'producer_sha256'),
                        (ROOT / 'source_contract.json', 'source_contract_sha256'),
                        (ROOT / 'inputs.json', 'inputs_sha256'), (Path(pre['manifest']), 'manifest_sha256'),
                        (Path(pre['donor']), 'donor_sha256')):
        assert sha(path.read_bytes()) == pre[field]
    assert sha(CORE.read_bytes()) == CORE_SHA
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 5 and len(controls['read_policy_cases']) == 8
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    historical_path = Path('out/all_routes_combined_v414_candidate.nds')
    assert sha(historical_path.read_bytes()) == '699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c'
    historical = NdsImage.open(historical_path)
    reports, shots, memories, entries, planes, plan_cases = [], {}, {}, {}, [], []
    for card in (*CARDS, None):
        name = 'disabled' if card is None else f'card{card}'
        folder = CAP / ('village_cards_v699_final_' + name)
        rp, fp = folder / 'capture_report.json', folder / 'fixture/fixture.json'
        report, fixture, contract = read(rp), read(fp), read(folder / 'run_contract.json')
        assert report['frames'] == 4000 and report['cold_boot'] and not report['savestate_loaded']
        assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
        assert not report['callback_errors'] and not report['hardware_device_verification']
        assert report['scripted_input_schedule'] == read(ROOT / 'inputs.json')
        assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        receipt = report['isolated_event_request_fixture']
        assert receipt['enabled'] == (card is not None) and receipt['receipt_sha256'] == sha(fp.read_bytes())
        assert not receipt['ordinary_scene_reachability_or_earned_village_trigger_verified']
        assert bool(report.get('synthetic_original_event_image_argument_fixture')) == (card is not None)
        assert fixture['producer_sha256'] == contract['producer_sha256'] == pre['producer_sha256']
        assert contract['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
        assert fixture['host_slot_restored_core_file_exact'] and not fixture['errors'] and not fixture['mismatches']
        assert len(fixture['rows']) == fixture['callbacks'] == 1 and fixture['applied'] == (card is not None)
        row = fixture['rows'][0]
        assert row['frame'] == 3749 and row['only_R1_changed_full_WRAM_DTCM_ITCM_and_other_CPU_bytes_exact']
        files = {k: checked(v) for k, v in row['files'].items()}
        cpu, raw, dtcm = files['CPU_before'], files['WRAM'], files['DTCM']
        expected, applied = plan(cpu, raw, dtcm, card or 168, enabled=card is not None)
        assert files['CPU_after'] == expected and applied == (card is not None)
        assert len(files['WRAM']) == 0x400000 and len(files['ITCM']) == 0x8000 and len(files['DTCM']) == 0x4000
        values = struct.unpack('<32I', cpu)
        assert values[5] == 84 and values[4] == 0x02276F88 and values[18] == 0x02029FB8
        if card is not None:
            assert [i for i, (a, b) in enumerate(zip(cpu, expected, strict=True)) if a != b] == [20]
            assert struct.unpack_from('<I', expected, 20)[0] == card
        entries[name], shots[name], memories[name] = files, pictures(report), {}
        assert set(shots[name]) == set(FRAMES)
        for snap in report['read_only_capture_RAM_snapshots']:
            value = checked(snap)
            if snap['frame'] in memories[name]:
                assert memories[name][snap['frame']] == value
            memories[name][snap['frame']] = value
        assert set(memories[name]) == set(FRAMES)
        reports.append({'case': name, 'report': str(rp), 'report_sha256': sha(rp.read_bytes()),
                        'receipt': str(fp), 'receipt_sha256': sha(fp.read_bytes())})
        image_index = card if card is not None else 84
        path = f'/evstill/evstill{image_index:03d}.pxl'
        source = current.read_file(path)
        if card is not None:
            assert source == historical.read_file(path)
        pxl = PxlImage.from_bytes(source)
        assert (pxl.width, pxl.height) == (256, 192)
        pixels = [native5(p) for p in pxl.render().get_flattened_data()]
        for frame in (3900, 4000):
            upper = shots[name][frame].crop((0, 0, 256, 192))
            actual = [native5(p) for p in upper.get_flattened_data()]
            assert actual == pixels, (name, frame)
            raw = memories[name][frame]
            at = raw.find(source)
            assert at >= 0 and raw.find(source, at + 1) == -1
            planes.append({'case': name, 'image': path, 'frame': frame, 'all49152_native5_pixels_exact': True,
                           'whole_resident_PXL_address': BASE + at, 'source_sha256': sha(source)})
    ordinary = shots['disabled']
    before = [f for f in FRAMES if f <= 3700]
    assert len(before) == 12
    for card in CARDS:
        name = f'card{card}'
        assert all(shots[name][f].tobytes() == ordinary[f].tobytes() for f in before)
        assert all(memories[name][f] == memories['disabled'][f] for f in before)
        assert all(entries[name][tag] == entries['disabled'][tag] for tag in ('CPU_before', 'WRAM', 'DTCM', 'ITCM'))
        assert all(shots[name][f].crop((0, 192, 256, 384)).tobytes() == ordinary[f].crop((0, 192, 256, 384)).tobytes() for f in (3900, 4000))
    sample = entries['card168']
    for card in CARDS:
        cpu, raw, dtcm = sample['CPU_before'], sample['WRAM'], sample['DTCM']
        for name, enabled, already, original_id in (
                ('selected', True, False, 84), ('disabled', False, False, 84),
                ('already_applied', True, True, 84), ('other_image', True, False, 83)):
            supplied = bytearray(cpu)
            struct.pack_into('<I', supplied, 20, original_id)
            after, applied = plan(bytes(supplied), raw, dtcm, card, enabled=enabled, already=already)
            assert applied == (name == 'selected')
            if not applied:
                assert after == supplied
            plan_cases.append({'card': card, 'case': name, 'applied': applied})
    for name, offset, xor in (('wrong_word', 4, 1), ('wrong_PC', 8, 4),
                              ('wrong_scene', 16, 4), ('wrong_LR', 72, 4), ('bad_options_pointer', 24, 0x10000000)):
        supplied = bytearray(sample['CPU_before'])
        struct.pack_into('<I', supplied, offset, struct.unpack_from('<I', supplied, offset)[0] ^ xor)
        try:
            plan(bytes(supplied), sample['WRAM'], sample['DTCM'], 168)
        except ValueError:
            pass
        else:
            raise AssertionError(name)
        plan_cases.append({'case': name, 'invalid_input_rejected': True})
    sheet = Image.new('RGB', (1024, 840), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, card in enumerate(CARDS):
        x, y = i % 4 * 256, i // 4 * 420
        draw.text((x + 5, y + 5), f'Image {card}: isolated request fixture', fill='white')
        sheet.paste(shots[f'card{card}'][3900], (x, y + 24))
    sp = ROOT / 'eight_actual_village_card_fixture_displays.png'
    sheet.save(sp)
    source_sheet = Image.new('RGB', (1024, 864), '#263238')
    sd = ImageDraw.Draw(source_sheet)
    for i, card in enumerate(CARDS):
        x, y = i % 2 * 512, i // 2 * 216
        sd.text((x + 5, y + 4), f'{card} original Japanese | actual English fixture', fill='white')
        source_sheet.paste(PxlImage.from_bytes(clean.read_file(f'/evstill/evstill{card:03d}.pxl')).render().convert('RGB'), (x, y + 24))
        source_sheet.paste(shots[f'card{card}'][3900].crop((0, 0, 256, 192)), (x + 256, y + 24))
    ss = ROOT / 'eight_source_and_actual_card_comparisons.png'
    source_sheet.save(ss)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'nine_terminal_cold_boots4000_frames_each': reports,
        'eight_cards_two_complete_actual_holds_each786432_native5_pixels_exact': True,
        'ordinary_image84_control_two_complete_holds98304_native5_pixels_exact': True,
        'complete_source_planes_and_resident_files': planes,
        'all96_pre_fixture_full_RGB_and_RAM_pairs_and8_complete_entry_states_exact': True,
        'all16_lower_screen_hold_pairs_exact_to_disabled_control': True,
        'only_single_ARM9_R1_input_changed_no_ROM_script_save_RAM_or_source_PXL_changes': True,
        'all8_current_card_files_unchanged_from_reviewed_V414': True,
        'fixture_plan_controls': plan_cases,
        'five_native_host_prefix_controls_and8_bounded_read_controls_pass': True,
        'actual_original_loader_renderer_crops_and_full_caption_display_verified_under_fixture': True,
        'ordinary_village_scene_reachability_generated_consumer_or_global_nonuse_NOT_proven': True,
        'initial_main_only_options_guard_failure_retained_no_fixture_applied': True,
        'all18_plaques_incomplete_and_full_goal_active': True,
        'review_sheets': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in (sp, ss)],
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V699 eight actual card displays:16 whole source planes786432 pixels,96 pre-fixture pairs, original control and37 plan cases pass; ordinary usage remains open.', flush=True)


if __name__ == '__main__':
    main()
