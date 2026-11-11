"""Verify the two item views and complete generated map-title coverage."""

import inspect
from pathlib import Path
import sys
from types import FunctionType

from dk4tool.patch import promotional_item_cards_v1 as patch
from scripts import stage_utility_weapon_item_cards_v1 as previous
from scripts.probe_promotional_item_full import verify as initialize
from scripts.review_promotional_item_cards_v1 import IDS, OUTPUT, RELEASE
from scripts.source_locked_derivation_v5118 import checked_text

item_table = patch.item_table
ROOT = Path('out/promotional_item_cards_staged_20261111_v1')
ROM = ROOT / 'promotional_item_cards_RESEARCH_ONLY.nds'
PREP = ROOT / 'staged_build.json'
PROOF = ROOT / 'stored_verification.json'
AMENDMENTS = {
    3006: ('A rare piece of clear rose quartz with a sharply defined six-rayed star.',
           'Keep the material, clarity and sharply defined six-rayed star together.'),
    3007: ("This rare phantom crystal contains a diamond. It's said to have grown again and to improve concentration.",
           'Restore the rare second growth and keep the claimed effect on concentration qualified.'),
}


def native_variants(arm, manuscript, plans):
    variants, titles = [], {}
    covered = set()
    for source in manuscript['native_initializers']:
        seed = source['seed']
        new = initialize(arm, seed)
        assert new['names'] == source['current']
        assert new['selected_default_indices'] == source['selected_default_indices']
        for ident in plans:
            row = new['names'][ident - 188]
            if ident < 198:
                if seed != 0:
                    continue
            else:
                base_item = new['selected_default_indices'][(ident - 198) // 4]
                if base_item in covered:
                    continue
            variants.append((ident, plans[ident], seed))
            titles[(seed, ident)] = row['name']
        covered.update(new['selected_default_indices'])
    assert covered == set(range(188, 198))
    assert len(variants) == 50 and len(set(titles.values())) == 50
    return variants, titles


context = vars(previous) | globals()
active_rows = FunctionType(previous.active_rows.__code__, context)
build = FunctionType(previous.build.__code__, context)
context.update(active_rows=active_rows, build=build)
stage_source = checked_text(inspect.getsource(previous.stage), {
    'Path(patch.__file__), Path(__file__)': 'Path(patch.__file__), Path(previous.__file__), Path(__file__)',
})
offline_source = checked_text(inspect.getsource(previous.offline), {
    '    for ident, item in plans.items():': '''    catalogue['item_advice_projection'].extend({} for _ in range(20))
    variants, titles = native_variants(arm, manuscript, plans)
    for ident, item, seed in variants:''',
    'item_resource_index=ident, item_common=common)': 'item_resource_index=ident, item_common=common, item_promotional_seed=seed)',
    'expected_draws(arm, catalogue, page, config, item_index=ident)':
        'expected_draws(arm, catalogue, page, config, item_index=ident, promotional_seed=seed)',
    "page=page, mode=mode,\n                    lines=lines": "page=page, mode=mode, seed=seed,\n                    lines=lines",
    "{row[\"item_name\"]}": "{titles[(seed, ident)]}",
    'assert len(cases) == 4 * len(IDS) and len(pictures) == 2 * len(IDS)':
        'assert len(cases) == 200 and len(pictures) == 100',
    'native_PARENT_crop_contract=parent, sheets=sheets,': '''native_PARENT_crop_contract=parent, sheets=sheets,
        native_promotional_initializers=manuscript['native_initializers'],
        complete_generated_titles_and_all_twenty_initial_fragment_slots=True,''',
})
exec(compile(stage_source + '\n\n' + offline_source, __file__ + '::promotional-item-stage', 'exec'), context)
stage, offline = context['stage'], context['offline']


if __name__ == '__main__':
    assert sys.argv[1:] in (['build'], ['offline'])
    (stage if sys.argv[1] == 'build' else offline)()
