"""Fresh clean-Japanese whole-exchange review; formatting and reconciliation remain pending."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/recruitment_scheme_prose_v2201')
DOC=Path('translations/recruitment_schemes_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/tavern_recruitment_schemes_source_v2195/all106_clean_current_context_catalog.json')
PROOFS=[
 Path('work/analysis/tavern_recruitment_context_v2196b/native_context.json'),
 Path('work/analysis/tavern_schemes_context_v2197b/native_context.json'),
 Path('work/analysis/tavern_followup_context_v2198/native_context.json'),
 Path('work/analysis/current_scheme_filter_binding_v2200/source_filter_and_current_name_contract.json'),
]
REVIEWS='''
883|Reports to the admiral that the party lacks sufficient money.|Retain the complete, straightforward shortfall report. We includes the company naturally; Admiral is the explicit source address, not an invented rank.
884|Tentatively reports that there seems not to be enough money.|Looks like preserves mitai and the softer assessment. It does not turn the estimated shortfall into a different fee or an accusation.
885|Hesitantly tells the admiral that there is not enough money.|Um... preserves the tentative opening before the clear financial refusal. The hesitation stays distinct from the direct883 without invented embarrassment or a new relationship.
886|Familiarly tells the admiral they are short of money.|Short on cash is idiomatic and direct, fitting the rougher ze ending. No profanity, insult or extra price is added.
887|A measured familiar voice reports insufficient funds.|Moving Admiral to the end gives the brief reply a calmer cadence. The source's older register does not require fabricated archaic English.
888|Calls out to the admiral with an emphatic complaint about insufficient money.|The exclamation conveys the stretched, lively address without an unnatural phonetic spelling of Admiral or an invented speech defect.
889|Politely begins an insufficient-funds report and trails off.|Short on funds and the ellipsis preserve the more formal, unfinished approach. This is still a refusal, not a promise that funds will appear.
890|States the quoted gold cost for recruiting sailors.|I'll recruit sailors is an intention before the native Yes/No decision. Gold stays grammatical for every full-width numeric amount and does not imply the payment already happened.
891|Casually proposes recruiting sailors for the quoted cost.|Some sailors gives the offer a conversational cadence without inventing a count. The price remains the only supplied quantity.
892|Politely says the quoted amount will be spent to gather sailors.|I'll spend ... to recruit preserves the explicit spending-for-purpose construction. It does not report a completed recruitment or a second charge.
893|A rougher voice offers to gather sailors at the quoted cost.|I'll find us some sailors carries the confident, helpful tone without fake dialect. Us refers naturally to the admiral's company rather than a new faction.
894|A firm voice states the expenditure to recruit sailors.|I'll spend ... recruiting keeps the more decisive intention. It neither guarantees a number nor moves the native debit ahead of approval.
895|A lively casual voice offers to gather sailors for the amount.|Find some sailors is an ordinary, energetic promise of effort. Some is number-neutral and no volunteers are declared already aboard.
896|A polite voice explains the money to be used for recruitment.|I'll use ... to recruit preserves both the specified funds and purpose. The full native numeric argument and confirmation remain intact.
897|Calls for anyone who wants to serve aboard the admiral's ship.|Who wants to sail with the Admiral? is a natural recruiting call. The naval context makes crew service clear without adding wages or an oath.
898|Directly asks who will join the admiral's ship.|Who'll join the Admiral's crew? conveys the direct invitation in the proven recruitment exchange. It does not imply that the volunteers have already been assigned.
899|Calls on those interested in sailing with the admiral to identify themselves.|Step forward preserves nanoridenasai as a clear recruiting instruction. The more courteous if you'd like keeps this voice distinct from902.
900|A rough voice asks whether anyone here wants to sail with the admiral.|Anyone here want... is natural spoken English and retains the call to the room. No derogatory label is invented for the potential sailors.
901|A familiar, considered voice asks for volunteers for the admiral's ship.|Who'll sail with the Admiral? retains the simple invitation without a contrived old-man dialect or a new condition of service.
902|Forcefully calls interested volunteers to come forward.|The question followed by Step forward! preserves the source's assertive command and differs from899's softer invitation.
903|A lively familiar voice asks for anyone interested in the admiral's ship.|Anyone for the Admiral's crew? is a complete, idiomatic call in context. It preserves the offer without adding a person count or a reward.
904|Reports how many people have gathered, before Assign Sailors.|We've got ... willing to join is a natural count report after the volunteer call. Its understood noun is people; it does not falsely say they have already been assigned to ships.
905|Politely relays a recent, pronounced condition affecting a named town.|I hear and lately preserve hearsay and time. The original status pointer is expanded into a grammatical private phrase; positive boom and negative conditions remain distinct, and Normal12 is excluded upstream.
906|Casually relays a recent, pronounced town condition.|Word is preserves the rougher keeper's hearsay. Going through fits the supplied condition phrase; the original UI labels stay unchanged while the scoped dialogue adds articles and degree.
907|An enthusiastic spoken response follows the recruitment call.|Aye! is an idiomatic nautical acknowledgment of that call. It is not attached to the independent town rumor, and no individual or group identity is invented for the reaction NPC.
908|Quotes an approximate thousand-gold cost to disrupt an enemy, then asks what scheme to use.|Disrupting the enemy and about preserve purpose and approximation. What kind ... in mind? is natural consultation, not a report of a successful operation.
909|Says a thousand gold coins can fund disruption and asks which scheme to choose.|The courteous With ... we can construction preserves the stated budget and possibility. The question still precedes both target selection and any charge.
910|Suggests a thousand gold coins should be enough, then asks which scheme to use.|Should be enough conveys the conversational sufficiency check. It avoids turning the speaker's confidence into guaranteed success.
911|Confidently says a thousand gold coins can unsettle the enemy and asks for a plan.|Throw the enemy off balance localizes kakuran naturally. What scheme do you want? preserves the direct, familiar register without adding a threat.
912|A considered voice says a thousand gold coins should suffice and asks which plan is best.|Certainly reflects the source confidence and emphasis on sufficiency. It remains the speaker's assessment, not a change to the original success mechanics.
913|Enthusiastically proposes using a thousand gold coins to surprise the enemy.|Really surprise them and What should we do? retain the lively anticipation. No invented weapon, victim or guaranteed result replaces the source generality.
914|Politely estimates roughly a thousand gold coins and asks which disruptive scheme to try.|About and should preserve the estimate. Shall we try maintains measured courtesy without an artificial archaic voice.
915|Confirms the selected scheme label, then politely asks for the opposing faction.|Correct? and Please choose preserve the two-step consultation. The exact native UI action label stays recognizable, and target selection has not yet happened.
916|Casually checks the chosen scheme and asks which faction to target.|Then? is a natural label acknowledgment. Which faction preserves the source organization scope without substituting a person or a town.
917|Directly confirms the selected plan and asks for the opponent.|Right? and are we targeting keep the familiar, practical voice. The faction has not already been chosen or attacked.
918|A measured familiar voice checks the plan and asks which opposing faction to use.|The short then? fits the source reflective confirmation. It preserves the choice without a fabricated archaic pronoun or title.
919|Livelily acknowledges the plan and asks which faction to face.|Right? So... carries the conversational transition. Which faction keeps the intended target category explicit.
920|Formally considers the named plan, then asks which faction to choose.|Hmm and shall we preserve deliberation and courtesy. The label argument is retained in full, not treated as a character name.
921|Asks which town the selected enemy fleet should be made to head toward.|I send them is a natural strategist question in the Lure Fleet branch. Them refers to the selected opposing fleet, not an invented player detachment.
922|Casually asks which town to send the selected fleet to.|Are we sending them to? preserves the impending choice. The town is a destination, not a claim that the fleet has arrived.
923|Directly asks the admiral for the selected fleet's destination.|Which town do you want me to send them to? preserves the rougher practical question without adding orders or a completed movement.
924|A measured voice asks which town to send the fleet toward.|Shall we send them to? gives the familiar source question a considered cadence. No new timing or travel distance is introduced.
925|A lively voice asks where the fleet should go.|Which town should they go to? keeps the simple, conversational wording while the preceding selection supplies the fleet referent.
926|Formally asks which town the admiral would like the fleet sent to.|Would you like us to... preserves deference and the causative plan. The collective us is ordinary company speech, not a new fleet.
927|Politely asks which town should receive the rumors.|The complete town question is natural in the Bad Rumors branch. In preserves the place of distribution rather than changing it to the subject of the rumor.
928|Casually asks where to spread the rumors.|The shared natural wording works for this shorter source alternative. A different English accent is not needed to manufacture a distinction.
929|Directly asks in which town the rumors should be spread.|Do you want the rumors spread in? retains the rougher, practical request. It does not claim that spreading has already begun.
930|A measured familiar voice asks which town to use for the rumor operation.|Shall we spread... gives this voice a considered register. The town remains the location, not the faction being maligned.
931|Livelily asks where the rumors should be spread.|Where do you want us to... is natural within the native town-selection exchange. The preceding branch and actual selector retain the town scope.
932|Formally asks in which town the admiral would like rumors spread.|Would you like us to... preserves the deferential question. The plan stays conditional on a selection and later confirmation.
933|Asks which other faction the already selected faction should be turned against.|Which faction makes the second-target scope clear. The original filter excludes the player and first target; no new participant or completed feud is invented.
934|Casually asks whom the selected faction should be induced to fight.|Get them to pick a fight with is an idiomatic rendering of kenka saseru. Them refers to the first faction, not the admiral's own crew.
935|Politely asks whom to make the first faction fall out with.|Who should we turn them against? preserves the relational aim. Who naturally refers to a named organization in this dialogue, not an invented person.
936|Directly asks which opponent should be set against the selected faction.|Set them against conveys the intended discord without forcing a literal insult for doitsu. The second choice remains unmade.
937|A measured voice asks which faction should become the first faction's opponent.|Shall we turn them against? preserves the considered question. The first faction is supplied by the surrounding exchange and not silently changed.
938|A lively voice asks whom the selected faction should be made to fight.|Picking a fight with retains the casual kenka effect. It asks about an intended quarrel rather than declaring a war has occurred.
939|Formally asks which faction the admiral wants the first target turned against.|Would you have us... preserves the more formal register. It adds no rank or guaranteed hostility outcome.
940|Confirms a plan to lure the named faction's fleet to the named town.|We'll ... Is that correct? is natural neutral confirmation. From avoids awkward possessives with Fleet names, and faction-before-town order is preserved.
941|Politely checks that the admiral wants a named faction fleet lured to a town.|You'd like us to... preserves the deferential confirmation. It describes the requested plan, not a movement already completed.
942|Casually checks drawing a fleet from the named faction out to a town.|So and drawing ... out preserve the conversational check and lure intent. Both complete names remain in their original roles.
943|Softly confirms the admiral's wish to draw a faction fleet to a town.|You want us to... right? preserves the source request for agreement. No feminine English stereotype or new relationship is added.
944|Directly confirms luring the named faction fleet to a town.|So, we're luring ... right? matches the firm, familiar check. It is an intended action inside a Yes/No prompt, not a report of success.
945|A measured familiar voice checks the planned fleet lure and destination.|Have I got that right? naturally conveys no jana confirmation. It retains the town and faction without fabricated archaic language.
946|Livelily confirms making the named faction fleet come out to a town.|Come out to preserves the source more concrete wording. You want... right? keeps the admiral's approval pending.
947|Formally confirms the faction fleet and lure destination.|We'll lure ... Is that correct? is courteous and complete. It avoids adding an explicit order or rank beyond the source confirmation.
948|Politely confirms inducing two named factions to oppose each other.|We're to turn ... against each other preserves the formal proposal. Both faction names and their mutual relationship remain explicit.
949|Courteously checks setting the two factions against one another.|The concise question is natural when the preceding two selections supply the plan. It is not missing a completed action or a result.
950|Casually checks whether the two named factions should be made to fight.|So, we're getting ... to fight? preserves the conversational confirmation. It does not imply the factions are already fighting.
951|Softly checks the admiral's wish for the two factions to fight.|You want ... right? retains the deferential check. Each other preserves the mutual opposition without inventing a third faction.
952|Directly checks causing the two named factions to fight one another.|Getting ... to fight each other is idiomatic and assertive. So and right? preserve the request for confirmation, not a victory claim.
953|A measured familiar voice checks pitting the two factions against each other.|Pit ... against ...? is a natural elliptical confirmation in this complete exchange. The two selected targets remain clear; a longer artificial old-man form is unnecessary.
954|Livelily checks whether the two factions should quarrel with each other.|Quarrel preserves the lighter kenka register of this voice. The question does not replace the native scheme with a completed battle.
955|Formally confirms setting the two factions against each other.|We're to set ... correct? preserves the careful briefing tone. The paired names remain complete and no outcome is promised.
956|Politely confirms spreading unfavorable rumors in a town about a faction.|In and about preserve town-first/faction-second roles. The confirmation remains an intended operation, not news already spread.
957|Courteously confirms the town and faction for a bad-rumor scheme.|The statement followed by Is that correct? preserves the source polite check. Neither argument is mistaken for the other's type.
958|Casually checks spreading bad rumors at the selected town about the selected faction.|We're spreading ... right? is a natural plan confirmation. Context keeps its future intent, and both native fields stay in order.
959|Softly checks a personal assignment to spread bad rumors at a town about a faction.|I'm to... correct? expresses the source first-person task naturally. It does not invent an extra agent or completed rumor.
960|Directly asks whether to spread bad rumors in the town about the faction.|You want me to... preserves the practical request for approval. In and about prevent reversal of location and target.
961|A measured familiar voice checks the bad-rumor plan's location and subject.|Is that right? gives the confirmation a considered cadence. The English preserves both names and the intended nature of the action.
962|Livelily checks telling people in the town that the faction is disreputable.|Bad news localizes tondemonai yatsu by effect and works with organization names. It invents no specific scandal, crime or accusation beyond the bad rumor.
963|Formally considers and confirms spreading bad rumors in a town about a faction.|Hmm and correct? preserve the thoughtful formal voice. The two arguments retain their native town/faction order.
964|Offers to make the arrangements and anticipates how the plan will turn out.|Looking forward to seeing how it turns out preserves anticipation. This reply precedes the source debit and later effects; it does not claim the scheme succeeded.
965|Offers to arrange the plan and proposes awaiting good news.|Let's wait for good news preserves the hopeful shared outlook. It is not a guarantee that favorable news will actually arrive.
966|Asks the admiral to leave arrangements to the speaker and wonders about the outcome.|Leave ... to me and I wonder preserve willingness and uncertainty. The trailing ellipsis remains hesitation, not a manual display break.
967|Offers to handle the rest and hopes it goes well.|The concise, softer hope preserves the emotional progression after confirmation. It does not change an arrangement into a successful result.
968|A direct familiar voice offers to arrange the rest and looks forward to the outcome.|Leave ... to me preserves confidence, while looking forward preserves anticipation. No success or additional payment is invented.
969|A measured voice undertakes arrangements and anticipates the outcome.|I'll see to... suits the source considered register. Eager to see expresses tanoshimi naturally without an artificial archaic dialect.
970|Livelily offers to handle the rest and wonders whether it will go well.|I'll handle the rest and I wonder if it'll work out preserve the combination of enthusiasm and uncertainty.
971|Formally undertakes arrangements and looks forward to the results.|I'll make the arrangements retains the polite commitment. Results is still future-facing and does not assert that the scheme worked.
972|Relays that the regular ship due this month apparently sank in a storm.|This month's regular run preserves schedule and regularity. Apparently and the ellipsis keep the report hearsay; it is a separate town rumor, not a scheme outcome.
973|Politely asks which town's broker should be bribed.|Broker and bribe preserve the commercial intermediary and intended corrupt payment. It is a location choice before the separate ownership confirmation.
974|Casually asks in which town the admiral intends to bribe a broker.|Do you plan to bribe? preserves intention rather than reporting payment. The town remains the location, not a faction.
975|Directly asks which town's broker is to be bribed.|Are we bribing? is ordinary plan language in this question. It retains the explicit broker and does not move the charge earlier.
976|A measured familiar voice asks which town's broker to bribe.|Shall we bribe? preserves the considered request without manufactured archaic speech or a new intermediary.
977|Livelily asks which town's broker should be bribed.|Should we bribe? is clear, natural English for the source. The katakana emphasis needs no invented mispronunciation or speech defect.
978|Politely confirms bribing the named faction's broker in the named town.|In ... we're to bribe ...'s broker preserves location-first and ownership-second. It is a confirmation, not an already completed bribe.
979|Courteously confirms the selected town and the faction whose broker will be bribed.|The statement and Is that correct? retain the polite check. The possessive is the original faction affiliation, not an invented personal relationship.
980|Casually checks bribing the selected faction's broker at the selected town.|So, in ... right? preserves the conversational confirmation. Neither full native name is dropped or reversed.
981|Directly checks a personal assignment to bribe the faction's broker in the town.|I should bribe ... Is that right? preserves the practical check. The original ownership and location remain distinct.
982|A measured familiar voice checks the broker-bribery plan in the selected town.|Then? gives the confirmation its considered cadence. It does not assert the broker accepted or that the scheme has succeeded.
983|Livelily confirms bribing the faction's broker at the town.|Right? preserves the upbeat check; bribe translates the emphasized katakana naturally. No fake accent or changed payment is introduced.
984|Tells the admiral the place is full and there is no seat for private discussion, then suggests another day.|It's packed and nowhere to sit preserve both the crowd and seating reason. Another day is explicit in the source; no plan or charge has yet been made.
985|Says the crowd prevents private discussion and suggests a different day.|With this crowd... is a natural full refusal. Another day preserves betsu no hi rather than inventing tomorrow or a mandatory waiting period.
986|Familiarly tells the admiral that the crowd prevents private discussion and suggests another day.|Let's come back another day preserves the casual proposal. It neither invents a new reason nor silently advances the game date.
987|A measured voice notes the lack of a private seat and asks whether to come back.|Come back later preserves denaosu without inventing a specific day. Admiral is the source vocative, and the refusal stays a question.
988|Livelily reacts to the crowd, says a private talk is impossible and suggests tomorrow.|Wow keeps the reaction, and tomorrow preserves the explicit ashita. The line does not substitute the vaguer another day used by other voices.
'''
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists()
 packet=read(PACKET);proofs=list(map(read,PROOFS));assert len(proofs[0]['all120_actor_voice_selections_plus3_null_fallbacks'])==120 and len(proofs[1]['all320_actual_actor_voice_selections'])==320 and len(proofs[2]['all160_actual_actor_voice_selections'])==160
 assert len(proofs[0]['original_rumor_and_interjection_fragments'])==2737 and len(proofs[2]['sixteen_condition_branch_cases_for_972'])==16
 review={}
 for line in REVIEWS.strip().splitlines():
  if not line.strip():continue
  n,gloss,note=line.split('|');n=int(n);assert n not in review;review[n]=(gloss,note)
 assert set(review)==set(range(883,989))
 prior={}
 for name in('recruitment_editorial_manuscript_v3.json','tavern_schemes_editorial_manuscript_v4.json','scheme_followup_editorial_manuscript_v2.json'):
  p=Path('translations')/name
  for r in read(p)['records']:
   n=r['message_id'];assert n not in prior;prior[n]=(p,r)
 assert set(prior)==set(review)
 tables={}
 for p in proofs[:3]:
  for k,ids in p.get('three_original_role_voice_tables',p.get('original_voice_tables',{})).items():
   for slot,n in enumerate(ids):
    if n!=-1:assert n not in tables;tables[n]=(int(k,16),slot)
 groups=[
  dict(IDs=list(range(883,905))+[907],flow='Original role1 shortage883-889 or quoted recruitment890-896;approved cost ->volunteer call897-903 ->907 reaction ->count904 ->Assign Sailors. Count means gathered,not assigned.'),
  dict(IDs=[905,906],flow='Independent original578F4 town-condition reports:eligible original town bit,same region and status0-11;Normal12 excluded. Native UI status pointers are preserved and expanded only by the scoped dialogue formatter.'),
  dict(IDs=list(range(908,964)),flow='Role2 strategist introduction908-914 ->action label confirmation915-920 and first nonplayer faction selection. Lure:921-926 destination ->940-947 faction/town confirmation. Forge Papers:933-939 second opposing faction ->948-955 faction pair confirmation. Bad Rumors:927-932 location ->956-963 town/faction confirmation. These are voice alternatives,not consecutive speakers.'),
  dict(IDs=list(range(964,972)),flow='After the final plan is approved,one964-971 voice undertakes arrangements. Original1000-gold deduction follows;the speech is not a report of the scheme outcome.'),
  dict(IDs=[972],flow='Separate original town-rumor branch;the supplied source condition return5..11 selects972. Storage between scheme voices does not make it a scheme result.'),
  dict(IDs=list(range(973,984)),flow='Bribe action selects973-977 broker town ->978-983 town/faction confirmation ->approved arrangements964-971 and original subsequent charge. Source field order is town then faction.'),
  dict(IDs=list(range(984,989)),flow='Original refusal branch returns before scheme selection and charge. Retain the spoken privacy/seating explanation without claiming a newly simulated crowd state.'),
 ]
 rows=[]
 for source in packet['records']:
  n=source['message_ID'];path,old=prior[n];assert old['source_hex']==source['source_hex'];english=' '.join(source['current_stored_English'].split());assert english==old['english'].removesuffix('{PAD}')and english.isascii();gloss,note=review[n]
  table,slot=tables.get(n,(None,None))
  parent=0x02054014 if n in(905,906,907,972)else 0x02053E38 if n==904 else 0x02053D24 if n in(*range(890,897),*range(940,964),*range(978,984))else 0x02053DB8
  speaker='Original Tavern rumor NPC'if n in(905,906,972)else'Original Tavern reaction NPC'if n==907 else'Assigned role1 companion'if n<=904 else'Assigned role2 Strategist'
  group=next(g for g in groups if n in g['IDs']);r=deepcopy(source);r.update(id=f'COMMON_MESSAGE_{n}',message_id=n,japanese=source['clean_Japanese'],english=english+'{PAD}',speaker=speaker,context=group['flow'],source_meaning=gloss,localization_note=note,fresh_retained_wording_justification=note,editorial_decision='retain-wording',previous_manuscript=str(path),previous_manuscript_sha256=sha(path.read_bytes()),source_voice_table=table,source_voice_slot=slot,native_binding=dict(parent=parent,table_or_ID=904 if n==904 else table,status_argument_identity_required=n in(905,906)),English_argument_source_indices=list(range(english.count('%s'))),review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),status='fresh-whole-exchange-source-prose-reviewed-native-formatting-and-reconciliation-pending');assert english.count('%s')==source['clean_Japanese'].count('%s');rows.append(r)
 ROOT.mkdir(parents=True);doc=dict(format='dk4-common-entry-manuscript-v1',translation_policy='natural-dialogue-v2',encoder='dialogue-fixed-v1',target_locale='en-US',file_path='/COMMON/MESFILE.DK4',review_gates=['source','context','localization','naturalness','formatting'],source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],source_COMMON_sha256=packet['source_COMMON_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256'],revised_IDs=[],retained_count=106,formatting_review_pending=True,conversation_groups=groups,source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proofs={str(p):sha(p.read_bytes())for p in PROOFS},records=rows,English_identical_to_current_registered_V2171=True,no_new_historical_completion_credit=True,actual_native_fragments_not_earned_gameplay=True,full_goal_complete=False);save(DOC,doc);save(ROOT/'source_first_whole_exchange_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=106,revised=0,individually_justified_retentions=106,whole_exchange_and_current_source_provider_review_complete=True,native_formatting_current_actual_and_reconciliation_pending=True,no_ROM_registry_or_patch_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(reviewed=106,revised=0,retained=106,formatting_pending=True))
