"""Show three unmasked actual later-frame pairs;do not normalize observed differences."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_later_pairs_v7222b');ACTUAL=Path('work/analysis/lil_B225_English_actual_v7221/all13_English_speeches14_pages_complete_native_masks25_commands_630B_source_comparison.json');LATER=Path('work/analysis/lil_B225_later_v7222/following_final_components_and_measured_timing_RNG_RGB_limits.json')
if __name__=='__main__':
    assert not ROOT.exists();d,later=map(read,[ACTUAL,LATER]);assert later['actual_proof_sha256']==sha(ACTUAL.read_bytes());src=read(d['source_actual_proof']);reports=[read(x['capture_report']) for x in [src,d]];photos=[{p['frame']:p for p in r['frames_captured']} for r in reports];samples=d['later_sampled_whole_frame_comparisons'];assert samples;wanted=[samples[0]['frame'],samples[len(samples)//2]['frame'],16001];ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,1230),'#263238');draw=ImageDraw.Draw(sheet);pairs=[]
    for index,frame in enumerate(wanted):
        files=[];pixels=[]
        for column,label in enumerate(['Source','English']):
            p=photos[column][frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];im=Image.open(p['path']).convert('RGB');assert im.size==(256,384);pixels.append(im.tobytes());draw.text((column*256+3,index*410+3),label+' frame'+str(frame),fill='white');sheet.paste(im,(column*256,index*410+24));files.append(dict(language=label,capture=p['path'],sha256=p['PNG_sha256']))
        equal=pixels[0]==pixels[1];assert equal==next(r['whole_RGB_equal'] for r in samples if r['frame']==frame);pairs.append(dict(frame=frame,captures=files,whole_RGB_equal=equal))
    path=ROOT/'source_English_three_later_pairs_unmasked.png';sheet.save(path);save(ROOT/'three_actual_later_pairs.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),later_measurement=str(LATER),later_measurement_sha256=sha(LATER.read_bytes()),pairs=pairs,review_sheet=str(path),review_sheet_sha256=sha(path.read_bytes()),all_crops_full256x384_actual_source_pixels_without_masking_or_recreation=True,all_measured_later_differences_kept_in_full_measurement_not_only_selected_examples=True,no_causal_orwhole_RAM_future_sequence_equivalence_claim=True,visual_review_pending=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False))
