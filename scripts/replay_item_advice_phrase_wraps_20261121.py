"""Replay the original Items Advice button on the revised eagle and earrings replies."""

import sys
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_figurehead_navigation_gift_advice_v1 as earlier
from scripts import replay_sailing_help_20261120 as startup
from scripts import stage_item_advice_phrase_wraps_20261121 as stage
from scripts import verify_rumor_and_cooperation_v1 as portrait


base = stage.base
ITEMS = stage.ROOT / 'lisbon_items'
PROOF, SHEET = ITEMS / 'gameplay.json', ITEMS / 'lisbon_advice_comparison.png'
ITEM_IDS = (114, 138)
ITEM_NAMES = ('Eagle Figurehead', 'Ceramic Earrings')
COMMANDS = (earlier.COMMANDS[0] | {'inventory_items': list(ITEM_IDS)}, *earlier.COMMANDS[1:])
CASES = ((3158, 9600, 9900, 10200), (3147, 10800, 11100, 11400), (3171, 11700, 12000, 12300))
TOWN = (8400, 13100)


def replay():
    binding = SimpleNamespace(ROOT=stage.ROOT, ROM=stage.ROM, PREP=stage.PROOF, RELEASE=stage.parent.RELEASE,
                              ARM=stage.ARM, load=base.load, save=base.save, digest=base.digest, NdsImage=base.NdsImage)
    env = vars(earlier) | dict(stage=binding, ITEMS=ITEMS, ITEM_IDS=ITEM_IDS, ITEM_NAMES=ITEM_NAMES, COMMANDS=COMMANDS)
    FunctionType(earlier.run.__code__, env)('items')
    verify()


def verify():
    terminal_path = ITEMS / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path = Path(terminal['report'])
    candidate_sha = base.digest(stage.ROM)
    assert base.digest(report_path) == terminal['report_sha256'] and terminal['candidate_sha256'] == candidate_sha
    report, _ = portrait.checked_report(report_path, candidate_sha, TOWN[1])
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_inventory_fixtures')
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and terminal['unchanged_original_save']
    assert base.digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    inventory, = report['synthetic_inventory_fixtures']
    assert inventory['synthetic_advice_unlock']
    assert [(r['item_id'], r['name'], r['result_owner_kind']) for r in inventory['items']] == [
        (n, name, 0) for n, name in zip(ITEM_IDS, ITEM_NAMES, strict=True)]
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = base.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal) and [row['command'] for row in journal] == list(COMMANDS)
    frames = {r['frame']: r for r in report['frames_captured'] if r['path'].endswith('_navigation.png')}
    snapshots = {r['frame']: r for r in report['read_only_capture_RAM_snapshots']}
    image = base.NdsImage.open(stage.ROM)
    arm, kanji = image.read_file(stage.ARM), image.read_file('/GRP/KANJI.FNT')
    raster, _, _ = stage.portrait.font_tools(image)
    font = GameAsciiFont.from_arm9(arm)
    offsets = [unpack_from('<I', arm, at)[0] - stage.advice.BASE for at in (0x5444C, 0x54450)]
    rows = {r['message_ID']: r for r in base.load(stage.PROOF)['records']}
    found = []
    for message, before, at, after in CASES:
        snap = snapshots[at]
        assert snap['read_only_export'] and base.digest(snap['path']) == snap['sha256']
        raw = Path(snap['path']).read_bytes()
        assert len(raw) == 0x400000
        plain, display = [raw[x:x + 256].split(b'\0', 1)[0] for x in offsets]
        row = rows[message]
        assert plain.hex() == row['staged_hex'] and display.hex() == row['display_hex']
        plane, glyphs = stage.portrait.render_portrait(raster, arm, kanji, display)
        assert stage.sha256(plane).hexdigest() == row['ink_sha256']
        assert bytes(bool(value) for value in plane) == portrait.portrait_ink(frames[at]['path'], portrait.PAPER)
        header, box = portrait.complete_mask(font, 'Hans Letzel', portrait.captured(frames[at]), 16, 277, (98, 97, 98))
        assert portrait.captured(frames[before]).tobytes() == portrait.captured(frames[after]).tobytes()
        found.append(dict(message_ID=message, item_name=row['item_name'], lines=row['visible_lines'], complete_body_ink=True,
                          glyph_count=len(glyphs), adviser='Hans Letzel', adviser_nameplate_pixels=header, nameplate_bounds=box,
                          capture=frames[at], return_to_identical_item=True, revised=message in stage.EDITS))
    assert portrait.captured(frames[TOWN[0]]).tobytes() == portrait.captured(frames[TOWN[1]]).tobytes()
    sheet = Image.new('RGB', (768, 216), '#283644')
    captions = ImageDraw.Draw(sheet)
    for i, row in enumerate(found):
        x = i * 256
        captions.text((x + 4, 4), row['item_name'], fill='white')
        sheet.paste(portrait.captured(row['capture']).crop((0, 192, 256, 384)), (x, 22))
    sheet.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=candidate_sha, actual_emulator=True, hardware=False,
                          original_Advice_button=True, inventory_and_advice_flag_fixture=True,
                          live_items=found, original_item_views_and_town_return=True, natural_inventory_acquisition=False,
                          sheet={'path': str(SHEET), 'sha256': base.digest(SHEET)},
                          evidence={str(p): base.digest(p) for p in (report_path, terminal_path, journal_path, SHEET)}))
    print('Verified the Eagle Figurehead, Ceramic Earrings and Sextant advice and exact Lisbon return.', flush=True)


if __name__ == '__main__':
    action = sys.argv[1]
    if action == 'startup':
        FunctionType(startup.startup.__code__, startup.env | {'parent': stage.parent, 'stage': stage})()
    elif action == 'verify':
        verify()
    else:
        assert action == 'play'
        replay()

