"""Locate17 uncredited legacy metadata references; do not expose or translate old English."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_metadata_lead_v7665c')
if __name__=='__main__':
    assert not ROOT.exists();p=Path('translations/maria_deep_route_v24.json');d=read(p);assert d['file_path']=='/data/SC3.DK4'
    rows=[dict(id=r['id'],file_path=d['file_path'],legacy_speaker_metadata=r.get('speaker'),legacy_context_metadata=r.get('context')) for r in d['records'] if r['id'].startswith('DK4_MES_B207_')]
    ledger=Path('translations/editorial_review_current_v1.json');l=read(ledger);keys={historical_key(r) for f in l['completed_editorial_families'] for r in f['records']}
    assert len(rows)==17 and not keys&{historical_key(r) for r in rows} and sum(r['legacy_speaker_metadata']=='Filippo' for r in rows)==8
    ROOT.mkdir(parents=True);save(ROOT/'17_uncredited_SC3B207_metadata_refs_clean_complete_exchange_review_pending.json',dict(metadata_path=str(p),metadata_sha256=sha(p.read_bytes()),records=rows,source_only_reference_lead_not_Japanese_gloss_ortranslation=True,old_English_bodies_not_exposed_orused_for_gloss_orlocalization=True,metadata_speaker_context_labels_unapproved_until_whole_clean_source_review=True,live_ledger_sha256=sha(ledger.read_bytes()),source_current_coverage_overlap=0,clean_full_command_inventory_gloss_source_consumer_name_entry_native_actual_andrelease_all_pending=True,not_an_exact_clone_orautomatic_B234_B246_B237_approval=True,next_action='Inventory the complete clean SC3 block207 andits neighbors/controls;write faithful full-exchange glosses before inspecting current English. Recheck file-qualified live coverage. Obtain own-current Maria captain3 context when needed;never borrow Lil/Rafael/Hodram route defaults.',new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
