# V519: isolated Osaka and Naha graphics verification

The user authorized isolated location fixtures and other testing cheats. This batch
uses copied saves and changes only eight active-ship coordinate bytes per run.
Original discovery and docking then load the town and its facilities. No normal
voyage, earned unlock, complete playthrough or hardware verification is claimed.

The unchanged V518 ROM passes four complete alternate sprite/caption checks:
Tavern and Inn in Osaka and Naha. Full first/final glyphs and blank cells match.
The retained original artwork remains byte-identical to the clean source.
Three Osaka story frames match every one of the 49,152 background37 pixels on
the top screen. Naha Tavern/Inn match 17,440 unobstructed background47 pixels
each, excluding portrait, nameplate and dialogue occlusions.

Verifier: `scripts/verify_japan_location_v519.py`.
Proof: `work/analysis/japan_location_v519/location_proof.json`.
The verified Nagasaki donor save remains unchanged. No production ROM or patch
changes were made. V518 remains the experimental release; canonical unchanged.
Fixture screenshots are stored separately from the normal-play guide under
`E:/Rota Nova translations/Screenshots/Test fixtures/japan_location_v519`.
The guide archiver now rejects location-fixture captures.

All22 original requirements and all18 incomplete plaques remain under audit.
Other native composition, artwork restoration, condition and deep Gallery/ending
checks remain. The graphics goal is active. Revisit older record-based checks
when the full goal is complete.
