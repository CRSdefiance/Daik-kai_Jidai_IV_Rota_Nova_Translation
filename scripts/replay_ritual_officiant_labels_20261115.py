"""Compare both revised nameplates in original Rafael dialogue with ordinary inputs."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
import sys

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from scripts import headless_desmume_v193 as harness
from scripts import stage_ritual_officiant_labels_20261115 as stage
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_captain_biographies_v1 import captured, shots


base = stage.base
OUTPUT = stage.ROOT / 'story_nameplates.json'
SHEET = stage.ROOT / 'story_nameplates.png'
INPUTS = Path('work/analysis/Julio_script_correction_20261101/ordinary_Rafael_inputs.json')
ROUTE = '/data/SC0.DK4'
SCENES = {162: 132, 304: 135}
CAPTURES = (2800, 3400, *range(3970, 6900, 60), 7160, 7480)
NAME_SECTION = (12, 276, 84, 289)
PLAQUE = (0, 272, 88, 289)
INK = (98, 97, 98)


def replay(block, side):
    parent = stage.parent
    rom, expected = (parent.ROM, base.load(parent.RELEASE)['candidate_sha256']) if side == 'previous' else (
        stage.ROM, base.load(stage.STORED)['candidate_sha256'])
    assert base.digest(rom) == expected
    folder = stage.ROOT / f'scene_{block}_{side}'
    folder.mkdir()
    image, clean = [base.NdsImage.open(path) for path in (rom, stage.CLEAN)]
    arm = image.read_file(stage.ARM)
    archive = image.read_file(ROUTE)
    blocks = IlnkContainer.parse(archive).blocks
    opening, scene = blocks[44], blocks[block]
    original_opening = IlnkContainer.parse(clean.read_file(ROUTE)).blocks[44]
    inventory, _, _ = scoped_inventory()
    _, opening_dialogue = inventory(arm, opening)
    assert opening_dialogue[0]['offset'] == 40 and opening[8:40] == original_opening[8:40]
    commands, speeches = inventory(arm, scene)
    assert any(scene[row['offset'] + 5] == SCENES[block] for row in speeches)
    assert commands[-1]['word'] == 0
    end = commands[-1]['offset'] + commands[-1]['native_extent']
    # Prepend the original New Game initialization and keep the complete target block.
    content = bytearray(opening[:40] + scene[8:end])
    pack_into('<H', content, 4, len(content) - 8)
    inserted = bytes(content) + bytes(-len(content) % 4)
    prepared, _ = inventory(arm, inserted)
    moved = [row for row in prepared if row['offset'] >= 40]
    assert len(moved) == len(commands)
    for old, new in zip(commands, moved, strict=True):
        assert old['offset'] + 32 == new['offset'] and old['whole_command_hex'] == new['whole_command_hex']
    blocks[44] = inserted
    image.replace_file(ROUTE, IlnkContainer(blocks).to_bytes())
    fixture = folder / 'initialized_dialogue_RESEARCH_ONLY.nds'
    image.save(fixture)
    image.replace_file(ROUTE, archive)
    assert bytes(image.rom.save()) == rom.read_bytes()

    events = [row for row in base.load(INPUTS) if row['start'] < 7480]
    program = folder / 'inputs.json'
    base.save(program, events)
    old_argv = sys.argv
    try:
        sys.argv = [harness.__file__, '--rom', str(fixture), '--out', str(folder / 'capture'), '--frames', '7501',
                    '--inputs-json', str(program), '--press-start', '-1', '--capture-every', '999999',
                    '--capture-at', *map(str, CAPTURES)]
        harness.main()
    finally:
        sys.argv = old_argv
    report = folder / 'capture/capture_report.json'
    data = base.load(report)
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert data['ROM_sha256'] == base.digest(fixture) and data['scripted_input_schedule'] == events
    assert not data.get('battery_save_preloaded') and not any(v for k, v in data.items() if k.startswith('synthetic_'))
    base.save(folder / 'fixture.json', dict(base_ROM_sha256=expected, research_ROM_sha256=base.digest(fixture),
        source_route=ROUTE, source_block=block, stored_story_block_sha256=stage.digest(scene),
        original_commands=len(commands), all_commands_and_controls_transferred_bytes_exact=True,
        parent_inverse_exact=True, original_event_natural_activation=False, capture_report=str(report)))


def visible_name(font, photo, label):
    expected = set()
    for index, ch in enumerate(label):
        glyph = font.decode(ch)
        expected.update((4 + 6 * index + x, 1 + y) for x in range(6) for y in range(11) if glyph.getpixel((x, y)))
    crop = photo.crop(NAME_SECTION)
    actual = {(x, y) for x in range(crop.width) for y in range(crop.height) if crop.getpixel((x, y)) == INK}
    return actual == expected


def verify():
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    result, pictures, evidence = [], [], {}
    for block, ident in SCENES.items():
        rows = []
        for side in ('previous', 'revised'):
            path = stage.ROOT / f'scene_{block}_{side}' / 'fixture.json'
            fixture = base.load(path)
            report = Path(fixture['capture_report'])
            evidence.update({str(p): base.digest(p) for p in (report, path)})
            rows.append((fixture, shots(base.load(report))))
        (before, old), (after, new) = rows
        assert before['stored_story_block_sha256'] == after['stored_story_block_sha256']
        assert old.keys() == new.keys()
        equal, changed = [], []
        for frame in old:
            a, b = captured(old[frame]), captured(new[frame])
            if a.tobytes() == b.tobytes():
                equal.append(frame)
                continue
            extent = ImageChops.difference(a, b).getbbox()
            assert PLAQUE[0] <= extent[0] < extent[2] <= PLAQUE[2]
            assert PLAQUE[1] <= extent[1] < extent[3] <= PLAQUE[3]
            if visible_name(font, a, 'Priest') and visible_name(font, b, 'Officiant'):
                changed.append(dict(frame=frame, bounds=extent, source=old[frame], target=new[frame]))
                if len(changed) == 1:
                    pictures.append((f'Rafael B{block} | Actor {ident}', a, b))
        assert changed and equal
        result.append(dict(block=block, actor_ID=ident, matched_complete_nameplates=changed, exact_control_frames=equal,
                           all_sampled_image_differences_inside_nameplate=True))
    sheet = Image.new('RGB', (1024, 2 * 274), '#222d33')
    draw = ImageDraw.Draw(sheet)
    for row, (title, a, b) in enumerate(pictures):
        for col, (name, photo) in enumerate((('Previous', a), ('Revised', b))):
            draw.text((col * 512 + 8, row * 274 + 8), f'{title} | {name}', fill='white')
            sheet.paste(photo.crop((0, 264, 256, 384)).resize((512, 240), Image.Resampling.NEAREST), (col * 512, row * 274 + 28))
    sheet.save(SHEET)
    base.save(OUTPUT, dict(candidate_sha256=base.digest(stage.ROM), results=result, sheet=str(SHEET),
                           sheet_sha256=base.digest(SHEET), evidence=evidence,
                           scope='Initialized Rafael script replay for both actor IDs. Ordinary controller inputs. Natural acquisition not exercised.'))
    print('Verified both Officiant nameplates:', [len(row['matched_complete_nameplates']) for row in result])


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--block', type=int, choices=SCENES)
    parser.add_argument('--side', choices=('previous', 'revised'))
    args = parser.parse_args()
    if args.block is None:
        verify()
    else:
        assert args.side
        replay(args.block, args.side)
