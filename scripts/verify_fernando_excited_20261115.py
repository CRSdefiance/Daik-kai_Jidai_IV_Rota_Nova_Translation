"""Compare Fernando's Normal and Excited status through the same Deck replay."""

from argparse import ArgumentParser
from hashlib import sha256
from json import dumps
from pathlib import Path
from struct import unpack_from
import sys

from PIL import Image, ImageChops, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.patch.sailor_mood_caption import OFFSET, POINTER_FIELD
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as original_fixture
from scripts import register_town_market_wraps_20261115 as current
from scripts import verify_sailor_stat_labels_20261114 as stats
from scripts.probe_button_prompt_native import BASE, STACK, STOP, call, machine
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.seal_shared_text_source_v1 import reference
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_plaque_release_v247 import find_mask


base = current.base
ROOT = Path('work/fernando_excited_deck_20261115_v1')
OLD = Path('work/sailor_fernando_latest_20261114_v1/replay/capture_report.json')
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/fernando_excited_deck_20261115_v1.json')
CASES = {11400: None, 11800: 2, 12200: 1, 12600: 3, 13000: 0, 13400: None}
EARLY = (11100, *range(11101, 11131), 11140, 11160, 11200)
CAPTURES = (*EARLY, *CASES, 13800)
MOOD_FIELD = (52, 124, 108, 144)
TITLE_FIELD = (0, 0, 256, 15)
DECK_TEXT = (12, 108, 244, 166)
SKILLS = (('Command', 1, 16, 273), ('Sailing', 2, 96, 273), ('Survey', 3, 176, 273),
          ('Finance', 4, 16, 297), ('Observe', 9, 96, 297), ('Vigor', 0, 176, 297),
          ('Aim', 6, 16, 321), ('Swords', 5, 96, 321), ('Speech', 7, 176, 321), ('Guile', 8, 16, 345))
LOCKS = ((0x7E070, 0x7E0BC), (0x80A84, 0x80ABC), (0xCB184, 0xCB190), (0x659B8, 0x65A00),
         (0x7DCC8, 0x7DE20), (0x80938, 0x80988), (0x12104, 0x122A4), (0x123C8, 0x1242C), (0x1278C, 0x12834))


def fixture(arm, raw, request):
    release = base.load(current.RELEASE)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert len(raw) == 0x400000 and request == {'actor': 20, 'mood': 0}
    clean = base.NdsImage.open(current.stage.CLEAN).read_file(current.stage.ARM)
    assert all(arm[a:b] == clean[a:b] for a, b in LOCKS)
    assert unpack_from('<I', clean, POINTER_FIELD) == unpack_from('<I', arm, POINTER_FIELD) == (BASE + OFFSET,)
    assert arm[OFFSET:OFFSET + 8] == b'Excited\0'
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    assert get(0x7F244) == 2
    actor = get(0xCB184) + 4 + 20 * 32
    vtable, = unpack_from('<I', raw, actor - BASE)
    getter, = unpack_from('<I', raw, vtable + 0x20 - BASE)
    name = get(getter - BASE, (actor,))
    assert bytes(u.mem_read(name, 9)) == b'Fernando\0'
    assert get(0x7E0B4, (actor,)) == 3
    get(0x7E0AC, (actor, 0))
    assert get(0x7E0B4, (actor,)) == 0 and get(0x7E070, (actor,)) == BASE + OFFSET
    at = actor + 7 - BASE
    assert raw[at] == 3 and bytes(u.mem_read(actor + 7, 1)) == b'\0'
    after = raw[:at] + b'\0' + raw[at + 1:]
    return after, dict(actor_ID=20, captain_ID=2, actor_address=actor, original_name_pointer=name,
        original_mood_setter=BASE + 0x7E0AC, original_mood_getter=BASE + 0x7E0B4,
        before_RAM_sha256=sha256(raw).hexdigest(), after_RAM_sha256=sha256(after).hexdigest(),
        changes=[dict(address=BASE + at, before=3, after=0)])


def replay(case, attempt):
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    history = base.load(OLD)
    assert history['cold_boot'] and not history['savestate_loaded'] and not history.get('battery_save_preloaded')
    path = ROOT / (case if attempt == 1 else f'{case}_{attempt}')
    path.mkdir(parents=True)
    events = path / 'inputs.json'
    base.save(events, history['scripted_input_schedule'])
    command = {'until': 11400}
    if case == 'excited':
        command['condition_fixture'] = dict(actor=20, mood=0)
    commands = path / 'commands.jsonl'
    commands.write_text(''.join(dumps(c) + '\n' for c in (command, {'until': 13800}, {'stop': True})), encoding='utf-8')
    stdin, argv, old = sys.stdin, sys.argv, original_fixture.set_condition
    stream = GrowingCommands(commands)
    try:
        original_fixture.set_condition = fixture
        sys.stdin = stream
        sys.argv = [harness.__file__, '--rom', str(current.ROM), '--out', str(path / 'capture'),
            '--frames', '13801', '--inputs-json', str(events), '--touchscreen', '--capture-every', '999999',
            '--capture-at', *map(str, CAPTURES), '--pause-at', '11100', '--dump-pause-ram', '--allow-condition-fixtures']
        harness.main()
    finally:
        sys.stdin, sys.argv, original_fixture.set_condition = stdin, argv, old
        stream.close()


def skill_values(arm, raw, actor):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    values = {}
    for name, index, _, _ in SKILLS:
        call(cpu, 0x7EEB0, (index,))
        address = cpu.reg_read(UC_ARM_REG_R0)
        assert bytes(cpu.mem_read(address, len(name) + 1)) == name.encode('ascii') + b'\0'
        call(cpu, 0x7DCC8, (actor, index))
        value = cpu.reg_read(UC_ARM_REG_R0)
        assert value <= 500
        values[name] = value
    return values


def deck_message(arm, raw):
    cpu = machine(arm)
    cpu.mem_write(BASE, raw)
    selected = []

    def capture(u, address, size, _):
        selected.append(u.reg_read(UC_ARM_REG_R0))
        u.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, capture, begin=0x0205528C, end=0x0205528C)
    for register, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP), (UC_ARM_REG_R0, 20), (UC_ARM_REG_R1, 0)):
        cpu.reg_write(register, value)
    cpu.emu_start(BASE + 0x12104, STOP, count=20000)
    result, = selected
    return result


def ink_mask(font, text, x, y):
    return {(x + 6 * index + dx, y + dy) for index, char in enumerate(text)
            for glyph in (font.decode(char),) for dx in range(6) for dy in range(11) if glyph.getpixel((dx, dy))}


def verification(attempt):
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert candidate == release['candidate_sha256']
    image = base.NdsImage.open(current.ROM)
    arm = image.read_file(stats.stage.ARM)
    font = stats.GameAsciiFont.from_arm9(arm)
    art = stats.PxlImage.from_bytes(image.read_file(stats.stage.ART)).render().convert('RGB')
    proof = base.load(Path('releases/all_routes_editorial_20261114_sailor_stat_labels_candidate/verification/stage.json'))
    assert sha256(image.read_file(stats.stage.ART)).hexdigest() == proof['asset_sha256']
    assert all(arm[row['offset']:row['offset'] + 4] == bytes.fromhex(row['after']) for row in proof['words'])
    inputs = base.load(OLD)['scripted_input_schedule']
    evidence = {str(p): base.digest(p) for p in (current.RELEASE, OLD, Path(__file__))}
    images, reports, memory = {}, {}, {}
    for case in ('normal', 'excited'):
        path = ROOT / (case if attempt == 1 else f'{case}_{attempt}') / 'capture'
        report_path = path / 'capture_report.json'
        report = base.load(report_path)
        assert report['ROM_sha256'] == candidate and report['frames'] == 13800
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and report['scripted_input_schedule'] == inputs
        assert not any(value for key, value in report.items() if key.startswith('synthetic_') and key != 'synthetic_condition_fixtures')
        journal = path / 'navigation_command_journal.json'
        records = base.load(journal)['commands_received']
        assert [row['frame'] for row in records] == [11100, 11400, 13800] and all(row['validation_passed'] for row in records)
        assert records[-1]['command'] == {'stop': True}
        by_frame = shots(report)
        images[case] = {n: captured(by_frame[n]) for n in CAPTURES}
        reports[case] = report
        memory[case] = {}
        for row in report['read_only_pause_RAM_snapshots']:
            raw = Path(row['path']).read_bytes()
            assert row['read_only_export'] and sha256(raw).hexdigest() == row['sha256']
            memory[case][row['frame']] = raw
            evidence[row['path']] = row['sha256']
        evidence.update({by_frame[n]['path']: by_frame[n]['PNG_sha256'] for n in CAPTURES})
        evidence.update({str(p): base.digest(p) for p in (report_path, journal)})
    normal, excited = reports['normal'], reports['excited']
    assert all(normal[key] == excited[key] for key in ('core_DLL_sha256', 'core_options'))
    assert not normal.get('synthetic_condition_fixtures')
    raw = memory['excited'][11100]
    assert raw == memory['normal'][11100]
    _, change = fixture(arm, raw, dict(actor=20, mood=0))
    assert excited['synthetic_condition_fixtures'] == [change | {'frame': 11100}]
    at = change['changes'][0]['address'] - BASE
    assert (memory['normal'][11400][at], memory['excited'][11400][at]) == (3, 0)
    skill_scores = {case: skill_values(arm, memory[case][11400], change['actor_address'])
                    for case in ('normal', 'excited')}

    selection_table = unpack_from('<20I', arm, 0x148448)
    sheet = Image.new('RGB', (1040, 406 * 3), '#252830')
    draw = ImageDraw.Draw(sheet)
    output = []
    for frame, skill in CASES.items():
        unselected, tested = (images[mode][frame] for mode in ('normal', 'excited'))
        diff = ImageChops.difference(unselected, tested)
        bounds = diff.getbbox()
        mood_bounds = diff.crop((0, 0, 256, 192)).getbbox()
        assert bounds and mood_bounds and MOOD_FIELD[0] <= mood_bounds[0] < mood_bounds[2] <= MOOD_FIELD[2]
        assert MOOD_FIELD[1] <= mood_bounds[1] < mood_bounds[3] <= MOOD_FIELD[3]
        diff.paste((0, 0, 0), MOOD_FIELD)
        for name, _, x, y in SKILLS:
            rectangle = (x, y, x + 60, y + 11)
            for case, screen in (('normal', unselected), ('excited', tested)):
                text = f'{name:>7}{skill_scores[case][name]:3d}'
                assert stats.visible_white(screen, *rectangle) == ink_mask(font, text, x, y), (frame, case, text)
            diff.paste((0, 0, 0), (x + 42, y, x + 60, y + 11))
        assert diff.getbbox() is None, frame
        title = find_mask(font, 'Sailor Info', tested, TITLE_FIELD)
        assert title['ink_pixels'] == len(stats.visible_white(tested, *TITLE_FIELD)) == 111
        find_mask(font, 'Sail Handler', tested, (82, 53, 180, 75))
        find_mask(font, 'Fernando Dias', tested, (82, 18, 225, 50))
        mood = find_mask(font, 'Excited', tested, MOOD_FIELD)
        assert mood['ink_pixels'] == len(stats.visible_white(tested, *MOOD_FIELD))
        find_mask(font, 'Normal', unselected, MOOD_FIELD)
        selected = set(range(6) if skill is None else selection_table[skill * 2:skill * 2 + 2])
        for i, label in enumerate(stats.stage.LABELS):
            y = 99 + 15 * i
            expected = stats.font_pixels(font, label, y) if i in selected else set()
            assert stats.visible_white(tested, 124, y, 170, y + 15) == expected
            assert all(stats.native5(tested.getpixel((u, v))) == stats.native5(art.getpixel((u, v)))
                       for u in range(124, 170) for v in range(y, y + 15) if (u, v) not in expected)
        output.append(dict(frame=frame, title=title, mood=mood, selected_stats=sorted(selected), upper_mood_bounds=list(mood_bounds)))
        if frame in (11400, 11800, 13400):
            row = (11400, 11800, 13400).index(frame)
            for column, (name, screen) in enumerate(zip(('Normal', 'Excited'), (unselected, tested), strict=True)):
                x = column * 520 + 4
                y = row * 406 + 3
                draw.text((x, y), f'{name} - frame {frame}', fill='white')
                sheet.paste(screen.crop((0, 0, 256, 192)).resize((512, 384), Image.Resampling.NEAREST), (x, y + 16))
    assert all(images['normal'][n].crop(TITLE_FIELD).tobytes() == images['excited'][n].crop(TITLE_FIELD).tobytes()
               for n in EARLY)
    diff = ImageChops.difference(images['normal'][13800], images['excited'][13800])
    diff.paste((0, 0, 0), DECK_TEXT)
    assert diff.getbbox() is None
    path = ROOT / 'fernando_normal_excited_comparison.png'
    sheet.save(path)
    clean_rom = base.NdsImage.open(current.stage.CLEAN)
    clean = clean_rom.read_file(stats.stage.ARM)
    source = common_message_entries(clean_rom.read_file(current.stage.COMMON), clean)
    deployed = owned_entries(image.read_file(current.stage.COMMON), arm,
                             sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    comments = []
    for case, ident, note in (
        ('normal', 1527, 'The Sail Handler gives practical advice about slowing down. The English uses the game’s Half Open setting and keeps the instruction together.'),
        ('excited', 1837, 'Bring it on! gives Fernando a short, exuberant reaction that suits this mood. His Japanese challenges whatever comes his way.'),
    ):
        assert deck_message(arm, memory[case][13800]) == ident
        lines = [part.strip() for part in deployed[ident].text.decode('ascii').splitlines()]
        wanted = set().union(*(ink_mask(font, line, 16, 113 + i * 12) for i, line in enumerate(lines)))
        pictured = images[case][13800]
        actual = {(x, y) for x in range(DECK_TEXT[0], DECK_TEXT[2]) for y in range(DECK_TEXT[1], DECK_TEXT[3])
                  if pictured.getpixel((x, y)) == (0, 8, 0)}
        assert actual == wanted
        comments.append(dict(mood=case, message_ID=ident, source_Japanese=source[ident].text.decode('cp932'),
            English=' '.join(lines), source_reference=reference(source[ident]), current_reference=reference(deployed[ident]),
            source_hex=source[ident].text.hex(), current_hex=deployed[ident].text.hex(),
            complete_ink_pixels=len(actual), localization_note=note, decision='retention',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True)))
    base.save(OUTPUT, dict(candidate_sha256=candidate, translation_policy='natural-dialogue-v2', target_locale='en-US',
        Japanese=clean[OFFSET:OFFSET + 8].split(b'\0')[0].decode('cp932'), English='Excited',
        clean_AND_ROM_ARM9_offset=OFFSET, original_pointer_field=POINTER_FIELD, decision='retention',
        localization_note='Excited expresses the positive, energized mood selected by the original victory response without implying intoxication.',
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True),
        changed_bytes=change['changes'], cases=output, full_stat_plaque_masks=36, title_transition_sample_frames=list(EARLY),
        all_skill_values_from_original_getter=skill_scores, complete_skill_row_masks=120,
        Deck_return_frame=13800, Deck_return_comments=comments, hardware=False, natural_mood_acquisition=False,
        source_scope='Standard Lil New Game and mast assignment. One original Fernando mood byte was set in the isolated emulator before opening Sailor Info.',
        sheet=str(path), sheet_sha256=base.digest(path), evidence=evidence, new_editorial_credit=0))
    print('36 complete stat plaques, 120 skill rows, six titles and two Deck return comments pass.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('normal', 'excited', 'verify'))
    parser.add_argument('--attempt', type=int, default=1)
    args = parser.parse_args()
    if args.case == 'verify':
        verification(args.attempt)
    else:
        replay(args.case, args.attempt)
