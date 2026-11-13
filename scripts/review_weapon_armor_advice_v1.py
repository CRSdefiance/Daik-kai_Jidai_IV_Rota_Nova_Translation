"""Review Hans and Mikhail's complete weapon and armor advice selection."""

from inspect import getsource
from types import FunctionType

from dk4tool.patch.item_interface_research import ROLES
from scripts import register_item_production_advice_v1 as parent
from scripts import review_item_production_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = previous.ROOT / 'weapon_armor_advice_context_v1.json'
IDS = tuple(range(3057, 3107))
ITEMS = (
    'Black Rapier', 'Laocoon Sword', 'Lohengrin Saber', 'Crescent Shotel', "Hero's Scimitar",
    'Golden Cutlass', 'Valiant Bec de Corbin', 'Azure Talwar', 'Sweeping Katzbalger', 'Loyal Falchion',
    'Fallen Angel Katar', 'White Flamberge', 'Bloodstained Shamshir', "Judas' Demonblade", "Zhao Yun's Spear",
    'Orcrist of Atonement', 'Red-Haired Pirate Sword', 'Minotaur Axe', 'Namahage Cleaver', 'Tlaloc Knife',
    'Vepar Halberd', "Kublai's Greatsword", 'Holy Spear of Ares', 'Excalibur', 'Muramasa',
    'Blue Oak Shield', 'Armadillo Hide', 'Silver Sallet', 'Phoenix Bascinet', 'Giant Tortoise Shield',
    'Spirit Dress', 'Bladebreaker Gi', 'Cooling Armor', 'Kanem Warrior Shield', 'Zealot Cuirass',
    'Crimson Ringmail', "Timur's Chainmail", 'Peacock Mail', 'Tula Warrior Helm', 'Ninja Garb',
    'Amber Brigandine', "Jaguar God's Vest", "Bandit's Mail", 'Empress Gown', "Noritsune's Armor",
    'Attila Suit', 'Medusa Shield', "Saladin's Silver Armor", 'Charles Martel Armor', 'Minerva Shield',
)
DECKHAND = (
    None, 'The adviser suggests giving the item to a deckhand.',
    'Retain the straightforward recommendation and the deck role. The item is already identified on the card.',
)
EITHER_ROLE = (
    "I'd give this to a deckhand or the Boarding Leader.",
    'The adviser suggests giving the weapon to a deckhand or the leader of the boarding party.',
    'Keep both options. Use the same Boarding Leader title as the game’s item and crew interfaces.',
)
BOARDING_LEADER = (
    'Give this to the Boarding Leader.',
    'The adviser recommends equipping the leader of the boarding party.',
    'Use the displayed Boarding Leader title and keep the recommendation directed to that role.',
)
TRUSTED_FIGHTER = (
    "I'd give this to a brave fighter you can count on.",
    'The adviser says to entrust this weapon to a brave warrior who can be relied upon.',
    'Give the recommendation a conversational voice and keep the two qualities of courage and reliability.',
)
ARMOR_EITHER = (
    "I'd make sure a deckhand or the Boarding Leader had this.",
    'The adviser would like a deckhand or the leader of the boarding party to have this armor.',
    'Keep the adviser’s personal recommendation and both possible recipients. Use the displayed Boarding Leader title.',
)
QUALITY = (
    None, 'Someone confident in their fighting ability should be given gear of at least this quality.',
    'Retain the link between confidence in combat and the caliber of equipment. The existing advice is direct and specific.',
)
RARE = (
    None, 'The adviser remarks that one seldom encounters a piece as fine as this.',
    'Retain the warm understatement and the implication of rarity, without asserting that there is only one.',
)
DECISIONS = {
    **dict.fromkeys((3057, 3063), DECKHAND),
    **dict.fromkeys((3058, 3061, 3064, 3066, 3076), EITHER_ROLE),
    **dict.fromkeys((3060, 3067, 3068, 3074, 3088, 3089, 3092, 3093), BOARDING_LEADER),
    **dict.fromkeys((3069, 3070), TRUSTED_FIGHTER),
    **dict.fromkeys((3085, 3090, 3091, 3094, 3095), ARMOR_EITHER),
    **dict.fromkeys((3096, 3098), QUALITY),
    **dict.fromkeys((3100, 3101), RARE),
    3059: ('They say Lohengrin was a swan in human form, with uncanny powers. This saber looks awfully sharp, too.',
           'Lohengrin is said to have been an incarnation of a swan with supernatural powers. The saber looks remarkably sharp as well.',
           'Keep the in-game legend attributed and the blade’s sharpness as a separate observation.'),
    3062: ("For the price, it isn't much of a weapon. It might make you look a little grander, though.",
           'It is not as useful as its price would suggest, though it could make its bearer look a little more distinguished.',
           'Let the dry joke follow the price judgment. Use a regular ASCII I.'),
    3065: ('One of your officers could use it, Admiral. Or you could wield it yourself.',
           'A fellow navigator could use it, or the admiral could keep it as their own weapon.',
           'Keep the genuine choice between one of the officers and the admiral carrying it personally.'),
    3071: ("They call it Gentian. Anyone who can wield it well must be a formidable warrior.",
           'The weapon is named Rindo, literally gentian. Anyone who could master it would have to be a very strong warrior.',
           'Keep Gentian as the weapon’s spoken nickname alongside the item title Zhao Yun’s Spear.'),
    3072: ('This is just the thing for a skilled Boarding Leader.',
           'This is especially suited to a capable leader of the boarding party.',
           'Retain the enthusiastic recommendation, with the game’s displayed role title.'),
    3073: ("I'd make sure this went to a skilled Boarding Leader.",
           'The adviser especially wants a capable leader of the boarding party to have this weapon.',
           'Give the emphasis a natural personal voice. Keep the skill requirement and the displayed role title.'),
    3075: ("I'd give this to a deckhand for protection.",
           'The adviser suggests giving it to someone such as a deckhand for self-defense.',
           'Keep the protective purpose and frame the remark as equipment advice.'),
    3077: (None, 'This fine piece should go to a formidable fighter who can be trusted.',
           'Retain the value of the weapon and the two separate qualifications for its bearer.'),
    3078: ('You could give it to one of your crew, Admiral, or wield it yourself.',
           'A companion could carry it, or the admiral could use it as their personal weapon.',
           'Use the broader crew wording here. Keep both choices and the source address to the admiral.'),
    3079: ('Hmm! This is a fine weapon. I can feel some unseen power in it.',
           'The adviser reacts with admiration at the quality of the weapon and senses a power that cannot be seen.',
           'Let the reaction turn into a quiet observation. Use weapon for the spear and a regular ASCII I.'),
    3080: (None, 'The adviser recognizes the legendary object and never thought they would see it firsthand.',
           'Retain the trailing recognition and personal amazement. The item title supplies Excalibur. Normalize both I glyphs.'),
    3081: (None, 'The adviser recognizes a magic sword and feels increasingly drawn to it the longer they look.',
           'Retain the recognition, pause and growing fascination. Normalize both I glyphs.'),
    3082: (None, 'The adviser recommends keeping the shield on hand with a deckhand.',
           'Retain the spoken “keep this on hand” and the deck role.'),
    3083: (None, 'Even someone lacking confidence in their fighting ability could handle it.',
           'Retain the reassurance and its focus on the wielder’s confidence.'),
    3084: (None, 'The adviser calls it a convenient piece of armor.',
           'Retain the brief approving appraisal that suits the simple piece of armor.'),
    3086: (None, 'The adviser recommends having a deckhand keep the shield.',
           'Retain the short recommendation to put the shield in a deckhand’s hands.'),
    3087: (None, 'The armor is light and easy to handle.',
           'Retain both physical qualities in a succinct appraisal.'),
    3097: (None, 'A fighter confident in their skills would do well with equipment of this quality.',
           'Retain the softer recommendation and the caliber of the equipment.'),
    3099: (None, 'This piece is suitable even as the admiral’s own armor.',
           'Retain the sense that the armor is worthy even of the admiral.'),
    3102: (None, 'The adviser pauses, then calls the item truly splendid.',
           'Retain the thoughtful pause and the warm admiration.'),
    3103: (None, 'The item holds a power the adviser finds impossible to put into words.',
           'Retain the feeling of an indescribable power contained within the shield.'),
    3104: (None, 'The adviser exclaims that this is what a true hero should wear.',
           'Retain the emphatic praise and the true hero language.'),
    3105: ("A great conqueror's dignity and bearing... What a sight! This is what makes being a naturalist worthwhile.",
           'The armor has a conqueror’s dignity and bearing. The adviser delights in seeing it and calls this a reward of being a naturalist.',
           'Keep the shift from admiration to personal delight, along with the explicit naturalist reference in the shared reply.'),
    3106: (None, 'The shield would be suitable even as the admiral’s own defense.',
           'Retain the succinct approval and the standard of equipment worthy of the admiral.'),
}
DATA = {n: (item, *DECISIONS[n]) for n, item in zip(IDS, ITEMS, strict=True)}


def main():
    assert ROLES[8] == 'Boarding Leader' and ROLES[15] == 'Deckhand'
    assert set(DECISIONS) == set(IDS)
    env = vars(previous) | globals() | {'RELEASE': parent.RELEASE}
    bindings = checked_text(getsource(previous.bind_advice_callers), {
        'len(cases) == 144': 'len(cases) == len(IDS) * 6',
    })
    exec(compile(bindings, __file__ + '::same-native-item-index-and-speaker', 'exec'), env)
    source = checked_text(getsource(previous.main), {
        "('source_item_cards_and_coin_context_v1.json', 'utility_weapon_item_cards_context_v1.json')":
            "('utility_weapon_item_cards_context_v1.json', 'armor_item_cards_context_v1.json')",
        "row['item_ID'] < len(IDS)": "IDS[0] - FIRST <= row['item_ID'] <= IDS[-1] - FIRST",
        'list(range(len(IDS)))': '[n - FIRST for n in IDS]',
        'and 144 original caller-fragment checks.': "and {len(IDS) * 6} original caller-fragment checks.",
    })
    exec(compile(source, __file__ + '::source-current-and-item-card-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
