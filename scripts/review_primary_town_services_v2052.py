"""Fresh whole-exchange source/prose review of84 primary town-service entries."""
from collections import Counter
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/town_services_editorial_v2052')
SOURCE=Path('work/analysis/town_services_source_v2051/all84_clean_current_primary_town_service_exchanges.json')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v1.json')
# ID|faithful source gloss first|logical English (=retains current visible words)|individual reason
TEXT=r"""
0|A polite companion tells the admiral that people appear to be gathering in the square.|Admiral, people seem to be gathering in the square.|Restore the uncertainty and ongoing gathering; People gather was a flat fragment that lost the advisory tone.
1|A hesitant polite companion notes that people seem to be gathering in the square.|Admiral, it looks like a crowd is gathering in the square...|Preserve the source's hesitant unfinished observation rather than declaring a crowd simply present.
2|A casual companion draws the admiral's attention to an apparent gathering in the square.|Hey, Admiral, looks like people are gathering in the square.|The casual Hey and looks like keep the bright advisory voice and the source's uncertainty.
3|A casual companion tells the admiral that people seem to be gathering in the square.|Hey, Admiral, it looks like people are gathering in the square.|Restore Hey and the ongoing gathering without adding a purpose for the crowd.
4|A brash companion points out an apparent crowd gathering in the square.|Admiral, looks like a crowd's gathering in the square.|The contraction fits the source's casual emphatic ending; they're at the Square omitted both the crowd and the tentative observation.
5|An older reflective voice says people seem to be gathering in the square.|Admiral, people seem to be gathering in the square.|The measured phrasing preserves the older voice without forcing an archaic English dialect or inventing an event.
6|Another casual advisory voice draws the admiral's attention to an apparent gathering in the square.|Hey, Admiral, looks like people are gathering in the square.|This Japanese wording matches variant2; the same natural English retains that deliberate equivalence instead of inventing a distinction.
7|A mature formal companion says people appear to be gathering in the square.|Admiral, people appear to be gathering in the square.|Appear preserves the source's measured formality and uncertainty; no reason for the crowd is invented.
8|A trader asks what the visitor needs.|=|Need help is a natural casual shop greeting; it matches the actual Trader entry and invites the service menu without adding a sales promise.
9|The trader thanks the customer and invites continued patronage.|=|Thanks! Come again naturally expresses both gratitude and the invitation to return for future business.
10|The trader reluctantly agrees to offer a small discount.|=|Okay. A little discount for you is natural spoken shop dialogue; Okay carries the concession and little preserves the scale.
11|A polite transaction voice asks whether the proposed terms are acceptable.|Will this be all right?|Restore the polite confirmation register and preserve the question without assuming whether the player is buying or selling.
12|A casual transaction voice asks whether the proposed terms are acceptable.|=|This okay is an idiomatic relaxed confirmation and stays distinct from the more formal variants.
13|Another polite transaction voice asks whether the proposed terms are acceptable.|=|Is this okay is natural and neutral enough for the polite source; no extra condition is implied.
14|A blunt transaction voice seeks confirmation of the proposed terms.|=|Good with this keeps the direct casual tone and the confirmation function.
15|An older or reflective transaction voice asks whether the proposed terms will do.|=|Will this do is a natural restrained confirmation and preserves the source's measured register.
16|A playful elongated transaction voice asks whether the proposed terms are acceptable.|=|This good is a natural breezy spoken question and keeps the short playful delivery without an invented pet name.
17|A mature polite transaction voice asks whether the proposed terms are acceptable.|=|Does this look all right preserves a courteous,considered confirmation rather than a brusque demand.
18|The trader charges a fee each time market prices are viewed and asks which town's prices the customer wants.|There's a fee each time you check prices. Which town's prices would you like to see?|Restore the market-price subject and per-view condition; a generic report did not fully explain what the player is purchasing.
19|A polite bargaining voice asks for a slightly better price.|=|Could you improve the price is a natural courteous request and leaves the direction of the price adjustment to the actual transaction.
20|A direct bargaining voice asks whether the price can be improved.|=|Can you improve the price is concise,direct and faithful without adding a discount amount.
21|A casual hesitant bargaining voice asks the other party to think again about the price.|Think you could do a little better on the price?|This is idiomatic American bargaining and preserves the friendly tentative approach rather than a stiff request to reconsider.
22|Another casual bargaining voice asks for reconsideration of the price.|Couldn't you give me a better price?|The spoken question keeps the request gentle but direct. It avoids the unnaturally formal Please reconsider the price.
23|A blunt bargaining voice asks the other party to improve the price a little.|=|Can you do better than that is idiomatic and preserves the brash challenge without specifying an unsupported adjustment.
24|An older bargaining voice apologetically asks for a somewhat better price.|Sorry to ask, but could you give me a slightly better price?|Preserve the apology and measured politeness. Better price avoids narrowing the source's generic amount request to lowering a purchase price.
25|A very casual bargaining voice urges the other party to offer a small favor or discount.|Come on, give me a little break on the price!|Keep the energetic demand and small concession in natural spoken English,without inventing a relationship or a discount percentage.
26|A mature polite bargaining voice asks the other party to reconsider the amount.|Could you perhaps offer a better price?|Perhaps keeps the measured politeness,and better price sounds more natural than rethink the price in this exchange.
27|A departure warning says one ship has no sailors at all and tells the player to hire sailors or reorganize before returning.|One of your ships has no sailors. Hire some or reorganize your fleet, then come back.|Restore the zero-crew condition and the return-after-remedy instruction. Reorganize the fleet preserves the wider formation option rather than inventing one specific crew assignment.
28|A departure warning says one ship is short of sailors and recommends reviewing the fleet's formation before sailing.|One of your ships is short of sailors. Better check your fleet's formation before sailing.|Keep the recommendation distinct from the zero-crew refusal; do not turn advice into an absolute ban on departure.
29|A polite companion reports that some ships need repairs before setting sail.|Admiral, we have ships that need repairs before we set sail.|Restore the actual problem and its timing; repair before sailing had lost the report that ships need work.
30|A hesitant polite companion notes that some of the fleet's ships seem to need repairs.|=|The existing it looks like and some of our ships naturally preserve both the uncertainty and the fleet context.
31|A casual companion asks the party to wait because some ships need repairs before sailing.|=|Hold on gives the interruption its force,and the remaining sentence clearly preserves the repair-before-departure condition.
32|A brash companion urges repairs before sailing and warns that leaving the ships as they are is dangerous.|=|Let's repair and It's too risky like this preserve both the practical action and the urgent warning in natural conversation.
33|An older companion says ship repairs must take priority over departure.|=|Repairs must come before we set sail is idiomatic and retains the source's firm priority without adding a new restriction.
34|A childish companion fears drowning and asks that the ships be repaired first.|=|I don't want to drown and Let's get the ships fixed first retain the comic personal fear and the requested remedy without inventing kinship.
35|A mature polite companion says repairs should precede departure.|=|We should repair the ships before departing is natural formal advice and remains distinct from the brash and childish variants.
36|A polite hesitant companion warns that these supplies look likely to run out very soon.|Admiral, it looks like we'll run out of supplies very soon...|Restore the tentative warning and its reference to the current supplies while retaining the unfinished concerned tone.
37|A casual companion warns that supplies will soon run out at the present rate.|=|At this rate and in no time preserve the cause and urgency in an idiomatic casual voice.
38|A direct companion observes that supplies will soon be exhausted.|=|We'll soon run out of supplies, Admiral is natural and faithful; moving the address to the end does not change the intent.
39|A firm mature companion warns the admiral that the stored supplies will soon be exhausted.|Admiral, these supplies will run out in no time.|Replace the unrelated raw crowd text with the actual supply warning. Active-consumer and native display binding remain separate pending gates.
40|A casual food-focused companion worries that they will soon have nothing to eat with the current supplies.|Hey, won't we run out of food soon with so little aboard?|Restore the food-specific worried question rather than the unrelated raw crowd text. Do not substitute a generic gathering alert.
41|A mature expressive companion says that with so few supplies they will be exhausted very soon.|=|Goodness and With so few supplies naturally preserve the exasperation,small stock and imminent exhaustion.
42|A polite companion expresses mild unease about whether the current supplies are sufficient.|=|I'm not sure these supplies will be enough preserves the source's cautious concern without escalating it into an imminent-empty warning.
43|A casual companion asks whether the supplies are a little short.|=|Aren't we just a bit short on supplies is idiomatic and preserves the mild rhetorical concern.
44|A hesitant polite companion is a little worried about the small quantity of supplies.|=|I'm a little worried about having so few supplies captures both the personal concern and its restrained strength.
45|Another casual companion asks whether the supplies are a little short.|=|Aren't we a little short on supplies retains the conversational question and mild degree without adding an emergency.
46|An older direct companion asks whether they are taking too few supplies.|=|Aren't we taking too few supplies is a natural measured challenge and remains distinct from the imminently-empty variants.
47|A childish companion asks whether there will be enough food for them and notes that supplies seem low.|=|The two existing questions preserve the child's personal appetite and broader concern. No family term or extra threat is added.
48|A mature polite companion reflects that the quantity of supplies seems low.|=|Hmm and We seem to be short on supplies naturally retain the thoughtful,measured observation without an invented deadline.
49|The port attendant asks whether the player wants to resupply for the stated amount of gold currency.|Want to resupply for %s gold?|Make the cost and action one natural question. Gold is the game's currency unit and avoids a one-coins agreement problem for a variable amount; the numeric substitution remains exact.
50|A formal host welcomes the visitor and invites them farther inside.|=|Welcome. Please, come inside preserves both the courteous greeting and invitation without inventing a facility title.
51|A casual barkeep welcomes the visitor and asks what they would like.|=|Welcome! What will you have is a natural American bar greeting,and the actual Hangzhou scene shows this service-menu introduction.
52|A polite seller quotes a fixed price of ten gold coins.|=|That'll be 10 coins is idiomatic service dialogue and keeps the exact fixed amount; the game's currency context makes the unit clear.
53|A casual seller quotes a fixed price of five gold coins.|=|5 coins is a natural terse spoken quote and preserves the exact amount shown in the actual drink-order exchange.
54|The barkeep directly addresses the named serving attendant and asks that attendant to pour for the guest.|%s, pour our guest a drink.|Restore the argument's role as the person being called. Please serve %s incorrectly made that named attendant the recipient of service.
55|The barkeep calls the named attendant and announces a customer.|Hey, %s! We've got a customer!|Keep the casual Hey while restoring the reason for the call. The actual Hangzhou sequence calls Miwa and receives her reply.
56|The serving attendant cheerfully acknowledges the call.|=|On it is an idiomatic energetic acknowledgment and fits the actual reply that follows the barkeep's call.
57|The serving attendant gives a warm welcome.|=|Welcome naturally conveys the greeting; an extra English interjection is unnecessary to preserve its warmth.
58|The serving attendant reacts with pleased recognition and welcomes the named visitor.|Oh, %s! Welcome!|Restore the delighted recognition before the welcome while keeping the exact named-visitor argument and adding no relationship.
59|An unattributed yes/no prompt proposes another drink in a courteous offer.|=|Here, have another drink is a natural offer. The actual screen has no speaker nameplate and has Yes/No controls,so no named speaker or demand is invented here.
60|A polite barkeep quotes a fixed charge of twenty gold coins.|=|That'll be 20 coins preserves the polite service register and exact fixed amount.
61|A casual barkeep quotes a fixed charge of ten gold coins.|=|Ten coins is natural spoken billing and preserves the exact amount at the end of the captured drink interaction.
62|A casual facility attendant greets the visitor and asks their business.|=|Need something is an idiomatic casual opening and does not invent a particular service or affiliation.
63|A polite facility attendant welcomes the visitor.|=|Welcome! Come in conveys the source's friendly courteous greeting without adding a new instruction beyond the conventional invitation.
65|A neutral polite docking confirmation asks whether to call at the named town.|=|Dock at %s is a clear natural confirmation and preserves the town argument unchanged.
66|A casual docking confirmation asks whether to call at the named town.|=|The same concise Dock at %s works for this casual variant; no extra formality or new intent is added.
67|A friendly direct docking confirmation asks whether to call at the named town.|Shall we dock at %s?|The inclusive question preserves the friendly confirmation and makes the crew's proposed action explicit without inventing a rank.
68|An older reflective docking confirmation asks whether to call at the named town.|Shall we put in at %s?|Put in is natural nautical English and gives the older measured voice a distinct phrasing without changing the action.
69|A casual docking confirmation asks whether to stop at the named town's port.|Want to stop at %s's port?|Restore the source's port-stop wording in a casual question,retaining the exact town argument.
70|A mature formal docking confirmation asks whether to call at the named town.|=|Shall we call at %s is idiomatic nautical phrasing and preserves the formal source voice.
71|A polite crew-assignment confirmation asks whether it is acceptable to leave the stated number of sailors unassigned.|Is it all right to leave %s of our sailors unassigned?|Preserve the count and confirmation while making the grammar valid for both one and many; no sailor is dismissed or reassigned by this text.
72|A friendly crew-assignment confirmation reports the remaining unassigned count and asks whether that is acceptable.|We've left %s of our sailors unassigned. Is that okay?|The quantifier of our sailors works for one and many,and the contraction keeps the friendly voice without adding a consequence.
73|An older crew-assignment confirmation asks whether to proceed with the stated count unassigned.|Shall we proceed with %s of our sailors still unassigned?|Preserve the older measured request for approval and avoid the one-sailors agreement error in the current template.
74|A casual crew-assignment confirmation asks whether it is acceptable that the stated count remain unassigned.|Is it okay to leave %s of our sailors unassigned?|The casual okay and number-neutral quantifier preserve the question without implying that the sailors are unwanted or must be dismissed.
75|A mature formal crew-assignment confirmation seeks approval to leave the stated count unassigned.|Do you approve of leaving %s of our sailors unassigned?|This preserves the formal approval request and works for one or many without inventing a commander's title.
76|A tribute presenter announces the month's amount and politely offers it for acceptance.|This month's tribute is %s gold. Please accept it.|Keep the existing incoming-payment interpretation and polite offer; use the currency unit gold so a variable amount of one remains grammatical. Native payment-direction binding is still required before release.
77|A hesitant tribute presenter announces the month's amount and politely offers it with a trailing pause.|This month's tribute is %s gold. Please accept it...|Retain the hesitant ellipsis and polite offer,with the exact numeric amount and number-neutral currency unit. Native presenter/currency binding remains a release gate.
78|A tribute presenter states the amount for this month.|The tribute for this month is %s gold.|The existing neutral declaration works; changing only the currency noun avoids singular/plural disagreement while preserving the exact amount.
79|A friendly tribute presenter states the month's amount.|This month's tribute comes to %s gold.|Comes to is natural friendly reporting. Keep the amount unchanged and use a currency unit that does not depend on the number.
80|A casual tribute presenter states the month's amount.|Here's this month's tribute: %s gold.|The contraction and direct presentation retain the source's casual emphatic voice; the currency quantity stays exact.
81|An older emphatic tribute presenter announces the amount and urges the recipient to accept it.|This month's tribute is %s gold. Go on, please accept it.|Retain the older speaker's urging and polite offer,not a demand that the player pay. Exact native payment-direction confirmation remains pending.
82|A courteous tribute presenter asks the recipient to accept the month's stated amount.|Please accept this month's tribute of %s gold.|The existing polite offer remains natural; the number-neutral currency unit preserves the same amount for one or many.
83|Towns where the named power holds exclusive contracts have sent the stated gold amount in tribute.|Towns under %s's exclusive contracts paid %s gold in tribute.|Retain the current clear payer,exclusive-contract condition and argument order. Change only the variable currency noun for number-neutral grammar; no new tax rate is introduced.
84|The player receives the stated gold amount as fees for lending items.|Received %s gold in item rental fees.|Restore the item-lending source of the income,which the generic Rental income left implicit. Preserve the exact amount without a one-coins grammar error.
"""

def speaker(n):
    if n<8 or 29<=n<=48:return 'Companion advisory source voice '+str(n)
    if n in(8,9,10,18):return 'Trader'
    if 11<=n<=17:return 'Transaction confirmation source voice '+str(n-11)
    if 19<=n<=26:return 'Bargaining source voice '+str(n-19)
    if n in(27,28,49):return 'Port service attendant'
    if n in(50,51,52,53,54,55,60,61):return 'Facility host or barkeep,source service role'
    if n in(56,57,58):return 'Serving attendant,source drink exchange'
    if n==59:return 'Unattributed drink-offer confirmation'
    if n in(62,63):return 'Facility attendant'
    if 65<=n<=70:return 'Docking confirmation source voice '+str(n-65)
    if 71<=n<=75:return 'Crew-assignment confirmation source voice '+str(n-71)
    if 76<=n<=82:return 'Monthly tribute presenter,precise native role pending'
    return 'Income notification'

if __name__=='__main__':
    assert not ROOT.exists()and not DOC.exists()
    source=read(SOURCE);plans=[line.split('|')for line in TEXT.strip().splitlines()];assert len(plans)==len(source['records'])==84
    assert [int(p[0])for p in plans]==[r['message_id']for r in source['records']]
    rows=[]
    for original,(number,gloss,proposed,note)in zip(source['records'],plans,strict=True):
        n=int(number);current=re.sub(r'\s+',' ',original['current_stored_English']).strip().translate(str.maketrans({'Ｉ':'I','Ｆ':'F'}))
        target=current if proposed=='='else proposed;assert target==target.strip()and '\n'not in target and '{'not in target
        assert target.count('%s')==original['source_Japanese'].count('%s')and '%'not in target.replace('%s','')
        decision='retain-wording'if proposed=='='else'revise';family=next(g for g in source['families']if n in g['IDs'])
        rows.append(dict(**{k:original[k]for k in('id','message_id','file_path','source_reference','current_reference','source_hex','current_hex','source_Japanese','current_stored_English')},
            source_meaning=gloss,speaker=speaker(n),english=target+'{PAD}',editorial_decision=decision,localization_note=note,
            **({'fresh_retained_wording_justification':note}if decision=='retain-wording'else{'finding':note}),
            context='Complete functional exchange: '+family['name']+'. Voice tables are alternative branches,not consecutive speakers. Trader requests andconcessions precede price confirmation;Port crew/repair/supply warnings precede departure/resupply choice;formal/casual tavern greeting-cost-attendant call/reply precedes drink-offer confirmation andbilling;docking/assignment prompts preserve yes/no decisions;tribute andrent announcements preserve incoming payment andsubstitution roles. Separate ritual64 isexcluded forits ownfull conversation review. Anonymous source roles arekept where acharacter identity isnot yet proven.',
            family=family['name'],full_exchange_native_IDs=family['IDs'],source_format_arguments=['%s']*target.count('%s'),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_consumer_actor_argument_currency_and_display_binding_pending=True))
    ROOT.mkdir(parents=True);(ROOT/'source_packet.json').write_bytes(SOURCE.read_bytes())
    save(DOC,dict(format='dk4-ilnk-translation-batch-v1',file_path='/COMMON/MESFILE.DK4',source_file_sha256=source['current_COMMON_sha256'],
        editorial_clean_source_file_sha256=source['clean_COMMON_sha256'],source_ROM=source['clean_ROM'],source_ROM_sha256=source['clean_ROM_sha256'],
        current_ROM=source['candidate'],current_ROM_sha256=source['candidate_sha256'],required_runtime_ARM9_sha256=source['ARM9_sha256'],
        encoder='dialogue-fixed-v1',dialogue_profile='shared',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        format_review_pending=True,draft_only_not_registered_or_formatting_approved=True,
        retained_visible_wording_normalizes_legacy_layout_and_fullwidth_reserved_Latin_only=True,
        native_parameters_remain_printf_slots_not_story_FI_FA_FO_macros=True,
        next_gates=['Bind active native COMMON callers,argument roles andpayment direction.','Native literal handling,complete glyph/wrapping/bounds/pagination proofs forall84 andtyped substitutions.',
            'Exact full-cache reblocking/copy preservation andunowned opaque resource bounds.','Representative revised town/dialogue transitions.','Registered cumulative build andexact clean-input patch.'],full_goal_complete=False))
    decisions=Counter(r['editorial_decision']for r in rows)
    save(ROOT/'source_prose_review_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=84,decisions=dict(decisions),
        complete_functional_exchanges_and_all_source_voice_alternatives_reviewed=True,
        each_row_has_gloss_context_and_revision_or_retention_reason=True,all_formatting_gates_false=True,
        anonymous_native_role_and_tribute_direction_binding_remain_release_gates=True,
        ROM_registry_or_ledger_not_changed_by_this_producer=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_records=84,decisions=dict(decisions),native_formatting_argument_role_and_release_pending=True))
