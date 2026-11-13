"""Fresh whole-exchange prose review of61 shared-town entries; formatting still pending."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_trade_port_review_v2151');DOC=Path('translations/town_trade_port_contextual_editorial_manuscript_v1.json');PACKET=Path('work/analysis/town_trade_port_source_v2149/all61_clean_current_context_catalog.json');CONTEXT=Path('work/analysis/town_trade_port_context_v2150b/clean_graphs_current_typed_arguments_and_companion_roles.json')
REVISED={654:"If you've brought %s, be sure to sell your stock at the Market soon!",655:'Time to sell %s and rake in the money!'}
REASONS={
267:"Retain the complete Sell refusal. The native eligible-ship list is empty; the line does not invent a last-ship rule or call the operation scrapping.",
653:"Retain like hotcakes: it conveys the merchant's lively report of strong current sales, accommodates every product name, and makes no stockout or quantity claim.",
654:"Revise the compressed Brought ...? and blunt now! into a courteous conditional followed by prompt selling advice. Market matches the existing facility label; your stock is number-neutral for all goods. Preserve brought goods, urgency and selling location without inventing a forecast.",
655:"Revise profit handsomely to rake in the money. The merchant is eagerly rallying to sell the named good and make lots of money; the idiom preserves that energetic, colloquial patter.",
765:"Retain the additional market-share favor and reassuring follow-up. Too preserves the supplemental offer, while a little adds no numeric amount or invented investment condition.",
766:"Retain the idiomatic shopkeeper farewell. Come back anytime naturally requests repeat business after the distinct share, letter and thank-you branches without introducing another obligation.",
767:"Retain both product names in native order, fast sales and frequent stockouts. The plural pronoun refers to the two goods, so the complete explanation remains grammatical across product names.",
768:"Retain the surprised acknowledgment, gratitude and repeated shortages. Demand is number-neutral and faithfully explains why a delivery of the supplied good helps.",
769:"Retain the enthusiastic favorable-treatment offer followed by its two-product explanation. Sweeten the deal conveys service without promising an unsupported discount percentage.",
770:"Retain hesitation before agreeing to favorable treatment. Demand's booming works for mass or plural goods and preserves the cause without adding a precise benefit.",
771:"Retain the wish for an early end to the war and its present harm to trade. The merchant sounds frustrated without inventing a forecast or military outcome.",
772:"Retain the recent economic improvement and resulting ease of business. The conversational contraction and lately preserve the temporal direction.",
773:"Retain the recent downturn and strong complaint about doing business. A real struggle conveys the source emphasis without inventing bankruptcy or shortages.",
774:"Retain the sudden idea, letter of introduction and gratitude for popular goods. This branch does not add the large-quantity qualification used by other reward lines.",
775:"Retain And as an additional reward and retain recommendation, many goods and gratitude. The complete branch continues with the any-town explanation rather than the small-town limit.",
776:"Retain the sudden offer of an introduction for a large quantity. Its following upgrade check and letter distinction remain separate spoken records in the native graph.",
777:"Retain recognition of the existing introduction and adding a few words to upgrade it. The line explicitly reaches recommendation without inventing a second physical letter.",
778:"Retain the sudden recommendation offer and thanks for a large quantity. It matches the any-town follow-up and remains distinct from the additional And variant.",
779:"Retain small town, both possible authorities, market share and should. The merchant expresses an expectation rather than guaranteeing an exact grant.",
780:"Retain any town and both authorities, with should preserving uncertainty. This is the recommendation branch, so no small-town limitation is imported.",
781:"Retain the explicit contrast between introduction in small towns and recommendation in any town. The brief two-sentence explanation naturally clarifies the upgrade.",
782:"Retain deliberation, the connection to popular goods and a little extra. The vague favor remains vague; the line promises no specific bonus size.",
783:"Retain surprise, gratitude and Keep them coming. The merchant asks for continued supply in lively American sales language without adding a transaction reward.",
784:"Retain the five-ship fleet limit and resulting dock placement. The explanation concerns the new ship, not a fleet deletion or a permanent ban on purchase.",
785:"Retain design-copy language in the buy-a-matching-ship exchange. The following native specification and price/preparation lines establish a new matched ship; the question is concise and natural.",
786:"Retain the two spoken stat labels and their order. Masts: 1 is grammatical label usage where a sentence ending in 1 masts would fail; durability retains its supplied value without inventing units.",
787:"Retain the brief acknowledgment of keeping the ship in the dock. The first-person plural is natural for the yard staff and preserves the service.",
788:"Retain the direct question selecting a ship for sale. It is a full conversational prompt and does not confuse sale with the copy-purchase branch.",
789:"Retain the conversational price offer and question. The installed original-call adapter supplies the complete singular/plural gold-coin amount, so no currency fact is omitted.",
790:"Retain the complete, upbeat no-repairs-needed response. It states the native empty repair list without adding a reason or repair cost.",
791:"Retain the polite volunteer's complete offer of help. I'll and too express a willing additional contribution without overstating special skill.",
792:"Retain the familiar volunteer's I can help and upbeat ending. Native IC expands to the Japanese first-person pronouns boku/atashi, not a character name; English I preserves both meanings without deleting a named person.",
793:"Retain let me help as the softer request to be allowed to join the repairs. It distinguishes this voice from the more assertive volunteers.",
794:"Retain lend a hand and the assertive exclamation for the rougher ore voice. The helpful intent stays intact without adding profanity or a new rank.",
795:"Retain the calmer elder-register offer with the repair task explicit. English does not need a fabricated archaic dialect to distinguish the measured offer from the rougher one.",
796:"Retain the eager youthful voice's lively address and full repair offer. The enthusiasm distinguishes oira from the formal and hesitant alternatives without inventing age or kinship.",
797:"Retain could and the trailing hesitation. The volunteer begins an offer and trails off; it is not a completed refusal or a deliberate visual line break.",
798:"Retain the condition that this helper participates and the exact percentage discount. They're avoids unsupported gender, and percent is a word while the single native argument remains intact.",
799:"Retain the quoted repair cost and explicit shortfall. The typed argument supplies complete gold-coin units; the broker's straightforward conclusion adds no new fee.",
800:"Retain the repair quote followed by a natural confirmation. Singular/plural currency is supplied by the original scoped numeric call rather than hardcoded in the paragraph.",
801:"Retain the one-day duration and request to wait until completion. Both source facts remain clear and the service worker's request is natural English.",
802:"Retain complete repair, the price and permission to proceed. The conditional offer does not silently repair the ship before the player answers.",
803:"Retain the same-specification ship, full price, preparation duration and purchase question. Native argument order is name/typed gold/typed days; literal FA/FI/FO/IC letter pairs in names remain data.",
804:"Retain the zero-remodeling branch, matching target ship and complete price. No preparation duration is invented, and the purchase still requires confirmation.",
805:"Retain the rhetorical objection and captain requirement. The speaker reminds the admiral to command a ship; the line does not ask whether to adopt a new rank.",
806:"Retain future disposal of excess food and confirmation. Any excess preserves the conditional quantity and does not claim all provisions will be thrown away.",
807:"Retain Claudio's emphatic insistence on staying beside the admiral. The affectionate confidence is not recast as kinship or a newly invented personal relationship.",
808:"Retain Camille's concern and request to stay, addressing the actual admiral short name. Direct you avoids an unsupported gender, and the literal-name path preserves all supplied bytes.",
809:"Retain Gerhard's formal refusal and insistence on remaining the admiral's aide. I will suits the source polite register; a casual contraction would weaken that distinction.",
810:"Retain Sera's halting reluctance and ellipses. The words stay whole, and the hesitation does not invent a romantic motive or inability to speak normally elsewhere.",
811:"Retain Xien's explicit guardian relationship and refusal to leave the ship. Guardian is supported by koukennin; no father or grandfather relation is inferred.",
812:"Retain the warning about dumping excess water and the confirmation. Nautical dumped naturally distinguishes water disposal from food disposal without changing the mechanic.",
813:"Retain the observed low water and conversational offer to resupply. It remains a question rather than claiming resupply has already happened.",
814:"Retain apparent sailor fatigue and the suggestion of the inn. Why not let them rest is advice, not an invented mandatory rest rule.",
815:"Retain the complete no-cargo statement. No extra vocative is needed to convey the source familiar address in this service refusal.",
816:"Retain the insufficient funds for full replenishment and offer to buy an affordable amount. No exact proportion or guarantee of full supplies is invented.",
817:"Retain the question about the water-to-food ratio with both materials explicit. It remains a player choice and does not silently reverse their proportions.",
818:"Retain the polite, unfinished refusal invoking clear billing. The understatement fits the payment problem without inventing posted prices, cash-only policy or cheap drinks.",
819:"Retain the blunt no-free-drinks refusal. Its terse roughness contrasts naturally with the polite billing reply without adding insults.",
1245:"Retain the complete required-price shortfall. The original numeric argument and mass currency noun gold remain grammatical for one or many coins.",
1246:"Retain the price and courteous confirmation. Native acceptance may debit the amount; the English does not imply payment before the answer. Gold remains number-neutral."
}
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True);packet=read(PACKET);context=read(CONTEXT);assert packet['current_ARM9_sha256']==context['ARM9_sha256'];previous={}
 for name in['town_responses_manuscript_v1.json','market_replies_manuscript_v1.json','market_stock_manuscript_v3.json','shipyard_editorial_manuscript_v3.json','port_services_editorial_manuscript_v2.json']:
  p=Path('translations')/name
  for r in read(p)['records']:
   if r['message_id']in packet['selected_IDs']:assert r['message_id']not in previous;previous[r['message_id']]=(p,r)
 assert set(previous)==set(REASONS)==set(packet['selected_IDs']);rows=[]
 for source in packet['records']:
  n=source['message_ID'];path,old=previous[n];assert old['source_hex']==source['source_hex'];oldtext=old['english'].removesuffix('{PAD}');assert ' '.join(source['current_stored_English'].split())==oldtext
  row=deepcopy(source);row.update(id=f'COMMON_MESSAGE_{n}',message_id=n,japanese=source['clean_Japanese'],english=REVISED.get(n,oldtext)+'{PAD}',speaker=old['speaker'],context=old['context']+' Fresh V2150b binds clean/current source decisions and native typed arguments; table neighbors are not presumed consecutive speech.',source_meaning=old['source_meaning'],localization_note=REASONS[n],editorial_decision='revise'if n in REVISED else'retain-wording',previous_manuscript=str(path),previous_manuscript_sha256=sha(path.read_bytes()),review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='fresh-source-context-prose-reviewed-native-display-revised-gameplay-release-pending')
  if n not in REVISED:row['fresh_retained_wording_justification']=REASONS[n]
  rows.append(row)
 groups=[dict(name='Independent current-trend sales advice',IDs=[653,654,655],flow='Source trend state and random alternative choose one product-bound remark.653/655 are alternatives during strong sales;654 is the later sell-soon advice,not a single consecutive speech.'),dict(name='Market supplementary share favor and repeat-business farewell',IDs=[765,766],flow='765 adds preferential share and reassurance;766 closes the original transaction branch. Full bonus eligibility is not inferred.'),dict(name='Market product shortages and economic replies',IDs=list(range(767,774)),flow='One/two supplied products and the favorable-treatment flag choose767/768/769/770;independent economic state chooses771/772/773 or original greeting8.'),dict(name='Market letters, upgrade explanation and alternative closing favors',IDs=list(range(774,784)),flow='774->779->766;775/778->780->766;776->777->781->766;alternative782/783->766. Retain introduction/recommendation,small/anytown,andlarge quantity distinctions.'),dict(name='Yard new/matching ship, sale and dock placement',IDs=[267,784,785,786,787,788,789,803,804],flow='Buy/copy selects a source ship andshows specs then803 positive preparation or804 no-remodeling confirmation;fleet limit784 anddock787 are their original branches. Sell selects788->789,with267 when the eligible list is empty.'),dict(name='Yard repair inquiry, seven volunteer voices, discount and confirmation',IDs=list(range(790,803)),flow='No damage790;otherwise price/insufficient funds799 orconfirm800/802. Eligible helper level>=25 queues one791..797voice anddiscount798. Accepted repairs give one-day request801.'),dict(name='Port resupply, command and companion reassignment refusals',IDs=list(range(805,818)),flow='Port service branches select relevant command/resupply/rest/cargo questions. Reassignment chooses Claudio807,Camille808,Gerhard809,Sera810 orXien811 under original actor/route conditions;these are independent vetoes.'),dict(name='Tavern payment refusals and generic service charge',IDs=[818,819,1245,1246],flow='Distinct polite/rough insufficient-payment replies818/819. Generic service charge1246 asks approval;1245 states insufficient funds. Preserve native confirmation/debit direction.')]
 doc=dict(format='dk4-common-entry-manuscript-v1',translation_policy='natural-dialogue-v2',encoder='dialogue-fixed-v1',target_locale='en-US',file_path='/COMMON/MESFILE.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_COMMON_sha256=packet['source_COMMON_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256'],revised_IDs=sorted(REVISED),retained_count=59,formatting_review_pending=True,conversation_groups=groups,source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context=str(CONTEXT),native_context_sha256=sha(CONTEXT.read_bytes()),records=rows,no_new_historical_completion_credit=True,full_goal_complete=False);save(DOC,doc);save(ROOT/'source_context_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=61,revised_IDs=sorted(REVISED),justified_retentions=59,all61_clean_Japanese_and_original_functional_exchanges_reviewed=True,IC_proven_first_person_not_a_character_name=True,prices_days_and_literally_named_ships_preserved=True,formatting_actual_revised_and_release_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(reviewed=61,revised=2,retained=59,formatting_pending=True))
