# Porto Estado window resources: actual native registration and loading

V239 is research verification; V218 remains the registered candidate. The previous
goal turn made progress by verifying title05's physical Extras display. This turn
replaces the older supplied-owner window loading check with actual native owners.

## Verified scope

The unchanged initializer constructs five window resources. Their owner addresses
are obtained from initialized native objects and their actual filename fields,
rather than pairing nearby filename literals with assumed pointers.

| Path | Actual native owner | Source content reviewed |
|---|---|---|
| `/_pxl/winframe00.pxl` | `02313344` | Complete English Porto Estado title, original gold logo, small subtitle and copyright. |
| `/_pxl/winframe01.pxl` | `02313330` | Original gold PORTO ESTADO decorative panel; retain. |
| `/_pxl/winframe02.pxl` | `0231331C` | Original dark textured backing; retain. |
| `/_pxl/winframe03.pxl` | `02313308` | Original paper and border; retain. |
| `/_pxl/winframe05.pxl` | `023132F4` | Original Latin ROTA NOVA banner; retain. |

All five actual registered owners execute the original resource cache allocation,
whole-image view constructor, virtual view copy and complete resource resolution.
All 84,648 source bytes, including headers, palettes and indices, match V218.
Both view buffers retain their guards, native routines return with saved registers
and stack intact, and every file handle closes. Only SDK filesystem operations are
bridged to the exact ROM. No header, owner, cache result or file data is substituted.

All five full source images were visually reviewed at native resolution. Existing
English and Latin lettering is preserved; backing textures and borders contain no
additional readable Japanese instruction. These are scoped content decisions.

The generalized research function also reruns its original seven-title default
successfully. Both affected scripts pass Ruff. No production renderer, ROM builder,
release profile, ROM, patch or translation asset was changed.

## What this does not prove

The source-view calls are explicit research invocations. They do not prove that an
actual scene requests the same crops, nor prove physical window composition.
`/_pxl/logo.pxl` and `/_pxl/startmenu0.pxl` have no literal filename occurrence in
the inspected main ARM9 bytes; generated names and indirect consumers remain
possible. This is not evidence that either asset is globally unused.

An adjacent literal reference at `020FA8B0` resolves to `/_pxl/wl_icons.pxl`, not
winframe00. It must not be presented as the Porto Estado title's scene consumer.
The earlier six supplied crop contracts remain historical research, not actual
scene bounds. Embedded WINFRAME relationships, physical crops, gameplay, the
standalone logo and other full-goal requirements remain open.

## Evidence

- `scripts/verify_window_resources_v239.py`.
- `work/analysis/window_resources_v239/native_proof.json`.
- `work/analysis/window_resources_v239/full_source_sheet.png` and five full previews.
- Generalized helper: `scripts/verify_title_display_v229.py`; its default title
  scope is unchanged and verified.

The full graphics goal stays active. Final completion still requires the unresolved
Online transcripts, native/embedded/environmental displays, naming consistency,
complete registered integration and remaining visual/gameplay checks. Revisit the
older record-based checks at eventual completion as requested.
