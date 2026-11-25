"""Run an unchanged verification script with regular collection of unreachable native callback cycles."""
import argparse
import gc
import json
import os
import runpy
import sys
import threading
import time
import traceback
from pathlib import Path
from scripts.run_registered_build_with_gc_v1 import memory
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script',type=Path,required=True)
    parser.add_argument('--telemetry',type=Path,required=True)
    parser.add_argument('arguments',nargs=argparse.REMAINDER)
    args=parser.parse_args();assert not args.telemetry.exists() and args.script.is_file()
    assert os.environ.get('PYTHONMALLOC')=='malloc'
    arguments=args.arguments[1:] if args.arguments[:1]==['--'] else args.arguments
    locked={str(p):sha(p.read_bytes()) for p in [args.script,Path('dk4tool/rom/nds.py'),Path('scripts/registered_editorial_runtime.py'),Path('scripts/registered_editorial_runtime_v2.py')]}
    args.telemetry.mkdir(parents=True)
    request=dict(script=str(args.script),arguments=arguments,locked_sources=locked,system_allocator='malloc',
        gc_thresholds=[10,1,1],collection_interval_seconds=0.5,no_native_assertion_test_guard_orinput_override=True,new_credit=0)
    (args.telemetry/'request.json').write_text(json.dumps(request,indent=2)+'\n',encoding='utf-8')
    stop=threading.Event();state=dict(collections=0,unreachable_collected=0,errors=[],peak_private_bytes=0)
    started=time.monotonic();threshold=gc.get_threshold();gc.set_threshold(10,1,1)
    def collect():
        while not stop.wait(0.5):
            try:
                state['unreachable_collected']+=gc.collect();state['collections']+=1;data=memory()
                state['peak_private_bytes']=max(state['peak_private_bytes'],data['private_bytes'])
                if state['collections']%15==0:
                    with(args.telemetry/'collections.jsonl').open('a',encoding='utf-8') as output:
                        output.write(json.dumps(dict(elapsed_seconds=round(time.monotonic()-started,1),**data,**state))+'\n')
            except Exception as error:state['errors'].append(repr(error))
    thread=threading.Thread(target=collect,daemon=True);thread.start();failure=None
    try:
        sys.argv=[str(args.script),*arguments];runpy.run_path(str(args.script),run_name='__main__')
    except BaseException:
        failure=traceback.format_exc();(args.telemetry/'failure_traceback.txt').write_text(failure,encoding='utf-8');raise
    finally:
        stop.set();thread.join(timeout=2);gc.set_threshold(*threshold)
        unchanged=all(sha(Path(p).read_bytes())==digest for p,digest in locked.items())
        (args.telemetry/'completion.json').write_text(json.dumps(dict(**request,terminal=True,completed_without_exception=failure is None,
            elapsed_seconds=round(time.monotonic()-started,1),garbage_collection=state,all_locked_sources_unchanged=unchanged),indent=2)+'\n',encoding='utf-8')
        assert unchanged
