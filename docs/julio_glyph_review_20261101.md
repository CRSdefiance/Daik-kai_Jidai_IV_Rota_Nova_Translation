# Julio's mismatched F: confirmed cause and tested correction

The current registered Lisbon/Guild-fixed ROM still selects full-width F and I
for Julio's captain explanation, SC0 B43 R17. The user's hardware photo is direct
evidence of the visible mismatch; it does not identify which ROM was photographed.
This investigation independently confirms the same text in the current candidate.

The historical `safe_literal_markup` helper in
`scripts/revalidate_name_migration_v276.py` replaced literal capital F/I with
full-width Latin to avoid reserved macro prefixes. That frozen producer remains
unchanged. The later `native-guard-v255` policy supports ordinary literal letters
while rejecting actual macro collisions. Blind Unicode normalization is unsafe.

The proposed correction retains the established English exactly. The complete
clean B43 personnel tutorial was read for context: captain, sail handlers,
helmsman, adjutant, surveyor, lookout and the Deck instruction. Julio is explaining
why a ship needs a captain; there is no new rule about Rafael leaving the ship.
The wording remains natural explanatory dialogue and adds no rank or relationship.
The change removes only unintended wide Latin glyphs and regenerates protected,
pair-safe automatic breaks. The resulting record retains its 113-byte allocation,
speaker06, FI substitution and four native rows. It is a formatting revisit with
zero new editorial completion credit.

Evidence: `work/analysis/julio_glyph_review_20261101_v3/report.json` and its
`comparison.png`. The report pins the candidate/manifest/ARM9, source/current and
proposed bytes, formatter profile, diagnostics and individual glyph events.

- Eight original current native lookups (whole/body, four alignments) select the
  exact legacy target. This catches the effective catalogue text that a scan of
  stored SC0 alone misses.
- Three literal-only native macro-parser cases retain normal F/I unchanged.
  These tests deliberately do not construct a captain or claim actual FI expansion.
- Both current and proposed native 216x64 pages match independent font pixels,
  complete glyph order, bounds and canaries. The comparison sheet was directly
  viewed: the proposed F/I match the surrounding font; no missing letter or extra
  row appears. Default Rafael expansion is host-supplied for this render test.
- Existing literal-prefix and ASCII-guard regressions: 23 passed. The sole
  line-break-count warning compares the old stored one-break draft with the
  three-break proposal. The clean Japanese and proposed English each use four
  rows; this specific difference is justified, with no authored positioned break.
- The broad scan flags 33 stored entries and 109 resident historical catalogue
  entries. These may overlap and are review candidates, not 142 proven defects.
  Other catalogue selections, intended fixed-width text and decoded-source
  coverage require individual classification; no global replacement is approved.

Two initial audit-tool failures are preserved with their producers and diagnosis
in the earlier evidence folders: the first oracle reserved blank cells incorrectly;
the second census decoded an actor control as CP932. They are checker errors,
not game defects. The successful reusable checker separates speech controls from
text and preserves the original native checks.

No ROM, release registry, canonical parent or completion count changed. Actual
FI substitution, progressive gameplay and registered cumulative integration of
this correction remain pending. Keep the existing ASCII right-bound runtime fix.

Continuation: finish this small confirmed correction alongside the pending Hodram
batch. Its already-reviewed full-width I retentions now need the same focused
glyph-consistency check; retain the prose and all unaffected completed evidence.
Do not restart all 224 records. Broader candidate classification can be grouped
with subsequent complete-exchange editorial batches.
