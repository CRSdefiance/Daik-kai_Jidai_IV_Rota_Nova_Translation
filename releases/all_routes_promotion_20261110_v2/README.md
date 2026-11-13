# Translation DS cumulative promotion candidate — November 10, 2026

Local testing ROM: `out\promotion_ready_20261110_v2\Translation_DS_All_Routes_20261110_v2_candidate.nds` with its adjacent `.manifest.json`.
This is a fresh clean-input reconstruction, byte-identical to the latest registered Lil382 cumulative release. It adds no new internal ROM changes. All 726 registered entries and 114 accepted layers are included, preserving Rafael/tutorial localization, earlier storyline/shared work, Market Trade-screen correction, name fixes and the registered ASCII right-bound correction.

Apply `translation.xdelta` to the clean Japanese ROM SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. Expected output SHA-256: `545a2aed763129baeaa5fe625ca29cd1a818bc585dc308cecb5f6958009e9b0f`. Patch SHA-256: `944d5a25b6e8edb1225fb1bd5ba1b3efa62996b52c520cf897009e3ba52286a3`. The new testing copy was compared byte for byte with the registered candidate. No historical work folders are required to apply the patch. Exact build-time manifest and release registry are included as gzip files.

Fresh repository checks: 27 passed, no failures, errors or skips. All 61 registered release checks remain bound to these exact bytes. Existing emulator evidence includes the candidate's own Maria/Hangzhou cold boot, 24 protected name getters and representative Lil dialogue/menu/page transitions. This packaging step adds no gameplay or hardware coverage. Detailed observed versus offline-only coverage is in PRIOR_Lil382_RELEASE_NOTES.md and verification/.

The next 269 Lil B243–B282 reviews are preserved in Git as unfinished work and are excluded from this ROM. Their four prose gates pass; full display/storage/gameplay/release gates do not. A native FE panel complete-consumption failure remains under investigation. No pending proposal is credited or shipped.

Cold-boot this exact filename and test title/New Game, Rafael's opening/tutorial, town/Market Trade, dialogue names, wrapping and transitions. Main remains V4701 until explicit user acceptance. The integrated count is 24,475; the full editorial goal remains active. Older ROMs, translations, justified retentions and evidence remain preserved.

After cloning, run `git lfs pull` for the coverage ledger. Raw ROMs are local; the clean-input patch is committed to GitHub.
