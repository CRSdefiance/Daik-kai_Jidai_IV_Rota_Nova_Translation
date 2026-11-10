"""Bind each completed focused run to its ordinary host return; no replay."""
from PIL import Image, ImageDraw
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'transition_review_v1'; assert not out.exists()
    out.mkdir(); runs=[]
    for choice,frames in [(0,22721),(1,11681)]:
        terminal=load(ROOT/f'display_run_menu{choice}_v1/terminal.json')
        report,observer=map(load,[terminal['report'],terminal['observer']])
        pixel=load(ROOT/f'display_pixels_menu{choice}_v1/focused_actual_pixels.json')
        last=pixel['ordered_selected_source_calls'][-1]['frame']
        later=[r for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>last]
        supply=next(r for r in later if r['text_CP932']==' Want to resupply for ６００ gold?')
        departure=next(r for r in later if 'Departed Hangzhou.' in r['text_CP932'])
        assert last<supply['frame']<departure['frame']<report['frames']==frames
        samples=[]
        for label,event in [('resupply',supply),('departure',departure)]:
            capture=next(c for c in report['frames_captured'] if c['frame']>=event['frame']+90)
            assert digest(capture['path'])==capture['PNG_sha256']
            samples.append(dict(kind=label,event_frame=event['frame'],event_text=event['text_CP932'],capture=capture))
        final=report['frames_captured'][-1]
        assert final['frame']==frames and digest(final['path'])==final['PNG_sha256']
        samples.append(dict(kind='final sailing',capture=final))
        sheet=Image.new('RGB',(1536,800),'#eee'); draw=ImageDraw.Draw(sheet)
        for i,sample in enumerate(samples):
            draw.text((i*512+4,4),sample['kind']+' @'+str(sample['capture']['frame']),fill='black')
            with Image.open(sample['capture']['path']) as im:
                sheet.paste(im.convert('RGB').resize((512,768),Image.Resampling.NEAREST),(i*512,25))
        path=out/f'menu{choice}_transitions.png'; sheet.save(path)
        runs.append(dict(choice=choice,frames=frames,samples=samples,review_sheet=dict(path=str(path),sha256=digest(path))))
    save(out/'receipt.json',dict(runs=runs,source_complete_hosts_reach_resupply_departure_andfinal_sailing=True,
        direct_visual_review_pending=True,original_optional_story_conditions_not_activated=True,new_credit=0))
    print('Bound both actual host returns without repeating emulator runs.')

if __name__=='__main__':main()
