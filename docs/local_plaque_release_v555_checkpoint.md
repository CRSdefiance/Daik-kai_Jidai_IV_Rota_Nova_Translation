# V555 integrated original plaque margins

The previous goal turn made progress: local source texture prototypes identified
and rejected faint Japanese glyph-shaped seams. V555 integrates the conservative
alternative through the complete registered release stack.

## Release identity

- Experimental candidate: `out/all_routes_combined_v555_candidate.nds`.
- Actual E location: `E:/Rota Nova translations/Generated/out/all_routes_combined_v555_candidate.nds`.
- Candidate SHA256: `8d64339a6376e713526b78e1279f88c2db3ecd0648171aaad7a17511f5b50654`.
- Canonical build base: `out/raphael_natural_v2_accepted_base.nds`.
- Base SHA256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Registered profile: `all-routes-unified-v555`.
- All114 accepted layers and470 inherited batches retained. The additional
  source-margin stage is `translations/local_plaque_texture_v1.json`.
- Manifest: `out/all_routes_combined_v555_candidate.manifest.json`.
- Clean-ROM patch: `out/all_routes_combined_v555_candidate.xdelta`.
- Patch SHA256: `090248356e24c707d143bb4e35df74f3881b8b409fda34108010cb92c62a3c4d`.
- Patch input is `work/clean.nds`, SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- No canonical promotion or human acceptance is claimed.

## Exact change and preservation

Relative to V546 only `/_pxl/dividecrewinfo.pxl` and `/_pxl/personinfo.pxl`
change. The source-locked stage restores208 crew-atlas and216 person-atlas
material pixels,424 total across10 changed plaques among11 reviewed wooden
source regions. Level already matches at all selected margin points and receives
no change. The six intentionally redesigned stat plaques are unchanged.

Each changed point retains its original Japanese atlas colour at the same
coordinate, lies inside the reviewed source/localized interior, and stays
outside the protected Japanese text reconstruction band. No English ink,
existing bevel, header, palette, geometry or unrelated pixel is changed.
Protected text areas retain the fine source grain already integrated in V542;
concealed texture is reconstruction, not recovered original information.

All ARM9/ARM7 code, heap/startup/cache geometry, dialogue and other translated
artwork remain byte-exact to V546. The prior921-entry graphics preservation
proof is bound to the exact V546 parent; unchanged files retain that evidence
and the two revised PXLs retain their headers/palettes/extents.

## Verification

- `scripts/build_integrated_release.py --profile all-routes-unified-v555
  --out out/all_routes_combined_v555_candidate.nds`.
- `scripts/verify_local_plaque_release_v555.py --static-only` and full verifier.
- All17 independent full font masks pass, including first/final letters.
-61 whole native plaque crops pass across three Assign Sailors and four Sailor
  Info frames, including background, borders and complete English lettering.
-56 unique startup regression frames remain byte-identical to V546;57 capture
  records include the duplicate final frame. Same input schedule and core options.
- Exact reconstruction from the clean-ROM xdelta patch matches the entire ROM.
- Ruff passes for the new source-margin module and verifier.

Cold-boot tests use the existing DeSmuME libretro core with no loaded savestate,
preloaded battery save, synthetic inventory/location, or production cheats.
The first fresh-run command omitted the schedule's required touchscreen option
and failed argument validation before boot. It received no testing credit; the
corrected run completed21200 frames. All three emulator handles finished exit0.

Actual screenshots were visually reviewed for readable text and residual Japanese
texture ghosts. They show no ghosts from the rejected per-pixel prototype.
These selected emulator scenes do not prove hardware behavior or a full route.

## Artifacts and remaining review

- `work/analysis/local_plaque_release_v555/release_proof.json`.
- `stage_proof.json`, static proof, navigation schedules and exact reconstruction.
- `E:/Rota Nova translations/Generated/work/emulation_v193/local_plaque_v555_crew`.
- Corresponding `_person` and `_fresh` capture folders.
- `E:/Rota Nova translations/Screenshots/Guide candidates/V555 plaques` holds
  reviewed Assign Sailors/Sailor Info screenshots with a provenance receipt.
  Guide publication is not approved and the global plaque audit is not closed.

User cold-boot review areas: title menu, New Game/character selection, established
story/town screens, Assign Sailors and Sailor Info. The automatic ordinary replay
provides targeted evidence for these changed plaques and startup regressions.
All18 plaque/hint entries remain incomplete under the user's instruction; broader
family/style/context review remains open. All22 historical requirements retain
their exact scope. Other graphics/native consumers and gameplay gates remain
open. The full graphics goal remains active.
