"""Record the requested one-pixel experimental release and preserve rollback files."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/font_offset_one_20261027')
ROM = Path('out/font_v2_draw_down_one_20261027_test.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    release = read(ROOT / 'release_verification.json')
    captures = read(ROOT / 'capture_verification.json')
    dialogue = read(ROOT / 'dialogue_verification.json')
    replies = read(ROOT / 'short_reply_verification.json')
    sailing = read(ROOT / 'sailing_button_verification.json')
    native = read(ROOT / 'native_font_offset_proof.json')
    exact = read(ROOT / 'exact_change_verification.json')
    visual = read(ROOT / 'visual_review.json')
    assert visual['reviewed'] and not visual['blocking_findings']
    digest = sha(ROM.read_bytes())
    assert release['candidate_sha256'] == captures['candidate_sha256'] == dialogue['candidate_sha256'] == sailing['candidate_sha256'] == digest
    assert dialogue['biography_line_spacing_pixels'] == 12 and dialogue['confirmation_extra_pixels_below'] == []
    assert len(replies['actual_original_Hodram_reply_panels']) == 2 and sailing['all_three_Inspect_descenders_complete']
    assert exact['all_other_ROM_bytes_identical'] and exact['byte_exact_confirmed_diagnostic_ROM']
    assert native['guarded_glyph_cases'] == 128 and captures['paired_button_mask_count'] == 8
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest
    note = f'''# One-pixel font offset - experimental test ROM

`{ROM.name}` keeps the improved letters and draws the live ASCII font one pixel
below its original drawing origin. This is one pixel higher than the previous
two-pixel-offset trial. The biography line spacing remains12 pixels. No letter
shapes, dialogue, wrapping, line-spacing instructions or other layout settings change.

Use a fresh emulator boot for testing. Your previous ROMs and promoted main are
preserved. This candidate is experimental and awaits your gameplay acceptance.

## Exact build provenance

- Candidate SHA-256: `{digest}`
- Profile: `{release['profile']}`
- Registered construction predecessor stack: `{release['predecessor']}`
- Predecessor SHA-256: `{release['predecessor_sha256']}`
- Immutable canonical base: `{release['canonical_base']['path']}`
- Canonical SHA-256: `{release['canonical_base']['sha256']}`
- Complete V4749 plus improved-font stack and registered one-pixel guarded painter:
  {release['complete_manifest_batches']} manifest entries and all{release['existing_accepted_layers']} accepted baked layers.
- Only `/__arm9__.bin` changes from the improved-font predecessor. The integrated
  builder reconstructs the full stack from the canonical base; no revoked ROM or
  research ROM is used as a construction parent or byte source.
- Read-only comparison with the previous two-pixel trial shows exactly one changed
  ROM byte: the drawing instruction's immediate2 becomes1. Every other ROM byte,
  including the improved1045-byte font, biography settings,14-row button strip and
  lazy1792-byte button buffer, is identical. The output also exactly matches the
  previously verified one-pixel diagnostic ROM.
- Original staged pool, autoload extents, Japanese font, controller icons, artwork,
  source files, accepted status and promoted main V4701 are preserved.

## Verification

- Canonical baseline, complete registry snapshot/profile/manifest, unchanged-file
  and code ownership, helper-slot references and exact font identity pass.
-128 guarded native glyph cases across both pixel formats and tight buffer heights
  pass. Full descenders and completed brackets/symbols remain inside the tested
  drawing bounds. Four-line native dialogue retains its original16-pixel row pitch.
-29 existing integrated-release/font regression tests pass.
- Four fresh cold boots cover7001 Hodram frames,4001 Lil New Game frames,17401
  town/refit frames and32800 sailing frames. No loaded savestate or callback errors.
  The town run uses the existing isolated test battery; the other replays use
  ordinary inputs without injected gameplay state. This is targeted emulator
  evidence, not a complete route or hardware test.
- Hodram's `Everything correct?` matches all213 glyph-ink pixels and all blank
  cells; the former stray-dot rows below are clean.
- Actual `Aye!` and `Aye, aye!` replies have complete masks and no pixels below
  their glyph cells. The Lil opening's three complete lines and rows below also pass.
- All three biography lines have complete masks atY330/342/354: unchanged12-pixel
  spacing. This change intentionally does not increase the gap between those lines.
- Eight actual startup/town button masks are exactly one pixel below the original
  high-font test. Twelve sailing button masks pass, including the full `p` tail in
  `Inspect` at all three sampled frames. No tail clipping found in these samples.
- Title, selection/biography, confirmation, short replies, opening dialogue,
  town/refit and sailing screenshots were viewed. Other game screens remain for
  your gameplay testing before acceptance.

The prior two-pixel profiles remain revoked and their failures/proofs preserved.
They had passed button checks, but did not fit the original12-pixel modal glyph
cell. This candidate uses11 glyph rows plus a1-pixel offset and adds explicit
checks for stray pixels outside the normal glyph rectangle.

Evidence and previews: `work/font_offset_one_20261027/`.
'''
    Path('docs/font_offset_one_20261027.md').write_text(note, encoding='utf-8')
    ROM.with_suffix('.README.md').write_text(note, encoding='utf-8')
    heading = 'One-pixel font-offset playable test, 2026-10-27'
    summary = ('\r\n\r\n## ' + heading + '\r\n\r\n'
        'Registered complete V4749/improved-font successor usesY+1 and retains biography12pixel line spacing. '
        'All other bytes match the prior two-pixel trial; reconstruction uses only the canonical baseline '
        'and nonrevoked improved-font profile. Full Everything correct?, Aye!, Aye, aye! and three Lil '
        'opening masks plus empty rows below pass. All three biography lines retain12pixel pitch. '
        '128 guarded native cases,29 regressions,eight actual startup/town button masks and twelve '
        'sailing masks (including three full Inspect p tails) pass. Four cold boots cover61203frames; '
        'town uses the inherited isolated battery,others ordinary input. Sheets viewed. Targeted emulator '
        'evidence only;experimental user acceptance pending. MainV4701, canonical base,previous ROMs, '
        'revoked experiments,translation ledger and all historical proofs remain unchanged. '
        'See [one-pixel font test](font_offset_one_20261027.md).\r\n')
    for path in [Path('docs/known_issues.md'), Path('docs/todo.md')]:
        if heading not in path.read_text(encoding='utf-8'):
            with path.open('a', encoding='utf-8', newline='') as stream:
                stream.write(summary)
    pin_path = Path('translations/rom_retention_pins.json')
    pins = read(pin_path)
    if not any(Path(p['path']).resolve() == ROM.resolve() for p in pins):
        pins.append(dict(path=ROM.resolve().as_posix(), reason='User-requested one-pixel font-offset test; preserve during gameplay testing and rollback comparison.'))
    pin_path.write_text(json.dumps(pins, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    handoff = dict(candidate=str(ROM.resolve()), candidate_sha256=digest,
        manifest=str(ROM.with_suffix('.manifest.json').resolve()), manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        profile=release['profile'], base=release['canonical_base'], changed_internal_files=['/__arm9__.bin'],
        improved_font_unchanged=True, biography_line_spacing_unchanged=True,
        previous_ROMs_and_main_preserved=True, experimental_user_acceptance_pending=True)
    (ROOT / 'handoff.json').write_text(json.dumps(handoff, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(handoff, indent=2))
