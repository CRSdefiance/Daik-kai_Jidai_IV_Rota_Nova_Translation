"""Derive ten additive pending reviews without rewriting historical identifiers."""
import re
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_checkpoint_tools_v4623')
assert not ROOT.exists()
source=Path('scripts/checkpoint_lil_B176_v4573b.py')
target=Path('scripts/checkpoint_lil_B177_v4623.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
replacements={
    'Lil-B176-banana-age-Owner-Cook-doubt-purchase-order-and-prospective-Seville-fashion10':
        'Lil-B177-tomato-red-passion-youthful-love-dry-Cook-cook-sell-and-prospective-Genoa-fashion10',
    'lil_B176_checkpoint_v4573b':'lil_B177_checkpoint_v4623',
    'work/analysis/promotion_v4571b/promotion_receipt.json':'work/analysis/editorial_handoff_verification_v4600/verified_handoff.json',
    'lil_B176_native_approval_v4572':'lil_B177_native_approval_v4622',
    'lil_B176_editorial_manuscript_v3':'lil_B177_editorial_manuscript_v5',
    'lil_B176_checkpoint_text_v4573':'lil_B177_checkpoint_text_v4623',
    'unfinished_editorial_scope_v4545':'unfinished_editorial_scope_v4599',
    'remaining_B177_B180':'remaining_B178_B180',
    'lil_B176_v4573':'lil_B177_v4623','lil_B176_scope_reconciliation_v4573':'lil_B177_scope_reconciliation_v4623',
    'row_count_notes=3':'row_count_notes=5',
    'V4571':'V4599','V4573':'V4623','v4573':'v4623','B176':'B177',
    "note = '5875 fresh rereads:5865 integrated/10 pending;source/prose5878. B176 credited once as pending;no completion or actual scene credit.'":
        "note = '5885 fresh rereads:5875 integrated/10 pending;source/prose5888. B177 credited once as pending;no completion or actual scene credit.'",
}
numbers={176:177,48:38,5865:5875,5875:5885,5868:5878,5878:5888,4012:4022,4022:4032,
         4276:4286,4266:4276,3728:3733,2137:2142}
replacements.update({str(k):str(v) for k,v in numbers.items()})
for key in replacements:assert key in text,key
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(replacements,key=len,reverse=True))
text=re.sub(pattern,lambda m:replacements[m.group()],text)
compile(text,str(target),'exec')
inventory=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
remaining=[b for b in read(inventory)['blocks'] if 178<=b['block']<=180]
assert len(remaining)==3 and sum(b['speeches'] for b in remaining)==38
assert sum(b['typed_menu_2100_commands']+b['typed_actor_style_4100_commands'] for b in remaining)==0
target.write_text(text,encoding='utf-8',newline='\n')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),
    target=str(target),target_sha256=sha(target.read_bytes()),remaining_scope_source=str(inventory),
    remaining_scope_source_sha256=sha(inventory.read_bytes()),remaining_B178_B180_physical_speeches=38,
    no_completion_credit_added_yet=True,full_goal_complete=False))
