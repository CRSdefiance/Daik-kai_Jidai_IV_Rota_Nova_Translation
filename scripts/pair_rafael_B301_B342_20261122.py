"""Bind the two remaining Rafael script ranges to their registered input."""

from argparse import ArgumentParser
from pathlib import Path

from scripts import pair_rafael_B221_B240_20261122 as prior
from scripts import register_rafael_B261_B280_20261122 as parent
from scripts.source_locked_derivation_v5118 import checked_text


RANGES = {
    301: (320, 453, 11, 145, 19),
    321: (342, 556, 16, 298, 48),
}


def paths(start):
    stop = RANGES[start][0]
    root = Path(f"work/analysis/rafael_B{start}_B{stop}_followup_20261122")
    return root, root / "paired_source_registered_candidate.json"


def bind(start):
    stop, records, captions, variants, style_tables = RANGES[start]
    root, output = paths(start)
    reference = Path(f"translations/rafael_B{start}_B{stop}_integrated_final_review_v1.json")
    source = checked_text(prior.source, {
        'range(221, 241)': f'range({start}, {stop + 1})',
        'len(ready) == 270': f'len(ready) == {records}',
        'for r in ready) == 7': f'for r in ready) == {captions}',
        'for r in ready) == 29': f'for r in ready) == {variants}',
        'for g in groups) == 4': f'for g in groups) == {style_tables}',
        '270 exact source and current records bound across Rafael B221–240, including seven choice labels and 29 actor-style variants.':
            f'{records} exact source and current records bound across Rafael B{start}–B{stop}, including {captions} captions and {variants} actor-style variants.',
    })
    scope = prior.scope | dict(base=parent.base, native=parent.native, ROOT=root, PAIRED=output, EARLIER=reference, parent=parent)
    exec(compile(source, __file__ + "::exact-source-current-binding", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("start", type=int, choices=RANGES)
    bind(parser.parse_args().start)
