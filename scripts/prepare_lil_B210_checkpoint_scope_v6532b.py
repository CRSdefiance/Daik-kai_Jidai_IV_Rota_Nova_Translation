"""Correct the checkpoint's prior-scope key using the actual predecessor producer."""
import ast
from pathlib import Path
from scripts import prepare_lil_B210_sealed_checkpoint_v6532 as template
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B210_sealed_checkpoint_tools_v6532b')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/checkpoint_lil_B210_source_prose_v6501.py');text=source.read_text('utf-8');tree=ast.parse(text);env=dict(vars(template))
    for variable,name in [('oldsummary','SUMMARY'),('oldnext','NEXT')]:env[variable]=next(ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
    env['oldgates']=next(ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='gates');failed=Path(template.__file__);node=next(n for n in ast.walk(ast.parse(failed.read_text('utf-8'))) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='changes' for t in n.targets));changes=eval(compile(ast.Expression(node.value),str(failed)+'::frozen-mapping','eval'),env);bad="previous=old['unfinished_editorial_scope_v6501']";assert changes.pop(bad)=="previous=old.get('unfinished_editorial_scope_v6501')";actual="previous=old['unfinished_editorial_scope_v6493']";assert actual in text;changes[actual]="previous=old['unfinished_editorial_scope_v6501']"
    row=derive(str(source),'scripts/checkpoint_lil_B210_sealed_v6532.py',changes);ROOT.mkdir(parents=True);save(ROOT/'exact_prior_scope_preparation.json',dict(derived=row,failed_preparer=str(failed),failed_preparer_sha256=sha(failed.read_bytes()),actual_predecessor_scope6493_in_original6501_producer_updated_to_current6501=True,only_scope_key_preparation_correction_no_native_guard_or_credit_change=True,all_prior_failed_sources_and_evidence_preserved=True,full_goal_complete=False));print('Sealed checkpoint prepared against actual current scope6501;earlier absent-key rejection retained,no ledger change yet.')
