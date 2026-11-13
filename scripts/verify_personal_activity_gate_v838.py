"""Original Deck-entry time/at-sea gate; controlled CPU inputs, not gameplay."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_personal_release_v838 import ROOT
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_chatter_v838_deck_interactive2')


def main():
    rom = Path('out/all_routes_combined_v838_candidate.nds')
    arm = NdsImage.open(rom).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x12B58, 0x12B78), (0x13B90, 0x13D80), (0x34674, 0x34688),
             (0x82B98, 0x82BA0), (0x93E0, 0x9598))
    assert all(arm[a:b] == clean[a:b] for a, b in spans)
    snapshot = CAP / 'frame_011200_arm9_ram.bin'
    raw = snapshot.read_bytes()
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    def get(fn, *args):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    model = get(0xCB1A8)
    fleet = model + 4 + 0x84 * get(0x2E58C)
    calendar = get(0xCB1B4)
    controller = model + struct.unpack_from('<I', arm, 0x13C90)[0]
    last_deck = struct.unpack_from('<I', arm, 0x13D70)[0]
    observed = {'docked_town': get(0x34674, fleet),
                'calendar_tick': struct.unpack_from('<I', raw, calendar + 8 - BASE)[0],
                'last_Deck_entry_tick': struct.unpack_from('<I', raw, last_deck - BASE)[0],
                'last_controller_tick': get(0x82B98, controller),
                'roles': {str(n): get(0x81F54, controller, n) for n in (0, 4, 5, 6)}}
    icon_table = struct.unpack_from('<I', arm, 0x13C88)[0]
    icons = struct.unpack_from('<6I', arm, icon_table - BASE)
    mapping = [{'native_icon_ID': n, 'actor_ID': get(0x93E0, n)} for n in icons]
    cases = []
    for sea, deck_age, controller_age, zero_last in [
            (True, d, c, False) for d in (959, 960, 961) for c in (959, 960, 961)] + [
            (False, 960, 960, False), (True, 960, 960, True)]:
        cpu.mem_write(BASE, raw)
        # Explicit test-only counter/model fixtures. No live emulator writes.
        now = 4000
        cpu.mem_write(calendar + 8, struct.pack('<I', now))
        cpu.mem_write(last_deck, struct.pack('<I', 0 if zero_last else now - deck_age))
        cpu.mem_write(controller + 0x28, struct.pack('<I', now - controller_age))
        flags = raw[fleet + 0x50 - BASE]
        cpu.mem_write(fleet + 0x50, bytes([(flags | 8) if sea else (flags & ~8)]))
        view = 0x02468000
        cpu.mem_write(view, bytes(0x500))
        calls = []
        def selected(u, pc, size, unused):
            calls.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        hook = cpu.hook_add(UC_HOOK_CODE, selected, begin=BASE + 0x13B90, end=BASE + 0x13B90)
        try:
            call(cpu, 0x13C94, (view,))
        finally:
            cpu.hook_del(hook)
        expected = sea and not zero_last and deck_age >= 960 and controller_age >= 960
        assert calls == ([view] if expected else [])
        assert struct.unpack('<I', cpu.mem_read(last_deck, 4))[0] == now
        cases.append({'at_sea': sea, 'Deck_age': deck_age, 'controller_age': controller_age,
                      'last_Deck_zero': zero_last, 'native_scheduler_selected': bool(calls),
                      'native_entry_timestamp_updated': True})
    save(ROOT / 'original_activity_entry_gate.json', {
        'candidate_sha256': sha(rom.read_bytes()), 'source_RAM': str(snapshot), 'source_RAM_sha256': sha(raw),
        'all_source_code_spans_equal_clean': [list(s) for s in spans],
        'only_direct_scheduler_caller': '02012B6C inside the original Deck entry02012AB0',
        'observed_docked_save': observed, 'source_six_icon_to_actor_mapping': mapping,
        'icon_lookup93E0_is_constant_conversion_not_assigned_room_occupancy': True,
        'eleven_original_native_threshold_cases': cases,
        'required_at_sea_and_nonzero_previous_Deck_entry_and_both_ages_at_least960_ticks': True,
        'no_live_RAM_ROM_save_or_random_changes': True,
        'activity_scheduler_body_intercepted_not_actual_comment_activation_or_eligibility_approval': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Original Deck-entry gate:11 native threshold cases pass. Dockside time0 cannot activate;icon IDs are not room assignments.', flush=True)


if __name__ == '__main__':
    main()
