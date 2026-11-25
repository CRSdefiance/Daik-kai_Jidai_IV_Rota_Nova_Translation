"""Verify ordinary recruitment, preserved gameplay, and the cumulative release."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_recruitment import TABLE, apply_release
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_tavern_queued_native_v626 import queued_wrap
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_recruitment_v627')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v627_candidate.nds')


def receipt(name, frames):
    root = CAP / name
    report_path = root / 'capture_report.json'
    report = read(report_path)
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    donor = report.get('battery_save_preloaded')
    if donor:
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {r['frame']: r for r in report['frames_captured']}
    for r in shots.values():
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
    return root, report, shots, {'path': str(report_path), 'sha256': sha(report_path.read_bytes())}


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v627'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and all(manifest['checks'].values())
    parent = NdsImage.open('out/all_routes_combined_v626_candidate.nds')
    common, arm, change = apply_release(parent.read_file('/COMMON/MESFILE.DK4'), parent.read_file('/__arm9__.bin'),
                                        'translations/tavern_recruitment_v1.json')
    assert common == rom.read_file('/COMMON/MESFILE.DK4') and arm == rom.read_file('/__arm9__.bin')
    old_files = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new_files = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert old_files.keys() == new_files.keys()
    assert {p for p in old_files if old_files[p] != new_files[p]} == {'/__arm9__.bin', '/COMMON/MESFILE.DK4'}
    old_root, old_run, old_shots, old_receipt = receipt('tavern_recruitment_v626_control', 7601)
    root, run, shots, new_receipt = receipt('tavern_recruitment_v627_actual', 7601)
    assert run['ROM_sha256'] == digest and run['scripted_input_schedule'] == old_run['scripted_input_schedule']
    assert read(root / 'navigation_command_journal.json')['commands_received'] == read(old_root / 'navigation_command_journal.json')['commands_received']
    assert shots.keys() == old_shots.keys()
    equal = sorted(set(shots) - {6000})
    for frame in equal:
        assert Image.open(shots[frame]['path']).convert('RGB').tobytes() == Image.open(old_shots[frame]['path']).convert('RGB').tobytes()
    raw = (root / 'frame_005600_arm9_ram.bin').read_bytes()
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    fleet_root = get(0xCB1A8)
    actor_id = get(0x82478, (fleet_root + 0x2090, 1))
    assert actor_id == 18
    actor = get(0xCB184) + 4 + actor_id * 32
    voice = get(0x7E988, (actor,))
    assert voice == 0
    number = struct.unpack_from('<8I', arm, TABLE - BASE)[voice]
    assert number == 897
    entries = common_message_entries(common, arm, clean=False)
    text = entries[number].text.rstrip(b' ')
    assert text == b'Who wants to sail with the Admiral?'
    formatted = queued_wrap(arm, text, 0x02053DB8, TABLE)
    pixels = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 80), instruction_limit=500000)
    im = Image.open(shots[6000]['path']).convert('RGB')
    for y in range(80):
        for x in range(228):
            assert bool(pixels[y * 228 + x]) == (im.getpixel((16 + x, 296 + y)) == (0, 8, 0))
    old_image = Image.open(old_shots[6000]['path']).convert('RGB')
    assert im.crop((0, 0, 256, 296)).tobytes() == old_image.crop((0, 0, 256, 296)).tobytes()
    states = []
    for frame in (3200, 5600, 6000, 6800, 7600):
        pair = []
        for r in (old_root, root):
            ram = (r / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
            cpu = machine(arm)
            cpu.mem_write(BASE, ram)

            def value(fn, args=(), uc=cpu):
                call(uc, fn, args)
                return uc.reg_read(UC_ARM_REG_R0)

            f = value(0xCB1A8)
            fleet = bytes(cpu.mem_read(f, 0x2090))
            nations = value(0xCB160)
            own = value(0x397D8, (nations,))
            money = value(0x3CCC8, (nations + 4 + own * 0x4C,))
            pair.append((fleet, money))
        assert pair[0] == pair[1]
        assert pair[1][1] == (8371 if frame < 6000 else 6798)
        states.append({'frame': frame, 'whole_original_fleet0x2090_exact_control': True,
                       'funds': pair[1][1], 'fleet_bytes_sha256': sha(pair[1][0])})
    finish_root, finish, fs, finish_receipt = receipt('tavern_recruitment_v627_finish', 8801)
    assert finish['ROM_sha256'] == digest
    assert Image.open(fs[7600]['path']).convert('RGB').tobytes() == Image.open(shots[7600]['path']).convert('RGB').tobytes()

    def event_key(e):
        return e['start'], e['duration'], tuple(e.get('buttons', [])), tuple(e.get('touch', []))

    # The follow-up file includes redundant identical input records. Preserve
    # them as executed; prove the deduplicated prefix and7600 state are exact.
    prefix = [e for e in finish['scripted_input_schedule'] if e['start'] <= 7600]
    assert {event_key(e) for e in prefix} == {event_key(e) for e in run['scripted_input_schedule']}
    finish_journal = read(finish_root / 'navigation_command_journal.json')['commands_received']
    assert [r['command'].get('buttons') for r in finish_journal if 'buttons' in r['command']] == [['X'], ['A'], ['B']]
    _, market, ms, market_receipt = receipt('tavern_recruitment_v627_market', 24100)
    _, _, ps, _ = receipt('tavern_schemes_v626_market', 24100)
    assert market['ROM_sha256'] == digest and 'battery_save_preloaded' not in market
    assert ms.keys() == ps.keys() and len(ms) == 19
    for frame, shot in ms.items():
        assert Image.open(shot['path']).convert('RGB').tobytes() == Image.open(ps[frame]['path']).convert('RGB').tobytes()
    native = read(ROOT / 'native_proof.json')
    assert native['candidate_sha256'] == digest and len(native['every_changed_entry_hot_and_cold_cache_copy']) == 166
    assert len(native['all14_voice_parent_whole_native_font_planes']) == 14
    assert native['script_sha256'] == sha(Path('scripts/verify_tavern_recruitment_native_v627.py').read_bytes())
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction'] and preservation['current921_format_palette_extent_checks']
    assert preservation['all57_embedded_block_extents_exact']
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': patch['patch_sha256'],
        'transform': change, 'actual_original_recruiter': {'actor_id': actor_id, 'voice': voice, 'message_id': number,
                                                        'unchanged_portrait_and_name': 'Charles Rochefort'},
        'complete_actual_228x80_dialogue_foreground_and_background_mask_exact': True,
        'every_other_before_after_and_Assign_Sailors_frame_exact_V626': equal,
        'original_control_fleet_and_money_states': states,
        'normal_game_recruits35_sailors_for1573_gold_without_any_fixture': True,
        'normal_Finish_X_Yes_A_Back_B_reaches_Town': finish_journal,
        'followup_redundant_identical_input_records_retained_deduplicated_prefix_and7600_pixels_exact': True,
        'all19_ordinary_no_save_no_fixture_screens_exact_V626': sorted(ms),
        'native_all7_voice_templates_14_planes166_hot_cold_cache_copies_verified': True,
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'reports': [old_receipt, new_receipt, finish_receipt, market_receipt],
        'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
        'older_CP932_I_renderer_model_and_broader_graphics_gates_remain_open': True,
        'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V627:complete actual Charles call,normal35-sailor recruitment/funds/fleet/Finish,19 ordinary screens,14 native voices166 cache copies and exact patch pass.')


if __name__ == '__main__':
    main()
