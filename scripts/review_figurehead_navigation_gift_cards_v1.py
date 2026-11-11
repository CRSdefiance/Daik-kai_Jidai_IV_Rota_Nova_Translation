"""Review figureheads, navigation instruments and the adjacent gifts from clean Japanese."""

import inspect
from pathlib import Path

from dk4tool.patch.reviewed_item_cards import item_table
from scripts import review_utility_weapon_item_cards_v1 as previous
from scripts.register_crew_equipment_item_cards_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text

OUTPUT = previous.ROOT / 'figurehead_navigation_gift_cards_context_v1.json'
IDS = tuple(n for n in range(2929, 2963) if n != 2931)
DATA = {
    2929: (
        'A great eagle in swift flight. Fit this figurehead and the ship surges ahead.',
        'A figurehead shaped like a large eagle flying swiftly in the sky. When fitted, it makes the ship move faster.',
        'Keep the eagle’s size and motion, then give the effect in plain nautical language.',
    ),
    2930: (
        'Three sweet little pigs make a comforting sight. For some reason, a ship with this figurehead gets by on less food.',
        'A figurehead of three cute, soothing piglets. For some reason, less food is needed on a ship with it.',
        'Keep all three piglets, their comforting effect and the unexplained reduction in food consumption.',
    ),
    2932: (
        'Found after the white whale vanished, this was taken as a sign of its wish for peace. It’s said to help ships stay afloat.',
        'The white whale figurehead was found after the whale disappeared and is taken as a sign that the whale did not want to fight. Fitting it reportedly makes a ship less likely to sink.',
        'Preserve the sequence, the attribution to the whale and the qualified effect on the ship.',
    ),
    2933: (
        'The dragon glares as if ready to strike. This figurehead is said to make the ship’s cannon fire more powerful.',
        'A figurehead of a dragon glaring at an enemy as though about to strike it down. It is said to increase the cannon firepower of the ship carrying it.',
        'Describe the figurehead’s expression and preserve the reported in-game effect.',
    ),
    2934: (
        'A dolphin and its calf swim happily across the open sea. This figurehead is said to help you spot more at sea.',
        'A figurehead of a cute parent dolphin and calf swimming contentedly across the open sea. It supposedly lets you see more things.',
        'Preserve the parent and calf and the reported improvement in what the player can see.',
    ),
    2935: (
        'This figurehead of an innocent maiden brings people comfort and peace with its delicate beauty.',
        'A figurehead shaped like an innocent young woman. Its delicate beauty offers people respite and peace.',
        'Keep the figure and the two emotional effects in a natural sentence.',
    ),
    2936: (
        "An eerie figurehead with a demon's curse, said to have varied effects.",
        'An eerie figurehead imbued with a demon’s curse that seems to have various effects.',
        'Retain the ominous description and the deliberate uncertainty about the effects.',
    ),
    2937: (
        'The king stands at the head of his troops, urging them on. His example lifts the spirits of the crew.',
        'A figurehead of a king leading from the front and encouraging those under him. The sight inspires the sailors.',
        'Keep the king’s position, encouragement and effect on the crew.',
    ),
    2938: (
        "Mary cradles her child in this figurehead. Heaven's protection gives it a mysterious power to ward off illness.",
        'The figurehead depicts the Madonna holding an infant. Wrapped in Heaven’s deep protection, it has a mysterious power to repel illness and similar harms.',
        'Keep the Madonna and child, divine protection and the warding power in two direct sentences.',
    ),
    2939: (
        'Invented in China, this navigation tool is essential for finding your bearings at sea.',
        'A navigational instrument invented in China and indispensable for checking direction at sea.',
        'Keep the Chinese origin and use the ordinary nautical phrase for checking direction.',
    ),
    2940: (
        'A navigation tool for pinpointing your position at sea.',
        'A navigational instrument useful for determining your exact current position at sea.',
        'Name the instrument’s purpose in a compact catalogue phrase.',
    ),
    2941: (
        'Hellenistic astronomer Aristarchus made this telescope, letting you see great distances.',
        'A telescope made by the Hellenistic astronomer Aristarchus, through which one can see a considerable distance.',
        'Retain the established name, period and practical use.',
    ),
    2942: (
        'A glass rose so delicately crafted that it looks like a living bloom frozen in place.',
        'A rose-shaped piece of glasswork so delicate that it looks like a real rose frozen as it was.',
        'Retain the natural image and the contrast between the glass and a real flower.',
    ),
    2943: (
        'These marbles get their vivid colors from a special process their makers keep secret.',
        'Beautifully colored marbles made by a special treatment of the raw materials. The method is kept secret.',
        'Put the colors, process and secrecy together in a complete sentence.',
    ),
    2944: (
        'Finely crushed gold, valuable even as dust. It has a beauty quite unlike that of gold bars.',
        'Gold reduced to grains like sand. It remains valuable and has an appeal distinct from gold ingots.',
        'Preserve its value and the comparison with gold bars in two sentences.',
    ),
    2945: (
        'A stone mill for grinding flour to make bread dough. An ideal gift for a hardworking woman.',
        'A stone mill for grinding flour for bread dough, said to be an excellent gift for a hardworking woman.',
        'Keep the source’s specific gift description and clarify what the stone mill is for.',
    ),
    2946: (
        'A graceful watercolor by Huizong, the Northern Song emperor skilled in painting and calligraphy. It reflects his refined upbringing.',
        'A watercolor painted by Huizong, Northern Song emperor skilled in painting and calligraphy. Its elegance reflects a refined upbringing.',
        'Restore both arts, the imperial title and what the writer attributes the painting’s grace to.',
    ),
    2947: (
        'Legend says a beautiful woman came down from Heaven and forgot this turban when she returned.',
        'A legendary turban said to have been left behind by a beautiful woman who descended from Heaven and forgot it when she returned.',
        'Keep the descent, return and accidental loss, all within the legend.',
    ),
    2948: (
        'A book on love and beauty by Sappho, the ancient Greek poet.',
        'A book of works by the ancient Greek woman poet Sappho, on love and beauty.',
        'Retain the concise entry, author and both themes. Her established name carries the identification.',
    ),
    2949: (
        'A jar unearthed in a layer older than pottery itself, fueling debate among scholars of antiquity.',
        'A jar found in a layer that predates the development of pottery, provoking debate among scholars of antiquity.',
        'Retain the apparent contradiction and the reason for scholarly debate.',
    ),
    2950: (
        'A statue of a beautiful woman, believed to be ancient Greek. It’s considered a masterpiece of its age.',
        'A statue of a beautiful woman believed to date to the Greek period and regarded as a culmination of the skills of its time.',
        'Keep the uncertain attribution and the appraisal of its craftsmanship.',
    ),
    2951: (
        'Stained glass depicts a small flower in a vase. Lovely colors capture its delicate beauty.',
        'Stained glass modeled on a small flower in a single-stem vase. Beautifully colored glass captures the flower’s delicate beauty.',
        'Retain the balanced two sentences and the connection between the color and the delicate flower.',
    ),
    2952: (
        'A gold crown from Silla, the first state to unite the Korean Peninsula. Its ornate work is remarkable for a piece from about the 7th century.',
        'A gold crown made in Silla, the first state to unite the Korean Peninsula. Its ornate workmanship is remarkable for a piece believed to date to around the seventh century.',
        'Keep the source’s geographic term and approximate date and preserve the emphasis on the artistry.',
    ),
    2953: (
        'Earrings of small ceramic beads, beautifully colored by mixing red and white materials.',
        'Earrings made of small ceramic beads, with beautiful coloring achieved by skillfully blending red and white material.',
        'Retain the materials, both colors and the connection between the blend and its appearance.',
    ),
    2954: (
        'A rare, large jade jewel, perfectly round and said to glow white when light falls on it.',
        'A large, beautiful, finely rounded jade bead, particularly rare because it is said to shine white under light.',
        'Retain the readable catalogue phrase, unusual color under light and qualified effect.',
    ),
    2955: (
        'A classic Indian tale completed around the fourth century, about a celestial maiden and a sage who fall in love.',
        'An Indian classic completed around the fourth century. It tells of the love between a celestial maiden and a sage.',
        'Restore the approximate date, remove the full-width capital I and keep the two characters’ identities.',
    ),
    2956: (
        'This pitcher is kept in the Shosoin in Nara. It may have been made in Persia and carried across the sea.',
        'A pitcher held in the Shosoin in Nara. It is said to have been made in Persia and carried from far away by sea, though this is uncertain.',
        'Keep both the place it is held and the uncertainty around its origin and journey.',
    ),
    2957: (
        'Light brings out the vivid blue mottling inside this Chinese tea bowl.',
        'A Chinese tea bowl whose mottled blue pattern becomes vivid when light falls on the inside.',
        'Use one fluid sentence while keeping the origin, use and optical effect.',
    ),
    2958: (
        'An expensive Persian carpet, meticulously handwoven and embroidered with a large sunflower.',
        'A costly Persian carpet carefully woven by hand and embroidered with a large sunflower.',
        'Retain the natural catalogue wording and both kinds of craft.',
    ),
    2959: (
        'A soft silk robe of very thin, pure white cloth, exceptionally light.',
        'A soft silk robe made from very thin pure white cloth. It is exceptionally light.',
        'Retain the readable short description and all three qualities of the cloth.',
    ),
    2960: (
        'A Goryeo celadon incense burner from Korea, prized for the color of its glaze.',
        'A Korean incense burner of Goryeo celadon. The color of its glaze is particularly beautiful.',
        'Keep the specific ceramic tradition and the color as the admired quality.',
    ),
    2961: (
        'A costly magnifier with the world’s largest lens, for clear viewing.',
        'An expensive magnifier that gives a clear view of anything, with the world’s largest lens.',
        'Retain the succinct catalogue wording and the source’s superlative about the lens.',
    ),
    2962: (
        'A colorful tropical bird, uncannily skilled at copying human speech.',
        'A vividly colored bird from warm regions, remarkably good at imitating human speech.',
        'Retain the color, habitat and uncanny gift for mimicry in the established voice.',
    ),
}

source = checked_text(inspect.getsource(previous.main), {
    'category = 1 if ident < 24 else 2': 'category = 5 if ident < 124 else 4 if ident < 127 else 7',
    "kind = 'Utility item' if category == 1 else 'Weapon'":
        "kind = {5: 'Figurehead', 4: 'Navigation instrument', 7: 'Gift'}[category]",
    'utility and weapon cards.': 'figurehead, instrument and gift cards.',
    'evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))}':
        'evidence={str(path): base.digest(path) for path in (RELEASE, Path(previous.__file__), Path(__file__))}',
})
env = vars(previous) | globals()
exec(compile(source, __file__ + '::clean-current-catalogue-review', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    main()
