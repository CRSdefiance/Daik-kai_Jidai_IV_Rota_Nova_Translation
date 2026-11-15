"""Cold-boot an exact staged successor in a clean emulator subprocess."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['staged','parent-startup','out']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    staged,parent=map(load,[a.staged,a.parent_startup])
    assert staged['parent_sha256']==parent['candidate_sha256']
    assert digest(staged['candidate'])==staged['candidate_sha256']
    reportpath=Path(parent['capture_report']);assert digest(reportpath)==parent['capture_report_sha256']
    prior=load(reportpath)
    assert prior['cold_boot'] and prior['frames']==4001 and not prior['callback_errors']
    assert not prior['savestate_loaded'] and not prior.get('battery_save_preloaded')
    a.out.mkdir(parents=True);inputs=a.out/'exact_predecessor_inputs.json';save(inputs,prior['scripted_input_schedule'])
    command=[sys.executable,'-m','scripts.headless_desmume_v193','--rom',staged['candidate'],
        '--out',str(a.out/'capture'),'--frames','4001','--inputs-json',str(inputs),
        '--capture-every','999999','--capture-at',*map(str,prior['exact_requested_capture_frames']),'--dump-ram']
    save(a.out/'run_plan.json',dict(staged=str(a.staged),staged_sha256=digest(a.staged),
        parent_startup=str(a.parent_startup),parent_startup_sha256=digest(a.parent_startup),
        previous_capture=str(reportpath),previous_capture_sha256=digest(reportpath),
        inputs=str(inputs),inputs_sha256=digest(inputs),command=command,
        emulator_separate_clean_subprocess=True,no_gameplay_orverification_credit_before_original_checker=True,new_credit=0))
    subprocess.run(command,check=True)
    fresh=a.out/'capture/capture_report.json';report=load(fresh)
    assert report['ROM_sha256']==staged['candidate_sha256'] and report['frames']==4001
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert report['scripted_input_schedule']==prior['scripted_input_schedule']
    assert report['exact_requested_capture_frames']==prior['exact_requested_capture_frames']
    save(a.out/'subprocess_completion.json',dict(report=str(fresh),report_sha256=digest(fresh),
        original_RGB_RAM_payload_andgetter_verifier_still_required=True,new_credit=0))

if __name__=='__main__':main()
