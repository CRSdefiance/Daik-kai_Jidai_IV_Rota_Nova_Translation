"""Verify both complete status fields, their runtime storage and clean reconstruction."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_inn_numerals_20261119 as verification
from scripts import stage_town_shortage_20261119 as stage
from scripts.verify_captain_biographies_v1 import captured, shots

base, inn = stage.base, verification.inn
STARTUP = stage.ROOT/'own_startup'
STARTUP_PROOF = stage.ROOT/'own_startup_verification.json'
PLAYBACK = stage.ROOT/'verified_shortage.json'
SHEET = stage.ROOT/'shortage_comparison.png'


def mask(image,font,text,field, color):
    x0,y0,x1,y1 = field
    ink = {(x0+6*i+x,y0+1+y) for i,char in enumerate(text) for x in range(6) for y in range(11)
           if font.decode(char).getpixel((x,y))}
    visible = {(x,y) for x in range(x0,x1) for y in range(y0,y1) if image.getpixel((x,y)) == color}
    assert ink and visible == ink, (text,field,len(ink-visible),len(visible-ink))
    return dict(text=text,rectangle=field,complete_ink_pixels=len(ink))


def read_run(case, candidate, evidence):
    version = 3 if case == 'corrected' else 2
    folder = stage.replay.ROOT/f'{case}_{stage.replay.PAUSE}_v{version}'
    files = [folder/'capture_report.json',folder/'navigation_command_journal.json',
             folder.with_name(folder.name+'_stack')/'requests.json']
    report, commands, trace = map(base.load,files)
    assert report['ROM_sha256'] == candidate and report['frames'] == 11600
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == base.digest(donor['source'])
    changed, = report['synthetic_condition_fixtures']
    assert changed['frame'] == stage.replay.PAUSE and changed['town_index'] == 11
    assert changed['changes'] == [dict(address=changed['town_address']+0x6A,before=12,after=7)]
    assert not report['natural_condition_event_verified']
    assert all(command['validation_passed'] for command in commands['commands_received'])
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    rows = {row['PC']:row for row in trace['rows']}
    open_, ready, build, show = (rows[pc] for pc in (stage.replay.TRADE_INIT,stage.replay.FRAME_READY,stage.replay.BITMAP_ALLOC,stage.replay.SHOW))
    did_fix = case == 'corrected'
    take = stage.TRADE_FRAME + (stage.NEW_BITMAP_BYTES if did_fix else 0)
    assert open_['sp']-ready['sp'] == 24+take
    width = stage.WIDTH if did_fix else stage.SOURCE_WIDTH
    assert build['width_height'] == [width,stage.HEIGHT]
    hdr = build['header_fields']
    assert hdr[:3] == [4,width//4,stage.HEIGHT]
    pixels = (build['bitmap_header'] + hdr[4]) & 0xFFFFFFFF
    assert build['bitmap_header'] == build['trade_object']+0xBAC
    assert pixels == build['trade_object']+(stage.TRADE_FRAME-stage.OBJECT_OFFSET if did_fix else 0xAD4)
    assert build['trade_object'] == ready['sp']+stage.OBJECT_OFFSET
    end = pixels+width*stage.HEIGHT//2
    assert ready['sp'] <= pixels < end <= open_['sp']-24
    assert show['destination'] == [64,166,112 if did_fix else 100,178]
    lower = [row['sp'] for row in rows.values()]
    assert min(lower) >= 0x02000000 and max(lower) <= 0x02400000
    evidence.update({str(p):base.digest(p) for p in files})
    return report, rows


def verify():
    assert not PLAYBACK.exists() and not SHEET.exists()
    proof = base.load(stage.PROOF)
    evidence = {}
    old, old_trace = read_run('baseline',proof['parent_sha256'],evidence)
    new, fixed_trace = read_run('corrected',proof['candidate_sha256'],evidence)
    assert new['ROM_sha256'] == base.digest(stage.ROM)
    for key in ('core_options','core_DLL_sha256','scripted_input_schedule','synthetic_condition_fixtures'):
        assert old[key] == new[key]
    before, after = map(shots,(old,new))
    assert before.keys() == after.keys()
    gamefont = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    hits = []
    seen = {}
    expected = {3200:'Town',9200:'Town',9600:'Town',10400:'Local',11600:'Cargo'}
    for frame in sorted(before):
        a,b = (captured(s[frame]) for s in (before,after))
        difference = ImageChops.difference(a,b)
        if not difference.getbbox():
            continue
        view = expected[frame]
        x,y,color = (76,62,(230,230,230)) if view=='Town' else (64,166,(230,230,230))
        region = (x,y,x+stage.WIDTH,y+stage.HEIGHT)
        difference.paste((0,0,0),region)
        assert difference.getbbox() is None,(frame,difference.getbbox())
        old_mask,new_mask = (mask(photo,gamefont,text,region,color) for photo,text in ((a,'Shorta'),(b,'Shortage')))
        hits.append(dict(frame=frame,view=view,original=old_mask,corrected=new_mask))
        seen[view] = (a,b)
        evidence.update({s[frame]['path']:s[frame]['PNG_sha256'] for s in (before,after)})
    assert set(seen) == {'Town','Local','Cargo'}
    sheet = Image.new('RGB',(1024,1206),'#263238')
    draw = ImageDraw.Draw(sheet)
    for row,view in enumerate(('Town','Local','Cargo')):
        for col,(img,heading) in enumerate(zip(seen[view],('Original','Corrected'),strict=True)):
            left,top = col*512,row*402
            draw.text((left+5,top+3),f'{view} / {heading}',fill='white')
            sheet.paste(img.crop((0,0,256,192)).resize((512,384),Image.Resampling.NEAREST),(left,top+18))
    sheet.save(SHEET)
    evidence[str(SHEET)] = base.digest(SHEET)
    evidence[str(Path(__file__))] = base.digest(__file__)
    base.save(PLAYBACK,dict(candidate_sha256=proof['candidate_sha256'],prior_sha256=proof['parent_sha256'],
        ordinary_input_after_one_Lisbon_status_fixture=True,hardware=False,natural_shortage_observed=False,
        case_frames=hits, pixels_outside_status_exact=True, exact_original_bounded_trade_allocation=old_trace,
        exact_widened_bounded_trade_allocation=fixed_trace,
        sheets=[dict(path=str(SHEET),sha256=evidence[str(SHEET)])],evidence=evidence))
    print('Complete Shortage masks and exact surrounding pixels pass in Town Summary and both Trade views.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('startup','patch','verify'))
    action = parser.parse_args().action
    if action == 'verify':
        verify()
    else:
        task = getattr(verification,action)
        FunctionType(task.__code__,vars(verification)|globals())()
