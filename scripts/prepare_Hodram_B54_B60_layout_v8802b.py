"""Preserve unparseable first producer; qualify apostrophe and actual six reactions."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

if __name__=='__main__':
    source=Path('scripts/plan_Hodram_B54_B60_v8802.py');target=Path('scripts/plan_Hodram_B54_B60_v8802b.py')
    receipt=Path('work/analysis/Hodram_B54_B60_layout_preparation_v8802b')
    assert not target.exists() and not receipt.exists() and not Path('work/analysis/Hodram_B54_B60_layout_v8802').exists()
    original=source.read_bytes();text=original.decode('utf-8')
    try:ast.parse(text)
    except SyntaxError as exc:syntax=dict(line=exc.lineno,message=exc.msg)
    else:raise AssertionError('Expected preserved syntax failure')
    rows=read('translations/hodram_B54_B60_editorial_manuscript_v1.json')['records']
    reactions=[r['id'] for r in rows if r['english'] in ['…','？']];assert len(reactions)==6
    changes={"('don't','mention')":'("don\'t",\'mention\')','assert len(REACTIONS)==7':'assert len(REACTIONS)==6','work/analysis/Hodram_B54_B60_layout_v8802':'work/analysis/Hodram_B54_B60_layout_v8802b'}
    for a,b in changes.items():assert text.count(a)==1;text=text.replace(a,b)
    ast.parse(text);compile(text,str(target),'exec')
    inverse=text
    for a,b in reversed(list(changes.items())):assert inverse.count(b)==1;inverse=inverse.replace(b,a)
    assert inverse.encode('utf-8')==original
    target.write_bytes(text.encode('utf-8'));receipt.mkdir(parents=True)
    save(receipt/'preserved_syntax_failure_andqualified_successor.json',dict(source=str(source),source_sha256=sha(original),target=str(target),target_sha256=sha(target.read_bytes()),
        original_syntax_failure=syntax,actual_six_reaction_IDs=reactions,exact_textual_inverse_except_declared_qualification=True,
        native_numeric_constants_andall_other_source_text_unchanged=True,source_locked_AST_helper_inapplicable_to_unparseable_original=True,
        no_ROM_registry_ledger_credit_ororiginal_producer_change=True,new_credit=0,full_goal_complete=False))
    print('Preserved syntax failure; qualified exact apostrophe and six reaction bindings; source inverse exact.')
