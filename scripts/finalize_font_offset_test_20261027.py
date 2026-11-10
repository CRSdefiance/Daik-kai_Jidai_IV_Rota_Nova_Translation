"""Handoff only the successful cumulative successor; preserve the revoked experiment."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/font_offset_test_20261027_v2')
ROM = Path('out/font_v2_draw_down_two_v2_20261027_test.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


if __name__ == '__main__':
    release = read(ROOT / 'release_verification.json')
    captures = read(ROOT / 'capture_verification.json')
    sailing = read(ROOT / 'sailing_button_verification.json')
    native = read(ROOT / 'native_font_offset_proof.json')
    visual = read(ROOT / 'visual_review.json')
    assert visual['reviewed'] and not visual['blocking_findings']
    assert release['candidate_sha256'] == captures['candidate_sha256'] == sailing['candidate_sha256'] == sha(ROM.read_bytes())
    assert captures['paired_button_mask_count'] == 8 and sailing['all_three_Inspect_p_tails_complete']
    assert native['guarded_glyph_cases'] == 128
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == release['candidate_sha256']
    total_frames = sum(r['frames'] for r in captures['runs']) + sailing['frames']
    note = f'''# Improved font with drawing position lowered two pixels - test ROM

Candidate: `{ROM.name}`. Experimental; user gameplay acceptance is pending.
Load this ROM with a fresh emulator boot. The previous font test and promoted
main are preserved for rollback. No existing save, source ROM or release is replaced.

The improved font pixels are unchanged. The common ASCII painter now draws them
two pixels lower in both4-bit and16-bit formats. Character advance, wrapping,
line spacing, dialogue, Japanese glyphs, controller icons and baked artwork retain
their existing data and behavior. Some baked artwork does not use this live font.

Button captions use a14-row text strip rather than12 rows. Their original visible
frame and horizontal placement remain intact: text copies occupy screen rows178
through191. A single zeroed1792-byte buffer is allocated through the original native
allocator at the first nonempty footer draw and reused for later labels. The old
1536-byte DTCM scratch and neighboring SDK data are not enlarged or overwritten.
The common painter limits writes to the actual backing image height. Tight text
surfaces can still crop at their own existing boundaries; no claim is made that
every compact field in the game was visually tested.

## Provenance

- ROM SHA-256: `{release['candidate_sha256']}`
- Profile: `{release['profile']}`
- Exact predecessor: `{release['predecessor']}`
- Predecessor SHA-256: `{release['predecessor_sha256']}`
- Immutable construction base: `{release['canonical_base']['path']}`
- Construction-base SHA-256: `{release['canonical_base']['sha256']}`
- Only `/__arm9__.bin` differs from the previous font test: seven source-locked
  instructions and a256-byte previously blank reserved helper slot. The improved
  1045-byte font table itself is identical. All other internal files/components,
  staged payload, DTCM initialization data, autoload extents and artwork are exact.
- Complete V4749 plus prior font test plus this registered offset layer:
  {release['complete_manifest_batches']} manifest entries and all{release['existing_accepted_layers']} accepted baked layers.
- Promoted main remains V4701. Canonical baseline and accepted-layer status unchanged.

## Verification

- Exact predecessor, candidate, frozen registry, profile, complete manifest,
  baseline and unchanged-file/code ownership checks pass. No original absolute
  word or ARM branch references point into the declared helper slot across
  {release['reference_units']} loaded ARM9/overlay units.
- Four-line native dialogue matches independent pixels withY+2 and unchanged
  16-pixel row spacing.128 guarded glyph tests cover both pixel formats and
  backing heights0,2,10,11,12,13,14,16, including all five descenders and symbols.
- Original footer initializer, view constructor, placement, complete label
  raster and copy rectangles execute. Independent full pixel planes include
  `g j p q y` and `[gyp]`; their last row fits. The native allocator return and
  final GPU copy are explicit offline test boundaries, separately covered by
  actual cold-boot gameplay.
- Existing integrated-release/font tests:29 passed.
- Actual cold boots:4001 New Game frames,17401 town/refit frames and32800 sailing
  frames ({total_frames} total). No loaded savestate or callback errors. The town
  run uses the existing isolated battery fixture; the others use ordinary inputs
  without injected gameplay state. These are targeted emulator checks, not a
  complete route or hardware verification.
- Eight complete actual button masks (Back,Select,Finish,Undo,Edit across sampled
  states) are exactly two pixels lower with unchangedX. Twelve sailing button
  masks pass, including the full `p` descender in `Inspect` at all three sampled
  frames. All font ink and blank cells match the actual screenshots.
- Viewed title, captain selection, opening dialogue, town/refit and sailing
  screens, button comparison and native descender sheet. No blocking clipping
  found in those samples. The later original Food-has-run-out popup is normal
  replay gameplay and is not counted as footer coverage.

## Preserved failed experiment

`font_v2_draw_down_two_20261027_test.nds` and profile
`font-v2-draw-down-two-20261027` are revoked: allocating during the static footer
constructor caused a white startup/entry into original exception handling before
the logo. Its ROM, config, producers, native passes and read-only CPU failure
snapshot remain preserved. Valid video callbacks alone did not prove startup.
The successor defers allocation until a nonempty footer label is drawn. Both
early startup and actual complete button masks now pass. The small disposable
startup probe is research-only and is not the handoff ROM.

Evidence: `work/font_offset_test_20261027_v2/`.
Please check other short button captions, brackets, nameplates and multiline
dialogue during play before accepting this experiment as the main build.
'''
    Path('docs/font_offset_test_20261027.md').write_text(note, encoding='utf-8')
    ROM.with_suffix('.README.md').write_text(note, encoding='utf-8')
    summary = ('\r\n\r\n## Font drawing Y+2 experimental successor, 2026-10-27\r\n\r\n'
        'Complete V4749/prior-font stack retained. Improved ASCII bytes unchanged; common painter drawsY+2 '
        'with actual-image row bounds. Footer views/backing/copy are14rows inside the original frame, '
        'using one lazy1792-byte native allocation instead of extending the DTCM scratch into SDK globals. '
        '128 native guarded cases,complete footer descenders,29 regressions and three actual cold boots '
        '(4001 New Game/17401 town/32800 sailing) pass. Eight actual button masks are exactly2pixels lower; '
        'twelve sailing masks include three complete Inspect p tails. Sheets viewed. '
        'Only owned ARM9 code changes; font,other files,artwork,pool and autoload extents preserved. '
        'Earlier eager-allocation offset candidate is revoked for white startup; all failures/producers retained. '
        'MainV4701 and canonical base unchanged; no editorial credit or user acceptance inferred. '
        'See [font offset test](font_offset_test_20261027.md).\r\n')
    for path in [Path('docs/known_issues.md'), Path('docs/todo.md')]:
        if 'Font drawing Y+2 experimental successor, 2026-10-27' not in path.read_text(encoding='utf-8'):
            with path.open('a', encoding='utf-8', newline='') as stream:
                stream.write(summary)
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    for path, reason in [
        (ROM, 'User-requested global font drawing-offset test; preserve during gameplay testing.'),
        (Path(release['predecessor']), 'Exact rollback and two-pixel alignment comparator for current font test.'),
        (Path('out/font_v2_draw_down_two_20261027_test.nds'), 'Revoked eager-allocation startup experiment; preserve failure evidence and reproducibility.')]:
        if not any(Path(p['path']).resolve() == path.resolve() for p in pins):
            pins.append(dict(path=path.resolve().as_posix(), reason=reason))
    pins_path.write_text(json.dumps(pins, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    handoff = dict(candidate=str(ROM.resolve()), candidate_sha256=release['candidate_sha256'],
        manifest=str(ROM.with_suffix('.manifest.json').resolve()), manifest_sha256=sha(ROM.with_suffix('.manifest.json').read_bytes()),
        profile=release['profile'], canonical_base=release['canonical_base'],
        changed_internal_files=['/__arm9__.bin'], previous_font_and_main_preserved=True,
        experimental_user_gameplay_acceptance_pending=True)
    (ROOT / 'handoff.json').write_text(json.dumps(handoff, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(handoff, indent=2))
