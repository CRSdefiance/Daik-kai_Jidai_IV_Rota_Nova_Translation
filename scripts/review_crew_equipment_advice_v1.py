"""Review the forty original crew-equipment Advice replies."""

from inspect import getsource

from scripts import register_weapon_armor_advice_v1 as parent
from scripts import review_item_production_advice_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = previous.ROOT / 'crew_equipment_advice_context_v1.json'
IDS = tuple(range(3107, 3147))
BOARDING_BOOK = (
    'A Boarding Leader you can count on knows how to fight and is skilled with a sword.',
    'A leader of the boarding party who excels with a sword and knows how to fight can be relied upon.',
    'Keep reliability, swordsmanship, and wider fighting knowledge. Use the displayed role title.',
)
DATA = {
    3107: ('Magic Leather Gloves', 'Give this to the Sail Handler.',
           'The adviser recommends equipping the person who handles the sails.',
           'Keep the practical recommendation and match the role title shown in the item interface.'),
    3108: ('Tireless Hawser', 'Give this to the Sail Handler on the mainmast.',
           'The adviser suggests giving this to the crew member responsible for the sails on the mainmast.',
           'Keep the exact mast and the role, with the assignment in natural spoken order.'),
    3109: ('Milky Way Chart', None, 'A lookout must know which direction the ship is moving.',
           'Retain the direct explanation of what a lookout needs to know.'),
    3110: ('Starlight Globe', None, 'The lookout must know the ship’s direction with precision.',
           'Retain the emphasis on the exact heading, which distinguishes this advice from the chart.'),
    3111: ("Horace's Poems", None, 'Work on deck is dull, and reading a book of poetry could offer a change of pace.',
           'Retain the familiar complaint and the light recommendation to read poetry.'),
    3112: ('Arabian Nights', None, 'Work on deck is dull, and a story might provide a distraction.',
           'Retain the parallel opening and the different suggestion of a story.'),
    3113: ('World Pun Book', "Deck work is dull. A good joke or two ought to liven things up.",
           'Work on deck is dull, and telling humorous stories or jokes could help pass the time.',
           'Keep the repeated setup and make the spoken humor fit the joke book.'),
    3114: ('Golden Dividers', None, 'The accuracy of a survey chart depends on the quality of the tools.',
           'Retain the concise explanation of why better tools matter.'),
    3115: ('Pocket Watch', None, 'Knowing the exact time makes it possible to calculate the ship’s speed accurately, which should help surveying.',
           'Retain the practical link between timekeeping, speed, and surveying.'),
    3116: ("Rocco's Sailing Guide", "Learn the tricks that come with practice and you'll be a better helmsman for it.",
           'Knowing techniques developed through repeated practice greatly helps a person steer.',
           'Restore the advice about learned technique and keep the benefit to steering. The source gives no number of years.'),
    3117: ('Heavenly Wristband', None, 'The captain’s ability is what calls down the heavens’ protection.',
           'Retain the aphorism linking the captain’s ability to heavenly favor.'),
    3118: ('Guiding Staff', None, 'A captain needs charisma, the ability to draw fellow navigators to them.',
           'Retain the plain observation about charisma and the people it helps win over.'),
    3119: ('Warrior Ocarina', "Keeping the sailors' spirits up is part of a captain's job, too.",
           'Raising the sailors’ morale is another important duty of a captain.',
           'Keep the duty and the addition to the preceding kinds of responsibility. Use a natural spoken idiom for morale.'),
    3120: ('Boastful Beak', 'A First Mate has to talk disgruntled sailors around and negotiate with other factions.',
           'A first mate is responsible for persuading dissatisfied sailors and negotiating with other factions.',
           'Keep both duties and replace the inconsistent “adjutant” with the in-game role name.'),
    3121: ('Travels of Marco Polo', "A voyage is easier on the nerves with a First Mate who knows the world's geography.",
           'It is reassuring to sail with a first mate well versed in world geography.',
           'Keep the reassurance and the reason for it. Match the role title in the game.'),
    3122: ('War Drum', 'A Boarding Leader has to know how to command troops, too.',
           'The leader of the boarding party also needs the ability to command troops.',
           'Restore the leader’s responsibility and the source’s sense of an additional skill.'),
    3123: ("Poseidon's Roar", 'One shout from the Boarding Leader can rally the fighters.',
           'The leader’s single roar can rouse the troops.',
           'Restore the source of the shout, the effect on the fighters, and the one-shout emphasis.'),
    3124: ('Gallic Wars', *BOARDING_BOOK),
    3125: ("Alexander's Campaigns", *BOARDING_BOOK),
    3126: ('Miracle Bullet Charm', 'Luck plays a bigger part in gunnery than you might think.',
           'Unseen luck also plays a large part in gunnery ability.',
           'Give the invisible influence of luck the sound of a wry observation.'),
    3127: ('Gunpowder Manual', 'A Gunner ought to know how gunpowder behaves.',
           'A gunner needs to know the properties of gunpowder.',
           'Restore what the gunner must know about gunpowder and retain the game’s role title.'),
    3128: ('Demon-Piercing Arrow', "This arrow seems to bring an archer's focus to its very limit.",
           'The arrow appears to heighten its archer’s concentration as far as it can go.',
           'Restore both the uncertainty and the strength of the arrow’s apparent effect.'),
    3129: ('Lion-Fang Saw', 'A fine edge like this is a great help to a shipwright.',
           'A wonderfully sharp edge like this is a strong ally for a shipwright.',
           'Keep the praise for this edge and its particular usefulness to a shipwright.'),
    3130: ("Phidias' Chisel", 'What an edge! Any shipwright would be glad to have it.',
           'The adviser marvels at how sharp the tool is and says it is a great help to a shipwright.',
           'Let the more emphatic praise sound like a reaction while keeping the shipwright connection.'),
    3131: ('Self-Sharpening Plane', "An edge like this is a shipwright's best friend.",
           'An edge this sharp is a strong ally for a shipwright.',
           'Use a familiar spoken idiom for a tool that makes a shipwright’s work easier.'),
    3132: ("Herophilus' Medicine", 'Some of the old medical arts were quite remarkable.',
           'There are techniques in old medicine that are still worthy of admiration.',
           'Restore the adviser’s respect for remarkable older techniques.'),
    3133: ('Da Vinci Anatomy', 'Knowing how the body works is the foundation of medicine.',
           'Understanding how the body works is fundamental to medical care.',
           'Restore the whole thought in a spoken sentence.'),
    3134: ('Canon of Medicine', 'I hear medicine in the Islamic world is remarkably advanced.',
           'The adviser has heard that medicine in the Islamic world is highly advanced.',
           'Keep the reported quality and its degree. The phrasing refers to a regional medical tradition.'),
    3135: ("Hestia's Pot", "Wonderful... A cook couldn't ask for a better pot.",
           'The adviser is impressed and calls it the cooking tool of a cook’s dreams.',
           'Keep the admiring pause and make the praise specific to the pot in view.'),
    3136: ('Pink Apron', None, 'Dressing like a cook somehow makes one feel capable of making tasty food.',
           'Retain the playful cause and effect and the speaker’s “somehow.”'),
    3137: ('Gauze Mask', None, 'Tending livestock is harsh work, and the adviser hopes to make it even a little easier.',
           'Retain the practical concern for the people who tend the animals.'),
    3138: ('Stylish Boots', 'Those are stylish boots. They ought to make tending animals more comfortable.',
           'The adviser admires the tall boots and thinks they will make animal care more comfortable.',
           'Keep both the stylish look and the benefit to the wearer during animal care.'),
    3139: ("Gregory's Crown", 'Just the sort of thing missionaries dream of having.',
           'This is an object that missionaries long to have.',
           'Keep the longing and make the appraisal sound spoken.'),
    3140: ('Illustrated Bible', "Here's a Bible anyone can understand.",
           'This is a Bible that anyone can understand.',
           'Restore the claim about who can understand it.'),
    3141: ('Ancient Cross', None, 'The piece makes its history felt.',
           'Retain the concise admiration for an object steeped in history.'),
    3142: ('Art of War', 'The best victory is the one you win without fighting.',
           'Winning without fighting is the best kind of victory.',
           'Restore the maxim as a complete spoken sentence.'),
    3143: ('Gupta Spirit Beast', 'The power to see the future... I wonder if the great strategists of old had that gift.',
           'The adviser wonders whether great strategists of long ago might also have had the power to see the future.',
           'Restore the pause and the adviser’s speculation. The source does not establish that the old strategists could see the future.'),
    3144: ("Hannibal's Campaigns", 'Outwitting the enemy is the heart of strategy.',
           'Turning the tables on the enemy through clever thinking is the essence of strategy.',
           'Give the concise observation its natural cadence and preserve the emphasis on outwitting an opponent.'),
    3145: ('Kinokuniya Abacus', 'They say it can work out even the trickiest totals in the blink of an eye.',
           'It reportedly calculates difficult sums of money in a moment.',
           'Keep the report and the speed, with the abacus and its trade context supplying the kind of total.'),
    3146: ("Vezas' Scales", 'With this, I doubt anyone could overcharge you or buy your goods for a pittance.',
           'With this item the adviser doubts anyone could charge too much or force the price down when buying from the player.',
           'Restore both directions of the price abuse and keep the adviser’s qualified confidence.'),
}


def main():
    env = vars(previous) | globals() | {'RELEASE': parent.RELEASE}
    bindings = checked_text(getsource(previous.bind_advice_callers), {
        'len(cases) == 144': 'len(cases) == len(IDS) * 6',
    })
    exec(compile(bindings, __file__ + '::same-native-item-index-and-speaker', 'exec'), env)
    source = checked_text(getsource(previous.main), {
        "('source_item_cards_and_coin_context_v1.json', 'utility_weapon_item_cards_context_v1.json')":
            "('crew_equipment_item_cards_context_v1.json',)",
        "row['item_ID'] < len(IDS)": "IDS[0] - FIRST <= row['item_ID'] <= IDS[-1] - FIRST",
        'list(range(len(IDS)))': '[n - FIRST for n in IDS]',
        'and 144 original caller-fragment checks.': 'and {len(IDS) * 6} original caller-fragment checks.',
    })
    exec(compile(source, __file__ + '::source-current-and-item-card-review', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
