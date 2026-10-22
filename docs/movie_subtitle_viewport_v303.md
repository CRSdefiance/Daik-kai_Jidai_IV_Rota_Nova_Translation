# Actual movie subtitle crop repair V302/V303

V302's fresh playback found a real defect in the inherited M22 subtitle card.
V303 corrects its cause in the authoring rule and integrates source-reviewed
captions in the full combined candidate. All five translated movie cards are
now verified during actual unskipped production playback.

## Defect and high-level authoring rule

The FLS record encodes the native visible width in its first word's high16 bits.
The decompressed allocation is rounded wider. M20/M22/M24 subtitle widths are
168/176/216, while all five storage textures are256 pixels wide.

M20 had an earlier explicit168-width correction. The other four translated
cards were authored around the256-column allocation. In actual V299 Lil playback,
M22 card1 loses42 pixels at source columns176..179:12 white fill and30 opaque black
outline pixels. The first-line mask locates the texture at native screen48,150;
the missing tail lies beyond its176-wide view. This clips the final punctuation
of "It's too dangerous!". Other cards remain complete but have off-center layouts
relative to their native subtitle rectangles.

New subtitle batches set `native_viewport_policy: header-width-v1`. The builder
derives the layout width from the source metadata, rejects an explicit conflicting
storage width, and rejects any foreground/outline ink beyond the native view.
Four negative256-width cases are rejected. Historical batches retain their old
behavior for reproduction. The workflow rule is documented in the build protocol.
No decoder, viewport, animation timing, code, palette or storage size is changed.

## Faithful complete wording

Clean original cards were extracted and visually reviewed. M22 retains the
warning and Lil's twice-repeated reassurance. M24 retains the ship arrival and
captain-report instruction. The second M24 card's original `と思われます` expresses
an inference; "Looks like a foreign merchant ship!" restores that uncertainty,
followed by "Admiral, your orders?". Every complete English line fits its original
compressed slot at the native width. No wording is shortened to fit storage.

| Movie/card | Current English | Native width |
|---|---|---:|
| M20/27 | What is it, Clau? / What did you want to show? |168|
| M22/1 | Hey, don't! / It's too dangerous! |176|
| M22/2 | It's fine, it's fine. / Leave it to me! |176|
| M24/3 | The ship's here! / Report to the captain! |216|
| M24/4 | Looks like a foreign merchant ship! / Admiral, your orders? |216|

M20 is unchanged. Clau remains the original `クラウ` familiar address to Claudio;
the source question and requested item are conveyed naturally in English.

## Actual playback and independent full-pixel checks

Fresh V303 production cold boots select Rafael, Lil and Hodram using ordinary
title/New Game/captain confirmation inputs. There are no later movie-skip events,
loaded savestates, live RAM writes or forced movie/viewer overrides. Runs finish
at6000/6000/7000 frames; all three processes exit successfully, callback errors
are empty and every captured PNG/report identity is checked.

All five cards match every opaque white letter and black-outline pixel from their
complete stored textures in multiple actual frames:8559 distinct source pixels
across31 complete captured card instances. First, interior and final letters
and punctuation are included. All visible ink fits the native source widths.
Transparent source positions show nonblack original scenery, so the subtitle
background is not an opaque black panel. The full five-card preview was inspected.

Native screen origins are M20(39,140), M22/1(48,150), M22/2(41,149),
M24/3(13,147) and M24/4(24,147). The authoring centers each complete line inside
its source rectangle; it preserves the original movie placement.

The original bytecode command parser masks bits8..12. Movie commands are
standalone halfwords, not the message object'sFFFF sentinel. Clean/current source
candidates are SC0B44 offset26 `4900`, SC2B22 offset18 `4902`, and SC1B42 offset36
`4904`; the native caller adds20. Actual playback verifies M20/M22/M24 in those
route openings. The first Hodram attempt lacked its2500 confirmation and remained
on the captain form; it is explicitly excluded as playback evidence. A fresh
corrected run supplies that ordinary confirmation.

All261 clean FLS textures were checked for exact copies of the five Japanese
source cards. Only the five original self-copies match, and all are localized.
This is exact dimension/palette/index equivalence, not proof excluding transformed,
rescaled, differently encoded or approximate copies elsewhere.

## Registered candidate and preservation

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v303` |
| Candidate | `out/all_routes_combined_v303_candidate.nds` |
| ROM SHA256 | `b9a4af601390a4551ae2c11ab4d06b7f3c8ebc2de6cd5178228becb3aa146107` |
| Patch | `out/all_routes_combined_v303_candidate.xdelta` |
| Patch SHA256 | `c675a099f3cf083f2e51b8994b532dc75490f8d60c6b4d0c1e393d09ced68bc2` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Inherited comparison | `out/all_routes_combined_v299_candidate.nds` |
| Comparison SHA256 | `9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Status | Experimental; user acceptance pending; canonical base unchanged |

All467 inherited batches and every accepted requirement/stage remain; two new
canonical-source FLS batches make469 total. The manifest records the complete
registry, source hashes, profile and changed records/files. Only M22 and M24
change versus V299, and only their four owned compressed pixel slots change.
All metadata, palettes, dimensions, archive lengths, animation data and other
assets remain exact. ARM9/ARM7, overlays, all route/COMMON/HELP text, other graphics,
font resources, banner and entry addresses are exact V299. Full V299 reproduces
byte-for-byte before and after the shared builder edit. The clean patch reconstructs
V303 byte-for-byte. Ruff and diff whitespace checks pass.

## Remaining goal work

Experimental: user should test fresh starts and unskipped Rafael/Lil/Hodram
openings, especially full subtitle punctuation and solid outlines over pale/dark
scenery. Earlier naming, actor repair, plaque style and other integrated work are
preserved. This does not certify all movies, all Gallery unlocks, deep scenes,
legacy raw-comic display or physical hardware. All11 legacy native composition
gates and all18 plaque/hint entries plus Armor/Weapon variants remain open.
Low-resolution Online promotional images remain exempt by user instruction.

The full graphics goal remains active/incomplete. At actual completion, revisit
older record-based checks as requested; this defect is another example of why
storage dimensions cannot substitute for native display bounds.

Evidence: V302 `crop_defect.json` and failed/full-card capture proof; V303
`preparation.json`, `release_proof.json`, actual `proof.json`,
`movie_subtitle_review.png`, build/reproduction/verification logs and three
`work/emulation_v193/movie_viewport_v303_*` captures.
