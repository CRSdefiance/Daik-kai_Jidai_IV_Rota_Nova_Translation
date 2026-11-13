"""Recover a duplicate preparation substitution; prior relocation proof is preserved."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    prior=Path('scripts/prepare_lil_B139_B140_relocation_v3478.py');tree=ast.parse(prior.read_text(encoding='utf-8'))
    call=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='make' and ast.literal_eval(n.args[1])=='scripts/prepare_lil_B139_B140_research_v3479.py')
    a,b,changes=map(ast.literal_eval,call.args);a,b=Path(a),Path(b);assert not b.exists();t=a.read_text(encoding='utf-8')
    for x,y in changes:
        if x=='for n in [138]':assert 'for n in [139,140]' in t;continue
        assert x in t,x;t=t.replace(x,y)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B139_B140_research_tools_v3479b');assert not root.exists();root.mkdir(parents=True)
    plan=Path('work/analysis/lil_B139_B140_relocation_v3478/nested_source_relocation_research.json');assert len(read(plan)['blocks'])==2
    save(root/'provenance.json',dict(previous_failed_preparation=str(prior),previous_failed_preparation_sha256=sha(prior.read_bytes()),failure='Duplicate substring substitution: n in [138] had already updated the for clause. No research image had been created.',previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),preserved_successful_relocation=str(plan),preserved_relocation_sha256=sha(plan.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,full_goal_complete=False))
