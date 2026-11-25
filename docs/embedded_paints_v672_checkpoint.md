# V672: embedded caption palettes and complete controlled native crops

## Gap addressed

V602 established that five English captions in the loose Frame atlas also
exist in the right half of CMMNIMG.DK4 block5. That was exact index-shape proof,
not color or alpha equivalence. V672 checks the retained external palette words
and native drawing behavior without inventing a legacy loader or its descriptor
creator. V666 remains the unchanged current compiled experimental candidate.

## Original/native component result

Both complete512x256 original/current atlas index arrays equal their respective
256-wide loose Marker and Frame halves. Palette block4 remains byte-exact to the
clean ROM:83 banks,16 colors each. All307 current compact-font pixels in Pick
Cargo, Pick Ship, Done, Rank and Cancel match independently generated full font
masks, including complete leading/trailing letters and spaces.

The original corner-copy function01FF92D8, its clipper and every executed
instruction remain exact to the clean ROM. Scratch descriptors point at unchanged
legacy palette/packed-index bytes. Their width512/height256, source rectangle
[440,32,72,24], destination[16,40], palette bank and flags are explicit test
inputs. They are not claimed to be values made by an original legacy parent.

All664 cases pass: original Japanese/current English x83 banks x2 modes x2
backgrounds. All32,636,928 destination words match the independent palette/index
model, including untouched screen regions. Every expected source paint byte is
written; no completed output is read, no outside-crop write occurs, all source
bytes and surrounding guards remain exact, and each full call returns with its
saved registers and stack intact.

Flag4 follows palette-bit15 alpha. Flag260 sets bit8 and copies every palette
word regardless of bit15. With these raw legacy palette bytes, primary ink9 is
written under flag4 only in banks74 and82. Under flag260 it is written in all
banks, but11 banks give it the same RGB5 color as background index0. These are
explicit component contracts, not discovered defects in an actual game screen.
The original and translated primary-ink/background alpha and contrast classes
match for each contract. Original Japanese antialias shade masks are not equated
to the deliberate monochrome English compact-font masks.

## Exact observed palette relationship

Clean source banks0..40 establish a single32-entry RGB5 channel lookup; independent
banks41..82 verify it. Applying that declared lookup per channel and setting
bit15 exactly when the complete legacy word is nonzero reproduces every one of
1328 modern palette words, for both Marker and Frame in both original/current
ROMs. Together with complete index-half equality this establishes the declared
mapped-storage relationship for all10,878,976 atlas pixels/bank combinations per
version. It does not identify or execute a runtime conversion routine.

Naive raw-word/opacity-only alternatives fail and their mismatch counts are
retained. The same map applied to CMMNIMG's distinct portrait store matches only
39817 of637952 pixel colors at corresponding positions, so it cannot be promoted
to a global legacy converter or portrait-equivalence claim. No palette or asset
bytes are changed to force a relationship.

## Retained correction and visual review

An initial verifier assertion incorrectly assumed original Japanese captions
used only indices0/9. Source inspection found antialias indices1/4/5/6 as well.
The failed source and log are retained. The corrected verifier paints every
actual original index and separately checks current monochrome font pixels;
no ROM, native code, palette or source art changes.

All16 selected controlled caption crops were visually inspected in the8-row
paired4x review sheet. Both mode behavior and complete current captions are shown,
including genuinely transparent cases. These are derived views of verified
native software output, not emulator screenshots or guide candidates.

## Scope still open

Original archive loading, descriptor creation, actual palette/mode selection,
native GPU composition and ordinary gameplay consumers remain unresolved.
Confirm and all five miniature control contexts stay open. No global non-use
or actual legacy display credit follows. All18 plaques remain incomplete, all22
historical requirement objects remain exact, and the full graphics goal stays
active with the older-record follow-up and final acceptance still required.

## Reproduction and storage

- Native replay: `scripts/verify_embedded_paints_v672.py`.
- Source-color relation/review: `scripts/relate_common_palette_v672.py`.
- Proof: `work/analysis/embedded_paints_v672/native_embedded_paint_proof.json`.
- Relation: `work/analysis/embedded_paints_v672/palette_correspondence.json`.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V672 Embedded caption painting`.
- Current candidate: `out/all_routes_combined_v666_candidate.nds`.
- SHA256: `706350a55a058b7a87b67d396333ed397dac664ba36ea378161d18fd085ba121`.

No ROM, exact patch, manifest, registry, canonical or release-pointer changes.
