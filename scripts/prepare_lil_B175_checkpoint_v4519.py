"""Derive the additive B175 coverage stage with exact previous-checkpoint binding."""
import re
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B175_checkpoint_tools_v4519')
if __name__=='__main__':
    target=Path('scripts/checkpoint_lil_B175_v4519.py');assert not ROOT.exists() and not target.exists()
    source=Path('scripts/checkpoint_lil_B174_v4475.py');text=source.read_text(encoding='utf-8')
    replacements={
        'Lil-B174-Julian-Mihwa-crown-gratitude-grandfather-aspiration-conditional-date33':
            'Lil-B175-pirate-encirclement-pride-sea-challenge-unnamed-sword-and-banter32',
        'lil_B174_checkpoint_v4475':'lil_B175_checkpoint_v4519','promotion_v4452':'promotion_v4512',
        'lil_B174_native_approval_v4474':'lil_B175_native_approval_v4518',
        'lil_B174_editorial_manuscript_v5':'lil_B175_editorial_manuscript_v3',
        'lil_B174_checkpoint_text_v4475':'lil_B175_checkpoint_text_v4519',
        'unfinished_editorial_scope_v4449':'unfinished_editorial_scope_v4500',
        'remaining_B175_B180':'remaining_B176_B180',
        'all5_speech_sheets_viewed':'all4_mixed_speech_sheets_viewed',
        'lil_B174_v4475':'lil_B175_v4519','lil_B174_scope_reconciliation_v4475':'lil_B175_scope_reconciliation_v4519',
        'V4452':'V4512','V4445':'V4496','V4475':'V4519','v4475':'v4519','B174':'B175',
    }
    numbers={33:32,23:19,10:13,17:13,174:175,90:58,5800:5833,5833:5865,5803:5836,5836:5868,
             3947:3980,3980:4012,4234:4266,4201:4234,3686:3709,2114:2124}
    replacements.update({str(k):str(v) for k,v in numbers.items()})
    pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<!\d)'+k+r'(?!\d)' for k in sorted(replacements,key=len,reverse=True))
    text=re.sub(pattern,lambda m:replacements[m.group()],text)
    compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
    inventory=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
    remaining=[b for b in read(inventory)['blocks'] if 176<=b['block']<=180]
    assert len(remaining)==5 and sum(b['speeches'] for b in remaining)==58
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),
        target=str(target),target_sha256=sha(target.read_bytes()),remaining_scope_source=str(inventory),
        remaining_scope_source_sha256=sha(inventory.read_bytes()),remaining_B176_B180_physical_speeches=58,
        full_goal_complete=False))
    print('Prepared B175 pending coverage:5865 reread/5833 completed/32 pending;5868 source/prose. B176-B180 physical speeches58 verified.')
