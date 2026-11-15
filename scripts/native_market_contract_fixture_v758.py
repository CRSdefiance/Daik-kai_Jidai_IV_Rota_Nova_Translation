"""Declared facility selector or Gerhard/share/XP fixtures for actual dialogue."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.review_market_contract_v758 import ROOT
from scripts.verify_village_wrap_v608 import read


def assign(arm, raw, request):
    proof = read(ROOT / 'native_review_RESEARCH.json')
    original = NdsImage.open('out/all_routes_combined_v757_candidate.nds').read_file('/__arm9__.bin')
    assert sha(arm) in (sha(original), proof['target_ARM9_sha256']) and len(raw) == 0x400000
    assert request in ({'mode': 'governor'}, {'mode': 'advice'})
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(f, args=()):
        call(u, f, args)
        return u.reg_read(UC_ARM_REG_R0)
    town = get(0xB6618)
    assert get(0xB65E4) == 22 and get(0xB4A88, (town,)) == 0
    fields = []
    if request['mode'] == 'governor':
        assert get(0xB507C, (town, 6)) == 64
        fields.append((town + 12, bytes((raw[town + 12 - BASE] & ~64,)), 'clear only native Palace facility selector bit6'))
    else:
        for lo, hi in ((0x825E4, 0x8261C), (0x829C8, 0x82A44), (0x7DD38, 0x7DE20), (0xBAA74, 0xBAB3C)):
            assert arm[lo:hi] == original[lo:hi]
        root = get(0xCB1A8)
        controller = root + struct.unpack_from('<I', arm, 0xBAB34)[0]
        model = get(0x82E04, (controller,))
        assert bytes(u.mem_read(model + 8, 24)).split(b'\0')[0] == b'Vestaros'
        assert get(0x825E4, (controller, 3)) == 208 and get(0x7B60, (3,)) == 20
        assert get(0x132C0, (model, 18)) == 24 and get(0x82BC4, (controller, 21)) == 16
        assert get(0x82BC4, (controller, 18)) == 208
        actor = get(0xCB184) + 4 + 16 * 32
        vt = struct.unpack('<I', u.mem_read(actor, 4))[0]
        name = get(struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0] - BASE, (actor,))
        assert bytes(u.mem_read(name, 24)).split(b'\0')[0] == b'Gerhard'
        assert get(0x7DD38, (actor, 4, 20)) == 149
        assert raw[town + 0x12 - BASE:town + 0x14 - BASE] == bytes((21, 0))
        fields += [(model + 0x1E + 18, bytes((20,)), 'existing empty room18 type for native role3'),
                   (controller + 6 + 21, bytes((208,)), 'remove Gerhard from old room21'),
                   (controller + 6 + 18, bytes((16,)), 'assign Gerhard to original role3 room'),
                   (actor + 16, struct.pack('<I', 250000), 'one Gerhard experience counter'),
                   (town + 0x12, bytes((2, 1)), 'unused company/share pair')]
    after, changes = bytearray(raw), []
    for address, payload, field in fields:
        for k, value in enumerate(payload):
            at = address + k - BASE
            if after[at] != value:
                changes.append({'address': BASE + at, 'before': after[at], 'after': value, 'field': field})
                after[at] = value
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == len(changes)
    u.mem_write(BASE, bytes(after))
    if request['mode'] == 'governor':
        assert len(changes) == 1 and get(0xB507C, (town, 6)) == 0
        state = {'native_facility_flag6_after': 0}
    else:
        assert get(0x825E4, (controller, 3)) == 16
        assert get(0x7DD38, (actor, 4, 20)) == 226 and get(0xB4A88, (town,)) == 1
        assert get(0xBAA74, (0x02450000,)) == 1
        voice = get(0x7E988, (actor,))
        state = {'original_extra_stock_predicate_after': 1, 'native_role3_actor': 16,
                 'source_ability4_20_after': 226, 'native_voice_index': voice,
                 'expected_message': 754 if voice in (0, 1) else 753 + voice}
    return bytes(after), {'synthetic_contract_or_advice_fixture': True, 'mode': request['mode'],
        'changes': changes, 'original_town22': True, **state,
        'all_other4MiB_RAM_bytes_exact': True, 'no_earned_contract_share_role_experience_or_advice_creation_claim': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
        'fixture_source_sha256': sha(Path(__file__).read_bytes())}
