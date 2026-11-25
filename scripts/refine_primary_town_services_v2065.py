"""Notes-only successor:exact display evidence and resolved tribute direction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_refinement_v2065')
OLD=Path('translations/primary_town_services_contextual_editorial_manuscript_v2.json')
NEW=Path('translations/primary_town_services_contextual_editorial_manuscript_v3.json')
DISPLAY=Path('work/analysis/town_services_consumer_audit_v2064b/actual_eight_consumers_four12pixel_rows_and_numeric_scope.json')
VOICES=Path('work/analysis/town_services_voice_tables_v2063/nine_clean_exact_voice_tables_and_all_native_catalog_selections.json')
SELECTOR=Path('work/analysis/town_services_selector_v2061/early_numeric_parent_dispatch_contract.json')
if __name__=='__main__':
 assert not ROOT.exists()and not NEW.exists();doc=read(OLD);display,voices=read(DISPLAY),read(VOICES)
 actual={r['native_ID']for r in display['actual_font_rows']};assert actual=={8,49,51,53,55,56,59,61}
 for r in doc['records']:
  n=r['message_id']
  for k in('localization_note','finding','fresh_retained_wording_justification'):
   if k in r:r[k]=r[k].replace('Native presenter/currency binding remains a release gate.','The native caller establishes incoming currency flow; unbound presenter identity stays anonymous.').replace('Exact native payment-direction confirmation remains pending.','Exact native caller and cloned transfer cases confirm incoming payment.')
  r.pop('native_consumer_actor_argument_currency_and_display_binding_pending',None)
  r['native_formatting_repacking_revised_gameplay_and_release_pending']=True
  if n in actual:r['actual_consumer_context']=dict(proof=str(DISPLAY),paper=[228,48],font=[6,12],line_step=12,original_current_gameplay_only=True)
  tables=[t for t in voices['tables']if n in t['source_members']]
  if tables:r['native_voice_table_bindings']=[dict(table=t['table'],members=t['source_members'],proof=str(VOICES),catalog_selection_not_conditional_scene_visit=True)for t in tables]
 assert [r['english']for r in doc['records']]==[r['english']for r in read(OLD)['records']]
 assert [r['editorial_decision']for r in doc['records']]==[r['editorial_decision']for r in read(OLD)['records']]
 doc['supersedes_draft_notes_only']=str(OLD);doc['prior_manuscript_sha256']=sha(OLD.read_bytes())
 doc['current_consumer_and_selector_evidence']={str(p):sha(p.read_bytes())for p in(DISPLAY,VOICES,SELECTOR)}
 doc['next_gates']=['Bind proposed formatter routing to actual numeric and nine voice-table source parents; retain unrelated IDs and the ritual64 exclusion.','Prove all84 complete glyphs,whole words,leading/trailing ink,bounds and pagination using the measured 228x48/6x12 consumers where applicable. Original monthly/table and literal-modal paths remain distinct.','Source-locked single8KiB COMMON reblock,all3668 copy preservation,opaque1484 prefix/carrier1931 protections.','Representative revised town/dialogue transitions.','Registered cumulative build and exact clean-input patch.']
 ROOT.mkdir(parents=True);save(NEW,doc)
 save(ROOT/'refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),all84_English_bodies_and_decisions_unchanged=True,all_formatting_gates_false=True,evidence=doc['current_consumer_and_selector_evidence'],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(manuscript=str(NEW),records=84,English_unchanged=True,formatting_pending=True))
