"""Recorded native compiler results,source-locked to exact reviewed paragraphs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.activity_special_layout_v986 import layout,serialize
from scripts.verify_village_wrap_v608 import read
INDEX=Path('translations/activity_special_native_modal_layout_v1.json')
INDEX_SHA='f5f3241df1138aef9d4d1a0aae66d853d84196e6258c18b399e6ec12adf4a45c'

def compiled(row):
    assert 1872<=row['message_id']<=1888
    if row['consumer']!='assignment-refusal-modal':
        assert row['consumer']=='Deck-CabinInfoView' and row['message_id'] not in (1878,1879,1880)
        return serialize(layout(row['english']))
    assert sha(INDEX.read_bytes())==INDEX_SHA
    doc=read(INDEX);proof=Path(doc['source_native_font_proof'])
    assert sha(proof.read_bytes())==doc['source_native_font_proof_sha256']
    selected=[r for r in doc['rows'] if r['message_id']==row['message_id']]
    assert len(selected)==1;case=selected[0]
    assert case['english']==row['english'] and case['consumer']==row['consumer']
    encoded=bytes.fromhex(case['native_generated_hex'])
    assert b' '.join(encoded.split())==row['english'].encode('ascii')
    return encoded

def visible_lines(row):
    return [s.strip().decode('ascii') for s in compiled(row).split(b'\n')] if row['consumer']=='assignment-refusal-modal' else layout(row['english'])
