# V688: bounded control-owner aliases and exact resource boundaries

## Result

This checkpoint investigates an untested address path for Confirm and the Frame
atlas: owner pointers assembled by arithmetic or read through a constant pointer
table, rather than loaded directly as a literal. It identifies no new gameplay
parent. All six control-context requirements remain open.

The bounded ARM analyzer covers 380736 aligned words in the original ROM and
443599 current views, including main sections, overlay0 and the current verified
startup-copy live POOL view. Staged storage and its copied executable addresses
are treated separately. It models literal/read-only mapped word loads and
unshifted scalar arithmetic. Values never cross a call, branch, conditional,
memory store or unmodelled instruction. Its computed-alias and indirect-table
positive controls pass; conditional/call/store controls clear unknown values.
This is lead generation, including possible inline-data disassembly, not proof
that every decoded word is executable or every dynamic path has been covered.

Both versions resolve only the 50 already known owner-load sites: two Confirm
initializer loads and 48 Frame sites. All 100 original/current literal-load
instructions execute in isolation with the expected target, unchanged other
registers, main RAM, stack and link register. No additional supported constant
alias or pointer-table lead remains. This does not exclude Thumb, variable
arithmetic, cross-call/branch dataflow, runtime pointer tables or another reader.

## Correct boundary, and a rejected false lead

The first draft conservatively included 24 bytes around each owner. That
incorrectly swept in the first word of the next object. It produced four extra
Confirm-window candidates and 88 extra Frame-window candidates per version.
Those results and that draft remain retained rather than silently discarded.

The complete original resource initializer at 0210E190 executes 2864 distinct
instructions in each ROM and returns with its saved registers and stack intact.
No calls or loaders are bridged. Exact target writes are at offsets
4,8,0,0,12,16. Each five-word object contains its vtable, two self-linked list
fields, filename pointer and FFFFFFFF resource index. A separate guarded native
constructor check executes all six instructions without touching its neighbors.

| Target | Owner | Next separate owner | Next resource |
|---|---|---|---|
| Confirm | 023139C0 | 023139D4 | `_pxl/plate4016.pxl` |
| Frame | 02313F60 | 02313F74 | `_pxl/__marker.pxl` |

The adjacent 40×16 plaque resource is not a Confirm field or a demonstrated
Confirm consumer. The Marker resource likewise must not be counted as a Frame
field. These bounds apply to the source-bound class checked here, not all native
objects. An initial independent verifier also lacked Capstone's `fp` register
alias; its diagnostic is retained and the mapping corrected without game changes.

## Consequence

Do not repeat the same literal/constant-owner search or promote the adjacent
plaque/marker paths as missing-control coverage. A useful next parent lead needs
a distinct gameplay state, actual dynamic pointer/reader evidence or a different
rendering path. Existing controlled native graphic tests remain valid; this
checkpoint supplies no new screenshot, rendering, wireless connection or
ordinary control display credit. No global unused-art claim is made.

All 18 plaque/hint objects remain incomplete and all 22 historical requirement
objects remain exact. Current V685 ROM, manifest, patch, registry, canonical
baseline and release pointers are unchanged. Previous goal turn was progress
(V686/V687); this evidence changes the next investigation and is progress.

## Evidence

- `scripts/trace_control_aliases_v688.py`.
- `scripts/verify_control_owners_v688.py`.
- `scripts/verify_control_aliases_v688.py`.
- `work/analysis/control_aliases_v688`: final proof, all candidate chains,
  native initializer writes, controls and retained rejected assumptions.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V688 Control owner aliases`.
- No new ROM, guide promotion, commit or push. Full graphics goal remains active.
