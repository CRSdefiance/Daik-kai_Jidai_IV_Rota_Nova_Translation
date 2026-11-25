# V723: fleet-row graphics in ordinary Port → Dock → Swap Ships

V722 resolved the Treasure Name panel. This turn identifies the original
`/Iseki/dock.pxl` consumer and verifies the fleet labels in a current normal menu.
No production graphic,code,ROM,patch or release profile changes.

## Actual context

One13100-frame V712 cold boot uses a byte-exact copy of the Syracuse save and
ordinary controls only. Info → Dock Ships and Fleet Info are retained navigation
detours; neither receives credit as this asset's consumer. The correct route is
**Port → Dock → Swap Ships**. It constructs original `15CShipChangeView` at02189280.
Its view at parent+6838 selects original owner022A44B8 and the complete256x192
source at0,0 with palette bank0. Six complete native cache getters resolve every
byte of the actual resident file,with normal saved-register/stack returns and no
I/O/image bridge.

The source labels remain faithful:旗艦 → Flagship and2番艦–5番艦 → Ship2–Ship5,
with normal English spacing. All five complete original-font masks match the
current stored image. Dimensions,palette and earlier source work are retained.

## Display and occupied-row distinction

Six holds verify every glyph and blank cell of the four visible empty-slot
labels:24 complete font masks. All19,200 pixels in their complete50x16 source
rectangles match the screenshots at native color precision. Leading and final
letters remain intact. Ordinary Down inputs do not select these empty slots in
this one-ship active fleet; no selection-change coverage is claimed.

The first slot is occupied by Vestaros. Its ordinary ship name/icon/cell covers
the baked Flagship placeholder. Flagship is therefore **not claimed visible in
the final screenshots**. No attempt is made to erase the ship overlay or invent
an empty-flagship gameplay state to make that claim.

The actual parent's original base-draw fragment020A6CDC–020A6D34 is executed on
captured RAM with the captured source view and a supplied renderer interface
from the same modal scene. Both software planes start poisoned. It writes every
one of49,152 lower-plane words,which match the complete source-index/raw-palette
model exactly. No output is read before it is written; the other plane remains
poisoned. All executed instruction bytes match the registered ROM. All five
labels,including Flagship,are present in this complete native underlay.

This is an isolated source-bound drawing-fragment result,not a captured live
before-overlay GPU frame,a complete parent-function return/ABI proof,or a claim
that the covered Flagship appears on screen. An initial diagnostic used the
owner-list interface instead of the adjacent renderer and failed at53433430;
the corrected component test uses023117DC. That diagnostic was not a game crash.

Back exits normally without assigning/swapping ships or saving. The final whole
two-screen town equals its pre-Port screenshot exactly. The actual Swap Ships
screen and returned town were visually inspected. Other fleet compositions and
the other arrange-view parents remain outside this evidence.

## Evidence and current queue

- Verifier: `scripts/verify_fleet_rows_v723.py`; Ruff passes.
- Proof,exact inputs and native underlay: `work/analysis/fleet_rows_v723/`.
- Terminal report/captures/RAM on E under `Generated/work/emulation_v193/fleet_rows_v723_actual`.
- Archive: `E:/Rota Nova translations/Screenshots/Audit comparisons/V723 Fleet row graphics`.
- Ordinary unmodified guide candidates: `E:/Rota Nova translations/Screenshots/Guide candidates/V712 Swap Ships`.

The original consumer/evidence-link follow-up for Iseki/dock is resolved with the
above visibility limits. slackimg12 and Press a button remain. The current matrix
retains an immutable V722 snapshot before updating its current links. All18
original overall plaque/hint objects remain incomplete; all22 historical objects
stay exact. Other control/card/comic/legacy contexts and final verification remain
open. Online exclusions,brown marks and the post-goal older-record check persist.

V712 remains unchanged,SHA256
`6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030`.
No new build,canonical promotion,publication approval,commit or push. Goal active.
