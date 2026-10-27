# Earned armor clue and new Tavern defects V409–V411

V408 remains unchanged and experimental. Its verified ROM SHA-256 is
`65c785efb7870bc0b2bf54195d826d8f0528dc99c1a8dcc0fc629896863d1956`.
The previous chat reply's different hash was a reporting error; the actual ROM,
manifest, release proof and E-drive copy all agree with the value above.

## Normal progression

V409 cold-boots the normally saved Riga checkpoint. Ordinary Sail departure,
steering, cold-weather and rats events produce actual voyage progress. The captured
clue score increases from5252 at5600 to6176 at10200, above the original6000 threshold.
The fleet stalls briefly near Stockholm's coast, then normal course corrections
reach Dock at Stockholm?; A docks. This is actual play, not a stat/save edit.

The normal Save menu creates slot4. V410 cold-boots that battery and loads the
remembered fourth slot; the score is6539 and Stockholm Docked is retained. The
previously fixed reputation rumor renders correctly. Order Drink triggers the
normal hostess interaction; after declining another drink, the player selects
Treat Everyone and accepts the208-coin cost. A patron provides the Blue Oak Shield
clue in the North Sea. The original4A394 item getter reads clue flag1, changed
from0, while the item remains unacquired.

Normal Save creates slot5. V411 cold-boots and loads it normally; the same earned
score and clue flag are retained. Original Riga donor hashes are unchanged.
Verifier: `scripts/verify_earned_armor_clue_v411.py`; targeted Ruff passes.
Proof: `work/analysis/manual_clue_progress_v409/earned_clue_proof.json`.
Convenience save: `E:\Rota Nova translations\Saves\hodram-blue-oak-clue-v408.dsv`.
SHA-256: `43914e41436b1f770981f942a1c5fe3b2e4c11437e1f9748736e80de68cf807f`.

## Confirmed text defects to correct next

The actual clue screen retains Japanese 旦那 before the English tip and splits
treasure across rows. COMMON870 itself is English with three original printf
arguments; the address comes from a separate ARM9 literal. Eight eight-byte
Tavern address slots at143BD0..143C08 contain four 旦那 copies and the female
姐さん/姉さん variants. The clue uses143BE0/143BE8, not the already reviewed
round announcement's separate143C00/143C08 pair. Exact source bytes, every pointer
reference and clean/current neighbors870–873 are recorded in
`work/analysis/shared_tavern_addresses_v412/source_review.json`.

The ordering line Barkeep, drinks all! also warrants source-based natural-English
review. These are confirmed outstanding defects, not completed translations.
The next change must localize the shared address providers without inventing
kinship or status, and give the clue whole-word formatting on its actual portrait
path. Preserve V408's working rumor scope and the original4096-byte ITCM bound.
The clue capture is evidence only and is not archived as a finalized guide screen.

## Goal scope

No armor or weapon was acquired/equipped, no Gallery/ending unlock was synthesized,
and no ROM changed. All18 plaque/hint entries remain fully_completed:false and
all22 historical requirements stay in the ledger. The graphics goal remains active.
Low-resolution Online images remain user-exempt. Revisit older record-based checks
on actual full completion. These are targeted emulator runs, not a full playthrough.
