"""Copy native events before the first return assertion, retaining every assertion.

v1 stopped when a rejected encoding returned early, before its diagnostic copy.
Only move that read-only copy earlier; preserve the failed producer/partial files.
"""
import ast,inspect
from pathlib import Path
from scripts import Rafael_B45_FE_source_painter_v7894 as native_FE
from scripts.source_locked_derivation_v5118 import native_numbers

original=Path('scripts/probe_maria_B50_FE_boundary_v1.py').read_text(encoding='utf-8')
tree=ast.parse(original);roots=adapters=0
key=next(line for line in inspect.getsource(native_FE.make_source_painter).splitlines()
    if line.startswith('        assert cpu.reg_read(UC_ARM_REG_R0)==string+len(text)'))
value="        OBSERVATIONS.append(dict(events=events,complete_input_hex=text.hex()))\n"+key
for node in ast.walk(tree):
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ROOT' for t in node.targets):
        assert node.value.args[0].value=='work/Maria_B50_FE_resolution_20261109_v1'
        node.value.args[0]=ast.Constant('work/Maria_B50_FE_resolution_20261109_v2');roots+=1
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='adapter' for t in node.targets):
        assert node.value.func.id=='checked_text' and len(node.value.args)==2
        node.value.args[1]=ast.Dict(keys=[ast.Constant(key)],values=[ast.Constant(value)]);adapters+=1
assert roots==adapters==1
source=ast.unparse(ast.fix_missing_locations(tree))
assert native_numbers(source)==native_numbers(original)
exec(compile(source,__file__+'::same-native-matrix-read-only-events-before-return-guard','exec'),globals())
