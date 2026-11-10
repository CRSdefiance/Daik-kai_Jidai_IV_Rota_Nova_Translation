"""Plan only the changed source-bound food-acceptance paragraph with the proven Rafael formatter."""
import linecache
from pathlib import Path
from scripts import plan_rafael_B81_B84_v1 as previous
from scripts.audit_story_glyph_consistency import load

def qualify_source(doc):
    p=Path(doc['subset_of']);assert previous.sha(p.read_bytes())==doc['subset_of_sha256']
    parent=load(p);assert parent['single_live_contextual_prose_revision_ID']=='DK4_MES_B81_R0220'
    assert len(doc['records'])==1 and doc['records']==[r for r in parent['records'] if r['id']=='DK4_MES_B81_R0220']
    zeros,bindings=previous.qualify_source(parent)
    assert doc['records'][0]['source_selector']==14
    return set(),[r for r in bindings if r['id']=='DK4_MES_B81_R0220']

source=previous.source;env={**previous.env,'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-native-bounds-one-live-contextual-prose-refinement'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
