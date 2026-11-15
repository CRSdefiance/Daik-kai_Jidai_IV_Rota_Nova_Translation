"""Review the 40 consecutive crew-role equipment descriptions from clean Japanese."""

import inspect
from pathlib import Path

from dk4tool.patch.reviewed_item_cards import item_table
from scripts import review_utility_weapon_item_cards_v1 as previous
from scripts.register_armor_item_cards_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_item_interface_research import ATTRIBUTE_ROLES

OUTPUT = previous.ROOT / 'crew_equipment_item_cards_context_v1.json'
IDS = tuple(range(2889, 2929))
DATA = {
    2889: (
        'These magic leather gloves protect your hands when you raise or lower the mast.',
        'Mysterious leather gloves that protect the hands when raising or lowering a mast.',
        'Name both actions and keep the plain instruction-like tone of the catalogue.',
    ),
    2890: (
        'A thick, pure white rope for the mast. For some reason, using it makes you want to work harder.',
        'A thick, pure white rope used on the mast. For some mysterious reason it raises the user’s desire to work.',
        'Preserve the color and intended use, then let the odd benefit speak for itself.',
    ),
    2891: (
        'A scroll showing the stars of the Milky Way. A navigator with time to spare is said to have drawn it from the night sky.',
        'A scroll depicting the stars of the Milky Way. It is said to have been drawn by a navigator with nothing to do but look up at the night sky.',
        'Restore the scroll and use time to spare to avoid calling the navigator lazy.',
    ),
    2892: (
        'This mysterious celestial globe uses starlight to show where the stars are.',
        'A mysterious celestial globe built to project star positions by the light of the stars in the night sky.',
        'Identify the celestial globe and keep the source of the light and what it shows.',
    ),
    2893: (
        'Horace, a poet born in Rome before the Common Era, urges us to enjoy the day without being ruled by desire.',
        'These are the works of Horace, a Roman poet born before the Common Era. He urges people to enjoy the day without becoming captive to excessive desire.',
        'Use neutral dating and retain both sides of the advice.',
    ),
    2894: (
        'This collection of folktales comes mainly from Arabia. A young woman tells one story after another over 1,001 nights.',
        'A collection of folk tales chiefly from Arabia. A young woman tells a variety of tales over a thousand and one nights.',
        'Keep Arabia as the principal origin and preserve the frame story and exact number of nights.',
    ),
    2895: (
        'A collection of groan-worthy puns from around the world. Its compiler is said to have been Japanese.',
        'A book full of unfunny puns gathered from around the world, said to have been compiled by a Japanese person.',
        'Give the dry joke a natural English turn and distinguish the compiler from the original authors.',
    ),
    2896: (
        'The king of a once-great realm is said to have spared no expense on these solid-gold dividers for his finest navigators.',
        'Very expensive solid-gold dividers. A king in a country at the height of its splendor is said to have spent lavishly to make them for skilled navigators.',
        'Preserve the traditional attribution, the outlay and the intended recipients.',
    ),
    2897: (
        'A pocket watch with the Madonna inside its lid, said to bring blessings.',
        'A pocket watch with a picture of the Madonna inside its lid. It is said to bring protection to whoever carries it.',
        'Retain the concise reference to the image and the attributed blessing.',
    ),
    2898: (
        'The veteran navigator Rocco tells his life story in a rough, blunt style. His book doubles as a guide to handling a ship.',
        'A useful shiphandling guide by the veteran navigator Rocco. He wrote his autobiography in a rough style.',
        'Keep the established Rocco spelling and clarify how the memoir serves as a practical guide.',
    ),
    2899: (
        'The angel carved in relief on this mysterious bracelet brings divine favor.',
        'A mysterious bracelet whose angel carved in relief brings heavenly favor.',
        'State the link to the angel and keep the carving technique visible.',
    ),
    2900: (
        'A leader who carries this mysterious staff is said to guide every follower toward good.',
        'A staff with a mysterious power. When carried by the leader of a group, it supposedly guides all who follow toward good.',
        'Preserve the condition that the staff is held by a leader and the broad effect on the group.',
    ),
    2901: (
        'A dove-shaped instrument whose soft, clear tone is said to calm listeners and inspire them to act.',
        'A dove-shaped instrument. Its clear, soft tone is said to calm those who hear it and kindle their motivation.',
        'Retain the natural description and both reported effects.',
    ),
    2902: (
        'A strange ornament makes its owner spout one tall tale after another.',
        'A mysterious ornament that somehow causes the person who holds it to blurt out one made-up statement after another.',
        'Retain the comically blunt verb and the repeated tall tales.',
    ),
    2903: (
        "Completed in the 13th century, this book tells what Marco Polo saw and heard on his travels in the East.",
        'A book completed in the thirteenth century that collects what Marco Polo saw and heard on his journey to the East.',
        'Restore what the traveler saw and heard, and keep the source’s dating and direction.',
    ),
    2904: (
        'This drum sounds on the battlefield to signal troops to advance or withdraw.',
        'A drum sounded on the battlefield to signal the advance or retreat of troops.',
        'State that the drum relays the signal and keep both possible orders.',
    ),
    2905: (
        'This necklace holds the soul of Poseidon, god of the sea and one of the twelve Olympians. It is a symbol of courage.',
        'A necklace containing the soul of Poseidon, the sea god and one of the twelve Olympians. It symbolizes courage.',
        'Restore Poseidon’s place among the Twelve and keep the symbolism distinct.',
    ),
    2906: (
        'Caesar wrote this account in the first century BC. It details nearly seven years of war against the Gauls.',
        'Caesar wrote this book in the first century BC. It describes in detail nearly seven years of war against the Gauls.',
        'Keep the date and duration and name the people the campaign was against.',
    ),
    2907: (
        'An account of the routes taken by Alexander, king of Macedon, on his campaigns in the fourth century BC.',
        'A text detailing the course of the campaigns of Alexander, king of Macedon in the fourth century BC.',
        'Make Alexander’s role and period clear and retain the focus on his routes.',
    ),
    2908: (
        'A bullet-shaped charm said to bring miraculous luck.',
        'A bullet-shaped pendant said to carry luck capable of calling forth miracles.',
        'Retain the clear description, the object’s shape and the qualified effect.',
    ),
    2909: (
        'A scroll recording exact proportions and preparation conditions for refining gunpowder.',
        'A scroll that precisely records the mixture and preparation conditions for refining gunpowder.',
        'Keep the nature and precision of the in-game document in catalogue language.',
    ),
    2910: (
        'A legendary arrow from the age of myth, said to have been used by angels against demons.',
        'A legendary arrow that angels supposedly used to strike down demons in the age of myth.',
        'Restore the uncertainty and place the story in the age of myth.',
    ),
    2911: (
        "A master craftsman's saw passed down from antiquity. It's said to have been used to build an emperor's throne room.",
        'A master craftsman’s saw passed down from long ago, said to have been used when an emperor’s chamber was built in antiquity.',
        'Preserve the handed-down craftsmanship and the traditional attribution.',
    ),
    2912: (
        'A sharp chisel said to have been favored by Phidias, the ancient Greek sculptor. An artist’s spirit is said to dwell in it.',
        'A keen chisel said to have been favored by Phidias, a Greek sculptor from before the Common Era. The spirit of an artist is said to inhabit it.',
        'Keep both attributions qualified and avoid identifying the spirit more specifically than the source.',
    ),
    2913: (
        'A superb plane with a diamond blade that never chips.',
        'An excellent woodworking plane whose diamond blade does not chip.',
        'Retain the clear short entry and its exact material and benefit.',
    ),
    2914: (
        'The world’s oldest medical book, compiled by Herophilus, a pioneer of medicine in the Hellenistic age.',
        'The world’s oldest medical book, compiled by Herophilus, a forefather of medicine in the Hellenistic era.',
        'Restore the source’s worldwide superlative and the role of the compiler.',
    ),
    2915: (
        'An up-to-date medical text by Italian genius Leonardo da Vinci, drawing on his own study of the human body.',
        'An up-to-date medical book in which the Italian genius Leonardo da Vinci compiled the findings of his research on the human body.',
        'Restore the scope of his own research and use an ordinary capital I.',
    ),
    2916: (
        'A comprehensive medical text written in the Muslim world in the 11th century.',
        'A comprehensive work on medicine written in the Islamic world in the eleventh century.',
        'Use natural catalogue wording and keep the period and broad geographic context.',
    ),
    2917: (
        'This pot is said to have belonged to Hestia, hearth goddess and one of the twelve Olympians. Add ingredients and it cooks on its own.',
        'A pot said to have belonged to Hestia, the hearth goddess and one of the twelve Olympians. Put ingredients inside and they cook on their own.',
        'Restore Hestia’s place among the Twelve and keep the self-cooking effect simple.',
    ),
    2918: (
        'A cute pink apron. Whether it suits rough sailors is another matter.',
        'A very cute apron. Whether pink looks right on seamen, many of whom are rough characters, is another question.',
        'Retain the dry second sentence and the joke about the contrast between the apron and its wearer.',
    ),
    2919: (
        'A small mask invented to keep out smells from the Livestock Room. Each one is made by hand with care.',
        'A small mask invented to protect against bad smells from the animal room. Each is carefully handmade.',
        'Keep the singular item and use the established Livestock Room label.',
    ),
    2920: (
        'It takes a lot of precious rubber to make these stylish boots and keep feet clean in the Livestock Room.',
        'Stylish rubber boots made with a large amount of precious rubber because the wearer’s feet inevitably get dirty in the animal room.',
        'Keep the unusual use of precious rubber and use the established Livestock Room label.',
    ),
    2921: (
        'Pope Gregory VII wielded great authority in the 11th century. His crown symbolizes the absolute power of the papacy.',
        'The crown of Pope Gregory VII, who wielded authority in the eleventh century. It symbolizes the absolute power of the pope.',
        'Identify the pope explicitly and preserve the nature of the symbol.',
    ),
    2922: (
        'An illustrated Bible that clarifies difficult passages.',
        'A Bible whose difficult parts have been made easier to understand by adding illustrations.',
        'Retain the compact wording and the reason for the illustrations.',
    ),
    2923: (
        'Made the year Christ died, this miraculous cross resurfaced after over a thousand years underground.',
        'A miraculous cross made in the year of Christ’s death. It lay underground for more than a thousand years before appearing at the surface.',
        'Retain the clear chronology and the miraculous character of the item.',
    ),
    2924: (
        'Chinese strategist Sun Tzu wrote mostly about land warfare. Few of his lessons apply at sea, but those that do are useful.',
        'A treatise by the Chinese strategist Sun Tzu. Much of it concerns land warfare. Little applies at sea, although that part is useful.',
        'Restore the author’s role and keep the qualification that only some lessons apply at sea.',
    ),
    2925: (
        'This bronze figure likely comes from India’s fifth-century Gupta dynasty. It is said to foretell success or failure.',
        'A bronze statue believed to have been made in the fifth-century Indian Gupta dynasty, said to foretell whether something will succeed or fail.',
        'Restore India and keep both the provenance and reported ability qualified.',
    ),
    2926: (
        'A chronicle of the Carthaginian general Hannibal’s war with Rome before the Common Era. It tells of his unusual tactics.',
        'A chronicle of the Carthaginian general Hannibal, who fought Rome before the Common Era. It describes his distinctive and unusual strategy.',
        'Restore the role of general and give the date and description separate phrases.',
    ),
    2927: (
        'Merchants in China and Japan use this tool to calculate by flicking its beads with their fingers.',
        'A commercial counting tool used in China and Japan. Calculations are done by flicking its beads with the fingers.',
        'Keep both countries and describe how the merchant uses it in one clear sentence.',
    ),
    2928: (
        'A set of trading scales once used by a famous Muslim merchant. They are precise to the smallest measure.',
        'A trade balance used by a famous Muslim merchant. It is highly precise without the slightest error.',
        'Preserve the merchant’s role and the unusual accuracy in direct catalogue prose.',
    ),
}

source = checked_text(inspect.getsource(previous.main), {
    'category = 1 if ident < 24 else 2': 'category = 4',
    "kind = 'Utility item' if category == 1 else 'Weapon'": '''kind = 'Crew equipment'
        assert clean[field + 18:field + 20] == arm[field + 18:field + 20]
        role_attribute, effect = arm[field + 18:field + 20]
        role = ATTRIBUTE_ROLES[role_attribute]
        assert 0 <= role < 16''',
    "private_pointer_field=table + 4 * ident, native_callers=consumers,": '''private_pointer_field=table + 4 * ident, native_callers=consumers,
            native_role_attribute=role_attribute, native_role_index=role, native_role_effect=effect,''',
    'utility and weapon cards.': 'crew equipment cards.',
    'evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))}':
        'evidence={str(path): base.digest(path) for path in (RELEASE, Path(previous.__file__), Path(__file__))}',
})
env = vars(previous) | globals()
exec(compile(source, __file__ + '::clean-current-crew-catalogue', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    main()
