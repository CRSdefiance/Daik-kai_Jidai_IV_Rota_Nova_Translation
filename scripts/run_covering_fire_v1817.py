"""Current registered V1807 original covering-fire replay."""
import inspect
from pathlib import Path
from scripts import run_reinforcement_regional_live_v1041 as previous
from scripts.native_covering_fire_v1816 import apply_fixture

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('V1041','V1817').replace('scripts/native_reinforcement_proximity_v1040.py','scripts/native_covering_fire_v1816.py')
    anchor="    journal.write_text(";assert source.count(anchor)==1;at=source.index(anchor)
    source=source[:at]+"    commands=[json.loads(s)for s in Path('work/analysis/reinforcement_sniping_v1041/navigation.jsonl').read_text().splitlines()if s]\n"+source[at:]
    env={**previous.__dict__,'__file__':__file__,'ROM':Path('out/all_routes_combined_v1807_candidate.nds'),'ROOT':Path('work/analysis/covering_fire_run_v1817'),'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/covering_fire_v1817_1807'),'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env);env['main']()
