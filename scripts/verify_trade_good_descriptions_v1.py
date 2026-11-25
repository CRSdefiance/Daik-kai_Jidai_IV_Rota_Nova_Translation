"""Verify the viewed pages, ordinary Price Info replay and startup evidence."""

import argparse
from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts import replay_trade_good_descriptions_v1 as replay
from scripts import verify_item_production_advice_v1 as precedent
from scripts.verify_captain_biographies_v1 import captured, shots


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT, VISUAL = ROOT / 'own_startup_verification.json', ROOT / 'visual_layout_approval.json'
LIVE = ROOT / 'trade_good_price_info_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/trade_good_descriptions_repo_qa_20261111.xml')
PAPER = (16, 296, 244, 360)
CASES = ((137, 'Wheat', 13000, (13400,), 13800),
         (145, 'Cheese', 14600, (15000, 15400), 15800),
         (142, 'Fish', 16600, (17000,), 17400))
FOCUS = {137: (144, 222, 172, 250), 145: (144, 286, 172, 314), 142: (172, 254, 200, 282)}


def verify_startup():
    loader = SimpleNamespace(load=stage.base.load, RELEASE=stage.parent.RELEASE, NdsImage=NdsImage, ARM=stage.ARM)
    FunctionType(precedent.verify_startup.__code__, vars(precedent) | globals() | {'stage': loader})()


def approve_layout(viewed):
    base = stage.base
    assert not VISUAL.exists()
    proof = base.load(PROOF)
    assert base.digest(ROM) == proof['research_ROM_sha256']
    assert base.digest(stage.OUTPUT) == proof['manuscript_sha256']
    assert viewed == [row['sha256'] for row in proof['sheets']]
    assert all(base.digest(row['path']) == row['sha256'] for row in proof['sheets'])
    assert sum(len(row['pages']) for row in proof['records']) == proof['native_pages']
    assert sum(len(sheet['messages']) for sheet in proof['sheets']) == proof['native_pages']
    assert len(proof['records']) == 124 and proof['parent_inverse_exact']
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(row.get('tests', 0)) for row in tests) == 34
    assert all(int(row.get(key, 0)) == 0 for row in tests for key in ('errors', 'failures', 'skipped'))
    base.save(VISUAL, dict(candidate_sha256=proof['research_ROM_sha256'], native_records=124,
        native_pages=proof['native_pages'], sheet_sha256=viewed, repository_tests=34,
        all_pages_viewed=True, complete_glyphs_and_page_continuations=True,
        evidence={str(p): base.digest(p) for p in (PROOF, stage.OUTPUT, QA, Path(__file__))},
        actual_gameplay_and_registration_pending=True, new_credit=0))
    print(f"Approved {proof['native_pages']} visually reviewed native pages and 34 targeted tests.")


def exact_title(font, name, image):
    x0, y0 = 160, 209
    width = (len(name) - 1) * 5 + 6
    expected = {(i * 5 + x, y) for i, c in enumerate(name) for y in range(11) for x in range(6)
                if font.decode(c).getpixel((x, y))}
    actual = {(x, y) for x in range(width) for y in range(11)
              if image.getpixel((x0 + x, y0 + y)) == (230, 230, 230)}
    assert expected == actual, name
    return dict(text=name, bounds=[x0, y0, x0 + width, y0 + 11], glyph_advance=5, exact_ink_and_blank_cells=True)


def preserved_outside_focus(before, after, bounds):
    changed = ImageChops.difference(before, after).getbbox()
    if changed is not None:
        x0, y0, x1, y1 = changed
        assert bounds[0] <= x0 <= x1 <= bounds[2] and bounds[1] <= y0 <= y1 <= bounds[3], (changed, bounds)
    return changed


def verify_live():
    base = stage.base
    proof, visual, boot = map(base.load, (PROOF, VISUAL, BOOT))
    sha = base.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == visual['candidate_sha256'] == boot['candidate_sha256']
    terminal_path = replay.ROOT / 'terminal.json'
    terminal = base.load(terminal_path)
    report_path = Path(terminal['report'])
    assert base.digest(report_path) == terminal['report_sha256']
    report = base.load(report_path)
    assert terminal['candidate_sha256'] == report['ROM_sha256'] == sha
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert terminal['unchanged_original_save']
    frames = shots(report)
    snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}
    native = {row['message_ID']: row for row in proof['records']}
    image = NdsImage.open(ROM)
    arm = image.read_file(stage.ARM)
    font = GameAsciiFont.from_arm9(arm)
    addresses = [address - 0x02000000 for address in unpack_from('<2I', arm, 0x54890)]
    observed = []
    for n, name, before, pages, after in CASES:
        initial, returned = captured(frames[before]), captured(frames[after])
        title = exact_title(font, name, initial)
        assert title == exact_title(font, name, returned)
        blink = preserved_outside_focus(initial, returned, FOCUS[n])
        pages_verified = []
        for number, (frame, page) in enumerate(zip(pages, native[n]['pages'], strict=True), 1):
            shot = captured(frames[frame])
            ink = bytes(pixel == (0, 8, 0) for pixel in shot.crop(PAPER).get_flattened_data())
            assert sha256(ink).hexdigest() == page['pixel_sha256'], (n, number, page['visible_text'])
            snap = snapshots[frame]
            assert snap['read_only_export'] and base.digest(snap['path']) == snap['sha256']
            raw = Path(snap['path']).read_bytes()
            assert len(raw) == 0x400000
            template = bytes.fromhex(native[n]['display_hex'])
            assert all(raw[at:at + len(template) + 1] == template + b'\0' for at in addresses)
            pages_verified.append(dict(page=number, lines=page['visible_text'], captured_RAM=snap,
                frame=frames[frame], exact_glyph_and_blank_cell_match=True))
        observed.append(dict(message_ID=n, commodity_name=name, native_title=title, pages=pages_verified,
            price_selection_return_exact_outside_cursor=True, cursor_blink_bounds=blink,
            before=frames[before], after=frames[after]))
    category_blink = preserved_outside_focus(captured(frames[12600]), captured(frames[17800]), (0, 222, 72, 242))
    evidence = (PROOF, VISUAL, BOOT, terminal_path, report_path, QA, Path(__file__))
    ids = [row['message_ID'] for row in observed]
    base.save(LIVE, dict(candidate_sha256=sha, observed_ids=ids, observed=observed,
        ordinary_gameplay=True, fixtures=False, hardware=False, original_Price_Info_return=True,
        category_return_cursor_blink=category_blink,
        complete_pagination_and_exact_display=True, evidence={str(p): base.digest(p) for p in evidence}))
    base.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=ids, stored_cases=124, viewed_pages=visual['native_pages'],
        evidence={str(p): base.digest(p) for p in (*evidence, LIVE)}))
    print('Verified the Price Info description pages, native popup transitions and original list return.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('startup', 'layout', 'live'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        (verify_startup if args.action == 'startup' else verify_live)()
