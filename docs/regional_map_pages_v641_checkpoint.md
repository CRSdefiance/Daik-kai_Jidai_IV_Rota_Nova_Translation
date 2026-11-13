# V641: all seven regional map pages through ordinary controls

## Result and scope

A fresh V640 cold boot reaches all seven actual regional map pages, then returns
to the North Sea. Every complete 244x160 native bitmap and its palette match the
original blue seaarea source. The map painter's actual registered callback supplies
the complete source extent and destination; those values are not fitted to the
screenshot. A separate V636 cold boot repeats the exact complete input schedule.
All eight selected full two-screen images match that control without exclusions.

This advances the actual regional-page gap retained by V638-V640. It does not
claim travel to, docking at, or earned discovery of the displayed places. No ROM,
patch, wording, source art, release registry or release pointer changes. V640
remains the latest compiled experimental candidate; no V641 ROM is produced.

## Runs and ordinary navigation

- Candidate: `out/all_routes_combined_v640_candidate.nds`, SHA256
  `93868a0b250a3b52897225dac48ab29e0b14d1f097208ca9a418208dd29d0b9e`.
- Control: `out/all_routes_combined_v636_candidate.nds`, SHA256
  `c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d`.
- Both runs: 50,000 frames, no preloaded battery save, savestate, cheat or RAM/ROM
  fixture. Both use the same DeSmuME core and options.
- Current: `E:/Rota Nova translations/Generated/work/emulation_v193/regional_map_pages_v641`.
- Control: the adjacent `regional_map_pages_v641_control` folder.
- Exact schedule: `work/analysis/regional_map_pages_v641/complete_replay_inputs.json`.
- Interactive journal is retained. Its commands are not treated as execution
  receipts: terminal reports, captured RAM, PNGs and native exports verify results.

The existing map schedule reaches Area selection at 39,200. Y Area opens the
previously active regional map. Hovering Med. and pressing Y does not commit the
hovered choice: frame41,600 still contains the North Sea source page0. This
negative observation is preserved and receives no Mediterranean coverage credit.
A Done commits the hovered selection and opens the chosen regional page. Y Map
returns to global Area selection, enabling subsequent ordinary touches and A.

| Frame | Actual page | Displayed region |
|---:|---:|---|
|39600|0|North Sea|
|42800|1|Mediterranean|
|44000|2|Africa|
|45200|3|Indian Ocean|
|46400|4|Southeast Asia|
|47600|5|East Asia|
|48800|6|Americas|
|50000|0|North Sea repeated|

Unlike V640's region tooltips on global page7, these captures contain the actual
separate source bitmaps0-6. Upper-screen town or fleet information depends on
objects in the chosen region. The black upper screens in five selected views
also match the paired V636 control; they are not silently omitted from comparison.

## Verification

- Complete `/_pxl/seaarea.pxl` remains exact to clean. Its eight source palette
  banks are identical. The separate `/_pxl/seamap.pxl` remains exact too and is
  not substituted for the actual blue atlas.
- Each actual RAM bitmap matches exactly one complete source page, all19,520
  packed bytes/39,040 indices. Eight views check156,160 packed bytes/312,320
  indices. Wrong-page comparison is explicitly rejected.
- Every actual dynamic palette is byte-exact to the original source bank0.
- Actual map sprite02190E80 belongs to the captured renderer023117C4 linked chain.
  Its original callback0200CAF8 runs from each captured RAM copy, returns with
  full stack/saved-register ABI, and executes only clean-identical instruction
  words. Original getter and draw helper operands select header02279B38, bank0,
  source0,0, size244x160, destination6,16, software screen selector0.
- All eight read-only native exports verify same-frame main RAM and no main-RAM
  changes by serialization. Their complete exported regions are hash checked.
- All312,320 physical VRAM map-crop words match actual lower-screen pixels at
  native BGR555 precision. Screen placement is verified positively, not inferred
  from the software selector alone.
- All786,432 selected current/control two-screen pixels match exactly, including
  route overlays, tooltips, upper screens and controls. No overlay is masked from
  this comparison. Individual route-line/marker producer reconstruction is not
  claimed; their difference counts from the base map are reported separately.
- The initialized blue-source owner filename and one complete unique resident
  source file are verified in every actual RAM capture. Their presence alone is
  not used to establish display; actual selected bitmaps and painter operands do.

All eight current full screens were visually inspected. No new painting, palette
or display-bound defect was found. No new translation or independent source-text
interpretation is authored in this checkpoint.

## Evidence and remaining work

Verifier: `scripts/verify_regional_map_pages_v641.py`.
Proof: `work/analysis/regional_map_pages_v641/actual_regional_pages_proof.json`.
Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V641 Regional map pages`.
Two ordinary current North Sea/Mediterranean guide candidates are saved separately
on E. They document map browsing, not acquisition, travel or publication approval.

All18 original plaque/hint objects remain incomplete, and all22 historical
requirement objects/scopes remain unchanged. The additive evidence narrows the
remaining map work to separate sepia/legacy consumers, other map states and
unverified overlay producers. Raw comic/title consumers, village cards,
miniature/Confirm ordinary contexts, other movie/material variants, plaque
texture acceptance and final cold-boot acceptance remain open. Older record-based
checks remain due at actual full-goal completion. The full graphics goal stays
active. The preceding status answer was informational; this turn advances the
state through actual page selection and current/control display evidence.
