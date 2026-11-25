# V537 original movie paths (production V534 unchanged)

The original startup path plays M28. The original ending selector at 02040BF4
reads the active captain through 0207F244, adds 29, and calls 020D2B1C. This
selects M29 for Rafael, M30 for Hodram, M31 for Lil, and M32 for Maria. M28 is
the startup movie, rather than a captain ending. Its native caller at 0207D694
passes different setup arguments from the four ending selections.

## Original startup playback

The production V534 ROM cold boots for 10,000 frames without controller input,
battery-save preload, savestate, cheats, or movie-file substitution. Captures
every four frames cover two observed playback cycles. Both translated title
planes and all 19 distinct progressive name states match complete original
texture ink and shadows at native five-bit color precision. All 22 edited M28
textures receive visible evidence. Textures 30/31 have identical pixels, so
this does not distinguish their actual GPU bindings.

The reveal is credited from the largest complete matching state at each
capture, preventing a later complete name from being credited as its earlier
prefixes. Full leading and trailing letters are included. Remaining transparent
composition and every intermediate transition are not cleared by these masks.

## Original captain-ending paths with synthetic setup

An opt-in fixture changes only the temporary gameplay state at 022796BC from
1 to 4. In each successful application, exactly one byte changes. The original
ending-state branch at 0203E294 then selects the active captain's original
movie. All five relevant original code ranges remain byte-identical to the
clean ROM. The helper separately executes the original selector with explicit
teardown/playback contracts to verify its arguments and preserved-register ABI;
the actual playback evidence comes from DeSmuME, using the production ROM.

This exercise infers the original ending branch from its guarded state field,
unchanged code and observed captain-specific movie. It is not an instruction
trace of the running core or earned route completion. M29–M32 remain byte-exact
to the clean game; no replacement movie slot is used.

Rafael and Maria use verified disposable copies of existing test saves. Hodram
uses a copied Athens donor. Lil starts a fresh game with recorded ordinary
inputs. An empty historical Lil donor actually opened a Rafael New Game and
was correctly rejected by the active-captain guard. Its failed attempt receives
no ending display credit. Another Lil attempt applied the state while dialogue
was waiting for input; that field remained pending. The successful run advances
the remaining dialogue using ordinary A presses before M31 starts.

Full upper-screen image matches and complete "Save the ending data?" masks
are recorded per captain in the proof. Each full image comparison includes
49,152 pixels. These are sampled scene matches, not every movie frame or every
texture. Original donor saves and separate source copies are hash-checked after
exit. Synthetic screenshots stay in the test-fixture archive, and the normal
guide archiver rejects ending fixtures. No cheat enters the translation patch.

## Artifacts and remaining work

- Fixture: `scripts/native_ending_fixture_v537.py`.
- Capture frontend: `scripts/headless_desmume_v193.py --allow-ending-fixtures`.
- Verifier: `scripts/verify_original_movie_v537.py`.
- Proof and save provenance: `work/analysis/ending_caller_v537/`.
- Native captures: `E:/Rota Nova translations/Generated/work/emulation_v193/`.
- Selected labeled captures: `E:/Rota Nova translations/Screenshots/Test fixtures/original_movies_v537`.

No V537 ROM is built. Experimental production remains V534, SHA-256
`cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45`.
Canonical remains unchanged. All 22 original requirements and all 18 incomplete
plaque/hint entries are retained. Raw legacy artwork consumers, restoration,
other contexts, normal earned endings and hardware verification remain open.
The graphics goal remains active. Revisit older record-based checks at full
goal completion.
