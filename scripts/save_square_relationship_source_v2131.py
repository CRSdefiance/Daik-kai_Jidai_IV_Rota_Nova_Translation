"""Save exact clean story context for the Hayreddin relationship decision."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import export_mesfile_rows
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/square_relationship_source_v2131')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 rom=NdsImage.open('work/clean.nds');packets=[]
 for path in('/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4','/COMMON/MESFILE.DK4'):
  data=rom.read_file(path);rows=export_mesfile_rows(data,path,include_non_japanese=True);hits=[]
  for i,r in enumerate(rows):
   if any(w in r['japanese']for w in('ハイレディン','バルバロ','義理の父','養父','義父','妻の父')):
    hits.append(dict(id=r['id'],Japanese=r['japanese'],neighbors=[dict(id=q['id'],Japanese=q['japanese'])for q in rows[max(0,i-2):i+3]]))
  packets.append(dict(file_path=path,source_file_sha256=sha(data),hits=hits))
 save(ROOT/'clean_story_relationship_context.json',dict(source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),files=packets,finite_literal_name_and_relationship_search_not_proof_of_absence_of_every_paraphrase=True,decision='The reviewed source establishes a paternal tie but does not substantiate the previous narrower father-in-law wording. New wording the man he called his father avoids choosing a marriage,adoption or upbringing story.',native_message718_reference='work/analysis/market_context_source_v2108/market656_764_clean_current_context_catalog.json',lexical_reference=dict(title='Shogakukan Digital Daijisen: gifu',url='https://kotobank.jp/word/%E7%BE%A9%E7%88%B6-475463',supports_multiple_non_birth_paternal_ties=True,not_character_biographical_evidence=True),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(files=len(packets),hits=sum(len(p['hits'])for p in packets),no_specific_marriage_or_adoption_asserted=True))
