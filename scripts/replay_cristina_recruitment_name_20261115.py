"""Verify the complete recruitment exchange and spelling in initialized Lil play."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into
import sys

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from scripts import headless_desmume_v193 as harness
from scripts import replay_refit_help_startup_20261115 as boot
from scripts import stage_cristina_recruitment_name_20261115 as stage
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_captain_biographies_v1 import captured, shots


base, ROOT = stage.base, stage.ROOT
STARTUP = ROOT / 'own_startup_verification.json'
LIVE, SHEET = ROOT / 'story_replay.json', ROOT / 'story_replay.png'
INPUTS = Path('out/lil_opening_wraps_20261114_v1/inputs.json')
WATCH = (2200, 2950, *range(3720, 6520, 80), 6600, 6900)
BODY = (10, 294, 244, 367)
NAMEPLATE = (8, 272, 160, 291)
SPEAKERS = {2: 'Lil Argot', 6: 'Julio Erneco'}


def startup():
    source = checked_text(getsource(boot.startup.main), {
        'prior = stage.parent.stage.ROOT/"startup_retry"': 'prior = PRIOR_CAPTURE',
    })
    parent = base.load(stage.parent.RELEASE)
    snapshot = base.load(parent['own_registered_startup'])['read_only_snapshot']['path']
    env = vars(boot.startup) | dict(stage=stage, PRIOR_CAPTURE=Path(snapshot).parent.parent)
    exec(compile(source, __file__ + '::same-registered-startup-controls', 'exec'), env)
    env['main']()


def prepare(rom, expected, folder):
    assert base.digest(rom) == expected
    image, clean = [base.NdsImage.open(path) for path in (rom, stage.CLEAN)]
    arm = image.read_file(stage.ARM)
    archive = image.read_file(stage.FILE)
    blocks = IlnkContainer.parse(archive).blocks
    opening, scene = blocks[22], blocks[stage.BLOCK]
    original = IlnkContainer.parse(clean.read_file(stage.FILE)).blocks[22]
    walk, _, _ = scoped_inventory()
    original_rows, _ = walk(clean.read_file(stage.ARM), original)
    opening_rows, opening_speech = walk(arm, opening)
    rows, speeches = walk(arm, scene)
    assert opening_speech[0]['offset'] == 56 and opening[8:56] == original[8:56]
    assert [row['word'] for row in rows[-2:]] == [0, 0] and len(speeches) == 8
    footer = opening[opening_rows[-3]['offset']:opening_rows[-1]['offset'] + 4]
    assert footer == original[original_rows[-3]['offset']:original_rows[-1]['offset'] + 4]
    assert footer.hex() == '00c200a0ffff2c081b8200000000'
    # The fixture uses Lil's ordinary entry and exit around all eight original speeches.
    staged = bytearray(opening[:56] + scene[8:rows[-2]['offset']] + footer)
    pack_into('<H', staged, 4, len(staged) - 8)
    inserted = bytes(staged) + bytes(-len(staged) % 4)
    commands, shown = walk(arm, inserted)
    assert len(shown) == 8
    moved = [row for row in commands if 56 <= row['offset'] < 56 + rows[-2]['offset'] - 8]
    assert [row['whole_command_hex'] for row in moved] == [row['whole_command_hex'] for row in rows[:-2]]
    blocks[22] = inserted
    image.replace_file(stage.FILE, IlnkContainer(blocks).to_bytes())
    fixture = folder / 'initialized_lil_dialogue_RESEARCH_ONLY.nds'
    image.save(fixture)
    image.replace_file(stage.FILE, archive)
    assert bytes(image.rom.save()) == rom.read_bytes()
    return fixture, dict(input_candidate=expected, fixture_sha256=base.digest(fixture), source_block=stage.BLOCK,
                         original_complete_speeches=len(shown), input_candidate_inverse_exact=True)


def replay(side):
    proof = base.load(stage.STORED)
    rom, expected = (stage.parent.ROM, proof['previous_sha256']) if side == 'before' else (stage.ROM, proof['candidate_sha256'])
    folder = ROOT / side
    folder.mkdir()
    rom, result = prepare(rom, expected, folder)
    events = base.load(INPUTS)[:6] + [dict(start=frame, duration=5, buttons=['A']) for frame in range(3800, 6200, 320)]
    inputs = folder / 'inputs.json'
    base.save(inputs, events)
    previous = sys.argv
    try:
        sys.argv = [harness.__file__, '--rom', str(rom), '--out', str(folder / 'capture'), '--frames', '7001',
                    '--inputs-json', str(inputs), '--press-start', '-1', '--capture-every', '999999', '--capture-at', *map(str, WATCH)]
        harness.main()
    finally:
        sys.argv = previous
    report = folder / 'capture/capture_report.json'
    data = base.load(report)
    assert data['ROM_sha256'] == result['fixture_sha256'] and data['scripted_input_schedule'] == events
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('battery_save_preloaded') and not any(v for k, v in data.items() if k.startswith('synthetic_'))
    base.save(folder / 'terminal.json', result | dict(report=str(report), report_sha256=base.digest(report)))


def mask(font, text, image, bounds=BODY, baseline=297, ink=(0, 8, 0)):
    wanted = {(16 + 6 * i + x, baseline + 16 * row + y)
              for row, line in enumerate(text.split('\n')) for i, c in enumerate(line.lstrip(' '))
              for glyph in (font.decode(c),) for x in range(6) for y in range(11) if glyph.getpixel((x, y))}
    left, top, right, bottom = bounds
    visible = {(x, y) for x in range(left, right) for y in range(top, bottom) if image.getpixel((x, y)) == ink}
    if wanted == visible:
        return len(wanted)
    return 0


def verify():
    staged = base.load(stage.STORED)
    runs, evidence = [], {}
    for side, sha in (('before', staged['previous_sha256']), ('after', staged['candidate_sha256'])):
        terminal = ROOT / side / 'terminal.json'
        fixture = base.load(terminal)
        report = Path(fixture['report'])
        assert fixture['input_candidate'] == sha and fixture['original_complete_speeches'] == 8
        assert base.digest(report) == fixture['report_sha256']
        evidence.update({str(path): base.digest(path) for path in (terminal, report)})
        runs.append(shots(base.load(report)))
    before, after = runs
    assert before.keys() == after.keys()
    font = GameAsciiFont.from_arm9(base.NdsImage.open(stage.ROM).read_file(stage.ARM))
    matches, exact = [], []
    for frame in before:
        a, b = captured(before[frame]), captured(after[frame])
        if a.tobytes() == b.tobytes():
            exact.append(frame)
            continue
        left, top, right, bottom = ImageChops.difference(a, b).getbbox()
        assert BODY[0] <= left < right <= BODY[2] and BODY[1] <= top < bottom <= BODY[3]
        n, m = mask(font, stage.BEFORE, a), mask(font, stage.AFTER, b)
        if n and m:
            name = mask(font, 'Julio Erneco', b, NAMEPLATE, 277, (98, 97, 98))
            assert name
            matches.append(dict(frame=frame, previous=before[frame], revised=after[frame], complete_ink_pixels=[n, m],
                                speaker_nameplate_ink=name))
    assert matches
    assert all(frame in exact for frame in (2200, 6600, 6900))
    sequence = []
    earliest = 3700
    for row in staged['all_eight_dialogue_records']:
        raw = bytes.fromhex(row['target']['raw_hex'])
        text, speaker = raw[1:].decode('ascii'), SPEAKERS[raw[0]]
        for frame in sorted(n for n in after if earliest < n < 6400):
            pic = captured(after[frame])
            dialogue_ink = mask(font, text, pic)
            if dialogue_ink:
                name_ink = mask(font, speaker, pic, NAMEPLATE, 277, (98, 97, 98))
                assert name_ink
                sequence.append(dict(record=row['id'], frame=frame, screenshot=after[frame],
                                     dialogue_pixels=dialogue_ink, nameplate_pixels=name_ink))
                earliest = frame
                break
        else:
            raise AssertionError(f'Missing complete dialogue {row["id"]}')
    row = matches[0]
    sheet = Image.new('RGB', (1024, 5 * 266), '#222d33')
    draw = ImageDraw.Draw(sheet)
    panels = [('Before', row['previous']), ('After', row['revised'])]
    panels.extend((f'{i + 1}. {item["record"]}', item['screenshot']) for i, item in enumerate(sequence))
    for index, (label, path) in enumerate(panels):
        x, y = index % 2 * 512, index // 2 * 266
        draw.text((x + 8, y + 6), label, fill='white')
        panel = captured(path).crop((0, 264, 256, 384)).resize((512, 240), Image.Resampling.NEAREST)
        sheet.paste(panel, (x, y + 24))
    sheet.save(SHEET)
    base.save(LIVE, dict(candidate_sha256=staged['candidate_sha256'], exact_control_frames=exact,
        matched_complete_corrected_dialogue=matches, complete_exchange=sequence, sheet=str(SHEET),
        sheet_sha256=base.digest(SHEET), evidence=evidence,
        all_framebuffer_differences_inside_original_dialogue_body=True,
        scope='Original complete recruitment exchange in initialized Lil play. Ordinary inputs. Natural event activation was not exercised.'))
    print(len(matches), 'complete line holds passed, along with', len(exact), 'unchanged controls.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('before', 'after', 'startup', 'verify'))
    action = parser.parse_args().action
    replay(action) if action in ('before', 'after') else globals()[action]()
