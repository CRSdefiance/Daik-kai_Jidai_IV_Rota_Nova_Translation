# Combined V211: embedded START/touch prompt synchronized

2026-10-07. **Experimental; no promotion or full graphics-goal completion.**

## Source discovery and localization

The raw DSOBJR file contains a separate sub-screen sprite payload with the complete
Japanese instruction: `スタートボタンを押すか、下の画面をタッチしてください`.
It asks the player to press START or touch the lower screen. The visible title02
PXL was already translated, while this embedded copy remained Japanese.

V211 reuses the accepted English artwork and wording:

> Press START or
> touch the screen

This keeps both controls explicit and uses the established DS touch-screen wording.
No new font, palette quantization or approximate background restoration is used.

The initial whole-file 4bpp diagnostic was not a valid whole-image layout. Native
startup code reads 5,408 prefix bytes into the main sprite transfer, then seeks to
`1720` and reads the 4,096-byte sub-screen payload. That payload comprises four
consecutive 64×32 banks, assembled side by side as 256×32. The source prompt becomes
fully legible in that arrangement. The intervening 512-byte segment and all prefix
bytes remain untouched; index-only diagnostics do not establish their color roles.

## Registered integration

| Artifact | Identity |
|---|---|
| Candidate | `out/all_routes_combined_v211_candidate.nds` |
| SHA-256 | `d6cd1ecc3702d75a9f0c9e6e89a84501dbde8eb5fcaa9c6af82154716a8d5ae1` |
| Profile | `all-routes-unified-v211` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Prior candidate | complete registered V205 |
| Active batches | 467; all 466 V205 batches and prior terminal stages retained |
| Baked accepted layers | all 114 retained through the canonical base |
| Only changed path versus V205 | `/GRP/DSOBJR.DK4` |
| Patch | `out/all_routes_combined_v211_candidate.xdelta` |
| Patch SHA-256 | `25e047aa6dd8d3d89ad9762c9ed2051aa1ab2d94956251b7c78f0998c320b4d8` |

ARM9, ARM7 and every other ROM file remain byte-identical to V205. The banked-sync
adapter is separate from the revoked Common full-strip importer. It checks the
entire source, reference and owned-region hashes, integer/alignment/range limits,
dimensions and allowed palette indices. Five malformed inputs are rejected.

The new adapter reproduces V205 exactly before compiling V211. The registered
manifest names the full stack, canonical base and changed record. The patch
reconstructs V211 exactly from clean SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

## Pixel, loading and cold-boot evidence

- All 7,424 accepted PXL indices are copied exactly into the banked payload.
  The three extra rows are 768 transparent-zero padding indices. All 5,920 bytes
  outside the owned payload, including the palette segment, remain exact.
- Every leading/trailing letter, blank pixel and foreground index is retained:
  445 foreground pixels, source bounds `(81,3)–(174,26)`.
- Original startup open/read/seek/read/close spans load both the complete main
  prefix and the English sub-screen payload with exact bytes and guards. Their
  preceding buffer/stack context is explicit; graphics/DMA transfers between
  these spans are not executed by the filesystem probe.
- A fresh no-input 6,000-frame cold boot displays the English instruction. All
  8,192 prompt/background pixels match native five-bit RGB at origin `(0,312)`.
  Complete first/last letters and visible bounds pass.
- A separate fresh 14,900-frame run reaches the title menu, New Game selection,
  established Rafael-route dialogue and Lisbon town UI. These screens were
  visually reviewed; no savestate or emulator-memory injection is used.

The framebuffer match establishes the displayed English prompt; by itself it
does not distinguish PXL drawing from the raw copy. The independent native file
read proves that the embedded copy now contains the same complete English art.
No global hardware, every-state or all-graphics clearance is inferred.

## Artifacts and remaining work

Batch: `translations/objr_start_prompt_embedded_sync_v1.json`.
Adapter: `dk4tool/graphics/obj_banked_sync.py`.
Preparation/verifier: `scripts/prepare_objr_prompt_v211.py`,
`scripts/verify_objr_prompt_v211.py`.
Evidence: `work/analysis/objr_prompt_v211/saved_proof.json`, preparation, exact
prior reproduction, build logs and clean-patch reconstruction.
Cold boots: `work/emulation_v193/objr_prompt_v211/title/` and `town/`.

Focused Ruff passes. Four Online screenshot bodies, chosen-name consistency,
remaining raw/embedded/contextual consumers, the market indicators and broader
native/gameplay checks remain open. The goal stays active. Revisit older
record-based checks at eventual completion, as requested. Human acceptance of
this candidate is still pending.
