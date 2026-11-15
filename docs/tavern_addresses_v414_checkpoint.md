# Shared Tavern addresses and treasure clue V414

Experimental combined candidate; graphics goal active and incomplete.

## Source and localization

The genuine Blue Oak Shield clue in V408 displayed Japanese 旦那 mixed into English
and divided treasure across lines. Eight shared eight-byte Tavern slots at143BD0
through143C08 contain four male 旦那 copies and female姐さん/姉さん variants. Their
exact bytes and sole aligned pointer owners are locked by the V412 source review.
The clue's pair differs from the paid-round announcement's pair, explaining why
fixing872 alone did not remove the address elsewhere.

All four male providers now return Sir; all four female providers return Ma'am.
These are respectful vocatives, not a knighthood, marital status, or kinship claim.
Source-reviewed natural-dialogue-v2/en-US paragraphs also repair:

-865: Drinks for everyone!
-871: Bravo! A round of applause for %s!
-873: With your skills, %s, you'll find it for sure.

The order retains drinks for everyone and omits the redundant familiar barkeep
address. Applause retains the named payer/group while omitting the awkward gendered
honorific: native printf still receives both arguments, the second unused safely.
Encouragement keeps the speaker's confidence and the patron's skill. All authored
prose is one paragraph with complete source/context/meaning/review gates and no
manual layout spaces or breaks. Native prose QA has no errors or warnings.

## Bounded implementation and preservation

The new optional stage follows all V408 stages; the V408 module/config/ASM remain
unchanged and reconstructable. Only three COMMON text spans change, within their
existing allocations. All3668 offsets, other text, cache directories and file sizes
are unchanged. Address strings retain their original eight-byte slots/pointers.

The existing portrait word-wrapper scope expands from820/821 to870–873 while
preserving its exact parent54014, caller54160 and original first-row formatting
policy. Its suffix grows12 bytes. SDK section4 is4092/4096 bytes, leaving4 bytes;
the original arena and first3900 ITCM bytes are unchanged. Fonts, palettes,
all graphics, route files, HELP, ARM7 and other components remain byte-exact V408.
Existing reputation and equipment behavior remains unchanged in native scope cases.

20 real native cold/warm/neighbor copies,18 male/female clue printf/word-wrap/raster
cases,8 applause/encouragement printf cases, all eight loaded provider strings and
24 parent/message passthrough cases pass. Every tested clue retains all arguments,
letters, NUL/output guards and whole words. All five native previews were inspected.
Targeted Ruff passes.

## Actual final combined-ROM evidence

A fresh cold boot replays the exact normal earned-clue path using the unchanged
slot4 Stockholm battery. The final clue is entirely English:

Sir, here's a tip: the rare
treasure Blue Oak Shield is said to
be hidden in N. Sea.

All three lines begin at x22. All796 native glyph pixels and blank cells match,
including first S and final period. No word is split. The actual order also matches
its complete natural-English mask. All41 other comparable gameplay frames are
exact; changed pixels stay within the affected dialogue body. All23 fresh New Game
frames match. The full470-batch stack and every V408 stage remain. Exact clean-ROM
patch reconstruction passes. Female clue and encouragement/applause variants have
native provider/format/raster evidence; separate actual contexts remain unplayed.

Native verifier: scripts/verify_tavern_addresses_v413.py.
Release verifier: scripts/verify_tavern_release_v414.py.
Proof: work/analysis/tavern_addresses_release_v414/release_proof.json.
Finalized screenshot: E:/Rota Nova translations/Screenshots/blue-oak-shield-clue-v414.png.

## Exact handoff

ROM: E:/Rota Nova translations/all_routes_combined_v414_candidate.nds
SHA-256: 699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c
Patch: E:/Rota Nova translations/all_routes_combined_v414_candidate.xdelta
SHA-256: 1d16b5bf83e4741fee23d389a57f12bbf7846089b095a551504e38a323d3c6a6
Manifest: E:/Rota Nova translations/all_routes_combined_v414_candidate.manifest.json
Profile: all-routes-unified-v414
Canonical base: out/raphael_natural_v2_accepted_base.nds
Base SHA-256: 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe
Patch input: work/clean.nds, SHA-256
f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
Changed internal files: /COMMON/MESFILE.DK4 and /__arm9__.bin.
All E copies were SHA-256 verified. No canonical promotion occurred.

## Remaining goal

The Blue Oak Shield clue was earned normally; the armor itself is not yet acquired
or equipped. The clue save remains E:/Rota Nova translations/Saves/hodram-blue-oak-clue-v408.dsv.
All18 plaque/hint entries remain fully_completed:false, and all22 historical
requirements remain. Other health/mood, occupied equipment, original legacy art
consumers, Gallery/endings and regional contexts remain open. No synthetic progress,
item, unlock or live RAM injection was used. These are targeted emulator tests,
not a full playthrough or hardware verification. Low-resolution Online images are
user-exempt. Revisit older record-based checks at full graphics-goal completion.
