# Native FLS timeline and geometry V312

Research on unchanged V309, SHA256
`b099a1016d08870adbdbff8693be9b5fba2f0fa611c82358bafcd507199d5289`.
V311 verified all520 compressed palette/pixel decoding cases. This checkpoint
executes original timeline and CPU geometry code against current and clean
Japanese FLS files. No ROM, artwork or patch changes.

## Native execution scope

Each isolated stream uses the verified V310 constructor/parser, current captured
runtime globals and SDK filesystem bridges. Original020FD4F8 executes the complete
timeline to its native end. Original02100390 resolves animation-record inputs
to texture indices; these inputs cannot be assumed to equal texture indices.
The complete draw-state bytes are retained, including matrices and colour/alpha
controls. Global camera, canvas, colour, alpha and depth controls also participate
in distinguishing states.

Native020FEB28 computes four affine corners from the original previous frame
buffer, as the native draw loop does. Execution stops at020FEFCC, before
clipping/GPU processing. The native software matrix operations execute; no
geometry formula is substituted. Early inactive/alpha returns are handled at
the explicit caller return sentinel. Stack bytes and CPU context are restored
after the bounded geometry inspection, preserving subsequent timeline execution.

All15 actual FLS timelines finish. Current files and clean Japanese files produce
identical native state and prepared geometry, using the unchanged original engine
code. The proof contains per-file counts and complete states; the audit records
the final totals. Each version executes45,058 native update calls. This includes
the longer M28 credits and M29–M32 ending timelines, without gameplay unlocks.

## Subtitle and genre rectangles

All five opening subtitle quads retain their original width and32-row height:

| Asset | Width | First prepared upper-left, pixels | Instances in recorded states |
|---|---:|---|---:|
| M20/27 |168|(38.5999,139.75)|12|
| M22/1 |176|(47.3999,149.3999)|60|
| M22/2 |176|(40.3999,148.8499)|20|
| M24/3 |216|(13.0498,146.3499)|30|
| M24/4 |216|(24.0498,146.3999)|45|

These are native12-bit fractional corner coordinates, not an assumed GPU
rounding rule. Earlier V303 actual framebuffer checks separately verify complete
English ink and outlines at the observed screen positions. The geometry confirms
the intended168/176/216 rectangles used by the subtitle authoring repair.

The genre card's quad is exactly(0,0)–(256,192), consistent with V305's correction
to author the English label inside192 native rows rather than256 padded rows.
No previously translated letters, border, palette, dimensions or original motion
is changed by this checkpoint.

## Root file remains a scoped unknown

The raw root `/m02_03.fls` timeline reaches end after876 native update calls.
It activates no draw slot, including the reserved slot0, in this controlled
original update path; no quad is requested. This adds a specific native result
to the existing parser/raw-payload evidence. It does not establish a genuine
gameplay trigger, prove global disuse or rule out another raw-resource reader.
The original coastal artwork remains byte-exact and its broader use remains open.

## Limits and retained failures

The original renderer reads the previous pose buffer. Recording only the newest
writer buffer would misrepresent the draw input, so the geometry test follows
the native buffer selector. The initial geometry attempt omitted the early-return
sentinel and ran beyond a guarded return; that failure receives no display credit.

An initial local-slot-only proof is retained separately. The final proof also
includes global camera/colour/alpha/canvas/depth controls, so a transition cannot
be skipped just because its local slots are unchanged. Source/native shader
operations at and after clipping, texture binding/upload, palette banks, alpha
blending and final GPU output are not certified here. These are controlled native
state tests, not actual ending playback, a complete route or hardware verification.

## Current project status

Both authoritative graphics audits and progress documents record the results.
V309 remains the registered combined candidate with its unchanged exact patch.
All18 plaque/hint entries and Armor/Weapon variants remain incomplete. All11
legacy layout gates, hidden Gallery/actual ending contexts, occupied equipment
and alternate condition checks remain open. Low resolution Online screenshot
translation remains exempt by the user's instruction.

The full graphics goal remains incomplete. Continue original clipping/GPU
composition and genuine raw/virtual resource contexts, and revisit older
record-based checks at actual goal completion.

Evidence: `work/analysis/fls_frames_v312/all_files_proof.json`,
`local_slot_state_only_proof.json`, `all_run.log` and the two scripts
`research_fls_frames_v312.py --all` / `record_fls_frames_v312.py`.
Focused Ruff passes.
