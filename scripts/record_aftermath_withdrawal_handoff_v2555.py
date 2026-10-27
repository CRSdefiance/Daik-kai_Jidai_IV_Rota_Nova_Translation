"""Checkpoint paired14 completion and next eight source-bound withdrawal reports."""
from pathlib import Path
OLD=Path('scripts/record_aftermath_defeat_handoff_v2547.py')
SUMMARY=(
 'V2555 prepares eight withdrawal reports2114-2121 with exact clean/current references and two storage neighbors. Current source tests bind208 original voice selections,one717F8 mode2 report prefix,three original7251C mode2 callsites and nine preserved town/ship position pairs through current original513D0 distance code. All nine reproduce original distance classes0/1/2 using declared CPU scratch arguments;no emulator position is changed. Mode2 issues one withdrawal report,without the mode0/1 flagship-loss follow-up. Current/clean/historical snapshot source spans are exact. Unassigned role1 in the source model retains Charles18 fallback2114;the later historical actual sample uses original assigned Charles18. All eight current paragraphs match the registered75-record battle_aftermath_editorial compiler/manuscript. Context extraction adds zero fresh reread,source/prose or completion credit. '
 'Next read each complete clean utterance with its voice and withdrawal situation. Preserve decisions/orders versus observations,urgency,personal pronouns,actual forms of address and tone. Do not invent defeat,victory,surrender,flagship destruction,safe escape,rank or kinship. These are voice alternatives,not a sequential exchange. Use original role1 speech53D44,parent53DB8/table+27C and228x64 portrait body,then current exact formatter/loader/full fonts,copies,ABI,bounds,first/final glyphs and focused risks. Historical proof work/analysis/aftermath_withdrawal_verified_v1293/actual_withdrawal_verification.json covers2114 after original town attack and distance withdrawal,with a single disclosed pre-battle location/room fixture and normal A return clearing battle/town IDs. Only2114 has individual historical activation;other seven require honest family coverage plus current offline tests. Reuse the completed whole4MiB fixture audit by hash rather than repeat it unnecessarily. Historical town/ship motion and native distance results are not current earned travel or recruitment. '
 'This goal turn reconciles14 abandonment/flagship-loss reports in V2552 and audits them in V2553. All14 retain English and speaker metadata with individual new clean glosses,complete-pair references,reasons,five gates and exact integrated references. Fourteen current role1 pipelines/full228x64 fonts,28 cold/warm copies,four preserved2016/2138 holds,14 corruption controls,exact inputs,natural HP and normal A through Game Over/title pass. All font and historical sheets were viewed. Five flooding reports and two preserved1973 escape holds add no duplicate credit. The initial historical verifier stopped before execution for one missing Python space;its successor passes. No new emulator run,current startup approval or earned progression is claimed. Fresh coverage is2019 reread /2019 integrated-reconciled /zero pending. Another124 historical completions need this pass:123 COMMON plus SC2B294R73. Historical completion2143(1498 revised,645 retained),source/prose2259 and incomplete COMMON116 remain unchanged. Registered cumulative V2284 remains493 batches/114 accepted layers with the same exactly reconstructable clean-input patch. ROM,runtime,geometry,registry,profile,manifest and patch are unchanged. V1492 remains promoted;canonical/clean inputs,all ROMs and earlier translations are preserved. Every never-reviewed storyline,shared shop/town dialogue,random scene and remaining player-facing prose remains in scope. Separate graphics/all18 plaques,SC3B109 classification and later older-record technical re-audit remain open. Full goal active;all jobs terminal.'
)
if __name__=='__main__':
 source=OLD.read_text();start=source.index('SUMMARY=(');end=source.index("if __name__=='__main__':",start);source=source[:start]+'SUMMARY='+repr(SUMMARY)+'\n'+source[end:]
 changes={
  'aftermath_defeat_source_handoff_v2547':'aftermath_withdrawal_source_handoff_v2555',
  '(2005,2005,0)':'(2019,2019,0)','aftermath_defeat_context_v2546':'aftermath_withdrawal_context_v2554',
  'all14_clean_current_context_catalog':'all8_clean_current_context_catalog','next14_preflight':'next8_preflight',
  "packet['selected_IDs']==[*range(2016,2022),*range(2138,2146)]":"packet['selected_IDs']==list(range(2114,2122))",
  "len(context['all416_original_selected_voice_choices'])==416":"len(context['all208_original_voice_selections'])==208",
  "len(context['all208_complete_original_voice_report_pairs'])==208":"len(context['current_original513D0_on9_historical_town_ship_positions'])==9",
  "p['all14_clean_current_registered_compilations_match']":"p['all8_clean_current_registered_compilations_match']",
  '# Current editorial handoff - V2544':'# Current editorial handoff - V2552',
  'work/analysis/aftermath_fled_completion_v2544/completion_receipt.json':'work/analysis/aftermath_defeat_completion_v2552/completion_receipt.json',
  'work/analysis/editorial_handoff_verification_v2545/verified_handoff.json':'work/analysis/editorial_handoff_verification_v2553/verified_handoff.json',
  'scripts/prepare_aftermath_defeat_context_v2546.py':'scripts/prepare_aftermath_withdrawal_context_v2554.py',
  'next_aftermath_defeat_contextual_source_packet_v2547':'next_aftermath_withdrawal_contextual_source_packet_v2555',
  "V2547 prepares14 connected defeat-report alternatives;zero added credit.":"V2555 prepares8 withdrawal report contexts;zero added credit.",
  'V2547-next14-paired-defeat-reports-source-only':'V2555-next8-withdrawal-reports-source-only',
  'progress:6 fresh flight/victory retentions reconciled;next14 paired report contexts prepared':'progress:14 paired defeat reports reconciled;next8 withdrawal contexts prepared',
  '## V2547: Next14 paired defeat reports;zero new credit':'## V2555: Next8 withdrawal reports;zero new credit',
  'translations/aftermath_fled_contextual_final_review_v1.json':'translations/aftermath_defeat_contextual_final_review_v1.json',
  'work/analysis/aftermath_fled_completion_v2544/remaining_historical_fresh_review_inventory.json':'work/analysis/aftermath_defeat_completion_v2552/remaining_historical_fresh_review_inventory.json',
  '# Current editorial handoff - V2547':'# Current editorial handoff - V2555',
  "checkpoint='V2547'":"checkpoint='V2555'",'completed_this_goal_turn=6':'completed_this_goal_turn=14','next_packet_records=14':'next_packet_records=8','fresh_integrated=2005':'fresh_integrated=2019','other_historical_fresh_reviews=138':'other_historical_fresh_reviews=124',
  'V2547:6 flight/victory reports reconciled;next14 paired defeat contexts prepared with zero extra credit.2005 integrated,138 historical fresh reviews remain.':'V2555:14 paired defeat reports reconciled;next8 withdrawal contexts prepared with zero extra credit.2019 integrated,124 historical fresh reviews remain.',
 }
 # The replacement summary already names new evidence; change only old code.
 head=source[:source.index("if __name__=='__main__':")];body=source[len(head):]
 for a,b in changes.items():
  if a in body:body=body.replace(a,b)
  else:assert a=='aftermath_defeat_source_handoff_v2547',a
 head=head.replace('aftermath_defeat_source_handoff_v2547','aftermath_withdrawal_source_handoff_v2555')
 exec(compile(head+body,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
