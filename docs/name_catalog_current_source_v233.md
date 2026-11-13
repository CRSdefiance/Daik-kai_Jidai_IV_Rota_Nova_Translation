# Complete prose allocation: current-source catalog research V233

V233 is ARM9 research, **not a ROM candidate**. V218 remains unchanged and the
graphics goal stays active/incomplete. The preceding turn completed19 fresh SC0
editorial/layout reviews; ten complete sentences exceeded their old slots.

## Allocation implementation

The original exact-string message catalog is now rebased onto the exact V218 ARM9
source and expanded from25 to **35 source records**, with **51 unique keys**.
The ten new source/context-reviewed sentences keep their full wording and the
existing speaker selectors/name macros. Both whole and speaker-stripped forms
are registered where appropriate; ordinary protagonist records retain only their
whole-string form. The lookup includes the terminating NUL and remains scoped to
the original three story-copy callers. No script command or record boundary moves.

The complete route audit scans **128,492 NUL segments** across SC0–SC3. All35 selected
owners are covered, and no extra/unreviewed owner matches any key. Conflicting
same-string translations fail preparation. Current route resources remain exactly
V190-identical; they are lookup evidence, not translation input.

The current-source adapter keeps the historical name-field transform's strict
V190/clean guard. It reuses only its five proven interval changes after checking
the same old bytes, capacities, pointers and sole static aliases in separately
pinned V218. The original historical module is unchanged; no general source-hash
bypass is introduced.

All **52,576 inherited pool bytes** remain exact, including prior graphics/text/
helpers. The new total payload is **57,408 bytes**. It remains within explicit
pool/staging bounds, is cache-aligned, and preserves both native/IWRAM sections,
the original macro expander and unrelated primary-section bytes. Only scoped
lookup calls, startup/cache/arena metadata, the five selected name fields and the
new owned catalog payload differ in the analysis binary.

## Native verification

- **816 lookup cases:**51 keys, four input alignments, three scoped callers and a
  foreign caller. Arguments, source bytes, stack and registers survive; the foreign
  caller retains its original input.
- **153 exact-match negative cases:** extended-before-NUL, truncated and changed-
  first-byte inputs are not retargeted. No altered input inherits an exact-key match.
- **153 complete native macro-copy cases:**51 keys through all three callers.
  Every output byte, initial/final byte, embedded control, NUL and buffer guard is
  exact. Engine-safe literal glyphs and FI/FA/FU expansions survive. There are no name-
  getter or macro-result bridges.
- Actual startup/late-copy/cache and ARM7 loading preserve the entire payload,
  original ARM7 source/loaded sections, stack and startup registers.
- All route resources, inherited pool bytes and the original expander remain intact.
  Ruff passes for both new scripts.

## Fixture and release limits

Macro-copy execution uses the explicitly identified real player/heap from the
earlier V201 **named research cold boot**. Its capture, ROM and read-only4MiB RAM
hashes are checked. Only static code/data differences and the new owned pool are
applied inside the CPU fixture. This is not a claim that a changed V218 ROM was
cold-booted or that the original deep scenes/portraits/GPU were visited.

The five named fields and these catalog sentences do not constitute the whole
name migration. Other affected records still need source/editorial/layout review,
new fixed batches, complete default macro-length handling and registered integration.
The nine fixed-slot lines from V232 also remain outside the playable ROM. No partial
name-field binary is registered, handed off, promoted or saved as a ROM.

Four Online bodies, ambiguous source marks, embedded/environmental/native display
work and the final combined ROM/patch/gameplay remain within the full objective.
At eventual completion, revisit older record-based checks as requested.

## Evidence

- `scripts/prepare_name_catalog_v233.py` and `verify_name_catalog_v233.py`.
- `work/analysis/name_catalog_v233/catalog_plan.json` and `catalog_research_arm9.bin`.
- `route_scope.json`: complete source-owner audit.
- `native_proof.json`: startup,816 lookup,153 negative and153 native-copy cases.
- V232 manuscript, full layouts and source locks remain the editorial input;
  the older25-record V201 plan is independently hash-pinned and retained.

Source V218 ARM9 SHA-256:
`a4af5e53f570bdfe76c895fb8704ba0db461851b4935c591daa2ea23647652c1`.
The registered ROM stays SHA-256
`be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.
