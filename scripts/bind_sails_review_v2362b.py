"""Bind the preserved fresh manuscript to the completed current terms proof."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.sails_boarding_layout_v881 import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/sails_boarding_editorial_v2362b')
if __name__=='__main__':
 assert not ROOT.exists();docpath=Path('translations/sails_boarding_contextual_editorial_manuscript_v1.json');doc=read(docpath);packet=read(doc['source_context_packet']);terms=Path('work/analysis/sails_terms_v2361c/current_terms.json');assert read(terms)['Half_Open_and_Full_Open_terms_source_bound'];assert len(doc['records'])==doc['retained_count']==24 and doc['speaker_metadata_corrections']==[1532,1544]
 for row,source in zip(doc['records'],packet['records'],strict=True):
  assert row['message_id']==source['message_ID']and row['source_hex']==source['source_hex']and compiled(row)==bytes.fromhex(source['current_hex'])and row['source_meaning']and row['fresh_retained_wording_justification'];assert all(row['review'][k]for k in('source','context','localization','naturalness'))and not row['review']['formatting']
 ROOT.mkdir(parents=True);save(ROOT/'preserved_source_and_terms_binding.json',dict(manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),all24_fresh_glosses_reasons_and_source_current_references_preserved=True,current_terms_proof=str(terms),current_terms_proof_sha256=sha(terms.read_bytes()),original_review_producer='scripts/review_sails_boarding_v2362.py',original_review_producer_sha256=sha(Path('scripts/review_sails_boarding_v2362.py').read_bytes()),reason='The fresh manuscript and source-review receipt were saved before an ancillary terms-proof lookup failed. Preserve them and bind the completed2361c current terms without rerunning or overwriting the authoring producer.',no_editorial_completion_credit_until_all_remaining_checks=True,no_English_or_ROM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(fresh_source_records_preserved=24,current_terms_bound=True,formatting_pending=True))
