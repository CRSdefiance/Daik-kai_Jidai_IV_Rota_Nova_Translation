"""Run the current original modal wrappers on source-reviewed fleet and yard prose."""

import struct
from collections import Counter
from pathlib import Path

from scripts import preflight_setup_save_equipment_v1 as modal
from scripts.register_setup_save_equipment_v1 import RELEASE
from scripts.review_shipyard_fleet_setup_v1 import OUTPUT


ROOT = Path('work/SharedText_20261110_v1/shipyard_fleet_setup_preflight_v1')
PROOF = ROOT / 'preflight.json'


def name_samples(ctx):
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)

    def word(address):
        return struct.unpack('<I', cpu.mem_read(address, 4))[0]

    def label(obj, offset):
        getter = word(word(obj) + offset)
        pointer = get(getter - 0x02000000, obj)
        text = bytes(cpu.mem_read(pointer, 96)).split(b'\0', 1)[0].decode('cp932')
        return text, getter

    town_root = get(0xCB178) + 4
    towns = []
    for index in range(90):
        text, getter = label(town_root + index * 108, 8)
        assert text
        towns.append(dict(town_ID=index, text=text, getter=getter))
    actors = []
    for index in range(4, 114):
        given, surname = (label(ctx.actor_root + 4 + index * 32, field) for field in (0x20, 0x24))
        actors.append(dict(actor_ID=index, given=given[0], surname=surname[0], getters=[given[1], surname[1]]))
    ctx.calls.clear()
    return towns, actors


def variants(towns, actors):
    by_name = {row['text'] for row in towns}
    assert {'Lisbon', 'Santo Domingo'} <= by_name
    longest_towns = sorted((name for name in by_name if name.isascii()), key=lambda name: (len(name), name))
    pairs = {(row['given'], row['surname']) for row in actors if row['given'] and row['surname']
             and row['given'].isascii() and row['surname'].isascii()}
    ranked = sorted(pairs, key=lambda pair: (sum(map(len, pair)), pair))
    manuel, = (pair for pair in pairs if pair[0] == 'Manuel')
    return {261: [(value,) for value in dict.fromkeys(('Lisbon', 'Santo Domingo', longest_towns[-1]))],
            279: list(dict.fromkeys((ranked[0], manuel, ranked[-1], ranked[-2])))}


def main():
    assert not ROOT.exists()
    release = modal.load(RELEASE)
    ctx = modal.RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    manuscript = modal.load(OUTPUT)
    assert manuscript['registered_predecessor_sha256'] == ctx.release['candidate_sha256']
    towns, actors = name_samples(ctx)
    samples = variants(towns, actors)
    raster, _, meta = modal.font_tools(ctx.image)
    font = modal.GameAsciiFont.from_arm9(ctx.arm)
    checks = []
    for row in manuscript['records']:
        n = row['message_ID']
        for args in samples.get(n, [()]):
            assert len(args) == row['native_substitution_count']
            case, _ = modal.check_modal(ctx, row, args, raster, font)
            checks.append(case)
    ROOT.mkdir()
    holds = Counter(case['message_ID'] for case in checks if case.get('native_layout_pending'))
    modal.save(PROOF, dict(registered_input=ctx.receipt(), current_modal_cases=checks,
        current_native_town_names=towns, current_native_given_and_surnames=actors, focused_arguments=samples,
        dynamic_layout_holds=dict(holds), font_contract=meta, exact_proposed_prose_not_yet_stored=True,
        new_credit=0, full_goal_complete=False,
        evidence={str(path): modal.digest(path) for path in (OUTPUT, RELEASE, Path(__file__))}))
    print(f'{len(checks)} proposed native expansions, layout holds {dict(holds)}.')


if __name__ == '__main__':
    main()
