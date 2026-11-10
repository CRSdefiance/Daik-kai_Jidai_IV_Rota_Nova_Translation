"""Use the existing paragraph planner with exact current source/child ownership."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_maria286_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')

def qualify_source(doc):
    owner_path=ROOT/'source16_manuscript.json';source=load(owner_path)
    assert doc['source_owner_manuscript_sha256']==digest(owner_path)
    assert doc['source_owner_manuscript']==str(owner_path)
    assert doc['blocks']==[50] and doc['physical_speech_objects']==len(doc['records'])==17
    assert doc['source_editorial_objects']==len(source['records'])==16
    assert doc['runtime']==source['runtime'] and doc['current_ROM_sha256']==source['current_ROM_sha256']==digest(doc['current_ROM'])
    assert digest(doc['source_full_manuscript'])==doc['source_full_manuscript_sha256']
    parent=load(doc['source_full_manuscript']);byparent={r['id']:r for r in parent['records']}
    originals={r['id']:r for r in source['records']}
    assert all(r==byparent[r['id']] for r in source['records'])
    owner=doc['pagination_owners'][0]
    assert owner['source_ID']=='DK4_MES_B50_R0043' and owner['unchanged_logical_English']==originals[owner['source_ID']]['english']
    children=[r for r in doc['records'] if r.get('source_editorial_ID')==owner['source_ID']]
    assert [r['id'] for r in children]==owner['child_IDs'] and [r['native_child_page'] for r in children]==[1,2]
    assert ' '.join(r['english'] for r in children)==owner['unchanged_logical_English']
    assert [r['english'] for r in children]==owner['page_segments']
    clean=NdsImage.open('work/clean.nds');image=NdsImage.open(doc['current_ROM'])
    assert sha(image.read_file('/__arm9__.bin'))==doc['runtime']['ARM9_sha256']
    assert sha(image.read_file('/data/SC3.DK4'))==doc['current_archive_sha256']
    clean_block=IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks[50]
    block=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks[50]
    bindings=[];seen=set()
    keys=['source_hex','current_hex','source_reference','current_reference','source_complete_preamble_hex','source_selector']
    for row in doc['records']:
        ident=row.get('source_editorial_ID',row['id']);original=originals[ident];seen.add(ident)
        assert all(row[k]==original[k] for k in keys)
        if ident==owner['source_ID']:
            assert row['kind']=='system-FE' and row['source_selector']==254 and row['native_child_page_count']==2
            assert row['source_complete_paragraph']==original['english']
        else:assert row==original
        sr,cr=row['source_reference'],row['current_reference'];a,b=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
        head=bytes.fromhex(row['source_complete_preamble_hex'])
        assert clean_block[sr['offset']-5:sr['offset']+len(a)+1]==head[:5]+a+b'\0'
        assert block[cr['offset']-5:cr['offset']+len(b)+1]==head[:5]+b+b'\0'
        assert head[5]==a[0]==b[0]==row['source_selector'] and head[:5]==bytes.fromhex('0040ffff00')
        bindings.append(dict(id=row['id'],source_editorial_ID=ident,source_reference=sr,current_reference=cr,
            complete_source_header_hex=head.hex(),source_body_sha256=sha(a),virtual_pagination_child_not_new_source_coverage=ident==owner['source_ID']))
    assert seen==set(originals) and len(bindings)==17
    return set(),bindings

env={**previous.env,**globals(),'__file__':__file__}
exec(compile(previous.source,__file__+'::same-full-width-automatic-planner-scoped-complete-FE-ownership','exec'),env)
main=env['main']
if __name__=='__main__':main()
