# Remaining fleet-name getter text

## Current V148 research and V149 integration

Integrated in experimental V149. Saved ARM9 matches the research exactly;
all other V148 components and 3,668 COMMON selections are unchanged. Manifest,
canonical verifier and exact clean-ROM patch reconstruction pass. See
`all_routes_unified_v149_checkpoint.md`. Earlier build-pending statements below
describe the preparation chronology; gameplay and broader consumers remain open.

Full fleet-label research is repeated after the persistent-name repair. Both
mapped displays now execute the actual 3697C captain selector, native root and
current-character accessors, ordinary given-name dispatch or stored player-name
getter, formatter and glyph bodies. All 456 connected native rasters match
independently decoded pixels with complete ordered glyphs and bounded ink:
414 ordinary-name cases, forty player-field cases across four current-character
routes, and two no-captain sentinel cases. All-byte ARM9/overlay storage scanning
still finds only the original fallback pointer in the reused allocations.

The longest reviewed ordinary name is seventeen bytes. Complete Pirate-prefix
output occupies at most 144 pixels, ending at x186 in the fixed 192-pixel view.
The special player interface uses native vtable 148E94+20 -> 1371C, returning
owner+20. Valid sixteen-byte saved fields occupy at most 138 pixels, ending at
x180. This is a tested initialized-field bound; live captain setters/eligibility
and malformed saved fields are not proved. Captain index 208 is the native null
sentinel; 207 is not counted as an initialized ordinary actor.

Ten native ink panels are inspected: complete source-faithful labels, maximum
ASCII/CP932 fields and leading/final glyphs survive without clipping. Ordinary
actors execute their constructor; the player interface/vtable and saved field
remain initialization fixtures. Outer composition, bitmap clear/default vtable,
font loading and other virtual consumers remain open. Native glyph tests cannot
prove physical gameplay.

Durable `translations/fleet_name_*release*` and native-review inputs reproduce
the research bytes. Twenty-eight focused tests and lint pass. Registered V149
preserves all 435 V148 batches and postprocessing stages; combined rebuild and
saved-ROM/patch checks are underway. Canonical acceptance is not claimed.

Evidence: `work/analysis/fleet_names_v148_native_proof.json`,
`fleet_names_v148_research_arm9.bin`, and
`work/qa/fleet_names_v148_native/native_sheet.png`.

Earlier V147 research/pending statements below are historical.

## Connected native bitmap and complete ink

Shared parent setup 87644 calls bitmap D3AFC with the descriptor at dialog+1B74:
mode 4, halfword pitch 48, width 192, height 72, pixel storage at dialog+74.
Research executes the actual setup prefix 87680–876EC and verifies resulting
dimensions. Default bitmap vtable and successful outer parent initialization
remain fixtures; no allocation is invented or appended to ARM9.

Fourteen connected cases now execute each actual fleet caller, real text context
D5160, constructor-owned virtual getter, native formatting, D5404 and actual
ASCII/CP932 glyph-copy/painting bodies in one machine. All complete labels and
fixture names remain in the first row, within 192 pixels. Every full bitmap
matches independent font decoding; preceding guards and adjacent native resource
descriptor remain exact. Kanji cells use the original font asset. Bitmap clear
and initialized 6×12 font metrics remain explicit runtime contracts.

All fourteen native ink panels are visually reviewed: complete words, ASCII/
Japanese fixture names and first/final characters survive without clipping.
Physical palette, parent composition/input, actual captain-name bounds and other
virtual display consumers remain open; formatting/integration is not approved yet.

The style-one CP932 cases exposed an independent-pixel-model assumption: the
model always shaded with 14. Original D1964 shades style 15 with 14, styles 7–14
with zero, and remaining styles with 15. Nonzero font flags disable shadow.
The model now follows this source rule. Native shadow mutation rejects and all
inherited tooltip/Deck pixel regressions pass. Twenty-two focused tests and Ruff
pass, including native geometry and pixel corruption cases.

Proof: `work/analysis/fleet_name_connected_pixels_proof.json`; reviewed sheet:
`work/qa/fleet_name_native/native_sheet.png`. The preparation tool regenerates
the proof/sheet; preserve or repeat visual-review metadata if it is rerun.
V147 remains unchanged.

## Actual fleet display preparation

Two actual fleet consumers are now mapped: fixed caller 37568 and centered
caller 37CB8. Both load the dialog fleet index at +1B88, call real CB1A8,
and select fleet root+4+index*0x84. The actual CBA3C constructor prefix writes
the 134EE0 name vtable; native +8 dispatch reaches trampoline 36A60 and the
complete 36A6C getter. Fourteen full-English cases execute these paths through
native literal/ring allocation/formatter and stop at actual D5404 draw entry.

The fixed caller passes x42/y0. The centered caller executes actual CED28 byte
length and computes x=(192-6*CP932_byte_length)/2, y0. ASCII/CP932 names remain
complete; this byte-count rule must be retained when reviewing dynamic name
width. Context style at SP+30 is set to one by the actual caller. No glyph
rendering or parent width follows merely from this preparation proof.

Research uses fleet index zero, no affiliation and captain/name resolution
fixtures. Constructor runs only the prefix that establishes vtable ownership;
fixed-caller bitmap clear is contracted and text-context initialization is
skipped. The first C1314 candidate instead indexed the distinct CB178 array
with 0x6C stride; it is not used as fleet-layout evidence. Actual fleet indexing
uses 0x84, also consistent with 36B5C's native reciprocal division.

Tool: `scripts/probe_fleet_name_display_callers.py` (14 cases and Ruff pass).
Proof: `work/analysis/fleet_name_display_callers_proof.json`, including source
locks for both callers, constructor, root getter, trampoline, vtable and length.
Next: bitmap resource geometry/context/glyph raster, valid captain-name bounds,
other consumers and strict integration. V147 remains unchanged.

## Complete English relocation research

Research now fits both full drafts without ARM9 growth or shortening. The exact
reviewed V147 companion release owns 136 bytes and uses 108; its 28-byte spare
tail 138878–138894 holds complete `Unidentified fleet`. The old 16-byte fallback
slot 135260–135270 holds complete `Pirate %s`. Literals 36B54/36B58 are redirected;
all earlier fleet/companion/Options/name-format owners and every other ARM9 byte
remain exact. All-byte ARM9/overlay scanning finds only the mapped fallback start
reference in the reused ranges, with no interior or overlay address candidates.

All 193 actual English getter/formatter/return cases pass: one fallback plus six
ASCII/CP932 names at all 32 native ring indices, including wraparound. Complete
names/NULs, stack and ring neighbors/guards survive. Actual inherited companion
branch, ten Options formatter cases, twenty responses and six parenthesized-name
cases also pass after spare-tail reuse. Ruff passes. Native branch/name fixtures
remain explicit; no full gameplay or name-bound claim follows from these cases.

Native ownership lead: getter 36A6C is reached through trampoline 36A60, stored
at vtable 134EE0+8. Vtable address references occur at CBA78 and CC53C. Direct ARM
B/BL scanning finds no direct getter/trampoline calls; actual virtual consumers,
constructor ownership and downstream display still need tracing.

Tool: `scripts/prepare_fleet_name_relocation.py`.
Outputs: `work/analysis/fleet_name_relocated_arm9.bin` and
`fleet_name_relocation_proof.json`. Formatting approval, dynamic captain-name
bounds, visible geometry/raster and strict integration remain pending. V147 is
unchanged; the earlier storage-open notes below describe the source research.

Source-reviewed drafts from clean Japanese are **Pirate %s** for `海賊%s`
and **Unidentified fleet** for `所属不明艦隊`. They preserve the captain-name
substitution and uncertainty about affiliation. Natural-dialogue-v2 prose gates
pass; formatting remains open. No ROM/profile changes are made by this research.

## Native context and source evidence

Getter 36A6C first resolves affiliation via 352F4. An affiliation path uses the
ordinary name format, while the no-affiliation path calls captain getter 3697C.
No captain at 36B0C returns the literal at 36B54, targeting Japanese 135260.
A captain name from its virtual +20 getter flows into the format at 36B58,
targeting Japanese 135258, then ABFCC at 36B3C.

Seven actual source cases pass: one no-captain literal return and six full pirate
format preparations for empty, A, Even, Fleet, 海 and Indigo海 names. Native
returns restore the stack. The upstream affiliation/captain getters and name
strings are fixtures; complete enumeration/gameplay does not execute.

ABFCC is a ring-buffer formatter, not a direct destination sprintf. AC000 reads
the index at owner+8 and returns owner+12+index*128; it advances/wraps the index
across 32 slots. Research initially mistook the owner pointer for a destination;
the observed invalid write led to inspection and correction. Final execution
uses the actual allocator and formatter and preserves full output/NUL plus all
observed ring storage and external guards. Valid captain-name limits, ring
lifetime and downstream display consumers still need tracing.

## Storage and inherited translation

Five original owners occupy 13523C–135270 (52 bytes): numbered-fleet format,
ordinary-fleet format, concatenation format, pirate format, unidentified label.
The last two own 24 bytes; complete aligned English requires 32 bytes. Do not
shorten or truncate to force insertion. Relocation remains open.

Every-byte ARM9/overlay scanning finds three start references: 36B50→135250,
36B58→135258 and 36B54→135260. The ordinary format literal 36B4C is already
redirected to inherited English outside this original pool; its actual target
and complete wording are recorded in the proof. Other consumers of the old
ordinary-format bytes and the numbered-fleet owner remain unresolved. Absence of
direct hits does not establish unused storage.

The getter instructions and other literals match clean Japanese; the inherited
ordinary-format pointer differs intentionally and is preserved. Full current
getter bytes are hash-locked in the proof.

Tool: `scripts/probe_fleet_name_sources.py` (seven native cases and Ruff pass).
Draft: `translations/fleet_name_manuscript_v1.json`.
Proof: `work/analysis/fleet_name_source_proof.json`, pinned to V147 ARM9 SHA-256
`33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75`.

Next: trace complete source storage ownership and caller/name bounds, preserve
the inherited ordinary-format relocation, prove full English formatting and
rendering, then prepare strict integration and saved ROM/patch checks.
