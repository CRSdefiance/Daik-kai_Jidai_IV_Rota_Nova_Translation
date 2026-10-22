# V634: ordinary two-ship cargo and bounded selection trace

## New coverage

The prior V633 turn fixed the clipped Ship Info heading and centered Refit.
This turn exercises different ordinary gameplay paths on unchanged V633:
buying and naming a second ship, switching between two ships in Cargo Setup,
moving an occupied cargo slot through Temporary Storage, and canceling the
normal Finish confirmation. No miniature or Confirm crop is supplied.

The isolated copied-save session buys a Latina through the original Yard > Buy
flow and accepts its default name. A normal resupply prompt is also accepted.
Original money getters report38371 before purchase,35771 after it, and35671
after resupply. The original donor file is never saved over. The new ship has no
sailors, and the normal Port warning is acknowledged before selecting Cargo Setup.
The test does not claim an actual departure with that ship.

Two ship views are then exercised with ordinary L/R controls. The source view
slot at parent+18 changes from the12-byte Iron record to empty. After selection
from Temporary Storage, the same original12-byte record appears at parent+54,
and remains there across subsequent L/R changes. Exact bytes are retained in
the proof. These are source-bound view-state observations; the final cargo setup
is not committed or saved. X displays the original confirmation and B returns.

## Complete graphics and text checks

- Nine original-font heading masks pass, including every first/final letter and
  blank cell: **Vestaros Cargo Setup** and **Latina Cargo Setup**.
- Eight entire Temporary Storage banners pass all4096 pixels each, including
  letters, wood grain, bevels, palette and blank space:32768 pixels total.
- All nine captured header views resolve the original owner02313C7C and actual
  `_pxl/tempcargo.pxl` filename through captured native state. Original cached
  getter020D4170 returns the complete resident file byte-exact to current V633.
  The source header-choice field is0; no header or crop is injected.
- The full **Is this cargo setup okay?** prompt passes the original-font mask.
- A clean-ROM run replays the same54 inputs and confirms the original banner
  and tooltip behavior. The Japanese selected-item hint covers371 banner pixels
  at20600; current English covers246. The Japanese hint is40 pixels wide, while
  Iron's English hint is28. Both lie at the original hint position over the banner.
  Every other declared source banner frame matches its entire clean-ROM asset.
  This is an overlay, not a missing banner-letter repair.

The top heading center follows its full six-pixel character-cell width in the
256-pixel view. Vestaros's20 cells start at68; Latina's18 cells start at74.
Full first/final-character erasure controls are retained by the mask verifier.

## Runtime drawing investigation

A clearly named diagnostic-only copy of V633 uses the identical852-byte bounded
observer from V603. It adds01FFD000..01FFF000 and branches at the two original
corner/tiled drawing entries01FF92D8/01FFAE70. The original resource, crop,
palette, getter and draw inputs are untouched. The original autoload sections
are preserved except the one corner-entry branch and SDK autoload bookkeeping;
only ARM9 and the6208-byte overlay file differ. The overlay table is unchanged.
This ROM is not a release parent or a guide source. Instrumentation may alter timing.

All20 register/flags/stack/source ABI cases and the earlier deduplication,
overflow, rejection and positive-control tests pass against the new copy.
The actual trace run cold boots with the same donor and54 inputs. All80 unique
sampled two-screen frames match the unmodified V633 run exactly:7864320 pixel
positions. Source and diagnostic runs each end normally at22600 frames, with no
savestate, callback error, inventory/location/condition/outcome or unlock fixture.

The observer sees293091 calls through the two declared drawing entries. Its two
selected positive controls are ordinary source-row208 atlas decorations, one
from each entry. There are no target-shaped records and no overflow. Original
hook branches, observer code and unused log tail remain exact in the final
read-only ITCM export. Every original palette-color full miniature mask is also
absent from all80 sampled English screenshots.

These results specifically exclude the declared software-draw shapes in this
new purchase/naming/two-ship/cargo input path. They do not prove global non-use,
exclude unsampled frames, or cover arbitrary GPU, resized, partial/composed,
direct-color or embedded consumers. The five miniature and separate Confirm
ordinary parents therefore remain open. Earlier positive log-pointer identity
is not inferred from later RAM that could have reused its address.

## Diagnostics and wording follow-up

An initial menu discovery departed to Sea View and stopped normally at6000.
A separate first purchase discovery stopped normally at15000. They are retained
as diagnostics rather than the paired comparison run. Trying the whole modal
CSelectShipView callback020A0E50 as a standalone paint entry failed at020E4FAC;
that rejected probe earns no drawing/display credit. The executed ordinary
purchase list at9400 does contain live CSelectShipView vptr02150B38, object02188204.
The subsequent bounded runtime trace supplies the authoritative drawing evidence.

The original selected commodity is **鉄鉱石**, meaning **iron ore**. Current
English **Iron** remains a legacy abbreviation. Entry90 of
`translations/commodity_name_manuscript_v343.json` explicitly leaves older
abbreviation/fidelity review open. This is a concrete follow-up: review the
source commodity and related ore labels, then fit complete faithful names through
their existing provider/consumer layouts. No wording or production binary changes
are made in this evidence checkpoint. The next localization work should not
silently treat that old entry's source/localization flags as final approval.

## Files, audit and next work

- Current experimental candidate remains `out/all_routes_combined_v633_candidate.nds`.
- SHA256 remains `eea7c88cd8c6082cf56a8779421018913f2ef9b40ca3cc77fe1d1b13b74ec05f`.
- Diagnostic copy: `work/analysis/selection_contexts_v634/selection_trace_RESEARCH_ONLY.nds`.
- Preparation: `scripts/prepare_selection_trace_v634.py`.
- Verification: `scripts/verify_selection_contexts_v634.py`.
- Proof: `work/analysis/selection_contexts_v634/release_proof.json`.
- Runs under `E:/Rota Nova translations/Generated/work/emulation_v193/`:
  `selection_contexts_v634_two_ship_baseline`, `selection_contexts_v634_two_ship_trace`,
  `selection_contexts_v634_two_ship_original`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V634 Two ship selection contexts`.
- Guide candidates: `E:/Rota Nova translations/Screenshots/Guide candidates/V633 Two ship cargo`.

All18 original plaque/hint objects remain incomplete and exact, and all22
historical requirement objects/scopes remain exact. No production ROM, patch,
release registry, latest-compiled/latest-verified pointer, canonical baseline or
donor file changes. Current V633's full470-batch/114-layer integration and exact
patch remain their previously recorded evidence. No new921-asset or57-block
preservation claim is made from these UI tests. The full graphics goal is active;
legacy, village-card, miniature/Confirm, material, other movie and human-review
requirements remain open. Older record checks remain due at actual completion.
