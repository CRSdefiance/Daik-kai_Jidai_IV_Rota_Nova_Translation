"""Original Assign,A dismissal,selection cancel and Deck exit for Chapel refusals."""
import argparse,json
from pathlib import Path
from scripts.native_activity_special_fixture_v988 import SPECS
from scripts.verify_village_wrap_v608 import read

ROOT=Path('work/analysis/activity_special_v988')

def main():
    p=argparse.ArgumentParser();p.add_argument('--case',choices=tuple(k for k,v in SPECS.items() if v[2] is None),required=True)
    p.add_argument('--phase',choices=('activate','dismiss','exit'),required=True);args=p.parse_args()
    path=ROOT/f'{args.case}_navigation.jsonl';commands=[json.loads(s) for s in path.read_text().splitlines()]
    folder=Path(read(ROOT/f'{args.case}_run_plan.json')['folder'])
    source={'activate':16500,'dismiss':17100,'exit':17700}[args.phase]
    assert commands[-1]['until']==source and (folder/f'frame_{source:06d}_arm9_ram.bin').exists()
    if args.phase=='activate':extra=[{'until':16700,'buttons':['A'],'duration':8},{'until':16900,'duration':1},{'until':17100,'duration':1}]
    elif args.phase=='dismiss':extra=[{'until':17300,'buttons':['A'],'duration':8},{'until':17500,'buttons':['B'],'duration':8},{'until':17700,'duration':1}]
    else:extra=[{'until':17900,'buttons':['B'],'duration':8},{'until':18100,'duration':1},{'stop':True}]
    with path.open('a',encoding='utf-8') as f:
        for command in extra:f.write(json.dumps(command)+'\n')
    print(args.case,args.phase,'appended',len(extra),'original-input commands')

if __name__=='__main__':main()
