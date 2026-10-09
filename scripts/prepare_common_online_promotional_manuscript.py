"""Review full clean COMMON promotional meanings; presentation is unresolved."""
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

TEXT = {
    3289: ('Set Your Sights on a World Beyond the Map', 'Heading: aim for a world not found on a map; the trailing dash creates anticipation.'),
    3290: ('Become the captain of a sailing ship and set out across the boundless ocean aboard your own vessel. Form a fleet with companions who gather in the online world, unravel mysteries surrounding hidden ancient secrets, and fight gripping battles against pirate fleets as your adventurous voyages carry you into new worlds.', 'The player commands a sailing ship as captain, sails their own ship into an endless ocean, forms fleets with companions in the network-created world, solves mysteries of hidden ancient secrets, fights tense pirate-fleet battles, and continues voyages toward new worlds.'),
    3291: ('Stories Shared with All Kinds of People', 'Heading: human drama involving a variety of people.'),
    3292: ('Uncharted Waters Online is an online seafaring adventure RPG set in the Age of Discovery, the great movement that swept Europe in the early 1500s. Become an adventurer, merchant, or soldier and create stories with the many different people who share your world.', 'An online maritime adventure role-playing game set in the Age of Discovery movement that arose in early-sixteenth-century Europe. Players take roles such as adventurer, merchant or soldier and create human dramas with the varied people living in the same world.'),
    3293: ('Stories Shared with All Kinds of People', 'Duplicate of heading 3291: human drama involving a variety of people.'),
    3294: ('The game world spans nations including Portugal, Spain, and England. Choose your character\'s homeland when creating your in-game alter ego. Begin life as a seafarer by choosing the path of adventurer, merchant, or soldier in bustling home ports such as Lisbon, Seville, and London.', 'The server world consists of several nations, including Portugal, Spain and England. At character creation, players choose their alter ego\'s country of origin. They begin their seafaring lives as adventurer, merchant or soldier in national home ports such as Lisbon, Seville and London.'),
    3295: ('Live Life Your Way', 'Heading: different freely chosen ways of living are possible.'),
    3296: ('Start by exploring ports and trade goods near your homeland. As you chart coastal waters, trade goods and hunt pirates to develop your seamanship. You will gradually command faster, larger, sturdier ships. Team up with other players on guild assignments to build your fame as a seafarer, or invest to bring more ports into your nation\'s alliance. How you live is your choice.', 'Initially act around the home nation and explore new ports and goods. Once nearby geography is known, trade and suppress pirates to improve sailing ability, gradually gaining faster, larger and stronger ships. Cooperate with players on guild requests to raise seafaring fame, or invest to expand the nation\'s allied ports. Players freely choose varied ways to live.'),
    3297: ('Royal Orders Lead to New Adventures', 'Heading: receive orders from the king and depart on further adventures.'),
    3298: ('Royal orders let you open new sailing regions and embark on fresh adventures. Exotic clothing and goods await in foreign towns; great ruins and hidden treasures lie deep inland. Storms may block your fleet without mercy, and dangerous waters offer the chance to become a privateer. Voyages full of thrills and spectacle await every seafarer.', 'Orders from the king allow new sailing areas to be opened and new adventures begun. Rare clothing and products in other cultures\' towns, ruins and sleeping treasures deep inland, merciless storms obstructing fleets, and dangerous waters where the player can become a privateering pirate provide thrilling and spectacular voyages.'),
    3299: ('Live Freely as a Seafarer on the World\'s Seas!', 'Heading: the world\'s seas are the stage for a freely chosen seafaring life.'),
    3300: ('Choose from more than 50 professions in three branches: adventure, trade, and combat. As you gain experience at sea, you can change professions through the appropriate guild. A new profession changes which skills you can acquire and how your character develops.', 'More than fifty professions are available in adventure, trade and combat categories. Seafaring experience enables a profession change at the relevant guild. Changing profession greatly changes the kinds of skills obtainable and how growth occurs. Unlike the raster card, this full COMMON copy says more than fifty, not about fifty.'),
    3301: ('Sail Beyond the Distant Seas and Make Your Name as a Great Explorer!', 'Heading: sail into the far reaches of the vast ocean and establish a name as a great adventurer.'),
    3302: ('Majestic ancient ruins, legendary treasures, unknown life, and natural wonders... Countless mysteries lie hidden in a vast world brought to life in full 3D. Adventurers work together in pursuit of great discoveries.', 'Huge magnificent ruins, legendary treasures, unknown living things and natural marvels appear in a vast full-3D world with innumerable hidden mysteries. Adventurers cooperate to seek great discoveries.'),
    3303: ('Trade a Wealth of Goods and Enjoy Making a Profit', 'Heading: buy and sell diverse trade goods, having fun while earning money.'),
    3304: ('Hundreds of different goods are traded. Merchants\' dealings constantly change prices and shape the virtual economy. Invest in towns around the world to make them allied ports of your homeland, gain favorable trading terms, and add new local specialties to the goods on offer.', 'Several hundred types of trade goods are available. Transactions by merchants continually alter market prices and form the virtual economy. Investment in towns worldwide can make them the home nation\'s allied ports, permit favorable trading conditions and add new specialty goods to stock.'),
    3305: ('Fierce Battles on the High Seas!', 'Heading: heated battles unfold at sea.'),
    3306: ('Beyond every port lie dangerous, pirate-infested seas. Soldiers defeat pirates and build their fame while escorting adventurers and merchants. Players can also form pirate fleets together. Fleet battles fought with cannon fire and boarding combat are a highlight of the Age of Discovery.', 'Leaving a town enters dangerous seas with pirates. Soldiers escort adventurers and merchants, defeat pirates and increase fame. Players may themselves form pirate groups. Heated fleet battles using artillery and close combat are a star attraction of the age.'),
    3307: ('Your Nation Shapes Your Story!', 'Heading: the story changes greatly according to the nation to which the player belongs.'),
    3308: ('Adventures begin in the nations of Europe. Complete guild assignments and report discoveries from your voyages to build your fame as a seafarer. As your fame grows, the king will issue orders granting permission to sail into new seas. Meet many story characters along the way, with events unfolding according to the affairs of your nation.', 'Adventures start from European countries. Achieving guild requests and reporting discoveries increases seafaring fame, after which the king issues orders granting new sailing-region permission. Numerous event characters appear while traveling, and stories unfold according to each associated nation\'s situation. The duplicated source phrase does not create a second permission requirement.'),
    3309: ('An Ever-Changing World Brings Adventures of Every Kind!', 'Heading: the constantly changing world gives rise to varied adventures.'),
    3310: ('The virtual world changes constantly in response to each player\'s actions. Royal orders can spark great naval battles over allied ports, while players\' trading can cause dramatic shifts in market prices.', 'Each player\'s actions influence the continually changing virtual world. Examples are large naval battles over allied ports under royal orders and substantial changes in prices caused by player trade.'),
    3311: ('Set Out with Companions You Meet in Town!', 'Heading: depart on an adventure with companions met in town.'),
    3312: ('Take a voyage assignment from a town guild, then invite other players to form a fleet. Work together toward great discoveries: gather information in towns and use your companions\' skills, such as cartography and archaeology, to solve mysteries. Sharing a sunset at sea or a conversation in a tavern along the way is a special pleasure of its own.', 'Obtain a voyage-purpose request from a town guild, invite other players and form a fleet. Cooperate on town inquiries and solve mysteries using members\' skills such as mapmaking and archaeology to seek great discoveries. Enjoying sunsets at sea and talking together in taverns while traveling is especially enjoyable.'),
    3313: ('Sail the Open Seas in a Ship All Your Own!', 'Heading: travel the vast ocean in a personally customized, original ship.'),
    3314: ('Ships come in many types and sizes. Change their materials, weapons, number of sails, and emblems to create a vessel of your own. Customize your character\'s build and hairstyle, then choose from hundreds of items, including the clothes and hats favored by admirals and nobles of the age. Stroll through town in whatever style suits you.', 'Ship types range in size, and materials, weapons, sail count and emblems can be changed for a unique ship. Character physique and hairstyle are customizable, with several hundred equipment items including period admirals\' and nobles\' clothing and hats, allowing freely chosen appearances while walking through town.'),
    3315: ('Adventure in a World True to Its Time!', 'Heading: an adventure environment faithfully recreates the world of that period.'),
    3316: ('The seas are recreated in all their grandeur and beauty, changing with the region and time of day. Landmarks such as the Leaning Tower of Pisa and the Parthenon rise above the cities you visit. Explore inland through city gates or from landing sites, sail up the Nile, and excavate pyramids. The possibilities for adventure stretch endlessly before you.', 'The ocean is majestically and beautifully recreated with varied appearances by region and time. City landmarks include the Leaning Tower of Pisa and Parthenon. Players can explore inland from city gates and landing points, go upstream along the Nile and excavate pyramids, with ever-expanding adventure settings.'),
    3317: ('About the Online Version Tie-In', 'Heading: information about the tie-in with the Online version.'),
    3318: ('Uncharted Waters IV: Rota Nova offers extra ways to enjoy the game through a tie-in with the Windows edition of Uncharted Waters Online.', 'Rota Nova provides features that expand enjoyment of the game through a tie-in with the Windows edition of Uncharted Waters Online. This is historical source copy, not a claim that the service is currently available.'),
    3319: ('Join the Windows edition of Uncharted Waters Online and complete a quest to receive a password paired with a village name. Sail to that village in Uncharted Waters IV: Rota Nova and use the password to unlock new goods for trade.', 'Joining the Windows version of Online and completing a quest gives a password together with a village name. Sailing to the designated village in Rota Nova and using that password makes new trade goods appear and enables trade. Preserves the two-game and village-specific password relationship.'),
}


def main():
    clean = NdsImage.open('work/clean.nds')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),
                                     clean.read_file('/__arm9__.bin'))
    assert set(TEXT) == set(range(3289, 3320))
    rows = []
    for i, (english, meaning) in TEXT.items():
        e = entries[i]
        # These are source-authored full prose, not approved shared-dialogue
        # formatting. Keep plain ASCII while the actual consumer is traced.
        english.encode('ascii')
        rows.append({
            'id': f'COMMON_MESSAGE_{i}', 'message_id': i,
            'block': e.block, 'record': e.record_index,
            'source_hex': e.text.hex().upper(), 'japanese': e.text.decode('cp932'),
            'previous_japanese': entries[i - 1].text.decode('cp932'),
            'next_japanese': entries[i + 1].text.decode('cp932'),
            'english': english + '{PAD}', 'speaker': 'Online promotional information',
            'source_meaning': meaning,
            'context': (f'Full native COMMON selection {i}, clean B{e.block} R{e.record_index}. '
                        'Long Online promotional copy differs from the shorter raster cards. '
                        'ARM9 captions use separate inline pointers. COMMON consumer, visibility '
                        'and presentation are still unresolved; this is not insertion approval.'),
            'localization_note': ('Fresh full-source American English preserves all listed examples, '
                                  'places, choices, quantities, causal relationships and tie-in steps. '
                                  'Source staging spaces and line breaks are not translated prose. '
                                  'No new manual wrapping, deletion to fit four dialogue lines or '
                                  'inference that this COMMON copy is unused. Formatting is pending.'),
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
            'presentation': 'online-promotional-unclassified',
        })
    payload = {
        'format': 'dk4-common-entry-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'target_locale': 'en-US', 'encoder': 'dialogue-fixed-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'status': 'source-reviewed-draft-awaiting-consumer-and-presentation-mapping', 'records': rows,
    }
    destination = Path('translations/common_online_promotional_manuscript_v2.json')
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rows)} full-source promotional meanings; largest English paragraph '
          f'{max(len(v[0]) for v in TEXT.values())} ASCII bytes; formatting unapproved')


if __name__ == '__main__':
    main()
