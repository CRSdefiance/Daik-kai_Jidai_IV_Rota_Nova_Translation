# TITLEMAP deferred placement and bounds V222

V221 completed the source reads, palette preparation, bitmap construction and
source-art review for all 56 maps. This turn corrects the final-call assumptions
and verifies their native deferred placement. **V218 remains unchanged; the full
goal is active.**

## Actual caller arguments

The point literal at `0204BC88` selects `02116214`, whose values are (52,36).
The value at `0204BC8C` is **401**, an integer drawing priority. It is not a
source/destination coordinate pointer. The earlier direct-blit probe supplied an
incorrect destination object and treated this argument as a pointer.

The real caller obtains the native copy-interface adjustment from the primary
vtable's negative metadata. The map object's adjustment is +30 (hex); its queued
drawable state is at +44. Both are verified from the actual native constructors.

## All 56 native placements verified

Every case executes the unchanged source bitmap constructor, map copy-interface
and `020D4988` deferred queue routine, with the original map data/palette.

- Drawing priority is exactly 401.
- Destination bounds are exactly **(52,36)–(204,156)**, covering 152x120 pixels.
- All bounds fit a 256x192 DS screen.
- The actual native queue owner, source bytes, surrounding object guards,
  saved registers, stack and return are checked.
- No source image, border, marker or palette entry changes.

Active scene one and a null parent widget are explicit queue fixtures. They do
not establish legitimate map selection or a physical display result.

## Presentation scope correction

`020C9904` processes the UI hierarchy; it is not a direct bitmap pixel-copy
routine. This corrects the V221 description of that follow-up call as a scene
render. The previous fixture's failure does not establish a game defect.

This proof establishes native deferred placement and bounds, not final pixels,
GPU alpha/composition, input or gameplay selection. Those final display checks
remain separate and open. Do not claim an immediate framebuffer copy from the
native queue result.

## Evidence and remaining work

- `scripts/verify_titlemap_queue_v222.py`, focused Ruff passing.
- `work/analysis/titlemap_v222/native_queue_proof.json`: 56 source-pinned cases.
- V221 native source evidence and art-retain decisions remain valid.

The combined V218 ROM and its exact patch are retained. Remaining embedded/raw
consumers, four Online screenshot bodies/chat, confirmed-name consistency,
contextual/native display and final whole-scope gameplay audit remain in the goal.
Older record-based checks remain to revisit when the full goal is complete.
