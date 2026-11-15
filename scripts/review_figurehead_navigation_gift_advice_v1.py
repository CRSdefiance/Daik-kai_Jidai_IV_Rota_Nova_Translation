"""Review the advice for figureheads, navigation tools and regional gifts."""

from inspect import getsource

from scripts import register_crew_equipment_advice_v1 as parent
from scripts import review_item_production_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = previous.ROOT / 'figurehead_navigation_gift_advice_context_v1.json'
IDS = tuple(range(3147, 3181))
DATA = {
    3147: ('Eagle Figurehead', 'Fit it to any ship and the whole fleet should pick up speed.',
           'Fitting the figurehead on any one ship should increase the speed of the whole fleet.',
           'Restore the choice of any ship and the fleet-wide effect. Keep the adviser’s qualification.'),
    3148: ('Piglet Figurehead', "They say sailors on a ship fitted with this don't get hungry as quickly.",
           'The sailors on the ship that carries this figurehead reportedly get hungry less often or less intensely.',
           'Keep the reported effect on hunger and restrict it to the ship carrying the figurehead.'),
    3149: ('Shachihoko', 'It seems to drive off dangerous clouds. You could fit it to any ship.',
           'The figurehead appears to dispel dangerous clouds and may be fitted to any ship.',
           'Restore both the tentative claim and the practical choice of ship. Use the established Japanese item name.'),
    3150: ('White Whale Figurehead', "I'd fit this to a ship that matters to you.",
           'The adviser recommends fitting it to an important or valued ship.',
           'Keep the advice personal and leave the intended benefit unspecified.'),
    3151: ('Dragon Figurehead', 'Fit this to the ship with the strongest guns.',
           'The adviser says to install it on the ship with the greatest firepower.',
           'Use the practical criterion of firepower without implying that the game requires a particular class of ship.'),
    3152: ('Dolphin Figurehead', "Fit it to any ship and the whole fleet benefits. They say it'll let us spot things farther away.",
           'On any ship it works for the entire fleet. It is said to extend the range in which the fleet can discover things.',
           'Keep the fleet-wide effect and present the increased sighting range as something the adviser has heard.'),
    3153: ('Maiden Figurehead', None,
           'It ought to work on any ship and seems to cleanse or refresh the spirit and relieve fatigue.',
           'Retain the tentative statements and trailing reflection. Normalize the two full-width I glyphs.'),
    3154: ('Demon Figurehead', None,
           'The adviser hesitates and warns that once installed, it cannot be moved to another ship.',
           'Retain the hesitant opening and the irreversible transfer restriction.'),
    3155: ('King Figurehead', "I'd fit it to a ship with plenty of sailors. It looks like it'll help in boarding fights.",
           'The adviser suggests a ship with many sailors because it appears useful in hand-to-hand ship combat.',
           'Restore the order of the recommendation and its reason. Keep the probable benefit specific to boarding.'),
    3156: ('Madonna Figurehead', "It should bring heaven's protection to any ship. It might keep the crew from getting sick.",
           'Any ship should receive divine protection. The adviser thinks this could keep people from falling ill.',
           'Keep the protective belief and possible prevention distinct. Use an ordinary ASCII I.'),
    3157: ('Compass', None, 'This is a very useful tool for a surveyor.',
           'Retain the direct appraisal and its surveyor context.'),
    3158: ('Sextant', None, 'This is a fundamental tool for a surveyor.',
           'Retain the distinct recommendation of a basic instrument.'),
    3159: ('Aristarchus Telescope', "Give it to a lookout. It'll make items and ports easier to spot.",
           'A lookout who carries this will have an easier time finding items and ports.',
           'Name both things the lookout can find and preserve who should carry the instrument.'),
    3160: ('Frozen Rose', 'Beautiful work. Women around the North Sea might appreciate how delicate it is.',
           'The adviser praises the workmanship and suggests women around the North Sea will appreciate its delicacy.',
           'Name the specific region and keep the gift suggestion as the adviser’s judgment.'),
    3161: ('Rainbow Marbles', None,
           'The adviser admires it and thinks its simple beauty could be prized in countries with advanced seamanship.',
           'Retain the short admiration, the seafaring clue and the qualified appraisal of its simple charm.'),
    3162: ('Gold Dust', "Gold dust, eh? I seem to recall hearing that women in the north are especially fond of gold.",
           'The adviser recognizes gold dust and thinks they once heard that women in the north have a strong liking for gold.',
           'Restore the recognition, the uncertain recollection, and the difference between the gift and gold in general.'),
    3163: ('Bread Millstone', 'You need a strong arm to use it. I heard in Northern Europe that women there who love to cook would be glad to have it.',
           'It takes strength to use. The adviser heard in Northern Europe that women there who like cooking would appreciate it.',
           'Keep the physical effort, the specific location, and the attributed gift clue.'),
    3164: ('Huizong Art', 'I imagine people in Western Europe would be curious about art from the East.',
           'In Western European countries, Eastern art would likely be regarded as something rare or curious.',
           'Restore Western Europe and the sense of novelty. Keep it as an opinion about the gift.'),
    3165: ('Celestial Turban', None, 'Arabian dress seems quite mysterious to Europeans.',
           'Retain the perspective of the people the adviser thinks will find it intriguing.'),
    3166: ("Sappho's Poems", "Beautiful poetry. Around the Mediterranean, tales of ancient Greece's glory still fire the imagination.",
           'The adviser admires the poetry and says that stories of ancient Greek glory are famous around the Mediterranean for their romantic appeal.',
           'Keep the admiring opening and express the imaginative appeal of the stories without implying love stories.'),
    3167: ('Lamenting Jar', 'There are ancient ruins all over the Mediterranean. Someone who grew up there might find this interesting.',
           'There are many ancient ruins in the Mediterranean, and someone raised there might take an interest in this object.',
           'Restore the reason for the adviser’s guess, with room for individual taste.'),
    3168: ('Venus de Milo', "Everyone around the Mediterranean knows this statue. I'll wager plenty would want it. Magnificent...",
           'The statue is nearly universally known along the Mediterranean coast. Many people would likely want it. The adviser admires it.',
           'Restore the fame and the trailing admiration. Keep interest prospective.'),
    3169: ('Stained-Glass Flower', 'The Mediterranean is known for the finest stained glass. Someone from there should appreciate this.',
           'The Mediterranean boasts the best stained-glass workmanship, so someone from there will likely appreciate this piece.',
           'Distinguish the region’s craftsmanship from the potential recipient’s appreciation.'),
    3170: ('Silla Gold Crown', 'A girl I met in China wanted this in the worst way.',
           'A girl the adviser met in China was particularly eager to have this piece.',
           'Restore the personal encounter and keep the intensity without assuming her nationality.'),
    3171: ('Ceramic Earrings', 'I recall hearing about a woman learning to dance. It was in a tavern in some Indian Ocean town.',
           'The adviser recalls hearing, in a tavern in an unnamed Indian Ocean town, about a woman learning to dance.',
           'Keep the recalled report, the hearing location and the uncertainty about which town. Use ordinary ASCII I.'),
    3172: ('Jade Jewel', None,
           'The adviser has heard that a fleet from the East once reached East Africa and conveyed that jade brings good luck.',
           'Retain the route, the reported exchange and the jade belief. Normalize the opening I glyph.'),
    3173: ('Shakuntala', 'It seems Indian classics are widely read in Southeast Asia, too.',
           'Classical works from India also seem to be read widely in Southeast Asia.',
           'Restore the Indian origin and the adviser’s qualified observation.'),
    3174: ('Shosoin Pitcher', 'All the way from Persia to Japan... Perhaps this piece has deep ties to Asia.',
           'The object was brought from Persia to Japan, so it may have strong ties to Asia.',
           'Preserve the route and the tentative significance, with the adviser’s brief reflection.'),
    3175: ('Black Glass Bowl', "It is beautiful... Still, I doubt people in the West would see what makes it special.",
           'The adviser finds it beautiful and thinks people in the West would have difficulty appreciating its finer qualities.',
           'Keep the admiration and the personal opinion about potential recipients.'),
    3176: ('Embroidered Carpet', None,
           'It is a fine, painstakingly made piece, and carpets are also very popular in East Asia.',
           'Retain the praise for the craftsmanship and the regional clue.'),
    3177: ('Snow-Silk Robe', 'Fine silk, I see. I imagine people in the East would appreciate it, too.',
           'The robe is made of good silk and would probably be well received in the East as well.',
           'Retain both the appraisal and the qualified gift suggestion. Normalize the I glyph.'),
    3178: ('Goryeo Incense Burner', None,
           'Pottery is widely made in West Africa, where people should recognize the value of this fine piece.',
           'Retain the local craft as the reason for appreciation and keep West Africa specific.'),
    3179: ('Supreme Loupe', None,
           'Europe’s newest instruments are apparently quite hard to obtain in the New World.',
           'Retain the distinction between where it comes from and where it is scarce. Normalize the opening I glyph.'),
    3180: ('Rainbow Parrot', None,
           'The adviser admires the feather and has heard that many women in the New World are very fond of animals.',
           'Retain the visual reaction and the attribution of the regional gift clue.'),
}


def add_shachihoko_card(cards, japanese, runtime):
    item_id, message = 116, 2931
    assert item_id not in cards
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    address = get(0x4A53C, get(0xCB190) + 4 + item_id * 20)
    name = bytes(cpu.mem_read(address, 64)).split(b'\0', 1)[0].decode('cp932')
    assert name == 'Shachihoko'
    cards[item_id] = dict(id=f'COMMON_MESSAGE_{message}', item_name=name,
                          source_reference=previous.reference(japanese[message]))
    runtime.calls.clear()


def main():
    env = vars(previous) | globals() | {'RELEASE': parent.RELEASE}
    bindings = checked_text(getsource(previous.bind_advice_callers), {
        'len(cases) == 144': 'len(cases) == len(IDS) * 6',
    })
    exec(compile(bindings, __file__ + '::same-native-item-index-and-speaker', 'exec'), env)
    source = checked_text(getsource(previous.main), {
        "('source_item_cards_and_coin_context_v1.json', 'utility_weapon_item_cards_context_v1.json')":
            "('figurehead_navigation_gift_cards_context_v1.json',)",
        "row['item_ID'] < len(IDS)": "IDS[0] - FIRST <= row['item_ID'] <= IDS[-1] - FIRST",
        '    assert sorted(cards) == list(range(len(IDS)))':
            '    add_shachihoko_card(cards, japanese, runtime)\n    assert sorted(cards) == [n - FIRST for n in IDS]',
        'and 144 original caller-fragment checks.': 'and {len(IDS) * 6} original caller-fragment checks.',
    })
    exec(compile(source, __file__ + '::source-current-and-item-card-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
