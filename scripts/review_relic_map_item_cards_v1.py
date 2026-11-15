"""Review the forty base-game proofs, maps and map materials against clean Japanese."""

import inspect
from pathlib import Path

from dk4tool.patch.reviewed_item_cards import item_table
from scripts import review_utility_weapon_item_cards_v1 as previous
from scripts.register_figurehead_navigation_gift_cards_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text

OUTPUT = previous.ROOT / 'relic_map_item_cards_context_v1.json'
IDS = tuple(range(2963, 3003))
DATA = {
    2963: (
        'A yew bow said to be wielded by Ullr, the Norse god of hunting and a master archer.',
        'A bow made from yew, said to have been used by Ullr, a master archer and the god of hunting in Norse myth.',
        'Retain the qualified attribution, material, tradition and skill.',
    ),
    2964: (
        'Cambyses had this legendary crown made to show his power. He expanded the Achaemenid realm around the 5th century BC.',
        'A legendary crown commissioned by King Cambyses to display his authority. He extended Achaemenid territory around the fifth century BC.',
        'Keep the commission and its purpose clear, and retain the approximate dating in the source.',
    ),
    2965: (
        'A king of Aksum is said to have stamped documents with this solid gold seal. Aksum, a precursor to Ethiopia, thrived from the 2nd to 6th century.',
        'A pure gold seal that a king of Aksum reportedly used on documents. Aksum preceded Ethiopia and flourished from the second through sixth centuries.',
        'Keep the use attributed to a king and retain the state’s link to Ethiopia and period of prosperity.',
    ),
    2966: (
        "India's oldest text, dated to about the 15th to 10th centuries BC. It reflects early Aryan life and helped shape Indian thought.",
        'The oldest text from India, said to have taken shape around the fifteenth to tenth centuries BC. It reflects the worldview of early Aryans and became a source of Indian thought.',
        'Restore the perspective reflected in the text and its influence on Indian thought.',
    ),
    2967: (
        'A wooden plaque from Kediri, a kingdom that thrived in Indonesia from the 10th to 13th century. It is said to protect every islander.',
        'A wooden plaque handed down in Kediri, a kingdom that flourished in Indonesia from the tenth through thirteenth centuries. It reportedly protects every islander from harm.',
        'Restore the place and period and keep the protective effect attributed.',
    ),
    2968: (
        'A bronze candlestick said to have been used by Qin Shi Huang, who had it made in the 3rd century BC while building palaces like Epang.',
        'A bronze candlestick said to have been used by the Qin emperor Qin Shi Huang. He had it made when building grand palaces such as Epang Palace in the third century BC.',
        'Restore the date, the commission and the named palace while keeping the attribution qualified.',
    ),
    2969: (
        'A polished crystal skull whose creation remains a mystery.',
        'Crystal polished and shaped into a skull. How it was made remains a mystery.',
        'Retain the concise wording and the distinction between the visible material and the unknown method.',
    ),
    2970: (
        'An old map drawn on paper.',
        'An old map drawn on paper.',
        'Retain the compact wording and the identifying material.',
    ),
    2971: (
        'An old map drawn on cloth.',
        'An old map drawn on cloth.',
        'Retain the matching catalogue syntax and the cloth medium.',
    ),
    2972: (
        'An old map carved into a stone tablet.',
        'An old map incised on a stone tablet.',
        'Specify the tablet so the clue identifies the kind of object.',
    ),
    2973: (
        'An old map drawn on a mysterious lotus leaf that never withers.',
        'An old map drawn on a mysterious lotus leaf that does not wither.',
        'Use the literal physical property of the leaf and retain its mysterious nature.',
    ),
    2974: (
        'An old map disguised as a pattern.',
        'An old map in which something that looks like a pattern serves as the map.',
        'Retain the short clue and the pattern that doubles as a map.',
    ),
    2975: (
        'An old map drawn inside a thick piece of bamboo split open.',
        'An old map drawn on the inside of a thick piece of split bamboo.',
        'Restore the size of the bamboo and make the map’s location clear.',
    ),
    2976: (
        'An old map carved on a large knife blade.',
        'An old map carved on the blade of a large knife.',
        'Retain the natural clue and keep the location of the engraving specific.',
    ),
    2977: (
        'A detailed map of southern England with a mysterious mark.',
        'A detailed map of southern England marked with a mysterious symbol.',
        'Use southern England naturally and restore the map’s detail.',
    ),
    2978: (
        'A map of the ancient Roman capital and its surroundings. It covers nearly all of Italy.',
        'A map of the surroundings of the ancient Roman Empire’s capital, covering almost all of Italy.',
        'Keep the capital, its environs and the map’s geographic extent.',
    ),
    2979: (
        'An old map of Anatolia marking the site of a hidden Christian village.',
        'An old map of Anatolia marked with the location of a hidden Christian village.',
        'Use a complete catalogue phrase and keep the region and community intact.',
    ),
    2980: (
        'Caravans trading with legendary Timbuktu use this map of the Sahara. It shows the city in the heart of the desert.',
        'A desert map used by caravans trading with the legendary city of Timbuktu in the middle of the Sahara.',
        'Restore the city’s position and keep the relationship between the map and the caravans.',
    ),
    2981: (
        "A mysterious map with the King's Mosque marked at its center.",
        'A mysterious map marked in the middle with a label reading King’s Mosque.',
        'Retain the name and placement of the mark in natural English.',
    ),
    2982: (
        'A detailed map of the vast Mughal Empire in northern India. It shows the way to the capital, Delhi.',
        'A detailed map of the vast Mughal Empire in northern India showing the route to the capital at Delhi.',
        'Restore northern India, the scale of the empire and Delhi’s role as the capital in the source.',
    ),
    2983: (
        'A map from an ancient Cambodian dynasty. At its center is what looks like a royal palace and temple in one.',
        'A map from the time of an ancient Cambodian dynasty. A building drawn in the center appears to serve as both royal palace and temple.',
        'Keep the historical setting and restore the uncertainty around the building.',
    ),
    2984: (
        'A detailed map of northern China showing the route to the capital, Beijing.',
        'A detailed map of northern China showing the way to Beijing, the capital.',
        'Restore the degree of detail and identify Beijing as the capital.',
    ),
    2985: (
        "A partly illegible map leading to a great king's tomb.",
        'A map showing how to reach a great king’s tomb. Parts of it cannot be read.',
        'Retain the concise clue and the unreadable portions.',
    ),
    2986: (
        'A map leading to a legendary temple in golden Zipangu.',
        'A map showing the route to a legendary temple built in Zipangu, the land of gold.',
        'Retain the established name and the association with gold.',
    ),
    2987: (
        'A detailed map of the route between a distant island and an ancient city now in ruins.',
        'A map recording in detail the travel between a distant island and an ancient city that is now in ruins.',
        'Restore the detail and the contrast between the city’s age and its present state.',
    ),
    2988: (
        'An illustrated record of the cultural roots of the Aztec kingdom, complete with a map of the realm.',
        'A pictorial record of the cultural roots of the Aztec kingdom with an illustrated map of the kingdom.',
        'Restore the purpose of the document as well as the map it contains.',
    ),
    2989: (
        'A blank piece of parchment. Its purpose is a mystery.',
        'Parchment with nothing drawn on it. What it was used for is unknown.',
        'Keep the object plainly described and give its unexplained purpose its own sentence.',
    ),
    2990: (
        'Cloth covered in strange patterns.',
        'A piece of cloth marked with mysterious patterns.',
        'Retain the direct description and the clue carried by the pattern.',
    ),
    2991: (
        'The upper half of a stone tablet carved with a mysterious design.',
        'The upper half of a stone tablet engraved with a mysterious pattern.',
        'Restore the material and the patterned engraving, matching the lower half.',
    ),
    2992: (
        'A lotus leaf said to have stayed alive since ancient times without ever withering.',
        'A lotus leaf said to have lived since remote antiquity without withering.',
        'Keep the claim attributed and make the leaf’s distinctive property explicit.',
    ),
    2993: (
        'A coin believed to come from an ancient kingdom. Its pictures and lettering are too corroded to make out.',
        'A coin thought to have been used in an ancient kingdom, with pictures and lettering corroded beyond recognition.',
        'Restore the uncertain provenance and identify both things the corrosion has obscured.',
    ),
    2994: (
        'Intricate bamboo work believed to have been made in China during the Tang dynasty.',
        'Very finely made bamboo craft thought to have been produced in Tang-dynasty China.',
        'Preserve the artistry and restore the uncertainty about when and where it was made.',
    ),
    2995: (
        'A knife used in ceremonies by an ancient New World dynasty. Its blade is too dull to serve as a weapon.',
        'A knife used in ceremonies by an ancient dynasty of the New World. It lacks the sharpness to serve as a weapon.',
        'Distinguish its ceremonial use from the condition of the blade and keep the setting.',
    ),
    2996: (
        'A vivid pigment of a kind rarely used. No one knows what it was made from.',
        'A brightly colored pigment of a kind not in general use, made from unknown ingredients.',
        'Keep the rarity and unknown materials without adding a claim about which painters used it.',
    ),
    2997: (
        'A brass lamp apparently used in ceremonies.',
        'A brass lamp that appears to have been used in ceremonies and similar occasions.',
        'Retain the concise wording and the qualified use.',
    ),
    2998: (
        'The lower half of a stone tablet carved with a mysterious design.',
        'The lower half of a stone tablet engraved with a mysterious pattern.',
        'Restore the material and engraving and mirror the wording of the upper half.',
    ),
    2999: (
        'Made in ancient India, this platter appears to have been used as tribute to another country.',
        'An object made in ancient India that seems to have been used as tribute to another country.',
        'Use the catalogue title for the object and retain the apparent purpose and direction of the tribute.',
    ),
    3000: (
        'A small jar filled with a milky white liquid.',
        'A small jar filled with milky white liquid.',
        'Restore the size and describe the visible contents without identifying the liquid.',
    ),
    3001: (
        'An illustrated plan showing in detail how to assemble the bamboo craft.',
        'A detailed illustrated plan for assembling the bamboo craft.',
        'Restore the detail, the illustrations and what the plan assembles.',
    ),
    3002: (
        'A dagger sheath carved with a sun emblem.',
        'A sheath for a small knife carved with a design shaped like the sun.',
        'Retain the compact description and the engraved emblem.',
    ),
}

source = checked_text(inspect.getsource(previous.main), {
    'category = 1 if ident < 24 else 2': 'category = 8 if ident < 155 else 9 if ident < 162 else 10 if ident < 174 else 6',
    "kind = 'Utility item' if category == 1 else 'Weapon'":
        "kind = {8: 'Proof', 9: 'Named map', 10: 'Ruins map', 6: 'Map material'}[category]",
    'utility and weapon cards.': 'proof, map and map material cards.',
    'evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))}':
        'evidence={str(path): base.digest(path) for path in (RELEASE, Path(previous.__file__), Path(__file__))}',
})
env = vars(previous) | globals()
exec(compile(source, __file__ + '::clean-current-relic-map-review', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    main()
