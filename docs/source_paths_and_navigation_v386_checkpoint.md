# Remaining loose art and actual Info Mode V386

Evidence checkpoint using unchanged registered V383. The graphics goal remains
active. All 22 historical requirements and 18 incomplete plaque/hint entries remain.

## Four loose-image source reviews

Native-resolution previews of the four paths outside V385's tested loading families
are saved under `work/analysis/remaining_loose_paths_v386/`. They are source previews,
not emulator screens or guide images.

| Path | Source decision | Current evidence |
| --- | --- | --- |
| `/_pxl/copyright.pxl` | Retain original Latin copyright line and original date. | Entire file and every pixel remain exact to clean. |
| `/_pxl/ship_eurL.pxl` | Retain the mast, sail, sky, rail and ship-material texture; no separate Japanese caption. | Entire 312x246 image/file remains exact to clean. |
| `/_pxl/logo.pxl` | Retain existing English Uncharted Waters IV / Rota Nova localization. | Original header, palette and extent preserved; standalone consumer unproven. |
| `/_pxl/startmenu0.pxl` | Retain existing English Uncharted Waters IV / Porto Estado title localization and its original edition branding. | Original header, palette and extent preserved; consumer unproven. |

`source_review.json` records exact clean/current hashes and these decisions. This
does not declare the files unused or clear their original display requirements.
There is no newly confirmed Japanese text to translate in these four current views.

## Source-backed movement prerequisites

Clean HELP block83 states that the D-pad operates the rudder and L/R turns the sails;
touchscreen movement is also supported. Cardinal D-pad names are not themselves
proof of movement to those geographic directions. Source block76 requires a captain
and surveyor for Auto Move, a connected route and faction shares at its endpoints
and every intermediate city. Assigning a surveyor alone does not enable an arbitrary
destination. These conditions explain why prior route-gate failures do not prove
a broken Stop caption. Source extracts are in `auto_sailing_source_help.json`.

## Actual voyage and matched control

Two 8,800-frame cold boots use the same V383 ROM and unchanged genuine V328 battery
save. Both load the second slot normally. One supplies ordinary touchscreen steering
and Y; its control removes only the steering touches, retaining loading and Y.
No savestate, RAM injection or synthetic progression is used. Both exit normally.
Their whole screenshots are identical through frame6000 before steering.

At frame6800 the touch run visibly reads N57 E24, while the no-steering control
reads N57 E19, from an initial N57 E16. The coordinate region differs. This proves
an effect on movement; it does not calibrate absolute geographic touch headings,
separate speed from bearing, or independently decode native position fields.
The touch voyage ends at the visually read N58 E23 after encountering coastline.
No port, treasure, weapon or armor acquisition is credited. Early commentary calling
the touches a reliable absolute direction is superseded by this bounded result.

The no-steering control reaches actual Info Mode and selects the player's fleet.
Its complete upper176-row panel matches all 45,056 native five-bit RGB pixels:
819 white glyph pixels and exact black background/blank cells. Heading, full English
instructions, first/final letters and punctuation are intact. Both lower tooltip
lines, Bergstrom Fleet and Brigantine class, independently match complete native
font masks. `scripts/verify_navigation_info_v386.py` validates ROM/manifest, donor,
input schedules, every PNG hash, no errors/no savestate and those complete masks.
Targeted Ruff passes.

## Artifacts and remaining work

Proof: `work/analysis/navigation_touch_v386/display_control_proof.json`.
Actual reports: `work/emulation_v193/navigation_touch_v386/capture_report.json` and
`work/emulation_v193/navigation_no_steering_v386/capture_report.json`.
The finalized Info Mode screen is archived unchanged in
`guide/screenshots/info-mode-at-sea-v383.png` and copied with verified SHA-256 to
`E:\Rota Nova translations\Screenshots`.

Candidate remains `out/all_routes_combined_v383_candidate.nds`, SHA-256
`2259d228e48f8294831d6aeceffbd32654b4502623513d51762387f7b0b512d2`.
No new ROM or patch was needed; full release handoff remains in
`docs/tavern_round_v383_checkpoint.md`.

Precise arrival, occupied equipment, additional conditions, raw legacy consumers,
the four loose-image display paths, retained regional art and deeper Gallery/endings
remain open. Low-resolution Online translation remains user-exempt. These targeted
emulator checks are not complete routes or hardware tests. Revisit older record-based
checks when the full graphics goal is complete.
