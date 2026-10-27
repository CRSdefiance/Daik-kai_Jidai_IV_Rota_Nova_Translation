"""Inspect an exact live pause and append ordinary input only after inspection."""
import argparse
import json
from pathlib import Path
from types import FunctionType
from scripts import navigate_lil_crew_v1759b as prior
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

RUN=Path('work/analysis/lil_London_context_run_v1884')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_context_run_v1884_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'
snapshot=FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--frame',type=int,required=True)
    p.add_argument('--advance',type=int)
    p.add_argument('--button',choices=['A','B','START'])
    a=p.parse_args()
    raw,im,progress,photo=snapshot(a.frame)
    pending=[progress['rows'][i] for i in progress['pending'].values()]
    print(dict(frame=a.frame,capture=str(photo),RAM_sha256=sha(raw),pending=[r['source'] for r in pending]))
    if a.advance:
        latest=max(int(f.name.split('_')[1]) for f in CAP.glob('frame_*_arm9_ram.bin'))
        assert latest==a.frame,('stale pause;no input appended',latest,a.frame)
        command=dict(until=a.frame+a.advance,duration=8 if a.button else 1)
        if a.button:command['buttons']=[a.button]
        with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')
        print(dict(appended_ordinary_input=command))
