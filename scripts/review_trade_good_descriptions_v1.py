"""Bind the trade-good catalogue and review its first 30 descriptions."""

from collections import Counter
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_proof_and_relic_advice_v1 as parent
from scripts.inventory_native_common_extended_calls import mapped_dynamic_producers
from scripts.review_source_item_cards_and_coin_v1 import ARM, CLEAN, COMMON, ROOT, WIDE_ASCII, reference


OUTPUT = ROOT / 'trade_good_descriptions_source_comparison_v1.json'
NAMES = Path('translations/commodity_fidelity_v2.json')
FIRST, LAST = 137, 260
DECISIONS = {
    137: ('Native to the Mediterranean, wheat ranks with rice and corn as one of the three major grains. Its flour is used to make bread and noodles.',
          'A major grain alongside rice and corn, from the Mediterranean. Its grain is milled for bread, noodles and similar foods.',
          'Replace the unrelated save prompt and preserve the comparison with rice and corn, origin and uses.'),
    138: ('Along with wheat and corn, rice is one of the three major grains. Hulled rice is a staple in Japan and is used to make miso and sake.',
          'A major grain alongside wheat and corn. The husk is removed. Rice is a Japanese staple and is used in miso and sake.',
          'Keep the relationship to the other grains, the processing and the Japanese foods.'),
    139: ('Corn ranks with wheat and rice as one of the three major grains. It was grown in the New World before the Common Era and is used to make bourbon.',
          'A major grain alongside wheat and rice, cultivated in the New World before the Common Era. It is an ingredient in bourbon whiskey.',
          'Replace the save prompt with the source date, region and example use.'),
    140: ('A mild-tasting vegetable from the New World. Its underground tubers can be prepared in many ways and are a staple in some regions.',
          'A New World vegetable with mild-tasting edible underground stem tubers. It has many preparations and is a staple in some regions.',
          'Keep each fact and use the ordinary term tubers in place of a labored anatomical description. Normalize the full-width I.'),
    141: (None, 'Soybean seeds used to make foods such as tofu and miso. Said to come from northern China.',
          'Retain the useful food examples and the qualified origin. Soybeans are the seeds in question.'),
    142: ('Found in waters around the world, fish can be eaten raw or grilled.',
          'Fish can be caught all over the world and is eaten raw or grilled.',
          'Restore the worldwide distribution and both preparations.'),
    143: ('Beef can be boiled or grilled. In some cultures, people avoid it altogether.',
          'Cattle meat is boiled or grilled. Some cultures do not eat it at all.',
          'Use the established good name and keep the cultural distinction without guessing the reason.'),
    144: ('A starchy vegetable from the New World. Among vegetables, only tubers and beans have more calories.',
          'A New World vegetable rich in starch and ranked behind tubers and beans in calories.',
          'Replace the save prompt with the source origin, starch content and relative calorie comparison.'),
    145: ('Made by fermenting milk with lactic acid bacteria. The milk, such as cow or goat milk, the bacteria, and the length of aging all affect the flavor.',
          'Cheese is made by adding lactic acid bacteria to milk such as cow or goat milk. Flavor varies with the milk, bacteria and aging time.',
          'Restore the process and all three reasons for differences in flavor.'),
    146: ('A New World vegetable in the nightshade family, also called red nightshade. Tomatoes can be eaten raw or simmered.',
          'A nightshade-family vegetable also called red nightshade. It comes from the New World and is eaten raw or cooked.',
          'Preserve the alternate name, region and both preparations.'),
    147: ('The fruit of a large perennial plant native to Asia and a staple in the tropics. Varieties eaten raw are sweeter and differ from those used for cooking.',
          'Bananas grow on a large perennial native to Asia and are a tropical staple. The sugary varieties eaten raw differ from cooking varieties.',
          'Keep the plant, source region, role as a staple and the contrast between raw and cooking varieties.'),
    148: ('A sweetener made chiefly of sucrose and produced from crops such as tropical sugarcane and sugar beets.',
          'A sweetener made primarily of sucrose, produced from crops including sugarcane and sugar beet.',
          'Keep the main component and both crops.'),
    149: ('Honeybees collect nectar from flowers and store it in the hive. The resulting honey is high in sugar and rich in nutrients.',
          'Honey is stored in the hive by bees that gather nectar from flowers. It is high in sugar and has high nutritional value.',
          'Keep the origin in flower nectar and both properties.'),
    150: (None, 'A seasoning essential to the body that draws out moisture and prevents spoilage.',
          'Retain the concise uses and the physiological need. Normalize the full-width I.'),
    151: (None, 'Pressed from olives common along the Mediterranean. Often used for oil-packed anchovies. It oxidizes easily and is unsuitable for deep-frying.',
          'Retain the regional link, example use and reason it is unsuitable for frying in the source.'),
    152: (None, 'Oil pressed from coconut flesh, used for food and industrial purposes.',
          'Retain the clear explanation of the oil, food use and industrial use.'),
    153: (None, 'White, jellylike fruit flesh from southern China, used in Chinese desserts.',
          'Retain the texture, specific region and culinary use.'),
    154: ('A nut from a tree in the birch family that grows in temperate regions. Also known as a hazelnut.',
          'The fruit of a birch-family plant distributed in temperate areas. Also called a hazelnut.',
          'Keep the range and plant family. The alternate source name is the displayed English name.'),
    155: ('Dried grapes, common around the Mediterranean.',
          'Dried grapes found in abundance around the Mediterranean.',
          'Restore the Mediterranean association and remove the unrelated fragment from the shared storage record.'),
    156: ('Salted sturgeon roe, prized as a delicacy.',
          'A prized product made by salting sturgeon roe.',
          'Restore the animal, preparation and value. Keep it independent of the adjoining Sultana description.'),
    157: ('Dried fins from large sharks. Of the tail, dorsal, and pectoral fins, the tail fin is the most prized. The fins are soaked until soft, then simmered or used in soup.',
          'Dried fins of large sharks. Of tail, dorsal and pectoral fins, tail fins are superior. They are softened by rehydrating and simmered or used in soup.',
          'Restore the fin comparison and preparation, including soaking before cooking.'),
    158: ('The fruit of the pepper plant, used as a spice for its aroma and intense heat.',
          'The fruit of a pepper-family plant with a strong aroma and pungency, used as a spice.',
          'Restore both sensory qualities and the use as a spice.'),
    159: ('Dried flower buds of the clove tree, a member of the myrtle family. Cloves rank with pepper and cinnamon as major spices. Their fragrance suits meat dishes.',
          'Dried buds from the myrtle-family clove tree. Cloves are among the three leading spices alongside pepper and cinnamon and add aroma to meat dishes.',
          'Restore the plant and part used, the comparison and the familiar use.'),
    160: ('The seed kernel of the nutmeg tree, a tall evergreen. It helps mask strong odors in meat.',
          'Kernel from the fruit of a tall evergreen nutmeg tree, used to suppress the strong smell of meat.',
          'Keep the part of the plant, its growth habit and the purpose of the spice.'),
    161: ('Dried bark from the cinnamon tree, used for its sweet fragrance.',
          'Dried bark and similar material from the cinnamon tree, used to impart a sweet aroma.',
          'Replace the unrelated text with the principal material and its use.'),
    162: ('Ground pimento seeds. Known as allspice because its flavor recalls cloves, cinnamon, and nutmeg.',
          'Powdered pimento seeds, called allspice because they combine aromas of cloves, cinnamon and nutmeg.',
          'Keep the source term, preparation, familiar English name and all three flavor comparisons.'),
    163: ('Taken from the fruit of the tamarind, a tall evergreen in the legume family. It is used as a spice.',
          'A seasoning taken from the fruit of a tall evergreen tree in the legume family.',
          'Restore the fruit source and its use as a seasoning.'),
    164: (None, 'Dried saffron stigmas, used to flavor and color seafood dishes such as bouillabaisse.',
          'Retain the plant part, both culinary effects and the specific dish.'),
    165: (None, 'Fermented New World vanilla fruit with a distinct sweet scent. Alcohol extracts are used as flavoring.',
          'Retain the origin, processing, scent and use of the extract.'),
    166: ('Dried New World chili peppers, also called red pepper. Their heat is intense.',
          'Dried chili fruits from the New World, also called red pepper. They have a strong, biting heat.',
          'Replace the generic placeholder with the specific origin, alternate name and heat.'),
}


def main():
    base = parent.base
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(release['candidate']) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    source, current = map(parent.stage.NdsImage.open, (CLEAN, release['candidate']))
    source_arm, current_arm = source.read_file(ARM), current.read_file(ARM)
    japanese = common_message_entries(source.read_file(COMMON), source_arm)
    directory = sha256(current_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    english = owned_entries(current.read_file(COMMON), current_arm, directory)
    guarded = mapped_dynamic_producers(source_arm, japanese)['guarded_wrapper']
    for start, end in ((0xBE51C, 0xBE53C), (0xBF328, 0xBF338)):
        assert source_arm[start:end] == current_arm[start:end]
    assert (guarded['native_id_min'], guarded['native_id_max']) == (FIRST, LAST)
    goods = base.load(NAMES)['records']
    assert [row['index'] for row in goods] == list(range(LAST - FIRST + 1))
    rows = []
    for n, item in enumerate(goods, FIRST):
        jp, en = japanese[n], english[n]
        assert jp.message_id == en.message_id == n
        current_text = en.text.decode('cp932')
        logical = ' '.join(current_text.translate(WIDE_ASCII).split())
        finding = ('generic placeholder' if logical.startswith('Trade-good description.')
                   else 'unrelated save prompt or fragment' if logical.startswith('The game cannot save here.')
                   or logical == 'anyway?' else 'comparison required')
        row = dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, commodity_index=n - FIRST,
            commodity_name=item['English'], source_name=item['Japanese'], source_reference=reference(jp),
            current_reference=reference(en), source_hex=jp.text.hex(), current_hex=en.text.hex(),
            source_Japanese=jp.text.decode('cp932'), current_English=current_text, initial_finding=finding)
        if n in DECISIONS:
            revision, meaning, note = DECISIONS[n]
            target = revision or logical
            assert target.isascii() and '%' not in target
            row.update(english=target, source_meaning=meaning, localization_note=note,
                speaker='None', context=f'Trade-good description for {item["English"]}. The original guarded '
                    'selector maps the commodity index to this COMMON message. Renderer and in-game access '
                    'are pending verification.', decision='revision' if revision else 'retention',
                review=dict(source=True, context=False, localization=True, naturalness=True, formatting=False))
        rows.append(row)
    counts = Counter(row['initial_finding'] for row in rows)
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        source_ROM_sha256=release['clean_input_sha256'], current_ROM_sha256=release['candidate_sha256'],
        native_selector=guarded, exact_source_current_selector_spans=True,
        commodity_names=str(NAMES), commodity_names_sha256=base.digest(NAMES),
        counts=dict(counts), records=rows, drafted=len(DECISIONS), renderer_verified=False,
        new_gameplay=False, new_credit=0, full_goal_complete=False))
    print(f'{len(rows)} source-bound comparisons and {len(DECISIONS)} drafts. Stored findings: {dict(counts)}')


if __name__ == '__main__':
    main()
