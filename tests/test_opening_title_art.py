"""Fixed title regions, complete glyphs and exact original movie contracts."""
import copy
import json
import zlib
from pathlib import Path

import pytest

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.build_integrated_release import apply_fls_indexed_region_batch
from scripts.opening_title_v174 import (
    BATCH,
    BOXES,
    PROFILE,
    RESOURCE,
    artwork,
    preservation,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base,_=sources();target,ids=targets();return base.read_file(RESOURCE),target,ids


def test_original_movie_contract_and_gold_logo_preserved(case):
    _,target,ids=case;p=preservation(target)
    assert p['all_other_movie_bytes_exact'] and p['all_native_records_palettes_extent_exact']
    assert p['original_latin_rota_nova_art_outside_caption_exact']
    assert ids==['DK4_OPENING_M28_TITLE_4_V1','DK4_OPENING_M28_TITLE_5_V1']


@pytest.mark.parametrize('asset',[4,5])
@pytest.mark.parametrize('edge',['first','last'])
def test_lost_english_edge_ink_rejected(case,asset,edge):
    source,target,_=case;a=FlsArchive(target);t=a.texture(asset);x0,y0,x1,_y1=BOXES[asset]
    original=FlsArchive(source).texture(asset)
    pixels,e=artwork(original,asset);line=e['lines'][0 if edge=='first' else -1];left,top,right,bottom=line['full_glyph_box']
    columns=range(left,right) if edge=='first' else range(right-1,left-1,-1)
    # Remove a complete edge column in the first/final text line, including ink/outline.
    found=False
    for x in columns:
        if any(t.palette[pixels[y*(x1-x0)+x]][2] > t.palette[pixels[y*(x1-x0)+x]][0] + 8
               and t.palette[pixels[y*(x1-x0)+x]][2] > t.palette[pixels[y*(x1-x0)+x]][1] + 8
               for y in range(top,bottom)):
            for y in range(top,bottom):t.indices[(y0+y)*256+x0+x]=0
            found=True;break
    assert found
    with pytest.raises(ValueError,match='Complete English letter'):
        preservation(a.to_bytes())


def wrong_batch(tmp_path,batch):
    p=tmp_path/'wrong.json';p.write_text(json.dumps(batch),encoding='utf-8');return p


@pytest.mark.parametrize('change,message',[
 ('file','source SHA-256'),('pixels','texture pixels'),('native','native record'),
 ('box','escapes original'),('payload','extent or identity'),('duplicate','ownership')])
def test_source_record_bounds_payload_ownership_guards(case,tmp_path,change,message):
    source,_,_=case;b=json.loads(BATCH.read_text(encoding='utf-8'));r=b['records'][0]
    if change=='file':b['source_file_sha256']='0'*64
    elif change=='pixels':r['source_texture_sha256']='0'*64
    elif change=='native':r['source_record'][0]^=1
    elif change=='box':r['box']=[6,1,257,50]
    elif change=='payload':r['indices_zlib_hex']=zlib.compress(b'x').hex();r['indices_sha256']=sha(b'x')
    elif change=='duplicate':b['records'].append(copy.deepcopy(r))
    with pytest.raises(ValueError,match=message):apply_fls_indexed_region_batch(wrong_batch(tmp_path,b),source)


def test_gold_latin_logo_damage_rejected(case):
    _,target,_=case;a=FlsArchive(target);t=a.texture(5);t.indices[25*256+90]^=1
    with pytest.raises(ValueError,match='unowned title pixel'):
        preservation(a.to_bytes())


def test_previous_textures_and_palette_bytes_cannot_change(case):
    _,target,_=case;data=bytearray(target);a=FlsArchive(target)
    data[a.data_offset+a.records[4][2]+5]^=1
    with pytest.raises(ValueError,match='palette|Unrelated movie'):
        preservation(bytes(data))


def test_english_title_and_original_glyph_envelope():
    b=json.loads(BATCH.read_text(encoding='utf-8'))
    assert [r['source_japanese'] for r in b['records']]==['大航海時代IV','ロッタ ノヴァ']
    assert [r['english'] for r in b['records']]==[['Uncharted Waters IV'],['Rota Nova']]
    for r in b['records']:
        assert r['box']==BOXES[r['asset_index']]
        width,height=r['box'][2]-r['box'][0],r['box'][3]-r['box'][1]
        for line in r['artwork_proof']['lines']:
            x0,y0,x1,y1=line['full_glyph_box'];assert 0<=x0<x1<=width and 0<=y0<y1<=height


def test_all_v173_layers_and_terminal_stages_exact():
    s=json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'));a,b=s['profiles']['all-routes-unified-v173'],s['profiles'][PROFILE]
    assert b['batches']==a['batches']+[BATCH.as_posix()] and len(b['batches'])==455
    assert all(value==b[key] for key,value in a.items() if key not in ('batches','note','description'))
