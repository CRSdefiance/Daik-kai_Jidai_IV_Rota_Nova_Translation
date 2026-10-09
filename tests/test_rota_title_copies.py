"""Complete title-copy glyphs, native metadata, donors and pixel ownership."""
import copy
import json
import zlib
from pathlib import Path

import pytest

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.build_integrated_release import apply_pxl_indexed_region_batch
from scripts.rota_title_copies_v175 import (
 PROFILE,
 SPECS,
 batch_path,
 preservation,
 regions,
 sources,
 targets,
)


@pytest.fixture(scope='module')
def case():
 base,_=sources();return base,targets()


@pytest.mark.parametrize('index',range(3))
def test_complete_artwork_original_metadata_and_gold_overlap(case,index):
 _,t=case;s=SPECS[index];p=preservation(s,t[s['path']])
 assert p['all_unowned_scene_copyright_palette_header_extent_exact']
 assert p['overlapping_original_gold_pixels_exact']>0
 assert [l['text'] for c in p['cases'] for l in c['lines']]==['UNCHARTED','WATERS IV','Rota Nova']


@pytest.mark.parametrize('index',range(3))
@pytest.mark.parametrize('kind',['main','caption'])
def test_first_and_final_english_ink_rejected(case,index,kind):
 _,targets_=case;s=SPECS[index];target=targets_[s['path']];p=PxlImage.from_bytes(target)
 _payloads,cases=regions(s);proof=next(c for c in cases if c['kind']==kind)
 for edge in ('first','last'):
  line=proof['lines'][0 if edge=='first' else -1];x0,y0,x1,y1=line['full_glyph_box']
  xs=range(x0,x1) if edge=='first' else range(x1-1,x0-1,-1)
  for x in xs:
   ys=[]
   for y in range(y0,y1):
    c=p.palette[p.indices[y*256+x]]
    if c[2]>c[0]+8 and c[2]>c[1]+8:ys.append(y)
   if ys:break
  assert ys
  damaged=PxlImage.from_bytes(target)
  for y in ys:damaged.indices[y*256+x]=0
  with pytest.raises(ValueError,match='Complete English letter'):
   preservation(s,damaged.to_bytes())


@pytest.mark.parametrize('index',range(3))
def test_latin_body_copyright_and_scene_cannot_change(case,index):
 _,t=case;s=SPECS[index];target=t[s['path']]
 for x,y in ((80,s['main'][3]+13),(10,170)):
  p=PxlImage.from_bytes(target);p.indices[y*256+x]^=1
  with pytest.raises(ValueError,match='ornament or unowned'):
   preservation(s,p.to_bytes())


def altered(tmp_path,b):
 p=tmp_path/'wrong.json';p.write_text(json.dumps(b),encoding='utf-8');return p


@pytest.mark.parametrize('change,message',[
 ('file','source SHA-256'),('region','source region identity'),('box','escapes original'),
 ('payload','extent or identity'),('overlap','Overlapping'),('duplicate','Duplicate')])
def test_exact_source_bounds_payload_and_overlap_guards(case,tmp_path,change,message):
 base,_=case;s=SPECS[0];b=json.loads(batch_path(s).read_text(encoding='utf-8'));r=b['records'][0]
 if change=='file':b['source_file_sha256']='0'*64
 elif change=='region':r['source_region_sha256']='0'*64
 elif change=='box':r['box']=[4,50,257,101]
 elif change=='payload':r['indices_zlib_hex']=zlib.compress(b'x').hex();r['indices_sha256']=sha(b'x')
 elif change=='duplicate':b['records'].append(copy.deepcopy(r))
 elif change=='overlap':
  b['records'].append(copy.deepcopy(r));b['records'][-1]['id']='OTHER'
 with pytest.raises(ValueError,match=message):apply_pxl_indexed_region_batch(altered(tmp_path,b),base.read_file(s['path']))


def test_original_donor_palette_quantization_is_source_bound(case):
 base,_=case
 for s in SPECS:
  b=json.loads(batch_path(s).read_text(encoding='utf-8'));p=b['records'][0]['artwork_proof']
  assert p['background_source']==s['background']
  if s['background']:assert p['background_source_sha256']==sha(base.read_file(s['background']))
  assert p['lines'][0]['full_glyph_box'][1]>=s['main'][1]
  assert p['lines'][-1]['full_glyph_box'][3]<s['main'][1]+42


def test_prior_v174_batches_and_all_terminal_stages_exact():
 s=json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'));a,b=s['profiles']['all-routes-unified-v174'],s['profiles'][PROFILE]
 assert b['batches']==a['batches']+[batch_path(x).as_posix() for x in SPECS]
 assert len(b['batches'])==458
 assert all(v==b[k] for k,v in a.items() if k not in ('batches','note','description'))
