"""Verify actual raw loads, independent tail liveness and whole-screen controls."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_MEM_READ, arm_const

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.probe_button_prompt_native import call, machine
from scripts.replay_raw_portrait_tail_v689 import execute, payload_access
from scripts.trace_raw_portrait_tail_v689 import FOLDER, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save


def pictures(report):
    images = {}
    for s in report['frames_captured']:
        p = Path(s['path'])
        assert sha(p.read_bytes()) == s['PNG_sha256']
        im = Image.open(p).convert('RGB')
        if s['frame'] in images:
            assert images[s['frame']].tobytes() == im.tobytes()
        images[s['frame']] = im
    return images


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert pre['producer_sha256'] == sha(Path('scripts/trace_raw_portrait_tail_v689.py').read_bytes())
    assert pre['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    controls = read(ROOT / 'prefix_controls/native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 15 and len(controls['read_policy_cases']) == 8
    rp = FOLDER / 'capture_report.json'
    report = read(rp)
    assert report['frames'] == 4000 and report['ROM_sha256'] == pre['candidate_sha256']
    assert report['core_DLL_sha256'] == CORE_SHA and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('battery_save_preloaded')
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == read(pre['inputs'])
    observed = pictures(report)
    baseline = read(pre['baseline_report'])
    assert sha(Path(pre['baseline_report']).read_bytes()) == pre['baseline_report_sha256']
    expected = pictures(baseline)
    assert set(observed) == set(pre['capture_frames']) and len(observed) == 21
    assert all(im.tobytes() == expected[f].tobytes() for f, im in observed.items())
    older_path = Path(pre['older_4000_frame_baseline'])
    older = read(older_path)
    assert older['frames'] == 4000 and older['cold_boot'] and not older['savestate_loaded']
    assert older['scripted_input_schedule'] == report['scripted_input_schedule']
    assert older['core_DLL_sha256'] == CORE_SHA
    assert sha(Path(older['ROM']).read_bytes()) == older['ROM_sha256']
    old_baseline = older_path.parent
    assert (FOLDER / 'final_arm9_ram.bin').read_bytes() == (old_baseline / 'final_arm9_ram.bin').read_bytes()
    events = read(FOLDER / 'observer/events.json')
    assert events['producer_sha256'] == pre['producer_sha256']
    assert events['source_contract_sha256'] == pre['source_contract_sha256']
    assert read(FOLDER / 'run_contract.json')['preflight_sha256'] == sha((ROOT / 'preflight.json').read_bytes())
    assert events['callbacks'] == 9 and events['ignored'] == 0
    assert not events['mismatches'] and not events['errors']
    assert events['all_host_slots_restored_core_file_exact']
    assert events['CPU_WRAM_DTCM_configuration_unchanged_at_every_callback']
    rows = events['rows']
    assert [r['kind'] for r in rows] == ['raw_entry', 'raw_return'] * 4 + ['loop_complete']
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    blocks = IlnkContainer.parse(rom.read_file('/GRP/SLACKIMG.DK4')).blocks
    source = IlnkContainer.parse(clean.read_file('/GRP/SLACKIMG.DK4')).blocks
    cases = []
    for index in range(4):
        entered, returned, following = rows[index * 2:index * 2 + 3]
        a = struct.unpack('<32I', bytes.fromhex(entered['CPU128_hex']))
        b = struct.unpack('<32I', bytes.fromhex(returned['CPU128_hex']))
        c = struct.unpack('<32I', bytes.fromhex(following['CPU128_hex']))
        assert a[4:8] == (14 + index, 0x02233040, 0, 0) and a[18] == 0x0209EDEC
        assert a[13] == b[13] == index and c[13] == index + 1
        assert a[14] == b[14] == c[14] == 0x02192500
        raw = Path(returned['RAM']).read_bytes()
        assert len(blocks[14 + index]) == 14144 and blocks[14 + index] == source[14 + index]
        assert raw[0x233040:0x233040 + 14144] == blocks[14 + index]
        u, native = execute(returned, c[2])
        assert native['stop_PC'] == c[2]
        assert native['registers'] == list(c[4:19]) and native['CPSR'] == c[20]
        assert not native['raw_payload_reads'] and not native['raw_payload_writes']
        assert not native['executed_instruction_words_different_from_original']
        target_ram = Path(following['RAM']).read_bytes()
        assert bytes(u.mem_read(0x02000000, 0x400000)) == target_ram
        assert bytes(u.mem_read(0x027E0000, 0x4000)) == Path(following['DTCM']).read_bytes()
        poison = bytes((i * 37 + index * 19) % 256 for i in range(14144))
        altered, counterfactual = execute(returned, c[2], raw_override=poison)
        assert counterfactual['registers'] == native['registers'] and counterfactual['CPSR'] == native['CPSR']
        assert not counterfactual['raw_payload_reads'] and not counterfactual['raw_payload_writes']
        expected_altered = bytearray(target_ram)
        expected_altered[0x233040:0x233040 + 14144] = poison
        assert bytes(altered.mem_read(0x02000000, 0x400000)) == expected_altered
        assert bytes(altered.mem_read(0x027E0000, 0x4000)) == Path(following['DTCM']).read_bytes()
        cases.append({'block': 14 + index, 'source_bytes': 14144, 'source_sha256': sha(blocks[14 + index]),
            'native_tail': native, 'complete_actual_following_CPU_CPSR_RAM_DTCM_exact': True,
            'isolated_poison_control_sha256': sha(poison),
            'poison_changes_only_exact_supplied14144_bytes_not_views_CPU_or_other_RAM': True})
    # A positive original native header-word getter proves the read detector fires.
    calibration = machine(rom.read_file('/__arm9__.bin'))
    assert bytes(calibration.mem_read(0x020BEE88, 8)) == bytes.fromhex('040090e51eff2fe1')
    calibration.mem_write(0x02233040, b'\x78\x56\x34\x12')
    seen = []

    def observed_read(_u, _access, address, size, _value, _data):
        if payload_access(address, size, 0x027E0000):
            seen.append((address, size))

    handle = calibration.hook_add(UC_HOOK_MEM_READ, observed_read)
    try:
        call(calibration, 0xBEE88, (0x0223303C,))
    finally:
        calibration.hook_del(handle)
    assert seen == [(0x02233040, 4)] and calibration.reg_read(arm_const.UC_ARM_REG_R0) == 0x12345678
    assert all(payload_access(0x02233040 + mirror * 0x400000, 4, 0x027E0000) for mirror in range(4))
    assert not payload_access(0x027E0000, 4, 0x027E0000)
    final = Path(rows[-1]['RAM']).read_bytes()
    views = []
    for index in range(4):
        at = 0x02192500 + 0x5AC + index * 0x30
        words = struct.unpack_from('<12I', final, at - 0x02000000)
        assert words[5] == 4 and words[7:9] == (0, 0) and words[10:12] == (104, 136)
        owner = words[3]
        fp = struct.unpack_from('<I', final, owner + 12 - 0x02000000)[0]
        filename = final[fp - 0x02000000:fp - 0x02000000 + 128].split(b'\0')[0].decode('ascii')
        assert filename == f'_pxl/personbustup{index:02d}.pxl'
        views.append({'index': index, 'view': at, 'whole48_byte_view_hex': final[at - 0x02000000:at - 0x02000000 + 48].hex(),
            'owner': owner, 'initialized_owner_filename': filename,
            'whole_original_PXL_sha256': sha(rom.read_file('/' + filename)),
            'reserved_words_not_invented_as_zero': True})
    sheet = Image.new('RGB', (768, 410), '#263238')
    draw = ImageDraw.Draw(sheet)
    for col, frame in enumerate((1200, 1500, 2000)):
        draw.text((col * 256 + 5, 5), f'V685 ordinary frame {frame}', fill='white')
        sheet.paste(observed[frame], (col * 256, 24))
    sheet_path = ROOT / 'actual_chooser_and_confirmation.png'
    sheet.save(sheet_path)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'report': str(rp), 'report_sha256': sha(rp.read_bytes()),
        'events_sha256': sha((FOLDER / 'observer/events.json').read_bytes()),
        'retained_terminal_baseline_report': str(older_path),
        'retained_terminal_baseline_report_sha256': sha(older_path.read_bytes()),
        'retained_terminal_baseline_ROM_sha256': older['ROM_sha256'],
        'retained_terminal_baseline_RAM_sha256': sha((old_baseline / 'final_arm9_ram.bin').read_bytes()),
        '21_complete_current_baseline_two_screen_pairs_and_retained_terminal_RAM_exact': True,
        '15_native_host_controls8_mirror_controls_no_live_gameplay_fixture': True,
        'four_complete_actual_source_raw_loads': cases, 'four_final_constructed_views': views,
        'positive_native_read_detector_and_four_mirror_classifications_pass': True,
        'post_read_loop_segments_do_not_consume_raw_payload_and_build_loose_PXL_views': True,
        'last_raw17_after_loop_and_other_consumers_not_globally_excluded': True,
        'not_actual_display_clearance_for_raw_portraits_comics_or_legacy_CMMNIMG': True,
        'Sea_cow_review_retained_existing_documented_bullfighter_wordplay_no_translation_change': True,
        'all18_plaques_incomplete22_original_requirements_and_other_graphics_open': True,
        'review_sheet': str(sheet_path), 'review_sheet_sha256': sha(sheet_path.read_bytes()),
        'producer_sha256': pre['producer_sha256'],
        'replay_sha256': sha(Path('scripts/replay_raw_portrait_tail_v689.py').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V689:four exact native tails do not read raw bytes; four poison controls, actual PXL views and21 baseline pairs pass.', flush=True)


if __name__ == '__main__':
    main()
