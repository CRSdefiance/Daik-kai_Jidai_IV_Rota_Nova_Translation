"""Fresh whole-exchange market reread; no English or ROM changes."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.verify_market_context_v753 import selections, SPANS
from scripts.review_market_contract_v758 import context_cases
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
ROOT=Path('work/analysis/market_context_review_v2114')
DOC=Path('translations/market_contextual_editorial_manuscript_v1.json')
IDS=sorted(set(range(745,765))-{750,751,752})
NOTES={
745:'Anything else? naturally asks whether the customer has further business. Retain the concise merchant follow-up without adding a new offer or impatience absent from this question.',
746:'Just browsing? conveys the merchant\'s disappointed recognition of a transaction abandoned without an amount. The source ellipsis informs the reaction, but a separate written hesitation is unnecessary for this brief natural question.',
747:'The appreciative thanks and promise to put the investment to good use answer the successful amount choice naturally. Business we is appropriate and makes no promise about an invented return or percentage.',
748:'Huh? preserves the surprised reaction; not enough to work with states the practical refusal. The next sentence directs the player to return after earning more, preserving the progression from surprise to explanation to invitation.',
749:'The warning explicitly says the cargo holds are full and asks the buyer to reduce the purchase. Buy less covers quantity or selection without inventing a particular type of cargo restriction.',
753:'The direct complete warning states insufficient money in idiomatic English. The source familiar second-person address needs no extra you there or invented scolding.',
754:'The polite adviser weighs a possibility, limited to certain goods and the present occasion. Larger quantities and paying double preserve the actual proposal; retain the measured may be able rather than promising a universal offer.',
755:'The conversational looks like and they\'ll sell us retain the adviser\'s inference and seller perspective. Some goods, this time and double payment all remain explicit.',
756:'I think preserves the adviser\'s tentative observation. We can buy is idiomatic in this conversational voice and does not invent certainty beyond the opening qualification. Keep the quantity, limited selection, time and double-price condition.',
757:'Bigger quantities and right now give the rougher informal adviser a distinct, natural voice. Looks like still marks inference, and some goods limits the offer. No added slang, rank or identity is needed.',
758:'It seems and the seller-oriented construction preserve the measured older register without inventing an age-based name or relationship. The present offer, larger amount, limited goods and double payment remain intact.',
759:'I bet and the exclamation preserve the youthful enthusiasm. Lots more reflects takusan; some goods and this time keep the offer bounded, while double payment remains a condition.',
760:'It appears and certain goods distinguish the polite measured register from the more casual advisers. The wording preserves the current occasion, increased quantity and double payment without assigning a character identity.',
761:'The merchant apologizes, directs the player to sign a contract at the supplied facility, then asks them to return. At the %s is faithful to the native Palace or governor-office argument; no city is invented and the substitution is retained exactly.',
762:'The merchant first notes the inability to trade without market share, then admires the voluntary investment and asks the amount. Generous of you conveys kitoku in context without treating the player as merely strange. Retain all three conversational steps.',
763:'The surprised investment question leads into explicit flattery, then the amount prompt. Different from the rest faithfully preserves the merchant\'s praise without inventing a trait, title or new relationship.',
764:'The funds warning leads to the blunt charity objection and pay-to-see condition. A look keeps the object implicit as in the source; the current line does not invent a report identity or pretend this is an investment refusal.'}
if __name__=='__main__':
 assert not ROOT.exists() and not DOC.exists();ROOT.mkdir(parents=True)
 packet=read('work/analysis/market_context_source_v2108/market656_764_clean_current_context_catalog.json');rows={r['message_ID']:r for r in packet['records']}
 originals={}
 for p in ('translations/town_responses_manuscript_v1.json','translations/market_replies_manuscript_v1.json','translations/market_contract_manuscript_v2.json'):
  for r in read(p)['records']:originals[r['message_id']]=(p,r)
 records=[]
 for n in IDS:
  p,old=originals[n];r=deepcopy(rows[n]);english=old['english'];assert ' '.join(english.removesuffix('{PAD}').split())==' '.join(r['current_stored_English'].split())
  r.update(id=f'COMMON_MESSAGE_{n}',message_id=n,japanese=r['clean_Japanese'],english=english,speaker=old['speaker'],context=old['context'],source_meaning=old['source_meaning'],localization_note=NOTES[n],fresh_retained_wording_justification=NOTES[n],editorial_decision='retain-wording',decision='retain-wording',previous_manuscript=p,previous_manuscript_sha256=sha(Path(p).read_bytes()),review=dict.fromkeys(('source','context','localization','naturalness','formatting'),True),status='fresh-source-context-retention-native-and-representative-actual-verification-pending',formatting_gate_scope='Existing encoding retained; final native pages and actual consumer geometry still require the new evidence packet.')
  records.append(r)
 rom=NdsImage.open(packet['current_ROM']);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
 assert all(clean[a:b]==arm[a:b]for a,b in SPANS)
 assert selections(clean)==selections(arm)
 cases=context_cases(arm)
 save(ROOT/'original_market_decision_graph_current.json',dict(current_ARM9_sha256=sha(arm),clean_current_bound_source_spans=[dict(start=0x02000000+a,end=0x02000000+b,sha256=sha(arm[a:b]))for a,b in SPANS],investment_and_paid_viewing_fragments=selections(arm),advice_and_facility_context=cases,external_state_inputs_explicitly_supplied=True,not_actual_gameplay=True,not_full_transaction_eligibility_proof=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 doc=dict(format='dk4-common-entry-manuscript-v1',translation_policy='natural-dialogue-v2',encoder='dialogue-fixed-v1',target_locale='en-US',file_path='/COMMON/MESFILE.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],records=records,conversation_groups=[dict(name='Merchant follow-up and investment',IDs=[745,746,747,748,762,763],flow='Existing visit -> investment offer for share/no-share -> amount choice -> thanks, zero-amount browsing response or insufficient-funds refusal. These are alternatives, not one consecutive speech.'),dict(name='Trade capacity and funds warnings',IDs=[749,753],flow='Purchase selection -> capacity or funds objection; native purchase function controls the return.'),dict(name='Extra-stock adviser alternatives',IDs=list(range(754,761)),flow='Current extra-stock predicate -> one of seven role3 adviser voices; not seven consecutive speakers.'),dict(name='Contract refusal',IDs=[761],flow='Merchant visit -> missing contract -> facility-specific request to sign and return.'),dict(name='Paid market viewing refusal',IDs=[764],flow='Quoted viewing price -> insufficient funds -> merchant refusal.')],neighbors_reviewed_for_context=[743,744,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783],neighbor_review_does_not_add_completion_credit=True,unresolved_restart_annoyance_IDs=[750,751,752],unresolved_three_not_authored_or_revised_or_completed=True,no_ROM_or_registered_release_change=True,status='fresh-contextual-retentions-native-and-actual-checks-pending',full_goal_complete=False)
 validate_natural_dialogue_batch(doc);save(DOC,doc)
 print(dict(fresh_retention_drafts=len(records),native_decision_fragments=len(selections(arm)),unresolved=[750,751,752],ROM_changed=False))
