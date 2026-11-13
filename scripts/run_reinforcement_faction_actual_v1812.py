"""Current registered V1807 replay of original reinforcement event."""
import inspect
from pathlib import Path
from scripts import run_reinforcement_regional_live_v1049 as previous
from scripts.native_reinforcement_pact_v1811 import apply_fixture

if __name__=='__main__':
    source=inspect.getsource(previous.main).replace('V1049','V1812').replace('scripts/native_reinforcement_pact_v1048.py','scripts/native_reinforcement_pact_v1811.py')
    anchor="    journal.write_text("
    assert source.count(anchor)==1
    at=source.index(anchor)
    source=source[:at]+"    commands=[json.loads(s)for s in Path('work/analysis/reinforcement_sniping_v1049/navigation.jsonl').read_text().splitlines()if s]\n"+source[at:]
    env={**previous.__dict__,'__file__':__file__,'ROM':Path('out/all_routes_combined_v1807_candidate.nds'),'ROOT':Path('work/analysis/reinforcement_faction_actual_v1812'),'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_faction_actual_v1812_1807'),'apply_fixture':apply_fixture}
    exec(compile(source,__file__,'exec'),env);env['main']()
