"""Review the remaining item advice with its clean source and related item cards."""

from inspect import getsource

from scripts import register_figurehead_navigation_gift_advice_v1 as parent
from scripts import review_item_production_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = previous.ROOT / 'proof_and_relic_advice_context_v1.json'
IDS = tuple(range(3181, 3251))
REGIONS = ('the North Sea', 'the Mediterranean', 'Africa', 'the Indian Ocean',
           'Southeast Asia', 'East Asia', 'the New World')
PROOFS = ("Ullr's Bow", "Cambyses' Crown", 'Aksum Gold Seal', 'Rigveda',
          'Kediri Talisman', 'Qin Palace Lamp', 'Crystal Skull')
MAPS = ('Thales Paper Map', 'Cleobulus Cloth Map', 'Periander Stone Map', 'Solon Leaf Map',
        'Bias Coin Map', 'Chiron Bamboo Map', 'Pittacus Blade Map')
DATA = {}
for i, (region, proof, map_name) in enumerate(zip(REGIONS, PROOFS, MAPS, strict=True)):
    proof_name = f"{region}'s Proof of Conquest"
    DATA[3181 + i] = (
        proof, {1: f'{proof_name[0].upper()}{proof_name[1:]}.',
                3: "The Indian Ocean's Proof of Conquest."}.get(i),
        f'The adviser identifies the item as the Proof of Conquest for {region}.',
        'Use the complete regional name and the Help topic 4 term, matching the other Proof identifications.'
        if i in (1, 3) else 'Retain the concise identification, complete regional name and established term.',
    )
    DATA[3188 + i] = (
        map_name, None if i == 0 else f'It marks the location of {proof_name}.',
        f'The map marks the location of the Proof of Conquest for {region}.',
        'Retain the complete explanation of the mark and normalize the initial I.' if i == 0
        else 'Use the same complete clue as the other completed maps and name the region in full.',
    )

DATA.update({
    3195: ('Stone Circle Map', None,
           'London is the recommended starting point for the expedition.',
           'Retain London and the practical recommendation to begin the search there.'),
    3196: ('Arena Map', None,
           'Genoa is the recommended starting point for the expedition.',
           'Retain the concise directions and the named departure point.'),
    3197: ('Cave Village Map', 'This is a map of the area around Turkey.',
           'The adviser recognizes a map of the area in and around Turkey.',
           'Restore the approximate geographic scope. The adviser recognizes the region without giving a departure point.'),
    3198: ('Sahara Map', None,
           'Sao Jorge is the recommended starting point for the expedition.',
           'Retain the established port spelling and the clear starting-point advice.'),
    3199: ('Royal Mosque Map', 'Looks like a map of Arabia.',
           'The map appears to show the Arabian region.',
           'Restore the adviser’s tentative identification of Arabia.'),
    3200: ('Mughal Empire Map', None,
           'The adviser recommends heading inland from Calicut.',
           'Retain the port and the inland direction without adding a route.'),
    3201: ('Ancient Temple Map', 'Looks like a kingdom in Indochina.',
           'The drawing appears to depict a kingdom in Indochina.',
           'Make the recognition sound spoken and restore consistent Latin glyphs.'),
    3202: ('Beijing Map', None,
           'The adviser recommends going north overland from Hangzhou.',
           'Retain the departure point, direction and overland route.'),
    3203: ('Royal Tomb Map', "That's the Korean Peninsula.",
           'The adviser recognizes the map as depicting the Korean Peninsula.',
           'Restore the geographic feature the adviser identifies.'),
    3204: ('Golden Temple Map', None,
           'Osaka is the recommended starting point for the expedition.',
           'Retain the spoken instruction and use the established name Osaka.'),
    3205: ('Ancient City Map', "That's a Caribbean island on the map.",
           'The adviser recognizes one of the islands shown as Caribbean.',
           'Use a direct observation and leave the island unnamed.'),
    3206: ('Aztec Pictorial Map', None,
           'Veracruz is the recommended starting point for the expedition.',
           'Retain the short instruction and the exact port.'),
    3207: ('Old Parchment', None,
           'The parchment might show the North Sea Proof’s location, but this piece alone cannot be read.',
           'Retain the tentative clue and the immediate limitation. Normalize both full-width I glyphs.'),
    3208: ('Patterned Cloth', "This must show where the Mediterranean's Proof of Conquest lies. I can't make it out from this alone.",
           'The adviser is confident the cloth records the Mediterranean Proof’s location, but cannot decipher this piece alone.',
           'Restore confidence about what the cloth records while making its present unreadability sound spoken.'),
    3209: ('Upper Stone Tablet', None,
           'The adviser thinks this tablet marks the African Proof’s location and cannot read only half.',
           'Retain the tentative judgment, the missing half and the trailing thought. Normalize the I glyph.'),
    3210: ('Evergreen Lotus Leaf', "I think this shows where the Indian Ocean's Proof of Conquest lies. The question is how...",
           'The adviser thinks the leaf records the Indian Ocean Proof’s location in some form, but trails off over the method.',
           'Keep the tentative inference and the question of how the leaf could record the location.'),
    3211: ('Ancient Kingdom Coin', None,
           'The coin is probably needed to discover the Proof of Conquest in Southeast Asia.',
           'Retain the practical clue and its qualification. The coin is probably needed to find the Proof.'),
    3212: ('Tang Bamboo Craft', "This might have something to do with East Asia's Proof of Conquest.",
           'The bamboo craft may be connected to the Proof of Conquest in East Asia.',
           'Give the tentative connection a natural spoken cadence and restore the full name.'),
    3213: ('Ceremonial Knife', "No doubt about it. This is a key to finding the New World's Proof of Conquest.",
           'The adviser is certain the ceremonial knife is a key to finding the Proof in the New World.',
           'Keep the emphatic certainty and the role in finding the Proof without specifying how it works.'),
    3214: ('Red Dye', "This might have something to do with the map to the North Sea's Proof of Conquest.",
           'The red dye may be connected to the map for the North Sea Proof.',
           'Distinguish the map from the Proof itself and keep the link tentative.'),
    3215: ('Brass Lamp', "This looks like it has something to do with the map to the Mediterranean's Proof of Conquest.",
           'The lamp appears to be connected to the map for the Mediterranean Proof.',
           'Restore the connection to the map and the adviser’s measured confidence.'),
    3216: ('Lower Stone Tablet', None,
           'The adviser thinks this records the African Proof’s location and trails off because only half is present.',
           'Retain the matching clue for the other half, including the unfinished thought.'),
    3217: ('Kushan Platter', None,
           'The platter seems connected to something that records the Indian Ocean Proof’s location.',
           'Retain the indirect connection, which is still tentative. Normalize the regional name’s I glyph.'),
    3218: ('Lotion Jar', "This could be the key to finding the map to Southeast Asia's Proof of Conquest...",
           'The jar seems to be the key to finding the map for the Southeast Asian Proof, but the adviser trails off.',
           'Restore the distinction between finding the map and finding the Proof and preserve the hesitation.'),
    3219: ('Bamboo Assembly Plan', "Could this show where East Asia's Proof of Conquest lies?",
           'The adviser wonders if the plan records the location of the East Asian Proof.',
           'Restore the speculative question and the full regional term.'),
    3220: ('Sun-Crest Sheath', "This might have something to do with the map to the New World's Proof of Conquest.",
           'The sheath may be connected to the map for the New World Proof.',
           'Keep the tentative connection to the map and match the parallel clue for the Red Dye.'),
    3221: ('Flame Gem', "Even a ruby can't match that red. A beauty like this is rare. I'd give it to the Boarding Leader.",
           'The gem’s red exceeds that of a ruby. The adviser calls its beauty rare and recommends the Boarding Leader.',
           'Restore the rare beauty, the ruby comparison and the established crew role.'),
    3222: ('Old Dagger', "I'd give it to a deckhand or the Boarding Leader.",
           'The adviser suggests giving it to a deckhand or to the Boarding Leader.',
           'Keep both recipients and match the parallel recommendations for other weapons.'),
    3223: ('Eerie Mask', 'Give it to the Boarding Leader.',
           'The adviser recommends giving the mask to the Boarding Leader.',
           'Use the established role and retain the direct recommendation.'),
    3224: ('Clear Rose Quartz', 'Give it to a Gunner.',
           'The adviser recommends giving the quartz to a Gunner.',
           'Preserve the specific crew position and match the localized role name.'),
    3225: ('Gem-Eating Gem', 'Give it to the Purser.',
           'The adviser recommends giving the crystal to the Purser.',
           'Keep the advice and match the localized crew-role name.'),
    3226: ('Untouched Blade', None,
           'The adviser recognizes a magic sword, pauses, and finds it more engrossing the longer they look.',
           'Retain the matching reaction to the earlier magic sword, including the hesitation. Normalize the I glyph.'),
    3227: ('Witch Idol', None,
           'The adviser admires the mermaid figure and recommends giving it to the Gunner.',
           'Retain the natural reaction and the suggested recipient. The adviser calls the figure a mermaid.'),
    3228: ('Twisted Horn', "An animal horn. I hear it's prized in Chinese medicine.",
           'The adviser recognizes an animal horn and has heard that it is prized in Chinese medicine.',
           'Keep the identification, the cultural reference and the adviser’s attribution.'),
    3229: ("King's Shield", "There's a power in this I can't put into words. I'd entrust it to a warrior you can count on.",
           'The adviser senses an indescribable power in the shield and recommends giving it to a reliable warrior.',
           'Give the reaction room before the recommendation and keep the emphasis on trust.'),
    3230: ('Giant Red Spear', "You don't often come across a piece this fine. I'd entrust it to a warrior you can count on.",
           'The adviser rarely sees a piece of such quality and recommends giving it to a reliable warrior.',
           'Preserve the rare quality of the spear and match the parallel recommendation for the shield.'),
})

for i, relic in enumerate(('Flame Gem', "King's Shield", 'Twisted Horn', 'Untouched Blade', 'Old Dagger')):
    for part in range(1, 5):
        DATA[3230 + i * 4 + part] = (
            f'{relic} Map {part}',
            "A piece of an old map to a hidden treasure. I hear it takes four pieces to make a set.",
            'It is a fragment of an old map marking the hidden treasure’s location. Four fragments reportedly make a set.',
            f'Restore the treasure clue and the reported four-piece set for part {part} of the {relic} map. '
            'Match the other fragments because the adviser gives the same clue for each.',
        )

DATA = dict(sorted(DATA.items()))


def main():
    env = vars(previous) | globals() | {'RELEASE': parent.RELEASE}
    bindings = checked_text(getsource(previous.bind_advice_callers), {
        'len(cases) == 144': 'len(cases) == len(IDS) * 6',
    })
    exec(compile(bindings, __file__ + '::same-native-item-index-and-speaker', 'exec'), env)
    source = checked_text(getsource(previous.main), {
        "('source_item_cards_and_coin_context_v1.json', 'utility_weapon_item_cards_context_v1.json')":
            "('relic_map_item_cards_context_v1.json', 'promotional_item_cards_context_v1.json')",
        "row['item_ID'] < len(IDS)": "IDS[0] - FIRST <= row['item_ID'] <= IDS[-1] - FIRST",
        'list(range(len(IDS)))': '[n - FIRST for n in IDS]',
        'and 144 original caller-fragment checks.': 'and {len(IDS) * 6} original caller-fragment checks.',
    })
    exec(compile(source, __file__ + '::source-current-and-item-card-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
