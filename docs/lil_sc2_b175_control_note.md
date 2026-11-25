# Lil SC2 B175 Aziza confrontation control note

B175 contains 33 source records. The 32 dialogue records are translated in
`translations/lil_deep_route_v75.json`. `DK4_MES_B175_R0012` is a four-byte
`96 46 CA 80` event payload, not dialogue; it is explicitly excluded and
preserved unchanged.

Source presentation leads are `02` Lil, `09` Kamil, `FE` Aziza, and
`B7`-`B9` pirate crew. The `FI` name macro occurs four times and `FA`
once; all five source macro instances remain in their corresponding
English records. English prose avoids literal uppercase `I` and `F`,
which are unsafe renderer bytes.

All 32 translated records pass the fixed-byte, speaker, wrap, pair-phase,
macro, and first-glyph audit. Both exact-font contact sheets were visually
reviewed. Direct saved-ROM verification confirms all 32 inserted records
and the opaque event payload remains byte-for-byte unchanged.

Runtime cold-boot remains necessary to check Aziza's entrance, her crew's
portraits and nameplates, the `FI`/`FA` names, first and continuation
letters, and the encounter transitions.
