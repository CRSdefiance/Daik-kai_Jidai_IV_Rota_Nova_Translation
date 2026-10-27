"""Six current ASCII-Faticia expansions supplement the1417 historical-model/stress inputs."""
from copy import deepcopy
from pathlib import Path
from types import FunctionType
import inspect
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_reinforcement_sniping_layout_v1030 as original
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_arrival_native_v792 import prepared
from scripts.duel_editorial_layout_v1155 import compiled
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_fonts_v2515')
BASEPROOF=Path('work/analysis/escape_fonts_v2513/native_font_proof.json')
PIPELINE=Path('work/analysis/escape_pipeline_v2514d/current_direct_pipeline.json')
if __name__=='__main__':
 assert not ROOT.exists()
 base=read(BASEPROOF);pipeline=read(PIPELINE)
 old=read('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')
 older={r['variant']['slot']:r['variant']['name_hex']for r in old['cases']if r['message_ID']==1951 and r['variant']['kind']=='source-compact-actor-getter20'}
 changed=[r for r in pipeline['all208_current_compact_names_with_current_immutable_labels']if r['name_hex']!=older[r['actor_slot']]]
 assert len(changed)==1 and changed[0]['actor_slot']==194 and changed[0]['name']=='Faticia'
 assert bytes.fromhex(older[194]).decode('cp932')=='Ｆaticia'
 rom=NdsImage.open(base['candidate']);arm=rom.read_file('/__arm9__.bin')
 assert sha(arm)==base['ARM9_sha256']==pipeline['ARM9_sha256']
 rows={r['message_id']:r for r in read(base['manuscript'])['records']}
 source=inspect.getsource(original.native_layout)
 for a,b in[('0x02053DB8','0x02053F40'),("struct.pack('<I',n)","struct.pack('<I',table)"),("struct.pack('<I',table))\n    call","struct.pack('<I',0))\n    call")]:
  assert source.count(a)==1;source=source.replace(a,b)
 env=dict(original.__dict__);exec(compile(source,__file__,'exec'),env);native_layout=env['native_layout']
 class CurrentFont:
  @staticmethod
  def open(path):
   assert str(path)=='out/all_routes_combined_v255_candidate.nds'
   return rom
 raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
 ROOT.mkdir(parents=True);cases=[];previews=[]
 for n in range(1951,1957):
  formatted,lines=native_layout(prepared(arm),compiled(rows[n]),n,b'Faticia',0x02117500)
  assert lines[0].startswith('Faticia,') and ' '.join(lines)==rows[n]['english'].replace('%s','Faticia')
  pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
  assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
  p=ROOT/f'ID{n}_current_ASCII_Faticia.png'
  Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(p)
  previews.append(dict(message_ID=n,path=str(p),sha256=sha(p.read_bytes()),lines=lines))
  cases.append(dict(message_ID=n,variant=dict(kind='current-immutable-compact-label',slot=194,name_hex=b'Faticia'.hex()),
   compiled_hex=compiled(rows[n]).hex(),formatted_hex=formatted.hex(),lines=lines,native_font_sha256=sha(pixels),
   direct_frame=[0x02053F40,0x274,0x02117500],all_current_ASCII_initial_F_and_final_letters_full_words_native_bounds_and_ABI_pass=True,
   whole228x64_current_native_and_independent_font_canvas_equal=True))
 sheet=Image.new('RGB',(936,462),'#263238');draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(previews):
  x,y=i%2*468,i//2*154;draw.text((x+5,y+3),'ID'+str(row['message_ID'])+' current ASCII Faticia',fill='white')
  sheet.paste(Image.open(row['path']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
 image=ROOT/'all6_current_ASCII_Faticia_names.png';sheet.save(image)
 combined=deepcopy(base)
 combined.update(cases=base['cases']+cases,complete_native_font_cases=1423,base_current1417_font_proof=str(BASEPROOF),
  base_current1417_font_proof_sha256=sha(BASEPROOF.read_bytes()),all6_current_ASCII_Faticia_supplement_cases=cases,
  all208_current_compact_name_labels=pipeline['all208_current_compact_names_with_current_immutable_labels'],
  exact_current_name_changes_from_older_compact_catalog=changed,
  original1417_inputs_include_historical_fullwidth_Faticia_as_additional_stress=True,
  all_current_names_in_captured_model_covered_with_current_immutable_label_bytes=True,
  current_native_source_pipeline=str(PIPELINE),current_native_source_pipeline_sha256=sha(PIPELINE.read_bytes()),
  current_source_pipeline_cases=13,all13_current_source_pipelines_and416_voice_choices_pass=True,
  review_sheets=base['review_sheets']+[dict(path=str(image),sha256=sha(image.read_bytes()))],visual_review_pending=True,
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
 save(ROOT/'native_font_proof.json',combined)
 print('1423 current native font cases:1417 source/stress variants plus6 current ASCII Faticia expansions;all current model labels covered.')
