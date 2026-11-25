"""Source-bound Refit speaker, percentage and duration argument contracts."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R5, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_SP)

from dk4tool.patch.crew_role_labels import ORIGINAL
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_dialogue_v832')
ROM = Path('out/all_routes_combined_v831_candidate.nds')
LIVE = Path('work/emulation_v193/refit_editorial_v831_after')
TABLE = 0x02118680
IDS = tuple(range(1256, 1268))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'native_context.json').exists()
    rom, clean_rom = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, clean = rom.read_file('/__arm9__.bin'), clean_rom.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '3d6f3d28deedb42f9d5c333fd5a70b0722438f04e76a089b84672c2299c84d95'
    report = read(LIVE / 'capture_report.json')
    assert report['ROM_sha256'] == sha(ROM.read_bytes()) and report['frames'] == 20600
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 20000)
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and sha(raw) == snapshot['sha256']
    spans = ((0x17A7C, 0x17BA0), (0x17D70, 0x17D90), (0x53F4C, 0x53F9C),
             (0x118680, 0x1186A0), (0x7E988, 0x7E9A0))
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def text(pointer):
        assert BASE <= pointer < 0x02800000 - 256
        return bytes(u.mem_read(pointer, 256)).split(b'\0')[0]

    actors, hero = get(0xCB184), get(0x7F244)
    expected = (1256, 0xFFFFFFFF, 1257, 1258, 1259, 1260, 1261, 1262)
    assert struct.unpack('<8I', u.mem_read(TABLE, 32)) == expected
    voices = []
    for actor in range(208):
        obj = actors + 0x19E4 if actor == hero else actors + 4 + actor * 32
        voice = get(0x7E988, (obj,))
        selected = get(0x53F4C, (obj, TABLE))
        assert 0 <= voice < 8
        target = 1256 if expected[voice] == 0xFFFFFFFF else expected[voice]
        assert selected == target, (actor, hex(obj), voice, selected)
        voices.append({'actor_ID': actor, 'object': obj, 'voice': voice,
                       'message': selected, 'original_role_eligibility_not_inferred': True})
    assert get(0x53F4C, (0, TABLE)) == 1256
    controller = get(0xCB1A8) + 0x2090
    assigned = get(0x825E4, (controller, 13))
    helper = get(0x82428, (controller, 13))
    jp_pointer = struct.unpack_from('<I', clean, ORIGINAL - BASE + 13 * 4)[0]
    role_jp = clean[jp_pointer - BASE:].split(b'\0')[0].decode('cp932')
    label_slot = get(0x86314, (13,))
    role_en = text(struct.unpack('<I', u.mem_read(label_slot, 4))[0]).decode('ascii').strip()
    assert role_jp == '船大工' and role_en == 'Shipwright', (role_jp, role_en)
    role = {'role': 13, 'Japanese': role_jp, 'English': role_en,
            'current_assigned_actor_ID': assigned, 'original_assigned_object': helper,
            'source_assigned_getter': BASE + 0x82428, 'source_eligibility_function': BASE + 0x7E728,
            'minimum_native_ability': 25,
            'scope': 'The original event checks an assigned Shipwright and ability>=25. Actor voice lookup alone does not prove event eligibility.'}
    observed = []

    def intercept(uc, pc, size, unused):
        observed.append({'wrapper': pc, 'speaker_or_role': uc.reg_read(UC_ARM_REG_R0),
                         'message_or_table': uc.reg_read(UC_ARM_REG_R1),
                         'argument': text(uc.reg_read(UC_ARM_REG_R2)).decode('cp932') if pc == BASE + 0x53FE4 else None})
        if pc == BASE + 0x53FE4:
            uc.emu_stop()
        else:
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hooks = [u.hook_add(UC_HOOK_CODE, intercept, begin=BASE + p, end=BASE + p) for p in (0x53D44, 0x53FE4)]
    object_at = 0x02450000
    percentages, durations = [], []
    try:
        # Register/temporary-object cases begin after the original ability getter;
        # this is a source arithmetic/argument contract, not an actual offer.
        for ability in (25, 26, 39, 40, 49, 50, 99, 100, 199, 255):
            observed.clear()
            u.mem_write(object_at, bytes(0x198))
            u.mem_write(object_at + 0x190, struct.pack('<I', 100000))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R0, ability)
            u.reg_write(UC_ARM_REG_R7, 0)
            u.reg_write(UC_ARM_REG_R8, object_at)
            u.emu_start(BASE + 0x17AD0, STOP, count=100000)
            percent = ability // 5
            assert len(observed) == 2
            assert observed[0]['speaker_or_role'] == 13 and observed[0]['message_or_table'] == TABLE
            assert observed[1]['message_or_table'] == 1263 and observed[1]['speaker_or_role'] == 0
            assert observed[1]['argument'] == str(percent).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
            adjusted = struct.unpack('<I', u.mem_read(object_at + 0x190, 4))[0]
            assert adjusted == 100000 - 100000 * percent // 100
            percentages.append({'supplied_ability_result': ability, 'discount_percent': percent,
                                'original_100000_cost_after_discount': adjusted, 'calls': list(observed),
                                'synthetic_register_contract_not_actor_progress': True})
        for days in range(256):
            observed.clear()
            u.mem_write(object_at + 0x194, bytes([days]))
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_LR, STOP)
            u.reg_write(UC_ARM_REG_R7, 0)
            u.reg_write(UC_ARM_REG_R8, object_at)
            u.emu_start(BASE + 0x17B88, STOP, count=100000)
            assert len(observed) == 1 and observed[0]['message_or_table'] == 1267
            expected_days = str(days).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
            assert observed[0]['argument'] == expected_days
            durations.append({'temporary_duration_byte': days, 'original_argument': expected_days,
                              'message': 1267, 'argument_is_number_without_day_unit': True})
    finally:
        for hook in hooks:
            u.hook_del(hook)
    jp, en = common_message_entries(clean_rom.read_file('/COMMON/MESFILE.DK4'), clean), current_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm)
    packet = [{'message_id': i, 'source_hex': jp[i].text.hex(), 'Japanese': jp[i].text.decode('cp932'),
               'source_reference': vars(jp[i]) | {'text': jp[i].text.hex()},
               'current_hex': en[i].text.hex(), 'current_English': en[i].text.decode('cp932'),
               'current_reference': vars(en[i]) | {'text': en[i].text.hex()}} for i in range(1245, 1291)]
    save(ROOT / 'source_context_packet.json', {'source_ROM_sha256': sha(Path('work/clean.nds').read_bytes()),
                                               'current_ROM': str(ROM), 'current_ROM_sha256': sha(ROM.read_bytes()),
                                               'neighbors': packet})
    save(ROOT / 'native_context.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'current_ARM9_sha256': sha(arm),
        'source_ARM9_sha256': sha(clean), 'actual_RAM_source': snapshot,
        'source_code_spans_equal': [{'start': lo, 'end': hi, 'sha256': sha(arm[lo:hi])} for lo, hi in spans],
        'role': role, 'original_voice_table': list(expected), 'all208_native_voice_selections': voices,
        'null_actor_default': 1256, 'voice_class1_original_missing_slot_falls_back_to_first_valid1256': True,
        'percentage_argument_contracts': percentages, 'all256_duration_byte_argument_contracts': durations,
        'source_IC_meaning': 'Character-dependent first-person pronoun. Clean53914 selects 僕 or アタシ via the speaker predicate;English I is grammatical localization,not a removed actor name.',
        'prior_IC_native_evidence': 'scripts/review_shipyard_editorial_v759.py:original53914 source/current native expansion cases',
        'existing_actual_1266_reference': str(LIVE / 'frame_020000_cold_boot.png'),
        'new_offer_or_rename_or_discount_activation_not_claimed': True,
        'duration_unit_and_new_family_formatting_integration_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V832 source/native context:208 voice selections,10 discount cases,256 duration arguments;no ROM edits or completion credit.', flush=True)


if __name__ == '__main__':
    main()
