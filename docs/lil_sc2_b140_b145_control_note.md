# Lil SC2 B140–B145 translation and control note

The clean Japanese source is `work/sc2/script.csv` from `work/clean.nds`.
The four new batches cover 102 identified records: 101 translated text records
and one preserved event payload.

| Batch | Scene | Text records |
| --- | --- | ---: |
| V51, B140 | Lelystad founder's polder plan, Lil's pledge and new purpose | 49 |
| V52, B141–B142 | Shortfall visits and alternate full-funding branches | 27 |
| V53, B143 | Shipyard armor research request and 300,000-gold funding | 9 |
| V54, B144–B145 | Armor upgrade completion and Mediterranean Proof map reveal | 16 |

B141–B142 preserve the million-gold project cost, the founder's independently
raised tenth, and Lil's 900,000-gold contribution in both branches. Source
`FI` name macros are encoded as exact macros. B144 preserves the armor-upgrade
system notice; B145 uses the registered item names `Patterned Cloth` and
`Brass Lamp`. The B145 R0021 bytes `23 48 9C A8` form an opaque reveal event
payload. They are excluded from translation and remain unchanged in the ROM.

All 101 translated records pass fixed-byte, speaker-state, macro, wrap and
first-glyph audits. Every contact sheet for V51–V54 was visually reviewed.
Ambiguous contact-sheet opening glyphs were checked in individual exact-font
previews. Source leads `02/04/09/0D/10/14/15/17/6D/AB/FE` and the inherited
profile are preserved as applicable; future blocks must be checked against
their own source leads.

This is static verification. Cold-boot the combined candidate through the
polder funding choices, shipyard armor upgrade, system notice and cloth/lamp
map reveal before accepting it as a new base.
