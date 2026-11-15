"""Cold-boot a staged successor with the exact verified predecessor input/capture schedule."""
import argparse
import sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['staged','parent-startup','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    staged,parent=map(load,(args.staged,args.parent_startup))
    assert staged['parent_sha256']==parent['candidate_sha256']
    assert digest(staged['candidate'])==staged['candidate_sha256']
    prior=Path(parent['capture_report']);assert digest(prior)==parent['capture_report_sha256']
    capture=load(prior);assert capture['cold_boot'] and capture['frames']==4001 and not capture['callback_errors']
    args.out.mkdir(parents=True);inputs=args.out/'exact_predecessor_inputs.json'
    save(inputs,capture['scripted_input_schedule'])
    save(args.out/'run_plan.json',dict(staged=str(args.staged),staged_sha256=digest(args.staged),
        parent_startup=str(args.parent_startup),parent_startup_sha256=digest(args.parent_startup),
        previous_capture=str(prior),previous_capture_sha256=digest(prior),inputs=str(inputs),inputs_sha256=digest(inputs),
        frames=4001,exact_capture_frames=capture['exact_requested_capture_frames'],new_credit=0))
    sys.argv=['headless_desmume_v193.py','--rom',staged['candidate'],'--out',str(args.out/'capture'),
        '--frames','4001','--inputs-json',str(inputs),'--capture-every','999999','--capture-at',
        *map(str,capture['exact_requested_capture_frames']),'--dump-ram']
    harness.main()


if __name__=='__main__':main()
