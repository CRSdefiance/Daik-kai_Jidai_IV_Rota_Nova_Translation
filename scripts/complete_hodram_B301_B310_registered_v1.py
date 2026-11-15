"""Apply the predecessor's once-only credit contract to the exact new record scope."""
import ast
import re
from scripts.complete_hodram_B281_B300_registered_v2 import source as previous
from scripts.source_locked_derivation_v5118 import native_numbers

NUMBERS={384:234,181:127,203:107,704:705,39:40,18:8,242:73,
    17749:18133,18133:18367,11009:11136,7124:7231,18136:18370,
    373:225,374:228,11:9,134:96,135:97,239:129}
STRINGS={'B281_B300':'B301_B310','B251_B280':'B281_B300',
    'B281–B300':'B301–B310','B251–B280':'B281–B300',
    'B281-B300':'B301-B310','B251-B280':'B281-B300','384':'234',
    'v1 stopped at the stale-status assertion before writing an integrated review or changing the ledger.':
        'The predecessor B281-B300 workflow exposed this stale intake-status field; its qualified resolution is reused only after all current source, name, five-gate and registered proofs pass.'}
pattern=re.compile('|'.join(re.escape(k) for k in sorted(STRINGS,key=len,reverse=True)))

class QualifiedScope(ast.NodeTransformer):
    def visit_Constant(self,node):
        if type(node.value) is int and node.value in NUMBERS:
            return ast.copy_location(ast.Constant(NUMBERS[node.value]),node)
        if isinstance(node.value,str):
            return ast.copy_location(ast.Constant(pattern.sub(lambda m:STRINGS[m.group(0)],node.value)),node)
        return node
    def visit_keyword(self,node):
        if node.arg=='all384_individual_five_gates_pass':node.arg='all234_individual_five_gates_pass'
        # Five review gates remain five; only the observed menu count changes.
        if node.arg=='observed_menu_instances':
            assert isinstance(node.value,ast.Constant) and node.value.value==5
            node.value=ast.copy_location(ast.Constant(4),node.value)
            return node
        return self.generic_visit(node)

tree=QualifiedScope().visit(ast.parse(previous));ast.fix_missing_locations(tree)
source=ast.unparse(tree)+'\n'
assert native_numbers(source)==native_numbers(previous)
needle='    ledger[FAMILY] = dict('
assert source.count(needle)==1
source=source.replace(needle,"""    ledger[BATCH].update(long_QA_return_risk_unresolved=False,
        native_QA_capacity_guard_pass=True,QA_capacity_defect_only_in_oversized_fixture=True,
        qualified_passing_QA_runs=2,qualified_passing_QA_frames=34162,
        focused_initialized_runs=7,focused_total_frames=156887,
        bounded_QA_return_proof=conf['bounded_QA_return_proof'])
"""+needle)
compile(source,__file__+'::scope-only-derivation-preflight','exec')
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-preservation-and-qualified-status-resolution','exec'),globals())
