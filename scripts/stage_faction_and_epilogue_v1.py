"""Stage the seven shared notices and verify complete original panel layouts."""

import inspect
from pathlib import Path
import struct

from dk4tool.patch.faction_and_epilogue_wrap_v1 import transform
from scripts import stage_discovery_rewards_v1 as previous
from scripts.register_discovery_rewards_v1 import RELEASE
from scripts.review_faction_and_epilogue_v1 import OUTPUT as MANUSCRIPT
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/faction_and_epilogue_staged_20261111_v1')
ROM = ROOT / 'faction_and_epilogue_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
RETAIN_STORED = {334, 343}
AMENDMENTS = {}


def active_rows(manuscript):
    return {row['message_ID']: row for row in manuscript['records']}


def storage_text(rows):
    return {n: (row['current_English'] if n in RETAIN_STORED else row['english']).encode('ascii')
            for n, row in rows.items()}


def dynamic_samples(ctx):
    towns, actors = previous.fleet.name_samples(ctx)
    town_names = [row['text'] for row in towns]
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)

    def word(at):
        return struct.unpack('<I', cpu.mem_read(at, 4))[0]

    def text(ptr):
        return bytes(cpu.mem_read(ptr, 96)).split(b'\0', 1)[0].decode('cp932')

    root = get(0xCB160)
    factions = []
    for number in range(21):
        obj = root + 4 + 76 * number
        name = text(get(word(word(obj) + 8) - previous.BASE, obj))
        if name:
            factions.append(name)
    assert len(factions) == 20 and get(0x397D8, root) == 3
    captains = [text(get(0x7EA8C, ctx.actor_root + 4 + 32 * index)) for index in range(4)]
    assert text(get(0x7EA8C, ctx.actor_root + 0x19E4)) == captains[3]
    assert [name.split()[0] for name in captains] == ['Rafael', 'Hodram', 'Lil', 'Maria']
    given = [row['given'] for row in actors if row['given']]
    ctx.calls.clear()
    longest_town = max(town_names, key=lambda name: len(name.encode('cp932')))
    longest_faction = max(factions, key=lambda name: len(name.encode('cp932')))
    longest_given = max(given, key=lambda name: len(name.encode('cp932')))
    crew_names = [(name,) for name in ('Gerhard', 'Manuel', longest_given)]
    return {
        334: [('Lisbon', 'Clifford'), ('Amsterdam', 'Hayreddin Clan'), (longest_town, longest_faction)],
        335: crew_names,
        337: [(name,) for name in ('Pasha', 'Li Clan', longest_faction)],
        342: [(factions[index], captain) for index, captain in zip((0, 2, 1, 3), captains, strict=True)],
    }, dict(towns=town_names, factions=factions, original_given_name_cases=given,
            original_composed_captain_names=captains, current_native_captain=3)


def render_cases(ctx, clone, rows, storage, samples):
    code = checked_text(inspect.getsource(previous.render_cases), {
        'wrapper = RAW_NOTICE if n == 341 else target':
            "wrapper = row['native_callers'][0].get('raw_notice_wrapper', target)",
        "            if n in RETAIN_STORED:\n                before = run(ctx, source, args)\n"
        "                ctx.calls.clear()\n                assert before['native_wrapper_output_hex'] == result['native_wrapper_output_hex']":
            "            if n in RETAIN_STORED:\n                before = run(ctx, source, args)\n"
            "                ctx.calls.clear()\n                result['previous_native_lines'] = before['native_wrapper_lines']\n"
            "                result['retained_prose_layout_changed'] = before['native_wrapper_output_hex'] != result['native_wrapper_output_hex']",
    })
    env = {**vars(previous), **globals()}
    exec(compile(code, __file__ + '::actual-epilogue-and-raw-notice', 'exec'), env)
    return env['render_cases'](ctx, clone, rows, storage, samples)


def stage():
    sheets = previous.FunctionType(previous.save_sheets.__code__, vars(previous) | {'ROOT': ROOT})
    env = {**vars(previous), **globals(), 'save_sheets': sheets}
    exec(compile(inspect.getsource(previous.stage), __file__ + '::same-41-block-storage-and-parent-inverse', 'exec'), env)
    env['stage']()


if __name__ == '__main__':
    stage()
