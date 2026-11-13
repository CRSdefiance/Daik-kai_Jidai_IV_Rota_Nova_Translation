# Native graphics file-opening paths V301

V301 is research on the unchanged registered V299 candidate, SHA256
`9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f`.
The prior turn made verified progress on the current plaque audit. This turn adds
lower-level file-opening and generated-FLS caller evidence, beyond the V264
generic archive-wrapper census. No ROM, artwork, patch or profile changes.

## Complete SDK filename-open call census

Every current ARM9 MainCodeFile section and declared overlay is scanned for
aligned ARM BL, Thumb BL/BLX and literal pointers to SDK open `0x020DED50`.
There are 25 direct ARM calls, with no matching Thumb calls or function literals.
Each actual main-section caller context is checked byte-for-byte against clean.
The current candidate manifest and release-stack hashes match.

Twenty call sites load a literal filename into r1. Their exact PC-relative
instructions and string pointers resolve to existing DSOBJ, DSOBJR, OCINIT,
SKYWALL, OCETC, GMONS, DSCHR and RACE resources. Resolution retains original
requested spelling, the unique case-insensitive ROM path and the complete file
hash. This is a static argument/call census, not a claim that all 20 full parents
were executed or that every resulting image was displayed.

The five remaining calls obtain their filenames from these sources:

| SDK call | Native argument source |
|---|---|
| `020B7178` | Caller-supplied whole-file reader filename |
| `020D0474` | Caller-supplied archive/cache filename |
| `020D2B9C` | Generated FLS filename on the native stack |
| `020D6598` | Cached graphics descriptor field +0C |
| `02100348` | Caller-supplied stream filename |

The whole-file reader has two direct callers. Their original formatting literals
are `/evstill/evstill%03u.pxl` and `/towngrp/towngrp%02u.pxl`. They provide specific
event-still and town-background paths to follow rather than evidence of a raw
comic/archive consumer. The generic readers are not restricted to those names by
this census; computed/indirect paths remain possible.

## Actual generated FLS filenames

Original native entry `020D2B1C` copies `FLS\\logo.fls` for index0 and uses the
original sprintf routine to construct `FLS\\M%02d.fls` for indices20 and above.
Fourteen valid cases cover logo and M20 through M32, exactly all files in the
ROM's `/FLS/` family. Nineteen indices1 through19 are rejected without filesystem
access. A negative signed index is also rejected; missing M33 returns through
the original missing-file branch. There are 21 rejection/missing cases total.

Each valid case executes the original stack frame, filename construction, SDK
file-object constructor and open call, stopping immediately afterward at020D2BA0.
Only SDK existence/open results are bridged, mapping each requested name to its
actual existing ROM file. No decoder, palette, playback or GPU operation is
bridged or credited as tested. Native valid-case full parent return is not claimed;
invalid/missing cases do return with original stack/register ABI intact.

Nested sprintf/SDK frames reach 920 bytes below the initial stack. The initial
256-byte guard assumption was too narrow; the test records native writes and
checks untouched guards below a bounded 2KiB nested stack area and above the
caller stack. The filename and file-object ownership bounds remain asserted.
This is a test-fixture correction, not a ROM change.

Six direct callers reach the actual FLS entry. Original setup instructions are
recorded at2028A40,2029D74,2040C1C,207D664,207D694 and207D6B0. These are actual
scan addresses; they must not be substituted with manually converted guesses.
No direct Thumb or literal function pointer to that entry is found.

## Captain-dependent selection from current captured player data

The original2040C08 block calls the actual207F244 getter, adds29 to its result,
clears r1/r2/r3 and calls the FLS loader. Hash-checked read-only player RAM from
the four fresh V299 route runs supplies the current captain context. The actual
getter and caller prepare M29/M30/M31/M32 for Rafael/Hodram/Lil/Maria respectively.
Every non-stack RAM byte remains unchanged. There is no getter bridge, altered
gameplay state or loaded savestate.

This is a controlled caller-argument test. It does not prove the original trigger,
unlock, full movie parent, decoder or GPU display. Maria's source capture comes
from the declared one-byte selection test fixture, not a legitimate unlock.

## Remaining graphics scope

The root `/m02_03.fls` file is outside the generated `/FLS/` family. Its consumer
is not established by these two whole-file formats or the FLS filename tests.
Neither the generated FLS index19 rejection nor the loose SLACK slot19 fallback
proves the native use of SLACKIMG block19's raw comic planes. Keep all 11 legacy
layout/composition gates open and preserve their source/translated artwork.

No new raw-comic viewer is found by this step. No globally unused archive claim
is made. Continue with original FLS decoder/playback and the cached-descriptor/
stream callers, plus any indirect/generated legacy readers. Follow actual
consumers rather than forcing raw comic data into the loose-image helper.

All 18 plaque/hint entries remain incomplete under the user's ongoing audit.
Online low-resolution image translation remains exempt. V299 stays latest and
experimental. The graphics goal remains active/incomplete; revisit older
record-based checks at actual completion.

Evidence: `work/analysis/graphics_file_open_v301/proof.json` and
`caller_argument_proof.json`, with verification logs. Ruff passes for both new
scripts. No process is left running.
