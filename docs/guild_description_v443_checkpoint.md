# V443 Guild treasure descriptions

Status: experimental. All 22 historical requirements and all 18 plaque entries
remain in the audit; the full graphics goal is still active.

## Source and repair

Normal New Game Guild navigation exposed COMMON 3665 splitting `Some s` / `ay`.
Clean Japanese describes a rumored twisted horn, possibly a dragon's, that becomes
medicine effective against any illness. The reviewed English is: "They call this
a twisted horn. Some say it's a dragon's and that it can become medicine for any
illness." Source, context and five localization gates are in
`translations/guild_description_manuscript_v1.json`.

The portrait wrapper covers all 20 treasure descriptions (3648–3667). Only this
family uses 36 continuation cells; equipment, rumor and clue behavior retains 37.
The 48-byte selector occupies verified zero padding at 01FFCB40, with its declared
call at 01FFCAB0. All other first3900 ITCM bytes, main pool and arena bounds are
preserved. SDK section 4 is exactly4096 bytes; no growth remains in that section.

## Evidence

- All20 native renders preserve glyph order, ink and whole-word rows.
- All40 cold/warm COMMON copies pass guards and ABI checks.
- All42 existing rumor/clue/equipment/boundary/wrong-parent cases remain exact.
- Only3665 changes prose; all3668 offsets/cache sizes and other messages are stable.
- Actual New Game Guild offer has all995 glyph pixels and blank cells exact;
  all3 rows begin at x22. The captured screen was visually reviewed.
- All56 comparable title/New Game/story/town frames are pixel exact, as is the
  normally purchased Ancient Map view.
- The clean-ROM patch reconstructs the candidate byte for byte.

This is targeted automated DeSmuME testing, not hardware testing or a complete
playthrough. The other19 descriptions have native renderer tests rather than
actual gameplay captures. No canonical promotion is made.

## Handoff

Candidate: `all_routes_combined_v443_candidate.nds`

SHA-256: `832258728fdd37d7732e24a031515c602ab4dbe19e7fba98ace76ab0103c20aa`

Profile: `all-routes-unified-v443`. All470 inherited batches and all prior V440
stages are retained, plus `translations/guild_description_wrap_v1.json`.
Relative to V440, only `/COMMON/MESFILE.DK4` and `/__arm9__.bin` change.
Canonical base remains `raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.

Verifiers: `verify_guild_description_v442.py`,
`verify_guild_description_release_v443.py`, `verify_guild_description_live_v443.py`.
Proof: `work/analysis/guild_description_release_v443/release_proof.json`.

User cold-boot testing should cover title, New Game, established opening, town UI
and Guild map offers. Files and finalized guide screenshot are published to
`E:\Rota Nova translations`. All plaques remain under audit. Revisit older
record-based checks after the full graphics goal is complete.
