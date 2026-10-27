"""Fresh clean/current ordinary  prayer and strategy context;no duplicate credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_chapel_ordinary_v2407')
if __name__=='__main__':
 assert not ROOT.exists();oldpath=Path('work/analysis/battle_chapel_planning_v913/ordinary_context_and_terms.json');old=read(oldpath);rom=NdsImage.open('out/all_routes_combined_v2284_candidate.nds');clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'));rows=[]
 def ref(e):return dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text),table_offset=e.table_offset,record_index=e.record_index,start_in_record=e.start)
 prior={r['message_id']:r for r in old['records']};prior.pop(1409);prior[1406]=dict(message_id=1406,source_hex=jp[1406].text.hex(),current_text_hex=en[1406].text.hex())
 for r in prior.values():
  n=r['message_id'];assert jp[n].text.hex()==r['source_hex']and en[n].text.hex()==r['current_text_hex'];rows.append(dict(message_ID=n,clean_Japanese=jp[n].text.decode('cp932'),source_hex=jp[n].text.hex(),source_reference=ref(jp[n]),current_English=en[n].text.decode('cp932'),current_hex=en[n].text.hex(),current_reference=ref(en[n]),already_freshly_reviewed_context_only_no_duplicate_credit=True))
 assert rom.read_file('/__arm9__.bin')[old['native_ARM9_Schemes_caption_offset']:old['native_ARM9_Schemes_caption_offset']+8].hex()==old['native_ARM9_Schemes_caption_hex'];assert len(rows)==25
 ROOT.mkdir(parents=True);save(ROOT/'fresh_ordinary_supplement.json',dict(candidate='out/all_routes_combined_v2284_candidate.nds',candidate_sha256=sha(Path('out/all_routes_combined_v2284_candidate.nds').read_bytes()),records=rows,Chapel_Christian_register_grounded_in_explicit_Father_Son_Holy_Spirit_and_Bible_context=True,Claudio_nickname_context_is_clean1406_not_old_supplement1409=True,casualty_loss1652_explicit_contextual_inference_not_game_casualty_count=True,naval_battle_scope_not_all_sailing_preserved=True,schemes_caption_current_ARM9_hex=rom.read_file('/__arm9__.bin')[old['native_ARM9_Schemes_caption_offset']:old['native_ARM9_Schemes_caption_offset']+8].hex(),established_room_terms=old['established_room_terms'],established_term_documents={p:sha(Path(p).read_bytes())for p in old['established_term_documents']},prior_supplement=str(oldpath),prior_supplement_sha256=sha(oldpath.read_bytes()),no_new_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(context_records=len(rows),new_credit=0))
