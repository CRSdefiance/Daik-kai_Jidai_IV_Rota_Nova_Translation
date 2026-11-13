"""Bounded original-contact observer; stop before changing any live duel state."""
import argparse
import ctypes as ct
import json
from pathlib import Path
import struct
import time
from PIL import Image
from dk4tool.patch.duel_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/duel_escape_observer_v1180')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_escape_v1179_1166_compassAttack8')
JOURNAL = Path('work/analysis/duel_escape_v1179_compassAttack8/navigation.jsonl')
ROM = Path('out/all_routes_combined_v1166_candidate.nds')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--cycles', type=int, default=100)
    args = parser.parse_args()
    assert not ROOT.exists() and 1 <= args.cycles <= 1000
    ROOT.mkdir(parents=True)
    kernel = ct.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [ct.c_uint, ct.c_int, ct.c_uint]
    kernel.OpenProcess.restype = ct.c_void_p
    kernel.GetExitCodeProcess.argtypes = [ct.c_void_p, ct.POINTER(ct.c_uint)]
    kernel.CloseHandle.argtypes = [ct.c_void_p]
    handle = kernel.OpenProcess(0x1000, 0, args.pid)
    assert handle

    def alive():
        status = ct.c_uint()
        assert kernel.GetExitCodeProcess(handle, ct.byref(status))
        return status.value == 259

    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    rows = current_entries(common, arm)
    targets = {rows[n].text: n for n in (*range(1931, 1957), *range(1973, 1980))}
    owner = struct.unpack_from('<I', arm, 0x552A0)[0]
    frame, observations, reason = 5714, [], 'bounded_contact_limit'
    try:
        for cycle in range(args.cycles+1):
            deadline = time.monotonic()+60
            raw_path, image_path = CAP/f'frame_{frame:06d}_arm9_ram.bin', CAP/f'frame_{frame:06d}_navigation.png'
            while True:
                assert alive(), 'Same emulator process is terminal; inspect its result instead of restarting'
                try:
                    raw = raw_path.read_bytes()
                    image = Image.open(image_path).convert('RGB')
                    image.load()
                    assert len(raw) == 0x400000 and image.size == (256, 384)
                    break
                except (FileNotFoundError, OSError, AssertionError):
                    pass
                if time.monotonic() >= deadline:
                    raise TimeoutError('Same live process has not reached its requested pause; do not restart')
                time.sleep(0.1)
            template = raw[owner-0x02000000+0x2030:owner-0x02000000+0x2230].split(b'\0')[0]
            cpu, get = get_machine(arm, raw)
            context = list(struct.unpack('<3I', cpu.mem_read(get(0x3F0F8)+8, 12)))
            entry = {'cycle': cycle, 'frame': frame, 'RAM_sha256': sha(raw),
                'capture_sha256': sha(image_path.read_bytes()), 'context': context,
                'native_last_template_hex': template.hex(), 'last_template_ID_if_exact': targets.get(template),
                'cache_block_tag': raw[owner-0x02000000+0x2C]}
            observations.append(entry)
            if template in targets:
                reason = 'original_duel_or_escape_template_observed_stop_without_healing'
                break
            if context != [0, 1, 8]:
                reason = 'original_battle_context_ended'
                break
            root = get(0xCB1A8)
            own, enemy = root+4+132, root+4+8*132
            mobiles = [get(0x36C70, fleet+12) for fleet in (own, enemy)]
            entry['positive_Hull_Crew'] = [[get(0x5543C, m), get(0x55444, m)] if m else [0, 0] for m in mobiles]
            if any(v <= 0 for values in entry['positive_Hull_Crew'] for v in values):
                reason = 'disabled_vessel_no_revival'
                break
            if cycle == args.cycles:
                break
            command = {'until': frame+2, 'duration': 1, 'battle_fixture': {'duel_context': 'unarmoredContact'}}
            with JOURNAL.open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(command)+'\n')
            save(ROOT/'live_observation_journal.json', {'emulator_PID': args.pid, 'observations': observations,
                'last_command': command, 'commands_are_not_execution_receipts': True})
            frame += 2
            if cycle % 20 == 0:
                print(f'Contact cycle{cycle}, frame{frame}; original last template unchanged, positive vessels.', flush=True)
    finally:
        kernel.CloseHandle(handle)
    save(ROOT/'bounded_result.json', {'ROM': str(ROM), 'ROM_sha256': sha(ROM.read_bytes()),
        'emulator_PID': args.pid, 'observations': observations, 'stop_reason': reason,
        'emulator_left_paused_for_separate_visual_and_source_verification': True,
        'no_message_ID_RNG_actor_ID_or_battle_outcome_injection': True,
        'permitted_contact_location_low_positive_starting_HP_and_live_ship_recovery_only_before_duel': True,
        'no_actual_scene_or_completion_credit_without_separate_verifier': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Contact observer stopped: {reason}, frame{frame}; last template ID{observations[-1]["last_template_ID_if_exact"]}', flush=True)


if __name__ == '__main__':
    main()
