"""Fresh five-report capture review;preserve each registered compiler/prose owner."""
from pathlib import Path
from copy import deepcopy
from importlib import import_module
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_native_plan_v1255 import compiled as original_compiled
from scripts.flagship_precision_native_plan_v1356 import compiled as precision_compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/flagship_capture_editorial_v2581');DOC=Path('translations/flagship_capture_contextual_editorial_manuscript_v1.json')
PACKET=Path('work/analysis/flagship_capture_context_v2578/all5_clean_current_context_catalog.json');CONTEXT=Path('work/analysis/flagship_capture_context_v2578/source_context_packet.json')

def compiled(row):
 return precision_compiled(row) if row['message_id']==2015 else original_compiled(row)

NOTES={
2011:('A formal report says all the sailors aboard the enemy flagship have been defeated and that the ship was captured.',"We've defeated the enemy flagship's entire crew and captured the ship! preserves both completed actions and confines entire crew to that flagship. Defeated renders 倒し without inventing that all sailors were killed. The ship refers naturally to the same enemy flagship,not every enemy vessel. We've supplies the collective actor implicit in this role1 report. No new rank,address or permanent fleet addition is asserted."),
2012:('An excited informal speaker addresses the admiral and reports defeating every sailor aboard the enemy flagship and taking the ship.',"Admiral! We beat the enemy flagship's whole crew and took their ship! preserves the actual 提督 address and lively announcement. Beat keeps the broad defeat sense of 倒して,not an invented death toll. Whole crew explicitly belongs to the enemy flagship. Took their ship naturally conveys 拿捕した without inventing capture of the whole fleet,extra spoils or a new relationship."),
2013:('A forceful familiar speaker reports defeating every sailor aboard the enemy flagship and capturing it.',"We beat the enemy flagship's whole crew! The ship's ours! naturally gives the completed crew defeat and emphatic capture announcement. The ship's ours expresses 拿捕したぞ in an idiomatic triumphant voice. It does not promise that the captured vessel is permanently added to the active fleet or that all its sailors died. Crew remains limited to this flagship;no Admiral address is added where none appears."),
2014:('An informal speaker says our side beat all the enemy flagship\'s sailors and captured the ship itself.',"We beat their flagship's whole crew and took the ship! keeps the informal みんなやっつけて and 船ごとつかまえたよ as natural spoken English. Their flagship anchors both the crew and the captured ship. Beat does not invent deaths or a medical condition,and took does not turn the report into a cargo award or capture of every enemy vessel. No age,rank or kinship is inferred from the casual ending."),
2015:('A courteous emphatic report says the enemy flagship was captured after all its sailors were defeated.',"We've captured the enemy flagship after defeating its entire crew! preserves the source's crew-defeat then capture progression in natural English. Its refers specifically to the named flagship,retaining the registered precision correction and avoiding the superseded entire enemy crew scope that could suggest the whole fleet. Defeating does not assert killing. The courteous emphasis needs no artificial archaic voice or new title. This is a fresh justified retention of an existing correction,not a new prose revision."),
}
if __name__=='__main__':
 assert not ROOT.exists() and not DOC.exists()
 packet,context=read(PACKET),read(CONTEXT);owners=packet['registered_prose_owner_bindings'];prior={};owner_by_ID={}
 for owner in owners:
  module,attribute=owner['compiler'].rsplit('.',1);own_compiler=getattr(import_module(module),attribute)
  for r in read(owner['registered_manuscript'])['records']:
   n=r['message_id']
   if n in owner['selected_IDs']:
    prior[n]=r;owner_by_ID[n]=owner;assert compiled(r)==own_compiler(r)
 assert set(prior)==set(NOTES) and context['actual_logical_member_ID']==16 and context['actual_physical_FirstMate_object']==0
 rows=[]
 for s in packet['records']:
  n=s['message_ID'];r=deepcopy(prior[n]);owner=owner_by_ID[n];meaning,reason=NOTES[n]
  assert s['source_hex']==r['source_hex'] and bytes.fromhex(s['current_hex'])==compiled(r) and r['native_argument_count']==0 and not r['source_native_macros']
  r.update(file_path='/COMMON/MESFILE.DK4',consumer='original-53D44-logical-role1-flagship-capture-portrait',registered_prose_owner=owner['stage'],registered_manuscript=owner['registered_manuscript'],registered_compiler=owner['compiler'],
   context='Complete independent capture report after original72368 mode0 calls53D44(role1,02117740),saved parent53DB8/table+27C. Other result modes are flagship defeat or flight/victory,not subsequent replies. Original82478 logical member selection is distinct from82428 physical assignment. Historical actual logical memberGerhard16 is selected with physical First Mate empty;voice1 -1 falls back to2011. Voices1/3/4 all fall back to2011. Read crew defeat and taking the flagship as one completed report;the later victory/reward/cargo/sailing flow provides context,not extra prose credit or a guaranteed retained fleet/cargo award.2011-2014 retain the original aftermath owner;2015 retains the later precision owner. Storage neighbors2010 flooding and2016 abandonment are separate families. No native name arguments or macros occur here.',
   source_Japanese=s['clean_Japanese'],source_reference=s['source_reference'],current_reference=s['current_reference'],current_hex=s['current_hex'],current_stored_English=s['current_stored_English'],source_meaning=meaning,localization_note=reason,fresh_retained_wording_justification=reason,
   editorial_decision='retain-wording',speaker_metadata_corrected=False,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
  rows.append(r)
 ROOT.mkdir(parents=True);supplement=ROOT/'complete_capture_scope_and_two_owner_review.json'
 save(supplement,dict(records=[],all5_clean_capture_reports_freshly_read_with_logical_role_and_complete_outcome_context=True,
  every_entire_or_whole_crew_phrase_confined_to_the_enemy_flagship=True,defeat_not_automatically_death=True,explicit_Admiral_only2012=True,
  registered2015_precision_wording_retained_not_counted_as_new_revision=True,physical_FirstMate_empty_does_not_erase_logical_Gerhard16_selection=True,
  later_reward_and_cargo_disposition_context_only_no_extra_credit=True,no_invented_full_enemy_fleet_capture_or_permanent_fleet_or_spoil_award=True,completion_pending_native_historical_and_two_owner_reconciliation=True,full_goal_complete=False))
 doc=dict(format='dk4-natural-dialogue-manuscript-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',consumer_layout_profile='battle-aftermath-portrait-postmacro-v1',review_gates=['source','context','localization','naturalness','formatting'],file_path='/COMMON/MESFILE.DK4',source_ROM_sha256=packet['source_ROM_sha256'],current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],current_ARM9_sha256=packet['current_ARM9_sha256'],current_COMMON_sha256=packet['current_COMMON_sha256'],
  source_context_packet=str(PACKET),source_context_packet_sha256=sha(PACKET.read_bytes()),native_context_proof=str(CONTEXT),native_context_proof_sha256=sha(CONTEXT.read_bytes()),fresh_ordinary_supplement=str(supplement),fresh_ordinary_supplement_sha256=sha(supplement.read_bytes()),registered_prose_owner_bindings=owners,prior_manuscripts=[dict(path=v['registered_manuscript'],sha256=v['registered_manuscript_sha256']) for v in owners],revised_IDs=[],retained_count=5,speaker_metadata_corrections=[],formatting_review_pending=True,current_native_and_actual_family_reconciliation_pending=True,records=rows,full_goal_complete=False)
 save(DOC,doc);save(ROOT/'fresh_source_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),individual_new_glosses_and_retention_reasons=5,registered_prose_owners=2,English_body_revisions=0,speaker_metadata_corrections=0,completion_pending_current_native_historical_two_owner_reconciliation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('Five fresh capture retentions;both registered prose owners preserved. Eight voice-fonts,history and two-owner reconciliation pending.')
