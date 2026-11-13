# Translation DS cumulative promotion candidate

Testing ROM: `out\promotion_ready_20261110_v4\Translation_DS_All_Routes_20261110_v4_candidate.nds`, with its adjacent manifest.

This fresh clean-input reconstruction is byte-identical to the latest registered Lil269 cumulative candidate. It includes all 727 registered entries and 114 accepted layers: prior Rafael/tutorial localization, storyline/shared dialogue, Market Trade-screen correction, name/glyph fixes and ASCII right bounds. It adds no new internal ROM changes.

Apply `translation.xdelta` to the clean Japanese ROM SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. Expected output SHA-256: `9c4a1a0e6de61b7a0ca881006af9e30c186c99eb51da2465d36d2e2acc3d580c`. Patch SHA-256: `b40b722182e542bfb9c212bfee3c53a97a14f7c6db66f5edc3489cfc37dd2cbc`. The new copy matches the registered candidate byte for byte. Build-time manifest and registry are included as lossless gzip files.

All 62 registered release checks remain bound to the exact ROM. All 27 fresh repository tests pass with no failures, errors or skips. Existing candidate-owned startup, protected-name getter, native-page and representative gameplay evidence is reused; this packaging step adds no gameplay or hardware coverage. See REGISTERED_RELEASE_NOTES.md for observed versus offline-only coverage and unvisited conditions.

The next Lil361 B283–B298 source intake remains unfinished and excluded. Its clean-source packet and exact references are preserved in Git; no new prose or review credit is shipped. Integrated editorial reviews remain 24,744. The full editorial goal stays active.

Cold-boot this exact filename and test title/New Game, Rafael/tutorial, town/Market Trade, names, wrapping, pagination and transitions. Main remains V4701 pending your explicit acceptance. Earlier ROMs and translations are preserved. Raw ROMs remain local; this clean-input patch is committed to GitHub. Run `git lfs pull` after cloning for the coverage ledger.
