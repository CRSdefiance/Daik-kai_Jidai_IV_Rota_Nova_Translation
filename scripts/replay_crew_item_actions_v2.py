"""Verify successful remedy use with an existing crew member moved to the vacant cabin."""

from inspect import getsource
from struct import unpack

from unicorn.arm_const import UC_ARM_REG_R0

from scripts import replay_crew_item_actions_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = prior.ROOT.with_name('focused_item_use_success')
COMMANDS = (
    dict(until=8700, inventory_items=[23], buttons=['X'], duration=8),
    dict(until=9000, touch=[161, 45], duration=8),
    dict(until=9300, buttons=['A'], duration=8),
    dict(until=9800, condition_fixture={'event': 'remedy-condition'}, buttons=['Y'], duration=8),
    dict(until=10100, buttons=['A'], duration=8),
    dict(until=10400, buttons=['B'], duration=8),
    dict(until=10700, buttons=['B'], duration=8),
    dict(stop=True),
)


def set_condition(arm, raw, request):
    after_condition, proof = prior.set_condition(arm, raw, request)
    base = prior.inventory.BASE
    clean = prior.base.NdsImage.open(prior.stage.first.review.CLEAN).read_file(prior.stage.first.ARM)
    for lo, hi in ((0x8261C, 0x82640), (0x82A88, 0x82AE4), (0x82BB8, 0x82BD0)):
        assert arm[lo:hi] == clean[lo:hi]
    cpu = prior.inventory.machine(arm)
    cpu.mem_write(base, after_condition)

    def get(offset, *args):
        prior.call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    fleet, actor, remedy_cabin, previous_cabin = proof['fleet'], 16, 20, 21
    out = 0x02470000
    assert get(0x82A88, fleet, remedy_cabin, out, out + 4)
    assert unpack('<2I', cpu.mem_read(out, 8)) == (208, 14)
    assert get(0x82A88, fleet, previous_cabin, out, out + 4)
    assert unpack('<2I', cpu.mem_read(out, 8)) == (actor, 15)
    assert get(0x8261C, fleet, 14) == 208
    get(0x82BB8, fleet, previous_cabin, 208)
    get(0x82BB8, fleet, remedy_cabin, actor)
    assert get(0x8261C, fleet, 14) == actor and get(0x8261C, fleet, 15) == 208
    after = bytes(cpu.mem_read(base, len(raw)))
    assignment = [dict(address=base + i, before=a, after=b)
                  for i, (a, b) in enumerate(zip(after_condition, after, strict=True)) if a != b]
    assert {row['address'] for row in assignment} == {fleet + 6 + remedy_cabin, fleet + 6 + previous_cabin}
    proof['changes'].extend(assignment)
    return after, proof | dict(cabin_assignment=dict(actor=actor, from_cabin=previous_cabin,
        to_cabin=remedy_cabin, destination_cabin_type=14, original_setter=base + 0x82BB8))


def main():
    source = checked_text(getsource(prior.gameplay), {
        "commands.write_text(json.dumps(dict(until=8700, inventory_items=[ITEM], buttons=['X'], duration=8)) + '\\n',\n"
        "                        encoding='utf-8')":
            "commands.write_text(''.join(json.dumps(row) + '\\n' for row in COMMANDS), encoding='utf-8')",
        'from scripts.replay_crew_item_actions_v1 import set_condition':
            'from scripts.replay_crew_item_actions_v2 import set_condition',
    })
    env = vars(prior) | globals() | {'prior': prior.prior}
    exec(compile(source, __file__ + '::successful-item-use', 'exec'), env)
    env['gameplay']()


if __name__ == '__main__':
    main()
