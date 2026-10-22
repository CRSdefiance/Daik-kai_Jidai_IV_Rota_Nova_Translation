# V659: resolve Lil's 63-pixel transition edge at the actual scanline read

The previous V658 goal turn made progress by checking the pure-helper return
search gap and saving its evidence. This turn addresses V648's concrete remaining
movie-to-scene comparison. It does not change the ROM or artwork.

## Specific open question

V648 verified the original dissolve painter, all 16 source phases and the whole
stored bitmaps. At Lil frame2865, however, current and Japanese screenshots
differed at 63 positions on row79. End-of-frame VRAM could not establish exactly
when that row was displayed. A fitted frame delay was explicitly rejected.

The new test observes the source bitmap immediately before the pinned emulator's
original per-line renderer executes. It then predicts display colors using the
original ROM photograph and independently composed ROM movie backdrop. Screenshot
pixels and the finished renderer framebuffer are not used as expected source art.

## Diagnostic observer and source binding

The exact-hash DeSmuME95b4d79 DLL remains unchanged on disk. Only the isolated
diagnostic process temporarily detours the three host GPUSubsystem RenderLine
entry prologues. The PE's declared function ranges, original HBlank call sites,
VCount SFORMAT address and original GPU-pointer/line arguments bind all three
methods to the local pinned C++ source. The observed output format is BGR555.

Original prologues contain only pushes, stack adjustment and register copies;
none needs PC-relative relocation. Trampolines execute those exact instructions
and resume the original method. Twelve independent x64 emulation controls compare
all general registers, flags and the complete stack for original/relocated prefixes
at line arguments0/79/80/191. Each actual renderer call executes once. All three
entry prologues are restored before shutdown and the DLL file hash remains exact.

The callback reads bitmap source rows, IO registers and original ARM9 program
positions/registers. It does not write the game ROM, emulated CPU registers,
RAM, VRAM or inputs. Normal rendering still performs its normal writes. This is
host instrumentation, not an unmodified-core gameplay run; comparison controls
are required before credit is assigned.

An initial setup attempt stopped before retro_init and before any emulated frame:
the existing reader caches tag names, whereas 9REG has two legitimate SFORMAT
schemas. Separate reader instances resolve hardware IO versus CPU registers.
That failure is retained; no live process was restarted.

## Four ordinary cold boots and unchanged captured behavior

Current V653 and the untouched Japanese ROM each run an observed and an
unmodified-core baseline through frame2868, with identical ordinary Lil New Game
inputs. All four processes finish normally. No save, savestate, location,
inventory, health, money, unlock, outcome or movie-substitution fixture is used.

All 30 observed/baseline full two-screen pairs match every RGB pixel: 2,949,120
positions. The twelve transition frames2857–2868 each supply all 192 original
render calls in both builds: 4,608 observed scanlines. The observer produces no
errors or duplicate/missing rows. Captures at 2865 and2868 were visually inspected.
The partial patterns are the original dissolve, not untranslated lettering.

## Source pixels and exact same-frame composition

Every sampled source word is either transparent zero or the exact original
photograph color at that coordinate. All 1,179,648 words across the two twelve-frame
traces pass. Row opacity matches an original 4x4 dissolve phase; the prior complete
native phase-family proof is retained, and every instruction it executed remains
byte-exact between current and clean code.

At every observed row, original bankD mapping, BG3 direct-color format/priority,
identity horizontal affine mapping and y=line*256 hold. The 3D layer has lower
priority; blending and master brightness are disabled. This independently binds
the sampled source position and its visible/transparent interpretation.

Five CPU/GPU exports per build bind the complete original photo palette/indices,
actual Lil selection and original FLS texture/geometry resources. Their ten
complete upper-screen compositions match all 491,520 RGB positions in the same
displayed frames. The serialized 3D framebuffer is compared only as a diagnostic;
expected backdrop pixels come from ROM textures and committed geometry. There is
no per-frame/per-row delay fitting, screenshot-selected source phase, pixel waiver
or captured finished-framebuffer source.

## The exact edge and original DMA program positions

At frame2865, only row79 differs. Its original threshold5 cell is x congruent3
modulo4. At the observed read, current source opacity is still zero at those
64 positions; the clean source has the original photo word. The composed source
images predict exactly the 63 observed RGB differences. The remaining position,
x143/y79, has coincident photo and movie-backdrop RGB and is also checked.

The captured interpreter positions independently agree with that ordering:

- Current is at020E2750 in the original bitmap-copy setup, with channel3,
  source022F9794, destination06000000 and98304-byte length in its argument registers.
- Clean is at01FF98D4 after the original source/destination/control stores,
  with channel3, the same source/destination and control8000C000 retained in the
  original setup registers. The relevant complete code spans are clean-exact.

The observed raw IO DMA fields are not treated as an authoritative DMA-controller
state mirror. The finding follows actual source rows, interpreter positions and
original store order, not a guess from those fields or host wall-clock time.

This resolves the specific Lil63-pixel comparison retained by V648. It establishes
the pinned core's observed scanline composition, not an independent simulation
of every DMA cycle or accuracy on physical hardware. Other routes, transitions
and unsampled frames retain their existing evidence and limits.

## Evidence and unchanged graphics scope

- Proof: `work/analysis/transition_scanlines_v659/proof.json`.
- Verify: `python scripts/verify_transition_scanlines_v659.py`; targeted Ruff passes.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V659 Transition scanlines`.
- Diagnostic observed captures and unmodified-core baselines are labeled separately.
  No transition frame is promoted as a guide/publication image.
- ROM remains `out/all_routes_combined_v653_candidate.nds`, SHA256
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.

No ROM, artwork, patch, manifest, registry, canonical or release-pointer change
is required. All 18 original plaque/hint entries remain incomplete and all
22 historical scope objects remain unchanged. Other actual controls/cards/legacy
art, equipment/material review, broader movie/gameplay coverage and acceptance
remain open. The low-resolution Online exclusions, brown-mark retention and
after-goal older record checks remain in force. The full graphics goal is active.
