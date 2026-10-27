# Artwork caption release V298

V298 integrates the reviewed artwork name captions into the complete combined
release. It updates 15 scene captions and one Gallery description from the prior
Raphael/Kamil spellings to the locked Rafael/Camille spellings. Every other word,
caption subject, numbered variant and graphic is retained.

## Registered candidate identities

| Item | Identity |
|---|---|
| Candidate | `out/all_routes_combined_v298_candidate.nds` |
| Candidate SHA256 | `0e57a87c72d711b3cab3ac29ea8c7bb51c1ab1fd3b30ac3551983d1ee31a5a5b` |
| Patch | `out/all_routes_combined_v298_candidate.xdelta` |
| Patch SHA256 | `c94fe80c7e10216c0500b8ca62e95239291e930badb35b340dc84c03af527b0e` |
| Profile | `all-routes-unified-v298` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Exact inherited comparison candidate | `out/all_routes_combined_v296_candidate.nds` |
| Comparison SHA256 | `6096fb457d460c53964f1fe3c7aac33e152ac7eef28fefe6309e202760497833` |
| Clean patch input | `work/clean.nds` |
| Clean input SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Status | Experimental; not promoted or user accepted |

The neighboring manifest identifies the canonical base, complete registry hash,
all 467 inherited batches and accepted requirements, every inherited release
stage, caption configuration/dependency hashes, changed paths and changed records.
No accepted layer is omitted. `artwork_name_captions_release_v1.json` adds the
source-locked stage after the V296 actor repair. All inherited stages and batches
are identical to the V296 profile. Full V296 reproduces byte-for-byte both before
and after the shared builder change.

## Preservation and native display checks

Only `/__arm9__.bin` changes versus V296: 16 caption pointers, complete appended
strings, owned-pool loading/cache wrapper and size/arena bookkeeping. The inherited
82,400-byte payload prefix and ITCM/DTCM sections remain exact. The new payload is
82,880 bytes. All other native code and string/table bytes are preserved. All ROM
data files, route scripts, fonts, graphics, ARM7, overlay tables, icon/banner and
entry addresses are identical to V296. All 19,254 original actor fields pass the
stable native-offset gate. No script or dialogue renderer changes.

The registered candidate ARM9 is byte-identical to the previously reviewed V283
caption research target. The verifier also executes all 164 actual scene-caption
table selections on both 4-bit and 16-bit 256x192 surfaces: 328 complete cases.
Eight complete Gallery composites execute the four captain descriptions on both
formats, including the original overlay bitmap clear, centered Event Scenes title,
description, context/font calls and cleanup. No draw/clear instruction bridges.
Every complete output canvas matches independently decoded native font pixels;
first/internal/final letters, centering, bounds, header/stack/register guards pass.
Ruff passes. The clean-input patch reconstructs the candidate byte-for-byte.

Route/index, owner view, caller frames and font metrics are fixtures in these
native CPU checks. Original unlock conditions, user navigation and final GPU
composition of the changed Gallery/scene captions remain unverified.

## Actual targeted emulator run

A fresh DeSmuME cold boot completes 20,000 frames with ordinary scheduled inputs,
no loaded state, no RAM injection and no callback errors. The captured frames
show the title menu, New Game, Lil selection, her opening and Amsterdam signs and
shopkeeper UI. Six early title frames match the corresponding V296 captures
exactly. Frames 1200, 2000, 6000 and 20000 were visually inspected. All capture and
read-only RAM hashes pass. The process exited successfully.

The actual town dialogue reads "Bulk trade? Try the trade" / "house." Both lines
start at native x22, y296/y312. All 334 independent native font ink pixels match,
including complete leading/final letters and bounds. This is targeted emulator
evidence, not a complete route playthrough or hardware verification.

## Open gates and next integration

The candidate is experimental. User testing should include a fresh New Game,
normal dialogue, title/UI and legitimately unlocked Gallery/event scenes for each
captain, checking the Rafael/Camille captions and complete letters. Actual unlocked
Gallery and original deep-scene navigation remain open. No user acceptance or
canonical promotion is inferred from native tests.

V297's 444 reviewed route paragraphs and five shared name fields still need
registered integration with the pending COMMON/HELP work. The ordinary character
nameplate still says Kamil in this caption-only checkpoint; this is recorded as
pending full naming integration rather than claimed complete. Older caption
research targets and source review evidence are preserved.

All 18 plaque/hint entries and Armor/Weapon variants remain in the ongoing audit
with completion false. Broader native graphics consumer/crop/Gallery gates remain
open. Low-resolution Online promotional images are exempt by the user's direct
instruction. The full graphics goal remains active and incomplete. At actual
completion, revisit older record-based checks as requested.

Evidence: `work/analysis/artwork_caption_release_v298/release_proof.json`,
`transform_proof.json`, exact reconstructed ROM, build/reproduction logs, and
`work/emulation_v193/artwork_captions_v298/capture_report.json` plus PNG/RAM exports.
