# V696: final-build protection for the raw comic family

The previous goal turn made progress through V695's relocated sources and two
original embedded UI classifications. This turn protects the existing localized
comic artwork after all later integrated-release stages have run. No production
art, wording, ROM bytes, patch, release profile or canonical pointer changes.

## Gap and fix

The mixed archive stage verifies the raw comic batch when it first merges it
with the separately registered legacy PXL syncs. The previous final menu and
placeholder checks do not revalidate this artwork after later stages. Seven
in-memory changes demonstrate that those existing final checks accept damaged
comic output. No damaged ROM is written.

`dk4tool/graphics/raw_art_contract.py` now checks the final candidate just before
saving. Applicable profiles are selected from their actual complete batch list;
there is no separate manually maintained current-caption list. The contract
reconstructs the reviewed raw artwork from its exact canonical Japanese source,
locked font, complete English and source-bound per-record restoration rules.
The canonical raw block must also equal the clean Japanese block.

The final check covers all 3,225,600 bytes of SLACKIMG block 19:

- All 18 complete reviewed caption/restoration regions in ten edited frames.
- Every unowned source byte and all original high color bits.
- All 11 untouched frames, byte for byte.
- The user's preserved frame-6 brown-mark rectangle: 4,320 bytes.
- The original archive allocation and complete block-offset table.

Other archive blocks remain outside this raw-art contract because their own
registered PXL synchronization stages may change them. Those stages keep their
existing checks. The new guard does not treat a fixed whole-archive target hash
as permission to overwrite unrelated blocks.

## Meaningful regression controls

All seven isolated corruptions pass the previous final menu/placeholder gate
and are rejected by the new final comic gate:

1. A visible pixel deleted from the first English letter.
2. A visible pixel deleted from the final punctuation glyph.
3. A complete caption reverted to its original Japanese source region.
4. A changed word in the user-preserved brown-mark region.
5. An altered original high color bit.
6. A changed word in an otherwise untouched source-art frame.
7. A changed word in the reviewed estimated background restoration.

Unrelated story changes do not trigger this guard. A change in another archive
block does not make it claim ownership of that block. Profiles without a raw-art
batch report not applicable. Historical V185 passes using its own registered raw
batch rather than acquiring the later V251 fringe changes.

The contract protects the reviewed reconstruction; it does not claim exact
recovery of scenery originally hidden beneath Japanese lettering. The source
comparison sheets for frames 4–7 and 12–15 were opened this turn; no clear new
artwork defect was identified. The original comic viewer, real viewport, GPU
alpha and gameplay readability remain unverified. No substitute viewer is used.

## Complete integration check

The complete registered `all-routes-unified-v692` stack is rebuilt through the
integrated builder into `out/all_routes_combined_v692_raw_art_contract_rebuild.nds`.
Its entire ROM must be byte-exact to current V692, SHA-256
`0ff197ce9bbb48898c74a3c664609196867a5662bc3b346c612709038c54a47e`.
The final verifier checks all 470 batches, 114 accepted layers, original changed
paths/records/relocations and every prior manifest check, including the plaque
and source-bound story-format contracts. The reproduction manifest additionally
records the final raw-art contract.

This is an unchanged-binary reproduction, not a new candidate or canonical
promotion. The existing V692 patch remains applicable to the identical bytes;
no new patch or fresh emulator run is claimed. See `rebuild_proof.json` for the
actual completed comparison and reproduction-manifest hash.

All 18 plaque/hint entries remain incomplete. All 22 historical requirement
objects, user Online exclusions, brown-mark retention and older-record follow-up
remain unchanged. Actual comic/legacy/control/card contexts, restoration review
and final acceptance remain open. Full graphics goal remains active.

## Evidence

- Final guard: `dk4tool/graphics/raw_art_contract.py`.
- Corruption controls: `scripts/verify_raw_art_final_contract_v696.py`.
- Full-rebuild verifier: `scripts/finish_raw_art_contract_v696.py`.
- Analysis: `work/analysis/raw_art_final_contract_v696`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V696 Final raw comic contract`.
- No guide promotion, commit or push.
