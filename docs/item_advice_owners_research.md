# Item Advice menus and actual crew owners

Historical exact-target checkpoint. The newer [ship/parent/generated-map
checkpoint](item_ship_parent_generated_research.md) records later work; these
original target hashes and case results remain unchanged.

The full goal remains active. V158 remains the latest combined candidate.
The ARM9 research target is unchanged:
`edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663`.
These checks extend [item startup/provider evidence](item_cache_promotional_research.md).

## Advice command consumers

Gallery native 0204553C–020455A8 copies the six-word descriptor at 021156A8
to frame+4048. Regular item native 0204D104–0204D180 copies 0211627C to
frame+4058 and handles optional Select. Both execute actual 02023C60 against
option bit4, choosing the translated Advice pointer in slot2 only when enabled.
Native descriptor writes and guard bytes pass. These constructor segments
pause with a 40-byte frame; CPU state is restored explicitly before the separate
footer call. This does not prove full widget construction or controller input.

The actual generated descriptor reaches CA890→CA780 and native state transfer,
length measurement, font initialization, D5404/D16B4 rendering and cleanup.
12 cases cover both option states, both regular Select states and both pixel
formats. Complete Prev/Next/Advice/Back/Select text, pointer transfer, every
glyph, independent pixels, disabled slots, full widths, source ranges and
nonoverlapping destination positions pass. Six complete footer configurations
were visually reviewed using native text pixels and placement metadata.
Surface-view construction/origin and physical button/parent composition remain
contracts. A deliberately missing initial Advice character is rejected.

The first exploratory call omitted the copied pool because the existing harness
loaded it only for detail screens. That made Advice appear blank while the
resident labels rendered. The harness now initializes the complete pool for
item menus too. ROM code/text was unchanged; the completed proof requires
Advice in every enabled state. No credit is taken for the failed initial call.

ITEM_ADVICE now has a local formatting gate with exact-target proof. There are
34 locally verified visible label records; Use remains uncredited because its
mapped branch skips the heading draw.

## Actual crew-owner paths

The main item caller now executes native ownership classification 02049DE8,
equipment search 0207F044, crew table/current captain 020CB184/0207F244,
eligibility 02049A18 and the actual name virtual. The resulting kind2/owner index
is observed at 0204D700 and checked before rendering. Crew/name/ownership,
captain-index and eligibility callbacks are absent from these cases.

Ordinary crew objects use actual 0207EB3C constructors and 02148414 vtables.
Name selection runs 0207EB0C→0207EE08→0207F1F4→020CDAB4, resolving the
actual 207-entry source table, including relocated names. The current captain
uses the distinct interface at crew root+19E4, its 02148E94 vtable and native
0201371C name virtual. Captain interface initialization and mutable storage
remain explicit contracts. Equipment bytes/current-captain state are controlled
runtime inputs; these tests do not establish which characters are recruitable.

456 fresh raster cases cover:

- Every ordinary crew index 0–206 through the native weapon search in both
  pixel formats: 414 cases.
- Native armor search at first/middle/last indices 0/103/206 in both formats:
  six cases.
- Native mutable-captain name branch with every editor length 1–18 in both
  formats: 36 cases.

Actual item metadata, unsigned fields, original COMMON selection/copy, private
paragraph helpers, complete owner labels/names and numeric values execute.
Independent glyph/pixel vectors, every leading/interior/final character, full
view bounds and nonoverlap pass. The longest ordinary label is the 18-character
`Mysterious Old Man` at index170; it fits the x88 name column. Eight whole panels,
including names with semantic follow-up already recorded and both mutable-name
extremes, were reviewed. Name fidelity is a separate source-context audit.

The only getter callback left in these ownership raster cases is artwork, which
is explicitly unrendered. Runtime table initialization, warm COMMON cache,
local bitmap origin/font setup and final physical composition remain contracts.
Role-dependent equipment eligibility, ship owners, full random/download states,
counter allocation and parent crops/artwork remain pending.

## Verification and next integration gates

81 focused tests pass, including seven new menu and five new owner regressions.
Changed scripts pass Ruff. The preceding 52 promotional-target rasters, 198
metadata initializers and cache/startup proof retain their exact ARM9 target;
the new cases add consumers without changing ROM bytes. They are not a complete
physical gameplay verdict.

Evidence:

- `work/analysis/item_advice_menus_native_proof.json`
- `work/analysis/item_crew_owners_native_proof.json`
- `work/qa/item_advice_menus_native/native_sheet.png`
- `work/qa/item_crew_owners_native/native_sheet.png`
- `translations/item_interface_manuscript_v1.json`

Finish remaining item/provider/parent gates, refresh inherited release paths,
register/build the full candidate and verify saved manifest/lineage/patch before
handoff. Physical cold boot and explicit candidate acceptance are needed for
canonical promotion. Registry, canonical baseline and V158 remain unchanged.
No commit or push is claimed; revisit older record-based checks after completing
the full goal.
