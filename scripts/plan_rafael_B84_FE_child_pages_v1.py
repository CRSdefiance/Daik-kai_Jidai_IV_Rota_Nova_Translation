"""Apply the proven FE geometry to source-bound child panels;qualify their whole-paragraph ownership."""
import linecache
from pathlib import Path
from scripts import plan_rafael_B81_B84_v1 as previous
from scripts.audit_story_glyph_consistency import load

def qualify_source(doc):
    parent_path=Path(doc['subset_of']);assert previous.sha(parent_path.read_bytes())==doc['subset_of_sha256']
    parent=load(parent_path);zeros,bindings=previous.qualify_source(parent);originals={r['id']:r for r in parent['records']}
    assert doc['physical_speech_objects']==len(doc['records'])==4 and doc['source_editorial_objects']==2
    assert [r['source_ID'] for r in doc['pagination_owners']]==['DK4_MES_B84_R0470','DK4_MES_B84_R0539']
    result=[]
    for owner in doc['pagination_owners']:
        original=originals[owner['source_ID']];rows=[r for r in doc['records'] if r['source_editorial_ID']==original['id']]
        assert [r['id'] for r in rows]==owner['child_IDs'] and [r['native_child_page'] for r in rows]==[1,2]
        assert ' '.join(r['english'] for r in rows)==owner['unchanged_logical_English']==original['english']
        for row in rows:
            assert all(row[k]==original[k] for k in ['source_hex','current_hex','source_reference','current_reference','source_complete_preamble_hex','source_selector'])
            assert row['source_selector']==254 and not any(row['source_macros'].values()) and row['native_child_page_count']==2
            result.append(dict(next(r for r in bindings if r['id']==original['id']),id=row['id'],source_editorial_ID=original['id'],
                native_child_page=row['native_child_page'],virtual_pagination_child_not_new_source_coverage=True))
    return set(),result

source=previous.source
env={**previous.env,'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-FE-width-guard-phase-and-two-source-paragraph-ownership'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
