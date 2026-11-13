"""Execute the immutable registered pipeline with regular collection of unreachable Python/native callback cycles."""
import argparse
import ctypes as ct
import gc
import json
import runpy
import sys
import threading
import time
import traceback
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

DRIVER=Path('scripts/build_integrated_release_with_Fernan_field.py')
DRIVERS=[DRIVER,Path('scripts/build_integrated_release_with_reviewed_text_data_v3.py'),Path('scripts/build_integrated_release_with_static_text.py'),
    Path('scripts/build_integrated_release_with_grouped_fields.py'),Path('scripts/build_integrated_release_with_next_owned_fields.py'),
    Path('scripts/build_integrated_release_with_owned_fields.py'),Path('scripts/build_integrated_release_with_owned_names.py'),
    Path('scripts/build_integrated_release_with_runtime_bounds.py'),Path('scripts/build_integrated_release.py')]

def memory():
    from ctypes import wintypes
    class Counters(ct.Structure):
        _fields_=[('cb',wintypes.DWORD),('faults',wintypes.DWORD)]+[(key,ct.c_size_t)for key in
            ['peak_working_set','working_set','peak_paged_pool','paged_pool','peak_nonpaged_pool','nonpaged_pool','pagefile','peak_pagefile','private_bytes']]
    value=Counters();value.cb=ct.sizeof(value)
    get=ct.windll.psapi.GetProcessMemoryInfo;get.argtypes=[wintypes.HANDLE,ct.c_void_p,wintypes.DWORD];get.restype=wintypes.BOOL
    process=ct.windll.kernel32.GetCurrentProcess;process.restype=wintypes.HANDLE
    if not get(process(),ct.byref(value),value.cb):raise ct.WinError()
    return {k:getattr(value,k)for k in ['working_set','peak_working_set','private_bytes','peak_pagefile']}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',required=True);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--work',type=Path,required=True);parser.add_argument('--telemetry',type=Path,required=True)
    args=parser.parse_args();assert not args.telemetry.exists()and not args.work.exists()and not args.out.exists()and not args.out.with_suffix('.manifest.json').exists()
    pins={str(p):sha(p.read_bytes())for p in DRIVERS};registry=Path('translations/release_stack.json');registry_before=registry.read_bytes()
    args.telemetry.mkdir(parents=True)
    old_threshold=gc.get_threshold();gc.set_threshold(100,5,5);stop=threading.Event();state=dict(collections=0,unreachable_collected=0,errors=[],peak_private_bytes=0)
    def collect():
        while not stop.wait(2):
            try:
                found=gc.collect();data=memory();state['collections']+=1;state['unreachable_collected']+=found
                state['peak_private_bytes']=max(state['peak_private_bytes'],data['private_bytes'])
                if state['collections']<=3 or state['collections']%15==0:
                    with(args.telemetry/'collections.jsonl').open('a',encoding='utf-8')as stream:
                        stream.write(json.dumps(dict(elapsed_seconds=round(time.monotonic()-started,1),**data,**state))+'\n')
            except Exception as error:state['errors'].append(repr(error))
    started=time.monotonic();thread=threading.Thread(target=collect,name='unreachable-cycle-collector',daemon=True);thread.start()
    request=dict(driver=str(DRIVER),driver_andcanonical_bytes=pins,registry_sha256=sha(registry_before),profile=args.profile,out=str(args.out),work=str(args.work),
        gc_thresholds=[100,5,5],collection_interval_seconds=2,source_code_guards_checks_native_execution_andtarget_unchanged=True,
        no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0)
    (args.telemetry/'request.json').write_text(json.dumps(request,indent=2)+'\n',encoding='utf-8')
    error=None
    try:
        sys.argv=[str(DRIVER),'--profile',args.profile,'--out',str(args.out),'--work',str(args.work)]
        runpy.run_path(str(DRIVER),run_name='__main__')
    except BaseException:
        error=traceback.format_exc();(args.telemetry/'failure_traceback.txt').write_text(error,encoding='utf-8');raise
    finally:
        stop.set();thread.join(timeout=2);gc.set_threshold(*old_threshold)
        unchanged=registry.read_bytes()==registry_before and all(sha(Path(p).read_bytes())==value for p,value in pins.items())
        result=dict(**request,terminal=True,driver_completed_without_exception=error is None,elapsed_seconds=round(time.monotonic()-started,1),
            garbage_collection=state,all_original_driver_andregistry_bytes_unchanged=unchanged)
        (args.telemetry/'completion.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        assert unchanged
