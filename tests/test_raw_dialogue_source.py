import copy
import hashlib

import pytest

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch


def fixture(body=None):
    if body is None:
        body = '決意はかたいようだな\n他でもねえ。あんたのためだ'.encode('cp932')
    raw = b'\x94'+body
    source = IlnkContainer([raw+b'\0sentinel']).to_bytes()
    record = dict(id='DK4_MES_B00_R0000',
                  english="{SPEAKER:94}You're set on it, huh? Just for you, then.{PAD}",
                  raw_source=dict(hex=raw.hex(), presentation_prefix_hex='94'))
    batch = dict(format='dk4-ilnk-translation-batch-v1',file_path='/data/SC2.DK4',
                 source_file_sha256=hashlib.sha256(source).hexdigest(),
                 encoder='dialogue-fixed-v1',dialogue_profile='lil-story-deep-route-v110-live',
                 translation_policy='natural-dialogue-v2',records=[record])
    return raw,source,batch


def test_explicit_raw_source_retains_complete_prefix_allocation_and_neighbor():
    raw,source,batch = fixture()
    with pytest.raises(UnicodeDecodeError):
        raw.decode('cp932')
    rows = materialize_translation_batch(batch,source)
    assert rows[0]['source_hex'] == raw.hex().upper()
    assert rows[0]['japanese'] == '決意はかたいようだな{LB}他でもねえ。あんたのためだ'
    result = IlnkContainer.parse(rebuild_mesfile(source,rows)).blocks[0].split(b'\0')
    assert result[0][0] == 0x94 and len(result[0]) == len(raw)
    assert result[1] == b'sentinel'
    assert b"You're set on it" in result[0] and b'for you, then.' in result[0]


@pytest.mark.parametrize('change', ['bytes','prefix','speaker','profile','policy','file'])
def test_raw_source_rejects_unverified_or_mismatched_interpretations(change):
    _,source,batch = fixture()
    batch = copy.deepcopy(batch)
    row = batch['records'][0]
    if change == 'bytes':
        row['raw_source']['hex'] = '00'
    elif change == 'prefix':
        row['raw_source']['presentation_prefix_hex'] = '93'
    elif change == 'speaker':
        row['english'] = 'Lost the speaker.{PAD}'
    elif change == 'profile':
        batch['dialogue_profile'] = 'story'
    elif change == 'policy':
        batch['translation_policy'] = 'natural-dialogue-v1'
    else:
        batch['file_path'] = '/COMMON/MESFILE.DK4'
    with pytest.raises(ValueError):
        materialize_translation_batch(batch,source)


def test_raw_source_cannot_hide_an_embedded_unmapped_control():
    _,source,batch = fixture('決意はかたいようだな\n他でもねえ。あんたのためだ'.encode('cp932')+b'\x01')
    with pytest.raises(ValueError,match='unmapped controls'):
        materialize_translation_batch(batch,source)


def test_real_shift_jis_94_text_lead_stays_on_the_normal_decoder_path():
    source = IlnkContainer(['反対です'.encode('cp932')]).to_bytes()
    _,_,batch = fixture()
    batch['source_file_sha256'] = hashlib.sha256(source).hexdigest()
    with pytest.raises(ValueError,match='normal source resolution'):
        materialize_translation_batch(batch,source)
