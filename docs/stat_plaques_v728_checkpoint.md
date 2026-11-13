# V728: empty/full stat bars, complete plaques and restored screens

V727 made progress by tracing the original script-buffer source path. This
checkpoint tests a distinct remaining plaque risk: whether empty/full bars and
three-digit attributes obscure the translated labels or equipment hints.
V712 remains the registered combined ROM.

## Three actual emulator runs

Three 9,500-frame cold boots use a byte-exact isolated copy of the existing
Syracuse donor, the unchanged pinned core and the same twenty UI actions.

| Case | Intervention before frame 5801 | Before frame 7201 |
|---|---|---|
| Control | Read only | Read only |
| Zero | Six displayed attributes set to 0 | Original six values restored |
| Hundred | Six displayed attributes set to 100 | Original six values restored |

The original attribute getter reads actor bytes 8–13. The original bar scaler
receives 100 as its denominator. The fixture resolves the actual active captain
through original native methods and checks the saved identity before writing.
The copied profile retains **Hodram** as its saved first name; the project's
chosen localization **Joakim** is unchanged. This test does not rename the save.

A process-local Python proxy calls each original `retro_run` exactly once.
Only six main-RAM bytes are written at each enabled intervention. No core DLL,
game code, source graphic, palette, font, original save or CPU register is patched.
The shared emulator harness is unchanged. Each complete 4 MiB before/after RAM
pair is saved and independently replayed. Exported general registers, instruction
address, DTCM and ITCM remain identical across each intervention. This does not
claim a separate full CPU/CPSR equivalence proof.

All three runs finish with the original stats restored. Normal controls reopen
Sailor Info, then return through the roster/menus to town. Both original donor
and isolated source-copy hashes remain unchanged. This is a synthetic display
test, not earned stat growth, natural acquisition, combat or skill mechanics.

## Actual display checks

- All seventeen independent source font masks remain complete.
- All 111 complete static plaque crops match current source pixels, including
  their letters, frames and material. The minimum/full bars do not cover them.
- Nine complete native hints match their wording and source paper backing:
  Equipped Items, Weapon and Blue Oak Shield in all three cases.
- All 54 three-cell attribute fields match the original font, including blanks
  and complete first/final digits. The numeric origin uses the fixed observed
  control-screen field; a whole-painter position model is not claimed.
- All 90 complete skill label/observed-value rows match their original font
  cells. Displayed values are reported as observations, not a mechanics oracle.
- All sixteen complete two-screen comparisons match the control exactly:
  six before the fixture and ten after restoration, reopening and town return.

The control and both 0/100 screenshots, plus their comparison sheet, were opened
for review. Empty and full colored bars, three-digit numbers, plaque edges,
equipment slots, hints and footer remain readable and complete. No artwork or
translation change is required by these tested states. Other attribute values,
actors and state combinations are outside this result.

## Research notes

The first control pilot stopped before any fixture write because its guard
expected the localized first name rather than the existing saved profile name.
That pilot and its contract are retained separately. The final producer binds
the copied source save and actual saved name, and remains frozen across all
three successful runs.

An exploratory check using an older skill-name/value helper was not adopted as
an oracle for the DS screen's field order. The final skill checks use the
established DS label/field layout and complete observed numeric glyphs; they
make no claim about the underlying skill formula. Attribute values themselves
are checked against the original six-byte getter and the captured RAM.

## Audit and storage

The tested stat-boundary scope leaves routine active work. The eighteen original
overall plaque/hint objects remain in the audit with completion false, and the
twenty-two historical requirement objects remain exact. Accepted material,
source-art decisions, four Online exclusions and approved marks remain intact.
Remaining original legacy/comic/control contexts and final integration review
are separate. Older record-based checks remain due after goal completion.

All captures, RAM pairs and read-only native exports are on E: under
`Rota Nova translations/Generated/work/emulation_v193/stat_plaques_v728_*`.
The proof and comparison sheet are in `work/analysis/stat_plaques_v728/`.
Selected original PNGs and the derived comparison are archived in
`E:/Rota Nova translations/Screenshots/Test fixtures/V728 Stat plaque boundaries`.
They are diagnostic fixtures, not guide or publication-approved screenshots.

V712 ROM, manifest, patch, registry and canonical baseline hashes are unchanged.
No new playable candidate, promotion, commit or push is made. Goal active.
