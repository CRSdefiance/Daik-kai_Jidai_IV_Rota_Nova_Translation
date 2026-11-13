"""Remaining flagged Help and complete linked item/ship/crew navigation."""

import json
from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare

PROSE = {
    135: ('Sailor Info', 'Select an officer from the list to view their [[158|character data]].',
          'Displays officer character data after selection from the list.',
          'Restore the original character-data link and the selection step.'),
    136: ('Ship Info', 'Select a ship from the list to view its [[195|ship data]].',
          'Displays each fleet ship\'s data after selecting from the list.',
          'Restore the original ship-data link instead of an invented field list.'),
    137: ('Fleet Info', 'Select one of your faction\'s fleets from the list to view its data. Selecting a regional fleet also lets you change its assigned policy.',
          'Own faction fleet data; select fleet from list. Regional fleet selection enables delegation policy changes.',
          'Keep the regional-fleet restriction and the selection step.'),
    138: ('Items', 'Select an item from the list to view its description. Depending on its type, you can equip or use it. If an officer has an item equipped that is unrelated to their current job, the officer\'s name appears in red. Give the item to another officer or change their job.',
          'Item descriptions/equipping; list selection opens item screen. Source square action equips/uses according to item type. Wearer name is red when equipped item is unrelated to job; reassign item or job.',
          'The name, not the item, turns red. Describe the equip/use action without carrying over an unsupported source-platform square glyph.'),
    139: ('Assign Sailors', 'Distribute sailors among your ships. Each ship shows Need, Now and Max: required, current and maximum crew. Press Left or Right to adjust a ship\'s current crew, or choose Auto to assign all ships at once. Ships below Need sail more slowly. Auto offers three policies: give priority to the flagship; assign the same percentage of maximum crew to each ship; or assign only the required minimum.',
          'Crew assignment; required/current/max counts; left/right adjust each ship; bulk auto supported. Below requirement slows ship. Flagship priority, equal maximum-relative percentages, required-minimum policies.',
          'Explain all three policies accurately without manual rows or ambiguous fill-first shorthand.'),
    140: ('Functions', 'From Functions, you can save, load, quit the game and change options.',
          'Save/load, end game, options and related functions.',
          'Restore the actual menu functions instead of see below.'),
    141: ('Golden Route Records', 'These records show the Golden Routes you have discovered. See [[201|Discovering Golden Routes]] and [[81|Reporting Golden Routes]].',
          'Information on Golden Routes discovered so far; discovery and report links.',
          'Keep both destinations and the already-discovered scope.'),
    142: ('Ancient Maps', 'Ancient Maps are said to reveal the locations of great treasures. They are torn into several pieces. Visit [[26|guilds]] in different cities to gather the fragments.',
          'Old maps reputedly reveal great treasures; torn into multiple pieces. Collect fragments from city guilds.',
          'Preserve the reputed nature of the treasure claim and the original Guild link.'),
    195: ('Ship Info', 'Select a ship through Info, then Ship Info, to view its data. See [[196|Hull]], [[197|Crew]], [[198|Water and Food]], [[199|Square Sail Performance]] and [[200|Fore-and-Aft Sail Performance]].',
          'Each ship\'s data; Info/Ship Info selects it. Five original data field links.',
          'Restore every original destination and use Hull from the current ship UI; no unrelated guns/cargo facts are added.'),
    196: ('Hull', 'Hull shows current and maximum durability. Matching values mean the ship is undamaged. If current durability is below the maximum, repairs at a shipyard restore it.',
          'Current/max durability; equality means no damage; lower current is restored by shipyard repair.',
          'Match the existing Hull field and retain the undamaged condition.'),
    197: ('Crew', 'These values are the required, current and maximum numbers of sailors. Change the crew assigned to each ship through [[139|Assign Sailors]] in the Shared Commands menu.',
          'Required/current/maximum crew counts; change allocations through shared crew organization command.',
          'Preserve the three-value order used by Need/Now/Max plaques.'),
    198: ('Water and Food', 'These are the barrels of water and food remaining. Running out causes crew fatigue to rise sharply. Your food lasts longer with help from [[116|Animal Keepers]] and [[115|Chief Cooks]].',
          'Remaining water/food barrels; zero sharply raises fatigue. Keeper/cook slows net food depletion.',
          'State the net food benefit without changing the Keeper\'s food production into a consumption formula.'),
    199: ('Square Sail Performance', 'This is main plus auxiliary square-sail performance. Higher values let you sail faster with the wind behind you. Main performance depends on the mainmast\'s [[52|sail type]] and equipment. Auxiliary performance comes from the foremast ahead of the mainmast and the mizzenmast behind it. Some ship types lack these auxiliary masts.',
          'Main+secondary horizontal sail values improve following-wind speed. Mainmast sail type/equipment determine main; fore/mizzen masts determine secondary; ship type may lack these.',
          'Keep both mast positions, main/auxiliary distinction and possible absence; do not promise arbitrary faster sailing.'),
    200: ('Fore-and-Aft Sail Performance', 'This is main plus auxiliary fore-and-aft sail performance. Higher values let you sail faster upwind. Main performance depends on the mainmast\'s [[52|sail type]] and equipment. Auxiliary performance comes from the foremast ahead of the mainmast and the mizzenmast behind it. Some ship types lack these auxiliary masts.',
          'Main+secondary vertical sail values improve adverse-wind speed. Mainmast sail type/equipment determine main; fore/mizzen determine secondary; possible absence by ship type.',
          'Fore-and-aft includes more than lateen sails; upwind expresses the original adverse-wind condition naturally.'),
    201: ('Discovering Golden Routes', 'You discover a Golden Route when the profit rate from trading a good exceeds 500 percent. Report discoveries to the guild. See [[81|Reporting Golden Routes]] and [[141|Golden Route Records]].',
          'Trading profit rate strictly exceeds500 percent triggers Golden Route discovery; advise guild report; report/records links.',
          'Keep strictly above500, not at least500, and do not invent the profit-rate formula.'),
}


def main():
    root = Path('work/analysis/interface_help_v456')
    manuscript = Path('translations/interface_help_manuscript_v1.json')
    with patch.object(prepare, 'ROOT', root), patch.object(prepare, 'MANUSCRIPT', manuscript), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v455_candidate.nds')), \
            patch.object(prepare, 'PARENT_TOPIC_COUNT', 210), patch.object(prepare, 'PROSE', PROSE):
        prepare.main()
    data = json.loads(manuscript.read_text(encoding='utf-8'))
    for row in data['records']:
        row['context'] = 'Original Shared Commands/Info/Ship Data Help and source-linked neighbors; current labels and reviewed role terminology retained.'
    manuscript.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    from dk4tool.patch.grand_race_menu_release import sha
    p = root / 'page_proposal.json'
    plan = json.loads(p.read_text(encoding='utf-8'))
    plan['manuscript_sha256'] = sha(manuscript.read_bytes())
    p.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
