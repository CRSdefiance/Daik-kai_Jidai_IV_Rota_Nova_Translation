# Native-height genre card V304/V305

V304's current source review rechecked the standalone raw FLS painting and
remaining retained marks, then identified a second native-size authoring problem.
V305 restores the genre card's original vertical center and approximate lettering
width without changing its established wording, palette or native geometry.

## Genre card source and correction

Clean `/FLS/logo.fls` texture3 reads `リコエイションゲーム`. The current project
wording remains `REKOEITION GAME`; no new brand/genre translation is introduced.
Its native record describes256x192, while the padded texture allocation is256x256.
The original Japanese visible ink occupies39,83 through215,109, centered at y96.
The inherited English occupies76,123 through179,132, centered at y127.5.

The old writer centered against the stored256 rows. The new `header-size-v2`
authoring policy derives both width and height from the original record metadata.
It rejects explicit sizes that disagree with native dimensions and rejects ink/
outline outside the native rectangle. The FLS writer accepts an optional native
layout height. Historical callers retain their original default behavior, and
V303's width-only subtitle batches reproduce exactly; their heights already32.

Complete English is centered in256x192. The native-size20 font matches the
original's approximate ink width:172 pixels versus176, improving on the old103.
New actual ink bounds are42,89 through214,103, centered exactly at y96. No letters
are trimmed, condensed or shortened. The complete foreground has787 pixels.
Two negative native-size cases are rejected. Other logo pictures remain exact.

## Actual current startup

A fresh production V30520000-frame ordinary-input cold boot displays all787
foreground pixels exactly in two actual startup frames450/480, at source origin0,0.
Every first/interior/final glyph is included. The genre, title menu and final town
frames were visually inspected. The run reaches title/New Game, Rafael's opening
and Lisbon town/harbor UI. No state is loaded or RAM injected, callback errors are
empty, every capture hash passes, and the process exits successfully.

This is targeted actual emulator evidence, not all-movie, all-route or hardware
verification. The five corrected subtitle cards are byte-identical to V303 and
retain their prior actual playback proof.

## Current root image and retained marks

`/m02_03.fls` is still the clean raw-storage file. Its512-byte palette and262144
pixels decode as512x512, with377 in the visible-height word. Original coastal
painting, stored padding and roundtrip are exact. Full source review finds no
readable Japanese caption or instruction; the retain-original-art decision stands.

All261 current FLS textures were checked for exact decoded copies of that root
palette/bitmap: only the root self-copy matches. M20's128-tile images are not an
exact whole root copy, and a proposed regular4x4 tile correspondence is not adopted.
Visual resemblance alone does not authorize synchronization or a native-consumer
claim. The root file's actual consumer/projection remains unknown.

The consecutive original comic panels6/7/8/9 were compared. Both retained brown
water-mark regions in raw SLACKIMG block19 frame6 are byte-for-byte clean source,
including their adjacent scenery. Their reading or anatomical interpretation
remains unproved; the publisher search did not supply author/creator evidence.
No kana reading, horn identification or unused-data claim is invented. These
uncertainties and all11 legacy native-layout/composition gates remain open.

## Registered release and preservation

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v305` |
| Candidate | `out/all_routes_combined_v305_candidate.nds` |
| ROM SHA256 | `f9cba4b0b48a57f9afc51d7ef1d56f48fde6888202d65c237096f2d3407563d4` |
| Patch | `out/all_routes_combined_v305_candidate.xdelta` |
| Patch SHA256 | `35e3b485ac832e59fe3ec02d718dcbae26f843a2c1e02373b8c726e24fa3107f` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Inherited comparison | `out/all_routes_combined_v303_candidate.nds` |
| Comparison SHA256 | `b9a4af601390a4551ae2c11ab4d06b7f3c8ebc2de6cd5178228becb3aa146107` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Status | Experimental; user acceptance pending; canonical unchanged |

All469 inherited batches and every accepted requirement/stage remain, plus one
new canonical-source genre batch for470 total. The manifest records the complete
registry, batch/profile/source identities and changed files/records. Only
`/FLS/logo.fls` changes versusV303, inside one owned compressed pixel slot. All
metadata, palette, dimensions, allocation, other logo pictures, ARM9/ARM7/overlays,
routes, COMMON/HELP/names, other graphics and banner/entry addresses remain exact.
Full V303 reproduces byte-for-byte before and after writer/builder changes. The
clean-input patch reconstructs exactly. Two focused opening-movie tests and Ruff
pass. No unrelated release layer is removed or promoted.

## Remaining goal and user testing

Test the startup genre lettering and title/New Game flow on the user's emulator.
Legacy source interpretation/native composition, root-image consumption, Gallery/
deep scenes and all18 plaque/hint entries with Armor/Weapon variants remain open.
The low-resolution Online images remain exempt by direct user instruction. The
full graphics goal remains active/incomplete. At actual completion, revisit older
record-based checks as requested, including padded allocation versus native bounds.

Evidence: `work/analysis/root_fls_v304/source_proof.json`, V305 `preparation.json`,
`release_proof.json`, `live_proof.json`, source/target PNGs, reproduction/build logs,
exact reconstructed ROM and `work/emulation_v193/genre_card_v305` captures.
