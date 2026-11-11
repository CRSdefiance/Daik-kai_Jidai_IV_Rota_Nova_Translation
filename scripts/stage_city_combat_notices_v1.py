"""Verify the original combat portraits and the scoped spoils digit rendering."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import review_city_combat_notices_v1 as review
from scripts import stage_fleet_reports_v1 as first
from scripts import stage_fleet_reports_v2 as prior
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/city_combat_notices_staged_20261111_v1')
ROM, PROOF = ROOT / 'city_combat_notices_RESEARCH_ONLY.nds', ROOT / 'stored_verification.json'
OUTPUT = review.OUTPUT
AMOUNT_TABLES = (0x02116940,)
PHRASES = {}


def stage(runtime, release, rows, groups, verified=None):
    assembler = FunctionType(prior.install_in_scoped_assembly.__code__, vars(prior) | {'AMOUNT_TABLES': AMOUNT_TABLES})
    env = vars(prior) | {
        'first': SimpleNamespace(prior=first.prior, review=review), 'PHRASES': PHRASES,
        'AMOUNT_TABLES': AMOUNT_TABLES, 'install_in_scoped_assembly': assembler,
    }
    return FunctionType(prior.stage.__code__, env)(runtime, release, rows, groups, verified=verified)


def samples(kind, argument_groups, number):
    values = argument_groups[kind]
    if kind == 'gold':
        return [values[0], values[-1]]
    if kind == 'town':
        port = next(row for row in values if row['arguments'] == [b'Hamburg'.hex()])
        longest = max(values, key=lambda row: len(row['arguments'][0]))
        assert port['arguments'] != longest['arguments']
        return [port, longest]
    assert kind == 'ship'
    arnhem = next(row for row in values if row['arguments'] == [b'Arnhem'.hex()])
    longest = max((row for row in values if not row.get('offline_boundary_input')),
                  key=lambda row: len(row['arguments'][0]))
    assert values[-1]['offline_boundary_input'] and arnhem['arguments'] != longest['arguments']
    return [arnhem, longest, values[-1]]


def main():
    source = checked_text(getsource(first.main), {
        "            assert b' '.join(display.split()) == expected, (number, display, expected)":
            "            original_expanded = expected\n"
            "            if group['argument_kind'] == 'gold':\n"
            "                expected = template % (str(sample['value']).encode('ascii'),)\n"
            "            assert b' '.join(display.split()) == expected, (number, display, expected)",
        'expanded_hex=expected.hex(),': 'expanded_hex=original_expanded.hex(), normalized_visible_hex=expected.hex(),',
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == 35 and len(pages) == 80',
    })
    env = vars(first) | globals()
    exec(compile(source, __file__ + '::city-combat-native-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
