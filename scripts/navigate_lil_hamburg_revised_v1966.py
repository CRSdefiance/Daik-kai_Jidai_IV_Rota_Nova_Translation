"""Revised B74 progressive/FE holds, native choice and original join transition."""
import json
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import navigate_lil_crew_v1759b as prior
from scripts.calibrate_lil_speyer_choice_v1939 import planes, verify as verify_menu
from scripts.prepare_lil_hamburg_research_v1961 import ROM
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_revised_navigation_v1966')
RUN = Path('work/analysis/lil_Hamburg_revised_run_v1965')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY')
JOURNAL = RUN/'navigation.jsonl'
snapshot = FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})


def append(command):
    with JOURNAL.open('a',encoding='utf-8') as stream: stream.write(json.dumps(command)+'\n')


if __name__ == '__main__':
    assert not ROOT.exists()
    original = read('work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json')
    expected_ids = set(original['unique_observed_record_IDs'])
    assert len(expected_ids) == 79
    mapping = read('work/analysis/lil_Hamburg_relocation_v1960/nested_source_relocation_research.json')['blocks'][0]
    assert mapping['block'] == 74
    by_offset = {r['new_offset']-5:r for r in mapping['text_records']}
    fonts = {r['id']:r for r in read('work/analysis/lil_Hamburg_font_approval_v1959/all79_complete_native_font_and_macro_reconciliation.json')['cases']}
    calibration = read('work/analysis/lil_Hamburg_choice_calibration_v1964/original_current_menu_fixed_margin_calibration.json')
    assert calibration['calibrated_only_from_original_menu_before_revised_pixels']
    ui = read('work/analysis/lil_Hamburg_choice_v1958/original_choice_decoder_VM_geometry_and_native_pixels.json')
    menu = next(r for r in ui['current_and_reviewed_VM_and_font_cases'] if r['version'] == 'reviewed-research')
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    menu_planes = planes(arm,menu)
    wrapped = struct.unpack_from('<I',arm,0x54450)[0]
    source_join = original['original_art_pauses'][0]
    old_join = Image.open(source_join['holds'][1]['capture']).convert('RGB')
    join_ink = {(x,y) for y in range(192,384) for x in range(256) if old_join.getpixel((x,y)) == (0,8,0)}
    assert join_ink
    ROOT.mkdir(parents=True)
    frame = 49440
    holds, choices, joins = [], [], []
    for step in range(95):
        raw, im, progress, photo = snapshot(frame)
        pending = [progress['rows'][i] for i in progress['pending'].values()]
        active = [r for r in pending if r['source'].get('route') == 2 and r['source'].get('block') == 74]
        if not active:
            ends = [r for r in progress['rows'] if r['kind'] == 'after_command' and r['source'].get('route') == 2
                and r['source'].get('block') == 74 and r['source']['first_word'] == 0]
            assert ends and {r['id'] for r in holds} == expected_ids and len(choices) == len(joins) == 1
            assert sum(r['prefix_hex'] == 'fe' for r in holds) == 3
            save(ROOT/'closed_revised_B74_unit_and_normal_Hamburg_return.json',dict(research_ROM=str(ROM),
                research_ROM_sha256=sha(ROM.read_bytes()),terminal_frame_requested=frame,holds=holds,choices=choices,joins=joins,
                original_B74_end=ends[-1],terminal_capture=str(photo),terminal_capture_sha256=sha(photo.read_bytes()),
                all79_activated_revised_speeches158_holds_complete_native_independent_actual_ink=True,
                all3_FE_panels_six_actual_holds_match_separate_paper_planes=True,
                both_revised_choice_labels_two_holds_complete_native_actual_ink=True,
                original_join_command_and_complete_bottom_screen_ink_preserved=True,
                alternate_choice1_not_played=True,not_registered_candidate_or_editorial_completion=True,
                producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
            append({'stop':True})
            print(dict(revised_B74_closed=True,speeches=79,complete_speech_holds=158,FE_holds=6,choice_holds=2,join_holds=2,frame=frame),flush=True)
            break
        assert len(active) == 1
        src = active[0]['source']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256'] == mapping['research_block_sha256']
        at = src['payload_address']-0x02000000
        assert sha(raw[at:at+src['payload_bytes']]) == mapping['research_block_sha256']
        assert src['first_word'] in (0x4000,0x2100,0xa000),('Unknown pending command; left paused',src)
        choice, join = src['first_word'] == 0x2100, src['first_word'] == 0xa000
        spec = None
        if choice:
            assert not choices and src['instruction_offset'] == mapping['choice_commands'][0]['new_offset']
        elif join:
            assert not joins
            actual_join = raw[at+src['instruction_offset']:at+src['instruction_offset']+8]
            assert actual_join.hex() == source_join['original_non_speech_command_hex'] == '00a0ffff10100120'
        else:
            spec = by_offset[src['instruction_offset']]
            assert spec['id'] not in {r['id'] for r in holds},('Unexpected pagination; left paused',spec['id'])
            expected = Image.open(fonts[spec['id']]['preview']).convert('RGB')
            width = 228 if spec['target_hex'].startswith('fe') else 216
            assert expected.size == (width,64)
            wanted = {(16+x,296+y) for y in range(64) for x in range(width) if expected.getpixel((x,y)) == (0,8,0)}
        group = []
        for hold in range(2):
            raw, im, progress, photo = snapshot(frame)
            assert any(progress['rows'][i]['source'] == src for i in progress['pending'].values())
            if choice:
                menu_proof = verify_menu(im,menu,menu_planes)
            elif join:
                actual = {(x,y) for y in range(192,384) for x in range(256) if im.getpixel((x,y)) == (0,8,0)}
                assert actual == join_ink,('Original join ink differs; left paused',frame)
            else:
                actual = {(x,y) for y in range(296,360) for x in range(16,16+width) if im.getpixel((x,y)) == (0,8,0)}
                if actual != wanted:
                    save(ROOT/'glyph_mismatch_observation.json',dict(id=spec['id'],frame=frame,source=src,
                        missing_pixels=len(wanted-actual),extra_pixels=len(actual-wanted),run_left_paused_no_A_advance=True))
                    raise AssertionError('Incomplete revised glyph hold; left paused')
                if width == 216:
                    target = bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
                    assert cstring(raw,wrapped) == target
            at = src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']]) == mapping['research_block_sha256']
            group.append(dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw),
                source=src,complete_native_independent_actual_ink_equal=not join,
                original_join_complete_bottom_ink_equal=join,menu_proof=menu_proof if choice else None))
            if hold == 0: append(dict(until=frame+30,duration=1)); frame += 30
        if choice: choices.append(dict(source=src,holds=group,ordinary_A_selects_original_default0=True))
        elif join: joins.append(dict(source=src,holds=group,original_join_command_hex='00a0ffff10100120'))
        else: holds.append(dict(id=spec['id'],prefix_hex=spec['target_hex'][:2],
            consumer='original_FE_modal_5473C_mode1' if width == 228 else 'original_progressive_54020',holds=group))
        save(ROOT/'verified_revised_holds_LIVE.json',dict(rows=holds,choices=choices,joins=joins,next_pause_frame=frame+300,not_terminal_or_complete_scene_proof=True))
        print(dict(verified_speeches=len(holds),id=spec['id'] if spec else ('typed-choice' if choice else 'original-join'),frame=frame),flush=True)
        append(dict(until=frame+300,buttons=['A'],duration=8))
        frame += 300
    else: raise AssertionError('Bounded revised navigation exhausted; left paused')
