# Seoul gameplay verification V516

## Route and save provenance

The user-authorized Maria selection bypass was applied to an isolated exact V514
copy. Only ARM9 byte 0x9F068 changed (03A00003 → 03A00004). All graphics and every
other internal file/component stayed exact. Maria began through New Game at
Hangzhou. The earlier Auto Move attempts rejected Seoul and Nagasaki; they are
not credited as visits.

This run sailed with normal D-pad inputs through the original source-mapped
western channel, then east to Seoul. The first northward turn hit the shoreline;
a short move east cleared it. Read-only native ship snapshots record each
correction. The real game offered **Dock at Seoul?** at frame24440. Normal A
entered Seoul, resupplied, visited the Tavern and Inn, rested30 nights
(Jan25 → Feb24, fatigue21 →0), and saved in slot6.

Checkpoint: `E:/Rota Nova translations/Saves/maria-seoul-rested-v514.dsv`.
SHA-256: `942c74828a7b7396f7567ca2d405ddc4cdd329e4837f591777d35ee458794b0f`.
The selection bypass did not set route-completion flags: bits0–3 at the original
persistent progress field are zero after save and both later reload tests.

Two subsequent cold boots use the **ordinary registered V514 ROM**, with the
original 03A00003 instruction intact. Continue loads the saved Maria game
successfully. The whole upper town panel is exact after reload. The second run
visits both facilities again through normal inputs, providing production-ROM
screenshots without the unlock code active. The save's assisted origin remains
explicit; earning Maria's unlock through another completed route is not claimed.

## Current retained art and complete English

- Original Seoul background35 is byte-identical to the clean ROM. Four actual
  Tavern/Inn captures each match all17,440 unobscured pixels at native color
  precision. The exact rectangles exclude the portrait, nameplate and dialog.
  Painting behind those overlays is not counted as visible evidence.
- All five town specialties match complete native font/blank-cell masks in all
  four captures: **Hazelnuts, China, Silk, Silk Cloth, Ginseng**. These are town
  captures, distinct from V515's map previews.
- **Tavern** has complete native glyphs at x64,y244; **Inn** at x64,y264. The
  initial caption search used the wrong tooltip region; the correct positions
  resolve both full masks without changing the ROM or screenshots.
- The actual kbe04/kbe08 icons match all964/1715 nontransparent source pixels
  in both original-voyage and production-reload captures. These are the standard
  facility icons, not the Japanese alternate kbj icons.
- Original background getter returns35 for Seoul town57, facilities0/4/8.
  The source environment retain decision is preserved; its actual native display
  and independent English Tavern/Inn labels now have direct gameplay evidence.

Verifier: `scripts/verify_seoul_v516.py`.
Proof: `work/analysis/maria_asia_v516/seoul_proof.json`.
Reports: `maria_asia_v516_channel`, `maria_asia_v516_reload`,
`maria_asia_v516_production_facilities` under `work/emulation_v193`.
No savestate was loaded; no inventory, supply, condition or position was injected.
Targeted Ruff passes. Screenshots are copied without editing.

## Remaining scope

V514 remains the current experimental registered candidate, SHA-256
`c1416987c757f16c32f90e36c5f31db3f02529f6ceccf8b78cd3b0127f885199`.
This checkpoint adds gameplay evidence; it creates no new playable release and
does not promote the canonical baseline.

Osaka background37 and alternate Tavern/Inn composition in Nagasaki, Osaka and
Naha remain to verify. Other legacy/embedded-art, movie and plaque gates remain
as recorded in the full audit. All22 original requirements and all18 incomplete
plaque/hint entries are retained. The graphics goal is active. Revisit older
record-based checks when the full goal is completed, as requested.
