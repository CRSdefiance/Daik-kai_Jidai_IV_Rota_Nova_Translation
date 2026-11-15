# V680: original raw16 comic scaling and caption-edge preservation

V679 made progress through actual cached view headers, paired cold boots and a
123-file verified archive. This turn returns to the raw comic family. The current
experimental combined ROM remains V678; no art, dialogue, palette, native code,
patch, registry or release pointer changes.

## Native operation that accepts this source format

The original event-still loader's indexed8 fixed-canvas rejection was already
proved in V587. That borrowed filename/widget cannot clear these raw16 comics.
This checkpoint instead exercises the original scaled software-copy routine
01FF8E4C, whose direct16 branch accepts the320x240 source.

All21 current SLACKIMG block19 frames are loaded separately through original
0204704C and its original ILNK open/block-range/read/close code. Only SDK
filesystem operations are bridged to the exact current archive. Each requested
153600-byte source frame is reproduced exactly; all file handles close.

The source header, scratch address, source origin(0,0), full source size320x240,
destination and screen are **explicit isolated research inputs**. The descriptor
is not claimed to come from an original comic viewer. Original archive/read and
complete scaler code ranges are exact to the Japanese ROM. The full native
calls return with saved registers and stack intact.

## Full frame and clipping results

Each source frame executes two complete native cases:

- Full fit on screen0: destination[0,0,256,192], zero viewport origin.
- Clipped origin on screen1: the same destination with viewport origin(7,11),
  producing clipped destination[0,0,249,181].

All42 complete two-screen software buffers match an independent pixel-center
sampling formula, including untouched other-screen/outside pixels, all original
16-bit words and buffer/source guards:8,257,536 bytes. Four additional supplied
coordinate planes independently identify every selected source X/Y coordinate
under both conditions. A separate verifier reconstructs these outputs with a
source-forward midpoint model and checks every native output hash and saved RGB
plane.

The original scaler resamples the whole supplied source into the **clipped**
destination size. It does not render an unclipped large image and then crop its
left/top pixels. This source-bound behavior is retained; no general clipping
rule is imposed on other primitives or unknown comic parents.

All18 stored caption word planes still reproduce exactly from their source-locked
batch; the earlier331 stored character bounds remain applicable. Both first/final
characters of each caption retain visible contrast under both supplied native
scales:72 edge checks, zero missing edge contrasts. These are finite contrast
checks plus complete word-output checks, not a claim that each original source
pixel survives downsampling or that tiny text is legible on physical hardware.

All21 frame payloads remain exact to V506's reviewed artwork. The original brown
marks at frame6 rectangle[175,96,229,136] remain byte-exact to canonical source:
4320 bytes, SHA256
`3b0111f01e8f7a0857a723f28138d130e29caad046aa5d15f7367831ac1d6943`.
All original clear color high bits are copied without an opacity conversion.

## Visual review and limitations

Six labelled source/current/native-software comparison sheets cover all21 frames
and were opened. They preserve artist marks, decorative headings and earlier
English. The smaller caption typography remains visibly small; the controlled
scales retain their first/final contrast. No new source-text omission or cropped
edge letter was identified in this review. Existing uncertainty in reconstructed
paper, scenery and outlines remains documented.

The saved256x192 PNGs decode software-buffer color words as RGB. They are **not
emulator/GPU screenshots**. Direct-color high-bit alpha, real display composition,
the comic's original parent, actual chosen viewport and gameplay readability are
not cleared. No production high bit, source crop or art is changed to force a
different widget. This supplies a usable original native scaling contract, not
an original scene trigger or final comic acceptance.

## Evidence and full scope

- Producer: `scripts/research_comic_scaling_v680.py`.
- Independent verifier: `scripts/verify_comic_scaling_v680.py`.
- Analysis/proofs,42 software RGB planes and six review sheets:
  `work/analysis/comic_scaling_v680/` on E through the analysis junction.
- The exact executed producer is retained there. After its process completed,
  only import formatting changed; complete AST equivalence and both hashes are
  verified in `producer_source_provenance.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V680 Comic native scales`.
- Focused Ruff, native full-buffer assertions, independent reconstruction and
  final archive/hash checks pass.
- Candidate remains `out/all_routes_combined_v678_candidate.nds`, SHA256
  `d1aaf37bcb7dec218d200a5fa72a6c58e0fb50ab85a8bcb7766d4e749903e341`.

The latest plaque comparisons were presented for user material review; acceptance
is not assumed. All18 plaque/hint entries remain incomplete and all22 historical
requirement objects remain exact. Six small controls, eight village cards,
legacy/comic native consumers, source-restoration review, older record checks
and final acceptance remain in the active graphics goal. User Online exclusions
and brown-mark preservation remain in force. No new ROM, canonical promotion,
guide publication, commit or push is performed by this checkpoint.
