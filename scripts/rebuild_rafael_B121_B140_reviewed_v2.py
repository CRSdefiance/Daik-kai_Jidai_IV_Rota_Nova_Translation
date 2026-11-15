"""Supply the record-index metadata from each exact current reference before the unchanged rebuild."""
from pathlib import Path
from scripts.rebuild_rafael_B121_B140_reviewed_v1 import source as previous,TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text

ORIGINAL=Path('scripts/rebuild_rafael_B121_B140_reviewed_v1.py')
source=checked_text(previous,{
    "        records=[r for r in ordinary if r['block']==block]":
        "        records=[deepcopy(r) for r in ordinary if r['block']==block]\n        for row in records:\n            index=row['current_reference']['record_index']\n            assert row.get('current_record_index',index)==index\n            row['current_record_index']=index",
    '[TEMPLATE,Path(__file__),':'[TEMPLATE,ORIGINAL,Path(__file__),',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-rebuild-source-bound-current-index-metadata','exec'),globals())
