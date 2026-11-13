"""Compare21 complete Help articles,including the existing Rafael continuation,from sealed clean drafts."""
import re
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early_topics_clean_20261104')
RETAIN={
0:'Retain Help Index,all five correct destinations andthe accurate exclamation-marker explanation. These already form a natural functional index;ordinary wrapping isseparate.',
1:'Retain the established game title andclear overview introduction. All four source destinations andtheoverview/objective purpose arealready accurate.',
2:'Retain the natural invitation to sail withcompanions,the seven-region faction setup andtrade/battle objective. The surrounding maritime context makes seven seas an idiomatic equivalent,not a new count.',
5:'Retain the existing Mysterious Token term andthe natural rumor/unknown-nature explanation. Both object identity andhow itguides itsowner remain uncertain,as in Japanese.',
6:'Retain the initial three-captain restriction,different benefits/difficulty andall three approved full names. Captain describes the playable fleet-leader role;At first avoids wrongly limiting later unlocks.',
7:'Retain the clear Portuguese/Lisbon introduction,accessible early companions,20 percent military-investment discount anddoubled discovery bonus. The second bonus alreadyexists oncurrent continuation202. Do not misreport itas omitted orcredit that physical page asa second article.',
11:'Retain the existing clear building-sign instruction,City-only condition andall twelve correct destinations. Detach punctuation/leading spaces fromlink labels andrestore the source tip marker asformatting work;the ordinary English words remain unchanged.',
17:'Retain the concise accurate instruction:Draw a rival fleet to a chosen city in the current sea region. It preserves both choosing a destination andthe region restriction without inventing combat orcapture.',
}
REVISE={
3:('Game Goal',
   'Each captain has a different goal at the start. Rafael wants to become an accomplished sailor; Lil wants to make a fortune; Hodram wants to make his navy the strongest in the world. Every captain must collect all seven Proofs of Conquest and achieve supremacy in every sea region to complete the game. See [[4|Proofs of Conquest]].',
   'Correct unapproved Raphael toRafael. Restore accomplished sailor,the world-strength goal andexplicit completion condition;restore the missing original link4. Preserve the distinct three motivations.'),
4:('Proof of Conquest',
   "Each sea has one treasure proving its owner's supremacy. Blind searching will fail. Gather information and clues around the world. Rumor says [[5|Mysterious Tokens]] guide sailors to them.",
   'Retain the effective existing explanation andwarning. Remove unsupported worthy,which implies a moral orworthiness prerequisite absent fromclean Japanese;restore original link5 andkeep the rumor qualifier.'),
8:('Lil Argot',
   'A Dutch woman chasing a fortune through world trade. She starts with little money and powerful rivals nearby, making her route challenging. Home port: Amsterdam (North Sea). [Benefit 1] Sells trade goods for 5 percent more than normal. [Benefit 2] Selling goods that are in fashion grants twice the usual [[184|Influence]].',
   'Restore North Sea andthe source woman identity;make the limited starting funds/nearby rivals clear. Preserve the exact5 percent sale bonus andfashion-specific doubled gain;restore link184. Influence follows the existing Help184 label,with cross-consumer Power consistency still pending.'),
9:('Hodram Joakim Bergstrom',
   'A Swedish admiral determined to make his underfunded navy the strongest in the world. He starts with good ships thanks to his military position, but powerful rivals are nearby. Home port: Stockholm (North Sea). [Benefit 1] His country rewards him for winning battles against other factions. [Benefit 2] Victories grant twice the usual [[184|Influence]].',
   'Poor navy can mean weak ships andconflicts withgood starting ships;underfunded preserves the actual budget problem. Restore Joakim,the North Sea,the military reason forgood ships,andvictory versusother factions as the reward condition. Restore link184;do not invent rewardamounts orroyal sponsors.'),
10:('Game Over',
    "The game ends if any of these happens: your faction's [[150|Market Share]] drops to zero in every town; every ship in your fleet is sunk or captured in battle; or every ship in your fleet has no sailors left.",
    'Retain three alternative losses. Restore the own-fleet scope andin-battle condition;everytown avoids excluding ports byusing the narrower City class. Restore link150. Do not turn allships intooneship orallofficers.'),
12:('Tavern',
    'Recruit sailors and gather information. [!] Many towns in Arab cultural regions have no tavern for religious reasons, making it harder to recruit sailors. Be careful about starting battles there. See [[13|Order Drink]], [[14|Treat Everyone]], [[15|Recruit Sailors]] and [[16|Plot]].',
    'Restore the source religious context respectfully andthe many-towns qualifier. Keep recruitment difficulty andthe battle warning causally connected. Restore all four original links;avoid sweeping claims aboutpeople orreligion.'),
13:('Order Drink (Tavern)',
    'A drink costs 5 to 10 gold coins. You may hear news about nearby towns or other factions. [!] Talk with the well-informed women at taverns in [[145|Cities]]. They may even know where to find an item.',
    'Retain the correct costrange andinformation possibilities. Hosts invents an occupational role andobscures the clean female conversation partners;use women withoutadding ownership,age,romance orfamily ties. Restore City-class link145.'),
14:('Treat Everyone (Tavern)',
    'Buy drinks for everyone in the tavern. You can hear news about nearby towns and other factions, and you may learn about items. Doing this before you [[15|Recruit Sailors]] makes it easier to attract a crew.',
    'Retain the natural buy-drinks instruction andthe recruitment preparation benefit. Preserve may foritem information andrestore link15;do not promise a fullcrew ormake buying drinks mandatory.'),
15:('Recruit Sailors (Tavern)',
    "Recruit sailors for your ships. Towns with higher Growth offer more sailors at once, but hiring them costs more gold. Excess recruits are dismissed on the spot. Treating everyone to drinks beforehand helps. Then use [[139|Assign Sailors]] to distribute them among your fleet's ships.",
    'Expand the overcompressed wording only torestore precise source scope:town Growth,one recruitment group,immediate excessdismissal andsubsequent per-ship assignment. Preserve the useful existing drinks preparation instruction andrestore link139.'),
16:('Plot (Tavern)',
    'Plan a scheme against another faction. You can do this only when your [[118|Strategist]] has an idea. It costs 1,000 gold coins, and the plan may fail. You cannot use it in a sea region with no other factions. Except for Bogus Documents, you must have visited a town where another faction has [[150|Market Share]]. See [[17|Lure Fleets]], [[18|Bogus Documents]], [[19|Bad Rumors]] and [[20|Bribery]].',
    'Keep all eligibility rules andthe exactfee/failure possibility. Restore the regional scope andall six original links. Use the existing Help18 Bogus Documents heading rather than inconsistent forged Orders,anddo not narrow generic source documents toorders.'),
18:('Bogus Documents',
    'Forge documents to turn two other factions against each other. You can use this scheme only if there are at least two other factions. Select the two factions you want to make hostile to one another.',
    'Restore the explicit multiple-other-factions condition andbroad forgeddocuments meaning. Hostility doesnot byitself establish a formal declaration ofwar. Preserve the two selected targets.'),
19:('Bad Rumors',
    "Spread bad rumors about another faction in a town you choose within the current sea region. This reduces that faction's market share there. Your strategist will not think of this scheme if their ability is too low.",
    'Restore choosing a town withintheregion. Clean lowability prevents theidea;maynot incorrectly makes that a mere possibility. Do not claimthat ability changes the shareloss amount.'),
20:('Bribery',
    'Bribe a broker in a town where another faction operates to take some of its market share. Choose one town in the current sea region. Your strategist will not think of this scheme if their ability is too low.',
    'Retain broker andthe existing partial-share sense without inventing a governor orofficial. Restore the rival-town context andthe definite lowability eligibility limit;keep the regional destination restriction.'),
}

def logical_article(text):
    lines=text.splitlines();return lines[0].strip(),' '.join(' '.join(lines[1:]).split())

def visible_words(text):
    plain=re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]',r'\1',text)
    return re.findall(r"[A-Za-z0-9']+",plain)

if __name__=='__main__':
    output=Path('translations/help_T00_T20_contextual_manuscript_v1.json');assert not output.exists()
    draft_path=ROOT/'T00_T20_clean_meanings_andindependent_drafts_v1.json'
    current_path=ROOT/'current_T00_T20_verified_parent_v1.json';terms_path=ROOT/'native_UI_terms_andRafael_continuation_v1.json'
    draft,current,terms=map(load,[draft_path,current_path,terms_path]);originals={r['id']:r for r in draft['records']}
    assert set(RETAIN)|set(REVISE)==set(range(21)) and not set(RETAIN)&set(REVISE)
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file(current['file_path'])
    canonical_blocks=IlnkContainer.parse(canonical).blocks;rows=[]
    for record in current['records']:
        index=record['topic_id'];source=originals[record['id']]
        heading,existing=logical_article(record['current_English_with_link_IDs']);old_logical=existing
        continuation=None
        if index==7:
            continuation=terms['Rafael_article_continuation'];_,tail=logical_article(continuation['current_text'])
            existing=re.sub(r'\[\[202\|[^\]]+\]\]','',existing).strip()
            tail=re.sub(r'\[\[7\|[^\]]+\]\]','',tail).strip()
            existing=(existing+' '+tail).replace('[[184| Influence.]]','[[184|Influence]].')
        if index in RETAIN:
            english=existing;finding=RETAIN[index];decision='retention'
            if index==11:
                english="Select a building's sign to use its commands. Commands marked 'City only' are available only in a [[145|City]]. See [[12|Tavern]], [[21|Market]], [[26|Guild]], [[34|Inn]], [[35|Palace or Governor's Office]], [[42|Square]], [[44|Shipyard]], [[73|Port]], [[144|City Info]] and [[103|Shared Commands]]. [!] You may also be able to visit local [[80|ruins]]."
            assert visible_words(existing)==visible_words(english),(index,'retention changedwords')
        else:heading,english,finding=REVISE[index];decision='revision'
        links=[int(m[1]) for m in re.finditer(r'\[\[([0-9]+)\|[^\]]+\]\]',english)]
        assert links==source['original_link_IDs'],(index,links,source['original_link_IDs'])
        assert english.isascii() and heading.isascii() and '\n' not in english and '  ' not in english
        metric_pending=index in [7,8,9]
        row=dict(id=record['id'],topic_id=index,file_path=current['file_path'],speaker='In-game Help',heading=heading,english=english,
            context='Complete original Help article withits linked source definitions;T07 includes existing physical continuation202. Original menu destinations andcondition/benefit progression are reviewed together.',
            source_meaning=source['faithful_source_meaning'],localization_note=finding,
            source_reference=source['source_reference'],source_hex=source['source_hex'],clean_source_hex=source['source_hex'],
            canonical_source_hex=canonical_blocks[index].hex(),current_reference=record['current_reference'],current_hex=record['current_hex'],current_source_hex=record['current_hex'],
            current_English=old_logical,source_Japanese_with_link_IDs=source['source_Japanese_with_link_IDs'],
            original_links=source['original_links'],original_link_IDs=source['original_link_IDs'],current_link_IDs=record['current_link_IDs'],
            decision=decision,finding=finding,retention_reason=finding if decision=='retention' else None,
            retained_working_phrases_documented_in_finding=True,review=dict(source=True,context=True,localization=not metric_pending,naturalness=True,formatting=False),
            independent_draft_reference=dict(path=str(draft_path),sha256=sha(draft_path.read_bytes()),id=record['id']),
            current_reference_packet=dict(path=str(current_path),sha256=sha(current_path.read_bytes()),id=record['id']),
            source_first_complete_topic_review=True,no_authored_wraps_oralignment=True,
            fresh_native_font_links_rows_bounds_allocation_pagination_andvisual_checks_pending=True,
            metric_UI_Influence_versus_COMMON_Power_binding_pending=metric_pending,
            actual_gameplay=False,new_credit=0)
        if continuation:
            row['current_continuation']=continuation
            row['existing_202_forward_and7_back_navigation_must_be_preserved']=True
            row['second_bonus_is_present_in_existing_continuation_not_an_omission']=True
        rows.append(row)
    revised=sum(r['decision']=='revision' for r in rows);retained=sum(r['decision']=='retention' for r in rows)
    assert (revised,retained)==(13,8)
    save(output,dict(format='dk4-structured-help-contextual-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        not_a_release_batch=True,formatting_owned_by_compiler=True,file_path=current['file_path'],records=rows,
        source_clean_HELP_sha256=draft['source_archive_sha256'],source_canonical_HELP_sha256=sha(canonical),source_current_HELP_sha256=current['current_archive_sha256'],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        source_topic_count=202,current_topic_count=211,proposed_revisions=revised,justified_retentions=retained,
        all21_source_context_naturalness_reviews_passed=True,first_four_gates_passed=18,three_metric_label_bindings_pending=True,
        original_link_IDs_all_preserved_in_proposals=True,existing_nine_added_topics_andunselected_prose_preserved_required=True,
        COMMON_term_evidence_scope='Existing message terminology,not a new menu-label orrenderer execution proof.',
        deferred_current_202_pagination_repack_must_keep_complete_bonus_andbidirectional_navigation=True,
        no_native_rendering_orROM_oradditional_completion_claim=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [draft_path,current_path,terms_path,Path(__file__)]}))
    print('21 contextual Help reviews:13 proposed revisions/8 justified retentions;18 four-gate prose passes/three metric-label bindings pending. All formatting remains pending;zero credit.')
