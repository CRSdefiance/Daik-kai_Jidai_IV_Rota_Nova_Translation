"""User-authorized test crew refill; ten live bytes, persisted models unchanged."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_hot_spring_resilient_v1644 as previous
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROM = previous.ROM
REQUEST = {'testing_crew': 'restore_original_persisted_five_ship_counts'}
ROOT = Path('work/analysis/hot_spring_crew_fixture_v1650')


def apply_fixture(arm, raw, request):
    if request != REQUEST:
        return previous.apply_fixture(arm, raw, request)
    assert len(raw) == 0x400000
    assert sha(arm) == read('translations/hot_spring_notice_editorial_release_v1.json')['target_arm9_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0x5543C, 0x55454), (0x181B4, 0x181C4), (0x18398, 0x183A8), (0x36C70, 0x36CB8)]:
        assert arm[lo:hi] == clean[lo:hi]
    assert arm[0x55444:0x5544C] == bytes.fromhex('ba01d0e11eff2fe1')
    cpu, get = get_machine(arm, raw)
    assert get(0x2E58C) == get(0x7F244) == 1
    fleet = get(0xCB1A8) + 4 + 132
    assert struct.unpack('<3I', cpu.mem_read(get(0x3F0F8) + 8, 12)) == (0, 0, 0)
    after = bytearray(raw)
    owned, ships = set(), []
    for slot in range(5):
        mobile = get(0x36C70, fleet + 12 + 8 * slot)
        model = get(0x36C94, fleet + 12 + 8 * slot)
        assert mobile and model and get(0x564C8, mobile)
        hull, count = get(0x5543C, mobile), get(0x55444, mobile)
        persisted = [get(0x183A0, model), get(0x181BC, model)]
        assert persisted == ([60, 49] if slot == 0 else [25, 19])
        assert 0 < hull <= persisted[0] and 0 <= count <= persisted[1]
        address = mobile + 0x1A
        after[address - 0x02000000:address - 0x02000000 + 2] = struct.pack('<H', persisted[1])
        owned.update(range(address, address + 2))
        ships.append({'slot': slot, 'mobile': mobile, 'model': model, 'hull_unchanged': hull,
                      'before_crew': count, 'after_crew': persisted[1], 'unchanged_persisted_Hull_Crew': persisted})
    after = bytes(after)
    changes = [{'address': 0x02000000 + i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert len(owned) == 10 and changes and all(c['address'] in owned for c in changes)
    check, query = get_machine(arm, after)
    assert [query(0x55444, s['mobile']) for s in ships] == [49, 19, 19, 19, 19]
    return after, {'context': 'user_authorized_artificial_live_test_crew_refill', 'owned_bytes': sorted(owned),
                   'changes': changes, 'ships': ships, 'fleet': fleet,
                   'original_getter_55444_proves_live_crew_ushort_at_mobile_plus1A': True,
                   'targets_from_original_persisted_counts_not_guessed_maxima': True,
                   'only_ten_live_crew_bytes_changed_persisted_models_and_hull_exact': True,
                   'all_other4MiB_including_positions_fatigue_actor_skills_RNG_and_event_outcomes_exact': True,
                   'no_earned_recruitment_health_travel_or_original_save_change_claim': True,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
                   'fixture_sha256': sha(Path(__file__).read_bytes())}


if __name__ == '__main__':
    assert not ROOT.exists()
    raw = Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_resilient_v1645_1637/frame_042673_arm9_ram.bin').read_bytes()
    after, proof = apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'), raw, REQUEST)
    ROOT.mkdir(parents=True)
    save(ROOT / 'ten_byte_crew_refill_preflight.json', proof)
    print('Ten live crew bytes only:71 to125;persisted models,hull,skills,RNG,event outcomes and all other RAM unchanged.')
