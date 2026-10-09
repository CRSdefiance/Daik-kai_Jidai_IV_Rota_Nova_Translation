"""Complete gender symbols, source cells, and exact inherited graphic contracts."""
import json
from pathlib import Path

import pytest

from dk4tool.graphics.compact_font import (
    DATE_FONT_FACE,
    DATE_GLYPHS,
    FONT_FACE,
    GENDER_FONT_FACE,
    GENDER_FONT_SHA256,
    GENDER_GLYPHS,
    GLYPHS,
    glyph,
)
from dk4tool.graphics.pxl import PxlImage
from scripts.build_integrated_release import apply_pxl_native_label_batch
from scripts.marker_gender_v173 import (
    BATCH,
    LABELS,
    MARKER,
    OLD_SYNC,
    PROFILE,
    SYNC,
    preservation,
    sources,
    targets,
)


@pytest.fixture(scope='module')
def case():
    base, prior = sources()
    marker, embedded, _, _ = targets()
    return base, prior, marker, embedded


def test_complete_prior_captions_borders_and_both_copies(case):
    _, _, marker, embedded = case
    p = preservation(marker, embedded)
    assert p['changed_marker_pixel_count'] == 78
    assert p['prior_24_marker_captions_and_all_unowned_art_exact']
    assert [c['meaning'] for c in p['cases']] == ['Male','Female']


@pytest.mark.parametrize('symbol', ['♂','♀'])
def test_complete_symbol_edge_ink_rejected(case, symbol):
    _, _, marker, embedded = case
    p = PxlImage.from_bytes(marker)
    _, _, box, _ = next(row for row in LABELS if row[1] == symbol)
    ink = [y*256+x for y in range(box[1],box[3]) for x in range(box[0],box[2]) if p.indices[y*256+x]==15]
    for offset in (ink[0],ink[-1]):
        damaged = PxlImage.from_bytes(marker)
        damaged.indices[offset] = 1
        with pytest.raises(ValueError,match='complete symbol'):
            preservation(damaged.to_bytes(),embedded)


def test_no_older_compact_glyph_or_identity_changed():
    assert all(GENDER_GLYPHS[c]==rows for c,rows in DATE_GLYPHS.items())
    for face,table in ((FONT_FACE,GLYPHS),(DATE_FONT_FACE,DATE_GLYPHS)):
        for c in table:
            assert glyph(c,font_face=face).tobytes()==glyph(c,font_face=GENDER_FONT_FACE).tobytes()
    with pytest.raises(ValueError,match='Unsupported compact bitmap letter'):
        glyph('♂',font_face=DATE_FONT_FACE)


def test_wrong_font_face_identity_rejected(case,tmp_path):
    base,prior,_,_=case
    b=json.loads(BATCH.read_text(encoding='utf-8'));b['records'][0]['compact_font_sha256']='0'*64
    path=tmp_path/'wrong.json';path.write_text(json.dumps(b),encoding='utf-8')
    with pytest.raises(ValueError,match='compact font identity'):
        apply_pxl_native_label_batch(path,base.read_file(MARKER),prior.read_file('/__arm9__.bin'))


def test_symbol_overflow_rejected(case,tmp_path):
    base,prior,_,_=case
    b=json.loads(BATCH.read_text(encoding='utf-8'));b['records'][0]['box']=[235,98,241,109]
    b['records'][0].pop('background_indices_zlib_hex')
    path=tmp_path/'wrong.json';path.write_text(json.dumps(b),encoding='utf-8')
    with pytest.raises(ValueError,match='does not fit'):
        apply_pxl_native_label_batch(path,base.read_file(MARKER),prior.read_file('/__arm9__.bin'))


def test_unowned_marker_border_rejected(case):
    _,_,marker,embedded=case;p=PxlImage.from_bytes(marker);p.indices[96*256+234]^=1
    with pytest.raises(ValueError,match='unowned marker'):
        preservation(p.to_bytes(),embedded)


def test_all_v172_batches_and_stages_retained():
    s=json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    a,b=s['profiles']['all-routes-unified-v172'],s['profiles'][PROFILE]
    assert b['batches']==[SYNC.as_posix() if p==OLD_SYNC.as_posix() else p for p in a['batches']]+[BATCH.as_posix()]
    assert len(b['batches'])==454
    assert all(value==b[key] for key,value in a.items() if key not in ('batches','note','description'))


def test_batch_mapping_and_font_hash_pin():
    batch=json.loads(BATCH.read_text(encoding='utf-8'))
    assert [(r['source_japanese'],r['text'],r['box'],r['source_meaning']) for r in batch['records']]==LABELS
    assert all(r['compact_font_sha256']==GENDER_FONT_SHA256 for r in batch['records'])


def test_source_lock_rejected(case):
    base,prior,_,_=case;raw=bytearray(base.read_file(MARKER));raw[-1]^=1
    with pytest.raises(ValueError,match='PXL source SHA-256'):
        apply_pxl_native_label_batch(BATCH,bytes(raw),prior.read_file('/__arm9__.bin'))
