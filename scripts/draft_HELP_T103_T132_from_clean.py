"""Seal clean-source meanings and logical drafts for the connected Deck/crew tutorial exchange."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

PACKET = Path('work/analysis/Shared_HELP_early_topics_clean_20261104/clean_HELP_source_packet_v2.json')
OUT = Path('work/analysis/Shared_HELP_T103_T132_clean_20261104/clean_meanings_andfull_drafts_v1.json')

# Headings and unfamiliar stat/room labels remain provisional until compared with
# the current native UI. Known terms from earlier reviews are disclosed below.
DRAFTS = [
    (103, 'Common Commands', 'Commands usable in towns and at sea; triangle opens them; preserve six destinations.',
     'These commands are available both in town and at sea. Press X on either screen to open the menu. See [[104|Chart]], [[105|Deck View]], [[134|Info]], [[138|Items]], [[139|Crew]] and [[140|Functions]].'),
    (104, 'Chart', 'Shows current sea area and faction names. In areas with unvisited towns, only City-level towns show. Select town/fleet for data; connecting lines are routes; red routes support automatic movement. Square zooms to world before selecting another sea area.',
     'View a map of your current sea area and the factions there. In areas with towns you have not visited, only [[145|City]]-level towns appear. Select a town or fleet to view its information. Lines between towns are sailing routes; you can use Auto Move along red routes. To view another sea area, press Y to zoom out to the world map, then select an area.'),
    (105, 'Deck View', 'Assign companions by selecting person then room; room determines role. Required abilities gate assignments; higher ability strengthens role effect; three links.',
     "Assign your companions to positions aboard your ships. Select a companion, then place them in a room to assign its role. Each role has [[133|required abilities]]; companions who fall short cannot take that assignment. Higher abilities also make a companion more effective in the role. See [[106|Auto Assign]], [[110|Workrooms]] and [[127|Holds]]."),
    (106, 'Auto Assign', 'Automatic assignments selected with triangle in Deck, using exploration, trade or naval-battle policy; preserve links/order.',
     'Assign roles automatically. Press X in Deck View, then choose Exploration, Trade or Naval Battle. See [[107|Exploration]], [[108|Trade]] and [[109|Naval Battle]].'),
    (107, 'Exploration', 'Prioritize high-ability navigators for exploration-related roles.',
     'Arrange assignments for exploration, giving companions with high abilities priority for roles that help on exploratory voyages.'),
    (108, 'Trade', 'Prioritize high-ability navigators for trade-related roles.',
     'Arrange assignments for trade, giving companions with high abilities priority for roles that help with trading.'),
    (109, 'Naval Battle', 'Prioritize high-ability navigators for combat-related roles.',
     'Arrange assignments for battle, giving companions with high abilities priority for combat roles.'),
    (110, 'Workrooms', 'Rooms/positions where navigators perform duties; all sixteen destinations kept in source order.',
     "Your companions carry out their duties in these rooms and positions. See [[111|Private Cabin]], [[112|Recreation Room]], [[113|Lumber Room]], [[114|Infirmary]], [[115|Galley]], [[116|Livestock Room]], [[117|Chapel]], [[118|Strategy Room]], [[119|Accounting Room]], [[120|Captain's Cabin]], [[121|First Mate's Cabin]], [[122|Helm]], [[123|Survey Room]], [[124|Lookout]], [[125|Mast]] and [[126|Deck]]."),
    (111, 'Private Cabin', 'Rest room; assigned navigators recover physical and mental condition, not asserted specific HP/fatigue statistic.',
     'A room where companions can rest. Anyone assigned here recovers physically and mentally.'),
    (112, 'Recreation Room', 'Navigators and sailors rest; assigned navigator reduces crew fatigue buildup and recovers own fatigue/mental state.',
     'A room where companions and sailors can relax. Assign a companion here to slow the buildup of crew fatigue while helping that companion recover from fatigue and restore their spirits.'),
    (113, 'Lumber Room', 'Repair lumber; assigned Shipwright requires surveying>=130. Repairs while sailing, cheaper shipyard repair; no guaranteed instant repair.',
     'This room holds lumber for ship repairs. Assign a companion with Survey of at least 130 to serve as Shipwright. A Shipwright repairs your ships while you sail and lowers repair costs at the Shipyard.'),
    (114, 'Infirmary', 'Doctor needs observation>=150; less disease, slower crew fatigue buildup, enables disease-curing items.',
     'A room for treating the sick. Assign a companion with Observation of at least 150 to serve as Doctor. A Doctor helps prevent disease, slows the buildup of crew fatigue and lets you use items that cure disease.'),
    (115, 'Galley', 'Cook needs Aim>=70. Slower consumption of both food and water while sailing, slower crew fatigue.',
     'A room for preparing meals. Assign a companion with Aim of at least 70 to serve as Cook. A Cook makes food and water last longer at sea and slows the buildup of crew fatigue.'),
    (116, 'Livestock Room', 'Raises livestock for food; keeper needs vitality>=130; produces food while sailing, not water.',
     'A room for raising livestock for food. Assign a companion with Vitality of at least 130 to serve as Livestock Keeper. A Livestock Keeper produces food while you sail.'),
    (117, 'Chapel', 'Missionary needs persuasion>=160; slows crew fatigue; Square distribute goods can start trend. Some refuse Chapel due to principles/beliefs, no invented religion.',
     'A room where companions and sailors can worship. Assign a companion with Persuasion of at least 160 to serve as Missionary. A Missionary slows the buildup of crew fatigue and lets you [[43|Distribute Goods]] in the Square to start a [[25|trend]]. [Tip] Some companions refuse a Chapel assignment because of their beliefs.'),
    (118, 'Strategy Room', 'Strategist needs tactics>=120. Inspiration enables Tavern plot planning; may preempt enemy plots; gathers other-faction information after inn stay.',
     'A room for planning strategies. Assign a companion with Tactics of at least 120 to serve as Strategist. When your Strategist has an idea, you can [[16|Plan a Scheme]] at the Tavern. A Strategist may also foil enemy schemes and gathers information about other factions when you stay at an Inn.'),
    (119, 'Accounting Room', 'Accountant requires accounting>=100. May obtain trade-house discounts; may buy out stock at twice price; cannot sell at twice price. No unconditional discount/buyout claim.',
     'A room for managing fleet accounts. Assign a companion with Accounting of at least 100 to serve as Accountant. An Accountant may secure discounts at the Trade House. You may also be able to buy out goods by paying twice the price, but you cannot sell goods for double their value.'),
    (120, "Captain's Cabin", 'Source says only protagonist assigned, becomes Captain; slows crew fatigue; required for automatic movement.',
     'The room for the ship\'s commander. Only your main character can be assigned here, taking the role of Captain. A Captain slows the buildup of crew fatigue and is required for [[76|Auto Move]].'),
    (121, "First Mate's Cabin", 'First Mate needs persuasion>=100; Guild send negotiation documents, slows crew fatigue, urges town surrender during town battle.',
     "The room for the Captain's assistant. Assign a companion with Persuasion of at least 100 to serve as First Mate. A First Mate lets you [[27|Send Letters]] at the Guild and slows the buildup of crew fatigue. In battles against towns, the First Mate urges the town to surrender."),
    (122, 'Helm', 'Helmsman needs sailing>=60; easier direction changes, higher automatic movement speed.',
     'The position for steering the ship. Assign a companion with Sailing of at least 60 to serve as Helmsman. A Helmsman makes the ship easier to turn and increases its speed during Auto Move.'),
    (123, 'Survey Room', 'Surveyor needs surveying>=120; high ability shows latitude/longitude while sailing. Required for Auto Move; higher skill increases speed.',
     'A room for taking measurements at sea. Assign a companion with Survey of at least 120 to serve as Surveyor. A skilled Surveyor can tell you your latitude and longitude while sailing. A Surveyor is also required for [[76|Auto Move]]; higher skill increases your speed.'),
    (124, 'Lookout', 'Lookout needs observation>=70; easier discovery towns/etc, view nearby fleet information. High Aim can snipe enemy admiral in battle; success captures that ship, not whole fleet.',
     'A lookout post on the mast. Assign a companion with Observation of at least 70 to serve as Lookout. A Lookout helps you discover towns and other locations at sea and view information about nearby fleets. [Tip] A Lookout with high Aim may snipe the enemy admiral in battle. A successful shot lets you capture that ship.'),
    (125, 'Mast', 'Sail Handler needs sailing>=80; easier sail turning and faster Auto Move. All masts staffed enables automatic sail-angle changes at Half Open only.',
     'The ship\'s mast. Assign a companion with Sailing of at least 80 to serve as Sail Handler. A Sail Handler makes the sails easier to turn and increases your speed during Auto Move. With a Sail Handler at every mast, your companions automatically adjust the sail angle when the sails are [[83|Half Open]].'),
    (126, 'Deck', 'Deckhand needs vitality>=30; improves boarding power. Faster leveling but very high fatigue, advise health, not guaranteed level reward.',
     'The ship\'s deck. Assign a companion with Vitality of at least 30 to serve as Deckhand. A Deckhand strengthens your forces in [[98|boarding battles]]. [Tip] Companions assigned as Deckhands gain levels more easily, but tire very quickly. Keep an eye on their health.'),
    (127, 'Holds', 'Five kinds by function; companions only assigned in Quarters and Batteries; five ordered links.',
     'Storage areas inside the ship, divided into five types by their purpose. Companions can be assigned to the Quarters and Batteries. See [[128|Quarters]], [[129|Batteries]], [[130|Oar Room]], [[131|Supply Hold]] and [[132|Cargo Hold]].'),
    (128, 'Quarters', 'Up to four rooms; Boarding Leader needs Swords>=90; increases boarding power, participates in duels.',
     'Rooms where the boarding crew waits. You can have up to four. Assign a companion with Swords of at least 90 to serve as Boarding Leader. A Boarding Leader strengthens your forces in [[98|boarding battles]] and takes part in [[99|duels]].'),
    (129, 'Batteries', 'Gunner needs Aim>=90; enables more cannon fire, not specified damage/range/reload effect.',
     'The ship\'s gun emplacements. Assign a companion with Aim of at least 90 to serve as Gunner. A Gunner lets your ship fire more cannon shots.'),
    (130, 'Oar Room', 'Sailors row oars; cannot assign navigator; only oar-powered ships.',
     'A room where sailors work the oars. Only ships powered by rowers have one. Companions cannot be assigned here.'),
    (131, 'Supply Hold', 'Stores food/water for voyage; more rooms increase food/water capacity; cannot assign navigator.',
     'A hold for storing food and water for the voyage. More Supply Holds let you carry more of both. Companions cannot be assigned here.'),
    (132, 'Cargo Hold', 'Stores trade goods; more rooms increase capacity; up to five rooms; no navigator assignment.',
     'A hold for storing trade goods. More Cargo Holds let you carry more goods, up to a maximum of five holds. Companions cannot be assigned here.'),
]

if __name__ == '__main__':
    assert not OUT.exists() and [r[0] for r in DRAFTS] == list(range(103,133))
    packet = load(PACKET)
    clean_path = Path(packet['source_ROM'])
    assert sha(clean_path.read_bytes()) == packet['source_ROM_sha256']
    raw = NdsImage.open(clean_path).read_file('/COMMON/HELP.DK4')
    assert sha(raw) == packet['source_archive_sha256']
    blocks = IlnkContainer.parse(raw).blocks
    sources = {r['topic_id']:r for r in packet['records']}
    records = []
    for topic, title, meaning, english in DRAFTS:
        source = sources[topic]
        assert blocks[topic] == bytes.fromhex(source['source_hex'])
        assert english.isascii() and '\n' not in english and '  ' not in english
        import re
        ids = [int(n) for n in re.findall(r'\[\[([0-9]+)\|', english)]
        assert ids == [r['topic_id'] for r in source_links(blocks[topic])], topic
        records.append(dict(id=source['id'], topic_id=topic, source_reference=deepcopy(source['source_reference']), source_hex=source['source_hex'],
            source_Japanese_with_link_IDs=source['source_Japanese_with_link_IDs'], source_meaning=meaning, heading=title, english=english,
            speaker='Help narrator', context='Read with the complete connected Common Commands/Deck/assignments/rooms/holds exchange, source103 through133, plus linked role and movement explanations.',
            localization_note='Natural full instructional prose; preserve distinct companions versus sailors, source qualifications, probabilities and all link destinations. Exact current labels/buttons remain subject to native binding.',
            review=dict(source=True, context=True, localization=False, naturalness=True, formatting=False),
            current_English_comparison_pending=True, native_terms_andcontrols_binding_pending=True, all_fresh_display_gates_pending=True, new_credit=0))
    save(OUT, dict(format='dk4-help103-132-clean-meanings-logical-drafts-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        records=records, records_count=30, source_ROM=str(clean_path), source_ROM_sha256=packet['source_ROM_sha256'], source_HELP_sha256=sha(raw),
        clean_source_packet=str(PACKET), clean_source_packet_sha256=sha(PACKET.read_bytes()), source133_context=sources[133]['source_Japanese_with_link_IDs'],
        earlier_English_exposure_disclosure='Earlier role/skill glossary work exposed bodies114,115,116,123,124,125,128,129,130,132,133 among other out-of-scope articles, and headings110,113,117,118,119,120,121,123,125,126,127,128,129. Existing reviewed terms include Aim, Swords, Sail Handler, Boarding Leader, Deckhand, Quarters, First Mate and Auto Move. This is a new clean-Japanese drafting pass, not a claim that all older English was unseen.',
        draft_precedes_fresh_current_body_extraction=True, native_room_stat_andcommand_labels_provisional_except_already_bound_terms=True,
        all_source_link_sequences_exact=True, no_authored_line_breaks=True, all_current_comparison_andformatting_pending=True,
        new_credit=0, full_goal_complete=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print('30 clean-source meanings and full logical Deck/crew drafts sealed; current comparison, term bindings and display remain.')
