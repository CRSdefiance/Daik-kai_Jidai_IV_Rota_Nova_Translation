"""Package the five-glyph trial with proof, applied specimens and rollback provenance."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_punctuation_all_20261027 import GLYPHS
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_ascii_punctuation_all_20261027 import ROOT, ROM, PARENT, CONFIG, PROFILE, save
from scripts.preview_other_punctuation_20261027 import PROPOSALS, raster


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    release = read(ROOT / 'release_verification.json')
    dialogue = read(ROOT / 'dialogue_verification.json')
    captures = read(ROOT / 'capture_verification.json')
    native = read(ROOT / 'native_bounds.json')
    cursor = read(ROOT / 'cursor_verification.json')
    digest = sha(ROM.read_bytes())
    assert release['candidate_sha256'] == dialogue['candidate_sha256'] == captures['candidate_sha256'] == digest
    assert cursor['all_glyph_positions_identical']
    assert '29 passed' in (ROOT / 'regression_tests.log').read_text(encoding='utf-8')
    before = GameAsciiFont.from_arm9(NdsImage.open(PARENT).read_file('/__arm9__.bin'))
    after = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    rows = []
    for char, item in PROPOSALS.items():
        glyph = after.decode(char)
        actual = [''.join('#' if glyph.getpixel((x, y)) else '.' for x in range(6)) for y in range(11)]
        assert actual == item['rows'] == GLYPHS[char]
        rows.append(dict(character=char, rows=actual, exact_approved_design=True))
    save(ROOT / 'applied_design_verification.json', dict(candidate_sha256=digest,
        font_sha256=sha(after.glyphs), all_five_exact_approved_designs=rows,
        fixed_glyph_width=6, fixed_bitmap_height=11, native_drawing_offset_y=1))
    title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 30)
    heading = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
    normal = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    sheet = Image.new('RGB', (1320, 770), '#17252b')
    draw = ImageDraw.Draw(sheet)
    draw.text((26, 18), 'Approved punctuation applied to the new test ROM', font=title, fill='white')
    draw.text((240, 75), 'PREVIOUS TEST', font=heading, fill='#cbd8dc')
    draw.text((800, 75), 'NEW TEST ROM', font=heading, fill='#9bdfc2')
    for i, (char, item) in enumerate(PROPOSALS.items()):
        top = 125 + i * 118
        name = item['name'].replace(' (optional)', '')
        draw.text((26, top + 12), name, font=heading, fill='white')
        for x, font in [(240, before), (800, after)]:
            sample = raster(font, item['sample'])
            sheet.paste(sample.resize((sample.width * 5, 60), Image.Resampling.NEAREST), (x, top))
    draw.text((26, 735), 'Extracted from both actual ROMs. Same +1 offset and spacing; all following letters keep their positions.', font=normal, fill='#cbd8dc')
    sheet.save(ROOT / 'applied_punctuation_before_after.png')
    paired = Image.new('RGB', (1024, 635), '#17252b')
    draw = ImageDraw.Draw(paired)
    for column, folder in enumerate([Path('work/font_punctuation_20261027'), ROOT]):
        report = read(folder / 'cold_boot_hodram/capture_report.json')
        frames = {r['frame']: r for r in report['frames_captured']}
        draw.text((column * 512 + 10, 8), 'Previous test' if column == 0 else 'New five-punctuation test / same +1 offset', fill='white')
        for i, frame in enumerate([2000, 4000, 6000]):
            assert sha(Path(frames[frame]['path']).read_bytes()) == frames[frame]['PNG_sha256']
            source = Image.open(frames[frame]['path']).convert('RGB')
            picture = source.crop((0, 288, 256, 384)).resize((512, 192), Image.Resampling.NEAREST)
            paired.paste(picture, (column * 512, 32 + i * 200))
    paired.save(ROOT / 'live_punctuation_before_after.png')
    pins_path = Path('translations/rom_retention_pins.json')
    original = pins_path.read_bytes()
    pins = json.loads(original)
    physical = ROM.resolve().as_posix()
    if not any(p['path'] == physical for p in pins):
        pins.append(dict(path=physical, reason='User-requested complete five-punctuation font trial; retain for gameplay testing and rollback. SHA-256 ' + digest))
        assert pins_path.read_bytes() == original
        save(pins_path, pins)
    note = f'''# All approved punctuation test ROM, 2026-10-27

Candidate: `{ROM}`  
SHA-256: `{digest}`  
Manifest: `{ROM.with_suffix('.manifest.json')}`  
Experimental profile: `{PROFILE}`. Design approval is recorded by the user's request to apply all five
previewed revisions; no promotion of this playable candidate is inferred. Main remains V4701.

## Exact change and continuity

Built with the integrated release builder from immutable canonical base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Complete V4749/font stack retained: {release['complete_manifest_batches']} manifest entries and all
{release['existing_accepted_layers']} accepted layers already baked into that base.

Relative to `out/font_v2_punctuation_one_pixel_20261027_test.nds`, SHA-256
`9c2494830c3a60655fb09ab5cc67842851cbdbe8609083084ec447b81b363258`, only `/__arm9__.bin` changes:
{release['changed_ARM9_byte_count']} byte values within five owned11-byte glyph bitmaps. Every other
glyph (including improved letters, comma, question mark and completed brackets), every code byte,
all other files, story text, Japanese font, artwork, overlays and autoload sections/extents are identical.
Canonical-base changed paths and record IDs are in the neighboring manifest.

- Semicolon: single upper dot and full comma tail through raw row10.
- Double quotation marks: two separate curved strokes, matching the approved preview.
- Period: a single baseline dot.
- Exclamation mark: shorter stem and dot/gap matching the revised question mark.
- Tilde: the approved wavy shape replaces the former flat bar. Encoded text and the yen-shaped
  backslash glyph are unchanged.

All five match the exact previously shown designs. Character advance remains6 pixels; bitmap
height remains11; native drawing offset remainsY+1. Biography pitch remains12 and dialogue pitch16.
The quote can use an additional ink column inside its existing cell; following letters do not move.

## Verification

- Integrated manifest/dependency/source locks, baseline verifier and complete predecessor file comparison pass.
- Only the five owned glyph spans change; all executable code and layout bytes are identical to the prior test.
- {native['guarded_case_count']} actual native painter cases pass: both4-bit/16-bit modes, eight backing heights,
  all32 ASCII punctuation glyphs and g/j/p/q/y. Every available ink/blank pixel and memory guard matches.
- Native four-line sample includes all five revisions. Before/after painter events are identical for every
  glyph, proving quoted text and all following characters keep their x/y positions. Row pitch remains16.
- Native footer construction, rasterization and14-row copy checks pass for original captions and constructed
  stress captions containing all five new glyphs plus comma/question mark and descenders. Native allocator
  returns and final GPU copies are explicit test boundaries; actual button composition is checked separately.
- 29 existing integrated-release/font tests pass; retained log `regression_tests.log`.
- Three actual DeSmuME cold boots cover28403frames: New Game4001, Hodram7001 and town17401.
  Town uses an isolated copy of a retained battery fixture; others ordinary inputs. No loaded savestate or
  newly injected gameplay state. Original donor save preserved.
- Actual `Everything correct?`, `Warn them.`, `Aye!`, `Aye, aye!` and three Lil opening lines match complete glyph masks,
  including revised period/exclamation pixels and comma tails, with clean rows below. Three Hodram biography
  masks retain12pixel pitch. All eight startup/town button masks pass at the unchangedY+1 position.
- Semicolon, quotation marks and tilde are exercised in controlled native raster/footer checks, not a newly
  discovered ordinary gameplay occurrence. This is targeted emulator verification, not a full playthrough
  or hardware verification. Sheets and visual review are recorded separately under the evidence root.

## Evidence and reproduction

Evidence: `work/font_punctuation_all_20261027/`: registry before/after snapshots, proposed ARM9,
native pixel/guard/cursor proofs, cold-boot input plans, capture reports and hashes, full pixel masks,
regression log, applied font specimen and paired actual dialogue captures.
Patch: `dk4tool/patch/ascii_punctuation_all_20261027.py`. Locked config: `{CONFIG}`.
The reviewed preview producer is also dependency-locked; the final extracted ROM glyphs are checked against it.

Build: `python scripts/build_integrated_release.py --profile {PROFILE} --out {ROM}`.
Previous ROMs, historical producers, failed experiments, main and canonical base are preserved.
Candidate pinned by its resolved physical E-drive path. Retention-preview result is recorded separately;
no ROMs are deleted by this handoff.
'''
    for path in [ROM.with_suffix('.README.md'), Path('docs/font_punctuation_all_20261027.md')]:
        assert not path.exists()
        path.write_text(note, encoding='utf-8')
    entry = '''

## All five approved punctuation designs applied, 2026-10-27

Experimental profile font-v2-all-punctuation-one-pixel-20261027 preserves the complete V4749/font stack and
applies the exact previewed semicolon, double-quote, period, exclamation and wavy-tilde shapes. Only these
five ARM9 glyph bitmaps change from the comma/question-mark test; all other glyphs, files and code/layout
bytes are identical. Y+1,6pixel advance,12pixel biography pitch and16pixel dialogue pitch remain unchanged.
592 guarded native cases, original/stress footer captions, exact before/after per-glyph cursor events and29
regressions pass. Three actual cold boots (28403frames) verify full dialogue masks/empty rows, biography
spacing and eight button masks. Town uses the isolated retained battery fixture. Semicolon/quotes/tilde
use controlled native samples; no ordinary gameplay occurrence or full-route/hardware verification claimed.
Yen-shaped backslash unchanged. MainV4701 and canonical base unchanged; user gameplay acceptance pending.
All prior trials/failures retained. See [all-punctuation test](font_punctuation_all_20261027.md).
'''
    for name in ['known_issues.md', 'todo.md']:
        with (Path('docs') / name).open('a', encoding='utf-8') as handle:
            handle.write(entry)
    print('Verified five-punctuation handoff and applied specimens written:', digest)
