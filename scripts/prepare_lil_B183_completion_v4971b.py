"""Preserve the prepared producer and correct two historical-key references."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/lil_B183_completion_tools_v4971b');assert not root.exists()
    tool=derive('scripts/complete_lil_B183_v4971.py','scripts/complete_lil_B183_v4971b.py',{
        'actual_source_event182_selected':'actual_source_event183_selected',
        "inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4971']['path']))":"inventory=deepcopy(read(ledger['unfinished_editorial_scope_v4919']['path']))",
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,prior_prepared_producer_preserved=True))
