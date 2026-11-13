"""Fresh complete-exchange review of six original flee/victory voice reports."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/aftermath_fled_editorial_v2541')
DOC=Path('translations/aftermath_fled_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/aftermath_fled_context_v2538/all6_clean_current_context_catalog.json')
CONTEXT=Path('work/analysis/aftermath_fled_context_v2538/source_context_packet.json')
NOTES={
2046:('A formal report states that the enemy flagship has fled and that our side has won.',"The enemy flagship fled! We've won! preserves both explicit facts and the relief and certainty of the report in idiomatic speech. The contraction suits a spoken victory announcement without changing its factual meaning. No Admiral address appears here;none is added. Fled does not imply sinking,capture or the enemy admiral's death."),
2047:('A brisk report announces the enemy flagship\'s flight and our victory.',"The enemy flagship fled! Victory is ours! preserves the clipped opening and complete victory declaration. Victory is ours naturally renders 我々の勝利 without imitating Japanese sentence order. The report remains brisk,not a new command or a promise of victory later. No rank or form of address is added."),
2048:('An excited speaker reports that the enemy flagship fled and directly tells the admiral that our side has won.',"The enemy flagship fled! Admiral, we've won! keeps the excited rhythm and the explicit 提督 address in the second sentence. Admiral is justified by this clean source,not inferred from a portrait or another alternative. The report concerns an escaping flagship and victory,not a captured or killed opponent."),
2049:('A familiar older-register speaker reports the flagship\'s flight and confirms victory to the admiral.',"The enemy flagship has fled! We've won, Admiral! preserves the report and warm,confident victory announcement. Moving the explicit Admiral vocative to the natural end of the second sentence preserves whom the speaker addresses. The じゃな flavor does not justify invented kinship,a caricatured accent or an extra rank."),
2050:('An informal speaker says that the ship carrying the enemy admiral got away and realizes that our side has won.',"The enemy admiral's ship ran away! That means we won! keeps the source's concrete ship description,casual 逃げちゃった and the recognition expressed by 勝ったんだね. Ran away is natural lively personification in this informal voice. That means preserves the realization without adding a strategic explanation. The enemy admiral's fate and a child age are not invented."),
2051:('A courteous speaker reports the flagship\'s flight and confidently announces our victory to the admiral.',"The enemy flagship has fled! Admiral, victory is ours! retains the explicit 提督 address and the more measured,courteous victory declaration. The stately wording distinguishes this voice from the colloquial2050 and excited2048. The sentence-final な does not require an artificial English tag or an invented relationship. Fleeing remains distinct from sinking or capture."),
}
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists()
 packet,context=read(PACKET),read(CONTEXT);preflight=read('work/analysis/aftermath_fled_context_v2538/next6_preflight.json');priorpath=Path(preflight['registered_manuscript']);prior={r['message_id']:r for r in read(priorpath)['records']}
 rows=[]
 for source in packet['records']:
  n=source['message_ID'];r=deepcopy(prior[n]);meaning,reason=NOTES[n]
  assert source['source_hex']==r['source_hex']and bytes.fromhex(source['current_hex'])==compiled(r)
  assert r['native_argument_count']==0 and not r['source_native_macros']
  r.update(file_path='/COMMON/MESFILE.DK4',consumer='original-53D44-role1-fled-victory-portrait',
   context='Complete independent victory report selected by original72368 mode2 ->53D44(role1,02117900). Source role1 may use its existing fallback or an assigned existing crew member;voice class selects the alternative. Read the flight report and victory announcement together as one emotional progression. These stored alternatives are not consecutive dialogue. Adjacent2045 is city defense and2052 powder fire,not a reply. No name arguments or native macros occur in these six records.',
   source_Japanese=source['clean_Japanese'],source_reference=source['source_reference'],current_reference=source['current_reference'],current_hex=source['current_hex'],current_stored_English=source['current_stored_English'],
   source_meaning=meaning,localization_note=reason,fresh_retained_wording_justification=reason,editorial_decision='retain-wording',speaker_metadata_corrected=False,
   review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
  rows.append(r)
 ROOT.mkdir(parents=True);supplement=ROOT/'source_context_and_voice_review.json'
 save(supplement,dict(records=[],all6_complete_clean_reports_freshly_read=True,flight_and_victory_facts_distinct_from_capture_sinking_or_death=True,
  explicit_Admiral_addresses_only2048_2049_2051=True,source2050_informal_ship_reference_and_realization_preserved=True,
  alternative_voices_not_a_six_line_conversation=True,source_prose_or_completion_credit_pending=True,full_goal_complete=False))
 doc=dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',consumer_layout_profile='battle-aftermath-portrait-postmacro-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/COMMON/MESFILE.DK4',
  source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
  source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proof=str(CONTEXT),native_context_proof_sha256=sha(CONTEXT.read_bytes()),
  fresh_ordinary_supplement=str(supplement),fresh_ordinary_supplement_sha256=sha(supplement.read_bytes()),prior_manuscript=str(priorpath),prior_manuscript_sha256=sha(priorpath.read_bytes()),
  revised_IDs=[],retained_count=6,speaker_metadata_corrections=[],formatting_review_pending=True,current_native_and_actual_family_reconciliation_pending=True,records=rows,full_goal_complete=False)
 save(DOC,doc);save(ROOT/'fresh_source_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),individual_new_glosses_and_retention_reasons=6,English_body_revisions=0,speaker_metadata_corrections=0,completion_pending_native_historical_registered_reconciliation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Six fresh complete flight/victory contextual retentions;native,historical and registered reconciliation pending.')
