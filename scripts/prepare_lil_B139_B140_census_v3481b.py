"""Complete census preparation after a redundant import/path substitution."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    prior=Path('scripts/prepare_lil_B139_B140_references_v3480.py');tree=ast.parse(prior.read_text(encoding='utf-8'));common=ast.literal_eval(next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='common' for t in n.targets)))
    c=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='make' and ast.literal_eval(n.args[1])=='scripts/verify_lil_B139_B140_references_v3481.py')
    a,b=map(Path,map(ast.literal_eval,c.args[:2]));assert not b.exists();t=a.read_text(encoding='utf-8');changes=common+ast.literal_eval(c.args[2].right)
    for x,y in changes:
        if x=='lil_B138_research_v3442b':assert x not in t and 'scripts.prepare_lil_B139_B140_research_v3479' in t;continue
        assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B139_B140_census_tools_v3481b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous_failed_preparation=str(prior),previous_failed_preparation_sha256=sha(prior.read_bytes()),failure='The second source uses the research module only as an import;the import replacement had consumed the sole prior path substring. Successful loader retained.',previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
