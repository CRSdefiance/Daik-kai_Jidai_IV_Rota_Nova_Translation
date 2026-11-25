"""Actual request pixels, both original responses and post-answer state."""

from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageChops
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_specialty_fixture_v752 import assign
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.prepare_specialty_question_v752 import ROOT
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read, save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SAVE_SHA = 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'


def snapshot(report, frame):
    row = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == frame)
    raw = Path(row['path']).read_bytes()
    assert len(raw) == 4194304 and sha(raw) == row['sha256']
    return raw


def captures(folder, frames, fixture):
    report = read(CAP / folder / 'capture_report.json')
    assert report['frames'] == frames and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification']
    assert report['core_DLL_sha256'] == '42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
    assert sha(Path(report['ROM']).read_bytes()) == report['ROM_sha256']
    fixtures = report.get('synthetic_specialty_inventory_fixtures', [])
    assert len(fixtures) == int(fixture)
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k != 'synthetic_specialty_inventory_fixtures')
    if fixture:
        donor = report['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256'] == SAVE_SHA
        assert donor['copied_byte_exact_before_cold_boot'] and donor['source'] != donor['destination']
        arm = NdsImage.open(report['ROM']).read_file('/__arm9__.bin')
        _, receipt = assign(arm,snapshot(report,3200),{'item':4})
        assert fixtures[0]['frame'] == 3200 and receipt == {k:v for k,v in fixtures[0].items() if k != 'frame'}
        assert len(receipt['changes']) == 1
        adapter = report['controlled_specialty_harness_adapter']
        assert adapter['original_harness_file_unchanged']
        assert adapter['adapter_sha256'] == sha(Path('scripts/run_specialty_capture_v752.py').read_bytes())
        assert adapter['unchanged_original_harness_sha256'] == sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    else:
        assert not report.get('battery_save_preloaded')
    rows = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        rows[row['frame']] = row
    return report,rows


def main():
    rom = NdsImage.open('out/all_routes_combined_v752_candidate.nds')
    arm, common = rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries = common_message_entries(common,arm,clean=False)
    cpu = machine(arm)
    cpu.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]))
    font = GameAsciiFont.from_arm9(arm)
    block = IlnkContainer.parse(common).blocks[9]
    report_paths, checks, controls, states, responses = [],[],{},[],[]

    def text_pixels(picture, lines, body):
        expected = set()
        for row,line in enumerate(lines):
            for column,char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x,y)):
                            expected.add((22+column*6+x,296+row*16+y))
        actual = {(x,y) for y in range(body[1],body[3]) for x in range(body[0],body[2]) if picture.getpixel((x,y)) == (0,8,0)}
        assert actual == expected,(len(actual-expected),len(expected-actual),lines)

    for answer in ('decline','accept'):
        old,before = captures(f'specialty_v752_{answer}_751_final',6501,True)
        new,after = captures(f'specialty_v752_{answer}_752_final',6501,True)
        assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and set(before) == set(after)
        assert old['core_options'] == new['core_options']
        controls[answer] = []
        for frame in sorted(after):
            a,b = (Image.open(rows[frame]['path']).convert('RGB') for rows in (before,after))
            diff = ImageChops.difference(a,b)
            if frame not in (4200,4400,4600,4800):
                assert diff.getbbox() is None,(answer,frame,diff.getbbox())
                if frame in (5000,5200,5400,5600):
                    number = 743 if answer == 'accept' else 744
                    _,lines = native_layout(cpu,entries[number].text,number,())
                    text_pixels(b,lines,(16,294,244,366))
                    responses.append({'answer':answer,'frame':frame,'message_id':number,'lines':lines,
                        'every_glyph_and_blank_cell_exact':True,'capture':after[frame]})
                controls[answer].append(frame)
                continue
            _,lines = native_layout(cpu,entries[742].text,742,('Baby Shark','Caviar'),parent=0x02053FCC)
            body=(16,294,244,360)
            text_pixels(b,lines,body)
            diff.paste((0,0,0),body)
            assert diff.getbbox() is None,(answer,frame,diff.getbbox())
            ram=snapshot(new,frame)
            assert ram.count(block) == 1
            checks.append({'answer':answer,'frame':frame,'message_id':742,'lines':lines,'capture':after[frame],
                'every_glyph_blank_cell_yes_no_control_and_outside_pixel_exact':True,'entire_unique_resident_block9_exact':True})
        # Check observed post-answer object state, independently through the
        # original getters, after the acceptance/refusal text has appeared.
        state=[]
        for report in (old,new):
            u=machine(arm);u.mem_write(BASE,snapshot(report,5200))
            call(u,0xCB190,());item=u.reg_read(UC_ARM_REG_R0)+4+4*20
            call(u,0x4A224,(item,));available=u.reg_read(UC_ARM_REG_R0)
            call(u,0xB6618,());town=u.reg_read(UC_ARM_REG_R0)
            call(u,0xB3B58,(town,0));specialty=u.reg_read(UC_ARM_REG_R0)
            state.append({'available_item_bit':available,'original_town_slot_specialty_bit':specialty})
        assert state[0] == state[1]
        assert state[1] == {'available_item_bit':0 if answer=='accept' else 4,'original_town_slot_specialty_bit':0 if answer=='accept' else 1}
        states.append({'answer':answer,'state_at5200':state[1],
            'original_response_message':743 if answer=='accept' else 744,'response_full_frames_match':True})
        report_paths += [str(CAP/f'specialty_v752_{answer}_{version}_final/capture_report.json') for version in (751,752)]
    game,game_rows=captures('specialty_v752_newgame',4000,False)
    old,old_rows=captures('responses_v751_newgame',4000,False)
    assert game['scripted_input_schedule'] == old['scripted_input_schedule']
    equal=sorted(set(game_rows)&set(old_rows))
    assert equal == [1,60,180,3200,4000]
    assert all(Path(game_rows[f]['path']).read_bytes() == Path(old_rows[f]['path']).read_bytes() for f in equal)
    protected=Path('E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv')
    disposable=Path('E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')
    assert sha(protected.read_bytes()) == sha(disposable.read_bytes()) == SAVE_SHA
    save(ROOT/'gameplay_verification.json',{'candidate':'out/all_routes_combined_v752_candidate.nds','candidate_sha256':game['ROM_sha256'],
        'four_terminal6501_frame_paired_cold_boots':True,'one_byte_disposable_inventory_fixture':True,
        'actual_complete_question_holds':checks,'actual_complete_response_holds':responses,
        'unchanged_full_frame_controls':controls,'original_post_answer_states':states,
        'ordinary_no_save_no_fixture_New_Game_4000_frame':True,'whole_frame_New_Game_baseline_controls':equal,
        'additional_New_Game_visually_inspected_frames':{'1600':'intro narration','2000':'captain selection'},
        'protected_and_disposable_source_saves_unchanged':{'protected':str(protected),'disposable':str(disposable),'sha256':SAVE_SHA},
        'capture_reports':report_paths,'whole_routes_hardware_and_earned_item_acquisition_not_claimed':True,
        'verifier_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V752 question, both source response/state paths, controls and ordinary New Game verified.',flush=True)


if __name__ == '__main__':
    main()
