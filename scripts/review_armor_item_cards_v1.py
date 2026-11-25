"""Review all 25 armor catalogue cards from the clean Japanese."""

import inspect
from pathlib import Path

from dk4tool.patch.reviewed_item_cards import item_table
from scripts import review_utility_weapon_item_cards_v1 as previous
from scripts.register_utility_weapon_item_cards_v1 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = previous.ROOT / 'armor_item_cards_context_v1.json'
IDS = tuple(range(2864, 2889))
DATA = {
    2864: ('Mysterious, rock-hard blue oak forms this small, round shield.',
           'A small round shield made from a mysterious blue oak that is extremely hard.',
           'Retain the natural compact description. It keeps both the unusual wood and the shape of the shield.'),
    2865: ("Made from a large armadillo's hide, this shield is remarkably light and harder than iron.",
           'A shield made from the skin of a large armadillo. It is very light and harder than iron.',
           'Keep both material qualities and describe the animal’s size without implying a specific species.'),
    2866: ('Silver leaf gives this helmet a beautiful shine. A narrow slit lets the wearer see.',
           'A helmet with a slit for the eyes. The surface is covered with silver leaf and shines beautifully.',
           'Replace the clipped catalogue syntax with two direct sentences and keep the silver-leaf finish.'),
    2867: ('A beak-shaped point juts from this helmet. Its crest of a bird in flight stands for courage in the face of death.',
           'A helmet with a point shaped like a beak. Its ornament depicts a bird spreading its wings and symbolizes a spirit that does not fear even death.',
           'Make the two design features clear and preserve the meaning of the bird crest.'),
    2868: ('A shield of giant tortoise shell, far stronger than anything made from ordinary ore.',
           'A shield fashioned from the shell of a giant tortoise, much stronger than one made of ordinary mineral material.',
           'Retain the direct comparison and the shell material.'),
    2869: ("This pure white dress somehow warms the heart. Legend says the spirits protect whoever wears it.",
           'A pure white dress that mysteriously warms the heart of the wearer. Legend says the protection of spirits comes to the person who wears it.',
           'Keep the warmth mysterious and place the spirits’ protection inside the legend.'),
    2870: ("Light, tough martial garb that breaks an attacker's blade.",
           'Light, tough martial arts clothing that breaks the edge of a sword that strikes it.',
           'Retain the short, clear description of the garment and its effect in the catalogue.'),
    2871: ('Breathable yet sturdy, this armor supposedly keeps its wearer cool.',
           'Exceptionally well-ventilated and quite strong armor. The person wearing it is said to feel refreshingly cool.',
           'Retain the contrast between ventilation and strength, and the qualified description of the effect.'),
    2872: ('A sturdy shield carried by the warriors of Kanem, a kingdom that flourished in 11th-century central Africa.',
           'A sturdy shield used by the warriors of Kanem, a state that flourished in central Africa in the eleventh century.',
           'Restore the warriors as the users and make it clear that the kingdom flourished.'),
    2873: ('A knight in the grip of a strange superstition is said to have worn this armor. The design is in dreadful taste.',
           'Armor said to have been worn by a knight in the grip of a dubious superstition. Its design is in extremely poor taste.',
           'Preserve the uncertain attribution and let the blunt judgment land in its own sentence.'),
    2874: ('Linked rings strengthen this armor. Legend says it glowed red in battle when a god protected the knight wearing it.',
           'Joined rings make this armor stronger. Legend says it once shone red in battle and the knight wearing it was protected by a god.',
           'Restore the wearer as a knight while keeping the glow and divine protection attributed to legend.'),
    2875: ('Practical but a little heavy, this chainmail was worn by Timur, ruler of the Timurid Empire that thrived in the 14th century.',
           'A practical suit of chainmail designed above all for use. It is a little heavy. Timur, ruler of the Timurid Empire, which flourished in the fourteenth century, wore it.',
           'Restore Timur’s role and preserve the practical design and weight in a single catalogue sentence.'),
    2876: ('Peacock feathers make this mail a sight to behold. It was made to turn heads, and its protection is modest.',
           'Flashy mail with peacock feathers on the back. It is beautiful and striking, but less sturdy. It was made to stand out more than to be practical.',
           'Keep the creator’s priorities clear and avoid turning the comparative strength into a claim that the mail is weak.'),
    2877: ('Ancient Aztec warriors of Tula are said to have worn this legendary helmet to steel themselves for battle.',
           'A legendary helmet. Ancient Aztec Tula warriors are said to have worn it in battle to rouse their courage.',
           'Keep the helmet as something the warriors used to summon courage and keep the source’s cultural labels.'),
    2878: ('The black garb of Eastern ninja. It offers fine protection and lets them move freely without drawing attention.',
           'Black clothing worn by Eastern ninja. It is excellent protection that allows easy movement and helps them go unnoticed.',
           'Keep the source’s identification, the protection and both practical qualities in natural prose.'),
    2879: ('Fine armor with a mysterious yellow sheen. No one knows what it is made of or when it was made.',
           'A mysterious suit of armor with a glossy yellow color. It offers excellent protection. Its materials and date of manufacture are unknown.',
           'Use two complete sentences and preserve both unknowns.'),
    2880: ('A splendid vest of giant jaguar fur, said to come from the legendary Jaguar God.',
           'A splendid vest made from the fur of a huge jaguar, said to have been bestowed by the legendary Jaguar God.',
           'Retain the concise qualified attribution and the material.'),
    2881: ("This sinister armor was found among a knight's effects. He sold his soul to the devil for power. It is said to choose its wearer.",
           'Frightening armor found among the possessions of a knight who sold his soul to the devil for power. The armor supposedly chooses its wearer.',
           'Restore the discovery and the bargain with the devil, and keep the armor’s choice qualified.'),
    2882: ('This eerie gown offers excellent protection. A tyrannical empress is said to have worn it when she was assassinated.',
           'An eerie-looking but excellent piece of armor. It has a grim past, supposedly having been worn by an empress at the height of her tyranny when she was assassinated.',
           'Keep the protective quality and restore the legend’s uncertainty. The card title identifies the garment.'),
    2883: ('The Taira commander Noritsune wore this fine armor when he drowned at Dan-no-ura.',
           'A fine piece of armor. The Taira clan commander Taira no Noritsune wore it when he went under at Dan-no-ura.',
           'Keep the clan, role, name and location in a complete sentence.'),
    2884: ('Attila, king of the ancient Huns and feared throughout Europe, wore this superb armor.',
           'Superb armor worn by Attila, the king of the ancient Huns who was feared across Europe.',
           'Turn the original fragments into a direct sentence while keeping Attila’s role and reputation.'),
    2885: ("An excellent, eerie shield modeled on Medusa's hair.",
           'An excellent shield with an eerie appearance. Its design takes Medusa’s hair as its motif.',
           'Keep both the quality and the eerie motif, with the possessive and noun together.'),
    2886: ("Saladin, the Muslim hero who fought the Crusaders, wore this armor. It's seen as the mark of a just and virtuous person.",
           'Armor worn by Saladin, the Muslim hero who fought the Crusaders. It is regarded as a sign of a person who combines righteousness and virtue.',
           'Keep Saladin’s identity and the established conflict, and express both qualities in ordinary English.'),
    2887: ("Charles Martel of the Frankish kingdom wore this superb armor at the Battle of Tours-Poitiers. It's sturdy and fit for a king.",
           'Charles Martel of the Frankish kingdom wore this superb armor in the Battle of Tours-Poitiers. It is made to be sturdy and beautiful in a manner befitting a king.',
           'Keep the comparison with royal workmanship distinct from any title for Charles Martel. Correct the full-width F.'),
    2888: ('This stout shield gives off a mysterious glow. It is said to have belonged to Minerva, war goddess and one of the twelve Olympians.',
           'A mysterious, sturdy shield that shines on its own. It is said to belong to Minerva, goddess of war and one of the twelve Olympians.',
           'Restore the spontaneous glow and Minerva’s place among the Twelve.'),
}

source = checked_text(inspect.getsource(previous.main), {
    'category = 1 if ident < 24 else 2': 'category = 3',
    "kind = 'Utility item' if category == 1 else 'Weapon'": "kind = 'Armor'",
    'utility and weapon cards.': 'armor cards.',
    'evidence={str(path): base.digest(path) for path in (RELEASE, Path(__file__))}':
        'evidence={str(path): base.digest(path) for path in (RELEASE, Path(previous.__file__), Path(__file__))}',
})
env = vars(previous) | globals()
exec(compile(source, __file__ + '::original-clean-current-item-review', 'exec'), env)
main = env['main']


if __name__ == '__main__':
    main()
