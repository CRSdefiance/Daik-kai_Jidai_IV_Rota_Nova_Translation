"""Derive the full pre-write ledger audit, keeping main and latest candidate distinct."""
import re
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_handoff_audit_tools_v4624')
assert not ROOT.exists()
source=Path('scripts/verify_editorial_handoff_v4574c.py')
target=Path('scripts/verify_editorial_handoff_v4624.py')
assert not target.exists()
text=source.read_text(encoding='utf-8')
replacements={
    'checkpoint_lil_B176_v4573b':'checkpoint_lil_B177_v4623',
    'editorial_handoff_verification_v4574c':'editorial_handoff_verification_v4624',
    'unfinished_editorial_scope_v4573':'unfinished_editorial_scope_v4623',
    'unfinished_editorial_scope_v4545':'unfinished_editorial_scope_v4599',
    'lil_B176_scope_reconciliation_v4573':'lil_B177_scope_reconciliation_v4623',
    'lil_B176_v4573':'lil_B177_v4623',
    'remaining_B177_B180':'remaining_B178_B180',
    'V4573':'V4623','v4573':'v4623','B176':'B177',
    "controls['source_declared_end_offsets']==[386]":"controls['source_declared_end_offsets']==[482]",
    '00a0ffff010a0da1':'00a0ffff01090fa1','.blocks[176]':'.blocks[177]',
    "terms['chosen_city']=='Seville' and len(terms['exact_city_source_current_pointer_bindings'])==2":
        "terms['chosen_city']=='Genoa' and len(terms['exact_city_source_current_inline_span_and_pointer_bindings'])==4",
    "terms['chosen_ordinary_commodity_word']=='bananas' and terms['FE_Seville_notice_preserves_prospective_likelihood_not_current_or_guaranteed_boom']":
        "terms['chosen_ordinary_commodity_word']=='tomatoes' and terms['speaker_treats_tomato_fashion_as_opportunity_closing_FE_retains_prospective_likelihood']",
    "assert promoted['profile']==candidate['profile']=='all-routes-unified-v4541'":
        "assert promoted['profile']=='all-routes-unified-v4541' and candidate['profile']=='all-routes-unified-v4595'",
    "assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']==candidate['sha256']":
        "assert sha(Path(promoted['rom']).read_bytes())==promoted['rom_sha256']\n    assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==doc['current_ROM_sha256']",
}
numbers={5865:5875,5875:5885,5868:5878,5878:5888,4012:4022,4022:4032,
         4276:4286,4266:4276,3728:3733,2137:2142,48:38}
replacements.update({str(k):str(v) for k,v in numbers.items()})
for key in replacements:assert key in text,key
pattern='|'.join(re.escape(k) if not k.isdigit() else r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])' for k in sorted(replacements,key=len,reverse=True))
text=re.sub(pattern,lambda m:replacements[m.group()],text)
compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(source=str(source),source_sha256=sha(source.read_bytes()),
    target=str(target),target_sha256=sha(target.read_bytes()),
    main_V4541_and_latest_experimental_V4595_bound_separately=True,
    four_Genoa_inline_pointer_bindings_required=True,all_semantic_history_checks_before_first_write=True,
    no_completion_credit_added=True,full_goal_complete=False))
