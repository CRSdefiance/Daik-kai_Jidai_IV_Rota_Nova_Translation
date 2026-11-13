"""Fresh clean/current hobby references for battle reactions;no extra record credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_hobbies_v2382')
if __name__=='__main__':
 assert not ROOT.exists();rompath=Path('out/all_routes_combined_v2284_candidate.nds');rom=NdsImage.open(rompath);clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'));oldpath=Path('work/analysis/battle_personal_v891/hobby_and_term_context.json');old=read(oldpath);rows=[]
 def ref(e):return dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text),record_index=e.record_index,table_offset=e.table_offset,start_in_record=e.start)
 for r in old['ordinary_hobby_source_controls']:
  n=r['message_id'];assert jp[n].text.hex()==r['source_hex'];rows.append(dict(message_ID=n,clean_Japanese=jp[n].text.decode('cp932'),source_hex=jp[n].text.hex(),current_English=en[n].text.decode('cp932'),current_hex=en[n].text.hex(),source_reference=ref(jp[n]),current_reference=ref(en[n]),context_only_no_duplicate_fresh_credit=True))
 title='海戦事典'.encode('cp932');matches=[e.message_id for e in jp if title in e.text];assert matches==[1575]
 ROOT.mkdir(parents=True);save(ROOT/'fresh_hobby_context.json',dict(candidate=str(rompath),candidate_sha256=sha(rompath.read_bytes()),source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),ordinary_hobby_controls=rows,book_source_title='海戦事典',literal_title_matches=matches,English_Naval_Warfare_Encyclopedia_is_translation_not_external_official_title_claim=True,Maria_ippuku_is_break_no_smoking_or_specific_beverage_proven=True,Jam_rod_is_fishing_rod_from_source1372=True,Al_sharp_training_breaths_are_explicit_contextual_inference_from_source1378_fist_training=True,Carlo_nodding_off_direction_is_explicit_in_both_ordinary_and_battle_sources=True,Sera_flowers_retain_her_simple_voice_without_caricature=True,prior_context=str(oldpath),prior_context_sha256=sha(oldpath.read_bytes()),all_ordinary_references_context_only_no_duplicate_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(fresh_source_hobby_references=len(rows),title_match=[1575],extra_credit=0))
