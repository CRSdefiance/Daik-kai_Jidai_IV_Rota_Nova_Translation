# V576: actual Grand Race help, menus and bounded consumer investigation

The preceding user-response turn confirmed that the plaque defect was already
recorded; it did not advance the artwork or its verification. This goal turn adds
actual native UI evidence. Production remains the registered experimental V573,
SHA256 `f987f1c56ba5641544e5c84698c59351e39465b15001601adddf697698d89a77`.
No graphics, prose, ROM, patch, release registry or canonical baseline is changed.

## Isolated save and actual navigation

The original V521 checksum-valid system-unlock save is reused without modification.
Its SHA256 remains
`295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949`.
The original donor also remains byte exact. Its low four system completion bits
were artificially unlocked in that historical fixture; this run does not prove
earned completion or legitimate race access. The V521 manifest is retained. A
separate current manifest binds the same save to the verified V573 ROM hash.
The harness records this as a synthetic Gallery/system-unlock fixture rather
than silently treating the copied save as ordinary earned progress.

An initial native run stopped normally at frame7400. A fresh cold boot then
replayed its inputs and continued to frame12200, with no savestate or additional
RAM/code fixtures. It opened Grand Race > Read the Rules, visited all nine pages,
tested previous-page returns, selected Start Race and the copied Maria save,
confirmed loading, selected Host, reached the one-player waiting screen, and
returned with B to the title menu. Both processes finalized normally. The final
32-event input schedule and read-only RAM exports are retained.

The observed one-player Host screen does not show a Confirm control. Its
availability conditions remain untraced. This capture does not establish the
separate kakutei.pxl button's parent crop, a wireless connection, or a completed race. Source reference
inspection found its direct owner literal in the startup registration region;
that observation does not prove global non-use or identify every indirect caller.

## Complete native text and measured geometry

All nine actual pages pass their complete native-font title and body masks:
About the Race, Basic Rules, Your Ship, Race Area, Prizes, Map, Supplies,
Time Limit and Stopping a Race. All 49 body lines include their first/final glyphs,
spaces and blank cells. The complete 252x128 body foreground mask is also exact
on every page; no extra, missing or displaced gray text is accepted. The body
contains 16,785 ink points; the nine green titles contain 1,001.

The six actual menu labels—Start Race, Read the Rules, About the Race, Basic Rules,
Map & Supplies and Race Limits—pass 874 complete native-font ink points, including
all blank cells. Their pointers are read from actual menu entries, not inferred
from matching visible English alone. Each help descriptor and body pointer is
bound to captured RAM, the mapped current ARM9 and the existing manuscript's
compiled bytes. No translation is rewritten in this checkpoint.

Actual header origin is (4,192), body origin (4,216), glyph cells 6x11 and body row
pitch 16 pixels. Every observed body line is left aligned at x4. Each page rejects
the old 12-pixel pitch as a negative control. The historical compiler/model remains
unchanged for exact release reproduction; its 12-pixel research coordinates must
not be presented as measured native framebuffer geometry. The longest page has
eight lines, all above the footer. Previous returns from Prizes to Race Area and
from Stopping a Race to Time Limit reproduce the entire earlier frame exactly.
The complete source-linked English remains readable in the visual review.

## Miniature graphics remain unresolved

The Start Race popup, four-group rules popup, save selector, load confirmation,
Host/Join selector and host waiting state were inspected. Their six RAM snapshots
contain no valid 12-word frame-owner views under the established 02313F60 owner
layout, including no broader rectangles overlapping the five miniature cells.
This improves on the older exact-origin filter, but remains a bounded negative:
direct software blits, other view layouts, aliases, other states and other parents
are not excluded. Matching runtime menu words do not prove atlas-cell use.

Done, Rank, Cancel, Pick Cargo and Pick Ship therefore retain their unresolved
ordinary-consumer status. Grand Race setup provides no new display credit for
these atlas cells. The separate small M/D date graphics retain V562's actual
native-use evidence. The earlier name-field tap probe did not open an editor in
its tested New Game screen; it does not establish a global inability to edit names.

## Reproduction and saved evidence

- Verifier: `scripts/verify_grand_race_native_v576.py` (Ruff passes).
- Proof: `work/analysis/miniature_consumers_v576/native_help_and_consumer_proof.json`.
- Exact replay: `work/analysis/miniature_consumers_v576/final_recorded_inputs.json`.
- Fixture provenance: `current_save_fixture_manifest.json` in the same directory.
- Finalized native report and RAM: E:/Rota Nova translations/Generated/work/
  emulation_v193/grand_race_v576_complete.
- Sixteen unmodified full screenshots, reports, proof, replay and hashed provenance:
  E:/Rota Nova translations/Screenshots/Test fixtures/V576 Grand Race.

For unattended reproduction in a fresh output directory, use the existing
`headless_desmume_v193.py` with the V573 ROM, `--frames 12200`,
`--inputs-json work/analysis/miniature_consumers_v576/final_recorded_inputs.json`,
`--capture-every 12200 --capture-at 2400 3000 3400 4400 4800 5200 5600 6000 7000
7400 8400 8800 9200 10000 10600 11000 11400 11800`,
`--dump-capture-ram --touchscreen`, the original V521 `gallery-test-only.dsv` via
`--battery-save`, `--allow-gallery-fixtures` and the current manifest via
`--gallery-save-fixture-manifest`. Do not add a pause for an unattended replay.
The recorded run instead paused at10600 and continued through four ordinary
interactive inputs; both schedules are retained. The verifier intentionally
names the recorded evidence directory and does not treat a replacement run as
identical provenance without inspection.

These captures are labeled test fixtures, not ordinary guide candidates. No
guide publication, complete playthrough or physical-device behavior is claimed.
All 18 original plaque/hint entries remain incomplete and all 22 historical
requirements retain their exact objects and scope. The global plaque-material
defect and other graphics/native-context gates remain open. The full graphics
goal remains active; revisit older record-based checks at actual full completion.
