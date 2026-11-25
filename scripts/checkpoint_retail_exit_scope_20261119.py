"""Trace the original in-game System menu and its Quit and Options paths."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack, unpack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from scripts import checkpoint_exhibition_quit_warning_20261115 as earlier
from scripts import checkpoint_pending_shared_native_20261115 as census
from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_race_quit_common_20261114 as replay
from scripts import register_town_summary_20261119 as current
from scripts import verify_script_handoff_v732 as handoff
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots

base, stage = current.base, current.stage
ROOT = Path('work/retail_exit_scope_20261119')
OUTPUT = earlier.OUTPUT.with_name('retail_exit_scope_20261119_v1.json')
SESSION, PREFERENCES = 0x02279668, 0x02279824
SYSTEM, OPTIONS = 0x0203FAA0, 0x0203FC40
MAIN_MENU, FORMATTED = 0x02051F4C, 0x020546F8
CONFIRM = 0x0205466C
SAVE, LOAD = 0x0203EC84, 0x0203ED04
STATUS = SESSION + 0x54
CONTEXT_OUTER, CONTEXT_INNER = 0x02088724, 0x0203FBD0
STOCK_MODES = (0, 1, 2, 0xFFFFFFFF)
TEST_ARCHIVE, TEST_BLOCK = '/testdata/SC3.DK4', 164
SHOP_HISTORY = Path('work/analysis/unmapped_shop_references_v1688b/broader_native_and_script_reference_inventory.json')


def schedule(case):
    events, _, _, source, donor = replay.schedule('quit')
    if case == 'quit':
        return replay.schedule(case)
    times = (6401, 6801, 7201, 7601, 8001, 8401, 8801, 9201, 9601, 10001,
             10401, 10801, 11201, 11601)
    keys = ('DOWN', 'DOWN', 'DOWN', 'A', 'A', 'B', 'DOWN', 'A', 'B', 'B', 'DOWN', 'DOWN', 'A', 'A')
    followup = [dict(start=n, duration=8, buttons=[k]) for n, k in zip(times, keys, strict=True)]
    events = [event for event in events if event['start'] <= 6001] + followup
    return events, [event['start']+199 for event in events], 12100, source, donor


def capture(case):
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS={318,330,331,332,333},
        observer=replay.trace.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__+'::capture', 'exec'), scope)
    scope['main'](case)


def terminated(arm, address):
    offset = address - BASE
    assert 0 < offset < len(arm)
    return arm[offset:arm.index(0, offset, offset+128)].decode('cp932')


def run_case(cpu, arm, selections, *, mode, header=(0,0), preference_bits=0, confirm=False, io_success=False):
    """Supply input and I/O results at their actual widget boundaries."""
    cpu.mem_write(SESSION+8, pack('<2I', *header))
    cpu.mem_write(STATUS, pack('<I', mode))
    cpu.mem_write(PREFERENCES+0x3E, bytes([preference_bits]))
    cpu.mem_write(SESSION+0x64, bytes(4))
    keys = iter(selections)
    menus, common, settings, io = [], [], [], []

    def watch(u, pc, _size, _data):
        r0, r1, r2 = (u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        if pc == MAIN_MENU:
            descriptors = [unpack('<4I', bytes(u.mem_read(r0+16*i,16))) for i in range(r1)]
            assert r1 in (3,5) and len(menus) < len(selections)
            result = next(keys)
            menus.append(dict(rows=[dict(label=terminated(arm,p) if p else None, flags=list(values))
                                    for p,*values in descriptors], supplied_selection=result))
        elif pc == CONFIRM:
            common.append(r0)
            result = int(confirm)
        elif pc == FORMATTED:
            settings.append(dict(pointer=r0, text=terminated(arm,r0), arguments=[terminated(arm,r1),terminated(arm,r2)]))
            result = int(confirm)
        elif pc in (SAVE, LOAD):
            assert r0 == SESSION
            io.append('Save' if pc == SAVE else 'Load')
            if pc == SAVE:
                u.mem_write(r1, pack('<I', int(io_success)))
            result = int(io_success)
        elif pc in (0x020C989C,0x020C987C,0x020CF6F4,0x020CFA44):
            result = 0
        else:
            return
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    callbacks = [cpu.hook_add(UC_HOOK_CODE, watch, begin=address, end=address) for address in
                 (MAIN_MENU, CONFIRM, FORMATTED, SAVE, LOAD, 0x020C989C,0x020C987C,0x020CF6F4,0x020CFA44)]
    try:
        executed = call(cpu, SYSTEM-BASE, (0,), instruction_limit=3200)
    finally:
        for callback in callbacks:
            cpu.hook_del(callback)
    assert next(keys, None) is None
    final_mode, = unpack('<I', bytes(cpu.mem_read(STATUS,4)))
    dirty, = unpack('<I', bytes(cpu.mem_read(SESSION+0x64,4)))
    final_bits = bytes(cpu.mem_read(PREFERENCES+0x3E,1))[0]
    assert all(n == 319 for n in common)
    return dict(initial_mode=mode, final_mode=final_mode, menus=menus, COMMON_arguments=common, options=settings,
                supplied_IO=io, initial_preference_bits=preference_bits, surviving_preference_bits=final_bits,
                dirty=dirty, native_menu_and_options=OPTIONS in executed)


def controls(arm, clean):
    cpu = machine(arm)
    results = []
    for flag in STOCK_MODES:
        for answer in (False,True):
            rows = (2,4) if flag == 1 and not answer else (2,)
            sample = run_case(cpu,arm,rows,mode=flag,confirm=answer)
            assert sample['COMMON_arguments'] == ([319] if flag == 1 else [])
            assert sample['final_mode'] == (0 if flag != 1 or answer else 1)
            results.append(dict(case='Quit Game', supplied_yes=answer, **sample))
    for bits in (0,1,2,3):
        for option, mask in ((0,1),(1,2)):
            for answer in (False,True):
                sample = run_case(cpu,arm,(3,option,2,4),mode=1,preference_bits=bits,confirm=answer)
                assert sample['native_menu_and_options'] and not sample['COMMON_arguments']
                assert sample['surviving_preference_bits'] == (bits ^ mask if answer else bits)
                assert sample['dirty'] == int(answer)
                row, = sample['options']
                if not clean:
                    expected = ('Reports are %s. Change to %s?' if option == 0 else 'Sailing Help is %s. Change to %s?')
                    assert row['text'] == expected
                    assert row['arguments'] == (['On','Off'] if bits & mask else ['Off','On'])
                results.append(dict(case='Reports' if option == 0 else 'Sailing Help', supplied_yes=answer, **sample))
    for header in ((0,0),(0,1),(1,0),(1,1)):
        sample = run_case(cpu,arm,(4,),mode=1,header=header)
        assert sample['menus'][0]['rows'][0]['flags'][0] == int(header != (0,1))
        assert not sample['COMMON_arguments'] and sample['final_mode'] == 1
        results.append(dict(case='Save enabled check', session_header=header, **sample))
    for choice in (0,1):
        for accepted in (False,True):
            sample = run_case(cpu,arm,(choice,4) if not accepted else (choice,),mode=1,io_success=accepted)
            assert sample['supplied_IO'] == ['Save' if choice==0 else 'Load']
            assert sample['final_mode'] == (1 if not accepted else choice*2)
            assert not sample['COMMON_arguments']
            results.append(dict(case='Save or Load handoff', supplied_success=accepted, **sample))
    return results


def test_header(clean, image):
    history = base.load(SHOP_HISTORY)
    archived = next(row for row in history['script_event_and_test_containers'] if row['path'] == TEST_ARCHIVE)
    lead, = [r for r in archived['packed_halfword_matches'] if r['unclassified_test_header_word_at4']]
    assert (lead['block'], lead['offset'], lead['value']) == (TEST_BLOCK,4,750)
    raw = clean.read_file(TEST_ARCHIVE)
    assert raw == image.read_file(TEST_ARCHIVE) and current.native.digest(raw) == archived['sha256']
    blocks = IlnkContainer.parse(raw).blocks
    block = blocks[TEST_BLOCK]
    assert block[:4] == b'CS\x01\x01' and unpack_from('<I',block,4)[0] == 750
    assert len(block) == 760 and block[758:] == b'\0\0' and block[752:756] == b'\0\xc2\0\0'
    # Exercise the original cached script parent on the exact alternate payload.
    # The cache is supplied. A successful handoff makes no claim about how to reach this archive.
    code = checked_text(getsource(handoff.run), {
        'for route in range(4):': 'for route in (3,):',
        "path = f'/data/SC{route}.DK4'": 'path = TEST_ARCHIVE',
        'assert len(old_blocks) == len(blocks)': 'assert list(old_blocks) == [TEST_BLOCK]',
        'for index, block in enumerate(blocks):': 'for index, block in enumerate(blocks):\n                if index != TEST_BLOCK: continue',
        'assert len(cases) == 2614': 'assert len(cases) == 2',
        "print(f'{label} route{route}: {len(blocks) * 2} original handoffs and first instruction reads pass.', flush=True)":
            "print(f'{label}: two original handoffs on the supplied SC3 B164 cache passed.', flush=True)",
    })
    scope = vars(handoff) | dict(TEST_ARCHIVE=TEST_ARCHIVE, TEST_BLOCK=TEST_BLOCK)
    exec(compile(code,__file__+'::SC3-test-header','exec'),scope)
    fixture = dict(routes=[dict(route=3,SC_sha256=current.native.digest(raw),
        actions=[dict(kind=2,native_selected_block=TEST_BLOCK,payload_sha256=current.native.digest(block))])])
    ja, en = (scope['run'](rom, name, fixture) for rom,name in ((clean,'Clean'),(image,'Current')))
    for row in (ja,en):
        assert len(row['native_handoff_and_first_read_cases']) == 2
    return dict(path=TEST_ARCHIVE, block=TEST_BLOCK, header_hex=block[:8].hex(), numeric_offset=4, value=750,
        archive_sha256=current.native.digest(raw), block_sha256=current.native.digest(block), body_length=750,
        physical_bytes=760, trailing_alignment_bytes=2, final_command_hex=block[752:756].hex(),
        native_parent_cases=dict(clean=ja['native_handoff_and_first_read_cases'], current=en['native_handoff_and_first_read_cases']),
        supplied_cached_archive=True, storage_explanation='The field gives the scene body length. The original parent starts reading at byte 8.')


def live(case, release, font, evidence):
    directory = ROOT/case
    reports = [directory/path for path in ('capture/capture_report.json','requests.json','terminal.json')]
    report, trace, terminal = map(base.load,reports)
    events, _, end, source, donor = schedule(case)
    assert report['ROM_sha256'] == terminal['ROM_sha256'] == release['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule'] == events and report['frames'] == end == terminal['completed_frames']
    assert not any(value for key,value in report.items() if key.startswith('synthetic_'))
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert report['battery_save_preloaded']['source_sha256'] == donor['source_sha256'] == base.digest(donor['source'])
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    expected_count = 2 if case == 'quit' else 4
    assert len(trace['source_requests']) == expected_count
    for direct, copy in zip(trace['source_requests'][::2],trace['source_requests'][1::2],strict=True):
        assert (direct['PC'],copy['PC']) == (0x0205528C,0x020534F4)
        assert direct['message_ID'] == copy['message_ID'] == 319
        assert direct['caller_LR'] == copy['caller_LR'] == 0x02054680
    assert not terminal['target_COMMON_calls']
    shot = shots(report)
    expected = {5800:'Quit the game?'}
    if case != 'quit':
        expected.update({8200:'Reports are On. Change to Off?',9400:'Sailing Help is On. Change to Off?',11400:'Quit the game?'})
    panels = []
    for frame,text in expected.items():
        rgb = captured(shot[frame])
        ink = font_mask(rgb,font,text,16,297,(16,296,245,330),(0,8,0))
        panels.append(dict(frame=frame, complete_ink_pixels=ink, text=text, capture=shot[frame]['path']))
        evidence[shot[frame]['path']] = shot[frame]['PNG_sha256']
    for frame in ((6200,7000) if case == 'quit' else (6200,8600,9800,10200,11800)):
        captured(shot[frame])
        evidence[shot[frame]['path']] = shot[frame]['PNG_sha256']
    if case != 'quit':
        # Compare the original title menu choices as a fixed region after confirming Quit.
        tile = (94,250,162,348)
        assert captured(shot[11800]).crop(tile).tobytes() == captured(shot[1800]).crop(tile).tobytes()
        evidence[shot[1800]['path']] = shot[1800]['PNG_sha256']
    evidence.update({str(p):base.digest(p) for p in (*reports,source)})
    return dict(ordinary_Lisbon_existing_save=True, hardware=False, panels=panels,
        original_COMMON_requests=trace['source_requests'], exit_outcome='cancelled and opened Save' if case == 'quit' else 'cancelled first, confirmed Quit and returned to title')


def verify():
    assert not OUTPUT.exists()
    release,ledger = map(base.load,(current.RELEASE,base.LEDGER))
    candidate = base.digest(current.ROM)
    assert candidate == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    clean,image = map(base.NdsImage.open,(stage.CLEAN,current.ROM))
    ja,arm = (rom.read_file(stage.ARM) for rom in (clean,image))
    assert current.native.digest(arm) == release['target_ARM9_sha256']
    assert ja[SYSTEM-BASE:0x3FD4C] == arm[SYSTEM-BASE:0x3FD4C]
    for rom in (clean,image):
        roots = [(label,*row) for label,address,data in census.components(rom.rom)
                 for row in census.branch_hits(data,address,{SYSTEM,OPTIONS})]
        assert roots == [('ARM9 section 0',CONTEXT_INNER,OPTIONS,'arm_bl'),('ARM9 section 0',CONTEXT_OUTER,SYSTEM,'arm_bl')]
    rows_clean, rows_current = controls(ja,True), controls(arm,False)
    assert len(rows_clean) == len(rows_current) == 32
    for old,new in zip(rows_clean,rows_current,strict=True):
        for key in ('final_mode','COMMON_arguments','surviving_preference_bits','dirty','supplied_IO'):
            assert old[key] == new[key]
    source = earlier.common_message_entries(clean.read_file(stage.COMMON),ja)
    directory = current.native.digest(arm[earlier.DIRECTORY_OFFSET:earlier.TABLE_OFFSET])
    installed = earlier.owned_entries(image.read_file(stage.COMMON),arm,directory)
    previous = base.load(earlier.OUTPUT)['exhibition_warning']
    assert installed[318].text.hex() == previous['current_hex'] and source[318].text.hex() == previous['source_hex']
    assert installed[319].text.decode('ascii').strip() == 'Quit the game?'
    evidence = {str(p):base.digest(p) for p in (current.RELEASE,earlier.OUTPUT,SHOP_HISTORY,Path(handoff.__file__),Path(__file__))}
    font = GameAsciiFont.from_arm9(arm)
    games = {case:live(case,release,font,evidence) for case in ('quit','options_then_quit')}
    header = test_header(clean,image)
    records = [dict(message_ID=n, source_reference=earlier.reference(source[n]), current_reference=earlier.reference(installed[n]),
        source_Japanese=source[n].text.decode('cp932'), current_hex=installed[n].text.hex()) for n in (318,319,750,751,752)]
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=release['clean_input_sha256'], records=records,
        native_clean=rows_clean, native_current=rows_current, observed_gameplay=games, test_archive_lead=header,
        stored_exhibition_draft_retained=previous['english'], original_exhibition_display_path='unverified',
        exact_in_game_system_menu_entry=SYSTEM, hardware=False, new_contextual_credit=0, remaining_raw_shared_count=276,
        evidence=evidence, full_goal_complete=False))
    print('Verified 64 System menu cases, two Lisbon replays, and the historical test-script length-field lead.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('quit','options_then_quit','offline','verify'))
    case = parser.parse_args().case
    if case == 'offline':
        for path, clean in ((stage.CLEAN,True),(current.ROM,False)):
            arm = base.NdsImage.open(path).read_file(stage.ARM)
            print(path, len(controls(arm, clean)))
    elif case == 'verify':
        verify()
    else:
        capture(case)
