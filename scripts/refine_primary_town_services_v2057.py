"""Refine evidence notes after source-bound native roles; prose stays frozen."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_refinement_v2057')
OLD=Path('translations/primary_town_services_contextual_editorial_manuscript_v1.json')
NEW=Path('translations/primary_town_services_contextual_editorial_manuscript_v2.json')
PROOF=Path('work/analysis/town_services_roles_v2056b/active_eight_requests_and_tribute_payment_direction.json')
if __name__=='__main__':
 assert not ROOT.exists()and not NEW.exists()
 doc=read(OLD);proof=read(PROOF)
 assert proof['tribute76_to82_is_incoming_to_current_player_not_a_payment_demand']and proof['barkeep_actual_name']=='Mihwa'
 for r in doc['records']:
  n=r['message_id']
  for k in('localization_note','finding','fresh_retained_wording_justification'):
   if k in r:
    r[k]=r[k].replace('Miwa','Mihwa').replace('Native payment-direction binding is still required before release.','Original clean-exact caller and three cloned native transfer tests confirm incoming tribute to the player.').replace('Payment direction remains a native-context release gate.','Original clean-exact caller and three cloned native transfer tests confirm incoming tribute to the player.')
  if 76<=n<=82:
   r['speaker']='Monthly tribute presenter,source voice variant'
   r['native_payment_direction_proof']=str(PROOF)
   r['localization_note']+=' Original native caller debits the donor and credits the player; this is incoming tribute. Controlled branch tests are offline,not visits to monthly tribute gameplay.'
   if r['editorial_decision']=='revise':r['finding']=r['localization_note']
   else:r['fresh_retained_wording_justification']=r['localization_note']
  if n in(49,54,55,56,57,58,59,60,61):r['native_argument_and_exchange_role_proof']=str(PROOF)
  r['native_consumer_actor_argument_currency_and_display_binding_pending']=True
  r['remaining_native_release_gates']='Complete glyphs,consumer-specific wrapping/bounds/pagination,cache repack and revised representative gameplay; anonymous conditional roles do not invent actor identity.'
 assert [r['english']for r in doc['records']]==[r['english']for r in read(OLD)['records']]
 assert len(doc['records'])==84 and all(not r['review']['formatting']for r in doc['records'])
 doc['supersedes_draft_notes_only']=str(OLD);doc['prior_manuscript_sha256']=sha(OLD.read_bytes())
 doc['native_roles_proof']=str(PROOF);doc['native_roles_proof_sha256']=sha(PROOF.read_bytes())
 doc['next_gates']=doc['next_gates'][1:]
 ROOT.mkdir(parents=True);save(NEW,doc)
 save(ROOT/'refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),native_roles_proof=str(PROOF),native_roles_proof_sha256=sha(PROOF.read_bytes()),all84_English_bodies_and_decisions_unchanged=True,formatting_approval=False,no_ROM_registry_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(records=84,revisions=42,retentions=42,notes_refined_only=True,formatting_pending=True))
