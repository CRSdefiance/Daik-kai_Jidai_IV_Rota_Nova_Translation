"""Actual Market intro/amount/thanks/error text and original post-dialogue state."""

from pathlib import Path

from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_market_fixture_v753 import assign
from scripts.prepare_market_replies_v753 import ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read, save

CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SAVE_SHA='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'


def snapshot(report,frame):
    row=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==frame)
    raw=Path(row['path']).read_bytes();assert len(raw)==4194304 and sha(raw)==row['sha256'];return raw


def captures(folder,frames,mode=None,donor=True):
    report=read(CAP/folder/'capture_report.json')
    assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256']=='42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes())==report['ROM_sha256']
    fixtures=report.get('synthetic_market_display_fixtures',[])
    assert len(fixtures)==int(mode is not None)
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_market_display_fixtures')
    if donor:
        save_info=report['battery_save_preloaded'];assert save_info['source']!=save_info['destination']
        assert sha(Path(save_info['source']).read_bytes())==save_info['source_sha256']==SAVE_SHA
        assert save_info['copied_byte_exact_before_cold_boot']
    else:assert not report.get('battery_save_preloaded')
    if mode:
        arm=NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        _,receipt=assign(arm,snapshot(report,3200),{'mode':mode})
        assert fixtures[0]['frame']==3200 and receipt=={k:v for k,v in fixtures[0].items() if k!='frame'}
        adapter=report['controlled_market_harness_adapter'];assert adapter['original_harness_file_unchanged']
        assert adapter['adapter_sha256']==sha(Path('scripts/run_market_capture_v753.py').read_bytes())
        assert adapter['unchanged_original_harness_sha256']==sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    rows={}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256'];rows[row['frame']]=row
    return report,rows


def state(arm,raw):
    u=machine(arm);u.mem_write(BASE,raw)
    def get(fn,args=()):call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);root=get(0xCB160);company=get(0x397D8,(root,))
    return {'cash':get(0x3CCC8,(root+4+company*0x4c,)),
        'share':get(0xB4AA8,(town,company)),'investment_accumulator':get(0xB3FC8,(town,0)),
        'growth':get(0xB3FD4,(town,0)),'minimum_investment':get(0xB3FA4,(town,0))}


def main():
    rom=NdsImage.open('out/all_routes_combined_v753_candidate.nds');arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=common_message_entries(common,arm,clean=False);blocks=IlnkContainer.parse(common).blocks
    font=GameAsciiFont.from_arm9(arm);native=read(ROOT/'native_review.json')
    layouts={r['message_id']:r['generated_lines'] for r in native['all9_complete_font_planes']}
    checks,controls,states,reports,blink_controls=[],{},[],[],[]
    for mode,old_folder,new_folder in (
        ('share','market_v753_share_baseline','market_v753_share_probe'),
        ('low_funds','market_v753_low_funds_baseline','market_v753_low_funds_probe'),
        (None,'market_v753_ordinary_752','market_v753_ordinary_753')):
        old,before=captures(old_folder,7501,mode);new,after=captures(new_folder,7501,mode)
        assert old['scripted_input_schedule']==new['scripted_input_schedule'] and old['core_options']==new['core_options']
        assert set(before)==set(after);name=mode or 'ordinary';controls[name]=[]
        extra_rows=None
        if mode=='low_funds':
            extra,extra_rows=captures('market_v753_low_funds_blink_baseline',7501,mode)
            assert extra['scripted_input_schedule']==old['scripted_input_schedule'] and extra['core_options']==old['core_options']
            assert Path(extra_rows[6400]['path']).read_bytes()==Path(before[6400]['path']).read_bytes()
            reports.append(str(CAP/'market_v753_low_funds_blink_baseline/capture_report.json'))
        selected={f:763 if mode=='share' else 762 for f in (4800,5000,5200)}
        selected.update({f:748 if mode=='low_funds' else 747 for f in ((5400,5600) if mode=='low_funds' else (5800,6000,6200))})
        for frame in sorted(after):
            a,b=(Image.open(rows[frame]['path']).convert('RGB') for rows in (before,after));diff=ImageChops.difference(a,b)
            if frame not in selected:
                if mode=='low_funds' and frame in (6000,6200):
                    paired=5800 if frame==6000 else 6000
                    other=Image.open(before[paired]['path']).convert('RGB')
                    assert diff.getbbox()==(95,258,161,278)
                    assert ImageChops.difference(other,b).getbbox() is None
                    blink_controls.append({'scenario':name,'current_frame':frame,'baseline_frame':paired,
                        'entire_two_screen_image_exact_at_matching_highlight_phase':True,
                        'same_frame_difference_confined_to_Trade_highlight':list(diff.getbbox())})
                    continue
                if mode=='low_funds' and frame==6400:
                    other=Image.open(extra_rows[6401]['path']).convert('RGB')
                    assert diff.getbbox()==(7,242,51,258)
                    assert ImageChops.difference(other,b).getbbox() is None
                    blink_controls.append({'scenario':name,'current_frame':6400,'baseline_frame':6401,
                        'baseline_capture':'market_v753_low_funds_blink_baseline',
                        'entire_two_screen_image_exact_at_matching_highlight_phase':True,
                        'same_frame_difference_confined_to_Market_caption':list(diff.getbbox())})
                    continue
                assert diff.getbbox() is None,(name,frame,diff.getbbox());controls[name].append(frame);continue
            number=selected[frame];lines=layouts[number];expected=set()
            for row,line in enumerate(lines):
                for col,char in enumerate(line):
                    glyph=font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x,y)):expected.add((22+col*6+x,296+row*16+y))
            body=(16,294,244,366)
            actual={(x,y) for y in range(body[1],body[3]) for x in range(body[0],body[2]) if b.getpixel((x,y))==(0,8,0)}
            assert actual==expected,(name,frame,number,len(actual-expected),len(expected-actual))
            diff.paste((0,0,0),body);assert diff.getbbox() is None,(name,frame,diff.getbbox())
            block=blocks[entries[number].block];assert snapshot(new,frame).count(block)==1
            checks.append({'scenario':name,'frame':frame,'message_id':number,'lines':lines,'capture':after[frame],
                'all_glyphs_blank_cells_and_outside_pixels_exact':True,'unique_entire_resident_block_exact':True})
        observed=[]
        for report in (old,new):observed.append({str(f):state(arm,snapshot(report,f)) for f in (3400,6200,6400,7200)})
        assert observed[0]==observed[1]
        initial,held,post=(observed[1][str(f)] for f in (3400,6200,7200))
        assert initial['cash']==(0 if mode=='low_funds' else 8371) and initial['share']==int(mode=='share')
        assert held['cash']==initial['cash'] and held['investment_accumulator']==initial['investment_accumulator']
        amount=0 if mode=='low_funds' else initial['minimum_investment']
        assert amount in (0,2684) and post['cash']==initial['cash']-amount
        assert post['investment_accumulator']==initial['investment_accumulator']+amount
        states.append({'scenario':name,'before_during_and_after':observed[1],
            'cash_and_accumulator_update_only_after_blocking_thanks_closes':True,'actual_investment_amount':amount})
        reports.extend([str(CAP/f/'capture_report.json') for f in (old_folder,new_folder)])
    game,game_rows=captures('market_v753_newgame',4000,donor=False)
    old,old_rows=captures('specialty_v752_newgame',4000,donor=False)
    assert game['scripted_input_schedule']==old['scripted_input_schedule'] and set(game_rows)==set(old_rows)
    assert all(Path(game_rows[f]['path']).read_bytes()==Path(old_rows[f]['path']).read_bytes() for f in game_rows)
    protected=Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv')
    disposable=Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')
    assert sha(protected.read_bytes())==sha(disposable.read_bytes())==SAVE_SHA
    save(ROOT/'gameplay_verification.json',{'candidate':'out/all_routes_combined_v753_candidate.nds','candidate_sha256':game['ROM_sha256'],
        'six_terminal7501_frame_paired_Market_cold_boots':True,'ordinary_zero_fixture_and_two_declared_two_byte_scenarios':True,
        'actual_complete_dialogue_holds':checks,'whole_frame_unchanged_controls':controls,
        'cross_frame_menu_blink_phase_controls':blink_controls,'original_post_dialogue_states':states,
        'ordinary4000_frame_New_Game_and7_full_baseline_frame_pairs':sorted(game_rows),
        'protected_and_disposable_save_source_sha256':SAVE_SHA,'source_saves_unchanged':True,'capture_reports':reports,
        'other_five_entries_have_source_native_font_coverage_not_claimed_actual_triggered_dialogue':True,
        'no_hardware_full_route_or_earned_fixture_progress_claim':True,'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V753 actual investment762/763/747/748,original state transitions,controls and New Game pass.',flush=True)


if __name__=='__main__':main()
