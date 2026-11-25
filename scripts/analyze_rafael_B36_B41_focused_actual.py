"""Bind only the sixteen selected utterances to observed native calls and complete pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B36_B41_focused_actual_pixels_20261104')
FIXTURE=Path('work/analysis/Rafael_B36_B41_focused_actual_fixture_20261104/focused_fixture.json')
TERMINAL=Path('work/analysis/Rafael_B36_B41_focused_actual_run_20261104/terminal.json')
NATIVE=Path('work/analysis/Rafael_B36_B41_formatting_20261104/speech_display_approved_v3/all175_native_pages.json')

if __name__=='__main__':
    assert not ROOT.exists()
    fixture,terminal,native=map(load,[FIXTURE,TERMINAL,NATIVE])
    assert terminal['terminal'] and terminal['frames']==fixture['frames']==10001
    reportpath,observerpath=Path(terminal['report']),Path(terminal['observer'])
    assert sha(reportpath.read_bytes())==terminal['report_sha256'] and sha(observerpath.read_bytes())==terminal['observer_sha256']
    report,observer=map(load,[reportpath,observerpath])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(report['ROM']).read_bytes())
    assert not observer['errors'] and not observer['mismatches'] and observer['all_host_slots_restored_and_core_file_exact']
    byid={r['id']:r for r in native['records']};expected=[]
    for row in fixture['selected_records']:
        body=bytes.fromhex(row['expected_expanded_body_hex'])
        for number,page in enumerate(byid[row['id']]['complete_native_English_display']['pages'],1):
            plane=Path(page['native_plane']).read_bytes();assert sha(plane)==page['native_plane_sha256'] and len(plane)==216*64
            expected.append(dict(id=row['id'],page=number,selector=row['selector'],native_plane=page['native_plane'],native_plane_sha256=page['native_plane_sha256'],
                text_hex=body[page.get('start',0):].hex(),pixel_mask_sha256=sha(bytes(bool(v) for v in plane))))
    assert len(expected)==18 and len(fixture['selected_records'])==16
    allowed={p['text_hex'] for p in expected}
    paints=[r for r in observer['rows'] if r['kind']=='modal_paint' and r['frame']>=2800]
    target=[r for r in paints if r['text_hex'] in allowed]
    assert [r['text_hex'] for r in target]==[p['text_hex'] for p in expected],(len(target),len(expected))
    ordered={r['frame']:p for r,p in zip(target,expected,strict=True)}
    start=target[0]['frame'];end=next((r['frame'] for r in paints if r['frame']>target[-1]['frame']),report['frames'])
    samples=[]
    for cap in report['frames_captured']:
        if not start<=cap['frame']<end:continue
        active=next(r for r in reversed(target) if r['frame']<=cap['frame']);page=ordered[active['frame']]
        path=Path(cap['path']);assert sha(path.read_bytes())==cap['PNG_sha256']
        crop=Image.open(path).convert('RGB').crop((16,296,232,360))
        if sha(bytes(rgb==(0,8,0) for rgb in crop.getdata()))==page['pixel_mask_sha256']:
            samples.append(dict(**page,capture=cap,frame=cap['frame'],live_modal_frame=active['frame'],complete_native_body_plane_andblank_guards_equal=True))
    unique={}
    for sample in samples:unique.setdefault((sample['id'],sample['page']),sample)
    assert set(unique)=={(p['id'],p['page']) for p in expected},('missing',[(p['id'],p['page']) for p in expected if (p['id'],p['page']) not in unique])
    ROOT.mkdir();sheets=[];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    selected=[unique[p['id'],p['page']] for p in expected]
    for first in range(0,len(selected),6):
        group=selected[first:first+6];sheet=Image.new('RGB',(1536,1600),'#eee');draw=ImageDraw.Draw(sheet)
        for index,sample in enumerate(group):
            x,y=index%3*512,index//3*800
            draw.text((x+4,y+4),sample['id'].replace('DK4_MES_','')+' p'+str(sample['page'])+' actor'+str(sample['selector']),font=font,fill='black')
            picture=Image.open(sample['capture']['path']).convert('RGB').resize((512,768),Image.Resampling.NEAREST)
            sheet.paste(picture,(x,y+28))
        png=ROOT/f'focused_QA_{len(sheets)+1}.png';sheet.save(png);sheets.append(dict(path=str(png),sha256=sha(png.read_bytes()),pages=len(group)))
    save(ROOT/'focused_actual_pixels.json',dict(frames=10001,selected_utterances=16,selected_pages=18,complete_body_planes=len(samples),
        body_pages=samples,ordered_selected_source_calls=[dict(frame=r['frame'],id=p['id'],page=p['page']) for r,p in zip(target,expected,strict=True)],
        all_selected_pages_observed_in_exact_fixture_order=True,all_selected_complete_native_body_planes_andblank_guards_match=True,
        two_page_boundaries_andFU_andtwo_ASCII_I_andfour_wrap_cases_covered=True,review_sheets=sheets,direct_visual_review_pending=True,
        name_headers_present_in_captures_butnot_yet_independently_pixel_bound=True,
        unvisited_utterances=159,all175_conversations_reviewed_offline_not_naturally_played=True,
        natural_activation=False,original_location=False,earned_chronology=False,full_route=False,hardware=False,
        following_nonfixture_modal_frame=end,actual_gameplay=True,disclosed_initialized_fixture=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,TERMINAL,NATIVE,reportpath,observerpath,Path(__file__)]}))
    print('16 selected utterances/18 ordered pages/',len(samples),'complete body planes pass;three QA sheets andheader review pending.')
