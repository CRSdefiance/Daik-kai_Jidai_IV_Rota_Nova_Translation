"""Preserve failed AST selection; examine only constant single-key put paths."""
import runpy
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/prepare_Rafael_B49_completion_v8127d.py','scripts/prepare_Rafael_B49_completion_v8127e_generated.py',{
        "isinstance(n.args[0],ast.List) and ast.literal_eval(n.args[0])==[PENDING]":"isinstance(n.args[0],ast.List) and len(n.args[0].elts)==1 and isinstance(n.args[0].elts[0],ast.Constant) and ast.literal_eval(n.args[0])==[PENDING]",
    }))
    runpy.run_module('scripts.prepare_Rafael_B49_completion_v8127e_generated',run_name='__main__')
