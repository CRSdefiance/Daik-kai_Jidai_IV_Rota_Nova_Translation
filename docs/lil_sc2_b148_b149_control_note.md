# Lil SC2 B148-B149 control note

Both blocks are complete in `translations/lil_deep_route_v57.json`: all 24
B148 and 21 B149 clean-source records are natural-English dialogue. No
nontext payload is present in these blocks, so none is excluded. B148 follows
Maria's Batavia lead: a local recalls Kuhn's estranged son by the nickname
Kamil, forcing Lil and Fernando to reconsider what Kamil concealed. B149 is
the Tang Bamboo Craft and Bamboo Assembly Plan puzzle; both Kamil and
Fernando paths lead to the map to East Asia's Proof.

Presentation leads are `02` Lil, `09` Kamil, `0E` Emilio, `14` Fernando,
and `5C` the Batavia local. The source `FI` name macro in B149 R0044 is
preserved exactly. English prose avoids literal uppercase `I` and `F`, which
are unsafe renderer bytes. The fixed-byte, speaker, macro, wrap, pair-phase,
and first-glyph audits found zero blockers. All five exact-font contact
sheets were reviewed, and B148 R0094 was rechecked in its individual preview
after a naturalness edit. Direct saved-ROM verification confirms all 45
inserted segments and every prior exclusion.

Runtime cold-boot remains necessary for the Batavia conversation, Kamil
identity reveal, both bamboo-puzzle variants, name macro expansion, first
and continuation letters, and map transition before acceptance.
