# Live Sailor Info: both gender symbols and four translated plaques

V242 is a verification iteration, not a new ROM. V241 remains the registered
experimental combined candidate, SHA-256
`d863f74ba3e5466f5a221ba93e00d53fd1588a32cecdd349006b7eb0698e8027`.
The previous turn made progress by finding, translating and integrating the
navigator Sort/Filter popup. This turn verifies additional actual graphic displays.

## Normal menu path

Start a new game, reach a town, open X/Menu, move UP from the highlighted Route Map
entry to **Info**, then select **Sailors**, a navigator and their information page.
The highlighted left-hand radial entry is the selection; the visible top entry is
not necessarily selected. The earlier failed navigation selected Route Map. This
correction reaches the original Sailor Info consumer without any fixture changes.

Two independent cold boots reach the screen:

| Route / person | Captured frame | Visible symbol |
|---|---:|---|
| Rafael | 16600 | Male |
| Janus | 16900 | Male |
| Claudio | 17200 | Male |
| Julio | 17500 | Male |
| Lil | 10500 | Female |

All five screens were visually reviewed. R selects the next navigator on the
Rafael route. Lil reaches Amsterdam through her ordinary opening and the same
Info/Sailors path. No savestate, RAM injection, selector cheat or fixture ROM is
used. Both emulator processes are terminal; captured RAM is a read-only export.

## Complete source pixels and actual palette selection

Both 16×16 gender cells display at `[84,76,100,92]`, inside the upper screen.
Their source origins are male `(232,96)` and female `(240,112)`, exactly as the
original native parent branches select in V240. The complete circle/arrow or cross,
background and every original border pixel match: **1,280 of1,280 pixels** across
the five observed cells. No clipping or missing symbol ink is present.

The marker stores **83 four-bit palette banks**, not just the first16 palette
entries used by the simple preview renderer. The original view descriptor's
`0x30` field selects **bank48**. This is a bank number, not palette-entry offset48.
Its exact stored BGR555 colors explain the live cell's dark blue background and
lighter border. Every displayed pixel matches that bank at native five-bit precision.
The earlier bank-zero source thumbnail does not establish this native palette.
No palette or decoder was changed to manufacture a match.

All four translated `/_pxl/personinfo.pxl` plaques also match their complete source
cells on all five screens:

| Plaque | Source and live bounds | Pixels per display |
|---|---|---:|
| Health | `[3,103,49,118]` | 690 |
| Mood | `[3,123,49,138]` | 690 |
| Level | `[3,143,49,158]` | 690 |
| HP | `[3,163,49,178]` | 690 |

The **13,800 plaque pixels** include full words, first/last letters, blank cells,
paper background and borders. No dropped leading character or old Japanese glyph
remnant appears in these complete cells. The marker and personinfo resources are
byte-identical to V218; this verification introduces no asset or ROM change.

## Evidence and limits

- `scripts/verify_person_info_live_v242.py --lil-frame 10500`: passes; Ruff passes.
- `work/analysis/person_info_v242/live_pixels.json`: all five cell/plaques cases,
  actual palette-bank hash, recorded PNG/report identities and source hashes.
- `work/emulation_v193/person_info_v242/town/`: Rafael-route cold boot and normal
  Info/Sailors selection/next-navigation captures.
- `work/emulation_v193/person_info_v242/lil/`: Lil-route cold boot and female case.
- Native parent crop evidence remains `work/analysis/gender_consumers_v240/native_proof.json`.

The pinned DeSmuME core uses native256×384 software rendering, interpreter, one
core and English firmware. All PNG identities, ROM/core identity and empty callback
error lists pass. This verifies observed Sailor Info display/composition for both
genders, not every alternate parent, palette bank, embedded CMMNIMG consumer or
physical device. The other original crop consumer remains separately scoped.

Four unreadable Online screenshot bodies, other embedded/environmental/alternate
display consumers, name consistency and final full-scope gameplay/integration
requirements remain unfinished. The full graphics goal stays active. Revisit the
older record-based checks at eventual completion as requested.
