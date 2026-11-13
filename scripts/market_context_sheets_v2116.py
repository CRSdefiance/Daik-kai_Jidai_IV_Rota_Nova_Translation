"""Contact sheets for every native market page, with exact IDs and arguments."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/market_context_visual_v2116')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 proof=Path('work/analysis/market_context_pages_v2115/all18_market_native_pages.json');doc=read(proof)
 tiles=[(r,p)for r in doc['cases']for p in r['pages']];sheets=[]
 for start in range(0,len(tiles),12):
  subset=tiles[start:start+12];sheet=Image.new('RGB',(936,128*((len(subset)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
  for j,(r,p)in enumerate(subset):
   x,y=j%2*468,j//2*128;label=f"COMMON {r['message_ID']} {r['supplied_arguments']} offset {p['input_offset']}"
   draw.text((x+5,y+3),label,fill='white');sheet.paste(Image.open(p['preview']).resize((456,96),Image.Resampling.NEAREST),(x+5,y+24))
  path=ROOT/f'all_pages_{start//12:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
 save(ROOT/'all_native_pages_index.json',dict(proof=str(proof),proof_sha256=sha(proof.read_bytes()),pages=len(tiles),sheets=sheets,actual_gameplay=False,visual_review_pending=True,full_goal_complete=False))
 print(dict(pages=len(tiles),sheets=sheets))
