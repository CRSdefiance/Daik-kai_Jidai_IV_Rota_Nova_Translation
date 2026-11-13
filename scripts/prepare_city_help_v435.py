"""Faithful city-data/source-item prose, with native automatic pagination."""

from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare

PROSE = {
    145: ('City, Port or Village',
          "A settlement's size determines which commands are available. Cities are large settlements; ports are smaller ones. Villages allow resupply, but you cannot go ashore. An event may turn a village into a port.",
          'Settlement scale affects commands. Cities are large, ports small; villages permit supplies but not landing, and may become ports through events.',
          'Retain the resupply/landing distinction and the possibility of conversion by an event.'),
    146: ('Cultural Region',
          'Each city belongs to a cultural region. Trade-good prices vary by region, as do the building signs and available commands.',
          'Cultural affiliation affects commodity prices and building signs/available commands.',
          'Do not reduce the article to generic trade advice or equate culture with national ownership.'),
    147: ('Status',
          "A city's status affects prices. Normal: ordinary conditions. War: weapon prices rise; other prices fall. Plague: food and medicine prices rise; other prices fall. Famine: food prices rise; other prices fall. Boom: prices rise overall. Slump: prices fall overall. Shortage: prices rise for goods in the category that is in short supply.",
          'Seven city conditions and their exact price directions: normal; war/weapons; plague/food and medicine; famine/food; prosperity/all; recession/all; category shortage.',
          'Use Boom/Slump as idiomatic economic labels. Keep every price direction and affected category; active ARM9 status labels are a separate unfinished localization gate.'),
    149: ('Arms',
          "Arms measures how well a city is armed. It rises when you make [[37|military investments]] at the Palace or Governor's Office. Higher Arms makes a city less likely to surrender when attacked.",
          'City armament rises through military investment at palace/government; higher armament lowers likelihood of surrender under attack.',
          'Match the existing Arms field and retain less likely, without promising immunity to attack.'),
    150: ('Market Share',
          "Your market share determines how much of a city's specialty stock you can buy. A 1 percent share lets you sell without a limit. Increase your share through [[23|commercial investment]], [[37|military investment]], [[38|letters of introduction]] or [[39|letters of recommendation]]. You must obtain the first 1 percent through a [[36|contract]] at the Palace or Governor's Office. At your faction's home port, [[183|Home Port Points]] add to its share. See [[151|Exclusive Contracts]].",
          'Share determines purchasable proportion of specialty arrivals.1 percent permits unlimited selling. Four means of increasing share; first1 percent requires contract. Home-base points add home-city share. Link to monopoly.',
          'Retain both the initial-contract rule and later letter/investment methods, plus the home-port bonus. Do not shorten the article to fit one page.'),
    151: ('Exclusive Contracts',
          "A 100 percent market share gives your faction an exclusive contract and control of the city. You receive tribute each month and can have the city attack factions you are at war with. You cannot obtain a contract by the usual method in a city controlled by another faction's exclusive contract. Use [[38|a letter of introduction]] or [[39|a letter of recommendation]], or go to war with that faction.",
          '100 percent share grants monopoly/control, monthly tribute and attacks against warring factions. Ordinary contracting is unavailable under another monopoly; letters or war provide alternatives.',
          'Preserve all benefits and all three alternatives without inventing a guaranteed automatic contract from declaring war.'),
    194: ('Source Items',
          "Source items can create new specialties in a city. Bring one to the market, and the city may gain a new specialty. This will not work if the city is unsuitable for the item or already has five specialties. Several cities can suit the same item. Consider giving it to a convenient city, such as one where your faction has a high [[150|market share]].",
          'Source items may expand specialties at suitable markets; no increase if unsuitable or already five products. Several cities may suit an item; high own share is a useful criterion.',
          'Keep the suitability and five-specialty limits; do not confuse these specialty-producing items with ordinary raw-material trade goods.'),
}


def main():
    with patch.object(prepare, 'ROOT', Path('work/analysis/city_help_v435')), \
            patch.object(prepare, 'MANUSCRIPT', Path('translations/city_help_manuscript_v1.json')), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v434_candidate.nds')), \
            patch.object(prepare, 'PROSE', PROSE):
        prepare.main()


if __name__ == '__main__':
    main()
