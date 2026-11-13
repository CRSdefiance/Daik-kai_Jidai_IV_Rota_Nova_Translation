"""Verify ordinary shipyard selections and source-bound Refit wrap findings."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inspect_committed_gpu_v646 import CORE, CORE_SHA
from scripts.inspect_graphic_paints_v669 import units
from scripts.run_room_gender_v694 import CAP
from scripts.run_yard_selection_v705 import ROOT
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_graphic_paints_v669 import caller, intersecting, source_rect
from scripts.verify_village_wrap_v608 import read, save

FINDINGS = (
    (13400, 1287, ['  Square sails favor tailwin', 'ds.', ' No lateen sail ahead.'], 'tailwinds'),
    (14600, 1248, ['A carpenter can repair damag', 'ed', ' ships.'], 'damaged'),
    (15800, 1255, ['A purser enables deals and b', 'uyouts.'], 'buyouts'),
    (16100, 1249, ["A ship's doctor can cure ail", 'ments affecting crew members', ' and sailors.'], 'ailments'),
    (16400, 1250, ['A chief cook saves water and', ' food and reduces sailor fat', 'igue.'], 'fatigue'),
)


def load(suffix, pre, config):
    folder = CAP / f'yard_selection_v705_{suffix}'
    report = read(folder / 'capture_report.json')
    assert report['frames'] == config['frames'] == 19700
    assert report['ROM_sha256'] == pre['candidate_sha256'] and report['core_DLL_sha256'] == CORE_SHA
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['battery_save_preloaded']['source_sha256'] == pre['donor_sha256']
    assert report['scripted_input_schedule'] == read(config['inputs'])
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    contract = read(folder / 'run_contract.json')
    assert contract['config'] == config
    assert contract['runner_sha256'] == sha(Path('scripts/run_yard_selection_v705.py').read_bytes())
    shots = {s['frame']: s for s in report['frames_captured']}
    snapshots = {s['frame']: s for s in report['read_only_capture_RAM_snapshots']}
    assert sorted(shots) == sorted(snapshots) == config['captures']
    for s in shots.values():
        assert sha(Path(s['path']).read_bytes()) == s['PNG_sha256']
    for s in snapshots.values():
        assert s['read_only_export'] and sha(Path(s['path']).read_bytes()) == s['sha256']
    return folder, report, shots, snapshots


def main():
    pre, config = read(ROOT / 'preflight.json'), read(ROOT / 'run_config.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(CORE.read_bytes()) == CORE_SHA
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    folder, observed, shots, snaps = load('observed', pre, config)
    _base_folder, baseline, base_shots, base_snaps = load('baseline', pre, config)
    pilot = read(config['pilot_report'])
    assert sha(Path(config['pilot_report']).read_bytes()) == config['pilot_report_sha256']
    pilot_shots = {s['frame']: s for s in pilot['frames_captured']}
    assert shots.keys() == base_shots.keys() == pilot_shots.keys()
    for frame in shots:
        current = Image.open(shots[frame]['path']).convert('RGB').tobytes()
        assert current == Image.open(base_shots[frame]['path']).convert('RGB').tobytes()
        assert current == Image.open(pilot_shots[frame]['path']).convert('RGB').tobytes()
        assert Path(snaps[frame]['path']).read_bytes() == Path(base_snaps[frame]['path']).read_bytes()
    assert observed['frames'] == baseline['frames'] == max(snaps) == max(base_snaps)
    # These runs export capture RAM, including their exact last emulated frame.
    # They do not request a separate final_arm9_ram.bin export.
    assert Path(snaps[observed['frames']]['path']).read_bytes() == Path(base_snaps[baseline['frames']]['path']).read_bytes()
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    segments, originals = units(rom), units(clean)
    meta = read(folder / 'observer/paint_observer.json')
    assert meta['script_sha256'] == config['frozen_files']['scripts/observe_graphic_paints_v669.py']
    assert meta['source_contract_sha256'] == config['frozen_files'][str(Path('work/analysis/graphic_paints_v669/source_contract.json'))]
    assert meta['original_slot_restored_and_DLL_file_unchanged'] and not meta['overflow'] and not meta['mismatch']
    data = Path(meta['path']).read_bytes()
    assert sha(data) == meta['sha256'] and len(data) == meta['records'] * 160
    counts, guards, footprints, parents = Counter(), Counter(), Counter(), {}
    hits = []
    targets = {r['PC']: r for r in read('work/analysis/graphic_paints_v669/source_contract.json')['targets']}
    for row in struct.iter_unpack('<40I', data):
        frame, pc, instruction, screen, header, bank, desc, sp, lr, r15, cpsr, host = row[:12]
        assert 1 <= frame <= config['frames'] and pc in targets
        assert instruction == host == targets[pc]['original_instruction'] and r15 == pc + 8 and not cpsr & 32
        assert screen in (0, 1) and not header % 4 and not desc % 4 and not sp % 4
        counts[row[37]] += 1
        guards[row[38]] += 1
        if row[37] in (1, 2, 6):
            assert row[38] == 0
            rect = source_rect(row)
            assert all(0 <= n <= 256 for n in rect)
            assert rect[0] + rect[2] <= 256 and rect[1] + rect[3] <= 256
            assert 0 <= bank < (1 if row[37] == 2 else 83)
            footprints[(row[37], pc, *rect, bank)] += 1
            parents[(pc, lr)] = caller(segments, originals, lr, pc)
            if row[37] == 1:
                selected = intersecting(rect, pc == 0x01FFAE70, CELLS)
                if selected:
                    hits.append({'frame': frame, 'PC': pc, 'LR': lr, 'XYWH': rect, 'controls': selected})
    assert not hits and all(counts[k] == 0 for k in (2, 3, 4, 5, 7))
    states = []
    for frame in (3200, 5300, 9800, 12800, 13400, 19700):
        raw = Path(snaps[frame]['path']).read_bytes()
        ships, money = fleet_models(arm, raw, 1), funds(arm, raw)
        assert len(ships) == 5 and [r['name'] for r in ships] == ['Vestaros', 'Latina', 'Latina', 'Latina', 'Latina']
        assert money == 25975
        states.append({'frame': frame, 'ships': ships, 'funds': money})
    messages = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    source = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    font = GameAsciiFont.from_arm9(arm)
    defects = []
    for frame, message_id, lines, word in FINDINGS:
        image = Image.open(shots[frame]['path']).convert('RGB')
        expected = {(64 + i * 6 + x, 80 + j * 16 + y)
            for j, line in enumerate(lines) for i, ch in enumerate(line)
            for y in range(11) for x in range(6) if font.decode(ch).getpixel((x, y))}
        actual = {(x, y) for y in range(80, 155) for x in range(64, 232)
            if image.getpixel((x, y)) == (230, 230, 230)}
        assert actual == expected, (frame, sorted(actual ^ expected)[:8])
        assert max(map(len, lines)) <= 28
        raw = Path(snaps[frame]['path']).read_bytes()
        message = messages[message_id]
        assert word in message.text.decode('cp932')
        # Exact live text bytes must be present, rather than inferring the selected
        # message from a similar screenshot or from a historical record number.
        # The first mast hint and the later room hints have different live
        # allocation addresses. Bind each actual complete string separately.
        buffer = 0x0218CD78 if frame == 13400 else 0x0218D418
        start = buffer - 0x02000000
        assert raw[start:start + len(message.text)] == message.text
        for edge in (min(x for x, _ in actual), max(x for x, _ in actual)):
            assert {p for p in actual if p[0] != edge} != expected
        defects.append({'frame': frame, 'native_message_id': message_id,
            'clean_Japanese_source': source[message_id].text.decode('cp932'),
            'current_text': message.text.decode('cp932'), 'actual_complete_lines': lines,
            'word_split_by_original_fixed_character_wrap': word, 'complete_foreground_points': len(actual),
            'entire_168x75_body_foreground_and_blank_cells_exact': True,
            'actual_inline_text_buffer': buffer,
            'first_final_ink_column_erasure_controls_rejected': True})
    ids = list(range(1248, 1256)) + list(range(1268, 1290))
    family = [{'message_id': i, 'clean_source': source[i].text.decode('cp932'),
        'current': messages[i].text.decode('cp932'), 'source_block': source[i].block,
        'source_record': source[i].record_index, 'current_block': messages[i].block,
        'current_record': messages[i].record_index} for i in ids]
    save(ROOT / 'refit_repair_queue.json', {'source_stable_native_IDs_not_current_record_indices': family,
        'observed_native_columns': 28, 'confirmed_split_word_cases': defects,
        'required_next_step': 'Trace original Refit text setup/paint and implement source-reviewed word wrapping for the complete help family; preserve progressive dialogue IDs and verify actual first/final glyphs.',
        '30_help_messages_identified_not_all30_normal_contexts_verified': True,
        'no_new_translation_or_production_fix_claimed': True})
    save(ROOT / 'proof.json', {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'three_terminal19700_frame_cold_boots_pilot_observed_baseline': True,
        'observer_baseline_whole_RGB_pairs': len(shots), 'pilot_replay_whole_RGB_pairs': len(shots),
        'observer_baseline_full4MiB_capture_RAM_pairs': len(snaps), 'terminal_RAM_exact': True,
        'actual_drawing_entries': meta['records'], 'binding_counts': dict(counts), 'guard_counts': dict(guards),
        'footprints': [{'binding': b, 'PC': p, 'XYWH': [x, y, w, h], 'bank': k, 'entries': n}
            for (b, p, x, y, w, h, k), n in sorted(footprints.items())],
        'source_bound_callers': list(parents.values()), 'selected_miniature_footprints': hits,
        'six_control_normal_parents_still_open_no_global_nonuse_claim': True,
        'five_ship_and_unchanged_funds_states': states,
        'final_screen_is_cancel_remodeling_confirmation_not_completed_cancel_or_save': True,
        'five_complete_source_bound_Refit_body_wrap_defects': defects,
        '30_source_help_IDs_queued_for_shared_layout_fix': ids,
        'initial_noninteractive_pilot_EOF_at3200_terminal_exit1_retained_no_completion_credit': True,
        'no_fixtures_or_production_ROM_graphics_patch_registry_changes': True,
        'all18_plaques_and22_historical_requirements_remain_open_or_preserved': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V705: {len(shots)} full RGB/RAM pairs, {meta["records"]} original paint entries; five Refit wrap defects source-bound, 30-message repair queued.', flush=True)


if __name__ == '__main__':
    main()
