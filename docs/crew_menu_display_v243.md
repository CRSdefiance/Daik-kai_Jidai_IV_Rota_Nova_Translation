# Live Crew Setup and complete radial-menu captions

V243 is verification research. V241 remains the registered experimental candidate;
no ROM, patch or translation asset changes. The previous turn made progress on
both live gender symbols and four status plaques. This turn reaches actual Crew
Setup and verifies eight additional live captions within the full graphics goal.

## Normal input and actual DS interface

Start Lil's route, advance her normal opening to Amsterdam, open X/Menu, move
DOWN twice from Route Map to Crew Setup and select it. The DS interface is
**Assign Sailors**, with live Assigned/Reserve/Range fields, a ship row and ordinary
controller prompts. Selecting the ship opens the sailor's “Good with this?”
confirmation; B returns, and L switches the assignment mode. These screens were
visually inspected and the exact button schedule is saved. B returns to the radial
menu, and UP visits all six entries, with the highlighted entry on the left.

The older Set Crew/Balance/Minimum/Done atlas layout is not displayed by this
observed DS path. This is not a global unused-data claim or proof that those
stored cells never appear elsewhere. Their consumer/display questions remain open.

## Eight complete displayed captions

| Caption | Frame | Native font advance | Complete screen bounds |
|---|---:|---:|---|
| Crew Setup | 11200 | 5 | `[59,259,110,270]` |
| Deck View | 11500 | 5 | `[61,259,107,270]` |
| Route Map | 11800 | 5 | `[61,259,107,270]` |
| Info | 12100 | 5 | `[74,259,95,270]` |
| Items | 12400 | 5 | `[71,259,97,270]` |
| Functions | 12700 | 5 | `[61,259,107,270]` |
| No | 10300 | 6 | `[134,362,146,373]` |
| Yes | 10300 | 6 | `[202,362,220,373]` |

All **637 native-font ink pixels** and **2,926 ink/blank-cell pixels** pass.
The comparisons include complete first/last letters, internal spaces and the
absence of unexpected foreground within each full caption extent. Every caption
fits in the lower viewport. The menu captions use overlapping six-column glyph
cells at five-pixel advance; transparent foreground masks are combined without
erasing another glyph's ink. Yes/No use ordinary six-pixel advance. All eight words
were visually reviewed and read as natural English controls.

These live glyph masks match the original font and differ from the tested older
baked marker-caption masks. That establishes complete displayed words, not the
exact panel/atlas draw path. A font-pixel match alone does not identify the bitmap
resource that supplies the surrounding panel. No legacy atlas cell is cleared by
this evidence. In particular, the Yes/No check is the actual controller prompt,
not a claim that the translated frame-atlas Yes/No cells were selected.

## Evidence and limits

- `scripts/verify_crew_menu_live_v243.py`: execution and Ruff pass.
- `work/analysis/crew_buttons_v243/live_caption_proof.json`.
- `work/emulation_v193/crew_buttons_v243/navigation/capture_report.json`: actual
  normal controller schedule, native framebuffer PNG identities and final RAM export.
- `work/analysis/crew_buttons_v243/marker_bank0_source.png`: stored atlas inspection;
  this is explicitly a first-bank source preview, not native palette proof.

The ROM/core/PNG identities and empty callback-error list pass. The pinned DeSmuME
core uses interpreter, one core, English firmware and native256×384 software
rendering. No savestate, RAM injection or fixture ROM is used; the process is
terminal. Crew-allocation arithmetic and every alternate action are not inferred
from caption verification. Other palette banks, actual legacy atlas consumers and
embedded CMMNIMG relationships remain separate.

The full goal remains active: four unreadable Online bodies, other embedded/
environmental/alternate displays, confirmed-name consistency and full-scope final
visual/gameplay/integration work remain. Revisit the older record-based checks at
eventual completion as requested.
