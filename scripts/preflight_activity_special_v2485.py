"""Bind next17 clean/current payloads to their registered formatter;zero credit."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.activity_special_layout_v986b import compiled
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/activity_special_preflight_v2485')
if __name__=='__main__':
 assert not ROOT.exists();packetpath=Path('work/analysis/activity_special_context_source_v2484/all17_clean_current_context_catalog.json');packet=read(packetpath);ledger=read('translations/editorial_review_current_v1.json');rompath=Path(ledger['current_integrated_candidate']['path']);manifest=read(rompath.with_suffix('.manifest.json'));stage=manifest['relocations']['/COMMON/MESFILE.DK4']['activity_special_editorial'];configpath=Path(stage['release_config']);config=read(configpath);docpath=Path(config['manuscript']);doc=read(docpath);old={r['message_id']:r for r in doc['records']};ids=list(range(1872,1889))
 assert sha(rompath.read_bytes())==packet['current_ROM_sha256']==manifest['candidate_sha256']and sha(configpath.read_bytes())==stage['release_config_sha256']and sha(docpath.read_bytes())==config['manuscript_sha256']
 assert sorted(old)==packet['selected_IDs']==stage['proof']['reviewed_native_IDs']==ids
 for row in packet['records']:n=row['message_ID'];assert row['source_hex']==old[n]['source_hex']and bytes.fromhex(row['current_hex'])==compiled(old[n])
 f=ledger['contextual_story_natural_dialogue_pass_v1871'];assert f['fresh_pass_records_integrated']==1896 and not{('/COMMON/MESFILE.DK4',f'COMMON_MESSAGE_{n}')for n in ids}&{(r['file_path'],r['id'])for r in f['record_keys']}
 assert struct.unpack_from('<2I',NdsImage.open(rompath).read_file('/__arm9__.bin'),0x1147B8)==(216,36)
 ROOT.mkdir(parents=True);save(ROOT/'next17_preflight.json',dict(packet=str(packetpath),packet_sha256=sha(packetpath.read_bytes()),registered_manuscript=str(docpath),registered_manuscript_sha256=sha(docpath.read_bytes()),registered_config=str(configpath),registered_config_sha256=sha(configpath.read_bytes()),reviewed_native_IDs=ids,historical_changed_records=stage['proof']['changed_records'],all17_complete_clean_current_compiled_payloads_match=True,registered_activity_special986b_compiler_used=True,existing_native_parent_crop=[216,36],fresh_credit=0,current_native_context_and_editorial_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(next_records=17,new_credit=0,current_native_context_and_review_pending=True))
