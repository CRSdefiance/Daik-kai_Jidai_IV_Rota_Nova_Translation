"""Bind ordinary resupply/departure/final captures after both source-bound QA sequences."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B58_B70_clean_20261109')

def main():
    out=ROOT/'transition_review_v1';assert not out.exists();out.mkdir();samples=[]
    for key in ['rescue','town']:
        terminal=load(ROOT/f'display_runs_v1/{key}/terminal.json')
        report,observer=map(load,[terminal['report'],terminal['observer']])
        pixel=load(ROOT/f'display_pixels_v1/{key}/focused_actual_pixels.json')
        last=pixel['ordered_selected_source_calls'][-1]['frame']
        rows=[r for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>last]
        supply=next(r for r in rows if r['text_CP932']==' Want to resupply for ６００ gold?')
        depart=next(r for r in rows if 'Departed Hangzhou.' in r['text_CP932'])
        assert last<supply['frame']<depart['frame']<report['frames']
        for label,event in [('resupply',supply),('departure',depart)]:
            cap=next(c for c in report['frames_captured'] if c['frame']>=event['frame']+90)
            assert digest(cap['path'])==cap['PNG_sha256']
            samples.append(dict(run=key,kind=label,event_frame=event['frame'],event_text=event['text_CP932'],capture=cap))
        cap=report['frames_captured'][-1];assert cap['frame']==terminal['frames'] and digest(cap['path'])==cap['PNG_sha256']
        samples.append(dict(run=key,kind='final sailing',capture=cap))
    sheet=Image.new('RGB',(1536,1600),'#eee');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(samples):
        x,y=i%3*512,i//3*800;draw.text((x+4,y+4),s['run']+' '+s['kind']+' @'+str(s['capture']['frame']),fill='black')
        sheet.paste(Image.open(s['capture']['path']).convert('RGB').resize((512,768),Image.Resampling.NEAREST),(x,y+25))
    path=out/'transitions.png';sheet.save(path)
    save(out/'receipt.json',dict(samples=samples,review_sheet=dict(path=str(path),sha256=digest(path)),
        both_original_host_sequences_reach_resupply_departure_andfinal_capture=True,
        direct_visual_review_pending=True,original_source_scene_conditions_not_activated=True,new_credit=0))
    print('Bound six ordinary host-transition captures;direct visual review pending.')

if __name__=='__main__':main()
