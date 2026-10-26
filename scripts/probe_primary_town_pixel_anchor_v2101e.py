"""Calibrate native-font ink placement against the already-observed town hold."""
import inspect
from pathlib import Path
from PIL import Image
from scripts.verify_common_alignment_native_v257 import raster as original
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/town_services_pixel_anchor_v2101e')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True)
 cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_font_actual_v2060_V2047');obs=read(cap/'common_observer/requests.json');row=next(r for r in obs['rows']if r['source_request']['ID']==49)
 rom=NdsImage.open('out/all_routes_combined_v2047_candidate.nds');arm=rom.read_file('/__arm9__.bin')
 class Font:
  @staticmethod
  def open(path):return rom
 source=inspect.getsource(original).replace('struct.pack("<2I", 6, 16)','struct.pack("<2I", 6, 16)');env={**original.__globals__,'NdsImage':Font};exec(source,env)
 plane=env['raster'](arm,bytes.fromhex(row['text_hex']),0x01FFCE40-0x02000000,size=(228,48),instruction_limit=2000000);ink={(i%228,i//228)for i,v in enumerate(plane)if v==1}
 image_path=cap/'frame_031400_cold_boot.png';image=Image.open(image_path).convert('RGB');pixels={(x,y)for y in range(288,365)for x in range(256)if image.getpixel((x,y))==(0,8,0)};matches=[]
 for dy in range(290,311):
  for dx in range(29):
   actual={(x,y)for x,y in pixels if dx<=x<dx+228 and dy<=y<dy+48};expected={(x+dx,y+dy)for x,y in ink}
   if actual==expected:matches.append([dx,dy])
 print(dict(matches=matches,native_ink_pixels=len(ink),actual_ink_pixels=len(pixels)))
 save(ROOT/'original49_exact_native_ink_anchor.json',dict(matches=matches,native_ink_pixels=len(ink),source_font_row=row,source_capture=str(image_path),source_capture_sha256=sha(image_path.read_bytes()),native_plane_sha256=sha(plane),native_font_color=[0,8,0],producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 assert len(matches)==1
