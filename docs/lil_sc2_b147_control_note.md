# Lil SC2 B147 Maria reveal control note

B147 has 69 clean-source records. The V56 batch translates all 68 text records
into natural English and leaves `DK4_MES_B147_R0129` unchanged: its exact
four-byte `21 46 83 80` payload is the Maria identity-reveal event. The scene
introduces Maria Huamei Li, challenges Lil's trust in Kuhn, explains the
possible planted Li crest, and directs Lil to Kuhn's disowned son in Batavia.
Both Fernando and Julian departure variants are translated.

The source presentation leads are `02` Lil, `03` Maria, `04` Janus, `07`
Christina, `0F` Carlo, `10` Gerhard, `11` Al, `14` Fernando, `15` Ian, `17`
Manuel, `1A` Julian, and `FE` the mysterious woman before the reveal. Six
Li elder records begin with a source `0A` line break and have no speaker
selector. Five preserve `{LB}` as a guarded `20 0A 20` opening. R0021 omits
only the source blank first row: keeping it with the English text and fixed
allocation creates an empty trailing page. Its first visible character is
`A` in “Admiral, you baffle me,” as confirmed in the individual preview.
R0388 retains the source final-line layout with its documented waiver.

The three `FI` and two `FA` source name macros remain exact macros in R0005,
R0295, and R0392. Literal uppercase `I` and `F` were excluded from English
prose because their bytes trigger renderer behavior. The batch passes
fixed-byte, speaker, macro, wrap, entry-phase, and first-glyph audits with
zero unwaived blockers. All nine exact-font contact sheets and the individual
R0021, R0097, and R0392 previews were reviewed. The saved-ROM verifier
confirms all 68 inserted segments and the unchanged reveal control.

Runtime cold-boot remains necessary to check portraits, nameplates, macro
expansion, the reveal event, first and continuation letters, and the Batavia
transition before acceptance.
