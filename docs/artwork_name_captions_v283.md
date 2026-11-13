# Artwork caption name consistency V283

The previous goal turn made progress by recording final HELP navigation evidence
and preserving the Online-image scope exception. This turn corrects15 scene
captions and one Gallery description still using Raphael/Kamil. Their English
now uses the locked Rafael/Camille spellings. Source Japanese is checked against
the clean ROM; all other caption words, subjects and numbered variants remain.
Historic release manuscripts and pinned dependencies are preserved.

## Native evidence

The script `scripts/prepare_artwork_name_captions_v283.py` reproducibly appends
complete revised strings to the existing owned pool, updates only16 selected
pointer fields, and refreshes its existing startup/cache extent. All original
main-code bytes except those pointers and required startup/extent fields remain
exact. All original ITCM/DTCM sections and inherited pool bytes are exact.

Each revised string is rendered from its actual new pointer by the native
D5404/ASCII painter on a bounded256x192 primary surface. Complete glyph order,
independent font pixels, first/interior/final letters, centering/tracking and
bounds pass. Gallery's required pair-safe trailing space is invisible. Native
autoload, BSS clear, full pool copy and cache monitor pass, and every inherited
caption pointer is checked. The16-row native preview has been visually reviewed.
Ruff passes. The owned pool uses82880 bytes, within its existing reserved limits.

Evidence: `work/analysis/artwork_name_captions_v283/native_proof.json` and
`translations/artwork_name_caption_review_v283.json`.
Preview: `work/analysis/artwork_name_captions_v283/caption_review.png`.
The executable data fixture is `proposed_arm9_research_only.bin`; no playable ROM
or registered release profile was generated.

## Remaining gates

The isolated font surface is an explicit fixture contract. Actual caption-parent
selection and live GPU composition are still pending. Shared names, route text,
COMMON/HELP and artwork-caption changes must be integrated together through the
registered complete builder before handoff. V275 remains the latest playable
candidate. All18 plaques and Armor/Weapon variants remain incomplete as requested.
Low-resolution Online promotional images remain excluded from translation.
The full graphics goal is active and incomplete. Revisit older record-based
checks at actual completion.
