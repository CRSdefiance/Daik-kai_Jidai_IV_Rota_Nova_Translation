"""Keep the longer Price Info descriptions coherent across the four-row turn."""

from inspect import getsource
from types import FunctionType

from scripts import stage_trade_good_descriptions_v3 as third
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = third.ROOT.with_name('trade_good_descriptions_staged_20261111_v4')
ROM, PROOF = ROOT / third.ROM.name, ROOT / third.PROOF.name
OUTPUT = third.OUTPUT.with_name('trade_good_descriptions_context_v4.json')
AMENDMENTS = {
    139: ("Corn ranks with wheat and rice among the world's three major grains. It was grown in the New World before the Common Era. Corn is also used to make bourbon.",
          'Keep the early cultivation and bourbon use in complete sentences across the page turn.'),
    159: ('Cloves are the dried flower buds of the clove tree, a member of the myrtle family. A fragrant spice for meat, ranked with pepper and cinnamon.',
          'Keep the plant and part used together. Give the culinary use and comparison their own thought.'),
    180: ('Vessels coated with lacquer-tree sap. The process starts with a base coat. Color and technique in the top coat give each piece its look.',
          'Keep the base coat and the decorative top coat distinct across the page turn.'),
    182: ('Sheep or goat fleece is spun into yarn or woven into cloth. It is warm, absorbent, and springy. Wool has long kept Europeans warm in winter.',
          'Preserve the materials and textile uses, then give the European use a complete sentence.'),
    190: ('Wool floor coverings valued for warmth, protection from damp, and decorative appeal. Persian carpets are prized as the finest in art and handweaving.',
          'Keep the three purposes of wool rugs and the source appraisal of Persian carpets in complete thoughts.'),
    199: ('Jadeite can be opaque or translucent. The finest pieces have a deep green color and let light through. In China, jade ornaments also serve as protective charms.',
          'Keep the quality criteria and the Chinese use on their own sides of the page turn.'),
    213: ('Dried Korean ginseng root from East Asia. It contains steroid compounds and B vitamins. It was used to nourish and strengthen the body and heart.',
          'Keep its origin and contents together and present its historical uses in a complete sentence.'),
}


def stage_environment():
    env = third.stage_environment() | globals()
    rows = checked_text(getsource(third.four_rows), {'17 <= width <= 36': '15 <= width <= 36'})
    plan = checked_text(getsource(third.plan), {
        '76 <= len(left) <= 147 and 27 <= len(right) <= 108':
            '72 <= len(left) <= 147 and 26 <= len(right) <= 143',
        'len(tail) > 2': 'len(tail) > 4',
    })
    repack = checked_text(getsource(third.first.repack), {'1 <= len(lines) <= 6': '1 <= len(lines) <= 8'})
    exec(compile('\n\n'.join((rows, plan, repack)), __file__ + '::four-row-paginated-prose', 'exec'), env)
    return env


def main():
    base = third.first.base
    if not OUTPUT.exists():
        draft = base.load(third.OUTPUT)
        for row in draft['records']:
            n = third.first.FIRST + row['commodity_index']
            if n in AMENDMENTS:
                text, note = AMENDMENTS[n]
                assert row['decision'] == 'revision'
                row.update(english=text, localization_note=note)
        draft['four_row_page_refinements'] = sorted(AMENDMENTS)
        draft['actual_page_geometry'] = dict(rows=4, viewport=[16, 296, 244, 360],
            calibration='out/trade_good_descriptions_staged_20261111_v1/price_info/capture/capture_report.json')
        base.save(OUTPUT, draft)
    FunctionType(third.main.__code__, vars(third) | globals())()


if __name__ == '__main__':
    main()
