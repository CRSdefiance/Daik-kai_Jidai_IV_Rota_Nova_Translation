"""Execute the original monthly Golden Route caller with bounded offline route records."""

from struct import pack
from unicodedata import normalize

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from scripts import stage_golden_route_exchanges_v1 as stage


BASE, STACK, STOP = stage.BASE, stage.STACK, stage.STOP
TABLE, SEASON, DISPATCH = 0x0237455C, 0x020C4D14, 0x020DAD20
MODAL, FLAGS, DATE = 0x020546B8, 0x02279862, 0x02470000
OUTPUT = stage.ROOT / 'original_monthly_payout.json'
CASES = (
    ('eligible', 2, ((3, 24, 11, 71, 7),), 60, ((3, 23),)),
    ('not_an_arrival_month', 1, ((3, 24, 11, 71, 7),), 0, ((3, 23),)),
    ('not_reported', 2, ((2, 24, 11, 71, 7),), 0, ((2, 24),)),
    ('final_month', 2, ((3, 1, 11, 71, 7),), 60, ((4, 0),)),
    ('sum_only_eligible_goods', 1, ((3, 24, 11, 71, 7), (3, 24, 7, 157, 0)), 150, ((3, 23), (3, 23))),
    ('sum_two_eligible_goods', 2, ((3, 24, 11, 71, 7), (3, 24, 7, 157, 0)), 210, ((3, 23), (3, 23))),
)


def main():
    assert not OUTPUT.exists()
    base, review = stage.base, stage.review
    parent = base.load(review.parent.RELEASE)
    rt = base.RegisteredRuntime(review.parent.RELEASE, parent['own_registered_startup'], captain=3)
    draft, proof = map(base.load, (stage.OUTPUT, stage.PROOF))
    assert rt.receipt() == draft['registered_input'] == proof['registered_input']
    assert base.digest(stage.ROM) == proof['research_ROM_sha256']
    rom = review.parent.base.NdsImage.open(stage.ROM)
    arm, common = rom.read_file(stage.ARM), rom.read_file(stage.COMMON)
    clean = review.parent.base.NdsImage.open(review.CLEAN).read_file(stage.ARM)
    for first, last in ((0xDAD20, 0xDAE00), (0xABF50, 0xABF80)):
        assert arm[first:last] == rt.arm[first:last] == clean[first:last]
    ctx = stage.fleet.portrait.with_components(rt, arm, common)
    row = next(case for case in proof['records'] if case['message_ID'] == 3392)
    observations = []
    for label, month, routes, amount, remaining in CASES:
        cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
        assert all(not bytes(cpu.mem_read(TABLE + index * 28, 1))[0] for index in range(77))
        assert get(SEASON - BASE, 7, month) == int(month == 2)
        assert get(SEASON - BASE, 0, month) == 1
        for i, (state, time, purchase, sale, area) in enumerate(routes):
            cpu.mem_write(TABLE + i * 28, pack('<7I', state | (time << 8), purchase, sale, 11, 12, 13 + i, area))
        cpu.mem_write(DATE, pack('<3I', 0, 0, month - 1))
        cpu.mem_write(FLAGS, b'\x01')
        notices = []

        def stop(u, pc, size, _):
            number = u.reg_read(UC_ARM_REG_R0)
            pointer = u.reg_read(UC_ARM_REG_R1)
            raw = bytes(u.mem_read(pointer, 64)).split(b'\0', 1)[0]
            assert number == 3392
            notices.append(raw)
            u.emu_stop()

        cpu.hook_add(UC_HOOK_CODE, stop, begin=MODAL, end=MODAL)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.reg_write(UC_ARM_REG_R0, DATE)
        cpu.emu_start(DISPATCH, STOP, count=3000000)
        assert tuple(tuple(cpu.mem_read(TABLE + i * 28, 2)) for i in range(len(routes))) == remaining
        assert cpu.reg_read(UC_ARM_REG_PC) == (MODAL if amount else STOP)
        assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
        assert SEASON in provider.executed_current if any(state == 3 for state, *_ in routes) else not notices
        ctx.calls.clear()
        displayed = None
        if amount:
            native, = notices
            assert normalize('NFKC', native.decode('cp932')) == str(amount)
            template = bytes.fromhex(row['staged_hex'])
            displayed = stage.modal_case(ctx, template, native)['display']
            assert displayed == template % (native,)
        else:
            assert not notices
        observations.append(dict(case=label, original_month=month, supplied_records=routes,
            original_qualifying_profit=amount, remaining_state_and_months=remaining,
            native_display_hex=displayed.hex() if displayed else None))
    base.save(OUTPUT, dict(candidate_sha256=proof['research_ROM_sha256'], source_caller=DISPATCH,
        source_calendar_check=SEASON, original_modal=MODAL, observations=observations,
        original_month_counter_and_season_gate_preserved=True,
        offline_only=True, actual_payment_or_save_progress=False))
    print('Verified six native payout cases, including season, reported state, expiry and aggregate amount.')


if __name__ == '__main__':
    main()
