# V614 evidence checkpoint: correct regional-plaque parent identified

The complete V613 candidate remains unchanged. Its Golden Route batch has passed
and is archived separately. The graphics goal remains active.

## Why the earlier Fleet Info test did not show the regional plaques

The original full-background helper containing the `chihofleetinfo.pxl` branch is
`0208C968`, called at `0208C93C`. Its actual Route Map family includes `9CRouteMap`
and the original market/town-selection map variants. The prior Info > Fleet Info
screen uses `COtherFleetView`. Its selected-fleet overview and subsequent Ship
Data view do not establish execution of this Route Map background branch.

V611's unsuccessful override was therefore tested in the wrong parent screen.
The existing negative screenshots remain valid; they did not verify those five
plaques. Do not repeat that override on the same Fleet Info schedule.

## New actual source-parent evidence

A normal20,400-frame cold boot uses unchanged V613 and an exact isolated copy of
the established early-menu battery save, SHA256
`f22ff2cd301c306813e9a1f5c0633d78c75d1d5a9acdf668bcd89a117d1ad087`.
No savestate, code change or live RAM fixture is used. After leaving Info > Fleet
Info and Ship Data, normal Common-wheel input opens Route Map. Selecting the
existing player's fleet shows the original full main-fleet data background.

Actual captured parent `02186658` has vtable `0214BECC`; its source RTTI identifies
`9CRouteMap`. Its fleet selection at+6C58 is1. The embedded real full256x192 view
at parent+6BC0 binds to resource owner `02313C68`. Executing original initializer
`0210E710..0210E734` verifies that owner's filename `_pxl/fleetinfo.pxl`. The
original getter `020D4170` on the captured actual view returns the complete exact
resident named PXL at `022E1794`, without a supplied cache/owner bridge.

The actual main-fleet Level region `[83,75,125,93]` matches all756 native5 RGB
pixels to the saved atlas, including full lettering, fine material, original
frame and surrounding edge. This is main-fleet coverage, not regional coverage.
Allocation addresses are captured evidence, not permanent runtime promises.

Executing the original own-company/main-fleet/financial getters over all64 actual
fleet records finds one own-company fleet: index1, the main fleet. Its financial
pointer is null. Source code gives the main-fleet case precedence and selects
the ordinary `fleetinfo` background. No existing own regional fleet is available
in this donor, and the regional PXL remains absent from captured RAM.

## Next test and retained scope

Use the original Shipyard > Dock regional-fleet creation workflow on an isolated
developed-port save, then select that actual fleet in Route Map. A suitable
Syracuse donor already exists. Authorized test cheats can support prerequisites
if needed, with their exact effects recorded separately from earned progression.
The existing correct map parent now supplies a concrete target for that test.

Verifier: `scripts/verify_regional_parent_v614.py`.
Proof: `work/analysis/regional_context_v614/parent_proof.json`.
Complete input schedule: adjacent `complete_inputs.json`.
Report: `E:/Rota Nova translations/Generated/work/emulation_v193/regional_context_v614_natural/capture_report.json`.

These are targeted emulator tests, not a complete route or physical-device test.
No V614 ROM is created. V613 remains experimental with its inherited regional
native gap; V610 verified pointers stay unchanged. All18 original plaque/hint
entries remain incomplete and all22 historical scopes remain exact. Other
miniature, village, comic/legacy/title/movie and gameplay gates stay open.
