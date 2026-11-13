# Village-card route reference census V427

V414 remains unchanged. V426 excluded the eight white village-caption cards from
all164 original Gallery image choices. This checkpoint traces the complete original
story dispatch and checks the entire four-route archive set for direct references.

## Complete original dispatch to the scene call

Original main dispatcher0202A510 reads the top three bits of the first halfword.
Major opcode2 calls02029AA0, whose five-bit subopcode6 reaches02029F50. This branch
adds two bytes to the default two-byte instruction length. With bit15 of the second
halfword set, its low8 bits identify the event image passed to02028AA8 at02029FB4.
Thus the direct instruction encoding is first halfword46xx, followed by a halfword
with bit15 set and the desired image index in its low byte. Other low-byte flags
of the first word do not change that image-selection dispatch.

Full original code executes from the main dispatch to that actual parent call in
160 clean/current cases covering all eight card IDs, five flag patterns and two
operand high-byte patterns. Image arguments, four-byte lengths, untouched source
operands and neighbor guards pass. Relevant code is clean-exact. The supplied
owner/stream is an isolated decoder input, not a live route state or scene display.

## Conservative negative reference census

All bytes of all343/325/336/303 blocks in SC0/SC1/SC2/SC3 are scanned, in clean
and current ROMs:2614 blocks,2645278 potential four-byte positions. Every byte
position is included, even odd offsets, headers and padding. This deliberately
includes more positions than a correctly decoded instruction stream could use.

**Zero** positions encode any of images168,169,170,171,206,207,208,209 through this
direct event-image instruction. Instruction-boundary filtering cannot introduce
a missing byte pattern. Other positive image-like patterns are recorded only as
byte-pattern candidates; their many matches inside Japanese prose are not counted
as real instructions or used as reachability evidence.

This proves that none of the eight cards is referenced by this direct encoding in
the checked original/current route archives. Combined with V426, it rules out two
specific expected display paths. It does not rule out generated operands, another
container, an indirect caller or later runtime changes, and is not a global unused
resource claim. No ordinary scene/ending/Gallery display is credited.

## Audit disposition

Retain the reviewed English cards and exact image207 source fragment. Their unknown
live use is now specifically an indirect/generated-consumer question, rather than
an unresolved direct route instruction or Gallery-table question. The raw comics,
other legacy formats, normal environmental visits and the remaining graphics and
plaque contexts stay open. All18 plaques remain fully_completed:false. The full
goal remains active. Revisit older record-based checks at actual completion.

Verifier:scripts/verify_village_card_references_v427.py. Proof:
work/analysis/village_card_references_v427/reference_proof.json. Targeted Ruff passes.
No ROM, save, unlock, artwork or finalized guide image changed.
