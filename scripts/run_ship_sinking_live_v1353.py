"""Fresh cold boot with the actual-position one-time prebattle approach."""
import inspect
import json
from pathlib import Path
from scripts import run_ship_sinking_live_v1350 as previous
from scripts.native_ship_sinking_fixture_v1352 import apply_fixture

if __name__=='__main__':
    source = inspect.getsource(previous.main)
    old = "journal.write_text('',encoding='utf-8')"
    commands = [{'until':4900,'buttons':['A'],'duration':4,'battle_fixture':{'ship_sinking_context':'five_ship_approach'}},
                {'until':5000,'duration':1}]
    assert source.count(old)==1
    source = source.replace(old,"journal.write_text("+repr(''.join(json.dumps(c)+'\n' for c in commands))+",encoding='utf-8')")
    env = {**previous.__dict__,'__file__':__file__,'fixture':apply_fixture,
        'ROOT':Path('work/analysis/ship_sinking_live_v1353'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1353_1344')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
