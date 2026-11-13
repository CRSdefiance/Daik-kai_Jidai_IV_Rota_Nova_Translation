# V625/V626: original scheme names, queued voices and complete word wrapping

Previous goal turn made progress: V624 completed five hidden menu labels and
exposed Japanese confirmation names and broken word wrapping. This turn fixes
their shared providers and verifies all four original command paths. The full
graphics goal stays active; all18 original plaques remain incomplete and all22
historical requirements retain their original objects and scope.

## Source-faithful names and two corrected voices

Original CScheme name getters02093D28/02093D5C use a separate general table at
0214C5E8. Its types6..9 still returned Japanese even after the V624 menu fix.
V625 redirects fields0214C600/604/608/60C to the complete, existing V624 strings
Lure Fleet, Forge Papers, Bad Rumors and Bribe. No text storage grows. Both source
getters return each complete English string, including its terminator. This
shared provider applies wherever the original scheme-name getter is used.

Clean COMMON918/920 confirm the selected scheme and ask for an opposing faction.
Their old English incorrectly asked about a price. The new reviewed paragraphs
are `%s, then? Which faction should we target?` and
`Hmm, %s? Which faction shall we target?`. They preserve the single scheme-name
argument and natural older/formal voices. The custom source-locked native
transform validates the natural-dialogue-v2 manuscript and every clean source
byte. All eight two-voice/four-name native previews were inspected. Their fixed
slots are retained with trailing padding; native directory offsets, NULs, copy
extents, all neighbors and original macro machinery stay exact.

V625 also extends the existing direct portrait dispatcher from820..873 to988.
Its22008 old/new dispatch executions and230 native layouts pass, but the actual
Strategist introduction still splits words. This is a failed coverage assumption,
not a font fit or startup pass: those native tests supplied the Barkeep's direct
parent02054014. Preserve the V625 diagnostics; it is superseded by V626.

## Actual queued caller and twelve original voice tables

Original020572D0 calls02053D44 with role2 and table02118340. Original role/voice
selection reaches02054058 and returns to02053DB8; modal role choices return to
02053D24. At the shared dispatcher, their original voice-table argument is at
sp+27C. It is not the direct numerical-message argument at sp+274. The existing
SeaFoam wrapper independently documents this queued-parent contract.

V626 adds recognition of those exact two parents and twelve clean source tables:
02117B40 and021181E0/200/220/240/260/280/2A0/2C0/300/320/340.
Each original eight-slot voice table is checked against clean Japanese source.
The interval's unrelated021182E0 table, unaligned pointers and outside addresses
are excluded. The tables cover80 original message variants908..988, excluding
unrelated972. Both queued formats receive the existing paragraph helper after
the original expansion. All original selection, role, voice and argument rules
are retained. Unmatched cases restore their original parent before the unchanged
SeaFoam/other dispatcher.

The code uses reviewed immutable-string padding at01FFCE1C..CE40 and
01FFC664..C680 plus three released Japanese scheme-name strings at
0214C530..C538 and0214C550..C564. The former Japanese strings have no remaining
unaligned main/autoload/overlay reference after V625 redirects their sole table
owners. All four owned spans have zero such references before reuse. Existing
Joachim/Hodram/Bergstrom and Fleet%s strings retain every byte and terminator.
The Square scratch surface atC1A0, resource slotsC680/C6A0, all other code,
section extents, staged payload, startup/cache wrappers and arenas are exact.
No zero-filled scratch region is treated as free code storage.

The final native proof executes22008 unchanged numerical dispatches,115 original
and added table/parent controls, and160 complete queued voice/glyph layouts.
Every modeled word stays on one row and every visible character remains in order.
The original expansion buffers, guards, stack and register ABI pass. These
supplied layout arguments are separate from the actual game-provider evidence.

## Actual game tests

A fresh no-savestate V626 cold boot uses the same disclosed V624 isolated fixture:
three Gerhard room-assignment bytes, one experience word and three calendar days.
The source donor is unchanged. No menu flag, outcome, funds, cargo, artwork,
health or attribute is injected. Original menu eligibility and voice choice run.
The test stops normally at24801 and exports native RAM/ITCM.

- All four selection states of both menus retain32 complete framebuffer glyph
  masks and original source crop requests, including every first/final letter.
- Fourteen source-bound dialogues cover the full introduction; all four English
  scheme-name confirmations; broker, destination, opposing-faction and rumor
  prompts; every final scheme confirmation; and the arrangements notice.
- Bribe selects Castor Co./Lisbon and commits through normal A/Yes. One original
  type9 CScheme object is created. Funds remain8371 while its arrangements notice
  is open, then become7371 after the notice closes, as the original source order
  specifies. No completion or result flag is supplied by a fixture.
- Lure Fleet targets Castor Co./Lisbon, Forge Papers targets Castor Co./Albuquerque,
  and Bad Rumors targets Castor Co./Lisbon. Each normal B/No cancels its final
  confirmation. The complete existing scheme object and7371 funds stay exact
  after all three cancellations.
- Nineteen ordinary no-save/no-fixture New Game/Market frames match V624 byte for
  byte. All470 batches/114 accepted layers,921 PXL/FLS format/palette/extents,
 57 embedded extents and exact clean-ROM patch reconstruction pass. Only ARM9 and
  COMMON/MESFILE change versus V624; all graphics, routes and other components are
  retained.

## Explicit remaining checks

Ten dialogue cases match the complete original-renderer foreground mask in the
actual framebuffer. Four others expose a narrow older renderer-model discrepancy
at CP932 full-width I: the16-pixel-metric host raster predicts one additional
stroke column per glyph, while the actual complete left stroke is present.
Every non-I foreground/background pixel matches. Differences are retained at
their exact coordinates, rather than erased or called a whole-glyph pass.
The actual font object has6x12 metrics, but simply supplying those metrics to the
historical host raster changes line advance and does not resolve the shape.
The FNT file itself matches the entire resident data. A metric-only probe is
retained in the analysis folder, with no production font change. Calibrate the
actual renderer/view contract before claiming exact CP932 whole-glyph coverage.

Source review also finds independent recruitment alternatives897/898 split as
`...Admir` and `al? Step forward!` in old English. Their clean source entries are
separate complete voice lines, not one sentence across records. Their content
remains a concrete next repair; these are not cleared by wrapping their bytes.
The original Confirm/five miniatures/eight village cards, remaining legacy/comic/
logo/movie/material and broader gameplay gates remain open. All18 plaque entries
stay incomplete. The four low-resolution Online exemptions and preserved brown
marks remain in force. Older record-based checks remain due at full completion.

## Artifacts

- Experimental ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v626_candidate.nds`.
- ROM SHA256: `6164af2ddc9f77475b59a0ec05c10d57a9d99fd3853859e72b0b5fcea8510388`.
- ARM9 SHA256: `282ef872ceb9fbf9f0c27a8c315f4ea403f0e68746c5c1c7f3883e63df923651`.
- Adjacent xdelta SHA256: `7bad8d0a776f6f24274a6550b44f731a4eca69c31bb5bfd65a7dc52500784226`.
- Profile: `all-routes-unified-v626`, complete V624 plus `tavern_scheme_context`
  and `tavern_strategist_wrap`, retaining470 batches and114 accepted layers.
- Full proof: `work/analysis/tavern_schemes_v626/release_proof.json`.
- Verifiers: `scripts/verify_tavern_scheme_native_v625.py`,
  `scripts/verify_tavern_queued_native_v626.py`,
  `scripts/verify_tavern_scheme_release_v626.py`.
- Screenshot/source/proof archive:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V626 Tavern scheme contexts`.

Canonical `out/raphael_natural_v2_accepted_base.nds` remains SHA256
3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
No promotion, complete route/playthrough, hardware or full graphics completion is
claimed. Verified pointers are retained; the latest compiled experimental pointer
advances with all remaining limits recorded.
