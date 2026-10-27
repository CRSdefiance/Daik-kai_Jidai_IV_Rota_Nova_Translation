"""Keep native-generated modal layouts reconstructable without a historical ROM dependency."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.activity_special_layout_v986 import compiled
from scripts.verify_village_wrap_v608 import read,save

def main():
    root=Path('work/analysis/activity_special_v987');proof_path=Path('work/analysis/activity_special_v986/native_font_proof.json')
    proof=read(proof_path);doc=read('translations/activity_special_editorial_manuscript_v2.json')
    index=Path('translations/activity_special_native_modal_layout_v1.json');layout=Path('scripts/activity_special_layout_v986b.py')
    target=Path('dk4tool/patch/activity_special_editorial_v987b.py');source=Path('dk4tool/patch/activity_special_editorial.py')
    assert not any(p.exists() for p in (index,layout,target))
    cases={r['message_id']:r for r in proof['cases']};rows=[]
    for row in doc['records']:
        if row['consumer']!='assignment-refusal-modal':continue
        encoded=compiled(row);case=cases[row['message_id']]
        assert encoded.hex()==case['compiled_hex'] and ' '.join(case['generated_native_lines'])==row['english']
        rows.append({'message_id':row['message_id'],'english':row['english'],'consumer':row['consumer'],
            'native_generated_hex':encoded.hex(),'generated_visible_lines':case['generated_native_lines']})
    assert len(rows)==3
    save(index,{'format':'dk4-native-generated-argument-free-modal-layout-v1','source_native_font_proof':str(proof_path),
        'source_native_font_proof_sha256':sha(proof_path.read_bytes()),'source_ARM9_sha256':proof['ARM9_sha256'],
        'source_formatter_entry':0x02147AE5,'rows':rows,'all_breaks_generated_by_original_registered_native_balanced_formatter':True,
        'no_translator_authored_line_breaks_or_positioning':True})
    layout_text='''"""Recorded native compiler results,source-locked to exact reviewed paragraphs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.activity_special_layout_v986 import layout,serialize
from scripts.verify_village_wrap_v608 import read
INDEX=Path('translations/activity_special_native_modal_layout_v1.json')
INDEX_SHA='''+repr(sha(index.read_bytes()))+'''

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
    return [s.strip().decode('ascii') for s in compiled(row).split(b'\\n')] if row['consumer']=='assignment-refusal-modal' else layout(row['english'])
'''
    old=source.read_bytes();text=source.read_text(encoding='utf-8')
    needle='from scripts.activity_special_layout_v986 import compiled';assert text.count(needle)==1
    text=text.replace(needle,'from scripts.activity_special_layout_v986b import compiled')
    ast.parse(layout_text);ast.parse(text)
    with layout.open('x',encoding='utf-8') as f:f.write(layout_text)
    with target.open('x',encoding='utf-8') as f:f.write(text)
    from scripts.activity_special_layout_v986b import compiled as frozen_compiled
    assert all(compiled(row)==frozen_compiled(row) for row in doc['records'])
    assert source.read_bytes()==old
    save(root/'native_generated_layout_provenance.json',{'original_module':str(source),'original_module_sha256':sha(old),
        'original_module_unchanged':True,'successor':str(target),'successor_sha256':sha(target.read_bytes()),
        'source_native_font_proof':str(proof_path),'source_native_font_proof_sha256':sha(proof_path.read_bytes()),
        'native_generated_index':str(index),'native_generated_index_sha256':sha(index.read_bytes()),
        'all17_compiled_bytes_exact_to_executed_native_font_proof':True,
        'historical_ROM_not_required_by_new_production_compiler':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('All17 compiled bytes remain exact;three native-generated modal layouts now reconstruct from source-locked evidence without historical ROM access.')

if __name__=='__main__':main()
