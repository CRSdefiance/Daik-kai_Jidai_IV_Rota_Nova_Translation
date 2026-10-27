"""The same read-only exact menu reference checks in the supplied replay."""
import argparse,json
from pathlib import Path
from types import FunctionType
from scripts import observe_hot_spring_navigation_v1641b as previous
ROOT=Path('work/analysis/hot_spring_notice_supplied_v1643')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_supplied_v1643_1637')
mode=FunctionType(previous.mode.__code__,{**previous.__dict__,'ROOT':ROOT,'CAP':CAP},argdefs=previous.mode.__defaults__)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--frame',type=int,required=True);parser.add_argument('--expect');args=parser.parse_args();result=mode(args.frame)
    if args.expect:assert result['mode']==args.expect,result['mode']
    with (ROOT/'native_mode_observations.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(result)+'\n')
    print({'frame':args.frame,'mode':result['mode'],'exact_reference_pixels':result['mode']!='requires visual inspection'})
