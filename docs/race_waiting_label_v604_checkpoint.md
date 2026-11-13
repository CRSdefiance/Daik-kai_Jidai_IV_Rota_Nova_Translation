# V604: complete empty-player card status in Grand Race

The preceding goal turn made progress by introducing a bounded runtime drawing
trace. This batch extends it to Grand Race and fixes an actual native formatting
defect found there. V604 is an experimental integrated candidate. Canonical
acceptance has not changed and the full graphics goal remains open.

## Observed defect and faithful wording

An isolated cold boot of V599 reaches Grand Race > Start Race > the copied Maria
save > Host. The authorized historical system-unlock fixture enables this menu;
earned completion is not claimed. Its save is unchanged, SHA256
`295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949`.
The research observer and unmodified V599 produce the same entire waiting-screen
image at frame4400, independently confirming the problem is in the release.

The inherited empty-card string is `Waiting for a player`, 120 pixels wide at the
original six-pixel advance. In the third card, a later original background draw
overwrites all eight ink pixels of the final **r**. At frames4400/4800/5200 the
other two empty labels retain all201 ink points; this is not generalized as a
missing letter on every card. The earlier status description that several cards
were cut off is narrowed by this complete-mask measurement.

Clean and canonical source at02000000+16BA34 is `-- 参加待ち --`, an unoccupied
slot waiting for participation. `Awaiting player` conveys that status naturally
in a compact UI label. It is 90 pixels wide and fits all original card text
origins. No story information is removed. The original source is used for the
meaning; the earlier English wording is evidence of a defect, not a source lock
for a new translation.

## Shared fix and complete ownership

`dk4tool/patch/race_waiting_label.py` applies a final registered transformation
after the complete V599 stack. The original constructor selects one shared
fallback string at pointer field020FADDC. The current owned text span is
0216B927..0216B93C, including its terminator. Every byte position in all main
autoload sections and the original overlay is checked for stored pointers into
that span; the one original fallback pointer is the only match. The new phrase
and zero padding replace that exact span. No other string or pointer changes.

The complete original card painter020FABB0, fallback020FAD38, native ASCII
painter020D1604 and all four source coordinate records remain exact. This changes
the shared empty-card status everywhere its existing fallback is used. Historical
Grand Race manuscripts/compilers remain intact for exact older-build reproduction;
their longer empty-card wording is superseded for this registered current display.
There is no hook, new section, pool/heap growth, altered network state or resource
substitution in the playable candidate. No PXL, FLS or embedded-art bytes change.

## Native verification and regressions

The candidate and V599 each receive fresh Host and Join cold boots with identical
ordinary inputs and the same explicit system-unlock save. Host attempts A and
START, then B; Join searches for a host and returns with B. No wireless peer is
connected. A and START do not establish an available Confirm action with a lone
player, and successful multiplayer or a completed race is not claimed.

At three actual Host frames all three empty cards pass complete 6x11 font masks:
nine appearances and1,512 ink points. Their first/final letters, spaces and blank
tail through the entire old120-pixel field are checked. There are no residual old
letters. Their actual native text bounds are x74..164, at rows240/280/318. Every
other pixel of each whole two-screen frame is exact to V599, including existing
portrait, card backgrounds, occupied player name, instructions and footer.
All pre-waiting and Back-return Host captures match whole frames. All sampled
Join captures also match whole frames.

A separate ordinary24,100-frame New Game/Market replay uses no existing save or
synthetic fixture. It covers title/character selection, the opening, town and
purchase/sale navigation. All19 unique sampled full frames match V599 exactly.
This is targeted emulator coverage, not a complete playthrough or device test.

The Grand Race research trace is an additional5,200-frame run, recording27,582
calls through both drawing entries. Both positive controls pass; there are zero
target records and zero overflows. Its initial noninteractive attempt stopped
with EOF at the first input pause and receives no completed-run credit. The
fresh PTY run finalized normally. The ordinary kakutei Confirm graphic and the
five miniature cells retain unresolved parent status; the generic waiting-screen
text must not be mistaken for evidence that those graphics were used.

## Registered integrated output

- Profile: `all-routes-unified-v604`, experimental, all470 batches/114 accepted
  layers retained from V599.
- Candidate: `out/all_routes_combined_v604_candidate.nds`, physically on E under
  `Rota Nova translations/Generated/out`.
- SHA256: `fb8de61d20e94e742574bded2d8e4251305f2b56265ff8624dd766eaa6cf9158`.
- ARM9 SHA256: `236c41a67fe8ddc82181b9809c82980a08154b3dc886c44d2cb0f585f202606e`.
- Patch: `all_routes_combined_v604_candidate.xdelta`, SHA256
  `5fa980cd6995606989375b69e6be7083cfcb6fbe90c122e96e2a30d7bc20cc7a`.
- The patch reconstructs the exact candidate from clean ROM SHA256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- The immutable integrated build baseline is
  `out/raphael_natural_v2_accepted_base.nds`, SHA256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Only ARM9 differs from V599, entirely within the shared21-byte status span.
  Every graphics file/container is byte-identical to V599. Its921 decoded format,
  palette/extent checks and57 embedded-block checks therefore carry forward as
  preservation evidence, without new native-use claims.

The neighboring manifest records the canonical parent, registry hash, complete
layers, changed records and passed build gates. The current audit pointers now
identify V604; the old V581/V599 pointers are retained in a separate snapshot.
The18 original plaque/hint objects remain incomplete and all22 historical objects
retain their exact scope. No automatic user acceptance or canonical promotion.

Reproduce with the registered integrated builder, then the proof's explicit
Host/Join/Market input files and harness arguments. Run
`scripts/verify_race_waiting_label_v604.py`, followed by
`scripts/record_race_waiting_label_v604.py`. Checkpoints, native screenshots and
provenance are on E under Test fixtures/V604 Grand Race card status and Guide
candidates/V604 Market regression. The Grand Race shots use an unlock fixture;
only the Market shots qualify as ordinary guide candidates. Publication remains
unapproved. Other graphics gates and the final older-record review remain open.
