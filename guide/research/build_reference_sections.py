"""Update text-reference sections from the reviewed read-only DS item export."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / 'uncharted-waters-iv-rota-nova-ds-guide.txt'
ITEMS = json.loads((ROOT / 'research/ds-static-item-reference.json').read_text(encoding='utf-8-sig'))
assert len(ITEMS) == 188 and {row['index'] for row in ITEMS} == set(range(188))
assert all(0 <= row['effect'] <= 255 for row in ITEMS)
RULE = '=' * 72
LINE = '-' * 72


def heading(title):
    return f'{RULE}\n{title}\n{RULE}\n'


systems = heading('07. CONTROLS AND GAME SYSTEMS                                  [SYSTEMS]') + '''
07.1  OFFICERS, SAILORS, AND ENDURANCE
------------------------------------------------------------------------
Your named officers and the sailors assigned to ships are different
parts of the crew. Recruiting a companion does not replace the sailors
your fleet needs. In Assign Sailors, compare Need, Now, and Max, then
check Endurance before leaving port. Endurance is expressed in days;
it is not the same thing as a ship's durability. [G1]

Use the one-ship flagship option during Rafael's opening preparation.
As your fleet grows, check each ship rather than assuming the whole
fleet is ready because its total crew count looks healthy.

07.2  READING SAILOR INFO
------------------------------------------------------------------------
  Field       What it tells you
  --------------------------------------------------------------------
  Level       The officer's experience level.
  HP          Current hit points.
  Stamina     Physical stamina attribute.
  Agility     Agility attribute.
  Charm       Personal charm attribute.
  Wits        Intellectual ability.
  Spirit      Mental fortitude; different from the current Mood.
  Luck        Luck attribute.
  Health      Current physical condition.
  Mood        Current mental condition.

Keep attributes, skills, and temporary conditions separate. A high
Spirit value does not mean an officer cannot be Upset or Confused.
An item may improve a particular duty without changing every number
on the page. Inspect the equipment's role and Effect before assigning
it, then compare the relevant officer's displayed abilities. [G1]

Skills use the labels Vigor, Command, Sailing, Survey, Finance,
Swords, Aim, Speech, Guile, and Observe. The duel panel uses Fencing
for sword-fighting skill. These are ability labels, not extra crew
members or separate temporary conditions. [G1]

07.3  CREW DUTIES
------------------------------------------------------------------------
  Duty              Job
  --------------------------------------------------------------------
  Captain           Command of a ship.
  First Mate        Assistance to the captain.
  Strategist        Plans and strategy.
  Purser            Accounts and supplies.
  Surveyor          Surveying and navigation information.
  Sail Handler      Handling sails.
  Helmsman          Steering.
  Lookout           Keeping watch.
  Boarding Leader   Leading the boarding party.
  Gunner            Cannon fire.
  Missionary        Religious duties.
  Surgeon           Medical duties.
  Chief Cook        Preparing food.
  Shipwright        Ship repair duties.
  Animal Keeper     Care of animals.
  Deckhand          General deck duties.

Match Equipment to the duty shown in its item details. Role-specific
equipment has an eligibility check; giving it to somebody with the
wrong duty is not a substitute for placing the right officer at the
station. Exact assignment thresholds still need DS confirmation. [G1]

07.4  HEALTH AND MOOD
------------------------------------------------------------------------
  Health state     Meaning
  --------------------------------------------------------------------
  Healthy          No listed physical problem.
  Tired            Fatigued.
  Hurt             Minor injury.
  Wounded          Serious injury; worse than Hurt.
  Dying            Near death.
  Sick             Illness.
  Dead             Death.

Mood can read High, Good, Relaxed, Normal, Upset, or Confused. High
means an elevated mood here. Confused is a mental condition, while
Hurt and Wounded belong to Health. Check both fields after a difficult
voyage or battle rather than judging the officer by HP alone. [G1]

If Health is worsening, make recovery your next priority instead of
extending the voyage for an optional discovery. Exact recovery times
and guaranteed remedies for each state are not established yet.

07.5  WARNINGS AT SEA
------------------------------------------------------------------------
The warning's name tells you what sort of problem or encounter to
investigate. These labels include ordinary weather and discoveries
as well as dangers; not every message is a disease. [G1]

  Crew problems    Scurvy, Epidemic, Mutiny, Confusion
  Ship/supplies    Rat Infestation, Leaks
  Weather         Storm, Blizzard, Rain, Snow, Lightning, Fog, Calm
  Navigation      Reefs, Drift Ice, Tornado, Whirlpool
  Sea encounters  Giant Squid, Monster Fish, Whales, Dolphins, Sharks
  Other sights    Aurora, Sirens, Mermaids, Strange Bubbles

Keep track of supplies and crew condition when a warning appears.
Do not keep sailing simply because an encounter has an interesting
name. If the fleet is in trouble, a nearby port is a better immediate
objective than the next optional item.

07.6  UTILITY ITEMS TO WATCH FOR
------------------------------------------------------------------------
  Item              Intended use described by the game
  --------------------------------------------------------------------
  Golden Cat        Useful against rats.
  Lime Drops        Described as relieving thirst on a voyage.
  Hermes' Prayer    Described as protecting sailors during storms.
  Hua Tuo's Tonic   Described as effective against infectious disease.

These are the game's descriptions, not tested success percentages.
No consumption rule, exact protection duration, or guaranteed cure
rate is supplied here. In particular, the Lime Drops description alone
does not establish a specific scurvy-treatment procedure. [G1]

DS button/touch controls, disease treatment procedures, and detailed
crew-role effects remain to be added. The reference above covers the
labels and equipment matching, without inventing hidden formulas.

'''

equipment = heading('09. SHIPS, EQUIPMENT, AND COMBAT                                [SHIPS]') + '''
09.1  EQUIPMENT RATINGS
------------------------------------------------------------------------
Use these tables to compare items before deciding whom to equip.
Rating is the item's listed Effect value. It is not its price, a
character's HP, or a promise of that much damage in every battle.
For Equipment, the middle column names the relevant crew duty. [G1]

The tables cover 25 weapons, 25 pieces of armor, and 43 duty items
from the regular DS item catalog. Acquisition locations will be added
to the item directory; a high rating does not mean an item is available
at the beginning of the game.

'''
for category, subheading in [('Weapon', 'WEAPONS'), ('Armor', 'ARMOR'), ('Equipment', 'DUTY EQUIPMENT')]:
    equipment += subheading + '\n' + LINE + '\n'
    equipment += f"  {'Item':31} {'Duty' if category == 'Equipment' else 'Type':18} Rating\n"
    equipment += '  ' + '-' * 64 + '\n'
    for row in ITEMS:
        if row['category'] == category:
            role = (row['role'] or 'Special') if category == 'Equipment' else category
            equipment += f"  {row['name']:31} {role:18} {row['effect']:>3}\n"
    equipment += '\n'
equipment += '''09.2  BEFORE A BATTLE
------------------------------------------------------------------------
Save before committing to a scripted fight. Check crew allocation,
equipment ownership, and who will fill the combat duties. Buying a
weapon is only the first step: confirm Equipped By in the item screen.
Figureheads use Equipped Ship, so check the intended ship too. [G1]

A useful equipment comparison starts with the officer and their duty,
not just the highest number in the table. Keep a practical repair and
recovery plan for the return voyage as well as the battle itself.

Ship prices, capacities, sailing performance, cannon comparisons, and
tested battle setups are still being compiled. No PC ship table has
been substituted for the DS database.

'''

catalog = heading('12. ITEMS, ANCIENT MAPS, AND MYSTERY HUNTING                      [ITEMS]') + '''
12.1  FINDING THE RIGHT KIND OF ITEM
------------------------------------------------------------------------
The regular catalog contains 188 entries. Weapons, armor, and duty
equipment are listed with ratings in section 09. The remaining names
are grouped below so you can distinguish gifts, maps, and quest
objects instead of treating everything as ordinary equipment. [G1]

This is a name/category directory, not yet a complete location guide.
The 10 added DS Mystery Hunting treasures need their own entries;
PSP's extra treasure set is not included as if it belonged to DS.

'''
for category in ['Local Product', 'Navigation Gear', 'Figurehead', 'Gift', 'Mystery Item', 'Proof', 'Proof Map', 'Ruin Map']:
    catalog += category.upper() + '\n' + LINE + '\n'
    names = [r['name'] for r in ITEMS if r['category'] == category]
    for i in range(0, len(names), 2):
        catalog += f"  {names[i]:33}" + (names[i+1] if i+1 < len(names) else '') + '\n'
    catalog += '\n'
catalog += '''12.2  MAPS AND STORY ITEMS
------------------------------------------------------------------------
Keep a Proof Map separate in your mind from a Ruin Map. The former
points toward a regional proof, while the latter concerns a historic
site. The walkthrough identifies the story objects used to obtain
the proof maps. Avoid selling a mysterious item just because it has
no obvious immediate equipment use. [G1]

Use the English name in your inventory to match these lists. Where
Japanese sources use a different spelling, consult the glossary.
Locations, gift recipients, precise effects, and missable conditions
are still being added; absence from the current walkthrough does not
mean an item cannot be found.

'''

text = GUIDE.read_text(encoding='utf-8')
if '09.3  CANNON FIRE:' in text:
    combat_start = text.index('09.3  CANNON FIRE:')
    combat_end = text.index(RULE + '\n10. TRADE GOODS', combat_start)
    equipment = equipment.replace(
        'Ship prices, capacities, sailing performance, cannon comparisons, and\n'
        'tested battle setups are still being compiled. No PC ship table has\n'
        'been substituted for the DS database.\n\n', '')
    equipment += text[combat_start:combat_end]
if '07.7  NORMAL SAILING CONTROLS' in text:
    controls_start = text.index('07.7  NORMAL SAILING CONTROLS')
    controls_end = text.index(RULE + '\n08. HODRAM', controls_start)
    systems = systems.replace(
        'DS button/touch controls, disease treatment procedures, and detailed\n'
        'crew-role effects remain to be added. The reference above covers the\n'
        'labels and equipment matching, without inventing hidden formulas.\n\n', '')
    systems = systems.replace('station. Exact assignment thresholds still need DS confirmation. [G1]',
                              'station. Known DS-help requirements are listed in section 07.9. [G1]')
    systems += text[controls_start:controls_end]
if '12.3  DISCOVERY' in text:
    acquisition_start = text.index('12.3  DISCOVERY')
    acquisition_end = text.index(RULE + '\n13. SECRETS', acquisition_start)
    catalog += text[acquisition_start:acquisition_end]
for start, end, replacement in [('07. CONTROLS AND GAME SYSTEMS', '08. HODRAM', systems), ('09. SHIPS', '10. TRADE GOODS', equipment), ('12. ITEMS, ANCIENT MAPS', '13. SECRETS', catalog)]:
    a = text.index(RULE + '\n' + start)
    b = text.index(RULE + '\n' + end, a)
    text = text[:a] + replacement + text[b:]
assert '[G1] Game text and DS item-reference data.' in text
assert not [line for line in text.splitlines() if len(line) > 80]
GUIDE.write_text(text, encoding='utf-8')
print('Added 16 duty names, 13 status labels, 26 sea labels, and all 188 regular item names.')
