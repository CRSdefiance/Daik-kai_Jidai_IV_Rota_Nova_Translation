# Genuine Game Over display V445

The previous turn was progress: current inventory proof and consumer classifications.
This turn pursued the occupied-armor gameplay gate using the normal Copenhagen
save. The voyage failed and reached Game Over; armor was not acquired or equipped.
No ROM, live RAM, stats, item flags or unlock flags were modified.

## Normal progression and failed course

Unchanged experimental V443 cold-boots an isolated copy of
`E:\Rota Nova translations\Saves\hodram-copenhagen-docked-v414.dsv`.
Normal inputs load the saved sixth slot and depart. Northward steering encounters
the coast; a normal mermaid event occurs. The fleet remains at the same point
between13200 and14400 while the course presses against land. Supplies decrease,
a scurvy message appears and the sailor count falls. A southwest correction moves
the fleet, but the actual warning at15600 says `Vestaros has no sailors!`.
Ordinary input reaches Game Over at16400. The emulator then stops normally.

The original battery save remains hash exact. This failed sailing schedule is
recorded for provenance and regression, not an acquisition route to repeat.
Future acquisition work needs a corrected course/resupply plan or a normal save
near the armor. The existing Copenhagen donor remains the usable starting point.

## New actual graphics evidence

- Original `/_pxl/gameover.pxl` and `/_pxl/overfont.pxl` remain byte exact to clean.
  Their complete headers, palettes and pixels are found in the actual final RAM.
- Actual owners are0231390C and023138F8; native views are02192A00 and02192A74,
  with bank0 and full256x192 /160x32 extents.
- Original English `Game Over` is retained. At screen origin48,272, all835 ink
  pixels and all5120 caption/background cells match the complete source composite.
- All72 Select-label pixels and all237 crew-loss-warning pixels, including the
  complete dynamic ship name and blank cells, match the native font.
- A separate cold boot of V414 using the exact same donor and ordinary input
  schedule produces45 matching captured frames and a pixel-exact final screen.

The footer and14 additional bright pixels differ from the standalone background
PXL; their actual output matches V414. This is a full-frame regression comparison,
not independent identification of every overlay or a complete source-only
background composition proof. No correction is justified by these differences.

Verifier: `scripts/verify_game_over_live_v445.py`.
Proof: `work/analysis/armor_voyage_v445/game_over_proof.json`.
Reproducible normal input schedule: `work/analysis/armor_voyage_v445/replay_inputs.json`.
Reports: `work/emulation_v193/armor_voyage_v445/capture_report.json` and
`work/emulation_v193/game_over_parent_v445/capture_report.json`.

The final native screenshot is archived for a possible guide and copied to E.
No new ROM or patch is needed. V443 and its exact patch remain unchanged.
All22 historical requirements and all18 incomplete plaque entries remain in the
audit. This is targeted emulator evidence, not hardware testing or a completed
route. The full graphics goal remains active. Revisit older record-based checks
after true full-goal completion.
