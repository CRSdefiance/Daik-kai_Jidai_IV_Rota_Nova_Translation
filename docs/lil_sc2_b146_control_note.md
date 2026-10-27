# Lil SC2 B146 Kamil and Hodram control note

All 35 B146 records are dialogue or narration and are translated in
`translations/lil_deep_route_v55.json` from the clean Japanese source.
The scene begins with Lil searching for Kamil, then follows his meeting with
Hodram and his decision to sail with him for a while.

The source presentation leads are `01` Hodram, `02` Lil, `09` Kamil,
`14` Fernando, `97` sailor voice and `FE` narration. `97` is established
through earlier Lil lookout and sailor scenes, and `FE` is established as
the narration/system lead. Every B146 Kamil line begins with the `09`
speaker byte. Two source `FI` name macros, in R0039 and R0101, are preserved
as exact macros. No record in this block is excluded.

The inherited `lil-story-deep-route-v48-live` profile recognizes every lead.
The batch passes fixed-byte, speaker, macro, wrap and first-glyph audits with
zero blockers. Five exact-font contact sheets were reviewed; the short
`FE` cutaway caption was also checked in an individual preview. The exact
saved-ROM verifier confirms all 35 new segments and every prior exclusion.

Runtime cold-boot is still needed to verify portraits, nameplates, macro
expansion, the narrator cutaway and the transition to the next scene.
