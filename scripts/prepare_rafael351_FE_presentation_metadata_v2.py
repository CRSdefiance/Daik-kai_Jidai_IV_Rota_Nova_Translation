"""Classify the fifteen source-FE objects without changing prose or encoded source."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

if __name__ == '__main__':
    source = Path('translations/rafael_B121_B140_formatting_manuscript_v3.json')
    out = Path('translations/rafael_B121_B140_formatting_manuscript_v4.json')
    assert not out.exists()
    old = load(source); doc = deepcopy(old); seen=[]
    for row in doc['records']:
        if row.get('source_selector') != 254: continue
        assert row['kind']=='system-FE' and row['source_complete_preamble_hex']=='0040ffff00fe'
        key=(row['block'],row['source_reference']['record_index'])
        row['source_FE_presentation_kind'] = ('whispering sound' if key==(123,98) else
            'gold reward notice' if key==(126,20) else 'sailing tutorial')
        row['FE_is_not_an_ordinary_actor_nameplate'] = True
        if key==(123,98): assert row['source_Japanese']=='ひそひそ…'
        elif key==(126,20): assert row['source_Japanese']=='金貨２４０００枚を手に入れました'
        else: assert row['block'] in [127,128]
        seen.append(row['id'])
    assert len(seen)==15
    assert all(a['english']==b['english'] and a['review']==b['review'] for a,b in zip(old['records'],doc['records'],strict=True))
    doc.update(previous_formatting_input=str(source),previous_formatting_input_sha256=sha(source.read_bytes()),
        FE_metadata_only_no_wording_source_macro_or_gate_changes=True,source_FE_objects=seen)
    doc['evidence'].update({str(p):sha(p.read_bytes()) for p in [source,Path(__file__)]})
    save(out,doc)
    print('Classified15 source-FE objects:whispering,reward and13 sailing instructions;no prose/control/gate changes.')
