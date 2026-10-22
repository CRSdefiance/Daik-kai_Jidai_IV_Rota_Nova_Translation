"""Render DS discovery facts with catalog names and qualified clue requirements."""
import json
import re
import textwrap
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = 'https://dekunobou-rotanova.seesaa.net/article/28642373.html'
raw = '''Mediterranean|Venus de Milo|N43|E12|D
Mediterranean|Hermes' Prayer|N42|E29|D
Mediterranean|Celestial Turban|N36|E35|D
Mediterranean|Black Rapier|N39|E1|R
Mediterranean|Azure Talwar|N30|E18|R
Mediterranean|Phidias' Chisel|N38|E20|With Manuel, visit Alexandria's trading post, then Athens' shipyard.
Mediterranean|Minotaur Axe|N35|E26|Take Emilio to the Crete tavern.
Mediterranean|Minerva Shield|N37|E28|Enter Lisbon with Julio. The source also mentions visiting every guild (uncertain) and parking Christina's regional fleet in the Southeast Asian cultural area. Whether all these gates apply together remains unresolved.
Mediterranean|Hestia's Pot|N32|E22|With Emilio, visit Cyprus or Ragusa; the source leaves the precise facility unspecified.
Mediterranean|Gregory's Crown|N40|E15|Take Carlo to Venice's trading post.
Mediterranean|Judas' Demonblade|N32|E34|Visit every guild, station Janus' regional fleet in the Italian cultural area, then visit a guild.
Mediterranean|Poseidon's Roar|N38|W28|Visit every guild, station Charles' regional fleet in the West African cultural area, then visit a guild.
Mediterranean|Herophilus' Medicine|N43|E38|Bring Carlo to the Arab cultural area with Observe at least 150; the source does not identify a precise facility.
Mediterranean|Holy Spear of Ares|N37|E26|With Ian and the Mediterranean proof, visit Istanbul's tavern.
Mediterranean|Charles Martel Armor|N43|E3|With Gerhard and the Africa, Indian Ocean, and East Asia proofs, visit Nantes' square.
North Sea|Blue Oak Shield|N43|W4|R
North Sea|White Flamberge|N68|E16|R
North Sea|Orcrist of Atonement|N60|E27|R
North Sea|Lohengrin Saber|N52|E4|With Christina, visit a square in the German cultural area.
North Sea|Attila Suit|N55|E20|Take Manuel to Ragusa's square.
North Sea|Magic Leather Gloves|N55|E8|With Janus, visit Copenhagen's departure dock.
North Sea|Sweeping Katzbalger|N62|E18|Enter Bruges with Gerhard.
North Sea|Demon-Piercing Arrow|N58|W6|With Cesare, visit London's shipyard. Have at least 20% of the maximum sailor complement.
North Sea|Vepar Halberd|N64|W15|With Manuel, use Sofala's Zimbabwe temple lead and at least 50% Sofala share. Hodram also has a Sofala-square branch after Espinosa falls, while leading African influence.
North Sea|Phoenix Bascinet|N54|W0|With Samuel and Giant Tortoise Shield, visit Cape Town's departure dock.
North Sea|Excalibur|N50|W4|Use the Bristol square then tavern with the protagonist's Swords at least 200. Required proofs differ by protagonist; see the checklist below.
Africa|Silver Sallet|N21|W17|D
Africa|Coffee Tree|S9|E39|D
Africa|Lime Drops|N0|E6|D
Africa|Kanem Warrior Shield|N3|E10|R
Africa|Zealot Cuirass|N5|W3|R
Africa|Loyal Falchion|S25|E46|R
Africa|Crimson Ringmail|S4|E39|R
Africa|Armadillo Hide|S15|E46|Take Samuel to Muscat's departure dock.
Africa|Peacock Mail|S47|E37|Enter Bruges with Samuel and Phoenix Bascinet on days 1-15 of the month.
Africa|Amber Brigandine|N16|W24|Enter Cape Verde with Charles and at least one barrel of Amber.
Indian Ocean|Lamenting Jar|N28|E33|D
Indian Ocean|Golden Cat|N23|E35|D
Indian Ocean|Hero's Scimitar|N18|E57|R
Indian Ocean|Fallen Angel Katar|N22|E59|R
Indian Ocean|Bloodstained Shamshir|N16|E41|With Al, visit a tavern in the Indian cultural area.
Indian Ocean|Aristarchus Telescope|N28|E51|Bring Janus to Hormuz; the source does not name a facility.
Indian Ocean|Giant Tortoise Shield|N8|E78|With Samuel and Armadillo Hide, visit Manila's trading post.
Indian Ocean|Saladin's Silver Armor|N29|E32|Bring Al to Beirut's square. The source says either dialogue choice works.
Indian Ocean|Guiding Staff|N15|E80|Departure event after at least 80% Calicut share, visits to every town, and the Africa, Indian Ocean, and Southeast Asia proofs. Protagonist requirements are listed below.
Indian Ocean|Gupta Spirit Beast|N21|E72|With Fernando, visit a guild after visiting every guild and stationing Jam's regional fleet in the Indian cultural area.
Indian Ocean|Timur's Chainmail|N27|E49|With Cesare, visit a guild after visiting every guild and stationing Ian's regional fleet in the Arab cultural area.
Southeast Asia|Cinnamon Tree|N3|E101|D
Southeast Asia|Dolphin Figurehead|S6|E115|D
Southeast Asia|Dragon Figurehead|N7|E117|D
Southeast Asia|World Pun Book|N1|E104|R
Southeast Asia|Valiant Bec de Corbin|N1|E120|R
Southeast Asia|Milky Way Chart|N0|E132|R
Southeast Asia|Lion-Fang Saw|N9|E99|R
Southeast Asia|Cooling Armor|S8|E126|R
Southeast Asia|Medusa Shield|S40|E144|With Julian, visit Basra's tavern after building friendship with its tavern character Safia. The source gives no numerical friendship threshold.
East Asia|Shosoin Pitcher|N34|E135|D
East Asia|Tea Plant|N24|E120|D
East Asia|Pink Apron|N39|E127|R
East Asia|Art of War|N30|E120|R
East Asia|Noritsune's Armor|N33|E130|With Gerhard, sail from Osaka to Nagasaki and visit Nagasaki's departure dock.
East Asia|Zhao Yun's Spear|N21|E108|Visit Hangzhou's guild on the 10th. Choose the answers meaning you know the story, then Zhao Yun; exact English dialogue labels still need matching.
East Asia|Ninja Garb|N34|E136|With Yukihisa and Angelo, visit a guild in the Mediterranean cultural area.
East Asia|Bladebreaker Gi|N51|E141|With Ifa, visit an inn in the Southeast Asian cultural area.
East Asia|Empress Gown|N38|E117|Take Julian to Malacca's tavern.
East Asia|Kublai's Greatsword|N34|E120|Visit Quanzhou's square with the Africa proof.
East Asia|Muramasa|N45|E149|Visit every guild, station Yukihisa's regional fleet in the Japanese cultural area, then visit a guild.
New World|Gold Dust|N15|W85|D
New World|Maiden Figurehead|N10|W61|D
New World|Spirit Dress|N15|W61|R
New World|Tula Warrior Helm|N28|W95|R
New World|Tlaloc Knife|N22|W97|Rafael receives the lead through Havana's guild request. Other protagonists use a Treat Everyone clue.
New World|Warrior Ocarina|S4|W35|R
New World|Heavenly Wristband|N26|W82|R
New World|Red-Haired Pirate Sword|N24|W75|Take Christina to Seville's tavern.
New World|Jaguar God's Vest|N19|W104|Enter Tunis with Samuel on day 16 through the end of the month.'''

catalog = json.loads((root/'research/ds-static-item-reference.json').read_text(encoding='utf-8-sig'))
by_name = {item['name']: item for item in catalog}
records = []
for line in raw.splitlines():
    region, name, latitude, longitude, clue = line.split('|')
    assert name in by_name, name
    assert re.fullmatch('[NS][0-9]+', latitude)
    assert re.fullmatch('[EW][0-9]+', longitude)
    records.append(dict(region=region, name=name, latitude=latitude,
                        longitude=longitude, clue=clue, index=by_name[name]['index'],
                        source=source, status='DS-source report; not gameplay-tested'))
assert len(records) == len({r['index'] for r in records})
(root/'research/ds-discovery-reference.json').write_text(json.dumps(records, indent=2)+'\n', encoding='utf-8')

section = '''12.3  DISCOVERY COORDINATES AND CLUE REQUIREMENTS
------------------------------------------------------------------------
Get the clue before sailing to an item. These locations and event
requirements follow the DS discovery list [S1D]; knowing a coordinate
is not assumed to replace the clue flag. Keep the required officer
aboard for their event, and plan provisions for the return trip.

D = drink at a tavern for a clue. R = Treat Everyone for a clue.
Neither action has a guaranteed number of attempts in the source.
A numbered clue is explained after its regional table. These entries
are source reports, not searches verified in every protagonist's save.

'''
number = 0
for region in dict.fromkeys(r['region'] for r in records):
    section += region.upper()+'\n\n'
    section += '  Item                         Latitude Longitude Clue\n'
    section += '  --------------------------------------------------------------------\n'
    notes = []
    for row in (r for r in records if r['region']==region):
        clue = row['clue']
        if clue not in ('D','R'):
            number += 1
            notes.append((number, clue))
            clue = str(number)
        section += f"  {row['name']:29}{row['latitude']:9}{row['longitude']:10}{clue}\n"
    section += '\n'
    for num, note in notes:
        section += textwrap.fill(note, width=76, initial_indent=f'{num:2}. ', subsequent_indent='    ')+'\n\n'
section += '''EXCALIBUR: PROOFS TO HAVE BEFORE BRISTOL
  Rafael: North Sea, Africa, Indian Ocean, East Asia, New World.
  Hodram: North Sea, Africa, Indian Ocean, Southeast Asia, East Asia.
  Lil: Mediterranean, Africa, Indian Ocean, East Asia; also lead New
       World influence.
  Maria: Mediterranean, Africa, Indian Ocean, Southeast Asia, East Asia.
  Each branch also needs the protagonist's Swords at least 200.

GUIDING STAFF: OFFICER REQUIREMENTS
  Rafael: Julio; choose the response meaning "Please tell me."
          Its exact translated button label still needs matching.
  Lil: Camille. Hodram: Charles. Maria: no additional officer listed.
  The source says "every town" without defining the full set needed.
  Keep that scope unresolved rather than assuming a single region.

SAMUEL'S ARMOR CHAIN
  Muscat dock -> Armadillo Hide -> Manila trading post -> Giant
  Tortoise Shield -> Cape Town dock -> Phoenix Bascinet -> Bruges
  arrival on days 1-15 -> Peacock Mail. Search for each item before
  starting the next lead. Tunis on days 16 onward gives a separate
  Jaguar God's Vest lead. The date belongs to the clue event, not a
  claim that the buried treasure itself only appears on those days.

Read both hemispheres carefully. N0 and W0 preserve the source's
notation, and source-region headings need not match an item's modern
geographical location. These discoveries cover the DS article's list,
not every regular item: shop stock, story rewards, and the ten Mystery
Hunting treasures have separate acquisition rules.

'''
guide = root/'uncharted-waters-iv-rota-nova-ds-guide.txt'
text = guide.read_text(encoding='utf-8')
start = text.index('12.3  DISCOVERY')
end = text.index('12.4  PURCHASES')
text = text[:start]+section+text[end:]
assert all(len(line)<=80 for line in text.splitlines())
guide.write_text(text, encoding='utf-8')
print(f'Added {len(records)} DS-source discovery locations and clue requirements.')
