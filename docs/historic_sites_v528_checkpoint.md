# V528: complete shared historic-site names

## Source and localization

The previous survey discovered all 21 shared historic-site names still in
Japanese. V528 implements their clean-source English review, including Poitiers
Cathedral, Santa Maria Maggiore Basilica, Forbidden City, Tomb of King Muryeong,
Kinkakuji Temple, and Pyramids of the Sun and Moon. Names remain complete and
faithful to the game's site identities. Standard proper names such as Taj Mahal
and Parthenon do not need redundant English suffixes.

Original virtual name method `0x02087444` obtains its site index through
`0x02087460`, then metadata getter `0x020CD56C`, then the pointer table at
`0x0211BC1C`. Only those 21 original pointer owners and source-owned text spans
change. All 21 native getters return the complete English bytes with preserved
saved registers, including unaligned C-string addresses. Broader gameplay and
shared prose/macro contexts remain under audit.

## V527 rejected; allocation preserved in V528

V527 attempted to append these names to the inherited cached pool. Actual cold
boot showed a black upper screen and the persistent START prompt. It is revoked,
has zero credited site displays, and was not published or promoted. Actual RAM
shows the entire inherited/new pool copied correctly. Controlled boots establish:

- Inert section growth with original startup/allocator behavior boots normally.
- Pool growth with original Japanese name pointers and a 448-byte increase to
  allocator start `0x020E45DC` reproduces the black upper screen.
- The same pool growth retaining the original allocator start boots normally.

Changing the allocator start is isolated as this failure's trigger; the lower
level reason remains unproven. The original boundary cannot simply be retained
with appended strings occupying allocator-owned memory.

V528 packs all 337 English bytes into the 364 bytes belonging to the 21 original
name allocations. Only adjacent owned allocations are merged. Every clean source
string, terminator, aligned padding span, and pointer owner is checked; literals
into an interior or unowned span are rejected. Every byte outside those spans and
21 fields stays exact. No pool growth, code change, section extent, startup copy,
allocator boundary, cache wrapper, image, palette, border or dimension changes.

## Actual display and preservation

All 21 prior single-site fixtures are cold-boot replayed with the same input
schedule. Nineteen display the complete English name in both list and map header.
All 57 heading/name masks include first/final letters and blank cells. Every
framebuffer pixel outside the two name regions matches V525 exactly, including
world maps, location markers, original plaques and controls.

IDs 1 and 4 retain the existing fixture fault; their images match V525 exactly and
receive no display credit. The previous untouched-Japanese control reproduced
the ID 1 and all-site failures. Their cause, natural discovery, and normal
gameplay display remain open. No code or save workaround hides these failures.

All 56 fresh title/New Game/story/town/Help captures remain pixel-exact to V525,
without a fixture save. All 470 batches, 114 accepted layers, 675 PXL/FLS files,
and 921 preservation entries remain. Only ARM9 changes. Clean-ROM xdelta
reconstruction is exact. Targeted Ruff passes.

## Release

Experimental candidate: `out/all_routes_combined_v528_candidate.nds`.
Profile: `all-routes-unified-v528`.
SHA-256: `487f39e981d2779876c2f9a7f9094a39228a524fdda0600fb23abaf71a6ff082`.
Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Canonical unchanged. Registered configuration: `translations/historic_site_names_v2.json`.
Verifier: `scripts/verify_historic_sites_v528.py`.
Proof and preservation chain: `work/analysis/historic_sites_v528`.
Rejected-build/control evidence: `work/analysis/historic_sites_v527`.

ROM, patch, manifest and BUILD_NOTES_V528 are published with verified hashes to
`E:/Rota Nova translations`. Captures are labeled as fixtures in
`Screenshots/Test fixtures/historic_sites_v528`; they do not establish earned
discovery or ordinary travel. Human cold-boot acceptance is still required for
canonical promotion. All 22 original requirements and all 18 incomplete plaques
remain. The full graphics goal remains active; revisit older record-based checks
when the full goal is complete.
