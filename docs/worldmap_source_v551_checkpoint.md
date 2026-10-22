# V551 ordinary World Map source and bitmap evidence

The previous turn added4 standalone engine compatibility tests and2 native title
composites. This turn adds an ordinary World Map capture/source checkpoint.
V546 remains unchanged; no ROM, patch, registry, translation, save fixture or
source graphic is edited. All original requirements remain retained.

## Ordinary replay and real residency

The real V546 ROM cold-boots through the existing ordinary36000-frame menu input
schedule. No preloaded battery save, savestate, cheat, RAM injection or diagnostic
ROM is used. The run terminates with exit0. Captures at34800-36000 and read-only
RAM/native state exports are hash-verified. Native serialization does not load a
state and is verified not to change main RAM.

The exact complete156436-byte `/_pxl/seaarea.pxl` is resident at02325520 and its
original owner0231336C has cache tag1A. The earlier ordinary chooser snapshot has
neither the file nor a populated tag. This is residency evidence; the file alone
would not establish the drawn source. The sepia `/_pxl/seamap.pxl` owner02313B8C
is uncached and its exact file is absent in this snapshot. This is bounded to
this observed state, not global unused-data proof.

All8 complete original page-copy calls020474DC run on an isolated copy of the
actual captured cache state without any SDK filesystem bridge. Each19520-byte
packed page, original full return/stack/saved registers and destination guards
pass. The page choices are supplied contracts, not8 live user selections.

## Actual dynamic map and display

The captured direct map header at02279B38 is4-bit,61 row words,160 rows, palette
at+20 and pixels at+52. The actual direct view at02190E3C points to that header
and has244x160 extents. All9674 nonzero indices in its complete packed bitmap
match source page7 at their original coordinates. Every remaining index is0,
producing29366 background-colour pixels. This explains why an unmasked whole-page
comparison was insufficient. No meaning for the mask's creation is invented.

Its palette bytes equal the original blue atlas's first32 bytes. All8 stored
blue banks are identical, so colour equality alone cannot identify a unique bank.
The original source helper copies the first32 bytes; the actual mask-creation and
palette-selection lifecycle still need tracing. The source remains byte-exact to
clean, without an additional Japanese caption to translate.

At native origin6,208,all38759 bitmap-colour pixels match the actual framebuffer.
The remaining281 points are saved individually, not silently removed from proof:

| Component | Pixels | Bitmap-relative bounds |
|---|---:|---|
|Region1|176|122,80 to146,104|
|Region2|105|120,26 to132,38|

These are recorded overlay regions; their source producers have not yet been
independently identified. No icon/speaker/item identity is inferred from their
shape alone. They remain a concrete next display-composition gate.

## Actual VRAM output and rejected assumptions

The complete244x160 lower map crop matches all39040 decoded BGR555 words in
physical VRAM offset60000. The same-size upper crop matches offset40000. Neither
comparison excludes overlay points. Actual BG3 controls are4084, and the mapped
bank registers are retained in the proof.

An initial sub-engine/bankC-to-lower-screen assumption fails every pixel and is
not credited. Pinned DeSmuME source shows POWCNT1 reads engine state and does not
simply mirror the exported9REG bytes. Its raw exported zero must not be treated
as a verified current screen assignment. The positive bank-to-screen pixel
comparisons establish the observed output instead. Source files and their URLs/
hashes are recorded in `core_source/source_receipt.json`, pinned to95b4d79.

Likewise, the map buffer's blank prefix does not prove a blank entire bitmap.
The whole19520-byte comparison supersedes that rejected assumption. This
checkpoint does not claim an unmasked source page, source-exact overlay producer,
all palette/alpha states, all area pages or legacy CMMN/sepia runtime usage.

## Artifacts and scope

- `scripts/verify_worldmap_source_v551.py`; focused Ruff passes.
- `work/analysis/worldmap_source_v551/residency_and_bitmap_proof.json`.
- Captures:`E:/Rota Nova translations/Generated/work/emulation_v193/worldmap_source_v551`.
- Native screenshot and overlay review:
  `E:/Rota Nova translations/Screenshots/Test fixtures/worldmap_source_v551`.

The screenshot is ordinary gameplay evidence, saved with a hash receipt. It is
not marked guide-approved while the overlay producer proof remains open.
All22 historical requirement records are preserved exactly and all18 plaque/hint
entries remain incomplete. The full graphics goal stays active. Continue the
actual mask/overlay producers, original sepia/legacy contexts and other retained
graphics gates. Candidate SHA256 remains
499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
