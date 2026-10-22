# V712/V713: complete Refit explanations and actual bitmap lifetime

## Result and scope

V712 corrects the shared Refit help family: 31 source-reviewed English
paragraphs, generated word wrapping and one consistent left margin. Actual
ordinary navigation verifies 23 complete changed displays covering 13 distinct
messages. All 31 paragraphs separately pass the original native font routine in
the expanded bitmap. These are different scopes; this is not 31 ordinary visits
or a full route playthrough.

The initial status-only goal turn made no implementation progress. This resumed
turn identifies the native crop/field conflict, implements and tests the fix,
rejects two failed experimental candidates, and records the complete result.
The full graphics goal remains active.

## Why the old text disappeared

The original CRemodelCabinInfoView paints into a 168-by-84 bitmap. Three source
strips at rows 0, 12 and 24 appear at screen Y80, Y96 and Y112. Rows 36 through
47 hold the heading; rows 48 through 83 hold three detail rows. A longer English
paragraph could paint correctly in a supplied font test while its fourth line
was not copied to the screen and could overlap those other stored fields.

The revised view uses a 168-by-108 bitmap. The explanation owns source rows 0–59
and appears as one five-row crop at (64,80), using the original font's 12-pixel
line advance. Heading rows 60–71 and all three detail rows 72–107 keep their
original screen positions, complete text and bounds. Authored English contains
no manual indentation or line breaks; the formatter also flushes pending ASCII
pairs before its generated breaks.

The larger pixel buffer uses the original native new/delete routines. Both
parent destructors free it and clear its header pointer. Three descriptors
replace the original five; the two retired, exclusively owned records contain
the scoped cleanup callback. No unowned padding, arena boundary, staged pool,
cache shape or autoload section is expanded.

## Source and integration

The clean-Japanese/canonical-locked manuscript preserves room counts, placement
restrictions, wind effects and stated crew effects. Cabin ID1247 extends the
initial 30-message queue to 31. Spoken shipyard messages1256–1267 are unchanged.

The complete paragraphs fit by repacking only existing COMMON blocks15–17 and
their original directory offsets. All other 3,637 COMMON message strings are
exact. The original warm/cold message-copy tests cover all3,668 IDs. V712 adds
only the owned Refit layout/code spans to that text repack. All675 PXL/FLS
graphics files, all story files and every unrelated ROM component remain exact
to V692. The full470 batches and114 accepted layers remain present.

## Rejected experiments retained

- **V706 is revoked:** its late-pool/allocator-bound growth passes static/native
  checks but fails actual startup/input tests. V692 controls work. Its binary,
  logs and proofs remain; it is not a parent or a release.
- **V707:** the no-growth 30-message repack boots; Cabin was subsequently added.
- **V708:** the full31-message no-growth repack boots and all49 ordinary New Game
  screens match V692. Its actual Refit verifier catches the missing fourth line.
  It is an intermediate investigation build, not the corrected handoff.
- **V709:** read-only tracing finds13 actual help consumers, all using the same
  original 168-by-84 font context and12-pixel metrics. Native font tests alone
  therefore did not prove the screen's three-strip composition.
- **V710 is revoked:** the first expanded layout calls the wrong allocation
  entry02005148. The supplied native allocation bridge hid that mistake. Actual
  screen verification and the V711 trace expose a pixel pointer of0x80 and failed
  Refit behavior. Original failed evidence and DO_NOT_USE markers are retained.
- **V712:** source inspection selects the original new entry02005154; actual ROM
  allocation, drawing and cleanup now pass. No failed ROM supplies parent bytes.

The initial V710 CLI invocation used an unsupported output option and exited
before building. The corrected invocation and its later runtime failure are
separate retained logs. No running producer was edited or restarted after an
observation timeout.

## Actual emulator verification

Two V712 cold boots finish19,700 ordinary Yard frames and31,000 Maria New Game
frames. The latter uses the disclosed existing system-unlock donor, not earned
unlock or claimed route completion. No savestate is loaded. Verification covers:

- All59 complete two-screen Yard images:23 complete new help compositions and36
  unchanged prefix views. Every visible line's leading/final glyph is checked.
- All49 complete title, chooser, story and Hangzhou images against V692.
- All31 complete expanded native font bitmaps and pixel/text guards.
- Four ordinary fleet/fund states, preserving five ships and25,975 funds.
- Exact clean-ROM patch reconstruction and every inherited final build gate.

V713 is a separate20,600-frame ordinary allocation/exit test of the same V712
ROM. A read-only host observer records six complete states: layout entry,
original new, ready bitmap, destructor entry, original delete and cleared
pointer. It sees one9,072-byte allocation at023A97A0, freed once on the explicit
Cancel remodeling confirmation. All59 common whole RGB and4MiB RAM captures
match the unobserved V712 run. CPU, RAM, DTCM and configuration are unchanged by
callbacks; all host slots restore. Original allocator/free code is clean-exact.
Native prefix and bounded-read controls pass.

The final two B presses return to Copenhagen and open its Equipment/Rename
popup. Fleet/funds remain unchanged. This is not a saved-game roundtrip or a
repeated open/close stress test. The complete before/after sheet, actual Topsail
screen and final Copenhagen screen were visually inspected.

## Release and remaining work

- Candidate: `E:/Rota Nova translations/Generated/out/all_routes_combined_v712_candidate.nds`.
- SHA256: `6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030`.
- Profile: `all-routes-unified-v712`; matching manifest and clean-source xdelta
  patch are beside the ROM.
- Canonical parent: `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- This batch changes `/COMMON/MESFILE.DK4` and `/__arm9__.bin` relative to V692;
  the manifest contains the complete canonical diff, all accepted and inherited
  experimental batches, dependency hashes and changed records.
- Patch SHA256: `679af34d2db6d4154cfbfb854d31c1d749b614487b049f60cba1f8ab3db4d8dc`.
- Proofs: `work/analysis/refit_help_v712/` and `refit_help_v713/`.
- Screenshot archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V713 Refit help layout and lifetime`.

Only the latest compiled experimental pointer advances. Canonical acceptance
does not change. All18 original plaque/hint audit objects remain incomplete;
all22 historical requirements remain exact. Plaque wood/restoration review,
ordinary small-control/village/legacy/comic contexts, previously recorded model
gaps and final acceptance remain open. Revisit the older record-based checks
when the full goal is complete, as requested. The four low-resolution Online
screenshot bodies remain excluded and brown comic marks preserved. No guide
promotion, commit or push is made here.
