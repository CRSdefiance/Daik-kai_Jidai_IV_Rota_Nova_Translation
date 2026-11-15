"""Record the separate experimental handoff without promoting or replacing a ROM."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/font_test_20261027')
ROM = Path('out/font_descenders_symbols_v2_20261027_test.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    release = read(ROOT / 'release_verification.json')
    comparison = read(ROOT / 'cold_boot_comparison.json')
    visual = read(ROOT / 'visual_review.json')
    assert visual['reviewed'] and not visual['blocking_findings']
    assert release['candidate_sha256'] == sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == release['candidate_sha256']
    assert all(r['same_core_options_inputs_and_frame_schedule'] for r in comparison['runs'])
    total_frames = sum(r['frames'] for r in comparison['runs'])
    pairs = sum(len(r['paired_captures']) for r in comparison['runs'])
    note = f'''# Experimental font test - 2026-10-27

Load `font_descenders_symbols_v2_20261027_test.nds` normally in the emulator.
Cold boot the ROM rather than loading an old emulator savestate. The promoted
main and the V4749 predecessor remain available for rollback.

This uses the exact v2 mockup pixels: ordinary ASCII letters sit two pixels
higher inside their existing cells, `g j p q y` have full descenders, and
`[ ] ( ) {{ }} $ _` have their completed strokes. Tall punctuation shifts only
as far as its original top margin permits. Character widths, line spacing,
textbox origins, wrapping, Japanese fonts and pre-rendered artwork are retained.
The shift is stored in the glyph cells; no global textbox offset is patched.

## Build provenance

- Candidate: `{ROM.name}`
- Candidate SHA-256: `{release['candidate_sha256']}`
- Profile: `{manifest['profile']}`
- Complete predecessor: `out/all_routes_combined_v4749_candidate.nds`
- Predecessor SHA-256: `{release['predecessor_sha256']}`
- Immutable construction base: `{release['baseline']['path']}`
- Construction-base SHA-256: `{release['baseline']['sha256']}`
- Changed from V4749: only `/__arm9__.bin`, font bytes `[0x125A60,0x125E75)`.
  All other ARM9 bytes and every other internal file/component are identical.
- All {release['all_accepted_layers_preserved']} accepted baked layers and the full V4749
  stack remain present; {release['total_batches']} manifest entries include this font config.
- Promoted main stays V4701; no promotion, baseline replacement or editorial credit.

## Checks and limits

- Exact frozen registry, manifest, baseline, predecessor and font hashes pass.
- All94 printable glyphs pass independent complete native-renderer pixel checks;
  four-row dialogue and symbol samples preserve all glyphs and16-pixel row spacing.
- Existing release/font regression tests:29 passed. Original baked-artwork guards
  retain all exact material and glyph checks against their original source font.
- Two fresh automated DeSmuME cold boots:4001 New Game frames and17401 town/refit
  frames ({total_frames} total), with{pairs} matching-timing before/after captures.
  No savestate or callback errors. Opening background/portrait and selected refit
  artwork regions match V4749. Revised live lettering is intentionally different.
- Both before/after sheets were viewed. No blocking clipping was seen in the
  sampled title, character selection, opening dialogue or town/refit screens.
- The town run uses the existing isolated test battery; it does not establish
  earned progress. These are targeted emulator checks, not full-route or hardware
  testing. The supplied original guild scene has controlled native pixel coverage,
  rather than a new replay of that exact event. User gameplay acceptance is pending.

Review `g j p q y`, brackets/parentheses, nameplates and short menus during play.
The manifest beside the ROM records the full cumulative stack and changed records.
Evidence: `work/font_test_20261027/`. Original mockup files are retained.

The first build was rejected because a static sign-art check compared unchanged
art to the replacement runtime font. No ROM was saved by that failed build.
The successful successor checks final artwork with its exact original font and
keeps every original byte, pixel, palette, geometry and ownership guard.
'''
    Path('docs/font_test_20261027.md').write_text(note, encoding='utf-8')
    ROM.with_suffix('.README.md').write_text(note, encoding='utf-8')
    summary = ('\r\n\r\n## Experimental v2 ASCII font test, 2026-10-27\r\n\r\n'
        'Separate full V4749 successor applies the requested raised glyphs, complete descenders '
        'and bracket/symbol strokes. Only the original1045-byte ARM9 font span differs; '
        'code, spacing, text, Japanese fonts and artwork remain exact to V4749. '
        'Registered builder, baseline,94 native glyphs,29 regressions and two fresh cold boots '
        '(4001 New Game/17401 town frames) pass;31 paired captures and both review sheets checked. '
        'Targeted emulator evidence only;user gameplay acceptance pending. Promoted main V4701 '
        'and canonical baseline unchanged. Initial static-art reference failure retained; '
        'the final guard still checks complete original artwork bytes and pixels. '
        'See [font test details](font_test_20261027.md).\r\n')
    for path in [Path('docs/known_issues.md'), Path('docs/todo.md')]:
        if 'Experimental v2 ASCII font test, 2026-10-27' not in path.read_text(encoding='utf-8'):
            with path.open('a', encoding='utf-8', newline='') as stream:
                stream.write(summary)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    for path in [ROM, Path(release['predecessor'])]:
        resolved = path.resolve().as_posix()
        if not any(Path(p['path']).resolve() == path.resolve() for p in pins):
            pins.append(dict(path=resolved, reason='User-requested font experiment and exact rollback comparator; preserve during gameplay testing.'))
    pins_path.write_text(json.dumps(pins, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    handoff = dict(candidate=str(ROM.resolve()), candidate_sha256=release['candidate_sha256'],
        manifest=str(ROM.with_suffix('.manifest.json').resolve()),
        manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        profile=manifest['profile'], promoted_main_unchanged=True,
        visual_review=str(ROOT / 'visual_review.json'), user_gameplay_acceptance_pending=True)
    (ROOT / 'handoff.json').write_text(json.dumps(handoff, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(handoff, indent=2))
