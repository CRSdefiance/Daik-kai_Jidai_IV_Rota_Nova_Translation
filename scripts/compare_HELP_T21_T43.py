"""Review the next23 complete town-help articles;retain five complete working wordings."""
import re
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Shared_HELP_T21_T43_clean_20261104')
RETAIN={
21:"The market lets you buy and sell trade goods and gather information. If you bring a [[194|Source Item]] to a city's market, you may be asked to hand it over. Doing so adds to that city's [[152|specialties]]. See [[22|Trade]], [[23|Commercial Investment]] and [[24|Market Prices]].",
23:"Invest to develop a city's commerce. You can invest 1 to 20 units at a time. Each unit costs gold equal to half the city's Growth. Investment raises Growth. Your market share also increases if the city's total [[150|market share]] is below 100 percent or a faction you are [[187|at war with]] holds a share there. Higher Growth may add new [[152|specialties]].",
37:"Invest in a city's defenses, from 1 to 20 units at a time. Each unit costs gold equal to 50 percent of the city's Arms rating, or 40 percent for Rafael. Investment raises the city's Arms rating. Your market share also rises if the city's total [[150|market share]] is below 100 percent or a faction you are [[187|at war]] with owns a share. A higher Arms rating makes the city less likely to surrender when attacked and allows you to buy better ships and cannons.",
40:"Lend an item to the ruler of your home city. Earn monthly rent based on value. [[4|Proofs of Conquest]], Proof Maps, and [[142|Ancient Maps]] cannot be lent.",
43:"Give goods to residents for free. Requires a [[117|missionary]]. Those goods may become [[25|fashionable]] in nearby cities.",
}
NOTES={
21:'Retain the natural market introduction,conditional Source Item request anddefinite specialty increase afterthe gift. All five original links already exist. The current generic city wording isclear inthis market-command context anddoesnot restrict trading toCity-class settlements. Repair premature wraps/link boundaries without rewriting good prose.',
22:'Restore profit margin ratherthan ambiguous absolute profit,andthe stock/restocking explanation. Use Purser from119,not the draft accountant. Restore all five original links;preserve Lil5 percent andconditional bargaining/buyout.',
23:'Retain the full clear investment explanation:1-20 units,half Growth,certain Growth increase,both alternative market-share conditions andpossible specialties. No factual correction needed. Reflow logical paragraphs andpreserve all three original links.',
24:'Replace the awkward other cities cost coins toinspect withthe cost ofinformation. Specify red purchase prices,not every red price. Restore the original Trends25 link and50-200 range.',
25:'Repair the broken in monopoly cities sentence andvague Letter. Preserve general price increases,both trend causes andall conditional benefits. Name Introduction andRecommendation distinctly;restore all five original links. Do not invent guaranteed contracts ormutually exclusive rewards.',
26:'Restore selling items,which current Buy items omits. Preserve send letters/report routes/Ancient Maps andrestore all three original links. Keep City-only qualification inthe heading.',
27:'Replace Send diplomacy witha natural letter instruction. Use the accepted First Mate role represented by121 First Mate office,not an invented deputy rank. Keep same-region/1000-cost/failure/no-rivals limits andrestore all seven original links.',
28:'The Japanese increases the numeric Friendship rating,not generic Relations. Retain the simple friendly-letter intent andslight increase.',
29:'Distinguish the large numeric Friendship increase fromthe Allied relationship status. Preserve possible battle help andrestore original Allied186 link;no guaranteed assistance.',
30:'Specify Friendship falls afterbreaking the agreement. Current Relations isambiguous beside the separate relationship-state field. Preserve the concise action.',
31:'Describe an accepted truce,not a promise tointerrupt combat. Keep the explicit discard-if-arriving-during-battle exception andrestore the source At War187 link.',
32:'Distinguish Friendship fromAt War status;use the established Power metric consistently. Preserve red enemy Power andinvestment/battle ways totake share;restore187.',
33:'Correct the exact-200 ambiguity toatleast200,including scores above200. Use First Mate consistently with121;keep regional Proof prerequisite andrestore4. Do not promise coercion succeeds.',
34:'Retain one gold pernight,about10 Fatigue reduction,officer condition/HP recovery andpossible strategist information. Restore157/118 andtitle capitalization. Exact source cross cancel control remains unbound;do not approve its English as a physicalX button yet.',
35:'Restore all six command links andnatural complete Letter ofIntroduction/Recommendation distinctions. Keep contracts andmilitary investment;do not abbreviate good prose tofit a manual row.',
36:'Clarify that the three factions already have contracts,ratherthan merely being present. Preserve1-20 units,corresponding share/trading rights andthe separate combined100 percent rival-share block. Restore150.',
37:'Retain every word ofthe complete37+204+205 article. It already includes both share conditions,surrender resistance andbetter ships/cannons,aswell as1-20 units/50 percent Arms/Rafael40 percent. No omitted-benefit claim. Revisit the three-page wrapping without shortening;continuations arenot extra source credit.',
38:'Specify Letter ofIntroduction,Port-class restriction andexisting-contract versus new-contract outcomes. Preserve5 percent/1 percent andboth prohibitions. Contracts withthree factions,not vague factions present;restore25/36/150.',
39:'Specify Letter ofRecommendation andany town size. Preserve10 percent/1 percent andboth prohibitions. Distinguish actual contracts frommere presence;restore25/36/150.',
40:'Retain the concise home-base ruler loan,monthly rent byvalue andall three excluded item categories. The Palace command context scopes the lending location. Restore original4/142 links andtitle case;do not add terms ornew restrictions.',
41:'Preserve retrieval ofan already lent item andexplicitly cover the home-base governor office aswell asthe palace. Current palace-only wording obscures the source alternative.',
42:'Restore retail shops,which explains the square versus bulk market distinction. The source means selecting a shop sign within trend information,not a shop named Trends. Preserve25/43;exact current command label remains tobind.',
43:'Retain the complete concise giveaway explanation:free goods,required missionary andonly a possible trend innearby towns. Goods isclear fromthe Square trade-goods command context. Restore117/25 links;no extra reward orsuccessful trend invented.',
}

def words(text):
    return ' '.join(re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]',r'\1',text).split())

if __name__=='__main__':
    output=ROOT/'whole_article_comparisons_v1.json';assert not output.exists()
    draft_path=ROOT/'clean_meanings_andfull_drafts_v2.json';current_path=ROOT/'current_full_articles_verified_parent_v1.json'
    cont_path=ROOT/'Military37_complete_current_continuations_v1.json'
    draft,current,continuations=map(load,[draft_path,current_path,cont_path]);current_rows={r['topic_id']:r for r in current['records']};records=[]
    for source in draft['records']:
        t=source['topic_id'];old=current_rows[t];english=RETAIN.get(t,source['full_article_English_draft'])
        if t==22:english=english.replace('[[119|accountant]]','[[119|Purser]]')
        if t==27:
            english=english.replace('[[121|deputy]]','[[121|First Mate]]').replace('[[27|Send Negotiation Letter]]','[[27|Send Letter]]')
            for a,b in [('[[29|Make Alliance]]','[[29|Alliance]]'),('[[30|Break Alliance]]','[[30|Break Pact]]'),('[[31|Ceasefire]]','[[31|Truce]]'),('[[33|Intimidate]]','[[33|Coerce]]')]:english=english.replace(a,b)
        if t==33:english=english.replace('your deputy has','your First Mate has')
        body=old['current_English_with_link_IDs'].split('\n',1)[1]
        if t==37:
            chunks=[]
            for r in continuations['records']:
                lines=r['current_English_with_link_IDs'].split('\n');text=' '.join(lines[2:] if r['topic_id']==37 else lines[1:])
                chunks.append(re.sub(r'\[\[(?:37|204|205)\|[^\]]+\]\]','',text))
            body=' '.join(chunks)
        if t in RETAIN:assert words(body)==words(english),(t,words(body),words(english))
        records.append(dict(id=source['id'],topic_id=t,file_path=current['file_path'],
            source_reference=source['source_reference'],source_hex=source['source_hex'],source_meaning=source['clean_meaning'],
            source_Japanese_with_link_IDs=source['source_Japanese_with_link_IDs'],current_reference=old['current_reference'],current_hex=old['current_hex'],
            current_English=old['current_English_with_link_IDs'],original_link_IDs=source['original_link_IDs'],
            complete_current_continuations=continuations['records'] if t==37 else [],
            english=english,decision='retention' if t in RETAIN else 'revision',finding=NOTES[t],
            retention_reason=NOTES[t] if t in RETAIN else None,
            context='Read asone complete help article within the connected Market/Guild/Inn/Palace/Square command group;source/current neighbors andoriginal link destinations arebound.',
            review=dict(source=True,context=True,localization=t not in [34,42],naturalness=True,formatting=False),
            native_term_orcontrol_binding_pending=t in [34,42],fresh_display_allocation_widgets_andintegration_pending=True,new_credit=0))
    assert len(records)==23 and sum(r['decision']=='retention' for r in records)==5
    save(output,dict(records=records,records_count=23,proposed_revisions=18,justified_retentions=5,first_four_gates_passed=21,
        pending_localization_binding_topic_IDs=[34,42],all_fifth_gates_pending=True,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        all_five_retentions_word_exact_after_removing_old_wraps_andrestoring_link_markup=True,
        existing37_204_205_complete_article_bound_not_a_missing_text_finding=True,
        prior21_23_English_exposure_disclosed=True,new_credit=0,registered_integration_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [draft_path,current_path,cont_path,Path(__file__)]}))
    print('Next23 whole-article comparisons:18 proposed revisions/5 word-exact justified retentions;21 four-gate passes. Inn cross/Square label andall display gates remain.')
