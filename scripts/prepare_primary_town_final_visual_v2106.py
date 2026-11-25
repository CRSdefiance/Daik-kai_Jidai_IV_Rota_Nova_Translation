"""Contact sheets covering every corrected native page, including name stress."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_final_visual_v2106')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 proof=Path('work/analysis/town_services_actual_pitch_v2103b/all155_correct_pitch_native_pages.json');doc=read(proof);tiles=[(r,p)for r in doc['cases']for p in r['pages']];assert len(tiles)==156
 sheets=[]
 for start in range(0,len(tiles),20):
  subset=tiles[start:start+20];sheet=Image.new('RGB',(936,120*((len(subset)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
  for j,(r,p)in enumerate(subset):
   x,y=j%2*468,j//2*120;label=str(r['message_ID'])+' '+str(r.get('supplied_arguments',r.get('name_hex')))+' / '+str(p['input_offset']);draw.text((x+5,y+3),label,fill='white')
   assert sha(Path(p['preview']).read_bytes())==p['preview_sha256']
   with Image.open(p['preview'])as image:sheet.paste(image.resize((456,96),Image.Resampling.NEAREST),(x+5,y+22))
  path=ROOT/f'all_pages_sheet_{start//20:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),native_page_count=len(subset)))
 save(ROOT/'all_native_review_sheets.json',dict(source_proof=str(proof),source_proof_sha256=sha(proof.read_bytes()),sheets=sheets,native_pages=156,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print(dict(sheets=len(sheets),native_pages=156))
