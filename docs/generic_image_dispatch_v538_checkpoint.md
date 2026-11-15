# V538 connected image instruction and native framebuffer checks

Production remains experimental V534. This checkpoint maps the second original
image instruction and verifies the corresponding native widget in isolated
source-opcode fixtures. No production graphics, prose, patch or canonical base
changes.

## Original event instruction

Main dispatcher 0202A510 selects major opcode 2. Its subopcode 8 reaches
02029FFC. Both instruction forms pass the image kind and low-byte index to the
original widget at 02028A64, then 02028E8C. Kind 3 reaches 020470B4.

- Four-byte form: bit 15 of the second halfword is set.
- Eight-byte form: bit 15 is clear and two more halfwords follow.
- Kind is bits 8–9; the image index is bits 0–7.

All 256 index values are executed through each form: 512 connected cases.
The diagnostic stream is supplied, while the widget, vtables, registered owners
and cache come from actual captured V534 game RAM. Original dispatch, descriptor
construction, cleanup, view adoption, and complete cache loading execute in one
invocation. Only SDK filesystem operations are bridged. Execution stops after
widget setup and before its frame wait; this does not prove a complete controller
return, GPU binding or ordinary event reachability.

Every complete image header, palette and pixel payload matches its actual ROM
file. Input operands, length and neighboring guards remain intact; all file
handles close. No read from the legacy SLACK shared archive buffer occurs.

| Index | Selected loose image |
| --- | --- |
| 0–12 | Same-numbered slackimg PXL |
| 13–19 | slackimg12.pxl, the name-label sprite |
| 20–255 | slackimg20.pxl, the original Press a button! fallback |

This rules out raw comic selection through this whole index domain of the
identified instruction. Other archive consumers remain open; no global unused
resource claim is made.

## Native framebuffer verification

Fourteen research fixtures each replace one existing four-byte scene instruction
in SC0 block 44 at offset 30. The replacement uses the original kind-3 instruction
from clean SC1 block 296 at offset 12, varying only its image index. All instruction
offsets and lengths, translated prose, other controls, other blocks, art and ROM
components remain exact to production V534. These are research-only ROMs on E,
not playable release candidates.

Each fixture cold boots with the same ordinary Rafael opening inputs and runs
9,000 frames in DeSmuME, without a savestate or donor save. All eleven source
paintings (indices 0–10), the complete Name/Middle/Last/Company/Birth sprite,
its index-19 alias, and the complete Press a button! artwork match every nonzero
source-index pixel at native five-bit color precision. This includes all visible
lettering, edges and shadows. Their native rectangles fit within the upper screen.

The creature paintings display at (64,20), the labels at (106,20), and the
156×24 press-button graphic at (50,20). The two label cases each preserve all
2,581 nonzero source pixels. Index 19 visibly displays labels rather than the
320×240 raw comic.

Palette-zero transparency, every fade frame and legitimate story progression
are not inferred from these matches. Image 11's different original caller at
020640EC is outside this fourteen-case GPU test.

## Conservative reference census

All byte positions of each SC block and the complete EV files are scanned in
clean/current ROMs. EV files have VE headers and a declared body length equal to
file length minus 96; they are not ILNK containers or decoded instruction streams.
The initial census assumption was corrected from the actual headers.

Positive patterns remain candidates: prose and table fields can mimic opcodes.
Five specific clean/current source leads identify kind-3 image patterns 7/8/9
in Hodram blocks 115, 294, 296, 299 and 311. Their runtime event triggers remain
unverified. There are no patterns for indices 13–19 in the checked files; this is
a bounded encoding census, not a universal non-use claim.

## Evidence and remaining work

- `scripts/verify_generic_image_dispatch_v538.py` and `connected_dispatch_proof.json`.
- `scripts/prepare_generic_image_gpu_v538.py`: bounded research-fixture generator.
- `scripts/verify_generic_image_gpu_v538.py` and `native_GPU_proof.json`.
- Evidence and fixtures: `work/analysis/generic_image_dispatch_v538/`.
- Native captures: `E:/Rota Nova translations/Generated/work/emulation_v193/generic_image_gpu_v538_*`.
- Selected screenshots: `E:/Rota Nova translations/Screenshots/Test fixtures/generic_images_v538`.

All three scripts pass Ruff. Production V534 remains SHA-256
`cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45`.
All 22 original requirements and all 18 incomplete plaque/hint entries remain.
Raw legacy consumers, reconstruction underneath old Japanese lettering, other
contexts and hardware verification are still open. The full graphics goal is
active. Revisit older record-based checks at full completion.
