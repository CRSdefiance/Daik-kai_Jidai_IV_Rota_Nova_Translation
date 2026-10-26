"""Correct unused derivation key and preserve the failed initial preparer."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/prepare_lil_B172_completion_v4408.py','scripts/prepare_lil_B172_completion_v4408b_impl.py',{
        'lil_B172_completion_tools_v4408':'lil_B172_completion_tools_v4408b',
        "'[171]':'[172]','block=171':'block=172','== 171':'== 172'":"'[171]':'[172]','block=171':'block=172'",
        r'|paired_region_differences\x27\]':'',
    })
    print('Corrected preparer checks;original failure preserved;no ledger or release mutation.')
