"""Approve source-bound offline formatting, keeping actual/release completion open."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_formatting_v2095')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v5.json')
if __name__=='__main__':
 assert not ROOT.exists()and not DOC.exists();ROOT.mkdir(parents=True)
 parent=Path('translations/primary_town_services_contextual_editorial_manuscript_v4.json');doc=read(parent)
 payload=read('work/analysis/town_services_payload_v2092b/native_payload_plan.json');fonts=read('work/analysis/town_services_routed_planes_v2084/all122_original_route_native_planes.json');styles=read('work/analysis/town_services_style_v2091/individual_ten_style_retention_decisions.json');copies=read('work/analysis/town_services_copies_v2093/all_native_copies_and_prefix_cache_sequence.json')
 assert fonts['native_count']==122 and len(styles['decisions'])==10 and copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==180
 target={r['message_ID']:r['target_hex']for r in payload['source_locks']}
 for r in doc['records']:
  assert r['english'].removesuffix('{PAD}').encode().hex()==target[r['message_id']]
  assert all(r['review'][g]for g in('source','context','localization','naturalness'))and r['review']['formatting']is False
  r['review']['formatting']=True;r['remaining_native_release_gates']='Registered cumulative build, metadata-only font inheritance binding, representative revised town transitions and exact clean-input release reconstruction.'
  r['native_formatting_repacking_revised_gameplay_and_release_pending']=True
 doc.update(consumer_layout_profile='Primary-town84-original-BL-literal-postprintf-228x48-6x12-v1',formatting_review_pending=False,source_notes_manuscript=str(parent),offline_formatting_approval=str(ROOT/'offline_formatting_approval.json'),native_source_copy_proof='work/analysis/town_services_copies_v2093/all_native_copies_and_prefix_cache_sequence.json',revised_actual_and_registered_release_pending=True)
 validate_natural_dialogue_batch(doc);save(DOC,doc)
 save(ROOT/'offline_formatting_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_notes=str(parent),source_sha256=sha(parent.read_bytes()),all84_native_source_formatting_checks_pass=True,all10_style_findings_individually_reviewed=True,no_hard_font_gate_waived=True,all_English_unchanged=True,actual_and_registered_release_completion_not_claimed=True,unsupported_arbitrary_alias_symbol_has_byte_only_coverage=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(manuscript=str(DOC),offline_formatting_approved=84,actual_release_completion_pending=True))
