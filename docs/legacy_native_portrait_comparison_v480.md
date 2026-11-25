# V480 legacy/native portrait correspondence test

V474 remains unchanged. The SLACK13 atlas and El Gato clothing print were already
fully reviewed in V177. That older source decision is revalidated against current
bytes and is not counted as new completion credit. Original art remains intact.

The new work compares CMMNIMG.DK4 block0 against the distinct native CMMNIMG.000
store. Both are638464 bytes but their contents differ. Original reader code at
47A28–47A94 and47B3C–47B78 remains clean-byte-identical. It reads a512-byte palette
prefix and face data at512+index*3584,with3584-byte reads.

The coherent legacy56x64 interpretation and native read stride each partition
their complete store into178 cells. Every source byte is retained. Palette colours
are normalized to their lower15 BGR555 bits solely for colour correspondence;
alpha semantics and native legacy binding are not inferred from this normalization.
All178x178 complete colour hashes are compared:31684 pairs,zero exact matches.
Only3 corresponding palette entries have identical lower15 colour words.

This rejects treating equal byte length as equivalent portrait content. It does
not establish the legacy consumer,wrong colours,missing artwork,global non-use,
palette-bank behavior,alpha or real display. Do not redirect the legacy store
into the native one or grant it the native store's prior gameplay evidence.

Verifier: scripts/compare_legacy_native_portraits_v480.py;Ruff passes.
Proof: work/analysis/slack_portraits_v480/correspondence_proof.json.
The new contact sheet is analysis-only and is not archived as a guide screenshot.

Next work should trace the actual legacy owner/path or other unresolved display
contexts. A normal completed-route battery save would permit locked Maria/Gallery/
ending checks;the optional request is pending while independent work continues.
All22 historical requirements and18 incomplete plaques remain. No new ROM/patch
or canonical promotion. Revisit older record-based checks at full-goal completion.
