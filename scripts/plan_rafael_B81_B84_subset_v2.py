"""Plan the exact323-record subset andtwo byte-bound complete grammatical endings."""
import linecache
from pathlib import Path
from scripts import plan_rafael_B81_B84_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

def qualify_source(doc):
    parent_path=Path(doc['subset_of']);assert previous.sha(parent_path.read_bytes())==doc['subset_of_sha256']
    parent=load(parent_path);ids={r['id'] for r in doc['records']}
    assert len(ids)==323 and doc['held_source_IDs']==['DK4_MES_B84_R0470','DK4_MES_B84_R0539']
    expected=[r for r in parent['records'] if r['kind']!='typed-choice-label' and r['id'] not in doc['held_source_IDs']]
    assert doc['records']==expected
    zeros,bindings=previous.qualify_source(parent)
    return zeros,[r for r in bindings if r['id'] in ids]

source=checked_text(previous.source,{
    "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077']":
        "assert row['id'] in ['DK4_MES_B142_R0159','DK4_MES_B56_R0077','DK4_MES_B82_R0089','DK4_MES_B82_R0103']",
    "assert result['lines'][0 if row['id']=='DK4_MES_B56_R0077' else 3]==retention['exact_line']":
        "assert result['lines'][retention.get('line_index',0 if row['id']=='DK4_MES_B56_R0077' else 3)]==retention['exact_line']",
})
env={**previous.env,'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::exact-subset-and-complete-sentence-ending-retentions'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
