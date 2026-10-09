"""English opening title artwork with original texture records and palettes."""
import argparse
import copy
import json
import zlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_fls_indexed_region_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save

BASE=Path('out/raphael_natural_v2_accepted_base.nds')
PRIOR=Path('out/all_routes_combined_v173_candidate.nds')
PRIOR_SHA='19df444510eca115d1facc118180a793ef99cdcbc104f484428d3c0575b4f29f'
RESOURCE='/FLS/M28.fls'
BATCH=Path('translations/opening_m28_title_art_v1.json')
PROFILE='all-routes-unified-v174'
CANDIDATE=Path('out/all_routes_combined_v174_candidate.nds')
REPRO=Path('work/analysis/v173_title_builder_reproduction.nds')
OUT=Path('work/qa/opening_title_v174')
PROOF=Path('work/analysis/opening_title_v174_saved_proof.json')
FONT=Path('C:/Windows/Fonts/timesbd.ttf')
BOXES={4:[6,1,251,50],5:[151,39,201,50]}


def sources():
    if sha(BASE.read_bytes())!=CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes())!=PRIOR_SHA:
        raise ValueError('Exact canonical and V173 required')
    base,prior,clean=[NdsImage.open(p) for p in (BASE,PRIOR,Path('work/clean.nds'))]
    if not base.read_file(RESOURCE)==prior.read_file(RESOURCE)==clean.read_file(RESOURCE):
        raise ValueError('Exact untouched original title source required')
    return base,prior


def nearest(palette,rgb):
    return min(range(1,len(palette)),key=lambda i:sum((a-b)**2 for a,b in zip(palette[i][:3],rgb,strict=True)))


def artwork(texture,index):
    x0,y0,x1,y1=BOXES[index];width,height=x1-x0,y1-y0
    original=bytearray(b''.join(texture.indices[y*256+x0:y*256+x1] for y in range(y0,y1)))
    canvas=Image.new('L',(width,height));d=ImageDraw.Draw(canvas);line_cases=[]
    if index==4:
        font=ImageFont.truetype(str(FONT),size=29);lines=['UNCHARTED','WATERS IV'];pixels=bytearray(width*height)
        metrics=[font.getbbox(text) for text in lines];heights=[b[3]-b[1] for b in metrics]
        gap=3;total=sum(heights)+gap;y=(height-total)//2
        for text,b,h in zip(lines,metrics,heights,strict=True):
            w=b[2]-b[0];x=(width-w)//2
            if x<3 or y<2 or x+w+3>width or y+h+2>height:
                raise ValueError('Complete English title or outline does not fit source ink envelope')
            d.text((x-b[0],y-b[1]),text,font=font,fill=255)
            line_cases.append({'text': text,'full_glyph_box': [x,y,x+w,y+h],'font_size': 29})
            y+=h+gap
        outline=canvas.filter(ImageFilter.MaxFilter(3));white=nearest(texture.palette,(255,255,255));dark=nearest(texture.palette,(35,40,65))
        for y in range(height):
            for x in range(width):
                if x>=1 and y>=1 and outline.getpixel((x-1,y-1))>=128:pixels[y*width+x]=dark
                if outline.getpixel((x,y))>=128:pixels[y*width+x]=white
                if canvas.getpixel((x,y))>=128:
                    shade=y%23;rgb=(20,75,240) if shade<5 else (10,35,max(105,235-(shade-5)*8))
                    pixels[y*width+x]=nearest(texture.palette,rgb)
    else:
        font=ImageFont.truetype(str(FONT),size=9);text='Rota Nova';b=font.getbbox(text);w,h=b[2]-b[0],b[3]-b[1]
        x,y=(width-w)//2,(height-h)//2
        if x<0 or y<0:raise ValueError('Complete phonetic caption does not fit')
        pixels=original.copy();white=nearest(texture.palette,(255,255,255));blue=nearest(texture.palette,(40,60,205))
        removed=0
        for i,value in enumerate(original):
            r,g,bv,_=texture.palette[value]
            if bv>r+2 and bv>g+2:pixels[i]=white;removed+=1
        if not removed:raise ValueError('Original blue Japanese caption not found')
        d.text((x-b[0],y-b[1]),text,font=font,fill=255)
        for i,value in enumerate(canvas.tobytes()):
            if value>=128:pixels[i]=blue
        line_cases.append({'text': text,'full_glyph_box': [x,y,x+w,y+h],'font_size': 9,'original_blue_caption_pixels': removed})
    if not canvas.getbbox():raise ValueError('Empty English title artwork')
    return bytes(pixels),{'lines': line_cases,'mask_sha256': sha(canvas.tobytes()),'source_owned_box': BOXES[index],'font_sha256': sha(FONT.read_bytes())}


def targets():
    base,_=sources();return apply_fls_indexed_region_batch(BATCH,base.read_file(RESOURCE))


def preservation(target):
    base,_=sources();source=base.read_file(RESOURCE);a,b=FlsArchive(source),FlsArchive(target)
    if a.records!=b.records or a.data_offset!=b.data_offset or len(source)!=len(target):
        raise ValueError('Native title records/flags/dimensions/extent changed')
    owned_bytes=set();cases=[]
    for i in (4,5):
        original,new=a.texture(i),b.texture(i);pixels,evidence=artwork(original,i);cases.append(evidence)
        x0,y0,x1,y1=BOXES[i]
        for y in range(64):
            for x in range(256):
                wanted=pixels[(y-y0)*(x1-x0)+x-x0] if x0<=x<x1 and y0<=y<y1 else original.indices[y*256+x]
                if new.indices[y*256+x]!=wanted:raise ValueError('Complete English letter or unowned title pixel differs')
        if original.palette!=new.palette:raise ValueError('Original palette changed')
        start=a.data_offset+a.records[i][4];owned_bytes.update(range(start,start+a.records[i][5]))
    if any(x!=y for i,(x,y) in enumerate(zip(source,target,strict=True)) if i not in owned_bytes):
        raise ValueError('Unrelated movie bytes, textures, palettes or native records changed')
    return {'all_other_movie_bytes_exact': True,'all_native_records_palettes_extent_exact': True,
                'original_latin_rota_nova_art_outside_caption_exact': True,'complete_english_artwork_exact': True,'cases': cases}


def materialize():
    base,_=sources();source=base.read_file(RESOURCE);a=FlsArchive(source)
    batch={'format': 'dk4-fls-indexed-region-batch-v1','file_path': RESOURCE,'source_file_sha256': sha(source),'target_locale': 'en-US',
               'scope': 'Opening title localized as Uncharted Waters IV; preserve original Rota Nova Latin logo and localize duplicate phonetic caption.',
               'brand_sources': ['https://www.koeitecmo.co.jp/e/ir/docs/ird1_20250212_09e.pdf','https://www.gamecity.ne.jp/products/products/ee/Rldai4rn.htm'],'records': []}
    for i in (4,5):
        t=a.texture(i);pixels,proof=artwork(t,i)
        batch['records'].append({'id': 'DK4_OPENING_M28_TITLE_'+str(i)+'_V1','asset_index': i,'box': BOXES[i],
         'source_texture_sha256': sha(bytes(t.indices)),'source_record': a.records[i],'indices_zlib_hex': zlib.compress(pixels).hex(),'indices_sha256': sha(pixels),
         'source_japanese': '大航海時代IV' if i==4 else 'ロッタ ノヴァ','english': ['Uncharted Waters IV'] if i==4 else ['Rota Nova'],'artwork_proof': proof})
    save(BATCH,batch);target,_=targets();evidence=preservation(target)
    OUT.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(1048,600),'#303030');d=ImageDraw.Draw(sheet)
    for col,raw in enumerate((source,target)):
        f=FlsArchive(raw);x=12+col*520;d.text((x,8),'Original' if col==0 else 'English',fill='white')
        for row,i in enumerate((4,5)):
            d.text((x,30+row*276),'Texture '+str(i),fill='white')
            sheet.paste(f.texture(i).render().resize((512,128),Image.Resampling.NEAREST).convert('RGB'),(x,50+row*276))
        f.texture(5).render().crop(tuple(BOXES[5])).resize((300,66),Image.Resampling.NEAREST).save(OUT/('source_caption.png' if col==0 else 'english_caption.png'))
    sheet.save(OUT/'review.png');save(OUT/'evidence.json',dict(evidence,visual_review=False,
        scope='Storage and original ink-envelope proof. Native movie UV/composition/loading/GPU palette/alpha remain pending.'))
    print('Prepared two complete English opening-title regions.')


def register():
    if not json.loads((OUT/'evidence.json').read_text(encoding='utf-8'))['visual_review']:raise ValueError('Review artwork first')
    s=load_release_stack();p=copy.deepcopy(s['profiles']['all-routes-unified-v173']);p['batches'].append(BATCH.as_posix())
    p.update(note='Opening main logo Uncharted Waters IV and small Rota Nova phonetic caption, original records/palettes/Latin logo preserved. Native UV/composition pending; experimental.',
             description='All 454 V173 batches/stages exact, plus canonical-source M28 title-art layer; 455 batches.')
    s['profiles'][PROFILE]=p;save(RELEASE_STACK_PATH,s)


def verify():
    base,prior=sources()
    if REPRO.read_bytes()!=PRIOR.read_bytes():raise ValueError('Full V173 reproduction required')
    new=NdsImage.open(CANDIDATE);m=json.loads(CANDIDATE.with_suffix('.manifest.json').read_text(encoding='utf-8'));old=json.loads(PRIOR.with_suffix('.manifest.json').read_text(encoding='utf-8'));s=load_release_stack()
    if (m['base_sha256']!=CANONICAL_BASELINE_SHA256 or m['candidate_sha256']!=sha(CANDIDATE.read_bytes())
        or m['profile']!=PROFILE or m['batches']!=old['batches']+[str(BATCH)] or len(m['batches'])!=455
        or m['batches']!=[str(p) for p in resolve_release_batches(PROFILE,[],s)] or m['release_stack_sha256']!=sha(RELEASE_STACK_PATH.read_bytes())
        or m['required_batches']!=[str(p) for p in accepted_batch_paths(s)] or not all(m['checks'].values()) or m['relocations']!=old['relocations']):raise ValueError('Identity/inherited stack differs')
    before,after=rom_files(prior),rom_files(new);changed=sorted(p for p in before.keys()|after.keys() if before.get(p)!=after.get(p))
    if changed!=[RESOURCE] or m['changed_paths']!=sorted(old['changed_paths']+[RESOURCE]):raise ValueError('Unexpected changed paths')
    if any(m['changed_records'][p]!=ids for p,ids in old['changed_records'].items()):raise ValueError('Prior record IDs lost')
    target,ids=targets()
    if new.read_file(RESOURCE)!=target or m['changed_records'][RESOURCE]!=ids:raise ValueError('Saved artwork differs')
    evidence=preservation(target);verify_golden_content(base,new)
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes())
    if clean_sha!='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':raise ValueError('Wrong clean patch base')
    patch=CANDIDATE.with_suffix('.xdelta');reconstruction=Path('work/analysis/title_v174_patch_reconstruction.nds')
    make_xdelta(clean,CANDIDATE,patch);apply_xdelta(clean,patch,reconstruction)
    if reconstruction.read_bytes()!=CANDIDATE.read_bytes():raise ValueError('Patch reconstruction differs')
    save(PROOF,dict(evidence,status='pass-saved-v174-title-art-and-inheritance',candidate=str(CANDIDATE),candidate_sha256=sha(CANDIDATE.read_bytes()),
     canonical_base=str(BASE),canonical_base_sha256=CANONICAL_BASELINE_SHA256,previous_sha256=PRIOR_SHA,
     profile=PROFILE,profile_status='experimental',batch_count=455,candidate_arm9_sha256=sha(new.read_file('/__arm9__.bin')),
     registry_sha256=m['release_stack_sha256'],builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),
     complete_v173_reproduction_exact=True,changed_paths_vs_v173=changed,changed_paths_vs_canonical=m['changed_paths'],
     patch=str(patch),patch_bytes=patch.stat().st_size,patch_sha256=sha(patch.read_bytes()),clean_patch_base_sha256=clean_sha,patch_reconstruction_exact=True,
     native_UV_composition_loading_gameplay_verified=False))
    print(PROOF.read_text(encoding='utf-8'))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['materialize','register','verify']);globals()[parser.parse_args().action]()
