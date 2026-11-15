# Combined V161: name-entry plaques and treasure header

V161 is the latest **experimental** combined candidate. It adds six complete
English labels in three resources and preserves the V160 button prompt. The full
translation goal remains incomplete. No canonical promotion, commit or push is
claimed.

## What changed

The alternate name-entry atlas `/_pxl/slackimg12.pxl` and matching embedded
`/GRP/SLACKIMG.DK4` block 12 now contain all five labels:

| Japanese source | English | Meaning/context |
| --- | --- | --- |
| 名 | Name | Given name. |
| ミドルネーム | Middle | Middle name. |
| 姓 | Last | Surname. |
| 勢力名 | Company | Merchant organization/faction name; consistent with captain selection. |
| 誕生日 | Birth | Date of birth; consistent with captain selection. |

`/_pxl/mysterymap/mys_hunt_d.pxl` now displays **Treasure Name** for **秘宝名**.
Both words are retained. It is a complete natural English heading.

The plaques use the original compact five-pixel English advance. The font's two
blank top rows are verified empty for every character before they are trimmed;
all nine visible rows remain. The compiler centers them inside each plaque's
nine-row lettering interior. Its glyph checks reject trimming any visible pixel.
The same normal capitalization and every original glyph shape are preserved.
All top/bottom chrome, curved side borders, headers, palettes, dimensions and
pixel extents remain exact. Only the old baked lettering interiors are reconstructed.
The treasure header uses the original six-pixel advance and dark source palette.
All six list rows, borders and artwork outside its owned header rectangle remain
exact. Both loose and embedded plaque previews and the complete treasure panel
were visually reviewed.

Preview: `work/qa/name_treasure_graphics_v161/review.png`.
Full panel: `work/qa/name_treasure_graphics_v161/treasure_full_english.png`.
Source/prose/storage: `work/analysis/name_treasure_graphics_v161_artwork.json`.

## Defect caught before final packaging

Initial normal-case and uppercase research trials placed font pixels on the
plaque's bottom border. Changing capitalization did not fix the complete font
extent. The final correction removes only two proven blank rows and places
every visible row inside the original lettering area. The exact border regression
now passes. Neither failed trial was handed off or promoted; preserved research
files are `work/analysis/v161_plaque_border_trial.nds` and
`work/analysis/v161_uppercase_border_trial.nds`. Do not use them as release parents.

The earlier builder permitted one image sync per archive. It now merges separately
source-locked **disjoint blocks**, rejects overlapping ownership and duplicate
record IDs, and processes translated PXL inputs before archive synchronization.
Both block 20's earlier button prompt and block 12's new plaques use the original
canonical archive as their source. No batch is rebased onto a derived archive.
The final builder reconstructs V160 byte-for-byte, proving compatibility for
the existing complete stack.

## Verification and limits

22 focused graphics tests pass: six complete native label rasters and missing-first-
letter rejection, nine scoped image-size cases, blank-row trim rejection, exact
plaque chrome and treasure-list preservation, disjoint atlas merging, retained
button prompt, input dependency ordering and complete profile inheritance.
New implementation/test files and the builder pass Ruff.

Every label executes the unmodified native font lookup and paletted glyph
primitive with complete glyph cells, saved registers, stack and image canaries.
The scratch canvas has two padding rows so its full eleven-row font cells are
safe; complete visible output translates back to the exact asset coordinates.
This checks every character, including the first and final letters, rather than
only string length or allocation. The eight-bit treasure texture's glyph shapes
are verified in the native four-bit scratch canvas; its eight-bit pixel packing
and original palette are checked separately.

The native atlas-size/view path passes for name selectors 12–19 with their exact
shared resource table entry, and for the 256×192 treasure header supplied as a
controlled input. Loaded PXL resource class/header values remain input contracts.
The treasure selector table is also controlled; it does not prove the treasure's
live consumer. Actual file loading, live atlas crops, complete widget/GPU
composition, alpha/palette presentation, keys and physical gameplay remain
unverified. Native text/size evidence is
`work/analysis/name_treasure_graphics_v161_native.json`.

Saved-ROM verification proves all other V160 components and resources exact,
including ARM9, COMMON/HELP, all four routes and the previous button prompt.
Every inherited terminal/relocation stage and changed record is preserved.
Only the new embedded plaque record is appended to the existing archive's lineage.
Canonical menu/graphics invariants and exact clean-ROM patch reconstruction pass.
Earlier text matrices retain their original hashes; no rerun of those matrices
is claimed. Saved proof: `work/analysis/name_treasure_v161_saved_proof.json`.

## Candidate and lineage

| Artifact | SHA-256 |
| --- | --- |
| Canonical base: `out/raphael_natural_v2_accepted_base.nds` | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch base: `work/clean.nds` | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| V160 comparison | `8a2cd62835ac2b5ecc3e176877fcaf2f08f45f119dff1fd64006d634a09b40e6` |
| V161: `out/all_routes_combined_v161_candidate.nds` | `a3cf17dd8b434c5c93af39c89fe3623da3f00832a03a59f5993d4aa9126b4835` |
| ARM9, exact V160/V159 | `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf` |
| Registry at V161 build | `eaaa9a674f0088ee4666fb213a7cd9c840f895917792abd47b547bc6e62d530f` |
| V161 patch: 763680 bytes | `54abb07d670edd01491d06bb35c6d84f35bbce4b03404756aa5401f4cfc804b9` |

Profile: `all-routes-unified-v161`, experimental. All 437 V160 batches and terminal
stages remain; three additional source-locked batches bring the total to **440**:
`translations/name_entry_plaques_graphics_v1.json`,
`translations/treasure_name_header_graphics_v1.json` and
`translations/name_entry_plaques_embedded_sync_v1.json`.
All accepted layers are baked into the canonical baseline; zero additional
accepted batches are required. The adjacent `.manifest.json` records every
batch, changed record/path, inherited stage and build check.

Compared with V160, only these internal paths differ:
`/GRP/SLACKIMG.DK4`, `/_pxl/slackimg12.pxl` and
`/_pxl/mysterymap/mys_hunt_d.pxl`.

Compared with the canonical baseline, thirteen internal paths differ:
`/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`, `/GRP/SLACKIMG.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`,
`/_pxl/mysterymap/mys_hunt_d.pxl`, `/_pxl/personinfo.pxl`,
`/_pxl/slackimg12.pxl`, `/_pxl/slackimg20.pxl`,
`/data/SC0.DK4`, `/data/SC1.DK4`, `/data/SC2.DK4` and `/data/SC3.DK4`.

Before acceptance, cold-boot without a savestate and test the title, New Game
captain selection/name entry, an established story, town UI, inherited changed
item/Advice/Gallery screens, the treasure list, the alternate plaque atlas in
each actual display context, and the shared button prompt. Full visibility,
palette/alpha and controller behavior need physical verification. Finding all
alternate atlas contexts and proving actual load/crops remain mapping tasks.
Explicit user acceptance is required before canonical promotion.

## Full goal remaining

245 COMMON selections / 133 physical owners still need actual consumer/layout
integration. Other ARM9/UI, names/source fidelity, Reports/Sailing Help
persistence, BGM physical audio/input, downloaded items and complete gameplay
checks remain. The known graphics inventory now has **23** other confirmed
Japanese loose/FLS resources, **one** remaining matching embedded title copy,
the separate CMMNIMG atlas and unclassified artwork. These counts describe the
historical inventory after these edits; they do not clear every physical screen.
Final packaging/progress and GitHub commit/push remain campaign tasks. On full
goal completion, retain the requested note to revisit older record-based checks.
