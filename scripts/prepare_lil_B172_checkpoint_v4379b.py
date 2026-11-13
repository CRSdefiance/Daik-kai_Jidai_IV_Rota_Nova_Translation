"""Preserve stopped preparer; correct unused replacement and literal newline-key quoting."""
import runpy
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/prepare_lil_B172_checkpoint_v4379.py','scripts/prepare_lil_B172_checkpoint_v4379b_impl.py',{
        'lil_B172_checkpoint_tools_v4379':'lil_B172_checkpoint_tools_v4379b',
        ",'V4328':'V4378'":'',
        '        "(json.dumps(ledger':'        r"(json.dumps(ledger',
    })
    runpy.run_path('scripts/prepare_lil_B172_checkpoint_v4379b_impl.py',run_name='__main__')
