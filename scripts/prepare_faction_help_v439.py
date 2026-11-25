"""Complete faction help and a source-faithful Data Guide link label."""

from pathlib import Path
from unittest.mock import patch

from scripts import prepare_general_help_v431 as prepare

PROSE = {
    143: ('Data Guide',
          "This guide explains the game's data. See [[144|City Info]], [[153|Sea Info]], [[158|Sailor Info]], [[181|Faction Info]], [[191|Trade Goods]] and [[195|Ship Info]].",
          'Six data-topic links;181 is faction data, not an individual fleet data page.',
          'Correct Fleet Info to Faction Info for destination181; individual Fleet Info137 remains distinct.'),
    181: ('Faction Info',
          'Select a faction on the Route Map to view its information. See [[184|Influence]], [[182|Home Port]], [[190|Friendship]] and [[185|Relations]].',
          'Faction information is selected on the route map; links to power, headquarters, friendship and relations.',
          'Keep faction information distinct from the separate fleet/ship composition screens.'),
    182: ('Home Port',
          "This is the faction's home port. If its [[150|market share]] there falls to zero, its home port moves to another city. See [[183|Home Port Points]].",
          'Headquarters location;zero city share causes relocation to another city. Link to headquarters points.',
          'Keep the exact zero-share trigger, rather than saying any loss of share moves the home port.'),
    183: ('Home Port Points',
          "A faction receives bonus market share in its home port, called Home Port Points. Each flag shown represents one point. The bonus share equals the number of fleets the faction has. Other factions can take this portion of its share only through battles or schemes.",
          'Headquarters bonus share is shown as flags,one point per flag;fleet count determines bonus share. Only combat/schemes can steal that portion.',
          'Retain the exact fleet-count rule and only-through restriction; do not substitute generic investment advice.'),
    184: ('Influence',
          "Influence measures a faction's strength in the sea region shown. It increases with greater city [[150|market share]], victories over other factions and discoveries such as ruins.",
          'Regional faction power/size rises with city share, victories and discoveries including ruins.',
          'Influence matches the reviewed shared lore. Keep the displayed-region scope and all three increase methods.'),
    185: ('Relations',
          'Relations describes how a faction relates to yours. It can change through [[16|schemes]] at the tavern or [[27|diplomatic documents]] sent from the guild. The three basic relationships are [[188|Neutral]], [[186|Allied]] and [[187|At War]]. See also [[189|Subordinate]].',
          'Three relation levels;schemes and guild documents change them. Original links list neutral,alliance,war and additional subordination.',
          'Preserve the stated three levels and all four links by treating subordination as the separately referenced affiliation, without omitting it.'),
    186: ('Allied',
          "You have an alliance with this faction. You cannot attack its fleets. During battle, nearby allied fleets may come to your aid.",
          'Alliance prevents attacks on allied fleets;nearby allied fleets may assist during battle.',
          'Preserve may;an alliance does not guarantee help in every battle.'),
    187: ('At War',
          'You are at war with this faction. Approaching one of its fleets at sea starts a battle automatically. Cities where it holds an [[151|exclusive contract]] will also attack you. You can take its market share through [[23|commercial investment]], [[37|military investment]] or battles.',
          'War causes automatic fleet engagements and attacks from enemy monopoly cities. Shares can be taken through commercial/military investment or combat.',
          'Keep automatic engagement and enemy-controlled city attacks; retain both investment types and combat.'),
    188: ('Neutral',
          'You have ordinary relations with this faction.',
          'Normal relationship state.',
          'Neutral is a diplomatic state, distinct from Normal city conditions.'),
    189: ('Subordinate',
          "A subordinate faction will not oppose your fleet. Send [[27|diplomatic documents]] from the guild and successfully use [[33|Threaten]] to bring a faction under your control. [[33|Threaten]] requires [[4|a Proof of Conquest]].",
          'Subordinated factions do not oppose player fleet. Successful intimidation through guild diplomacy subordinates a faction;requires ruler proof.',
          'Preserve the success condition, repeated Threaten references and established Proof of Conquest term.'),
    190: ('Friendship',
          'This measures how friendly a faction is toward you. A higher value means better relations.',
          'Higher friendship value indicates better relationship with protagonist.',
          'Keep the direction of the numeric scale without inventing a threshold or guaranteed alliance.'),
}


def main():
    with patch.object(prepare, 'ROOT', Path('work/analysis/faction_help_v439')), \
            patch.object(prepare, 'MANUSCRIPT', Path('translations/faction_help_manuscript_v1.json')), \
            patch.object(prepare, 'PARENT', Path('out/all_routes_combined_v438_candidate.nds')), \
            patch.object(prepare, 'PARENT_TOPIC_COUNT', 208), patch.object(prepare, 'PROSE', PROSE):
        prepare.main()


if __name__ == '__main__':
    main()
