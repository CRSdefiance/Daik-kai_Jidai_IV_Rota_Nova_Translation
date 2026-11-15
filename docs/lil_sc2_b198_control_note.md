# Lil SC2 B198 namahage dream control note

All 15 B198 records are translated from the clean Japanese source. Yukihisa
hears a namahage demand to know whether he has been naughty, wakes from the
dream, finds a mysterious object, and plans to give it to the admiral. Angelo
reacts to the discovery.

The `FE` namahage, `0C` Yukihisa, and `0F` Angelo presentation states are
preserved. Fixed-byte limits require short natural renderings such as `Who?!`
and `Dream?`. English prose avoids literal uppercase `I` and `F`, which are
unsafe renderer bytes.

All 15 records pass the fixed-byte, speaker, wrap, pair-phase, and first-glyph
audit. Both exact-font contact sheets were visually reviewed, including all
repeated namahage prompts and the final line. Direct saved-ROM verification
confirms every insertion. Runtime cold-boot remains necessary to check the
dream sequence, object event, portraits, nameplates, and first letters.
