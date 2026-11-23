"""Bind native page planes to every naturally displayed Deck lesson panel."""

from pathlib import Path
from types import FunctionType

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_london_guild_assignments_20261118 as layout
from scripts import stage_rafael_deck_after_trade_20261119 as build
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

base,native = build.base,build.native
replay = build.review.replay
ROOT = build.ROOT/'verified_display'
PROOF = ROOT/'native_and_ordinary_gameplay.json'
STARTUP = build.ROOT/'own_startup_verification.json'
SC0,FONT = '/data/SC0.DK4','/GRP/KANJI.FNT'
TOOL = layout.quest.prior.TOOL
CHANGED = {7,20,23}


def load_run(case, candidate, expected, evidence):
    folder = replay.ROOT/case
    files = [folder/p for p in ('capture/capture_report.json','observer/commands.json','inputs.json','source_contract.json')]
    report,trace,inputs,_ = map(base.load,files)
    assert report['ROM_sha256'] == candidate and report['frames'] == replay.END
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key,value in report.items() if key.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == inputs
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == base.digest(donor['source'])
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    assert not trace['unreturned_at_capture_end']
    observed = [r for r in trace['rows'] if r['kind'] == 'after_command' and r['source'].get('block') == 43]
    assert len(observed) == 16
    for returned in observed:
        entered = trace['rows'][returned['entry_row']]
        assert entered['kind'] == 'before_command'
        for row in (entered,returned):
            source = row['source']
            assert (source['classification'],source['route'],source['block']) == ('original_SC_cache',0,43)
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256'] == source['registered_sha256'] == expected
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        assert returned['source']['instruction_offset'] == entered['source']['instruction_offset']
    returned = observed[-1]
    assert returned['source']['first_word'] == 0 and returned['result_words'][0] == 0
    evidence.update({str(p):base.digest(p) for p in files})
    return report, trace['rows'], observed


def pixel_page(arm, cjk, paint, raw):
    selector = raw[5]
    text = raw[6:raw.index(0,6)]
    if b' FI.' in text:
        assert selector == 6 and text.count(b' FI.') == 1
        text = text.replace(b' FI.',b' Rafael.')
    output = paint(arm,cjk,text)
    assert output['complete_consumed_bytes'] == len(text)
    page, = output['pages']
    assert page['native_independent_plane_equal']
    plane = TOOL.prior.masks(bytes.fromhex(page['native_plane_hex']))
    return selector,text,page,plane


def match_page(entered, returned, photos, font, selector, expected):
    interval = range(entered['frame']+25,returned['frame']-4)
    for n, capture in sorted(photos.items()):
        if n not in interval:
            continue
        image = captured(capture)
        if TOOL.body_masks(image) != expected:
            continue
        if selector == 6:
            ink,bounds = complete_mask(font,'Julio Erneco',image,16,277,(98,97,98))
            header = dict(text='Julio Erneco',ink_pixels=ink,bounds=bounds)
        else:
            assert selector == 0xFE
            name_ink = (98,97,98)
            assert not any(image.getpixel((x,y)) == name_ink for x in range(16,100) for y in range(277,288))
            header = None
        result = dict(frame=n,capture=capture['path'],sha256=capture['PNG_sha256'],speaker=header,
                      exact_first_internal_final_glyphs_and_clear_cells=True)
        return result,image
    raise AssertionError((entered['frame'],returned['frame'],selector,'complete dialogue page mask missing'))


def main():
    assert not ROOT.exists()
    staged,draft = map(base.load,(build.PROOF,build.review.OUTPUT))
    assert base.digest(build.ROM) == staged['candidate_sha256'] and staged['whole_parent_inverse']
    assert base.digest(build.parent.ROM) == staged['predecessor_sha256']
    assert base.digest(build.review.OUTPUT) == staged['manuscript_sha256']
    before,after = map(base.NdsImage.open,(build.parent.ROM,build.ROM))
    for path in (native.ARM,FONT,'/COMMON/MESFILE.DK4'):
        assert before.read_file(path) == after.read_file(path)
    arm,cjk = after.read_file(native.ARM),after.read_file(FONT)
    _, paint = build.stage.progressive.layout.prior.precedent.planners(arm)
    font = GameAsciiFont.from_arm9(arm)
    group, = staged['groups']
    source = native.IlnkContainer.parse(before.read_file(SC0)).blocks[43]
    target = native.IlnkContainer.parse(after.read_file(SC0)).blocks[43]
    assert native.digest(source) == group['before'] and native.digest(target) == group['after']
    evidence = {str(p):base.digest(p) for p in (build.PROOF,build.review.OUTPUT,replay.PRIOR,Path(__file__))}
    reports = [load_run(name,digest,packet,evidence) for name,digest,packet in (
        ('current',staged['predecessor_sha256'],group['before']),('corrected',staged['candidate_sha256'],group['after']))]
    assert reports[0][0]['scripted_input_schedule'] == reports[1][0]['scripted_input_schedule']
    assert reports[0][0]['core_options'] == reports[1][0]['core_options']
    assert reports[0][0]['battery_save_preloaded']['source_sha256'] == reports[1][0]['battery_save_preloaded']['source_sha256']
    photos = [shots(run[0]) for run in reports]
    indexed = {r['id']:r for r in draft['records']}
    lessons, samples = [], []
    for ordinal, command in enumerate(group['commands']):
        word = command['word']
        raws = []
        for block,side in ((source,'current'),(target,'stored')):
            raw = bytes.fromhex(command[side])
            start = command[side+'_offset']
            assert raw == block[start:start+len(raw)]
            raws.append(raw)
        for run,key in zip(reports,('current','stored'),strict=True):
            series = run[2][ordinal]
            assert series['source']['instruction_offset'] == command[key+'_offset']
            assert series['source']['first_word'] == word
        if word != 0x4000:
            assert raws[0] == raws[1] and not command['record_ids']
            continue
        ident, = command['record_ids']
        r = indexed[ident]
        assert raws[0][:6] == raws[1][:6] and raws[1][5] == r['source_selector']
        pages = []
        for raw,run,frames in zip(raws,reports,photos,strict=True):
            selector,body,native_page,expected = pixel_page(arm,cjk,paint,raw)
            returned = run[2][ordinal]
            entered = run[1][returned['entry_row']]
            hold,image = match_page(entered,returned,frames,font,selector,expected)
            evidence[hold['capture']] = hold['sha256']
            pages.append((dict(**hold,body_hex=body.hex(),native_plane_sha256=native.digest(bytes.fromhex(native_page['native_plane_hex']))),image))
        revision = r['source_reference']['record_index'] in CHANGED
        assert revision == (r['decision'] == 'revision')
        if revision:
            assert pages[0][0]['native_plane_sha256'] != pages[1][0]['native_plane_sha256']
            plan = group['plans'][ident]
            if r['source_reference']['record_index'] == 7:
                assert any("I'll show you" in line for line in plan['lines'])
            if r['source_reference']['record_index'] == 20:
                assert any('Each mast needs one.' in line for line in plan['lines'])
            if r['source_reference']['record_index'] == 23:
                assert any('count on your Helmsman.' in line for line in plan['lines'])
            samples.append((ident,pages[0][1],pages[1][1]))
        else:
            assert raws[0] == raws[1] and pages[0][0]['native_plane_sha256'] == pages[1][0]['native_plane_sha256']
        lessons.append(dict(id=ident,revision=revision,previous=pages[0][0],current=pages[1][0],command=command))
    assert len(lessons) == 12 and len(samples) == 3
    captain = next(r for r in lessons if r['id']=='DK4_MES_B43_R0017')
    assert bytes.fromhex(captain['current']['body_hex']).startswith(b"First, you're the captain, Rafael.")
    assert lessons[-1]['current']['speaker'] is None
    exits = [run[2][-1]['frame'] for run in reports]
    assert exits[0] == exits[1] and exits[0] < 15961
    following = [captured(run[15961]) for run in photos]
    assert ImageChops.difference(*following).getbbox() is None
    assert following[1].getpixel((1,199)) == following[0].getpixel((1,199))
    evidence.update({run[15961]['path']:run[15961]['PNG_sha256'] for run in photos})

    ROOT.mkdir()
    sheet = Image.new('RGB',(1024,3*404),'#263238')
    draw = ImageDraw.Draw(sheet)
    for row,(ident,a,b) in enumerate(samples):
        for col,(photo,caption) in enumerate(((a,'Previous'),(b,'Revised'))):
            x,y=col*512,row*404
            draw.text((x+4,y+4),f'{ident} / {caption}',fill='white')
            sheet.paste(photo.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+18))
    picture = ROOT/'ordinary_deck_comparison.png'
    sheet.save(picture)
    evidence[str(picture)] = base.digest(picture)
    base.save(PROOF,dict(candidate_sha256=staged['candidate_sha256'],predecessor_sha256=staged['predecessor_sha256'],
        ordinary_gameplay_existing_save=True,native_lesson_event_after_Trade=True,hardware=False,speakerless_system_page_exact=True,
        pairs=lessons,command_count=16,tutorial_exit_frames=exits,normal_Lisbon_return_frame=15961,
        fully_displayed_live_name_and_regular_F=True,sheets=[dict(path=str(picture),sha256=evidence[str(picture)])],evidence=evidence))
    print('Both ordinary replays show all 12 native pages, the live captain name and the normal tutorial return.')


if __name__ == '__main__':
    main()
