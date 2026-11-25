"""Preserve the following clean blocks before any predecessor-English comparison."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_after_B220_inventory_tools_v6963');assert not root.exists();jobs=[]
    for block,version in [(221,6963),(222,6964)]:jobs.append(('scripts/inventory_lil_B220_clean_v6918.py',f'scripts/inventory_lil_B{block}_clean_v{version}.py',{'B220':f'B{block}','v6918':f'v{version}','blocks[220]':f'blocks[{block}]','block=220':f'block={block}'}))
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    root.mkdir(parents=True);save(root/'source_locked_derivations.json',[derive(a,b,c) for a,b,c in jobs])
