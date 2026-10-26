"""Remove redundant nested replacement key;retain first failed preparer."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/prepare_lil_B173_completion_v4449.py','scripts/prepare_lil_B173_completion_v4449b_impl.py',{
        'lil_B173_completion_tools_v4449':'lil_B173_completion_tools_v4449b',
        "        ('dict(revised=19, retained=8)','dict(revised=8, retained=3)')":"",
    })
    print('Removed redundant replacement already handled by its containing key;no ledger or ROM mutation.')
