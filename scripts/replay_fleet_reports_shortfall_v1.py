"""Exercise the original month-end shortfall on the copied regional fleet save."""

from inspect import getsource
from json import dumps, loads
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import native_finance_fixture_v615 as finance
from scripts import replay_fleet_reports_v1 as prior
from scripts.native_call_abi_v764 import call
from scripts.native_inventory_fixture_v481 import machine
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = prior.ROOT.with_name('regional_fleet_shortfall_replay')
TARGET = 100
PAUSE = 13200


def fund_company(arm, raw, target):
    proof = prior.base.load(prior.stage.PROOF)
    assert prior.base.sha256(arm).hexdigest() == proof['research_ARM9_sha256']
    clean = prior.base.NdsImage.open(prior.stage.first.review.CLEAN).read_file(prior.stage.first.ARM)
    assert len(raw) == 0x400000 and target == TARGET
    assert arm[0x3CC80:0x3CCDC] == clean[0x3CC80:0x3CCDC]
    assert arm[0x2DD68:0x2DE00] == clean[0x2DD68:0x2DE00]
    base = prior.stage.first.BASE
    cpu = machine(arm)
    cpu.mem_write(base, raw)

    def get(offset, *args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    text = unpack_from('<I', arm, 0x54450)[0] - base
    assert b'Would you like to hear them?' in raw[text:text + 128].split(b'\0', 1)[0]
    fleets = get(0xCB1A8)
    records = get(0x367FC, fleets + 4 + 57 * 132)
    expenses, income, invested = unpack_from('<3I', raw, records + 0xC - base)
    assert (expenses, income, invested) == (691, 0, 0)
    companies = get(0xCB160)
    company = companies + 4 + 76 * get(0x397D8, companies)
    before = get(0x3CCC8, company)
    assert before == 897400
    get(0x3CC80, company, (target - before) & 0xFFFFFFFF)
    assert get(0x3CCC8, company) == target
    after = bytes(cpu.mem_read(base, len(raw)))
    changes = [dict(address=base + i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert changes and all(company + 0xC <= row['address'] < company + 0x10 for row in changes)
    return after, dict(company=company, original_money_setter=base + 0x3CC80, before_funds=before,
        supplied_funds=target, original_regional_expenses=expenses, changes=changes)


def main():
    commands = [loads(line) for line in (prior.ROOT / 'commands.jsonl').read_text(encoding='utf-8').splitlines()]
    prefix = [row for row in commands if row.get('until', 999999) <= PAUSE]
    assert prefix[-1]['until'] == PAUSE and len(prefix) == 8
    replay = prefix + [
        dict(until=13600, buttons=['A'], duration=8, company_funds=TARGET),
        dict(until=14000, buttons=['A'], duration=8),
        dict(until=14400, buttons=['A'], duration=8),
        dict(stop=True),
    ]
    source = checked_text(getsource(prior.gameplay), {
        'commands.touch(exist_ok=False)': "commands.write_text(''.join(dumps(row) + '\\n' for row in replay), encoding='utf-8')",
        "'--pause-at', str(PAUSE), '--dump-pause-ram', '--dump-ram'":
            "'--pause-at', str(PAUSE), '--dump-pause-ram', '--dump-ram', '--allow-finance-fixtures'",
    })
    env = vars(prior) | {'ROOT': ROOT, 'replay': replay, 'dumps': dumps}
    exec(compile(source, __file__ + '::original-settlement-shortfall', 'exec'), env)
    old = finance.fund_company
    try:
        finance.fund_company = fund_company
        env['gameplay']()
    finally:
        finance.fund_company = old


if __name__ == '__main__':
    main()
