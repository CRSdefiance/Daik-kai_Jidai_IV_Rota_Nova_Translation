"""Preserve the prepared loader and recover one duplicate reference-path substitution."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    prior=Path('scripts/prepare_lil_B141_reference_tools_v3555.py');tree=ast.parse(prior.read_text(encoding='utf-8'));common=ast.literal_eval(next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='common' for t in n.targets)))
    call=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='make' and ast.literal_eval(n.args[1])=='scripts/verify_lil_B141_references_v3556.py');a,b=map(lambda x:Path(ast.literal_eval(x)),call.args[:2]);assert not b.exists();changes=common+ast.literal_eval(call.args[2].right);t=a.read_text(encoding='utf-8');skipped=[]
    for x,y in changes:
        if x=='lil_B139_B140_research_v3479' and x not in t:assert 'scripts.prepare_lil_B141_research_v3554' in t;skipped.append(x);continue
        assert x in t,x;t=t.replace(x,y)
    assert len(skipped)==1;compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B141_reference_tools_v3555b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(prior_failed_preparation=str(prior),prior_failed_preparation_sha256=sha(prior.read_bytes()),failure='The complete module-name replacement consumed the only remaining old research basename in the reference producer. No reference verifier had executed.',preserved_prepared_loader='scripts/verify_lil_B141_loader_v3555.py',preserved_prepared_loader_sha256=sha(Path('scripts/verify_lil_B141_loader_v3555.py').read_bytes()),previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),all_previous_artifacts_preserved=True,full_goal_complete=False))
