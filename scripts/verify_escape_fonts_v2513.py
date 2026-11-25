"""Current corrected direct-frame printf/wrap and1417 full native font cases."""
import inspect,struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_contextual_spritsail_v1 import current_entries
from dk4tool.rom.nds import NdsImage
from scripts import probe_reinforcement_sniping_layout_v1030 as original
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_arrival_native_v792 import prepared
from scripts.duel_editorial_layout_v1155 import compiled,ESCAPE_IDS
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_fonts_v2513')
ROM=Path('out/all_routes_combined_v2284_candidate.nds')
MANUSCRIPT=Path('translations/escape_contextual_editorial_manuscript_v1.json')
REFERENCE=Path('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')

if __name__=='__main__':
 assert not ROOT.exists()
 rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
 doc=read(MANUSCRIPT);rows={r['message_id']:r for r in doc['records']};entries=current_entries(common,arm)
 assert sha(ROM.read_bytes())==doc['current_ROM_sha256'] and sha(arm)==doc['current_ARM9_sha256']
 assert all(entries[n].text==compiled(r)==bytes.fromhex(r['current_hex'])for n,r in rows.items())
 source=inspect.getsource(original.native_layout)
 replacements=[('0x02053DB8','0x02053F40'),("struct.pack('<I',n)","struct.pack('<I',table)"),("struct.pack('<I',table))\n    call","struct.pack('<I',0))\n    call")]
 for old,new in replacements:
  assert source.count(old)==1
  source=source.replace(old,new)
 env=dict(original.__dict__);exec(compile(source,__file__,'exec'),env);native_layout=env['native_layout']
 class CurrentFont:
  @staticmethod
  def open(path):
   assert str(path)=='out/all_routes_combined_v255_candidate.nds'
   return rom
 raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
 reference=read(REFERENCE);assert len(reference['cases'])==1417
 ROOT.mkdir(parents=True)
 cases=[];previews=[];representative=[];cache={};findings=[];source_findings=read('work/analysis/duel_escape_fonts_v1157/native_escape_fonts.json')['findings_requiring_review'];finding_indices={r['case_index']for r in source_findings}
 for i,prior in enumerate(reference['cases']):
  if i%32==0:cpu=prepared(arm)
  n=prior['message_ID'];row=rows[n];text=compiled(row);assert text.hex()==prior['compiled_hex']
  variant=prior['variant'];argument=bytes.fromhex(variant['name_hex'])if variant else None
  table=0x02117500 if n<1973 else 0x02117620
  formatted,lines=native_layout(cpu,text,n,argument,table)
  assert formatted.hex()==prior['formatted_hex'] and lines==prior['lines']
  expected=row['english'].replace('%s',argument.decode('cp932'))if argument else row['english']
  assert ' '.join(lines)==expected
  if formatted not in cache:
   pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
   assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
   cache[formatted]=pixels
  pixels=cache[formatted];assert sha(pixels)==prior['native_font_sha256']
  case=dict(message_ID=n,variant=variant,compiled_hex=text.hex(),formatted_hex=formatted.hex(),lines=lines,
   native_font_sha256=sha(pixels),direct_frame=[0x02053F40,0x274,table],
   current_original_printf_wrap_full_ABI_complete228x64_native_independent_font_and_guards_pass=True,
   all_leading_trailing_name_bytes_and_words_and_uniform_x6_margin_pass=True)
  cases.append(case)
  if i in finding_indices:
   assert n==1954 and len(lines)==2 and lines[0].endswith('Come on,') and lines[1]=='lads, cover them!'
   findings.append(dict(case_index=i,message_ID=n,variant=variant,lines=lines,native_font_sha256=sha(pixels),
    disposition='fresh-contextual-retention',reason='On is part of the complete interjection Come on, followed by a comma and the vocative lads. The natural spoken pause is readable across this exact generated boundary. It is not a preposition missing an object,a broken word or an orphan row. Complete glyphs and native bounds pass. This decision covers only these exact1954 variants.'))
  if not any(r['message_ID']==n for r in previews):
   p=ROOT/f'ID{n}_complete_current_direct_font.png'
   Image.frombytes('L',(228,64),bytes(0 if v else 255 for v in pixels)).save(p)
   preview=dict(message_ID=n,path=str(p),sha256=sha(p.read_bytes()),lines=lines)
   previews.append(preview);representative.append(case)
  if (i+1)%235==0:print(i+1,'current direct-frame full font/name cases pass',flush=True)
 assert len(cases)==1417 and len(representative)==13 and len(findings)==161
 assert [r['message_ID']for r in representative]==list(ESCAPE_IDS)
 sheet=Image.new('RGB',(936,1078),'#263238');draw=ImageDraw.Draw(sheet)
 for i,row in enumerate(previews):
  x,y=i%2*468,i//2*154
  draw.text((x+5,y+3),'ID'+str(row['message_ID'])+' current direct-speech font',fill='white')
  sheet.paste(Image.open(row['path']).resize((456,128),Image.Resampling.NEAREST),(x+5,y+22))
 p=ROOT/'all13_current_corrected_direct_escape_fonts.png';sheet.save(p)
 loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in ESCAPE_IDS]
 assert len(copies)==26
 save(ROOT/'native_font_proof.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),COMMON_sha256=sha(common),
  manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),cases=cases,complete_native_font_cases=1417,
  all13_complete_native_cases=representative,all26_native_cold_warm_copies=copies,native_file_IO_explicit_host_contract=True,
  all13_source_numeric_selection_complete_ABI_words_and_visible_ink_pass=True,current_parent_projection_controls=0,
  current_modal_font_consumers_no_Deck_parent_projection_claim=True,all1417_current_corrected_direct_frame_font_cases_reexecuted=True,
  all161_exact_Come_on_boundary_findings_freshly_reviewed=findings,no_other_word_or_missing_glyph_waiver=True,
  corrected_original_parent=0x02053F40,corrected_original_table_stack_offset=0x274,
  reference=str(REFERENCE),reference_sha256=sha(REFERENCE.read_bytes()),all1417_current_formatted_bytes_lines_and_font_planes_equal_corrected_reference=True,
  effective_native_layout_sha256=sha(source.encode()),unique_native_font_planes=len(cache),
  review_sheets=[dict(path=str(p),sha256=sha(p.read_bytes()))],visual_review_pending=True,
  scope='Current isolated CPU direct-frame printf,post-macro wrapper and full native font tests.208 compact model labels and27 legal-name stress inputs retain original argument bytes;NPC inputs also provide layout stress and are not all claimed duel participants. No current emulator run or live text/name injection.',
  producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
 print('1417 current corrected direct-frame font cases,161 exact contextual boundaries and26 cold/warm copies pass;current source pipeline and historical binding remain separate.',flush=True)
