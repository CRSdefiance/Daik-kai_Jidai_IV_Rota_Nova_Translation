"""Refine native Price Info pagination after the first contact-sheet review."""

from itertools import combinations
from types import FunctionType

from scripts import stage_trade_good_descriptions_v1 as first


ROOT = first.ROOT.with_name('trade_good_descriptions_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('trade_good_descriptions_context_v3.json')
AMENDMENTS = {
    138: ('Rice ranks with wheat and corn as one of the three major grains. Hulled rice is a staple in Japan and is used to make miso and sake.',
          'Keep the grain comparison, then give the Japanese staple and uses their own complete thought.'),
    140: ('A mild New World vegetable whose underground tubers are cooked in many ways. They are a staple in some regions.',
          'Preserve the tubers, preparations and regional role while giving the final fact a full sentence.'),
    145: ('Cheese is made by fermenting milk, such as cow or goat milk, with lactic acid bacteria. Flavor varies with the milk, bacteria, and aging time.',
          'Keep the full process together and give the three flavor variables a separate sentence.'),
    149: ('Honeybees store flower nectar in the hive. Honey is high in sugar and rich in nutrients.',
          'Keep the origin, storage and both properties in two concise sentences.'),
    159: ('Dried flower buds of the clove tree, a member of the myrtle family. A major spice alongside pepper and cinnamon, with a fragrance that suits meat dishes.',
          'Keep the definition and the culinary context as separate thoughts.'),
    163: ('A spice from the fruit of the tamarind, a tall evergreen in the legume family.',
          'Lead with the use and retain the fruit, growth habit and plant family.'),
    165: ('Fermented New World vanilla fruit has a distinct sweet scent. Its alcohol extract is used as flavoring.',
          'Keep the scent, origin, processing and extract while removing the dangling continuation.'),
    178: ('Glass vessels and ornaments are often shaped by blowing through a pipe into molten glass on its tip.',
          'Describe free-blowing directly and keep the pipe and glass at its tip together.'),
    179: ('Pottery and porcelain for tableware or art, shaped by hand, on a wheel, or in a mold.',
          'Keep both uses and all three methods in one statement.'),
    181: ('Designs cut into a surface and filled with another material, often gold, silver, or shell.',
          'Retain the technique and all three materials without stranding a phrase.'),
    187: ('Soft, absorbent, durable cloth woven from cotton yarn. A practical fabric used in India since before the Common Era.',
          'Give the historical context a complete sentence and preserve the material and handling qualities.'),
    194: ('Flat works of art include oil paintings, ink paintings, and watercolors. Collectors pay high prices for famous painters\' work.',
          'Keep the examples together and retain why work by a famous painter can be valuable.'),
    201: ('Worked coral has adorned weapons since antiquity. It was thought to ward off discord and evil.',
          'Preserve the historical use and present the protective qualities as a belief.'),
    202: ('Hawksbill shell, translucent yellow with brown spots. Used for combs, eyeglass frames, and ornaments.',
          'Keep the species, appearance and full list of uses without a stray word after the page turn.'),
    203: ('Resin fossilized underground. Yellowish, clear or translucent, it is used for brooches and other ornaments.',
          'Keep its origin, appearance and use in straightforward catalogue English.'),
    204: ('Clear quartz, an oxide mineral. Amethyst, smoky quartz, and rose quartz are varieties used for ornaments.',
          'Keep each variety together and preserve the material and its use.'),
    206: ('Gems formed inside pearl oysters and other shellfish. They can be white, silver-pink, or black. Perfectly round pink pearls are prized most.',
          'Keep the color list and the best grade distinct, with all of the original criteria.'),
    208: ('Clear blue gems held sacred and worn in rings by Christian clergy. Only diamonds rank higher in hardness and rarity.',
          'Keep the historical use together and move the complete comparison to the next thought.'),
    236: ('Fertilizer from seabird droppings that build up on tropical shores and islands. It contains nitrogen and phosphate.',
          'Put the use first and keep the origin and both nutrients.'),
    242: ('King salmon are the largest and longest-lived salmon. Spawning takes place year-round, so their runs upriver last a long time.',
          'Keep the causal link and describe the species as a whole.'),
    247: ('A fermented honey drink enjoyed by Celts and Vikings. It was valued for nourishment and warmth.',
          'Keep both groups and both reasons it was valued in complete thoughts.'),
    258: ('Diamonds from Siberia. Its harsh landscape is covered in permafrost, yet the region is rich in resources such as gold and diamonds.',
          'Keep Siberia’s conditions and its wealth together without stranding the examples.'),
}

WEAK_ENDS = {'a', 'an', 'at', 'for', 'in', 'of', 'the', 'to', 'with'}
CLAUSE_STARTS = {'and', 'but', 'so', 'where', 'which', 'while', 'yet'}


def three_rows(words):
    candidates = []
    for left, right in combinations(range(1, len(words)), 2):
        parts = (' '.join(words[:left]), ' '.join(words[left:right]), ' '.join(words[right:]))
        widths = [len(line) for line in parts]
        if not all(17 <= width <= 36 for width in widths):
            continue
        awkward = sum(line.rsplit(' ', 1)[-1].lower() in WEAK_ENDS for line in parts)
        balance = sum((width * 3 - sum(widths)) ** 2 for width in widths)
        candidates.append((awkward, balance, parts))
    return min(candidates)[2] if candidates else None


def plan(text):
    lines = first.rows_for(text)
    if len(lines) <= first.ROWS_PER_PAGE:
        return lines
    # The cursor advances only after three rows. Prefer sentence boundaries when
    # the first page has enough text for three readable rows, then clause breaks.
    words = text.split()
    choices = []
    for stop in range(1, len(words)):
        left, right = ' '.join(words[:stop]), ' '.join(words[stop:])
        if not (63 <= len(left) <= 110 and 26 <= len(right) <= 110):
            continue
        head, tail = three_rows(words[:stop]), first.rows_for(right)
        if head is None or len(tail) > first.ROWS_PER_PAGE:
            continue
        last, next_word = words[stop - 1], words[stop].lower()
        boundary = (0 if last.endswith(('.', '!', '?')) else 1 if last.endswith((',', ';'))
                    else 2 if next_word in CLAUSE_STARTS else 3)
        if last.lower() in WEAK_ENDS:
            boundary += 2
        choices.append((boundary, abs(len(right) - 56), -len(left), [*head, *tail]))
    return min(choices)[3] if choices else first.plan(text)


def stage_environment():
    env = vars(first) | globals()
    env['repack'] = FunctionType(first.repack.__code__, env)
    return env


def main():
    base = first.base
    if not OUTPUT.exists():
        draft = base.load(first.OUTPUT)
        for row in draft['records']:
            n = first.FIRST + row['commodity_index']
            if n in AMENDMENTS:
                text, note = AMENDMENTS[n]
                row.update(english=text, localization_note=note, decision='revision')
        draft['visual_amendments'] = sorted(AMENDMENTS)
        draft['editorial_decisions'] = {
            decision: sum(row['decision'] == decision for row in draft['records'])
            for decision in ('revision', 'retention')}
        draft['previous_visual_proof'] = str(first.PROOF)
        draft['previous_visual_proof_sha256'] = base.digest(first.PROOF)
        base.save(OUTPUT, draft)
    FunctionType(first.main.__code__, stage_environment())()


if __name__ == '__main__':
    main()
