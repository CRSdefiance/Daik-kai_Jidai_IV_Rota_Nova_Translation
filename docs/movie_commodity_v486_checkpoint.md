# V486 town-canvas allocation and movie-preview interference

Production remains V484, SHA-256
`f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
No prototype is distributed or promoted. Original saves and synced sources remain
untouched. All22 graphics requirements and18 incomplete plaques are retained.

## Exact constructor isolation

Matched controls preserve the current M28 bytes, emulator/core/options and input
schedule. The old successful plane46 result is3047 exact name/shadow pixels.

| Control | Name plane46 at frame3700 |
| --- | --- |
| Commodity code bank only | Exact |
| Commodity data plus code bank, original drawing calls | Exact |
| Full commodity stage with town hooks restored | Exact |
| Full stage with market hooks restored | Not displayed |
| Full stage restoring only town constructor B59AC | Exact |
| Full stage restoring only town text painter B63D4 | Not displayed |

The causal call in these controls is **020B59AC**. Its lazy image helper allocates
15104 bytes, changes the shared header at022BD774 from72 to132 rows and replaces
its VRAM pixel offset with an offset into that allocation. Source width is228;
original pixel data lies at0601BFC8 and contains8208 bytes. Its palette remains at
02125A20. Both the additional allocation and shared-header mutation merit review.

The initial hooks-only controls lacked scattered executable helper code stored
in former string slots. Adding just the compact text helper was insufficient.
These invalid dependency splits are excluded from conclusions; the successful
selective call restorations above retain the complete translated data/helper set.

## Allocation sensitivity

A control preserves the original header and original constructor output but
makes one persistent allocation.16 bytes permits the3047-pixel result;4096 and
15104 bytes do not. This proves size-sensitive allocation interaction in the
fixture. Capacity exhaustion, fragmentation, address placement and the exact
movie allocation failure remain unproven; no memory-limit fix is inferred.

## Private-header prototypes

The private-header prototype copies all8208 original VRAM bytes, preserves the
original header/pixels/palette binding, and provides blank extra rows. Independent
native tests pass complete copy, canaries, saved registers/stack and single
allocation reuse. Actual exported state confirms shared height72 and private
height132. However, movie playback still does not display the name on V360 or
V484. Deferring allocation to the commodity text painter also does not restore
the result. These are unsuccessful movie repairs, not release changes.

The genuine Istanbul prototype matches61 reference captures; frame5900 differs
and remains to review. Do not claim complete town regression equality or hand off
that prototype. Existing V484 town/boot/patch checks retain their original scope.

## Evidence and next step

Verifier: `scripts/verify_movie_commodity_v486.py`.
Proof: `work/analysis/movie_commodity_v486/control_proof.json`.
Native private-header evidence: `private_native_proof.json` in the same folder.
Research manifests, assembly, terminal reports and read-only exports are retained.
Selected diagnostic screenshots are copied to E outside the guide archive.

Next, reduce or remove the town-only expanded bitmap's heap footprint, or establish
safe lifetime cleanup around movie loading, while preserving all124 English
commodity names and complete town labels. Verify actual movie and town rendering
before registering a playable candidate. Original ending caller/unlock behavior
and all20 progressive M28 name planes still require their own evidence.
At full-goal completion, revisit older record-based checks.
