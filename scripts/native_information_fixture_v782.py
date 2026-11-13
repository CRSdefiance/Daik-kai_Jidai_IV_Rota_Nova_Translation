"""Two town-information bits through the original setters; no dialogue injection."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.native_recruit_shortfall_fixture_v782 import ARMS, BASE
from scripts.native_warning_fixture_v782_v3 import set_condition as qualify


def set_condition(arm, raw, request):
    if request == {'mode': 'enable-schemes'}:
        return qualify(arm, raw, request)
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request != {'mode': 'missing-contract-information'}:
        raise ValueError('Exact V780/V782 and declared missing-contract-information state required')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0xB50B8, 0xB50E4), (0x57068, 0x57104), (0x56F14, 0x56FCC)):
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def candidates(faction):
        count = get(0x57068, (faction, 0x02479000))
        assert count <= 90
        return list(struct.unpack('<'+'I'*count, u.mem_read(0x02479000, count*4))) if count else []

    assert get(0xB65E4) == 22
    assert candidates(0) == [11, 12] and candidates(9) == [19, 22]
    towns = get(0xCB178)
    fields = []
    for index in (11, 12):
        obj = towns+4+index*108
        assert get(0xB50D8, (obj,)) == 2
        before = struct.unpack('<H', u.mem_read(obj+8, 2))[0]
        get(0xB50B8, (obj, 0))
        after = struct.unpack('<H', u.mem_read(obj+8, 2))[0]
        assert after == before & ~2 and get(0xB50D8, (obj,)) == 0
        fields.append({'town_ID': index, 'address': obj+8, 'before': before, 'after': after})
    assert candidates(0) == [] and candidates(9) == [19, 22]
    result = bytearray(raw)
    owned = set()
    for field in fields:
        at = field['address']-BASE
        result[at:at+2] = struct.pack('<H', field['after'])
        owned.update((at, at+1))
    changed = [i for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert set(changed) <= owned and len(changed) == 2
    return bytes(result), {
        'synthetic_missing_contract_information_fixture': True, 'mode': request['mode'], 'ARM9_sha256': sha(arm),
        'two_declared_town_flag_halfwords': fields, 'only_bit1_cleared': True,
        'original_setter': BASE+0xB50B8, 'original_information_getter': BASE+0xB50D8,
        'original_town_candidate_provider': BASE+0x57068,
        'Castor_before_towns': [11, 12], 'Castor_after_towns': [], 'Pasha_towns_unchanged': [19, 22],
        'changes': [{'address': BASE+i, 'before': raw[i], 'after': result[i]} for i in changed],
        'all_other4MiB_bytes_exact': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(result),
        'cash_contract_shares_cargo_location_code_menu_flags_and_original_saves_unchanged': True,
        'no_normal_information_loss_or_earned_progress_claim': True}
