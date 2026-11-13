# Original event-still routing V426

V414 remains unchanged. The previous goal turn resolved the normal environmental
town assignments. This turn narrows the unknown viewer context of the eight white
village-caption cards, including image207's preserved clipped source fragment.

## Gallery selection

Original code02042C74–02042C90 initializes four route-list counts:46,41,39,38.
Original selection02042E5C–02042ECC chooses their image tables and loads the
matching count intoR9. R8 is the separate description-pointer table, not a count
or image-table endpoint. Early exploratory interpretations ofR8 were rejected.

Every one of the164 selections executes the exact argument-load fragment
02042F58–02042F68, stopping immediately before the real event-image reader call
at02042F6C. Clean and current tables, counts and arguments match:328 cases.
The village cards168–171 and206–209 occur in **none** of these lists.
Gallery unlocks therefore do not expose these cards through this original viewer.
This is a bounded conclusion about this viewer's tables, not an unused-art claim.

## Story scene selection

The original event-image reader02028B74 formats/loads evstill%03u.pxl.
Its scene parent02028AA8 is called at02029FB4. Original instructions at02029F94
read the second halfword of a supplied scene operand; bit15 selects the event-still
branch and the low8 bits supply the image number. All256 low-byte values with
two high-byte patterns execute in clean/current machines:1024 exact decode cases.
For example, operand80CF selects image207. The source operand bytes are unchanged.

This fragment receives explicit owner/stream inputs and stops at the parent call.
It does not identify the enclosing instruction opcode or prove that an actual
route contains a reachable image207 instruction. Searching arbitrary script bytes
for80CF would not prove instruction boundaries or live usage.

## Scope and next action

The relevant code is clean-exact. All eight current card filenames, dimensions,
source/current hashes and decoded operands are pinned in the proof. V330's complete
caption/source-fragment preservation evidence remains applicable. No ROM, save,
unlock or progress flag is changed; no simulated screenshot enters the guide.

Next, trace the instruction handler's dispatch and parse original route instruction
boundaries, then test any legitimate reachable scene. The raw comic consumer,
other legacy formats, normal Gallery/ending playback and broader graphics gates
remain open. All18 plaques remain fully_completed:false. Full goal is incomplete.
Revisit older record-based checks at actual completion.

Verifier:scripts/verify_event_still_routing_v426.py. Proof:
work/analysis/event_still_routing_v426/routing_proof.json. Targeted Ruff passes.
