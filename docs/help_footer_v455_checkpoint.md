# V455 complete English Help footer

Experimental; full graphics goal active. All22 historical requirements and all18
incomplete plaque entries remain in the audit.

## Translation and high-level formatting repair

Help's active Japanese labels 前, 次 and 最初 now read Prev, Next and First.
Prev/Next navigate viewed-article history. First returns to the initial Help
article; Index opens the contents. Actual Y input returns Shared Commands in the
tested initial context, preserving the distinction between First and Index.

Simply substituting English made the six-button row overflow. The correction
uses the original font's five-pixel tracking and two-pixel gaps for Help, with
complete wording. No glyph shapes, palettes, button artwork or border code change.
The shared renderer receives a copied descriptor. Scope recognizes Help's unique
Index/First pointers and the six exact native measurement call returns; layouts
without either unique pointer retain original metrics and already fit.

The footer bitmap is four-bit indexed. Each caption's stored width is rounded
up to an even pixel count so every following buffer starts on a whole byte.
This prevents the native copy from rounding an odd source coordinate and shifting
or clipping text. Padding belongs to the buffer formatter, not authored prose.

All code fits existing verified padding at01FFC980 (120 bytes) and01FFCB70
(104 bytes). The4096-byte ITCM section, other sections, main pool, arena bounds
and ROM component size do not grow. The original First slot fits the English
word; Prev/Next reuse immutable existing English strings.

## Failed experiments retained

- V451 misses the runtime copied descriptor and clips Prev in the six-button state.
- V453 recognizes the copy but allows odd source offsets, shifting Index by a
  pixel in the actual four-bit transfer. Pixel verification rejected it.

Both profiles are revoked, neither is published or used as a parent, and their
implementations remain available for historical reproduction. V455 uses V449's
complete stack as its parent.

## Evidence

- All256 original/copied enabled/disabled footer contracts pass native full glyph,
  pixel, placement, stack and register checks in4-bit/16-bit formats.
- All18 caller/descriptor scope cases pass;10 sailing/Golden Route footer cases
  retain exact original pixels/metadata;36 neighboring rumor/clue/equipment/Guild
  wrapper cases remain byte exact.
- Actual all-six state contains every first, interior and final letter and blank
  cell. Every source offset and stored width is even. All button bounds fit256 pixels.
- Actual Prev/Next return a whole page exactly; First, Index and Quit reach their
  original destinations. Quit returns to the city radial menu with Back/Select intact.
- Equivalent-action regression has41 whole frames exact and15 frames differing
  only in the footer: all56 non-footer regions match V449. The old exploratory
  touch at164,183 now hits a different repositioned button; its intended First
  action is replayed with Y. This input difference is explicit and verified.
- All470 inherited batches/stages and every non-ARM9 internal component, including
  all artwork, HELP, COMMON and routes, are byte exact. Clean patch reconstruction passes.

Tests are targeted DeSmuME emulator evidence, not hardware or full-route testing.
Ten older Help marker matches and the broader legacy/environment/Gallery/ending,
equipment and plaque requirements remain open. Revisit older record-based checks
at true full-goal completion.

## Handoff

ROM: `all_routes_combined_v455_candidate.nds`

SHA-256: `974dff8310bfdd3892e17decf732ff4d329c1f529b4c25d18aecafcdd84ed5fe`

Patch SHA-256: `e78b2a4d312656d07dd4dc1b1a42587eb10f3b99b31225ca710cd3eae4f3fb7d`

Profile: `all-routes-unified-v455`, all470 inherited batches and every V449 stage,
plus `translations/help_footer_release_v3.json`. Only `/__arm9__.bin` differs
from V449. Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
No canonical promotion is made.

Verifiers: `verify_help_footer_v454.py`, `verify_help_footer_release_v455.py`,
36 native neighboring wrapper comparisons, and targeted Ruff.
Proof: `work/analysis/help_footer_release_v455/release_proof.json`.
Actual report: `work/emulation_v193/help_footer_v455/capture_report.json`.
Regression report: `work/emulation_v193/help_footer_regression_v455/capture_report.json`.

ROM, exact patch, manifest and verified all-six screenshot are on
`E:\Rota Nova translations`. User cold-boot testing should cover title/New Game,
town, Help history with all six buttons visible, First/Index/Quit, and existing
sailing/item footers. All plaques stay under audit.
