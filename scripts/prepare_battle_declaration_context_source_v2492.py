"""Next22 clean/current complete utterances and neighbors;zero editorial credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('scripts/prepare_tavern_exchange_source_v2182.py')
if __name__=='__main__':
 source=OLD.read_text();changes={'town_trade_port_contextual_reference_v1':'refit_contextual_spritsail_v1','tavern_exchange_source_v2182':'battle_declaration_context_source_v2492','IDS=list(range(820,883))':'IDS=list(range(1889,1911))','==63':'==22','all63_clean_current_context_catalog':'all22_clean_current_context_catalog'}
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
 root=env['ROOT'];p=read(root/'all22_clean_current_context_catalog.json');rows=[]
 for r in p['records']+p['neighbors']:
  rows.append(dict(message_id=r['message_ID'],source_Japanese=r['clean_Japanese'],source_hex=r['source_hex'],source_reference=r['source_reference'],current_English=r['current_stored_English'],current_text_hex=r['current_hex'],current_reference=r['current_reference'],selected_next_inventory=r['selected'],source_argument_s_count=bytes.fromhex(r['source_hex']).count(b'%s')))
 save(root/'source_inventory.json',dict(candidate=p['current_ROM'],candidate_sha256=p['current_ROM_sha256'],ARM9_sha256=p['current_ARM9_sha256'],COMMON_sha256=p['current_COMMON_sha256'],records_and_neighbors=sorted(rows,key=lambda r:r['message_id']),completed_entries_added=0,source_prose_reviews_added=0,full_goal_complete=False))
 save(root/'extractor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),no_new_editorial_credit=True,full_goal_complete=False))
