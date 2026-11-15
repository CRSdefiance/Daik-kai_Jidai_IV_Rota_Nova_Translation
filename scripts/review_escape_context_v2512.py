"""Fresh contextual review of13 companion escape/cover alternatives."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.duel_editorial_layout_v1155 import compiled,ESCAPE_IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_editorial_v2512')
DOC=Path('translations/escape_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/escape_context_source_v2508/all13_clean_current_context_catalog.json')
CONTEXT=Path('work/analysis/escape_source_handoff_v2510/next13_direct_escape_source_packet.json')
NOTES={
1951:('A companion politely urges the named defeated person to escape and calls on everyone to provide cover.','%s, please get to safety! Everyone, give them cover! preserves the personal plea and separate collective command. Them refers neutrally to the named person rather than assuming a gender. Get to safety conveys the escape intent,not a successful escape already achieved.'),
1952:('A companion urgently tells the named person to flee quickly and reassures them that everyone will provide cover.','%s, get out of here! We\'ll all cover you! preserves urgency through the direct escape imperative and the inclusive all reassurance. It supplies no destination or guarantee of survival;it remains a companion\'s promise.'),
1953:('A companion urgently tells the named person to escape and rallies everyone to provide cover.','%s, get away now! Everyone, give them cover! retains explicit immediacy,the named addressee and the group call. Them remains neutral,with no invented relationship or particular weapon.'),
1954:('A rough-speaking companion asks the named person to flee and calls the others to provide cover.','%s, get out of here! Come on, lads, cover them! preserves the urgent plea and rough familiar collective 野郎ども in an established nautical register. Lads is this speaker\'s collective address,not a roster fact about every crew member. Come on conveys the rallying force;no rank,kinship or specific weapon is added.'),
1955:('An older-voiced companion tells the named person to escape and calls everyone to provide cover.','%s, get to safety! Everyone, cover them! preserves the imperative and collective support naturally. The older voice remains measured rather than adopting forced archaic syntax,family address or a new rank.'),
1956:('A simple reassuring companion urgently tells the named person to run and promises that everyone will protect them.','%s, run! We\'ll all protect you! retains the drawn-out plea as an urgent natural imperative and the collective promise. Protect preserves 守る without narrowing it to a particular attack or guaranteeing that protection succeeds.'),
1973:('A companion politely asks the admiral to escape and orders everyone to provide cover.','Admiral, please get to safety! Everyone, give them cover! retains the explicit 提督 address,the polite plea and the collective command. Them remains suitable for Rafael,Hodram,Lil or Maria;it invents neither a male-only role nor a family relationship.'),
1974:('A companion tells the admiral to escape while promising covering support.','Admiral, get to safety! We\'ll cover you! preserves the reassuring cover-and-escape thought in natural English order. It does not claim that the admiral has already reached safety or add an unseen rescue party.'),
1975:('A companion politely asks the admiral to escape and calls everyone to provide cover.','Admiral, please get to safety! Everyone, cover them! preserves the plea and the clipped collective call. The source explicitly supplies Admiral;them avoids assigning gender to the main-captain branch.'),
1976:('A rough-speaking companion asks the admiral to escape and firmly orders the others to provide cover.','Admiral, get out of here! Lads, cover them! retains the source rank,the urgent plea and the forceful 野郎ども command in the established nautical voice. The gendered-sounding group call is the character\'s own address,not a claim about actual crew composition;them leaves the admiral\'s gender open.'),
1977:('An older-voiced companion tells the admiral to escape and calls everyone to provide cover.','Admiral, get clear! Everyone, give them cover! is natural urgent nautical English for the escape-and-cover command. Get clear adds no named destination or completed retreat. Older speech is retained without kinship or artificial archaism.'),
1978:('A companion urgently tells the admiral to run and orders everyone to provide cover.','Admiral, run! Everyone, cover them! preserves the short urgent command and collective response. It does not turn a plea into an observed successful escape or specify the covering weapon.'),
1979:('A companion asks the admiral to entrust the covering support to them and to escape quickly.','Admiral, we\'ll cover you! Get to safety now! retains the reassurance,covering responsibility and explicit immediacy. We naturally voices the companion\'s support in this shipboard group situation;it adds no named helper,relationship or guaranteed outcome.'),
}

if __name__=='__main__':
 assert not ROOT.exists() and not DOC.exists()
 packet,context=read(PACKET),read(CONTEXT)
 priorpath=Path(context['registered_manuscript'])
 prior={r['message_id']:r for r in read(priorpath)['records']}
 assert set(NOTES)==set(ESCAPE_IDS)
 rows=[]
 for source in packet['records']:
  n=source['message_ID'];old=prior[n]
  assert source['source_hex']==old['source_hex'] and bytes.fromhex(source['current_hex'])==compiled(old)
  meaning,reason=NOTES[n]
  row=deepcopy(old)
  row.update(file_path='/COMMON/MESFILE.DK4',prior_speaker_metadata=old['speaker'],speaker_metadata_corrected=False,
   context='Original defeat-flow companion escape-and-cover response after player HP becomes nonpositive. Original First Mate or source-selected alternate companion speaks through53F0C. Named1951-1956 and Admiral1973-1979 are independent voice/actor-predicate alternatives,not consecutive speech. The main-captain IDs0-3 use the source Admiral address without a name argument;other IDs use original compact vtable+20 labels. Preserve direct return-parent02053F40/table stack+274;do not reuse the superseded53DB8/+27C frame. No actual outcome is imposed by wording. '+old['context'],
   source_Japanese=source['clean_Japanese'],source_reference=source['source_reference'],current_reference=source['current_reference'],
   current_hex=source['current_hex'],current_stored_English=source['current_stored_English'],source_meaning=meaning,
   localization_note=reason,fresh_retained_wording_justification=reason,editorial_decision='retain-wording',
   review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
  rows.append(row)
 ROOT.mkdir(parents=True)
 supplement=ROOT/'source_context_and_faithfulness_review.json'
 save(supplement,dict(records=[],all13_complete_clean_source_and_defeat_flow_reread=True,independent_alternatives_not_sequential_turns=True,
  all6_complete_compact_name_arguments_preserved=True,all7_Admiral_addresses_explicit_in_source=True,
  neutral_them_protects_all_four_captain_identities=True,rough_lads_retains_source_collective_address_not_a_roster_fact=True,
  escape_commands_and_cover_promises_not_completed_outcomes=True,correct_original_direct_frame_required=True,
  zero_credit_pending_native_historical_registered_reconciliation=True,full_goal_complete=False))
 doc=dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
  encoder='dialogue-relocatable-v1',consumer_layout_profile='duel-distinct-postmacro24x3-and-escape-speech35x4-v1',
  review_gates=['source','context','localization','naturalness','formatting'],file_path='/COMMON/MESFILE.DK4',
  source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
  current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
  source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),
  native_context_proof=str(CONTEXT),native_context_proof_sha256=sha(CONTEXT.read_bytes()),
  fresh_ordinary_supplement=str(supplement),fresh_ordinary_supplement_sha256=sha(supplement.read_bytes()),
  prior_manuscript=str(priorpath),prior_manuscript_sha256=sha(priorpath.read_bytes()),revised_IDs=[],retained_count=13,
  speaker_metadata_corrections=[],formatting_review_pending=True,current_native_and_actual_family_reconciliation_pending=True,
  records=rows,full_goal_complete=False)
 save(DOC,doc)
 save(ROOT/'fresh_source_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
  individual_new_glosses_and_retention_reasons=13,no_English_speaker_ROM_or_runtime_change=True,
  completion_pending_native_historical_registered_reconciliation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('13 fresh source glosses and contextual retention reasons saved;formatting and reconciliation pending.')
