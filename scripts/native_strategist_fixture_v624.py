"""Source-bound isolated Chart Room/Gerhard assignment for hidden Tavern UI."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ARM = '9a05ef9a25367d53dc7affa1c24e70b84fa9123388701adefcf94e0d21add280'
TARGET = 'e7c4e62f4fe5b621b1d4bed2123ab26d033698237e47b4b425e6fc9176a5b5a0'
CONTEXT = '98b57756ef56ef0cebf6c5ee7b1b18a45c56b1809cec81561253fe04f3457a01'
QUEUED = '282ef872ceb9fbf9f0c27a8c315f4ea403f0e68746c5c1c7f3883e63df923651'


def assign(arm, raw, request):
    if sha(arm) not in (ARM, TARGET, CONTEXT, QUEUED) or len(raw) != 0x400000 or request is not True:
        raise ValueError('Strategist fixture requires exact V623/V624/V625/V626,4MiB RAM and true')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x7B60, 0x7C34), (0x132C0, 0x132CC), (0x825E4, 0x8261C),
                   (0x829C8, 0x82A44), (0x82BC4, 0x82BD0), (0x82E04, 0x82E2C)):
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    root = get(0xCB1A8)
    assert get(0x2E58C) == 1
    controller = root + 0x2090
    assert get(0x825E4, (controller, 2)) == 208
    model = get(0x82E04, (controller,))
    assert bytes(u.mem_read(model + 8, 24)).split(b'\0')[0] == b'Vestaros'
    assert get(0x7B60, (2,)) == 19
    assert get(0x132C0, (model, 18)) == 24
    assert get(0x82BC4, (controller, 18)) == 208
    assert get(0x82BC4, (controller, 21)) == 16
    actor = get(0xCB184) + 4 + 16 * 32
    vt = struct.unpack('<I', u.mem_read(actor, 4))[0]
    name = get(struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0] - BASE, (actor,))
    assert bytes(u.mem_read(name, 24)).split(b'\0')[0] == b'Gerhard'
    before_skill = get(0x7DD38, (actor, 7, 6))
    changes = [
        {'address': model + 0x1E + 18, 'before': 24, 'after': 19},
        {'address': controller + 6 + 21, 'before': 16, 'after': 208},
        {'address': controller + 6 + 18, 'before': 208, 'after': 16}]
    after = bytearray(raw)
    for row in changes:
        assert after[row['address'] - BASE] == row['before']
        after[row['address'] - BASE] = row['after']
    u.mem_write(BASE, bytes(after))
    assert get(0x825E4, (controller, 2)) == 16
    assert get(0x7DD38, (actor, 7, 6)) == before_skill
    return bytes(after), {
        'synthetic_strategist_room_assignment_fixture': True, 'controller': controller,
        'source_named_model': model, 'crew_member': 'Gerhard', 'actor': actor,
        'old_room': 21, 'new_room': 18, 'new_room_type': 19,
        'original_Strategist_getter': 0x020825E4, 'original_getter_after_assignment': 16,
        'unchanged_original_submenu_skill': before_skill, 'changes': changes,
        'only_three_declared_room_type_and_assignment_bytes_changed': True,
        'code_inventory_stats_money_location_other_bytes_unchanged': True,
        'earned_qualifications_refit_or_assignment_not_claimed': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm)}


def assign_expert(arm, raw, request):
    """Assign Gerhard, increase one XP counter, and move the calendar three days.

    The original menu eligibility code still makes every availability decision.
    This is an isolated testing cheat, not earned progress or a valid saved route.
    """
    after, proof = assign(arm, raw, request)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x7E668, 0x7E678), (0x7E728, 0x7E750), (0x7DD38, 0x7DE20),
                   (0xCC9C8, 0xCCA30), (0x567CC, 0x56990), (0x571E0, 0x572C8)):
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    u.mem_write(BASE, after)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    actor = proof['actor']
    calendar = get(0xCB1B4)
    assert get(0x7E670, (actor,)) == 11209
    assert get(0x7E668, (actor,)) == 12211
    assert get(0x7E728, (actor,)) == 39
    assert struct.unpack('<I', u.mem_read(calendar + 8, 4))[0] == 26877
    result = bytearray(after)
    for address, before, target in ((actor + 16, 11209, 250000), (calendar + 8, 26877, 27021)):
        old, new = struct.pack('<I', before), struct.pack('<I', target)
        for i in range(4):
            assert result[address - BASE + i] == old[i]
            proof['changes'].append({'address': address + i, 'before': old[i], 'after': new[i]})
            result[address - BASE + i] = new[i]
    u.mem_write(BASE, bytes(result))
    assert get(0x7E670, (actor,)) == 250000
    assert get(0x7E668, (actor,)) == 12211
    level = get(0x7E728, (actor,))
    skill = get(0x7DD38, (actor, 7, 6))
    speech = get(0x7DCC8, (actor, 8))
    assert (level, skill, speech) == (111, 206, 201)
    # Native calendar decoder: month, day, within-day tick.
    out = 0x02450000
    get(0xCC9C8, (calendar, out, out + 4, out + 8))
    date = list(struct.unpack('<3I', u.mem_read(out, 12)))
    assert date == [6, 16, 45]
    proof.update({
        'synthetic_experience_and_calendar_fixture': True,
        'one_experience_counter_before': 11209, 'one_experience_counter_after': 250000,
        'calendar_ticks_before': 26877, 'calendar_ticks_after': 27021,
        'calendar_days_advanced': 3, 'original_zero_based_month_day_and_tick_after': date,
        'original_level_after': level, 'original_submenu_skill_after': skill,
        'original_Speech_skill_after': speech,
        'only_three_declared_room_type_and_assignment_bytes_changed': False,
        'code_inventory_stats_money_location_other_bytes_unchanged': False,
        'only_three_room_bytes_one_XP_word_and_one_calendar_word_changed': True,
        'attributes_health_goods_funds_location_menu_flags_outcomes_code_unchanged': True,
        'earned_experience_time_refit_assignment_or_campaign_progress_not_claimed': True,
        'after_RAM_sha256': sha(result)})
    return bytes(result), proof
