"""Bind actual allocator/free events to unchanged whole ordinary Refit frames."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_layout_v2 import CLEANUP
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v708 import load
from scripts.run_refit_display_v712 import ROM
from scripts.run_room_gender_v694 import CAP
from scripts.trace_refit_heap_v713 import FOLDER, ROOT
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_full_fleet_victory_v654 import funds
from scripts.verify_village_wrap_v608 import read, save


def main():
    digest = sha(ROM.read_bytes())
    observed, shots, receipt = load(FOLDER, digest, 20600)
    normal, reference, baseline = load(CAP / 'refit_help_v712_yard', digest, 19700)
    assert observed['scripted_input_schedule'][:len(normal['scripted_input_schedule'])] == normal['scripted_input_schedule']
    assert len(reference) == 59 and all(shots[f].tobytes() == im.tobytes() for f, im in reference.items())
    source_ram = {r['frame']: r for r in normal['read_only_capture_RAM_snapshots']}
    actual_ram = {r['frame']: r for r in observed['read_only_capture_RAM_snapshots']}
    ram_pairs = []
    for frame, row in source_ram.items():
        other = actual_ram[frame]
        a, b = Path(row['path']).read_bytes(), Path(other['path']).read_bytes()
        assert row['sha256'] == sha(a) == other['sha256'] == sha(b) and a == b
        ram_pairs.append(frame)
    events = read(FOLDER / 'observer/events.json')
    assert not events['errors'] and not events['mismatches'] and events['all_host_slots_restored']
    rows = events['rows']
    assert [r['kind'] for r in rows] == ['layout_begin', 'native_new', 'layout_ready',
        'cleanup_begin', 'native_delete', 'cleanup_ready']
    begin, allocate, ready, cleanup, delete, cleared = rows
    assert allocate['R0'] == 9072 and allocate['LR'] == 0x02019F9C
    assert ready['header_words'][:3] == cleanup['header_words'][:3] == [4, 42, 108]
    pointer = ready['pixels']
    assert 0x02000000 <= pointer <= 0x02400000 - 9072
    assert cleanup['pixels'] == delete['R0'] == pointer and delete['LR'] == CLEANUP + 32
    assert ready['surface'] == cleanup['surface'] == cleared['surface'] == begin['surface']
    assert ready['surface_words'][10:12] == [168, 108]
    assert cleared['surface_words'][4] == 0
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    current, original = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    clean_arm = original.read_file('/__arm9__.bin')
    assert arm[0x5154:0x525C] == clean_arm[0x5154:0x525C]
    assert arm[0xD6E3C:0xD6E7C] == clean_arm[0xD6E3C:0xD6E7C]
    assert current.read_file('/COMMON/MESFILE.DK4') == NdsImage.open('out/all_routes_combined_v708_candidate.nds').read_file('/COMMON/MESFILE.DK4')
    for row in rows:
        raw = Path(row['RAM']).read_bytes()
        assert sha(raw) == row['RAM_sha256']
        assert sha(Path(row['DTCM']).read_bytes()) == row['DTCM_sha256']
        if row['kind'] in ('layout_ready', 'cleanup_begin'):
            assert sha(raw[pointer - 0x02000000:pointer - 0x02000000 + 9072]) == row['whole9072_pixel_bytes_sha256']
    last = actual_ram[20600]
    raw = Path(last['path']).read_bytes()
    ships, money = fleet_models(arm, raw, 1), funds(arm, raw)
    assert len(ships) == 5 and money == 25975
    save(ROOT / 'heap_proof.json', {'candidate': str(ROM), 'candidate_sha256': digest,
        'ordinary20600_frame_cold_boot_cancel_and_exit_no_gameplay_fixture': receipt,
        'normal19700_frame_baseline': baseline,
        'all59_whole_two_screen_RGB_pairs_and_full4MiB_capture_RAM_pairs_exact': ram_pairs,
        'original_native_new_and_delete_code_exact_to_clean': True,
        'original_allocator_size9072_actual_pointer': pointer,
        'six_actual_complete_lifetime_events': rows,
        'one_allocation_one_matching_free_and_header_pointer_cleared': True,
        'five_ships_and25975_funds_retained_after_explicit_cancel_and_exit': ships,
        'six_target_prefix_controls': str(ROOT / 'native_prefix_controls.json'),
        'observer_no_CPU_WRAM_DTCM_or_configuration_mutation_and_host_slots_restored': True,
        'normal_parent_repeated_entry_and_all31_separate_visits_not_claimed': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V713 actual new/free9072 bytes, native header cleared,59 whole RGB/RAM pairs and unchanged fleet/funds pass.', flush=True)


if __name__ == '__main__':
    main()
