"""Source-faithful sea/sailor data articles behind the ongoing plaque audit."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare

PROSE = {
    153: ('Sea Info',
          'These values are displayed at sea. See [[154|Coordinates]], [[155|Food and Water]], [[156|Sailors]] and [[157|Fatigue]].',
          'Sea HUD data: latitude/longitude, food/water, fleet sailors and fatigue.',
          'Keep all four original data links and distinguish ordinary sailors from officers.'),
    154: ('Coordinates',
          'These are your current latitude and longitude. They are displayed when you have a highly skilled [[123|Surveyor]].',
          'Current latitude/longitude appear with a high-ability surveyor.',
          'Keep the surveyor condition; the source gives no numeric threshold here.'),
    155: ('Food and Water',
          'These are the barrels of food and water remaining. Running out of food or water causes crew fatigue to rise sharply.',
          'Remaining food/water barrel counts; zero causes a sharp fatigue increase.',
          'Explain the displayed units and shortage effect without inventing a daily consumption rate.'),
    156: ('Sailors',
          'This is the total number of sailors in your fleet. If no sailors remain, the game ends.',
          'Fleet-wide sailor count; zero means Game Over.',
          'Retain the exact zero-crew consequence rather than generic recruitment advice.'),
    157: ('Fatigue',
          'This is your crew\'s fatigue. When it reaches 100, you begin losing sailors. High fatigue can also lead to a mutiny.',
          'Crew fatigue100 starts sailor loss; high fatigue may cause rebellion.',
          'Keep the100 threshold and the possibility, not certainty, of mutiny.'),
    158: ('Sailor Info',
          'View an officer\'s data. See [[159|Mood]], [[160|Health]], [[161|Attributes]], [[168|HP and Health]], [[169|Level]], [[170|Skills]] and [[180|Equipped Items, Weapons and Armor]].',
          'Character data links to mental state, physical state, basic abilities, HP/vitality, level, skills and equipped item/weapon/armor.',
          'Match existing plaques. HP and Health names the existing vitality skill; the separate Health link explains current condition.'),
    159: ('Mood',
          'An officer\'s mood has six states: Excited, Good, Relaxed, Normal, Upset and Confused. Upset or Confused officers work less efficiently. Assign an officer to [[111|a Private Cabin]] or [[112|the Recreation Room]] to improve their mood.',
          'Six mental states; bad temper/confusion reduce work efficiency. Private/recreation rooms restore mental condition.',
          'Use the six current source-reviewed native labels, including Confused; preserve both recovery links.'),
    160: ('Health',
          'An officer\'s physical condition has six states: Healthy, Tired, Hurt, Wounded, Dying and Sick. Poor health reduces work efficiency or can prevent an officer from working. Assign them to [[111|a Private Cabin]] to recover. A [[114|Doctor]] can treat Sick officers with items such as medicine.',
          'Six physical states; poor condition reduces/prevents work. Private cabin restores health; ship doctor using medicine/items cures disease.',
          'Use current Hurt/Wounded distinction. Preserve the Doctor-and-item requirement; do not add Dead to the source list.'),
    161: ('Attributes',
          'Attributes represent an officer\'s innate abilities and affect their skills. See [[162|Stamina]], [[163|Agility]], [[164|Charm]], [[165|Wits]], [[166|Spirit]] and [[167|Luck]].',
          'Six innate basic abilities influence skill values.',
          'Keep the six established plaque terms and every original destination.'),
    162: ('Stamina',
          'Stamina measures physical toughness. Higher Stamina makes an officer less likely to collapse.',
          'Body robustness; higher values reduce tendency to collapse.',
          'Do not invent a direct HP formula or guaranteed immunity.'),
    163: ('Agility',
          'Agility measures speed and dexterity. Higher Agility gives an officer an advantage in battle.',
          'Quickness/dexterity; high values improve combat advantage.',
          'Preserve both senses rather than reducing this attribute to movement speed.'),
    164: ('Charm',
          'Charm measures charisma and personal presence. Higher Charm makes it easier to win people over.',
          'Charisma and breadth of character; high values win others\' support more easily.',
          'Personal presence conveys the source\'s broad appeal without restricting it to physical beauty.'),
    165: ('Wits',
          'Wits measures wisdom and knowledge. Higher Wits helps an officer handle situations more effectively.',
          'Wisdom/knowledge; higher values improve handling of situations.',
          'Use the established concise plaque term; do not invent an event-specific bonus.'),
    166: ('Spirit',
          'Spirit measures strength of will. Higher Spirit helps an officer stay calm in a crisis.',
          'Strength of will; high values reduce panic in adversity.',
          'Distinguish the permanent Spirit attribute from the current Mood condition.'),
    167: ('Luck',
          'Luck measures good fortune. Higher Luck makes it easier to escape dangerous situations.',
          'Fortune; high values help avoid crises.',
          'Do not promise automatic avoidance of every danger.'),
    168: ('HP and Health',
          'Injuries, such as those suffered in [[99|duels]], reduce HP. At zero HP, an officer becomes Dying. HP gradually returns when the officer stays at an inn or is assigned to [[111|a Private Cabin]] or [[112|the Recreation Room]]. The Health skill represents maximum HP and physical resilience. Higher Health makes illness less likely and suits [[116|Animal Keepers]] and [[126|Deckhands]]. It is influenced by Stamina and Spirit.',
          'Injury/duels lower HP; zero gives near-death condition. Inn/private/recreation rooms gradually restore it. Vitality indicates maxHP/robustness, disease resistance and suitability for keeper/deck crew; Stamina/Spirit influence it.',
          'Health is the current vitality skill label, distinct from current physical condition. Preserve gradual recovery, five links and both related attributes.'),
    169: ('Level',
          'Level represents an officer\'s sailing experience. It rises as they gain experience through activities such as sailing.',
          'Voyage level rises through sailing and other experience.',
          'Do not claim sailing is the only source of experience.'),
    170: ('Skills',
          'Skills show which jobs suit an officer. Starting values differ between officers and rise when they level up. Equipping certain items can also raise skills. See [[171|Command]], [[172|Sailing]], [[174|Survey]], [[176|Finance]], [[179|Observe]], [[168|HP and Health]], [[173|Aim]], [[178|Combat]], [[175|Social]] and [[177|Tactics]].',
          'Job suitability; basic skill values vary by officer and rise at level-up. Some equipment raises some skills. Ten original skill destinations.',
          'Preserve all ten links in original order and use the exact existing Sailor Info skill labels.'),
    171: ('Command',
          'Command measures an officer\'s ability to lead sailors and companions as a captain or admiral. Higher Command makes an officer a better leader. It is influenced by Spirit and Charm.',
          'Leadership of crew/companions as captain or admiral; high values suit leaders. Spirit/Charm relate.',
          'Retain both leadership contexts and both related attributes.'),
    172: ('Sailing',
          'Sailing measures ship-handling skill. Higher Sailing makes ship operations faster and suits [[122|Helmsmen]] and [[125|Sail Masters]]. It is influenced by Agility and Spirit.',
          'Ship handling ability; high values speed operations and suit helmsman/sail handler; Agility/Spirit relate.',
          'Preserve both roles and the ship-operation benefit rather than promising unrestricted faster travel.'),
    173: ('Aim',
          'Aim measures focus on a target. Higher Aim improves cannon accuracy in battle and helps an officer prepare good meals. It suits [[129|Gunners]] and [[115|Cooks]] and is influenced by Agility and Luck.',
          'Target concentration helps cannon accuracy and cooking; gunner/cook suitability; Agility/Luck relate.',
          'Keep the less obvious cooking benefit because it is explicit in the Japanese source.'),
    174: ('Survey',
          'Survey measures surveying and mapmaking skill. Higher Survey lets an officer determine the fleet\'s position accurately over a wider area. It suits [[123|Surveyors]] and [[113|Shipwrights]] and is influenced by Agility and Wits. Equipping items such as a sextant raises Survey. Give them to the officer assigned as Surveyor.',
          'Survey/chartmaking allows accurate position determination over broader area; surveyor/shipwright suitability; Agility/Wits relate. Sextant and similar equipment raise Survey; equip assigned surveyor.',
          'Keep wider-area accuracy and the equipment advice; do not replace Shipwright with a guessed navigation role.'),
    175: ('Social',
          'Social measures diplomatic ability. Higher Social suits [[121|Adjutants]] and [[117|Missionaries]]. It is influenced by Wits and Charm.',
          'Diplomatic aptitude; high values suit deputy/missionary; Wits/Charm relate.',
          'Use the existing Social skill label while explaining its diplomatic meaning.'),
    176: ('Finance',
          'Finance measures accounting ability. Higher Finance helps you negotiate lower buying prices and higher selling prices when trading. It suits [[119|Accountants]] and is influenced by Wits and Spirit.',
          'Accounting ability; high values enable haggling down/marking up in trade and suit chief accountant; Wits/Spirit relate.',
          'Keep both buying and selling benefits; do not add Social as a governing attribute.'),
    177: ('Tactics',
          'Tactics measures skill at devising schemes. Higher Tactics makes it easier to come up with strategies and suits [[118|Strategists]]. It is influenced by Wits and Luck.',
          'Cunning strategy; high values inspire schemes and suit adviser/strategist; Wits/Luck relate.',
          'The established Tactics label covers scheming here, not only battlefield formations.'),
    178: ('Combat',
          'Combat measures swordsmanship. Higher Combat gives an officer an advantage in [[98|boarding battles]] and [[99|duels]] and suits [[128|Marine Leaders]]. It is influenced by Stamina and Agility.',
          'Sword aptitude benefits close-quarters battle/duels and suits boarding leader; Stamina/Agility relate.',
          'Explain swordsmanship behind the existing Combat label; preserve all three original links.'),
    179: ('Observe',
          'Observe measures an officer\'s ability to notice their surroundings and sense danger. Higher Observe helps them spot distant objects and treat illness. It suits [[124|Lookouts]] and [[114|Doctors]] and is influenced by Spirit and Luck.',
          'Discovery/danger perception; high values help distant spotting and disease treatment; lookout/doctor suitability; Spirit/Luck relate.',
          'Keep medical usefulness and both roles; Health is not the Doctor\'s skill in this source.'),
    180: ('Equipped Items',
          'These are the items, weapons and armor currently equipped. Select an empty slot to equip something. Select an equipped item to remove it.',
          'Currently equipped item/weapon/armor; select empty to equip, occupied to unequip.',
          'Restore actual slot behavior; omit unrelated item-use/red-job advice from the old generic text.'),
}


def main():
    manuscript = Path('translations/sailor_data_help_manuscript_v1.json')
    with patch.object(prepare, 'ROOT', Path('work/analysis/sailor_data_help_v446')), \
            patch.object(prepare, 'MANUSCRIPT', manuscript), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v443_candidate.nds')), \
            patch.object(prepare, 'PARENT_TOPIC_COUNT', 208), patch.object(prepare, 'PROSE', PROSE):
        prepare.main()
    data = json.loads(manuscript.read_text(encoding='utf-8'))
    for row in data['records']:
        row['context'] = 'Original sea HUD or Sailor Info data help; source-linked neighboring articles and current plaque/condition/skill labels reviewed.'
    manuscript.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    # Preparation records the manuscript hash before adding the precise context.
    from dk4tool.patch.grand_race_menu_release import sha
    plan_path = Path('work/analysis/sailor_data_help_v446/page_proposal.json')
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    plan['manuscript_sha256'] = sha(manuscript.read_bytes())
    plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
