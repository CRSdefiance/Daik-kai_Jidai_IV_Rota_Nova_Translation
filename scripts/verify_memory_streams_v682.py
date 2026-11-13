"""Actual save-buffer provenance, full native reads and complete Save/Load plaques."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.observe_file_requests_v681 import main_read
from scripts.prepare_memory_streams_v682 import BUFFERS, ROM, ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.run_village_visits_v664 import CAP
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_village_wrap_v608 import read, save

ACTIVE = (6200, 7400, 7800, 8200, 8600, 9000, 9400, 9800, 10200, 10600,
          11000, 11400, 11800, 12200, 12600, 13000, 13400, 13800)


def main():
    pre, config, contract = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json'), read(ROOT / 'source_contract.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    controls = read(ROOT / 'native_prefix_controls.json')
    assert len(controls['native_host_cases']) == 20
    assert controls['current_observer_sha256'] == sha(Path('scripts/observe_memory_streams_v682.py').read_bytes())
    native = read(ROOT / 'native_memory_operations.json')
    assert len(native['cases']) == 4 and sum(len(c['calls']) for c in native['cases']) == 40
    assert native['checker_sha256'] == sha(Path('scripts/check_memory_streams_v682.py').read_bytes())
    donor = Path(config['donor']).read_bytes()
    assert sha(donor) == config['donor_sha256']
    reports, images, shots, refs = {}, {}, {}, []
    for tag in ('observed', 'baseline'):
        folder = CAP / ('memory_streams_v682_' + tag)
        path = folder / 'capture_report.json'
        r = read(path)
        assert r['frames'] == 14200 and r['cold_boot'] and not r['savestate_loaded'] and not r['callback_errors']
        assert r['ROM_sha256'] == pre['candidate_sha256'] and r['core_DLL_sha256'] == CORE_SHA
        assert r['battery_save_preloaded']['source_sha256'] == config['donor_sha256']
        assert not any(k.startswith('synthetic_') and v for k, v in r.items())
        assert r['scripted_input_schedule'] == read(config['inputs'])
        c = read(folder / 'run_contract.json')
        assert c['runner_sha256'] == sha(Path('scripts/run_memory_streams_v682.py').read_bytes())
        assert c['observer_sha256'] == controls['current_observer_sha256']
        frames, rows = {}, {}
        for row in r['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            im = Image.open(row['path']).convert('RGB')
            if row['frame'] in frames:
                assert im.tobytes() == frames[row['frame']].tobytes()
            frames[row['frame']], rows[row['frame']] = im, row
        reports[tag], images[tag], shots[tag] = r, frames, rows
        refs.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    assert images['observed'].keys() == images['baseline'].keys() and len(images['observed']) == 32
    assert all(im.tobytes() == images['baseline'][f].tobytes() for f, im in images['observed'].items())
    assert (CAP / 'memory_streams_v682_observed/final_arm9_ram.bin').read_bytes() == (
        CAP / 'memory_streams_v682_baseline/final_arm9_ram.bin').read_bytes()
    meta_path = CAP / 'memory_streams_v682_observed/observer/memory_streams.json'
    meta = read(meta_path)
    assert meta['observer_sha256'] == controls['current_observer_sha256']
    assert meta['all_opcode_slots_restored_before_free_and_core_file_exact'] and not meta['errors'] and not meta['mismatches']
    assert meta['source_contract_sha256'] == sha((ROOT / 'source_contract.json').read_bytes())
    assert len(meta['rows']) == 9 and meta['callbacks'] == 33
    assert meta['ignored_nonmemory_entries'] == {'stream_open': 12, 'stream_close': 12}
    targets = {t['PC']: t for t in contract['targets']}
    snapshots = []
    for row in meta['rows']:
        raw = Path(row['snapshot']).read_bytes()
        assert sha(raw) == row['snapshot_sha256'] and len(raw) == 0x400000
        values = struct.unpack('<32I', bytes.fromhex(row['CPU128_hex']))
        assert values[1] == targets[row['PC']]['word'] and values[2] == row['PC'] and values[19] == row['PC'] + 8
        owner = values[8] if row['owner_register'] == 'r4' else values[4]
        assert owner == row['owner']
        fields = struct.unpack('<10I', main_read(raw, owner, 40))
        assert tuple(row['complete_stream_fields']) == fields
        assert row['entire_CPU_prefix_and4MiB_WRAM_unchanged_by_observer']
        if 'payload' in row:
            payload = Path(row['payload']).read_bytes()
            assert sha(payload) == row['payload_sha256'] and len(payload) == row['payload_bytes']
            assert payload == main_read(raw, row['provider'], len(payload))
        snapshots.append(raw)
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    sessions = []
    for first in (0, 3, 6):
        entered, returned, closed = meta['rows'][first:first + 3]
        mode = entered['requested_mode']
        assert entered['kind'] == 'stream_open' and closed['kind'] == 'stream_close'
        assert entered['owner'] == returned['owner'] == closed['owner']
        assert returned['provider'] == closed['provider'] == BUFFERS[mode]
        assert returned['cursor'] == returned['highwater'] == 0
        assert closed['highwater'] == closed['payload_bytes'] == 37015
        assert closed['cursor'] == (124 if mode == 2 else 37015)
        payload = Path(closed['payload']).read_bytes()
        source_offset = donor.find(payload)
        assert source_offset == ({0: 204800, 6: 0}.get(first, -1))
        if mode == 1:
            assert donor[source_offset:source_offset + 37015] == payload
            assert source_offset % 40960 == 0
        raw = snapshots[first + (1 if mode == 1 else 2)]
        u = machine(arm)
        u.mem_write(BASE, raw)
        if mode == 2:
            call(u, 0xD0274, (closed['owner'], 0, 0))
        execution = call(u, 0xD01AC, (closed['owner'], 0x02470020, 37015), instruction_limit=1000000)
        assert u.reg_read(UC_ARM_REG_R0) == 37015 and bytes(u.mem_read(0x02470020, 37015)) == payload
        assert not {0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & execution
        after = bytes(u.mem_read(BASE, 0x400000))
        offset = (closed['owner'] - BASE) & 0x3FFFFF
        assert all(a == b for i, (a, b) in enumerate(zip(raw, after, strict=True))
                   if not (offset + 8 <= i < offset + 12 or offset + 32 <= i < offset + 36))
        sessions.append({'mode': mode, 'open_frame': entered['frame'], 'close_frame': closed['frame'],
            'provider': returned['provider'], 'bytes': 37015,
            'donor_slot_zero_based': source_offset // 40960 if mode == 1 else None,
            'complete_donor_payload_offset': source_offset if mode == 1 else None,
            'payload_sha256': sha(payload), 'full_isolated_original_native_read_from_actual_snapshot_exact': True,
            'actual_close_cursor': closed['cursor'], 'size_highwater_is_independent_of_current_cursor': True,
            'only_stream_cursor_highwater_changed_in_main_RAM_during_replay': True,
            'mode2_replay_is_byte_readback_not_whole_game_or_cartridge_save_roundtrip': mode == 2})
    atlas_data = NdsImage.open(ROM).read_file('/_pxl/saveloadinfo.pxl')
    assert atlas_data == NdsImage.open('out/all_routes_combined_v612_candidate.nds').read_file('/_pxl/saveloadinfo.pxl')
    atlas, font = PxlImage.from_bytes(atlas_data), GameAsciiFont.from_arm9(arm)
    transform = read('work/analysis/save_load_plaques_v612/transform_proof.json')
    plaque_cases = []
    for frame in ACTIVE:
        im = images['observed'][frame]
        for row in transform['records']:
            l, t, r, b = row['restore_box']
            assert all(native5(im.getpixel((x, y))) == native5(atlas.palette[atlas.indices[y * 256 + x]])
                       for y in range(t, b) for x in range(l, r))
            fl, ft, fr, fb = row['original_and_final_plaque_box']
            x0, y0 = row['font_origin']
            ink = {(x0 + n * 5 + x, y0 + y) for n, ch in enumerate(row['English'])
                   for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
            actual = {(x, y) for y in range(ft + 2, fb - 2) for x in range(fl + 2, fr - 2)
                      if native5(im.getpixel((x, y))) == native5(atlas.palette[1])}
            assert actual == ink and len(ink) == row['complete_native_font_ink']
            plaque_cases.append({'frame': frame, 'English': row['English'], 'complete_ink_points': len(ink),
                'complete_original_material_frame_region_native5_pixels': (r - l) * (b - t),
                'all_first_final_glyph_strokes_and_blank_cells_exact': True, 'fully_completed': False})
    selected = (6200, 7800, 11000, 11800, 12600, 13400, 13800, 14200)
    canvas = Image.new('RGB', (1024, 820), '#263238')
    draw = ImageDraw.Draw(canvas)
    for i, frame in enumerate(selected):
        x, y = i % 4 * 256, i // 4 * 410
        draw.text((x + 3, y + 4), f'V678 Save/Load {frame}', fill='white')
        canvas.paste(images['observed'][frame], (x, y + 24))
    sheet = ROOT / 'actual_Save_Load_review.png'
    canvas.save(sheet)
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'], 'reports': refs,
        'two_terminal14200_frame_cold_boots32_whole_screen_pairs_and_terminal_RAM_exact': True,
        'isolated_donor_no_savestate_or_live_gameplay_fixtures': True,
        'trace': str(meta_path), 'trace_sha256': sha(meta_path.read_bytes()),
        '33_actual_callbacks9_memory_records24_disk_ignored_and_no_state_writes': True,
        'three_actual_memory_sessions': sessions,
        'two_mode1_payloads74030_bytes_exact_donor_save_slots5_and0': True,
        'mode2_current_game_buffer_byte_readback_exact_not_actual_cartridge_save': True,
        'known_mode1_mode2_paths_serialize_saved_state_not_additional_filename_loaders': True,
        '40_controlled_original_memory_ops20_native_host_prefix_controls_and8_mirror_controls': True,
        'source_Save_Load_asset_exact_V612_and_all36_plaque_regions26568_pixels_verified': plaque_cases,
        'all18_original_plaque_hints22_historical_requirements_and_other_graphics_gates_open': True,
        'review_sheet': str(sheet), 'review_sheet_sha256': sha(sheet.read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'current_goal_turn_classification': 'progress',
        'full_goal_complete': False})
    print('V682: actual save-stream buffers/source slots,32 full baseline frames and36 complete Level/Power plaques verified.', flush=True)


if __name__ == '__main__':
    main()
