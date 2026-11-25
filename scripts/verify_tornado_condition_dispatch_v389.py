"""Original party-wide hazard callback with genuine captured data, isolated only."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import call, machine

ROOT = Path('work/analysis/condition_events_v389')
ROM = Path('out/all_routes_combined_v388_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    clean_rom = NdsImage.open('work/clean.nds')
    clean = clean_rom.read_file('/__arm9__.bin')
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    for lo, hi in [(0x65830, 0x65888), (0x65B08, 0x65C08), (0x72ED4, 0x72F38), (0x7E070, 0x7E108)]:
        assert arm[lo:hi] == clean[lo:hi]
    # The original tornado branch selects this descriptor and callback.
    assert struct.unpack_from('<I', clean, 0x73118)[0] == 0x02116FA0
    assert struct.unpack_from('<I', clean, 0x73120)[0] == 0x02065830
    entries = common_message_entries(clean_rom.read_file('/COMMON/MESFILE.DK4'), clean)
    ids = struct.unpack_from('<8I', clean, 0x116FA0)
    messages = [{'id': i, 'Japanese': entries[i].text.decode('cp932')} for i in ids if i < len(entries)]
    assert any('竜巻' in m['Japanese'] for m in messages)
    report_path = Path('work/emulation_v193/plaque_voyage_v379/capture_report.json')
    report = read(report_path)
    snapshot = report['read_only_RAM_snapshot']
    path = Path(snapshot['path'])
    ram = path.read_bytes()
    assert sha(ram) == snapshot['sha256'] and snapshot['read_only_export']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    u = machine(arm)
    u.mem_write(0x02000000, ram)
    # Adopt only the current reviewed lookup pointers after importing old globals.
    for row in read('translations/condition_labels_v1.json')['pointer_changes']:
        u.mem_write(0x02000000 + row['field'], struct.pack('<I', row['new_pointer']))
    actors = {}
    calls = []

    def observe(uc, address, size, _):
        if address != 0x02065830:
            return
        actor = uc.reg_read(UC_ARM_REG_R0)
        assert 0x02000000 <= actor < 0x02400000 - 32
        actors.setdefault(actor, bytes(uc.mem_read(actor, 32)))
        calls.append(actor)

    handle = u.hook_add(UC_HOOK_CODE, observe)
    try:
        call(u, 0x65B08, (0x02065830,))
    finally:
        u.hook_del(handle)
    assert actors
    cases = []
    for actor, before in actors.items():
        after = bytes(u.mem_read(actor, 32))
        expected = bytearray(before)
        if expected[6] == 0:
            expected[6] = 1
        if expected[7] <= 4:
            expected[7] = 5
        assert after == expected
        call(u, 0x7E0BC, (actor,))
        health_pointer = u.reg_read(UC_ARM_REG_R0)
        health = bytes(u.mem_read(health_pointer, 32)).split(b'\0', 1)[0].decode()
        call(u, 0x7E070, (actor,))
        mood_pointer = u.reg_read(UC_ARM_REG_R0)
        mood = bytes(u.mem_read(mood_pointer, 32)).split(b'\0', 1)[0].decode()
        assert after[7] == 5 and mood == 'Confused'
        cases.append({'actor_address': actor, 'old_health': before[6], 'old_mood': before[7],
                      'new_health': after[6], 'new_mood': after[7],
                      'native_health_text': health, 'native_mood_text': mood,
                      'only_original_condition_bytes_changed': True})
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'source_tornado_messages': messages, 'original_callback': 0x02065830,
             'original_whole_party_dispatcher': 0x02065B08, 'callback_invocations': calls,
             'genuine_snapshot_report': str(report_path), 'snapshot_sha256': sha(ram),
             'cases': cases, 'source_dispatch_and_getters_and_ABI_execute': True,
             'isolated_snapshot_and_current_lookup_fields_are_explicit_native_contracts': True,
             'not_live_emulator_injection_or_genuine_tornado_encounter': True,
             'actual_new_condition_display_still_pending': True,
             'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'party_dispatch_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Original tornado callback: {len(calls)} invocations/{len(cases)} genuine captured actors; complete native Confused lookup verified.')


if __name__ == '__main__':
    main()
