# V744: first shop and town editorial pass

Clean Japanese and current V712 native COMMON selections 656–687 received a
source/prose pass. The coverage ledger records **32 reviewed drafts: 19 proposed
revisions and 13 retained wordings**. This is not completed native-context,
formatting, gameplay or integrated-release coverage. No ROM was changed.

## Findings

- **657:** the current English omits the merchant recognizing the player as a
  sailor. The draft restores it while preserving the trade-house recommendation.
- **658:** replace the stiff business response with a conversational reply:
  “Business? Oh, it's been all right. I'm hoping a good deal comes along.”
- **676/677:** the current cooking pitch ends with “Discover” while the separately
  selectable fashion pitch starts with “the fashions…”. The fashion selection
  also omits the invitation addressed to ladies and gentlemen. Drafts restore
  each complete independent pitch. They share the packed owner with 675, so all
  three native selections must be preserved during reallocation.
- **683:** the Japanese describes people collapsing during an epidemic; it does
  not establish deaths. The draft preserves that distinction and the speaker's
  indignation without assigning a particular disease.
- **688:** the next country-briefing group needs review: current text begins
  “England unites England…”, whereas the Japanese discusses Britain and its
  constituent countries. This finding is queued, not counted among these 32.

Source phrasing and omissions determine the revisions. Already natural lines are
retained with explicit reasons. Different confirmation and announcement voices
remain separate variants; table adjacency is not evidence of a sequential scene.

## Artifacts

- `translations/shop_town_editorial_manuscript_v1.json`: one-paragraph drafts,
  clean Japanese, canonical/current byte references, glosses, decisions and notes.
- `translations/editorial_review_current_v1.json`: coverage and findings.
- `work/analysis/shop_editorial_v744/review.md`: complete readable comparison.
- `work/analysis/shop_editorial_v744/source_context_packet.json`: neighboring
  Japanese/current selections 652–690 and source/current packed owners.

The manuscript uses the required `natural-dialogue-v2` schema. Pending context and
formatting gates remain false, so the manuscript is deliberately not build-approved.
All source printf substitutions retain their type, count and order. No authored
line breaks or alignment spaces appear in the prose.

## Next integration work

Establish the actual callers and rendering contracts for these interaction groups.
Use the COMMON formatter and macro behavior proven for those consumers. The
generic story lint rejects some literal uppercase I/F spellings that the current
COMMON native macro guard explicitly supports; do not distort the prose to work
around a mismatched profile. The first exploratory generic encoder call also
used the wrong function signature; neither experiment modified ROM bytes or
received formatting credit.

Complete meaning must take priority over inherited slot lengths. Use the proven
native repacking facilities where necessary, preserving packed siblings, message
IDs, cache limits and every unselected message. Inspect generated line breaks and
letters, then integrate through a new registered combined profile and run targeted
native/ordinary gameplay checks. The current production reference remains V712;
the unfinished graphics audit and canonical base are preserved.
