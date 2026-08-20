# Standard-dialogue calibration

This note records the evidence behind the Phase 2 layout profile. It is deliberately
separate from any translation build. None of the work described here modifies a ROM.

## Offline findings

| Property | Result | Evidence |
|---|---:|---|
| ASCII advance | 6 px, fixed | ARM9 instruction at `+0xD169C` |
| Shift-JIS advance | 12 px, fixed | ARM9 instruction at `+0xD1674` |
| ASCII bitmap | 6 x 11 px | ARM9 glyph decoder at `+0xD1820` |
| ASCII table | 95 glyphs at `+0x125A60` | Codes `0x21`-`0x7F`, 11 bytes each |
| Full-width bitmap | 16 x 11 px | `KANJI.FNT`, 22 bytes per record |
| Full-width table | 3,340 glyphs | ARM9 map at `+0x125EC4` and exact file size |
| Line pitch | 16 px | Native screenshots and repeated baselines |
| Story dialogue content width | 216 px / 36 ASCII cells | Cold-boot SC0 boundary probe |
| Shared dialogue content width | 216 px / 36 ASCII cells | Cold-boot Market Info boundary probe |

`dk4tool audit-dialogue-font` validates seven renderer instruction signatures, the
Shift-JIS map ordering, glyph count, and exact `KANJI.FNT` size. It exits unsuccessfully
when the target ROM does not match those assumptions.

## Live calibration result

The disposable cold-boot probe was tested on 2026-08-05:

1. A 38-cell line wrapped its final two cells and a 39-cell line wrapped its final
   three. The story dialogue content width is therefore exactly 36 fixed-width ASCII
   cells, or 216 pixels.
2. For Raphael, `FI` displayed `Raphael`, `FA` displayed `Castor`, and `FO` displayed
   `Castor Co.`. Those substitutions use the normal glyph advances, so their live width
   depends on the current editable name/company value: 42, 36, and 60 pixels for the
   tested defaults.
3. Standalone `I` displayed the full-width Japanese first-person pronoun `僕`, occupying
   12 pixels. It is not a literal English capital I. English prose must continue to
   avoid that byte until the optional runtime renderer patch exists.

The help-window bound remains a separate calibration task. It must not inherit the
216-pixel story/shared value without its own evidence.

## Disposable live probe

The source-locked batch is `translations/standard_dialogue_calibration_probe.json`.
It changes only three records in Raphael's opening scene in `/data/SC0.DK4`:

| Record | Expected screen | Purpose |
|---|---|---|
| `DK4_MES_B44_R0025` | `38 cells: 1234567890123456789012345678` | Confirm that 228 pixels fit inside the dialogue box. |
| `DK4_MES_B44_R0039` | `39 cells: 12345678901234567890123456789` | Determine whether 234 pixels clip or cross the right boundary. |
| `DK4_MES_B44_R0067` | Four lines beginning `given:`, `family:`, `company:`, and `self:` | Observe the live width and value of each runtime substitution. |

Cold-boot the probe ROM, choose **New Game**, select **Raphael**, and advance through
the opening scene. Do not load a save state. Capture the whole screen for each of the
three probe messages, including the right dialogue-frame edge. Also note any clipping,
wrapping, dropped first character, Japanese text, or substituted value that runs into
the frame.

The probe is diagnostic only. It must not be renamed as a normal release, used as the
base of another build, or merged into a translation batch. Its observations have now
been incorporated into the offline `story` layout profile.

## Shared/help follow-up probe

The Market Info screenshot established that a 38-cell shared line wraps its final two
characters. The shared-message content width is therefore exactly 36 ASCII cells, or
216 pixels. This result is now encoded in the `shared` profile.

The second disposable probe uses two independent source-locked batches:

- `translations/shared_dialogue_calibration_probe.json`
- `translations/help_dialogue_calibration_probe.json`

The shared batch presents three boundary lines through early, independently reachable
screens:

| Expected line | Navigation target |
|---|---|
| `37 shared: ...` | Title screen **Opts**, then highlight/open **Sound** so its description appears. |
| `38 shared: ...` | In a city, open the **Market** and select **Market Info**. |
| `39 shared: ...` | Enter an ordinary market/shopkeeper interaction. |

The help batch replaces only the first `Game Overview` page and displays five lines
from 36 through 40 cells. Its exact in-game route remains unidentified; the title
**Extras** menu and the city **System/Function** menu were both ruled out by live
screenshots. Do not guess a route or load a save state from another ROM. When the route
is identified, capture the entire text window, including its right frame edge.

For every probe, record the longest line that remains on one row and the first line
that wraps or clips. Cold-boot the probe ROM and do not use save states.
