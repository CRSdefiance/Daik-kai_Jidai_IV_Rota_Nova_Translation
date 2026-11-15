"""Cold-boot the staged fix using preserved ordinary New Game and genuine-save market inputs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT=Path('work/market_goods_info_terminator_release_v1')

def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    assert sys.argv[1:] in [['startup'],['market']]
    mode=sys.argv[1];staged=load(OUT/'staged_successor.json')
    assert digest(staged['candidate'])==staged['candidate_sha256']
    if mode=='startup':
        previous=Path('work/hodram_residual_release_v1/own_startup_subprocess_v1/capture/capture_report.json')
        requested=[1,1000,1800,2200,3000,4000,4001]
    else:
        previous=Path('work/emulation_v193/commodity_production_cargo_v360/capture_report.json')
        requested=[1,1200,4000,6000,8000,8800,9200,9600,10000,10400,10800,11200,11600]
    parent=load(previous);assert parent['cold_boot'] and not parent['savestate_loaded'] and not parent['callback_errors']
    target=OUT/(mode+'_run_v1');assert not target.exists();target.mkdir()
    inputs=target/'unchanged_ordinary_inputs.json';save(inputs,parent['scripted_input_schedule'])
    capture=target/'capture'
    command=[sys.executable,'-m','scripts.headless_desmume_v193','--rom',staged['candidate'],'--out',str(capture),
        '--frames',str(parent['frames']),'--inputs-json',str(inputs),'--start-frame','-1',
        '--capture-every','999999','--capture-at',*map(str,requested),'--capture-native-state-at',str(parent['frames']),'--dump-ram']
    donor=parent.get('battery_save_preloaded')
    if donor:
        assert mode=='market' and digest(donor['source'])==donor['source_sha256']
        command+=['--battery-save',donor['source']]
    else:assert mode=='startup'
    save(target/'run_plan.json',dict(mode=mode,staged=str(OUT/'staged_successor.json'),staged_sha256=digest(OUT/'staged_successor.json'),
        predecessor_report=str(previous),predecessor_report_sha256=digest(previous),
        unchanged_inputs=str(inputs),unchanged_inputs_sha256=digest(inputs),command=command,
        source_save=donor,no_savestate_orRAM_gameplay_override=True,normal_Controller_andstylus_inputs=True,
        actual_pixels_andnative_state_verification_pending=True,new_credit=0))
    subprocess.run(command,check=True)
    report=load(capture/'capture_report.json')
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==staged['candidate_sha256'] and report['frames']==parent['frames']
    assert report['scripted_input_schedule']==parent['scripted_input_schedule']
    if donor:assert digest(donor['source'])==donor['source_sha256']
    print('Completed',mode,'coldboot;',report['frames'],'frames. Pixel/native-state verification remains.')

if __name__=='__main__':main()
