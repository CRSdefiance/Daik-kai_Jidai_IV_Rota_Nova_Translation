"""Audit B74 revised glyphs/FE/join/menu, source results and disclosed access."""
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.calibrate_lil_speyer_choice_v1939 import planes, verify as verify_menu
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Hamburg_revised_audit_v1967')
RUN = Path('work/analysis/lil_Hamburg_revised_run_v1965')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Hamburg_revised_run_v1965_RESEARCH_ONLY')
NAV = Path('work/analysis/lil_Hamburg_revised_navigation_v1966b/closed_revised_B74_unit_and_normal_Hamburg_return.json')
ORIGINAL = Path('work/analysis/lil_Speyer_original_audit_v1935b/original_Hamburg79_Speyer51_and_three_access_fixture_audit.json')
REF = Path('work/analysis/lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    # Reuse the complete frozen input/capture/4MiB/observer/fixture audit.
    source = Path('scripts/audit_lil_speyer_revised_v1941.py')
    prefix = source.read_text(encoding='utf-8').split('    mapping=next(')[0]
    for old,new in {
        'lil_Speyer_revised_audit_v1941':'lil_Hamburg_revised_audit_v1967',
        'lil_Speyer_revised_run_v1938':'lil_Hamburg_revised_run_v1965',
        'lil_Speyer_revised_navigation_v1940/closed_revised_B128_unit_and_normal_Hamburg_return.json':
            'lil_Hamburg_revised_navigation_v1966b/closed_revised_B74_unit_and_normal_Hamburg_return.json',
        'lil_Speyer_reference_census_v1931/all137_commands48_relative_sites_and_shipped_entry_census.json':
            'lil_Hamburg_reference_census_v1963/all123_commands20_relative_sites_and_shipped_entry_census.json',
    }.items():
        expected = 2 if old == 'lil_Speyer_revised_run_v1938' else 1
        assert prefix.count(old) == expected,(old,prefix.count(old))
        prefix = prefix.replace(old,new)
    env = {'__name__':'__main__','__file__':__file__}
    exec(compile(prefix,str(source),'exec'),env)
    plan, terminal, report, trace, nav, original, reference, frame, rom, digest, image, arm, photos, snapshots, replays = (
        env[k] for k in ('plan','terminal','report','trace','nav','original','reference','frame','rom','digest','image','arm','photos','snapshots','replays'))
    mapping = read('work/analysis/lil_Hamburg_relocation_v1960/nested_source_relocation_research.json')['blocks'][0]
    mapped = reference['blocks'][0]['mapped_commands']
    assert mapping['block'] == reference['blocks'][0]['block'] == 74 and len(mapped) == 123
    texts = {r['id']:r for r in mapping['text_records']}
    doc = read('translations/lil_hamburg_recruitment_editorial_manuscript_v3.json')
    fonts = {r['id']:r for r in read(doc['native_font_proof'])['cases']}
    target = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[74]
    assert sha(target) == mapping['research_block_sha256']
    by_offset = {r['new_offset']:r for r in mapped}
    rows = [r for r in trace['rows'] if r['source'].get('route') == 2 and r['source'].get('block') == 74]
    assert len(rows) == 232
    pairs, previous = [], 0
    for index,(before,after) in enumerate(zip(rows[::2],rows[1::2],strict=True)):
        src = before['source']
        spec = by_offset[src['instruction_offset']]
        assert before['kind'] == 'before_command' and after['kind'] == 'after_command' and src == after['source']
        assert trace['rows'][after['entry_row']] == before and src['first_word'] == spec['word']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256'] == mapping['research_block_sha256']
        if spec['word'] in (0x100,0x200,0x300):
            span = struct.unpack_from('<H',target,spec['new_offset']+2)[0]
            take = spec['word'] == 0x100 or (spec['word'] == 0x200 and previous == 0) or (spec['word'] == 0x300 and previous == 1)
            assert after['decoded_length'] == 4+(span if take else 0)
        else:
            assert after['decoded_length'] == spec['new_native_extent']
        if after['result_words'][0] == 2: previous = after['result_words'][1]
        if index+1 < len(rows)//2:
            assert rows[2*index+2]['source']['instruction_offset'] == src['instruction_offset']+after['decoded_length']
        pairs.append(dict(offset=src['instruction_offset'],word=spec['word'],frames=[before['frame'],after['frame']],
            native_decoded_length=after['decoded_length'],native_result_words=after['result_words']))
    prior_scene = next(r for r in original['scenes'] if r['block'] == 74)
    assert len(pairs) == len(prior_scene['original_command_pairs']) == 116
    for new,old in zip(pairs,prior_scene['original_command_pairs'],strict=True):
        assert by_offset[new['offset']]['old_offset'] == old['offset'] and new['word'] == old['word']
        assert new['native_result_words'] == old['native_result_words']
        new.update(original_observed_frames=old['frames'],observed_frame_delta=[a-b for a,b in zip(new['frames'],old['frames'],strict=True)])
    observed = []
    wrapped = struct.unpack_from('<I',arm,0x54450)[0]
    for group in nav['holds']:
        active = next((a,b) for a,b in zip(rows[::2],rows[1::2],strict=True) if a['source'] == group['holds'][0]['source'])
        assert len(group['holds']) == 2
        preview = Image.open(fonts[group['id']]['preview']).convert('RGB')
        width = 228 if group['prefix_hex'] == 'fe' else 216
        assert preview.size == (width,64)
        wanted = {(16+x,296+y) for y in range(64) for x in range(width) if preview.getpixel((x,y)) == (0,8,0)}
        for hold in group['holds']:
            at = hold['frame']
            assert active[0]['frame'] < at < active[1]['frame']
            assert hold['capture_sha256'] == photos[at]['PNG_sha256'] and hold['RAM_sha256'] == snapshots[at]['sha256']
            raw = Path(snapshots[at]['path']).read_bytes()
            im = Image.open(photos[at]['path']).convert('RGB')
            actual = {(x,y) for y in range(296,360) for x in range(16,16+width) if im.getpixel((x,y)) == (0,8,0)}
            assert actual == wanted and hold['complete_native_independent_actual_ink_equal']
            if width == 216:
                body = bytes.fromhex(texts[group['id']]['target_hex'])[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
                assert cstring(raw,wrapped) == body
            src = hold['source']
            assert sha(raw[src['payload_address']-BASE:src['payload_address']-BASE+src['payload_bytes']]) == mapping['research_block_sha256']
        observed.append(group['id'])
    assert len(observed) == len(set(observed)) == 79
    assert observed == [r['id'] for r in prior_scene['speech_observations']]
    assert set(observed) == set(texts) and not prior_scene['unvisited_speech_IDs']
    ui = read('work/analysis/lil_Hamburg_choice_v1958/original_choice_decoder_VM_geometry_and_native_pixels.json')
    menu = next(r for r in ui['current_and_reviewed_VM_and_font_cases'] if r['version'] == 'reviewed-research')
    menu_planes = planes(arm,menu)
    assert len(nav['choices']) == 1
    choice = nav['choices'][0]
    active = next((a,b) for a,b in zip(rows[::2],rows[1::2],strict=True) if a['source'] == choice['source'])
    assert active[1]['result_words'][:2] == [2,0]
    for hold in choice['holds']:
        at = hold['frame']
        assert active[0]['frame'] < at < active[1]['frame']
        assert hold['capture_sha256'] == photos[at]['PNG_sha256'] and hold['RAM_sha256'] == snapshots[at]['sha256']
        assert verify_menu(Image.open(hold['capture']).convert('RGB'),menu,menu_planes) == hold['menu_proof']
    assert len(nav['joins']) == 1
    old_context = read('work/analysis/lil_Hamburg_arrival_navigation_v1933/closed_original_scene_context.json')
    original_join = old_context['original_art_pauses'][0]
    old_image = Image.open(original_join['holds'][1]['capture']).convert('RGB')
    wanted_join = {(x,y) for y in range(192,384) for x in range(256) if old_image.getpixel((x,y)) == (0,8,0)}
    join = nav['joins'][0]
    active = next((a,b) for a,b in zip(rows[::2],rows[1::2],strict=True) if a['source'] == join['source'])
    assert join['original_join_command_hex'] == original_join['original_non_speech_command_hex'] == '00a0ffff10100120'
    for hold in join['holds']:
        at = hold['frame']
        assert active[0]['frame'] < at < active[1]['frame']
        assert hold['capture_sha256'] == photos[at]['PNG_sha256'] and hold['RAM_sha256'] == snapshots[at]['sha256']
        im = Image.open(hold['capture']).convert('RGB')
        assert {(x,y) for y in range(192,384) for x in range(256) if im.getpixel((x,y)) == (0,8,0)} == wanted_join
        assert hold['original_join_complete_bottom_ink_equal']
    ev = image.read_file('/data/EV2.DK4')
    states = []
    for at, complete in ((49440,0),(frame,1)):
        raw = Path(snapshots[at]['path']).read_bytes()
        cpu,get = get_machine(arm,raw)
        index = raw.find(ev[:96])
        assert index >= 0
        owner = BASE+index-0x34
        flags = {n:get(0x23840,owner+4,n) for n in (25,74,128)}
        assert flags == {25:0,74:complete,128:0}
        assert get(0x34674,get(0xCB1A8)+4+2*132) == 5
        assert get(0x3CCC8,get(0xCB160)+4+76) == 60000
        context = list(struct.unpack('<3I',cpu.mem_read(owner+0x2454,12)))
        assert context[:2] == [7,5]
        assert bytes(cpu.mem_read(BASE,0x400000)) == raw
        states.append(dict(frame=at,original_event_completion_flags=flags,original_town_ID=5,
            current_synthetic_company_funds=60000,current_original_event_context=context,all4MiB_unchanged_by_queries=True))
    ROOT.mkdir(parents=True)
    selected = ['DK4_MES_B74_R0005','DK4_MES_B74_R0022','DK4_MES_B74_R0056','DK4_MES_B74_R0076',
        'DK4_MES_B74_R0079','DK4_MES_B74_R0094','DK4_MES_B74_R0129','DK4_MES_B74_R0148',
        'DK4_MES_B74_R0167','DK4_MES_B74_R0188','DK4_MES_B74_R0235','DK4_MES_B74_R0264',
        'DK4_MES_B74_R0281','DK4_MES_B74_R0308','DK4_MES_B74_R0318','DK4_MES_B74_R0333',
        'DK4_MES_B74_R0312','DK4_MES_B74_R0322','DK4_MES_B74_R0325']
    by_id = {r['id']:r for r in nav['holds']}
    sheets = []
    for start in range(0,len(selected),4):
        sheet = Image.new('RGB',(512,800),'#263238')
        draw = ImageDraw.Draw(sheet)
        for index,ident in enumerate(selected[start:start+4]):
            x,y = index%2*256,index//2*400
            draw.text((x+3,y+3),ident,fill='white')
            sheet.paste(Image.open(by_id[ident]['holds'][1]['capture']).convert('RGB'),(x,y+16))
        path = ROOT/f'representative_revised_contacts_{start//4+1:02d}.png'
        sheet.save(path)
        sheets.append(str(path))
    save(ROOT/'revised_Hamburg79_choice_join_and_three_access_fixture_audit.json',dict(candidate=str(rom),candidate_sha256=digest,
        terminal_frame=frame,original_command_pairs=pairs,revised_speech_observations=nav['holds'],revised_choice=choice,revised_join=join,
        representative_contact_sheets=sheets,representative_visual_record_IDs=selected,original_native_town_and_event_transitions=states,
        all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified=True,
        all_readonly_observer_boundaries_and_host_restoration_pass=True,exact_fixture_replays=replays,
        normal_docking_B74_entry_and_Hamburg_return_not_overridden=True,
        all79_activated_revised_speeches158_holds_complete_native_independent_actual_glyphs=True,
        all3_FE_panels_six_actual_holds_match_separate_paper_planes=True,
        original_join_command_and_complete_bottom_screen_ink_preserved=True,
        both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds=True,
        native_menu_geometry_and_fixed_margins_calibrated_before_revised_pixels=True,
        same116_original_B74_commands_results_and_event_transitions=True,
        choice0_battle_lesson_actual_choice1_only_source_native_VM=True,
        synthetic_travel_and_funds_not_earned_gameplay_claim=True,
        first_navigator_capture_wait_expired_before_replay_reached49440_and_same_process_continued=True,
        command_frame_deltas_recorded_not_required_equal_after_prose_resize=True,
        not_a_registered_release_or_full_conditional_path_coverage=True,
        evidence={str(p):sha(p.read_bytes()) for p in (RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',NAV,ORIGINAL,REF,source,
            Path('scripts/navigate_lil_hamburg_revised_v1966.py'),Path('scripts/navigate_lil_hamburg_revised_v1966b.py'))},
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(revised_actual_speeches=79,complete_actual_native_speech_holds=158,FE_holds=6,join_holds=2,
        choice_holds=2,original_command_pairs=116,terminal_frame=frame,three_access_footprints_exact=True))
