"""Plan one reviewed successor paragraph with the full source-qualified Rafael geometry."""
import linecache
from pathlib import Path
from scripts import plan_rafael_B81_B84_v1 as previous
from scripts.audit_story_glyph_consistency import load

def qualify_source(doc):
    path=Path(doc['subset_of']);assert previous.sha(path.read_bytes())==doc['subset_of_sha256']
    parent=load(path);ident=parent['single_live_contextual_prose_revision_ID']
    assert len(doc['records'])==1 and doc['records']==[r for r in parent['records'] if r['id']==ident]
    zeros,bindings=previous.qualify_source(parent)
    raw=bytes.fromhex(doc['records'][0]['source_hex'])
    return zeros & {raw},[r for r in bindings if r['id']==ident]

source=previous.source;env={**previous.env,'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-complete-source-controls-native-bounds-one-reviewed-delta'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
