"""Inspect exact Speyer test pauses; append ordinary input only after inspection."""
import argparse
import json
from pathlib import Path
from types import FunctionType
from scripts import navigate_lil_crew_v1759b as prior
from dk4tool.patch.grand_race_menu_release import sha

RUN = Path('work/analysis/lil_Speyer_context_run_v1920')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_context_run_v1920_RESEARCH_ONLY')
JOURNAL = RUN/'navigation.jsonl'
snapshot = FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--frame',type=int,required=True)
    parser.add_argument('--advance',type=int)
    parser.add_argument('--button',choices=['A','B','START','UP','DOWN','LEFT','RIGHT'])
    args = parser.parse_args()
    raw,im,progress,photo = snapshot(args.frame)
    pending = [progress['rows'][i] for i in progress['pending'].values()]
    print(dict(frame=args.frame,capture=str(photo),RAM_sha256=sha(raw),pending=[r['source'] for r in pending]))
    if args.advance:
        latest = max(int(p.name.split('_')[1]) for p in CAP.glob('frame_*_arm9_ram.bin'))
        assert latest == args.frame,('stale pause;no input appended',latest,args.frame)
        command = dict(until=args.frame+args.advance,duration=8 if args.button else 1)
        if args.button:command['buttons']=[args.button]
        with JOURNAL.open('a',encoding='utf-8') as stream:stream.write(json.dumps(command)+'\n')
        print(dict(appended_ordinary_input=command))
