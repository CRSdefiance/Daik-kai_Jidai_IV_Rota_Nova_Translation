"""Fresh clean/current ordinary pig-care and food context;no duplicate credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_cooking_ordinary_v2398c')
if __name__=='__main__':
 assert not ROOT.exists();oldpath=Path('work/analysis/battle_cooking_livestock_v907/ordinary_context_supplement.json');old=read(oldpath);rom=NdsImage.open('out/all_routes_combined_v2284_candidate.nds');clean=NdsImage.open('work/clean.nds');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'));en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'));rows=[]
 def ref(e):return dict(block=e.block,offset=e.block_offset,copy_end=e.copy_end,bytes=len(e.text),table_offset=e.table_offset,record_index=e.record_index,start_in_record=e.start)
 for r in old['records']:
  n=r['message_id'];assert jp[n].text.hex()==r['source_hex']and en[n].text.hex()==r['current_text_hex'];rows.append(dict(message_ID=n,clean_Japanese=jp[n].text.decode('cp932'),source_hex=jp[n].text.hex(),source_reference=ref(jp[n]),current_English=en[n].text.decode('cp932'),current_hex=en[n].text.hex(),current_reference=ref(en[n]),already_freshly_reviewed_context_only_no_duplicate_credit=True))
 ROOT.mkdir(parents=True);save(ROOT/'fresh_ordinary_supplement.json',dict(candidate='out/all_routes_combined_v2284_candidate.nds',candidate_sha256=sha(Path('out/all_routes_combined_v2284_candidate.nds').read_bytes()),records=rows,pig_grooming_context_supported_by_clean1424_and1636=True,Emilio_first_person_pig_protest_supported_by_clean1429_and1639=True,Lil1643_pig_panic_subject_is_explicit_contextual_inference_from_assigned_pig_care_and_cannon_fright_not_new_fact=True,food_boasts_and_animal_reassurance_not_verified_mechanical_effects=True,prior_supplement=str(oldpath),prior_supplement_sha256=sha(oldpath.read_bytes()),no_new_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(context_records=len(rows),new_credit=0))
