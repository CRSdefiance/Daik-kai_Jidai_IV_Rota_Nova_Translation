# Combined V160: complete English button prompt

V160 is the latest **experimental** combined candidate. It adds one translated
instruction in two graphics resources. The full translation goal is incomplete.
It has not been promoted to the canonical baseline.

## Translation and artwork

The original **ボタンを押してください！** means “Please press a button.” The
localized instruction is **Press a button!** It retains the generic button
instruction and exclamation without inventing a particular controller key.

Both `/_pxl/slackimg20.pxl` and `/GRP/SLACKIMG.DK4` block 20 now contain the
complete English label. They use the game's original 6×11 English glyphs,
centered at (33, 6), with a dark outline and lower/right shadow. The gold/brown
palettes, 156×24 dimensions and all header fields remain exact. The owned baked
lettering/background rectangle is reconstructed from untouched side margins,
with ordered dithering; that background is not claimed pixel-identical. All
pixels outside the rectangle and all other embedded archive blocks are exact.
The original and both English source-palette previews were visually reviewed.

Preview: `work/qa/button_prompt_research/paired_review.png`.
Source/prose/storage evidence: `work/analysis/button_prompt_artwork_research.json`.
The release compiler draws the face glyphs from the locked game font; its
background contains the outline/shadow with face pixels cleared first.

## Verification and its scope

Eight focused tests pass, including complete native glyph pixels, rejection of
a missing first “P”, source-pixel drift rejection, full bitmap size/adoption,
paired release-batch equality, owned-rectangle preservation and release-stack
inheritance. All new scripts/tests pass Ruff.

The unmodified native `020D1604` text routine executes the entire English string
through the actual font lookup and paletted glyph painter. Its complete raster,
first/final glyphs, image header, canaries, stack and saved registers pass.
The native `020470B4` atlas selector executes the concrete existing PXL getter,
full bitmap initialization/view adoption and cleanup for selectors 20, 21 and
255. Every case preserves the complete 156×24 extent and caller ABI.

The loaded header/resource class is a **controlled input contract** for that
scoped sizing check. It does not prove the actual file loader or widget/GPU
initialization, palette/alpha presentation, hardware keys or all prompt contexts.
See `work/analysis/button_prompt_native_research.json`. The actual native
descriptor consumer `02028E8C` selects image slot 20 for type 3 and computes
horizontal centering; its complete widget construction/input path remains to
be mapped. Do not treat these scoped checks as physical gameplay approval.

The saved candidate contains the exact reviewed loose/embedded artwork. Every
other internal resource and component, including ARM9, all route scripts,
COMMON and HELP, is byte-identical to V159. All inherited relocation/terminal
stage reports and changed-record lists are exact. Existing V159 text proofs
retain their actual source hashes; no new execution of those matrices is claimed.
Canonical menu/graphics invariants and exact clean-ROM patch reconstruction pass.
Saved proof: `work/analysis/button_prompt_v160_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V159 comparison | `51a89ca2cf0ec6beab6e2a68670eb1cc6368d069fee1947fe5fc367a644d83a5` |
| V160: `out/all_routes_combined_v160_candidate.nds` | `8a2cd62835ac2b5ecc3e176877fcaf2f08f45f119dff1fd64006d634a09b40e6` |
| ARM9, exact V159 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V160 build | `99e6f19407d5bc234e6db217ee9c608d5498cd58e330e04995b496a28c1cf940` |
| V160 patch: 761601 bytes | `0c003e940a78fb261897c5c689111dc9329a13762f88bae0fafc34111260fe11` |

Registered profile: `all-routes-unified-v160`, experimental. It preserves all
435 V159 profile batches and all terminal stages, then adds
`translations/button_prompt_graphics_v1.json` and
`translations/button_prompt_embedded_sync_v1.json`: **437 batches** total.
All accepted layers are already baked into the canonical baseline; zero
additional accepted batches are required. The adjacent `.manifest.json`
records the exact baseline, registry, batch list, records, stages and checks.

Compared with the canonical baseline, eleven internal paths differ:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/SLACKIMG.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`,
`/_pxl/slackimg20.pxl`, `/data/SC0.DK4`, `/data/SC1.DK4`,
`/data/SC2.DK4` and `/data/SC3.DK4`.
Only the two button-prompt resources differ from V159.

Before acceptance, cold-boot without a savestate and check the title, New Game
captain selection, an established story scene, town UI, inherited changed
item/Advice/Gallery screens and every context displaying the shared button
prompt. Its palette/alpha, full visibility and controller behavior need physical
verification. Identifying all prompt contexts and proving native resource loading
remain mapping tasks. Explicit user acceptance is required before promotion.
No commit or push is claimed here.

## Full goal remaining

245 COMMON selections / 133 physical owners still need actual consumer/layout
integration. Other ARM9/UI consumers, graphics, name fidelity, Reports/Sailing
Help persistence, BGM physical audio/input, downloaded item states and complete
gameplay checks remain. The historical graphics inventory had 26 confirmed
Japanese loose/FLS resources and three matching embedded copies; V160 replaces
one loose resource and one embedded copy, leaving 25 and two respectively,
plus the separately inventoried CMMNIMG atlas and unclassified artwork. These
are inventory counts, not exhaustive physical-screen clearance.

Final packaging/progress and GitHub commit/push remain campaign work. When the
full goal is complete, make the requested note to revisit older record-based checks.
