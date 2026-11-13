# V479 actual captain portraits and legacy-read distinction

V474 is unchanged. Original portrait-loop screen resources resolve charselectinfo
and charselect. A fresh cold boot opens Choose Captain through ordinary New Game
navigation. Right-input sequence displays Rafael,Hodram,Lil,Rafael. Maria is not
observed in this navigation state;no unlock/progress flags are synthesized and
no exact unlock rule is asserted here.

Every visible portrait matches its native personbustup00/01/02 PXL at native
colour precision,all14144 pixels per104x136 image,bounds76,28,180,164. Four observed
instances include one repeated Rafael view. Current files remain clean-byte-identical.
Complete name-field masks pass for Rafael,Castor,Hodram,Joakim,Bergstrom,Lil and
Argot. The complete Camille spelling in Lil's selection biography also passes.
This verifies the observed names,not a new complete editorial review of every bio.

The genuine2400-frame RAM snapshot contains all14144 bytes of original SLACK
block17 at2233040,the destination loaded from the original reader literal9F0B4.
The source constructor's loop selects14–17 as established in V478. The actual
block17 buffer confirms archive access during captain selection.

The raw14–17 payloads differ from the corresponding loose PXL pixel arrays.
Binding raw14 to the loose00 palette did not match the displayed picture;the
loose PXL itself matched exactly. Therefore archive access and visible PXL pixels
are recorded separately. No unproved raw palette/colour interpretation,raw comic
display,global unused-file claim or fourth-captain display credit is granted.

Verifier: scripts/verify_portrait_selection_v479.py;Ruff passes.
Proof: work/analysis/portrait_selection_v479/selection_proof.json.
Report: work/emulation_v193/portrait_selection_v479/capture_report.json.

The finalized Lil selection screenshot is copied unchanged to E Screenshots.
No new ROM/patch. These are targeted DeSmuME checks,not hardware or full-playthrough
proof. All22 historical requirements and all18 incomplete plaques remain under
audit. Raw block19 and other legacy/environment/deep contexts remain open. Revisit
older record-based checks at actual full-goal completion.
