# V781: the next 50 shared dialogue entries reviewed

COMMON 1020–1069 now have clean Japanese, exact current references, source glosses
and editorial decisions: 34 proposed revisions and 16 retained wordings. These are
drafts. All 50 formatting approvals remain false until production and gameplay
verification. 420 entries have source/prose review, including 53 active drafts;
367 are completed (259 revised and 108 retained). V780 remains the latest ROM.
The full editorial goal and the separate graphics audit are still unfinished.

## Meaning and natural English

- 1020–1027 retain the natural missing-information and low-success warnings, with
  the original strength and voice distinctions. Four warning sites use the same
  role-2 voice table. They ask permission before the original scheme is scheduled.
- 1028–1034 distinguish village coordinates from town names, and a fleet's current
  anchorage from its destination. Unknown fleets are not newly called pirates or
  assigned a faction. Hearsay is retained where the source uses it.
- 1035–1048 replace padded fragments with complete conversational prompts. The
  speaker is the **barkeep**, who offers to recruit for the player's crew. Required
  crew shortfall is kept separate from spare cabin capacity. Number-neutral wording
  works for one as well as larger counts, without inventing a plural suffix.
- 1049–1069 restore personal details and natural voice: limited interest in romance,
  a wish to surpass Mom, pleasure in cooking, help for a hard-working mother after
  Dad left, daydreams, the wait for a sailor, a childhood wish to be a princess,
  younger siblings, strategic deference, an interest in steering a ship and the
  parrot that the player gave her. No death, retirement, wedding, new relative,
  collective escape for siblings or pet sex is invented. The complimentary drink
  is her original offer, not a new refund or game mechanic. Character opinions
  remain character dialogue. Already natural wording is retained.

All prose uses natural-dialogue-v2 and American English. Each record has its own
Japanese source, gloss, speaker/context note and editorial decision. Approved names
and every runtime actor name remain unchanged. No manual alignment or line break
is authored. Neighboring stored messages are not treated as sequential dialogue.

## Original context and providers

624 native selections cover all 208 actor/current-captain objects across three
original voice tables; three null fallbacks are also checked. Four original
low-success call sites, the no-information branch and both recruitment-continuation
call sites reach the unchanged original wrappers. The recruitment initializer
sets role 1 for both continuation prompts. Original ABF50 formats the difference
between the required crew or capacity and the recruited total. Twenty supplied
native difference fragments cover ten positive decimal-width examples.

Twenty-one actual barmaid catalog entries select all 21 private topics through
58F24, native actor index plus 863. This is the second chance branch in 591D0 after
the gift/relationship stage, distinct from the casual topics reviewed in V780.
48 original village fragments cover all 24 points in both NPC modes. 570 original
unknown-fleet fragments cover 114 town-name providers and all five variants.

These are original CPU fragments with declared town, count and mode inputs. They
establish meanings, arguments and callers, not earned events, complete eligibility
filters or actual player-visible scenes. Full caller/portrait-core eligibility is
still a release gate. All compared executable spans remain exact to clean source.

Two research assumptions were corrected before recording results: the role value
must be established through its original initializer, and B6618 returns a town
object rather than a numeric index. The village caller now uses the original town
object offset, with its bounds and stride checked. No ROM bytes were changed.

## Prospective formatting and visual review

857 native printf/layout cases preserve every expanded byte and complete word,
guards, argument copies and the saved-register contract. Cases cover the captured
town names and village coordinates, original full-width decimal counts and explicit
width stress values, including zero and a large signed-positive boundary. Stress
counts are not claims about physically available crew or the source branch's
positive-count eligibility. The existing native font correctly renders these
original numeric strings. Number-neutral prose avoids the one-sailor/plural trap.

Village coordinates contain a leading LF and alignment spaces. The CPU prototype
explicitly selects the existing scoped coordinate-compaction helper, preserving
complete N/S/E/W numbers and the source argument copies. This does not prove the
future dispatcher will select that helper for 1028/1029. The global coordinate
provider is not edited. Production ownership, exact membership and actual routing
must still be proved.

The first pass found two weak line endings, after an article and a preposition.
Natural rephrasing of Donna's daydream and Benazir's self-question repaired them
without dropping facts. The first manuscript, source programs and failed preview
artifacts are retained as research. The second pass has zero layout findings.

83 complete native font planes independently match the game font. All nine sheets
were visually reviewed for complete first/final letters, margins, bounds and fluent
line breaks. Every enlarged card is pixel-identical to its saved native plane;
three full-resolution standalone checks also confirm the leading letters. These
are CPU previews, not new in-game screenshots or production-formatting approval.

## Next gates and preservation

Finish original caller/filter and role/portrait-core eligibility; establish scoped
production routing without section, cache, arena or staged-payload growth; verify
all production outputs and complete native copies; build through the registered
combined release and reconstruct the exact clean-input patch. Then test warnings,
both recruitment continuations, rumors and personal topics with representative
actual conversations, controls and normal scene returns. User-approved fixtures
may make rare states reachable, with explicit provenance and protected donor copies.

All 50 drafts receive zero completed-entry credit until those gates pass. COMMON
1070 onward, drafts 750–752, all route scenes and other player-facing prose remain
in scope. The two older route leads observed in V780 remain queued. The separate
graphics audit, its 18 original plaques, excluded Online bodies and preserved brown
marks are unchanged. Revisit the older record-based checks at full goal completion.

V780, its exact patch, the registry, canonical base, clean ROM and original donors
remain unchanged. Research and previews are archived under E:/Rota Nova
translations/Editorial review/V781 Shared prose research. They are not promoted as
guide screenshots. No GitHub commit or push was performed.
