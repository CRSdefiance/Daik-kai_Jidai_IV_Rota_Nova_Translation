# V190 Online banner overlap correction and emulator verification

2026-10-05. Graphics goal active/incomplete. A new headless DeSmuME frontend
cold-boots the actual ROM and captures its software-rendered framebuffer through
the libretro API. The viewer's existing title banner obscured part of V189's
Profile/Quest Info screenshot headers. V190 moves the intact title canvas and
border to the bottom screen, above the promotional description.

Only two Online-specific draw-destination instructions change (four ARM9 bytes).
The constructor/visibility state, local coordinates, 256×192 canvas, font, border,
palettes, all screenshot/description artwork, earlier wording and other runtime
code remain preserved. All 13 pages use the corrected placement.

## Required handoff

- Candidate: `out/all_routes_combined_v190_candidate.nds`.
- SHA-256: `9ccff57aec0326722b89b85877fb5be23e63dc466022b1f7c2e0a984ccdd9424`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`.
- Canonical SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v190`; **experimental**, no user acceptance or canonical promotion.
- Accepted layers: baked into canonical base; 0 additional accepted batches.
- Experimental batches: all 465 V189 batches, all prior record IDs and terminal stages,
  plus `online_title_banner_release` as the new scoped terminal stage.
- Changed versus V189: `/__arm9__.bin` only, offsets `1058D4`, `105904`, `105906`, `105907`.
- All 36 changed paths versus canonical are listed in the neighboring manifest.
- ARM9 SHA-256: `9c03e253a6e91231a7e6d7ee112c07c632a3cfe16b2a33d2d349cc1e45857958`.
- Patch: `out/all_routes_combined_v190_candidate.xdelta`.
- Patch SHA-256: `0f6af906d148cfe10e0f6aefb143a39f3853671f96bfecdf37b4c0d52c7b6bd2`.
- Clean patch base: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Verification: full byte-exact V189 reproduction after builder change, complete
  manifest/batch/record/stage inheritance, four-byte code diff, golden menus,
  exact clean-ROM patch reconstruction, native emulator rendering/input and Ruff.
- Cold-boot areas reviewed in the emulator: opening/Press START, main menu,
  New Game/Lil selection and confirmation, Amsterdam and opening dialogue,
  Extras/Online categories and all 13 Online pages/image cycles. No savestate loaded.
- User/device review remains: changed Online layout, title/movie graphics and
  representative gameplay on the intended emulator/device. This is not a physical
  hardware test or approval to replace the canonical baseline.

## Rendered verification scope

Core: DeSmuME `git95b4d79`, official Windows x64 libretro build, interpreter,
one CPU core, software rendering at native 256×192 per screen, no frameskip.
DLL SHA-256: `42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b`.
Download provenance and official API references are saved in `work/emulation_v193`.
See [core documentation](https://docs.libretro.com/library/desmume/) and the
[official build collection](https://buildbot.libretro.com/nightly/windows/x86_64/latest/).
V193 names this emulator research; it is not a later ROM candidate.

The frontend loads the exact ROM normally, supplies scripted controller input
and copies returned framebuffer pixels. It does not replace filesystem reads,
inject game memory, load savestates or force menu/unlock flags. Optional RAM dumps
are read-only exports. A missing log callback caused the first core initialization
attempt to fail before ROM loading; supplying the required callback resolved it.

For all 23 actual Online screenshot resources, the complete 256×192 top screen
matches the candidate artwork after conversion to native five-bit RGB. No pixel
region is excluded and no error tolerance is used. This proves full visible
artwork, including complete header glyphs, without the earlier title occlusion.
For all 13 promotional cards, every nontransparent source-index pixel matches
the bottom-screen capture. All cards and relocated title borders/wording were
visually reviewed on the complete page sheet. The Profile banner interior also
matches its former native pixels exactly at its new screen location.

V190's sampled Lil confirmation, captain fields/nameplates, Amsterdam background
and opening dialogue show complete leading letters and ordinary wrapping. These
samples are representative scene evidence, not exhaustive route-text verification.
The biography uses Camille while dialogue/nameplates use Kamil; naming/source
consistency remains a separate fidelity audit item. Do not infer full movie/name-card,
deep-route, gallery, contextual-art, physical touch or hardware clearance from these
samples.

## Artifacts and remaining work

- `dk4tool/patch/online_title_banner_release.py`.
- `translations/online_title_banner_release_v1.json`.
- `scripts/headless_desmume_v193.py`, `verify_online_banner_v190.py`.
- `work/analysis/online_banner_v190_saved_proof.json`.
- `work/analysis/v190_online_pixel_matches.json`, `v190_online_caption_pixel_matches.json`.
- `work/emulation_v193/online_banner_comparison.png`.
- `work/emulation_v193/v190_all_online/page_review.png` and complete input/capture reports.
- `work/emulation_v193/v190_lil_scene/capture_report.json`.
- `work/analysis/v189_online_banner_builder_reproduction.nds` (exact V189).
- `work/analysis/online_banner_v190_patch_reconstruction.nds` (exact V190).

Four Online screenshot body/dialogue/chat translations, eleven unresolved ILNK
storage blocks, other formats/source fidelity and broader native/gameplay gates
remain. Keep the requested older record-based-check follow-up for full-goal
completion. The full graphics goal is not complete.
