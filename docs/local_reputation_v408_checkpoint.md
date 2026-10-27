# Natural local-reputation rumors V408

Experimental full combined candidate; graphics goal active and incomplete.

## Actual defect and clean source

Normal Riga-to-Stockholm travel and a Tavern visit displayed
Argot serves Amsterdam as Trader. Clean COMMON820 says a named figure associated
with a city/profession is renowned in these parts;821 says that figure has local
influence. Neither says the figure serves or is employed by that city.

Reviewed natural-dialogue-v2/en-US paragraphs preserve all three printf arguments
in their original order:

-820: %s of %s is a well-known local %s.
-821: %s of %s is an influential local %s.

Local preserves the original regional reputation/activity scope and does not add
birthplace or permanent residence. The dynamic profession's existing capitalization
is retained. The manuscript has clean source hex, neighboring context, gloss,
localization notes and every required review gate. Native prose QA has no warnings
or waivers. New prose has no authored line breaks or alignment spaces.

## Bounded storage and actual formatter

820 fits its existing51-byte span.821 needs a40-byte aligned copy span instead
of20. Only20 trailing spaces from neighboring823 fund that extension.823's actual
nearby-city prose is unchanged;822 is byte-exact. Two original uint16 offset fields
for822/823 shift by20. All3668 visible selections retain their text except the two
reviewed rumors. The41-block cache directory and COMMON file sizes are unchanged.
Twelve native cold/warm/neighbor copies preserve complete text, NUL and guards.

The real portrait preparation calls its inherited macro helper at02054160;
parent return02054014 and stack message field+274 identify the two rumors. A
new180-byte scoped helper reuses the proven whole-word formatter after substitution
and supplies the first-row guard as formatter state. All existing3900 ITCM bytes,
including the equipment321/327 wrapper and condition labels, remain exact.
Total4080 bytes stays inside the original4096-byte allocation, with16 bytes free.
No arena, font, palette, artwork or speaker-control change is made.

Ninety native three-argument printf/word-wrap/raster cases retain all letters and
whole words. Twenty-seven parent/message cases verify unrelated passthrough; the
existing two equipment cases are byte-exact. The longest raster exceeded the old
100000-instruction harness cap while still in native glyph code; its explicit
200000 cap permits full return with all ABI/guard checks. Existing defaults remain.

## Actual final-ROM evidence

The exact genuine Tavern input schedule is replayed in the registered final ROM.
Frame20400 displays Argot of Amsterdam is an / influential local Trader.
Both lines start at x22; all512 native glyph pixels and blank cells match, including
first A and final period. Every word is intact. All54 other comparable voyage,
Palace, introductory story and Tavern frames match V388 exactly. All23 fresh New
Game frames also match. All470 inherited batches and every V388 stage remain;
only COMMON and ARM9 differ. All graphics, routes, HELP, ARM7 and other components
are exact. Ruff and exact clean patch reconstruction pass.

Proof: work/analysis/local_reputation_release_v408/release_proof.json.
Native proof: work/analysis/local_reputation_rumors_v404/native_proof.json.
Verifier: scripts/verify_local_reputation_release_v408.py.
Finalized screenshot: E:/Rota Nova translations/Screenshots/tavern-local-reputation-v408.png.

## Rejected work and scope

V405's preview split local across rows. V406/V407 used the equipment/modal parent
and did not repair the actual portrait rumor's near-full first-row margin; their
profiles are revoked and none was handed off. The final helper targets the real
portrait caller. A partial native whole-parent attempt lacked a required bitmap
resource and is not credited as full parent execution; final emulator behavior is
verified. Early V408 emulator launches preceded completed ROM creation and failed
to load a missing file; the completed build's fresh ready-folder runs both succeed.

One ordinary1250-coin military investment and a normal drink occurred in the
isolated test path. The original Riga donor was unchanged. No weapon/armor was
acquired. The original whole treasure-clue routine returns0 on captured score5261;
the next regional eligible item is Blue Oak Shield, effect24, threshold6000. No
score, unlock, item or live RAM was injected. Normal progression remains needed.

The polite820 variant has native source/copy/format/raster proof; its separate
actual NPC context remains unplayed. All18 plaques remain fully_completed:false.
All22 historical graphics requirements and deeper contexts remain in the ledger.
These are targeted emulator tests, not a full playthrough or hardware verification.
Low-resolution Online translation remains user-exempt. Revisit older record-based
checks when the full goal is complete. No canonical promotion occurred.

## Exact handoff

ROM: E:/Rota Nova translations/all_routes_combined_v408_candidate.nds
SHA-256: 65c785efb7870bc0b2bf54195d826d8f0528dc99c1a8dcc0fc629896863d1956
Patch: E:/Rota Nova translations/all_routes_combined_v408_candidate.xdelta
SHA-256: 940cbb9e131ca65f0e3f0721cbddacaa98a85cde930bbe117b3fd16d40aaf7ff
Manifest: E:/Rota Nova translations/all_routes_combined_v408_candidate.manifest.json
Profile: all-routes-unified-v408
Canonical integration base: out/raphael_natural_v2_accepted_base.nds
Base SHA-256: 3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe
Patch input: work/clean.nds
Input SHA-256: f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d
Changed internal files: /COMMON/MESFILE.DK4 and /__arm9__.bin.
Experimental; explicit user cold-boot acceptance is still required for promotion.
