# Current Market composition and live stock V428

V414 remains unchanged. A fresh normal-control boot replays the Market visit and
reaches Lisbon's Deal screen at19700 frames. No donor save, research ROM, savestate,
unlock change or live RAM injection is used. The run finishes normally and exports
read-only main RAM, CPU/TCM and graphics state. All capture/state hashes pass.

## Complete current pixels

V248's independent source-atlas, native font/shadow and frame-cell composition
algorithm runs against the actual V414 capture. All2880 pixels in the five24x24
goods rectangles and all130 complete grade-digit ink pixels match. There are no
unexplained rectangle pixels or screenshot-derived exclusions. Source atlas and
the five original grade cells/palette remain clean-exact. Earlier V248 evidence
remains historical; this adds current-ROM display proof.

## Actual linked stock values

The read-only capture contains CTradingView at0218F25C. Its original runtime type
metadata names that class; field5F8 points to model021918C0. Original getters
020BCAF4,020BCAE8 and020BCADC return the actual goods, grade and quantity:

| Slot | Goods cell | Grade | Quantity |
|---|---:|---:|---:|
|0|13|4|3|
|1|14|4|5|
|2|27|5|8|
|3|78|5|7|
|4|86|4|5|

Every value matches its complete displayed source image/digit. Original fragment
020C1718–020C172C reads the actual view/model link and computes source x104 or112
for these five grades. The code matches clean, original getter ABI checks pass,
and the whole model remains unchanged by the isolated queries. This ties current
pixels to the actual linked stock, rather than accepting a vtable occurrence alone.
It does not establish transaction arithmetic or a live CPU instruction trace.

## Correction to V249 attribution

V249's BCC getters and C37B0 crop fragment remain valid supplied-input native tests
for their documented structure. They do **not** supply this visible local-stock
row, which uses CTradingView's BCA getters and C1718 fragment. The old claim that
C37B0/BCC mapped these five visible local slots is superseded here. The earlier
complete source/pixel proofs remain valid. The full live dispatch gate is not
silently closed by an isolated snapshot query.

## Original meaning and newly confirmed remaining translation

Original HELP block193 explicitly gives grades1–5 and grade1 as highest quality.
Its source first paragraph is decoded independently without the later embedded
link controls. The current block is byte-identical to clean and **still Japanese**.
Translate this meaningful help entry through the protected-link HELP workflow;
do not flatten its raw link controls through ordinary CP932 re-encoding. Its source
hash and exact grade ordering are recorded in live_stock_proof.json.

## Artifacts and remaining scope

Verifier:scripts/verify_market_live_v428.py. Evidence:
work/analysis/market_live_v428/proof.json and live_stock_proof.json. Targeted Ruff
passes. Finalized native screenshot:guide/screenshots/market-local-goods-v414.png,
also copied and verified on E with its manifest/provenance.

Quantity transaction arithmetic, other Market variants, remaining HELP translation,
environment/legacy/movie/Gallery contexts and all18 plaques remain open. No ROM,
patch or release profile change. Full goal remains active. Revisit older record-based
checks at actual completion.
