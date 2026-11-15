# Native archive caller census V264

V264 is research only. The registered playable build remains V263; no ROM,
patch, graphics asset or release profile was changed. Previous goal turn made
verified progress on dialogue alignment inheritance and complete Deck help.
This turn classifies previously unclassified generic archive-open consumers.

## Complete direct-caller coverage

Every current ARM9 MainCodeFile section and every declared ARM9 overlay is scanned
for aligned ARM BL, Thumb BL/BLX and literal pointers to native archive open,
block read, partial read and the SLACK archive wrapper. All16 direct call sites
are recorded. There are seven archive-open call sites, seven block-read sites,
one SLACK wrapper caller and one internal partial-reader call. No direct Thumb
calls or literal function pointers to these four targets are found in those units.
The exact candidate manifest and current registry hashes match.

| Native parent | Actual requested archive family | Source of block selection |
|---|---|---|
|02009710|GRP/CHARA.DK4|Argument plus6|
|0200977C|GRP/CHARA.DK4|Argument plus4, with cached-selection check|
|02024134|data/SC0.DK4 through SC3.DK4|Global route selects four-path table; block is argument|
|0204704C|GRP/SLACKIMG.DK4|Argument; only observed direct wrapper caller0209EDE8 selects captain blocks14–17|
|02053530 open fragment|COMMON/MESFILE.DK4|Native message cache block selection in enclosing parent|
|0206E578|data/WORLDMAP.DK4|Argument|
|0207CE1C|COMMON/HELP.DK4|Argument|

Ten native filename-selection cases execute these seven open sites, including
all four route choices. Native constructors, filename/table selection, archive
open and directory header parsing execute original ARM instructions. The actual
block counts match each exact saved-ROM archive. Only SDK filesystem operations
are bridged. Case-insensitive bridge resolution maps each requested filename to
one unique ROM path; both spellings are retained in the proof. Route selection,
parent arguments and the message-cache fragment context are supplied contracts.

Each parent is deliberately stopped immediately after archive open, before its
payload read/display. Native close/destructor calls clean up that interrupted
object, and all bridge handles close. This does not claim full parent return ABI,
block-read safety, GPU crops, unlocks, input behavior or a route playthrough.
All tested caller/reader code ranges are byte-identical to clean. Ruff passes.

## Consequence for raw comics and embedded banks

This broader generic-reader census found no additional direct raw-comic parent.
All direct SLACK archive-wrapper calls still lead to the known captain path.
The separate loose-image helper's slot19 still aliases the44x60 name-label sprite,
as proven in V209. Neither path proves native display of the21 raw320x240 comic
planes in SLACKIMG block19. Do not substitute a forced comic fixture for an actual
viewer or credit its screenshot as gameplay verification.

Computed branches, generated filenames, indirect consumers and code loaded outside
the declared units are not ruled out. This is not proof that raw comic/legacy data
is globally unused, and the11 unresolved legacy-block count is unchanged. Keep
their translations/source-preservation work and native-display gate open. Further
research must identify an indirect/generated consumer or establish original
viewer availability from stronger evidence, rather than repeating the failed
slot19 helper assumption.

All18 plaque/hint entries and Armor/Weapon variants remain incomplete. Four Online
source bodies, occupied equipment, broader contextual/native display checks and
final whole-goal verification remain open. Revisit older record-based checks at
actual goal completion.

Evidence: `work/analysis/archive_callers_v264/proof.json`.
Script: `scripts/research_archive_callers_v264.py`.
