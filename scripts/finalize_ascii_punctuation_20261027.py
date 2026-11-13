"""Write the verified test-ROM handoff without promotion or altering previous tests."""

import json
from pathlib import Path
from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_ascii_punctuation_20261027 import ROOT, ROM, CONFIG, PROFILE, save


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    release = read(ROOT / 'release_verification.json')
    dialogue = read(ROOT / 'dialogue_verification.json')
    captures = read(ROOT / 'capture_verification.json')
    native = read(ROOT / 'native_bounds.json')
    digest = sha(ROM.read_bytes())
    assert release['candidate_sha256'] == dialogue['candidate_sha256'] == captures['candidate_sha256'] == digest
    audit = read(ROOT / 'punctuation_audit.json')
    audit['unchanged_findings']['~'] = 'Flat top bar; check whether the legacy Japanese overline mapping is intentional before drawing a wave.'
    save(ROOT / 'punctuation_audit.json', audit)
    sheet = Image.new('RGB', (1024, 435), '#17252b')
    draw = ImageDraw.Draw(sheet)
    for column, folder in enumerate([Path('work/font_offset_one_20261027'), ROOT]):
        report = read(folder / 'cold_boot_hodram/capture_report.json')
        frames = {r['frame']: r for r in report['frames_captured']}
        draw.text((column * 512 + 10, 8), 'Before' if column == 0 else 'Punctuation test / same +1 offset', fill='white')
        for i, frame in enumerate([2000, 6000]):
            source = Image.open(frames[frame]['path']).convert('RGB')
            assert sha(Path(frames[frame]['path']).read_bytes()) == frames[frame]['PNG_sha256']
            image = source.crop((0, 288, 256, 384)).resize((512, 192), Image.Resampling.NEAREST)
            sheet.paste(image, (column * 512, 32 + i * 200))
    sheet.save(ROOT / 'live_punctuation_before_after.png')
    pins_path = Path('translations/rom_retention_pins.json')
    original = pins_path.read_bytes()
    pins = json.loads(original)
    physical = ROM.resolve().as_posix()
    if not any(p['path'] == physical for p in pins):
        pins.append(dict(path=physical, reason='User-requested comma/question-mark font trial; retain for gameplay testing and rollback comparison. SHA-256 ' + digest))
        assert pins_path.read_bytes() == original
        save(pins_path, pins)
    manifest = ROM.with_suffix('.manifest.json')
    base = release['canonical_base']
    note = f'''# Comma and question-mark test ROM, 2026-10-27

Experimental profile: `{PROFILE}`. User acceptance pending; promoted main remains V4701.

Candidate: `{ROM}`  
SHA-256: `{digest}`  
Manifest: `{manifest}`

Rebuilt by the integrated release builder from immutable canonical base
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
The complete V4749/font stack is retained: {release['complete_manifest_batches']} manifest entries,
including all {release['existing_accepted_layers']} accepted layers already baked into the canonical base.

Compared with the prior Y+1 trial (`out/font_v2_draw_down_one_20261027_test.nds`,
SHA-256 `fed25c1b5c360d32164e6530ca8106d1abaf87167531c66ce2dda01328341a6f`),
only `/__arm9__.bin` changes: {release['changed_ARM9_byte_count']} byte values within the two owned
11-byte comma and question-mark bitmaps. All other glyphs, including improved descenders and
brackets, are identical. Every instruction, helper, advance, drawing offset and line-spacing byte
is identical to the prior Y+1 trial. Biography pitch remains12 pixels; dialogue pitch remains16.
Other files, story text, Japanese font, artwork, overlays, autoload sections and extents are unchanged.
Complete canonical-base changed paths and record IDs are listed in the neighboring manifest.

The comma now has a head at baseline row8 and a tail through rows9/10. The question mark has
an open hook, shorter stem, two blank rows before a single-pixel baseline dot. Both retain the
6-pixel advance and11-row cell. The existing Y+1 drawing position fits all12 available cell rows.

## Verification

- Integrated manifest/source/dependency locks, canonical baseline verifier and exact predecessor file comparison pass.
- {native['guarded_case_count']} actual native painter cases cover both4-bit and16-bit surfaces,
  eight backing heights, all32 ASCII punctuation glyphs and g/j/p/q/y. Full available pixels and memory guards pass.
- Native footer constructor, caption rasterization and complete14-row copies pass, including comma/question-mark
  stress captions and descender tails. Allocator-return and GPU-copy boundaries are declared in the proof.
- 29 existing integrated-release/font regression tests pass.
- Three actual DeSmuME cold boots cover28403frames: Lil startup4001, Hodram7001 and town17401.
  Town uses an isolated copy of the retained battery fixture; other runs use ordinary controller inputs.
  No loaded savestate or newly injected gameplay state. Original donor save unchanged.
- The actual question mark in `Everything correct?` matches the complete revised glyph mask
  ({dialogue['confirmation_full_ink_pixels']} ink pixels for the whole sentence), with no stray ink below.
  `Aye, aye!` matches every ink and blank pixel, including the comma's final tail row.
  `Aye!`, three Lil opening lines and three Hodram biography lines also pass complete masks and empty-row checks.
- All eight startup/town button masks remain complete and at the same Y+1 placement.
  Native stress captions preserve full punctuation/letter tails. This is targeted emulator verification,
  not a full playthrough or hardware verification.

## Other punctuation found, unchanged in this ROM

- Semicolon: tail stops at baseline; strongest candidate for a further below-baseline correction.
- Double quotation marks: connected top row makes the two strokes less distinct.
- Period/exclamation mark: dot weights/orientations differ from the revised question mark; a consistency review may help.
- Tilde: flat top bar. Check the legacy Japanese overline mapping and actual uses before changing it into a wave.
- Backslash position contains a yen-shaped glyph, consistent with legacy Japanese font conventions.
  Check currency/encoding uses before replacement. No automatic currency-symbol change was made.
- Existing completed brackets, parentheses, braces, dollar sign and underscore remain intact.

## Evidence and reproducibility

`work/font_punctuation_20261027/` contains source/registry snapshots, proposed ARM9,
native proofs, exact cold-boot plans, capture reports/hashes, complete mask results,
32-glyph audit, before/after specimens and actual paired screenshots. The patch producer is
`dk4tool/patch/ascii_punctuation_20261027.py`, locked by `{CONFIG}`.
Build command: `python scripts/build_integrated_release.py --profile {PROFILE} --out {ROM}`.
Historical modules, prior test ROMs, failed experiments and main/baseline artifacts are preserved.
Candidate pinned using its resolved physical E-drive path. Retention preview is recorded separately;
no ROM deletion is authorized by this punctuation test handoff.
'''
    output = ROM.with_suffix('.README.md')
    assert not output.exists()
    output.write_text(note, encoding='utf-8')
    doc = Path('docs/font_punctuation_20261027.md')
    assert not doc.exists()
    doc.write_text(note, encoding='utf-8')
    entry = '''

## Comma/question-mark font test, 2026-10-27

Registered experimental profile font-v2-punctuation-one-pixel-20261027 retains the complete V4749/font stack,
Y+1 painter and unchanged12pixel biography/16pixel dialogue spacing. Only comma/question-mark bitmap bytes
change in ARM9; every other glyph, code byte, ROM file and artwork is identical to the prior Y+1 test.
592 native guarded cases, full native footer punctuation/descender captions,29 regressions and three actual
cold boots (28403frames) pass. Actual Everything correct? and Aye, aye! masks include the revised punctuation
with no stray ink below; eight actual button masks and full biography/opening masks pass. Town uses an
isolated retained battery fixture. Semicolon tail, connected double quotes, punctuation dot consistency and
legacy flat-bar tilde are flagged for review, unchanged. Yen-shaped backslash mapping requires encoding/currency
context before alteration. Targeted emulator evidence only; user acceptance pending. MainV4701 and canonical
base unchanged; all prior ROMs/failures retained. See [punctuation test](font_punctuation_20261027.md).
'''
    for name in ['known_issues.md', 'todo.md']:
        with (Path('docs') / name).open('a', encoding='utf-8') as handle:
            handle.write(entry)
    print('Handoff, audit, paired live screenshots and retention pin written:', digest)
