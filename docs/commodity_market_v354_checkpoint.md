# Market name and native-format repair V354

Status: verified research checkpoint; no registered candidate or patch handoff.
The current registered combined ROM remains V342. Full graphics goal incomplete.

## Corrected behavior

Goods Info now displays the complete commodity name on one line within its
available112-pixel width. The Local caption uses its original72-pixel column and
wraps longer names at a word boundary, with a second row only when needed. All
names remain full logical English strings in the commodity table. No authored
hard line breaks or shortened names are introduced.

Both fields have independent source regions in one private184x36,4-bit image.
Its4096-byte native allocation is reused through a persistent pointer in the new
declared ITCM section. The original shared464x96 image header and all22272 pixel
bytes are untouched by the formatter. This avoids the date/numeric-cell ownership
problem found in V346 and the name/status-row overlap exposed by V352.

The compact ASCII callback now respects the bitmap origin. Its scoped font table
retains all original callbacks except that origin-aware single-character method.
The original font class and tracking are restored after each draw. The first
prototype V350 omitted this origin; V351/V352 shared name rows with the status
line. Those prototypes are incomplete and must not be handed off.

## Native printf defect

The older translated template atARM9+15A058 was `%s\n  %s %d%` with a dangling
percent. Executing the real ABFCC/CE898 formatter with identical arguments proved:

```
Old: Black Glacier Sword
       Crafts 100%不足中
New: Black Glacier Sword
       Crafts 100%
```

The old parser read beyond the format's NUL terminator into the adjacent Japanese
string. V354 relocates the corrected `%s\n  %s %d%%` template into owned autoload
data. Name/category/integer argument order is unchanged. This removes a false
Japanese shortage suffix when the actual status predicate is inactive.

The separate status labels不足中 and流行中 are localized as **Shortage** and
**Trending**. Trending expresses current popularity without inventing scarcity or
a particular price premium. Their original predicates and trade calculations are
unchanged. Both labels pass complete pixels through the original native status
painter; genuinely eligible gameplay states remain to be captured.

## Allocation and preservation

The new SDK autoload section occupies01FFC000–01FFC77C. Original sections and
overlay0 remain exact; overlay0 ends at01FFB860 including its BSS. Static scans
find no old aligned pointers or ARM branches into the new interval. Both actual
cold boots contain the exact new payload except its expected mutable private-image
pointer. This is a declared code/data allocation, not a zero-filled ROM cave.
Computed indirect users and hardware behavior are not exhaustively ruled out.

The main heap/arena bounds, original cache/bootstrap code, original bitmap header,
commodity metadata, route scripts and graphics files/palettes/dimensions are
unchanged. The visible Goods Info view uses available space up to the right screen
edge; the Local column retains its width. The ARM assembler is pinned in the
optional `arm-analysis` dependencies as keystone-engine0.9.2.

## Evidence

- Preparation:`scripts/prepare_commodity_private_market_v353.py` emits V354.
- Native verifier:`scripts/verify_commodity_private_market_v353.py`.
- Actual verifier:`scripts/verify_commodity_private_market_live_v354.py`.
- `work/analysis/commodity_private_market_v354/native_proof.json`:124 complete
  names on both surfaces, long/short height reset, stale-ink clearing, unchanged
  input/old-atlas bytes and one reused allocation; two original-painter status cases.
- `native_printf_proof.json`:exact native old/new printf output, same arguments.
- `allocation_census.json`:declared spans and static-reference limits.
- `live_proof.json`:two complete cold boots, exact name/category/percent masks,
  loaded code, earlier matched frames and final-screen preservation outside the
  two owned label areas. Trade values, icons, arrival grid and other labels match.

Actual frames show China and the supplied Black Glacier Sword label. Maria's
visibility byte and the three substituted long labels remain controlled research
inputs, not a legitimate unlock or normal rare-stock claim. These are targeted
emulator tests, not a route playthrough or hardware verification.

## Remaining work

Audit Cargo, Price Info and other commodity-name consumers; exercise real shortage/
trend states and repeated scene visits; resolve the older dense opening-wipe
intermediate frame; register/rebuild all inherited layers into the combined ROM
and reconstructable patch. All18 plaques and their variants remain incomplete.
The low-resolution Online images remain exempt. Revisit older record-based checks
at actual full goal completion.
