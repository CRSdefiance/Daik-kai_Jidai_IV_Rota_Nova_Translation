# Source-resolution review and current graphics completion audit

V230 is an audit iteration, not a ROM candidate. **V218 is unchanged.** The previous
turn made progress on actual opening/menu pixels and seven native title loads.
This turn closes the remaining source-resolution review gap and records the full
goal's current requirements without treating partial proofs as completion.

## Actual resolution gap

The historical inventory contains921 assets. Its sheet generator only reduces
images larger than272x342. **892 previews were already displayed at source size**,
including all243 event images at256x192. The old generic “622 previews unreviewed”
coverage string was stale: its later review counter is zero and all additional
review sheets are recorded. That history is retained alongside the corrected audit.

Only **29 assets** were reduced. They now have complete source-size content reviews:

| Family | Assets | Decision |
|---|---:|---|
| Raw harbor FLS | 1 | Retain architecture, harbor, water, birds and original stored padding. |
| Cabin/interior strips | 3 | Retain furniture, room/interior and rigging paintings. |
| Character atlas | 1 | Retain actor/clothing/equipment/building sprite parts. |
| Deck construction sheets | 16 | Retain hulls, hatches, windows, sails, rigging and sea tiles. |
| Item/trade strips | 4 | Existing684 complete-cell reviews remain applicable under exact current locks. |
| Regional/world map strips | 2 | Retain unlabeled coastline/land/sea paintings. |
| Large ship sheet | 1 | Retain hull/compartment/rigging construction art. |
| M22 canal/town scenery | 1 | Retain original architecture, canal, sky and water. |
| Total | **29** | No additional Japanese UI caption or player instruction found. |

Twenty-five assets were reviewed on21 new source-size sheets. Four item/trade
atlases reuse their individually reviewed684 cells and source hashes. Long strips
are shown in overlapping windows; these are presentation cuts, not invented native
record boundaries. No preview resampling is used. Every pasted region is compared
against its full source pixels after saving, and all original strip pixels remain
available in the full previews.

All29 selected assets preserve their clean palette, dimensions, flags and complete
indices, totaling **3,007,120 decoded source pixels**. Their previews also match
the complete historical previews. Twenty-eight whole files remain clean-identical.
M22's surrounding movie file contains earlier translations, while the selected
scenery texture0 remains exactly original. Other textures are not cleared by this
one-texture comparison. Original LZ10 streams may differ from a re-encoder's valid
compression choices; decoded slot identity is checked without rewriting the ROM.

No tiny book, costume, plaque or painted ornament reading is invented. These are
source-content retain decisions. They do not establish every native palette bank,
alpha state, composition, city/actor association or physical display.

## Full goal audit

| Requirement | Current evidence | Status / next work |
|---|---|---|
| Natural, faithful English for every meaningful Japanese graphic | Source-locked graphics batches and decisions; four Online originals inspected again | **Incomplete:** Online24/27/31/33 retain unreadable body/chat/player/status text. Better exact source is needed. |
| Embedded copies and unclassified/contextual art | CHARA descriptors, CMMN/raw source reviews, four exact DSCHR pixel copies, native archive/read probes, six contextual retain decisions | **Partial:** eleven legacy ILNK relationships, remaining raw/parent mappings and ambiguous source marks remain open. |
| Palettes, dimensions, borders and previous translations preserved | V225 all921 format/palette/extent checks; V226 all81 registered ownership entries, zero new outside-region pixels; this29-asset source audit | **Scoped checks pass:** covered background restoration and some internal art boundaries remain approximate and need contextual review. |
| Complete first/last letters, display bounds and native loading/crops | V227 all57 stored labels; V229 observed opening/menu; V217 sailing panels; V218 no-target notice; other native loaders | **Partial:** remaining changed graphics/alternate consumers and physical crops/composition still need coverage. |
| One registered combined ROM and exact patch | Current V218 and its467-batch manifest; saved exact patch reconstruction proof; current hashes rechecked | **Current integration passes:** further approved changes must enter the same complete registered stack. No final release or promotion claimed. |
| Updated graphics audit and translation progress | Historical audit corrected with current follow-up;29 retain decisions; campaign/progress/todo updated | **Updated for current evidence**, with unresolved requirements retained. |
| Visual/gameplay verification before completion | Normal title/New Game/story/town/sailing cold boots and selected exact framebuffer checks | **Incomplete across full scope:** source-size review or CPU fixtures do not clear every remaining physical display/scene. |

Confirmed-name integration remains pending project work: the settled choices and
rationales are recorded, but the prepared route/nonroute migrations are not all in
the playable ROM. Preserve the naming, allocation and leading-glyph review gates.
No source, approval or completed migration is inferred from an old draft.

## Current registered artifacts

- ROM: `out/all_routes_combined_v218_candidate.nds`, SHA-256
  `be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.
- Patch: `out/all_routes_combined_v218_candidate.xdelta`, SHA-256
  `78a21b599468357488ad2f54ba71a9b25a90be6cb1e375f85612b3e0301c1f7e`.
- Manifest: SHA-256 `b9caaf2aee3e2e7fd16ee1813f3f1f02a33be6be8051b46be8fe3f889ee585a3`,
  profile`all-routes-unified-v218`,467 inherited batches; accepted layers are baked
  into the immutable canonical base.
- Exact reconstruction evidence remains
  `work/analysis/no_target_v218/saved_proof.json`; its candidate/patch hashes match
  the current files. No redundant rebuild or canonical promotion was performed.

## Review artifacts

- `scripts/prepare_full_resolution_review_v230.py` (Ruff passes).
- `work/analysis/graphics_resolution_v230/full_resolution_inventory.json`.
- `translations/full_resolution_graphics_decisions_v230.json`.
- All full previews and21 pixel-exact review sheets in the same analysis directory.
- Linked existing item/trade source review:
  `work/analysis/common_atlas_consumers_v210/source_reviews/inventory.json`.

The full goal remains **active and incomplete**. The unavailable exact Online
transcripts are a source dependency; independent implementation/display work still
exists, so this is not a blocked-goal declaration. At eventual completion, revisit
the older record-based checks as requested.
