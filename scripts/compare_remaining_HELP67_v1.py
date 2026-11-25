"""Record whole-article source/current decisions; retain good prose and leave all display gates open."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_HELP_T103_T132_v1 import logical_links, plain

ROOT=Path('work/analysis/Shared_HELP_T133_T201_clean_20261105')
DRAFT=ROOT/'clean_meanings_andall67_drafts_v2.json'
CURRENT=ROOT/'current_full_articles_verified_parent_v1.json'
BIND=ROOT/'remaining_active_terms_andcontrols_v1.json'
REASONS={
133:'Retain all16 corresponding job/skill thresholds in source order. Active Vigor, Speech, Guile and Command are correct; the source table justifies separate semantic entries.',
134:'Retain the concise Info hub and all five destinations; descriptive linked article names remain clear alongside abbreviated UI captions.',
135:'Retain the natural select-an-officer instruction and character-data destination.',
136:'Retain the clear ship-selection instruction and ship-data destination.',
137:'Retain faction scope and the conditional ability to change a regional fleet policy.',
138:'Restore the omitted DS Y action, observed removing and equipping Golden Cutlass. Retain the type restriction and source-supported red-name/job advice; consumable use and red warning were not newly activated.',
139:'Use observed Y Auto and policy labels Flagship, Even, Minimum. Preserve Left/Right, all three crew values, shortage penalty and proportional—not equal head-count—distribution. Keep policy explanations continuous across pages.',
140:'Retain all four Functions capabilities in a natural concise sentence.',
141:'Retain discovered-route scope and both discovery/reporting destinations.',
142:'Retain the hearsay about great treasures, torn fragments and guild-visiting advice without inventing treasure locations.',
143:'Retain the six-part data-guide hub and all original destinations.',
144:'Retain visited-city restriction, Route Map context and all seven data links.',
145:'Retain the distinct city/port/village sizes, village resupply-only restriction and possible event promotion.',
146:'Retain cultural-region effects on prices, building signs and available commands.',
147:'Retain all seven source conditions and exact price effects. Active referenced labels Normal/War/Plague/Famine/Boom/Slump/Shortage match.',
148:'Replace the separate Market with Trade House for commercial investment; retain possible new specialties and recruitment/cannon effects.',
149:'Retain Palace/Governor investment locations and reduced surrender likelihood, without turning it into immunity.',
150:'Retain percentage stock access, unlimited selling at1 percent, four growth methods, initial contract requirement, home-port bonus and exclusive-contract link. Move pagination away from You must / obtain.',
151:'Retain100-percent control, monthly tribute, attacks only on enemies and both ways around another faction\'s exclusive contract. Preserve the two source paragraphs instead of splitting Use from its object.',
152:'Use Products for the linked native Product category; retain possible expansion with Growth/delivery and replenishment each arrival month.',
153:'Retain the concise sea-data introduction and all four destinations.',
154:'Retain latitude/longitude and the highly skilled Surveyor condition; do not invent a numerical threshold.',
155:'Retain separate food-or-water exhaustion and sharply rising crew fatigue.',
156:'Retain fleet-wide sailor count and the zero-sailor game-over condition.',
157:'Retain the exact100 fatigue threshold and possible mutiny, without promising a guaranteed revolt.',
158:'Retain all seven character-data destinations, including active HP and Vigor and the distinct physical Health article.',
159:'Retain all six active moods, the two inefficient states and both recovery assignments.',
160:'Retain the six source conditions with active labels, reduced/prevented work, cabin recovery and Surgeon medicine. Do not add the native extra Dead state to this six-state explanation.',
161:'Retain innate-ability meaning and all six actual attribute labels: Stamina, Agility, Charm, Wits, Spirit, Luck.',
162:'Retain physical toughness and lower collapse likelihood without conflating Stamina with the Vigor skill.',
163:'Retain both speed and dexterity and the broad combat advantage.',
164:'Retain charisma/presence and winning people over, with no invented rank or leadership requirement.',
165:'Retain wisdom/knowledge and more effective handling of situations under the active Wits label.',
166:'Retain strength of will and remaining calm in a crisis under the active Spirit label.',
167:'Retain good fortune and easier escape from danger without inventing percentages.',
168:'Retain HP injury loss, zero-HP Dying state, gradual recovery and Vigor\'s maximum-HP/resilience/illness/job/attribute effects. Separate the two source concepts so illness / less likely is not split across pages.',
169:'Retain sailing experience and level gains from sailing and other activities.',
170:'Retain starting variation, level-up growth, item bonuses and all ten actual skill destinations.',
171:'Retain captain/admiral leadership ability and Spirit/Charm influences; Command is the active skill.',
172:'Retain quicker ship handling, both linked jobs and Agility/Spirit influences.',
173:'Retain both accurate gunfire and cooking, both jobs and Agility/Luck influences.',
174:'Retain survey/mapmaking, wider-area positioning, both jobs, Agility/Wits and equipping a sextant to the Surveyor. Active item reference confirms Sextant.',
175:'Retain diplomatic aptitude, First Mate/Missionary suitability and Wits/Charm with active Speech.',
176:'Retain accounting, bargaining in both price directions, Purser suitability and Wits/Spirit.',
177:'Retain devising schemes, easier strategic inspiration, Strategist suitability and Wits/Luck with active Guile.',
178:'Retain swordsmanship, boarding and duels, Boarding Leader suitability and Stamina/Agility.',
179:'Retain noticing surroundings/danger, distance and illness benefits, both jobs and Spirit/Luck.',
180:'Retain item/weapon/armor scope and the natural empty-slot versus equipped-slot action instructions.',
182:'Retain home-port relocation only when the faction\'s local share reaches zero, plus both source links.',
183:'Retain flags as one point each, fleet-count bonus share and battle/scheme-only loss. The existing wording already resolves the clean source without extra mechanics.',
185:'Retain three basic relations plus See also Subordinate, preserving the source\'s three-stage statement and fourth related link.',
186:'Retain no attacks on allied fleets and possible nearby aid rather than guaranteed assistance.',
187:'Retain automatic sea battles, hostile exclusive-contract cities and all investment/battle share-taking methods.',
188:'Retain the natural neutral-relations explanation without adding hostility or an alliance.',
189:'Replace both Threaten links with the reviewed Coerce action; retain submission, guild letters and Proof of Conquest requirement.',
190:'Retain friendliness toward the player and the higher-is-better relationship scale.',
191:'Use Trade House instead of the separate Market for trade; retain local specialties, city/market-condition prices and cultural-region base prices.',
192:'Retain18 categories and the price linkage among all goods in the same category.',
193:'Retain grades1–5,1 best, Growth-based specialty improvement and greater profits for better goods.',
194:'Identify native Product items naturally as raw materials and use Trade House. Retain possible growth, unsuitable-city and five-specialty limits, multiple suitable cities and high-share advice.',
195:'Retain Info/Ship Info navigation and all five ship-data destinations.',
196:'Retain current/maximum hull meaning, undamaged equality and shipyard restoration.',
197:'Retain required/current/maximum crew and the Assign Sailors destination.',
198:'Retain exhaustion fatigue and food-only conservation by Animal Keepers and Chief Cooks; do not extend it to water.',
199:'Retain main plus auxiliary square sails, following-wind benefit, mainmast equipment, fore/mizzen positions and possible absent masts.',
200:'Retain main plus auxiliary fore-and-aft sails, upwind benefit, mainmast equipment, fore/mizzen positions and possible absent masts; add no direct-upwind mechanics.',
201:'Retain strictly exceeds500 percent and both reporting/record links. The existing translation already has the correct boundary; do not change it to at least500.'}

def body(row):
    pages=[row,*row['complete_current_continuations']]; result=[]
    for p in pages:
        text=p['current_English_with_link_IDs'].split('\n',1)[1]
        text=re.sub(r'\[\[\d+\|(?:Continue reading|Back to article start)\]\]', '', text)
        result.append(text)
    return logical_links(' '.join(result))

if __name__=='__main__':
    out=ROOT/'whole_article_comparisons_v1.json';assert not out.exists()
    draft,current,binding=map(load,[DRAFT,CURRENT,BIND]);by={r['topic_id']:r for r in current['records']}
    assert set(by)==set(REASONS)==set(range(133,202))-{181,184}
    rows=[]
    for source in draft['records']:
        row=deepcopy(source);n=row['topic_id'];old=by[n];text=body(old);english=text
        assert row['source_hex']==old['source_hex'] and not old['continuation_foreign_incoming_links']
        title=old['current_English_with_link_IDs'].split('\n',1)[0].strip()
        if n==138:english=english.replace('can equip or use it.','can press Y to equip or use it.')
        if n==139:
            english="Distribute sailors among your ships. Each ship shows Need, Now and Max: required, current and maximum crew. Press Left or Right to adjust a ship's current crew, or press Y for Auto. Ships below Need sail more slowly. Auto offers three policies: Flagship gives priority to the flagship; Even assigns the same percentage of maximum crew to each ship; Minimum assigns only the required crew."
        if n==148:english=english.replace('at the market.','at the Trade House.')
        if n==152:english=english.replace('source items','products').replace('Source Items.','Products.')
        if n==189:english=english.replace('Threaten','Coerce')
        if n==191:english=english.replace('at markets.','at the Trade House.')
        if n==194:
            title='Products';english=english.replace('Source items can create','Products are raw materials that can create').replace('to the market,','to the Trade House,')
        decision='retention' if plain(english)==plain(text) else 'revision'
        assert (decision=='revision')==(n in [138,139,148,152,189,191,194])
        # Navigation belongs to the formatter; all clean-source informational links remain.
        assert [int(x) for x in re.findall(r'\[\[(\d+)\|',english)]==[r['topic_id'] for r in source_links(bytes.fromhex(row['source_hex']))]
        row.update(heading=title,english=english,current_English='\n\n'.join(p['current_English_with_link_IDs'] for p in [old,*old['complete_current_continuations']]),
            complete_current_logical_body=text,current_reference=old['current_reference'],current_hex=old['current_hex'],
            current_continuations=old['complete_current_continuations'],decision=decision,finding=REASONS[n],
            retention_reason=REASONS[n] if decision=='retention' else None,localization_note=REASONS[n],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            current_comparison_pending=False,native_binding_pending=False,independent_draft_pending=False,
            active_term_andcontrol_binding=str(BIND),active_term_andcontrol_binding_sha256=sha(BIND.read_bytes()),
            fresh_display_gates_pending=True,registered_integration_pending=True,new_credit=0)
        # Logical source paragraphs/entries, not manually positioned line breaks.
        if n==133:
            row['semantic_sections']=[p.strip() for p in english.rstrip('.').split(';')]
            row['semantic_section_reason']='The clean Japanese is a16-entry requirements table. Preserve entries as semantic rows, with automatic native wrapping and existing209 ownership.'
        if n in [139,150,151,168]:
            split={139:['Auto offers three policies:'],150:['Increase your share through','At your faction'],
                   151:['You cannot obtain a contract'],168:['The Vigor skill']}[n]
            sections=[english]
            for marker in split:
                assert sum(s.count(marker) for s in sections)==1
                for i,s in enumerate(sections):
                    if marker in s:
                        at=s.index(marker);sections[i:i+1]=[s[:at].strip(),s[at:].strip()];break
            row['semantic_sections']=sections;row['semantic_section_reason']='Preserve complete source concepts/paragraphs; the formatter owns all row and page boundaries.'
        rows.append(row)
    assert len(rows)==67 and sum(r['decision']=='revision' for r in rows)==7
    doc=dict(format='dk4-remaining-help67-whole-article-comparisons-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path=current['file_path'],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        source_current_HELP_sha256=current['current_archive_sha256'],records=rows,records_count=67,
        proposed_revisions=7,justified_retentions=60,first_four_gates_passed=67,all_fifth_gates_pending=True,
        all60_retained_bodies_word_exact_after_removing_native_phase_padding_andnavigation=True,
        existing_owned_continuations={str(n):[p['topic_id'] for p in by[n]['complete_current_continuations']] for n in by if by[n]['complete_current_continuations']},
        active_skill_names_Vigor_Speech_Guile_preserved=True,no_blanket_unconsulted_English_claim=True,
        clean_source_gloss_localized_terms_in_original_intake_remain_provisional_historical_not_shipped=True,
        actual_UI_controls_not_actual67_Help_pages=True,all67_fresh_formatting_native_visual_andregistered_integration_pending=True,
        new_credit=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DRAFT,CURRENT,BIND,Path(__file__)]})
    save(out,doc)
    print('All67 whole-article comparisons:7 revisions/60 justified exact-body retentions;four prose gates pass,all fresh formatting/display gates remain.')
