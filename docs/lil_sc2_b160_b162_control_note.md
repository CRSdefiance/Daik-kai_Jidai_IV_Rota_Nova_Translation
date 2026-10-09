# Lil SC2 B160-B162 stolen-ship control note

B160-B162 contain 23 source text records, all translated in
`translations/lil_deep_route_v67.json`: 21 in B160 and one dockworker
update each in B161 and B162. There are no opaque exclusions in this set.
The crew discovers its ship missing, hears a witness describe a lone man
sailing away, and checks back at the harbor.

Source presentation leads `02` Lil, `09` Kamil, `0E` Emilio, `0F`
Angelo, `74` dockworker, and `97` crew messenger are retained. The one
source `FI` name macro is preserved. The new `74` lead is registered in
`lil-story-deep-route-v67-live`. English prose avoids literal uppercase
`I` and `F`, which are unsafe renderer bytes.

The fixed-byte, speaker, macro, wrap, pair-phase, and first-glyph audit
found zero blockers. All three exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 23 inserted records.

Runtime cold-boot remains necessary to check the ship-discovery scene,
dockworker updates, portraits, nameplates, macros, first and continuation
letters, and transitions.
