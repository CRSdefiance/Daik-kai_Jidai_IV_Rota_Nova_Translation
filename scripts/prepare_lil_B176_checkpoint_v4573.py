"""Derive additive B176 coverage against the completed main promotion."""
import re
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_checkpoint_tools_v4573')
assert not ROOT.exists()
source=Path('scripts/checkpoint_lil_B175_v4519.py')
target=Path('scripts/checkpoint_lil_B176_v4573.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
replacements={
    'Lil-B175-pirate-encirclement-pride-sea-challenge-unnamed-sword-and-banter32':
        'Lil-B176-banana-age-Owner-Cook-doubt-purchase-order-and-prospective-Seville-fashion10',
    'lil_B175_checkpoint_v4519':'lil_B176_checkpoint_v4573',
    'promotion_v4512':'promotion_v4571b','lil_B175_native_approval_v4518':'lil_B176_native_approval_v4572',
    'lil_B175_editorial_manuscript_v3':'lil_B176_editorial_manuscript_v3',
    'lil_B175_checkpoint_text_v4519':'lil_B176_checkpoint_text_v4573',
    'unfinished_editorial_scope_v4500':'unfinished_editorial_scope_v4545',
    'remaining_B176_B180':'remaining_B177_B180','all4_mixed_speech_sheets_viewed':'all2_mixed_speech_sheets_viewed',
    'lil_B175_v4519':'lil_B176_v4573','lil_B175_scope_reconciliation_v4519':'lil_B176_scope_reconciliation_v4573',
    'row_count_notes=13':'row_count_notes=3','V4512':'V4571','V4496':'V4541',
    'V4519':'V4573','v4519':'v4573','B175':'B176',
}
numbers={32:10,19:5,13:5,175:176,58:48,5833:5865,5865:5875,5836:5868,5868:5878,
         3980:4012,4012:4022,4266:4276,4234:4266,3709:3728,2124:2137}
replacements.update({str(k):str(v) for k,v in numbers.items()})
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<!\d)'+k+r'(?!\d)' for k in sorted(replacements,key=len,reverse=True))
text=re.sub(pattern,lambda m:replacements[m.group()],text)
compile(text,str(target),'exec')
inventory=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
remaining=[b for b in read(inventory)['blocks'] if 177<=b['block']<=180]
assert len(remaining)==4 and sum(b['speeches'] for b in remaining)==48
assert sum(len(b['typed_menu_2100_commands'])+len(b['typed_actor_style_4100_commands']) for b in remaining)==0
target.write_text(text,encoding='utf-8',newline='\n')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),
    target=str(target),target_sha256=sha(target.read_bytes()),remaining_scope_source=str(inventory),
    remaining_scope_source_sha256=sha(inventory.read_bytes()),remaining_B177_B180_physical_speeches=48,
    full_goal_complete=False))
