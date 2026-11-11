"""Stage and verify every BGM title through its original Sound Setup consumer."""

from hashlib import sha256
from inspect import getsource
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import TABLE_END
from scripts import probe_native_sound_selector_bounds as selector
from scripts import replay_sound_bgm_titles_v1 as baseline
from scripts import review_sound_bgm_titles_v1 as review
from scripts import verify_common_alignment_native_v257 as raster_tools
from scripts.probe_bgm_title_pixels import center
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate


base, parent = review.base, review.parent
ARM, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET = review.ARM, review.COMMON, review.DIRECTORY_OFFSET, review.TABLE_OFFSET
ROOT = parent.TEST.with_name('sound_bgm_titles_staged_20261111_v1')
ROM = ROOT / 'sound_bgm_titles_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PANEL = (128, 16)
LONGEST_ID = 3265


def stage(arm, common, rows):
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    storage = {n: rows[n]['english'].encode('ascii') for n in review.REVISIONS}
    new_common, new_arm, entries, allocation = repack(common, arm, rows, storage)
    assert set(allocation['changed_visible_templates']) == review.REVISIONS.keys()
    assert allocation['all_41_blocks_fit_8KiB'] and allocation['all_unselected_native_copy_spans_exact']
    assert new_arm[:DIRECTORY_OFFSET] == arm[:DIRECTORY_OFFSET] and new_arm[TABLE_END:] == arm[TABLE_END:]
    return new_arm, new_common, entries, allocation


def get_raster(image):
    source = checked_text(getsource(raster_tools.raster), {
        'glyph_events=None):': 'glyph_events=None, origin=0):',
        '    u.mem_write(string, text': '    u.mem_write(ctx + 36, struct.pack("<I", origin))\n    u.mem_write(string, text',
    })
    env = vars(raster_tools) | {'NdsImage': SimpleNamespace(open=lambda _: image)}
    exec(compile(source, __file__ + '::Sound-Setup-centered-origin', 'exec'), env)
    return env['raster']


def longest_live_mask(font, title, origin):
    report_path = baseline.ROOT / 'capture/capture_report.json'
    receipt = base.load(baseline.ROOT / 'terminal.json')
    report = base.load(report_path)
    assert base.digest(report_path) == receipt['report_sha256']
    assert report['ROM_sha256'] == receipt['candidate_sha256'] == base.digest(parent.ROM)
    frame, = (row for row in report['frames_captured'] if row['frame'] == baseline.LONGEST)
    assert base.digest(frame['path']) == frame['PNG_sha256']
    image = Image.open(frame['path']).convert('RGB')
    ink = {(x, y) for y in range(258, 271) for x in range(PANEL[0])
           if image.getpixel((x, y)) == (230, 230, 230)}
    expected = {(origin + i * 5 + x, 259 + y) for i, char in enumerate(title)
                for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
    assert ink == expected, (len(ink), len(expected), sorted(ink ^ expected)[:10])
    return dict(frame=frame, complete_actual_ink=len(ink), report_sha256=base.digest(report_path))


def verify(arm, common, image, entries, rows):
    select = FunctionType(selector.select.__code__, vars(selector) | {
        'common_message_entries': lambda *_args, **_kwargs: entries,
    })
    raster = get_raster(image)
    font = GameAsciiFont.from_arm9(arm)
    cases, pages = [], []
    for n, row in rows.items():
        text = row['english']
        raw = text.encode('ascii')
        assert select(arm, common, n - 3249) == entries[n].text == raw
        x, y, tracking = center(arm, text)
        assert x == row['planned_geometry']['left'] and y == 50 and tracking == -1
        events = []
        # The real widget shows the full odd final pair. The narrow synthetic
        # surface stops before the final e; use a backing guard and bind the
        # visible 128 pixels to the ordinary emulator replay for this title.
        surface = (136, PANEL[1]) if n == LONGEST_ID else PANEL
        plane = raster(arm, raw, 0xD5404, tracking=tracking, size=surface, origin=x,
                       instruction_limit=2000000, glyph_events=events)
        for y0 in range(PANEL[1]):
            assert not any(plane[y0 * surface[0] + PANEL[0]:(y0 + 1) * surface[0]])
        pixels = b''.join(plane[y0 * surface[0]:y0 * surface[0] + PANEL[0]] for y0 in range(PANEL[1]))
        expected = bytearray(PANEL[0] * PANEL[1])
        visible = []
        for i, char in enumerate(text):
            pos = x + 5 * i
            assert pos + 6 <= PANEL[0]
            if char != ' ':
                visible.append(dict(code=ord(char), style=1, x=pos, y=0))
            glyph = font.decode(char)
            for gy in range(11):
                for gx in range(6):
                    if glyph.getpixel((gx, gy)):
                        expected[(gy + 1) * PANEL[0] + pos + gx] = 1
        assert [event for event in events if event['code'] != 32] == visible
        assert pixels == bytes(expected), (n, text, events)
        cases.append(dict(message_ID=n, reference=review.reference(entries[n]), original_selector_index=n-3249,
            original_center=[x, y], native_pixels_sha256=sha256(pixels).hexdigest(), complete_glyphs=len(visible),
            complete_text=text, retained_longest_live_mask=longest_live_mask(font, text, x) if n == LONGEST_ID else None))
        pages.append((n, Image.frombytes('L', PANEL, bytes(32 if value else 246 for value in pixels))))
    return cases, pages


def make_sheets(pages):
    result = []
    for start in range(0, len(pages), 20):
        group = pages[start:start + 20]
        sheet = Image.new('RGB', (532, 54 * ((len(group) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (n, page) in enumerate(group):
            x, y = 266 * (i % 2) + 5, 54 * (i // 2)
            draw.text((x + 4, y + 2), f'ID {n}', fill='white')
            sheet.paste(page.resize((256, 32), Image.Resampling.NEAREST), (x, y + 18))
        path = ROOT / f'track_sheet_{1 + start // 20:02}.png'
        sheet.save(path)
        result.append(dict(path=str(path), sha256=base.digest(path), tracks=len(group)))
    return result


def main():
    assert not ROOT.exists()
    review_input = base.load(review.OUTPUT)
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] == review_input['current_ROM_sha256']
    image = base.NdsImage.open(parent.ROM)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    assert all(sha256(arm[row['start']:row['end']]).hexdigest() == row['sha256'] for row in review_input['selector_code'])
    rows = {row['message_ID']: row for row in review_input['records']}
    new_arm, new_common, entries, allocation = stage(arm, common, rows)
    cases, pages = verify(new_arm, new_common, image, entries, rows)
    image.replace_file(ARM, new_arm)
    image.replace_file(COMMON, new_common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    sheets = make_sheets(pages)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
        manuscript_sha256=base.digest(review.OUTPUT), allocation=allocation, records=cases, sheets=sheets,
        original_selector_and_painter_exact=True, complete_parent_inverse=True,
        new_credit=0, visual_review_pending=True, gameplay_pending=True))
    print('38 exact native BGM lookups and centered title masks passed. The whole parent inverse is exact.')


if __name__ == '__main__':
    main()
