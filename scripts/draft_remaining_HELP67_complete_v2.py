"""Finish the45 source-only drafts; preserve the original67 meanings and22 earlier drafts."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T133_T201_clean_20261105')
PRIOR=ROOT/'clean_meanings_andfirst22_drafts_v1.json'
OUT=ROOT/'clean_meanings_andall67_drafts_v2.json'
DRAFTS={
155:('Food and Water','The barrels of food and water remaining. If either runs out, crew fatigue rises sharply.'),
156:('Sailors','The total number of sailors in your fleet. If it reaches zero, the game is over.'),
157:('Fatigue','Your sailors\' fatigue. At 100, you begin losing sailors. High fatigue can also lead to mutiny.'),
158:('Character Data','Information about a character. See [[159|Mood]], [[160|Physical Condition]], [[161|Basic Attributes]], [[168|HP and Health]], [[169|Level]], [[170|Skills]] and [[180|Equipped Items, Weapons and Armor]].'),
159:('Mood','A navigator\'s mental state has six levels: Elated, Energetic, Relaxed, Normal, Irritable and Confused. Irritable or Confused navigators work less efficiently. Assign a navigator to a [[111|Private Cabin]] or [[112|Recreation Room]] to help restore their mood.'),
160:('Physical Condition','A navigator\'s physical condition has six states: Healthy, Fatigued, Lightly Wounded, Severely Wounded, Near Death and Plague. Poor condition makes a navigator less effective at their job and may prevent them from working. A [[111|Private Cabin]] helps them recover. A [[114|Surgeon]] can treat Plague with medicine or other curative items.'),
161:('Basic Attributes','A navigator\'s underlying potential. Basic attributes influence their skills. See [[162|Stamina]], [[163|Agility]], [[164|Charm]], [[165|Intellect]], [[166|Will]] and [[167|Luck]].'),
162:('Stamina','Physical hardiness. A higher value makes a navigator harder to bring down.'),
163:('Agility','Speed and dexterity. A higher value gives a navigator an advantage in combat.'),
164:('Charm','Charisma and personal presence. A higher value makes it easier to win people over.'),
165:('Intellect','Wisdom and knowledge. A higher value helps a navigator handle problems more effectively.'),
166:('Will','Strength of will. A higher value helps a navigator keep their head in a crisis.'),
167:('Luck','Good fortune. A higher value makes it easier to escape danger.'),
168:('HP and Health','HP falls when a navigator is wounded, such as in a [[99|duel]]. At zero HP, their condition becomes Near Death. HP gradually recovers with a stay at an Inn or an assignment to a [[111|Private Cabin]] or [[112|Recreation Room]]. Health determines maximum HP and physical hardiness. High Health makes illness less likely and suits an [[116|Animal Keeper]] or [[126|Deckhand]]. It is influenced by Stamina and Will.'),
169:('Level','A navigator\'s level of experience. It rises as they gain experience through sailing and other activities.'),
170:('Skills','Skills show which jobs suit a navigator. Starting values vary by navigator, and skills rise as they gain levels. Equipping items can also raise certain skills. See [[171|Command]], [[172|Sailing]], [[174|Survey]], [[176|Finance]], [[179|Observe]], [[168|HP and Health]], [[173|Aim]], [[178|Swords]], [[175|Social]] and [[177|Tactics]].'),
171:('Command','The ability to lead sailors and companions as a Captain or Admiral. High Command suits a navigator for leadership. It is influenced by Will and Charm.'),
172:('Sailing','The ability to handle a ship. High Sailing makes ship handling quicker and suits a [[122|Helmsman]] or [[125|Sail Handler]]. It is influenced by Agility and Will.'),
173:('Aim','The concentration needed to hit a target. High Aim helps with accurate gunfire and good cooking, making a navigator suited to [[129|Gunner]] or [[115|Chief Cook]]. It is influenced by Agility and Luck.'),
174:('Survey','The ability to survey and draw charts. High Survey lets a navigator work out your position accurately over a wider area and suits a [[123|Surveyor]] or [[113|Shipwright]]. It is influenced by Agility and Intellect. [Tip] Equipping a Sextant or similar item raises Survey. Give one to your Surveyor.'),
175:('Social','An aptitude for diplomacy. High Social suits a [[121|First Mate]] or [[117|Missionary]]. It is influenced by Intellect and Charm.'),
176:('Finance','The ability to manage accounts. High Finance helps you bargain for lower purchase prices and higher sale prices. It suits a [[119|Purser]] and is influenced by Intellect and Will.'),
177:('Tactics','The ability to devise clever strategies. A high value makes ideas for schemes more likely and suits a [[118|Strategist]]. It is influenced by Intellect and Luck.'),
178:('Swords','An aptitude for sword fighting. High Swords gives an advantage in [[98|boarding battles]] and [[99|duels]], making a navigator suited to [[128|Boarding Leader]]. It is influenced by Stamina and Agility.'),
179:('Observe','The ability to notice your surroundings and sense danger. High Observe helps a navigator spot distant things and treat illness, making them suited to [[124|Lookout]] or [[114|Surgeon]]. It is influenced by Will and Luck.'),
180:('Equipped Gear','The item, weapon and armor a navigator has equipped. Select an empty slot to equip something, or select equipped gear to remove it.'),
182:('Home Port','The location of a faction\'s home port. If its [[150|share]] in that town falls to zero, the home port moves to another town. See [[183|Home Port Points]].'),
183:('Home Port Points','A faction gains bonus share in its home port equal to the number of fleets it has. This bonus is called Home Port Points and is shown as flags, one per point. Other factions can take this bonus share only through battle or schemes.'),
185:('Relations','Diplomatic relations have three basic states. They can change through [[16|Plot]] at the Tavern or [[27|Send Letter]] at the Guild. See [[188|Normal]], [[186|Allied]] and [[187|At War]]. [[189|Subordinate]] describes a faction that has submitted to you.'),
186:('Allied','You have an alliance with this faction and cannot attack its fleets. Nearby allied fleets may help you in battle.'),
187:('At War','You are at war with this faction. Approaching one of its fleets at sea automatically starts a battle. Towns where it holds an [[151|exclusive contract]] also attack you. You can take market share from a faction you are at war with through [[23|Commercial Investment]], [[37|Military Investment]] or battle.'),
188:('Normal','Normal diplomatic relations.'),
189:('Subordinate','A faction that has submitted to you will not attack your main fleet. To bring a faction under your control, choose [[27|Send Letter]] at the Guild and succeed with [[33|Coerce]]. [[33|Coerce]] requires a [[4|Proof of Conquest]].'),
190:('Friendship','How well a faction gets along with you. The higher the rating, the better your relationship.'),
191:('Trade Goods Data','Trade goods are bought and sold at the Trade House. The goods a town sells are its local specialties, which vary from town to town. Prices vary by town and fluctuate with market conditions. Base prices differ by cultural region. See [[192|Type]] and [[193|Grade]].'),
192:('Type','Trade goods fall into 18 categories. Goods in the same category are affected by market conditions together. Trading one good changes prices for all goods in its category.'),
193:('Grade','Trade goods are graded from 1 to 5, with Grade 1 the best. As a town\'s [[148|Growth]] rises, the grades of its [[152|local goods]] also improve. [Tip] Higher grades mean finer goods. Trading higher-quality goods brings greater profits.'),
194:('Raw Materials','Items that can become new local goods. Bring one to a Trade House and it may add a new specialty to that town. It will not work in an unsuitable town or one that already has five local goods. [Tip] Several towns may suit a raw material. Choose somewhere convenient, such as a town where your faction has a high [[150|share]].'),
195:('Ship Data','View a ship\'s data by choosing Ship Info from the Info menu and selecting a ship. See [[196|Durability]], [[197|Sailors]], [[198|Water and Food]], [[199|Square-Sail Performance]] and [[200|Fore-and-Aft Sail Performance]].'),
196:('Durability','Shows current and maximum durability. A ship is undamaged when the two values are equal. If current durability is below the maximum, repairs at a Shipyard restore it.'),
197:('Sailors','Shows the required, current and maximum number of sailors for the ship. Use [[139|Assign Sailors]] in the shared commands to change the crew assigned to each ship.'),
198:('Water and Food','The barrels of water and food remaining. If either runs out, crew fatigue rises sharply. [Tip] An [[116|Animal Keeper]] or [[115|Chief Cook]] helps food last longer.'),
199:('Square-Sail Performance','The combined performance of the main and secondary square sails. A higher value increases your speed with a following wind. Main-sail performance depends on the [[52|sail type]] and equipment on the mainmast. Secondary performance comes from the foremast ahead of the mainmast and the mizzenmast behind it. Some ship types lack these masts.'),
200:('Fore-and-Aft Sail Performance','The combined performance of the main and secondary fore-and-aft sails. A higher value increases your speed against the wind. Main-sail performance depends on the [[52|sail type]] and equipment on the mainmast. Secondary performance comes from the foremast ahead of the mainmast and the mizzenmast behind it. Some ship types lack these masts.'),
201:('Discover a Golden Route','A trade with a profit margin greater than 500 percent reveals a Golden Route. [Tip] Report routes you discover to the Guild. See [[81|Report a Golden Route]] and [[141|Golden Route Log]].'),
}

if __name__=='__main__':
    assert not OUT.exists();prior=load(PRIOR);doc=deepcopy(prior)
    expected=(set(range(133,202))-{181,184})-set(range(133,155));assert set(DRAFTS)==expected and len(expected)==45
    clean_path=Path(prior['source_ROM']);assert sha(clean_path.read_bytes())==prior['source_ROM_sha256']
    raw=NdsImage.open(clean_path).read_file('/COMMON/HELP.DK4');assert sha(raw)==prior['source_HELP_sha256'];blocks=IlnkContainer.parse(raw).blocks
    for row in doc['records']:
        n=row['topic_id'];assert blocks[n].hex()==row['source_hex']
        if n==168:row['source_meaning']=row['source_meaning'].replace('all4source links','all5source links')
        if n in DRAFTS:
            assert row['english']is None and row['independent_draft_pending']
            heading,english=DRAFTS[n]
            assert english.isascii()and '\n'not in english and '  'not in english
            assert [int(t)for t in re.findall(r'\[\[(\d+)\|',english)]==[r['topic_id']for r in source_links(blocks[n])],n
            row.update(heading=heading,english=english,independent_draft_pending=False)
            row['review']['naturalness']=True
    assert all(r['english']and r['review']['source']and r['review']['context']and r['review']['naturalness']and not r['review']['localization']and not r['review']['formatting']for r in doc['records'])
    assert all(r==next(s for s in prior['records']if s['topic_id']==r['topic_id'])for r in doc['records']if r['topic_id']<155)
    doc.update(format='dk4-remaining-help67-clean-meanings-all-drafts-v2',sealed_source_drafts=67,remaining_independent_drafts=0,
        previous_intake=str(PRIOR),previous_intake_sha256=sha(PRIOR.read_bytes()),all67_drafts_precede_fresh_current_body_extraction=True,
        native_basic_attributes_moods_conditions_andremaining_UI_names_provisional=True,
        approved_Proof_of_Conquest_Coerce_andinvestment_terms_reused_from_already_reviewed_topics=True,
        fresh_current_comparisons_andall_localization_display_integration_still_pending=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(OUT,doc)
    print('All67 independent Help drafts sealed:45 new drafts,first22 unchanged. Exact clean bytes/link order pass; current comparison/native/display gates remain.')
