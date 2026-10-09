"""Natural English Rota Nova title copies with original scenes and Latin ornament."""
import argparse
import copy
import json
import zlib
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
 CANONICAL_BASELINE_SHA256,
 RELEASE_STACK_PATH,
 accepted_batch_paths,
 apply_pxl_indexed_region_batch,
 load_release_stack,
 resolve_release_batches,
 rom_files,
 verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save

BASE=Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR=Path('out/all_routes_combined_v174_candidate.nds')
PRIOR_SHA='15df894e0661552af6d1d3f279f84601eb4b9802c0571d8adac07e32398ab089'
CANDIDATE=Path('out/all_routes_combined_v175_candidate.nds')
PROFILE='all-routes-unified-v175'
REPRO=Path('work/analysis/v174_pxl_art_builder_reproduction.nds')
OUT=Path('work/qa/rota_titles_v175')
PROOF=Path('work/analysis/rota_titles_v175_saved_proof.json')
FONT=Path('C:/Windows/Fonts/timesbd.ttf')
SPECS=[
 {'path': '/_pxl/logo.pxl','name': 'logo','background': None,'main': [4,50,252,101],'caption': [151,121,201,133],'latin_offset': [0,84]},
 {'path': '/_pxl/title/title03.pxl','name': 'title03','background': '/_pxl/title/title00.pxl','main': [4,8,252,57],'caption': [150,81,198,90],'latin_offset': [-2,41]},
 {'path': '/_pxl/title/title05.pxl','name': 'title05','background': '/_pxl/title/title04.pxl','main': [4,47,252,96],'caption': [150,120,198,129],'latin_offset': [-2,80]},
]


def batch_path(spec):return Path('translations/rota_title_'+spec['name']+'_art_v1.json')


@lru_cache(maxsize=1)
def sources():
 if sha(BASE.read_bytes())!=CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes())!=PRIOR_SHA:raise ValueError('Exact canonical and V174 required')
 base,prior,clean=[NdsImage.open(p) for p in (BASE,PRIOR,Path('work/clean.nds'))]
 for spec in SPECS:
  paths=[spec['path']]+([spec['background']] if spec['background'] else [])
  for path in paths:
   if not base.read_file(path)==prior.read_file(path)==clean.read_file(path):raise ValueError('Untouched original title/background required')
 return base,prior


def nearest(palette,rgb):return min(range(len(palette)),key=lambda i:sum((a-b)**2 for a,b in zip(palette[i][:3],rgb,strict=True)))


def regions(spec):
 base,_=sources();p=PxlImage.from_bytes(base.read_file(spec['path']))
 bg=PxlImage.from_bytes(base.read_file(spec['background'])) if spec['background'] else None
 mapping=[nearest(p.palette,c[:3]) for c in bg.palette] if bg else None
 latin=FlsArchive(base.read_file('/FLS/M28.fls')).texture(5)
 ox,oy=spec['latin_offset'];cases=[];payloads=[]
 for kind in ('main','caption'):
  box=spec[kind];x0,y0,x1,y1=box;w,h=x1-x0,y1-y0
  pixels=bytearray(p.indices[y*256+x] for y in range(y0,y1) for x in range(x0,x1))
  preserved=set()
  if kind=='main':
   for y in range(y0,y1):
    for x in range(x0,x1):
     i=(y-y0)*w+x-x0;lx,ly=x-ox,y-oy
     r,g,b,_=p.palette[p.indices[y*256+x]]
     latin_overlap=0<=lx<256 and 0<=ly<64 and latin.indices[ly*256+lx]!=0 and not (b>r+25 and b>g+20)
     if latin_overlap:preserved.add(i)
     else:pixels[i]=mapping[bg.indices[y*256+x]] if bg else nearest(p.palette,(0,0,0))
   font=ImageFont.truetype(str(FONT),size=25);lines=['UNCHARTED','WATERS IV'];draw_h=42
  else:
   # Caption owns only the blue phonetic lettering, not surrounding Latin-gold pixels.
   for y in range(y0,y1):
    for x in range(x0,x1):
     i=(y-y0)*w+x-x0;r,g,b,_=p.palette[p.indices[y*256+x]]
     if b>r+2 and b>g+2:
      pixels[i]=mapping[bg.indices[y*256+x]] if bg else nearest(p.palette,(255,255,255))
   font=ImageFont.truetype(str(FONT),size=9);lines=['Rota Nova'];draw_h=h
  mask=Image.new('L',(w,h));d=ImageDraw.Draw(mask);bs=[font.getbbox(s) for s in lines];hs=[b[3]-b[1] for b in bs];gap=2
  total=sum(hs)+gap*(len(lines)-1);y=(draw_h-total)//2;line_cases=[]
  for text,b,height in zip(lines,bs,hs,strict=True):
   width=b[2]-b[0];x=(w-width)//2
   if x<0 or y<0 or y+height>draw_h:raise ValueError('Complete title/caption cannot fit')
   d.text((x-b[0],y-b[1]),text,font=font,fill=255)
   line_cases.append({'text': text,'full_glyph_box': [x+x0,y+y0,x+x0+width,y+y0+height]})
   y+=height+gap
  if kind=='main':
   outline=mask.filter(ImageFilter.MaxFilter(3));white=nearest(p.palette,(255,255,255));dark=nearest(p.palette,(35,40,65))
   for y in range(h):
    for x in range(w):
     i=y*w+x;ink=mask.getpixel((x,y))>=128
     if i in preserved:
      if ink:raise ValueError('Complete English glyph overlaps original Latin ornament')
      continue
     if x>=1 and y>=1 and outline.getpixel((x-1,y-1))>=128:pixels[i]=dark
     if outline.getpixel((x,y))>=128:pixels[i]=white
     if ink:pixels[i]=nearest(p.palette,(15,50,max(115,235-(y%22)*6)))
  else:
   blue=nearest(p.palette,(40,60,205))
   for i,v in enumerate(mask.tobytes()):
    if v>=128:pixels[i]=blue
  cases.append({'kind': kind,'box': box,'lines': line_cases,'font_size': 25 if kind=='main' else 9,
        'font_sha256': sha(FONT.read_bytes()),'mask_sha256': sha(mask.tobytes()),'preserved_latin_ornament_indices': len(preserved),
        'background_source': spec['background'],'background_source_sha256': sha(base.read_file(spec['background'])) if bg else None})
  payloads.append(bytes(pixels))
 return payloads,cases


def targets():
 base,_=sources();return {spec['path']:apply_pxl_indexed_region_batch(batch_path(spec),base.read_file(spec['path']))[0] for spec in SPECS}


def preservation(spec,target):
 base,_=sources();old=PxlImage.from_bytes(base.read_file(spec['path']));new=PxlImage.from_bytes(target);payloads,cases=regions(spec)
 if len(old.source)!=len(target) or old.source[:old.pixels_offset]!=target[:new.pixels_offset]:raise ValueError('Original palette/header/extent differs')
 expected=bytearray(old.indices);owned=set()
 for kind,pixels in zip(('main','caption'),payloads,strict=True):
  x0,y0,x1,y1=spec[kind]
  for y in range(y0,y1):
   for x in range(x0,x1):
    offset=y*256+x;expected[offset]=pixels[(y-y0)*(x1-x0)+x-x0];owned.add(offset)
 if bytes(new.indices)!=bytes(expected):raise ValueError('Complete English letter, original Latin ornament or unowned scene pixel differs')
 x0,y0,x1,y1=spec['main'];gold_count=0
 for y in range(y0,y1):
  for x in range(x0,x1):
   offset=y*256+x;r,g,b,_=old.palette[old.indices[offset]]
   if r>g+10 and g>b+30 and r>120:
    gold_count+=1
    if old.indices[offset]!=new.indices[offset]:raise ValueError('Original overlapping gold N pixel differs')
 # Every unowned pixel, including existing title copyright and gold logo, remains original.
 assert all(old.indices[i]==new.indices[i] for i in range(256*192) if i not in owned)
 return {'path': spec['path'],'all_unowned_scene_copyright_palette_header_extent_exact': True,'complete_artwork_exact': True,
  'overlapping_original_gold_pixels_exact': gold_count,
  'changed_pixel_count': sum(a!=b for a,b in zip(old.indices,new.indices,strict=True)),'cases': cases}


def materialize():
 base,_=sources();OUT.mkdir(parents=True,exist_ok=True);evidence=[]
 for spec in SPECS:
  p=PxlImage.from_bytes(base.read_file(spec['path']));payloads,cases=regions(spec)
  batch={'format': 'dk4-pxl-indexed-region-batch-v1','file_path': spec['path'],'source_file_sha256': sha(p.source),'target_locale': 'en-US',
   'scope': 'English franchise title and Rota Nova phonetic caption; original Latin ornament/copyright/background outside owned regions preserved.','records': []}
  for kind,pixels,proof in zip(('main','caption'),payloads,cases,strict=True):
   box=spec[kind];original=bytes(p.indices[y*256+x] for y in range(box[1],box[3]) for x in range(box[0],box[2]))
   batch['records'].append({'id': 'DK4_ROTA_'+spec['name'].upper()+'_'+kind.upper()+'_V1','box': box,
    'source_region_sha256': sha(original),'indices_zlib_hex': zlib.compress(pixels).hex(),'indices_sha256': sha(pixels),
    'source_japanese': '大航海時代IV' if kind=='main' else 'ロッタ ノヴァ','english': 'Uncharted Waters IV' if kind=='main' else 'Rota Nova','artwork_proof': proof})
  save(batch_path(spec),batch)
 result=targets()
 for spec in SPECS:
  evidence.append(preservation(spec,result[spec['path']]))
  source=PxlImage.from_bytes(base.read_file(spec['path'])).render();english=PxlImage.from_bytes(result[spec['path']]).render()
  sheet=Image.new('RGB',(1048,412),'#303030');d=ImageDraw.Draw(sheet)
  for i,(title,image) in enumerate((('Original',source),('English',english))):
   d.text((12+i*520,8),title,fill='white');sheet.paste(image.resize((512,384),Image.Resampling.NEAREST).convert('RGB'),(12+i*520,28))
  sheet.save(OUT/(spec['name']+'_review.png'));english.save(OUT/(spec['name']+'_english.png'))
 save(OUT/'evidence.json',{'cases': evidence,'visual_review': False,
  'scope': 'Source-backed scenery restoration is palette-quantized in owned regions; actual loaders/crops/GPU-alpha/gameplay pending.'})
 print('Prepared three title copies, six complete English lettering regions.')


def register():
 if not json.loads((OUT/'evidence.json').read_text(encoding='utf-8'))['visual_review']:raise ValueError('Full previews must be reviewed')
 s=load_release_stack();p=copy.deepcopy(s['profiles']['all-routes-unified-v174']);p['batches'] += [batch_path(spec).as_posix() for spec in SPECS]
 p.update(description='All 455 V174 batches/stages unchanged plus three source-locked English Rota Nova title copies; 458 batches.',
  note='Standalone logo and two DS title copies use complete English franchise/phonetic captions; original Latin ornament/copyright/metadata retained, original scene donors quantized only in owned text regions. Native loading/crops/composition pending; experimental.')
 s['profiles'][PROFILE]=p;save(RELEASE_STACK_PATH,s)


def verify():
 base,prior=sources()
 if REPRO.read_bytes()!=PRIOR.read_bytes():raise ValueError('Full V174 reproduction required')
 new=NdsImage.open(CANDIDATE);m=json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'));old=json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'));s=load_release_stack()
 if (m['base_sha256']!=CANONICAL_BASELINE_SHA256 or m['candidate_sha256']!=sha(CANDIDATE.read_bytes()) or m['profile']!=PROFILE
  or m['release_stack_sha256']!=sha(RELEASE_STACK_PATH.read_bytes()) or m['batches']!=old['batches']+[str(batch_path(spec)) for spec in SPECS]
  or m['batches']!=[str(p) for p in resolve_release_batches(PROFILE,[],s)] or len(m['batches'])!=458
  or m['required_batches']!=[str(p) for p in accepted_batch_paths(s)] or not all(m['checks'].values()) or m['relocations']!=old['relocations']):raise ValueError('Saved identity/inheritance differs')
 before,after=rom_files(prior),rom_files(new);changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p));paths=sorted(spec['path'] for spec in SPECS)
 if changed!=paths or m['changed_paths']!=sorted(old['changed_paths']+paths):raise ValueError('Unexpected changed files')
 if any(m['changed_records'][path]!=ids for path,ids in old['changed_records'].items()):raise ValueError('Prior IDs lost')
 targets();evidence=[]
 for spec in SPECS:
  path=spec['path'];target,ids=apply_pxl_indexed_region_batch(batch_path(spec),base.read_file(path))
  if target!=new.read_file(path) or m['changed_records'][path]!=ids:raise ValueError('Saved title artwork differs')
  evidence.append(preservation(spec,target))
 verify_golden_content(base,new);clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes())
 if clean_sha!='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':raise ValueError('Wrong clean base')
 patch=CANDIDATE.with_suffix('.xdelta');reconstruction=Path('work/analysis/rota_v175_patch_reconstruction.nds')
 make_xdelta(clean,CANDIDATE,patch);apply_xdelta(clean,patch,reconstruction)
 if reconstruction.read_bytes()!=CANDIDATE.read_bytes():raise ValueError('Patch reconstruction differs')
 save(PROOF,{'status': 'pass-saved-v175-three-rota-title-copies-and-inheritance','cases': evidence,
  'candidate': str(CANDIDATE),'candidate_sha256': sha(CANDIDATE.read_bytes()),'canonical_base': str(BASE),'canonical_base_sha256': CANONICAL_BASELINE_SHA256,
  'previous_sha256': PRIOR_SHA,'profile': PROFILE,'profile_status': 'experimental','batch_count': 458,'candidate_arm9_sha256': sha(new.read_file('/__arm9__.bin')),
  'registry_sha256': m['release_stack_sha256'],'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()),'complete_v174_reproduction_exact': True,
  'changed_paths_vs_v174': changed,'changed_paths_vs_canonical': m['changed_paths'],'patch': str(patch),'patch_bytes': patch.stat().st_size,'patch_sha256': sha(patch.read_bytes()),
  'clean_patch_base_sha256': clean_sha,'patch_reconstruction_exact': True,'native_loading_crops_composition_gameplay_verified': False})
 print(PROOF.read_text(encoding='utf-8'))


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('action',choices=['materialize','register','verify']);globals()[parser.parse_args().action]()
