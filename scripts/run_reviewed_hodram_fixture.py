"""Cold-boot one declared complete-script QA fixture with ordinary controller input."""
import argparse
import sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures',type=Path,required=True)
    parser.add_argument('--block',type=int,required=True)
    parser.add_argument('--inputs',type=Path)
    parser.add_argument('--capture-extra',type=int,nargs='*',default=[])
    args=parser.parse_args();manifest=load(args.fixtures)
    fixture=next(f for f in manifest['fixtures'] if f['block']==args.block)
    rom=Path(fixture['research_ROM']);out=Path(fixture['capture_folder']);assert not out.exists()
    assert sha(rom.read_bytes())==fixture['research_ROM_sha256']
    basepath=Path(fixture['inputs']);assert sha(basepath.read_bytes())==fixture['inputs_sha256']
    inputs=args.inputs or basepath;values=load(inputs);base=load(basepath)
    assert all(r in values for r in base)
    additional=[r for r in values if r not in base]
    assert all(set(r)=={'start','duration','buttons'} and r['buttons'] in [['UP'],['DOWN'],['LEFT'],['RIGHT'],['A'],['B']] and 0<r['duration']<=10 for r in additional)
    frames=fixture['frames'];captures=sorted({3980,4000,frames-1,*range(4220,frames,240),*args.capture_extra})
    assert all(0<frame<frames for frame in captures)
    out.mkdir(parents=True)
    plan=dict(fixtures=str(args.fixtures),fixtures_sha256=sha(args.fixtures.read_bytes()),block=args.block,
        ROM=str(rom),ROM_sha256=fixture['research_ROM_sha256'],inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        original_fixture_inputs=str(basepath),additional_ordinary_controller_inputs=additional,frames=frames,requested_captures=captures,
        cold_boot=True,savestate=False,initialized_complete_script_not_natural_activation=True,
        no_RAM_RNG_role_roster_money_eventflag_orconditional_override=True,guide_photo_collection=False,
        actual_English_display_andtransitions_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    save(out/'run_plan.json',plan)
    sys.argv=['headless_desmume_v193.py','--rom',str(rom),'--out',str(out),'--frames',str(frames),
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at',*map(str,captures),'--dump-ram']
    harness.main()
    reportpath=out/'capture_report.json';report=load(reportpath)
    assert report['cold_boot'] and not report['savestate_loaded'] and report['frames']==frames and not report['callback_errors']
    assert report['ROM_sha256']==fixture['research_ROM_sha256'] and not report['hardware_device_verification']
    save(out/'terminal.json',dict(terminal=True,frames=frames,capture_report=str(reportpath),capture_report_sha256=sha(reportpath.read_bytes()),
        run_plan=str(out/'run_plan.json'),run_plan_sha256=sha((out/'run_plan.json').read_bytes()),actual_English_visual_andpixel_review_pending=True,new_credit=0))
    print('Terminal complete:',args.block,frames,'frames; actual review pending.',flush=True)

if __name__=='__main__':main()
