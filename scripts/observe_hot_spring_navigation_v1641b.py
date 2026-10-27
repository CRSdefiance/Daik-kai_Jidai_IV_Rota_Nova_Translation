"""Read-only exact reference pixels for native menu modes;never chooses an event."""
import argparse,json
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/hot_spring_notice_live_v1641')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_notice_live_v1641_1637')
REF=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_live_v1626_1622')

def mode(frame):
    path=CAP/f'frame_{frame:06d}_navigation.png'
    with Image.open(path) as image:picture=image.convert('RGB')
    matches=[];refs=[]
    for name,ref_frame,boxes in [('Info Mode',11900,[(0,0,256,112)]),('Search Mode',12100,[(0,0,256,112)]),
        ('Sea View',10000,[(80,0,176,16),(0,370,256,384)])]:
        reference=REF/f'frame_{ref_frame:06d}_navigation.png'
        with Image.open(reference) as image:other=image.convert('RGB')
        equal=all(picture.crop(box).tobytes()==other.crop(box).tobytes() for box in boxes)
        refs.append({'mode':name,'reference':str(reference),'reference_sha256':sha(reference.read_bytes()),'exact_boxes':boxes,'equal':equal})
        if equal:matches.append(name)
    assert len(matches)<=1,matches
    return {'frame':frame,'mode':matches[0] if matches else 'requires visual inspection','capture':str(path),'capture_sha256':sha(path.read_bytes()),
        'reference_pixel_tests':refs,'read_only_no_input_or_event_state_change':True}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--frame',type=int,required=True);parser.add_argument('--expect');args=parser.parse_args()
    result=mode(args.frame)
    if args.expect:assert result['mode']==args.expect,result['mode']
    with (ROOT/'native_mode_observations.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(result)+'\n')
    print({'frame':args.frame,'mode':result['mode'],'exact_reference_pixels':result['mode']!='requires visual inspection'})
