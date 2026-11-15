"""Faithful ship jobs/requirements and consistent established officer role names."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare
from scripts.prepare_sailor_data_help_v446 import PROSE as DATA_PROSE

PROSE = {
    106: ('Personnel',
          'You can assign officers to jobs automatically. Choose Auto on the Deck screen, then select [[107|Exploration]], [[108|Trade]] or [[109|Naval Battle]].',
          'Automatic officer placement; source Deck triangle action opens policy selection: exploration/trade/naval combat.',
          'Name the translated Auto action rather than repeating the source platform triangle symbol. Preserve all three policy links.'),
    107: ('Exploration',
          'This policy arranges officers for exploration. It gives priority to highly skilled officers in jobs useful for exploring.',
          'Exploration-suited assignments; high-ability officers prioritized for relevant jobs.',
          'Do not reduce the policy to a guessed pair of skills.'),
    108: ('Trade',
          'This policy arranges officers for trading. It gives priority to highly skilled officers in jobs useful for trade.',
          'Trade-suited assignments; high-ability officers prioritized for relevant jobs.',
          'Keep assignment priority rather than promising a specific income increase.'),
    109: ('Naval Battle',
          'This policy arranges officers for battle. It gives priority to highly skilled officers in jobs useful for combat.',
          'Combat-suited assignments; high-ability officers prioritized for relevant jobs.',
          'Do not restrict this policy to sword fighters when the source covers combat jobs broadly.'),
    110: ('Workrooms',
          'These are the rooms where officers perform their assigned jobs. See [[111|Private Cabin]], [[112|Recreation Room]], [[113|Lumber Room]], [[114|Infirmary]], [[115|Galley]], [[116|Livestock Room]], [[117|Chapel]], [[118|Strategy Room]], [[119|Purser\'s Office]], [[120|Captain\'s Cabin]], [[121|First Mate\'s Office]], [[122|Ship\'s Wheel]], [[123|Survey Room]], [[124|Lookout Tower]], [[125|Masts]] and [[126|Deck]].',
          'Officer workspaces;16 room destinations in original order.',
          'Preserve all16 links and use natural full room names consistent with existing officer roles.'),
    111: ('Private Cabin',
          'Officers rest here. Assigning an officer to a Private Cabin improves their physical condition and mood.',
          'Rest room restores assigned navigator body and mental states.',
          'Retain both kinds of recovery without inventing an instant full heal.'),
    112: ('Recreation Room',
          'Officers and sailors rest here. Assigning an officer to this room slows the increase in crew fatigue and helps the officer recover from fatigue and improve their mood.',
          'Crew/navigator rest; assignment lowers fatigue growth for sailors and restores navigator fatigue/mental state.',
          'Distinguish crew fatigue prevention from the assigned officer\'s recovery.'),
    113: ('Lumber Room',
          'This room stores lumber for repairs. Officers assigned here become Shipwrights and need Survey 130 or higher. A Shipwright repairs the ship during voyages and reduces repair costs at shipyards.',
          'Repair timber room; Shipwright requires Survey>=130. Voyage repairs and cheaper shipyard repairs.',
          'Preserve threshold and both repair benefits.'),
    114: ('Infirmary',
          'Sick people are treated here. Officers assigned here become Surgeons and need Observe 150 or higher. A Surgeon makes illness less likely and slows the increase in crew fatigue. Having a Surgeon also lets you use items that cure illness.',
          'Medical room; surgeon Observe>=150. Reduces disease likelihood/fatigue growth and enables disease-curing item use.',
          'Match Surgeon in the established native role table; retain item-use eligibility.'),
    115: ('Galley',
          'Meals are prepared here. Officers assigned here become Chief Cooks and need Aim 70 or higher. A Chief Cook slows the use of food and water during voyages and the increase in crew fatigue.',
          'Kitchen; chief cook Aim>=70. Slows food/water depletion and crew fatigue growth.',
          'Keep both supplies and fatigue effects; Aim is the source requirement, not Finance.'),
    116: ('Livestock Room',
          'Animals are raised here for food. Officers assigned here become Animal Keepers and need Health 130 or higher. An Animal Keeper produces food during voyages.',
          'Food livestock room; keeper vitality>=130. Produces food while sailing.',
          'Use the existing Health skill label from Sailor Info and distinguish it from physical condition.'),
    117: ('Chapel',
          'Officers and sailors worship here. Officers assigned here become Missionaries and need Social 160 or higher. A Missionary slows the increase in crew fatigue and lets you [[43|Distribute Goods]] at the square to start a [[25|Trend]]. Some officers refuse this assignment because of their beliefs.',
          'Worship room; missionary persuasion>=160. Slows fatigue; distribute products at square can initiate trend. Some officers refuse for convictions.',
          'Preserve both links and the belief-based refusal; do not invent a specific religion.'),
    118: ('Strategy Room',
          'Officers assigned here become Strategists and need Tactics 120 or higher. When a Strategist devises a scheme, you can [[16|Plan a Scheme]] at the tavern. They may also stop enemy schemes before they happen. When you stay at an inn, they gather information about other factions.',
          'Strategy room; adviser schemes>=120. Inspiration enables tavern plotting; may preempt enemy plots. Inn stay gathers rival faction information.',
          'Retain inspiration, may, and the inn condition rather than guaranteeing protection.'),
    119: ('Purser\'s Office',
          'The fleet\'s accounts are managed here. Officers assigned here become Pursers and need Finance 100 or higher. A Purser may get you lower prices at the market. You may also be able to buy up all available stock by paying twice the price, but you cannot sell at twice the price.',
          'Accounting room; purser Finance>=100. May obtain discounts and buy-out stock for double payment; cannot sell for double price.',
          'Keep the purchase/sale distinction and match Purser in the native role glossary.'),
    120: ('Captain\'s Cabin',
          'This is the ship commander\'s cabin. Only the main character can be assigned here, becoming Captain. A Captain slows the increase in crew fatigue and is required for [[76|Auto Move]].',
          'Commander room accepts protagonist only; becomes captain. Slows fatigue and required for automatic sailing.',
          'Preserve protagonist-only assignment; source table133 separately lists Command30.'),
    121: ('First Mate\'s Office',
          'This office is for the Captain\'s assistant. Officers assigned here become First Mates and need Social 100 or higher. A First Mate lets you [[27|Send Diplomatic Documents]] from the guild and slows the increase in crew fatigue. In battles against cities, they demand the city\'s surrender.',
          'Captain assistant room; deputy persuasion>=100. Enables guild document dispatch, slows fatigue and urges city surrender in city battle.',
          'Use the native First Mate role rather than Adjutant; a surrender demand is not guaranteed success.'),
    122: ('Ship\'s Wheel',
          'The ship\'s rudder is controlled here. Officers assigned here become Helmsmen and need Sailing 60 or higher. A Helmsman makes it easier to turn the ship and increases its speed during Auto Move.',
          'Rudder control room; helmsman Sailing>=60. Easier heading changes and faster automatic travel.',
          'Keep the Auto Move scope of the speed benefit.'),
    123: ('Survey Room',
          'Officers assigned here become Surveyors and need Survey 120 or higher. A highly skilled Surveyor lets you see your current latitude and longitude while sailing. A Surveyor is also required for [[76|Auto Move]]; higher skill makes it faster.',
          'Sea survey room; Surveyor Survey>=120. High skill displays coordinates, required for Auto Move and higher skill improves automatic speed.',
          'Retain role eligibility, coordinate display and both automatic travel facts.'),
    124: ('Lookout Tower',
          'This lookout platform is attached to a mast. Officers assigned here become Lookouts and need Observe 70 or higher. A Lookout helps you discover cities and other places at sea and view information about nearby fleets. A Lookout with high Aim may snipe an enemy admiral during battle. A successful shot lets you capture that ship.',
          'Mast lookout; Observe>=70. Helps find towns/objects and inspect nearby fleets. High Aim may snipe enemy admiral; success captures its ship.',
          'Preserve the separate Aim benefit and chance/success conditions.'),
    125: ('Masts',
          'These are the ship\'s masts. Officers assigned here become Sail Handlers and need Sailing 80 or higher. A Sail Handler makes it easier to turn the sails and increases speed during Auto Move. If every mast has a Sail Handler, they adjust the sails automatically when they are [[83|Half Open]].',
          'Masts; sail handler Sailing>=80. Easier sail rotation and faster Auto Move; all masts staffed enables automatic sail rotation at half-open.',
          'Use Sail Handler from the native role table and retain every-mast and half-open conditions.'),
    126: ('Deck',
          'Officers assigned to the Deck become Deckhands and need Health 30 or higher. A Deckhand improves your strength in [[98|boarding battles]]. Deckhands gain levels more easily but tire very quickly, so watch their physical condition.',
          'Deck crew vitality>=30 boosts close-quarters battle. Easier leveling but very rapid fatigue; monitor body condition.',
          'Keep both the experience benefit and fatigue tradeoff.'),
    128: ('Marine Barracks',
          'Marines wait here. A ship can have up to four Marine Barracks. Officers assigned here become Boarding Leaders and need Combat 90 or higher. A Boarding Leader improves your strength in [[98|boarding battles]] and takes part in [[99|duels]].',
          'Marine waiting quarters max4; boarding leader sword>=90. Stronger melee and participates in duels.',
          'Keep the four-room limit and use the existing Boarding Leader role.'),
    129: ('Gun Batteries',
          'These are the ship\'s gun batteries. Officers assigned here become Gunners and need Aim 90 or higher. A Gunner lets you fire more cannon shots.',
          'Gun positions; gunner Aim>=90 increases quantity of cannon fire.',
          'Do not substitute an accuracy bonus for the source\'s increased firing capacity.'),
    130: ('Rowers\' Quarters',
          'Sailors row the oars here. Officers cannot be assigned to this room. Only ships powered by rowing have it.',
          'Ordinary sailors row; no officer assignment; present only on human-powered ships.',
          'Distinguish sailors from assignable officers and retain the ship-type restriction.'),
    131: ('Supply Hold',
          'Food and water for voyages are stored here. Officers cannot be assigned to a Supply Hold. More Supply Holds let you carry more food and water.',
          'Voyage food/water storage, not assignable to officers. More holds increase capacity.',
          'Preserve both supply types and the assignment restriction.'),
    132: ('Cargo Hold',
          'Trade goods are stored here. Officers cannot be assigned to a Cargo Hold. More Cargo Holds let you carry more trade goods. A ship can have up to five Cargo Holds.',
          'Trade cargo storage, not assignable. More holds increase load; maximum5.',
          'Restore the five-hold limit instead of generic trading advice.'),
    133: ('Ability Requirements',
          'Sail Handler, Sailing 80; Lookout, Observe 70; Deckhand, Health 30; Surveyor, Survey 120; Helmsman, Sailing 60; Captain, Command 30; First Mate, Social 100; Boarding Leader, Combat 90; Gunner, Aim 90; Shipwright, Survey 130; Surgeon, Observe 150; Chief Cook, Aim 70; Animal Keeper, Health 130; Missionary, Social 160; Strategist, Tactics 120; Purser, Finance 100.',
          'All16 original room/role minimum skills and numbers in source order.',
          'Expand room labels to their explicitly mapped job names. Preserve every threshold without manual rows; separate Captain article retains protagonist-only rule.'),
}

# These original articles were restored in V447 but need exact native role terms.
ROLE_REPLACEMENTS = {160: [('A [[114|Doctor]]', 'A [[114|Surgeon]]')],
                     172: [('[[125|Sail Masters]]', '[[125|Sail Handlers]]')],
                     173: [('[[115|Cooks]]', '[[115|Chief Cooks]]')],
                     175: [('[[121|Adjutants]]', '[[121|First Mates]]')],
                     176: [('[[119|Accountants]]', '[[119|Pursers]]')],
                     178: [('[[128|Marine Leaders]]', '[[128|Boarding Leaders]]')],
                     179: [('[[114|Doctors]]', '[[114|Surgeons]]')]}
for topic, replacements in ROLE_REPLACEMENTS.items():
    title, english, gloss, note = DATA_PROSE[topic]
    for old, new in replacements:
        assert old in english
        english = english.replace(old, new)
    PROSE[topic] = (title, english, gloss, note + ' Role labels match the original native role selector\'s established English glossary.')


def main():
    root = Path('work/analysis/crew_help_v448')
    manuscript = Path('translations/crew_help_manuscript_v1.json')
    with patch.object(prepare, 'ROOT', root), patch.object(prepare, 'MANUSCRIPT', manuscript), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v447_candidate.nds')), \
            patch.object(prepare, 'PARENT_TOPIC_COUNT', 209), patch.object(prepare, 'PROSE', PROSE), \
            patch.object(prepare, 'LAYOUT_BY_TOPIC', {133: 'semicolon-entries-v1'}):
        prepare.main()
    data = json.loads(manuscript.read_text(encoding='utf-8'))
    for row in data['records']:
        row['context'] = 'Original Deck job/room or related Sailor Info Help; all source-linked neighbors and the existing16-entry native role glossary reviewed.'
    manuscript.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    from dk4tool.patch.grand_race_menu_release import sha
    plan_path = root / 'page_proposal.json'
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    plan['manuscript_sha256'] = sha(manuscript.read_bytes())
    plan_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
