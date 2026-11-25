# V607: actual village discovery and UI after a source-checked water fixture

The preceding goal turn was a status response and added no new evidence. This
batch makes progress by reaching original village discovery, docking, menu,
Promised Words editor and an actual rejected-answer response. It also exposes
an English formatting defect and untranslated village UI. No ROM, patch, artwork,
registry, canonical baseline or original donor save is changed.

## Correcting the test precondition

The V606 Maria setup finalized at 14,400 frames without a discovery; its pending
departure/story context was unsuitable. The separate Syracuse setup finalized at
5,600 frames without discovery after placing the ship at the village center.
Neither run receives village-card or normal village UI credit.

The original terrain decoder 01FFA10C and collision predicate 02069B5C execute
against source-exact WORLDMAP and original overlay data. Exact center (4896,2320)
returns collision result 1. Nearby point (4874,2320) returns 0, water. Its squared
distance from the village center is 484, within the original 32-unit visit radius.
The loaded page-cache contract is explicit. Decoder output guards and original
map input bytes remain exact. This replaces the rejected land-center setup;
it does not alter terrain or waive collision handling.

`run_village_water_v607.py` temporarily binds the unchanged headless harness's
opted-in location helper to the strict V607 helper. Its legacy command key
`location_town:0` denotes village 0 only in this research runner. The exact V604
ARM9 and 4MiB RAM are required. Only eight active ship coordinate bytes are owned;
six bytes actually differ. No fleet cache, discovery, development, resource,
dialogue, scene or input bytes are supplied. The original next-frame game logic
must still run. This is an authorized location fixture, not ordinary travel.

## Actual 17,800-frame run

The unchanged Syracuse donor is SHA256
`958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.
It is copied into an isolated battery-save directory before cold boot; no
savestate is loaded. The process finalizes normally with no callback errors.
All 90 capture receipts and every pause RAM export are hash-checked.

- Frame 5200: ordinary sailing after Syracuse departure; discovery mask is zero.
- The coordinate fixture is applied at frame 5200.
- Frame 5600: original fleet cache updates to (4874,2323), discovery mask becomes
  one, and Manuel Almeida says `Village in sight!`.
- Frames 6000/6400: the original discovery and docking prompts show イヌビク.
- Frame 6900: original village menu opens through the ordinary Yes selection.
- Frame 7800: selecting its last option reaches Charles Rochefort's request.
- Frame 8200: `Enter the promised words.` appears.
- Frame 8600: the actual Promised Words editor opens. Its real marked provider
  identifies parent 0218A498 and capacity 18, without supplying a fake parent.
- Actual Latin-page selections produce single-byte input and advancing cursor
  values. A at 9200 and six-byte `auaaaa` at 15400 are verified in captured RAM.
- The navigation intended to enter Aurora was incorrect. The actual confirmed
  input was `auaaaA`, not Aurora. It receives no successful-password credit and
  is not evidence of a keyboard implementation fault.
- Frame 17800: the original rejected-answer response is
  `The village chief has left.` No successful village development is claimed.

The final input schedule records the incorrect attempts as well as successful
navigation. Do not replace observed input with intended letters in future tests.
The explicit startup schedule, location command and recorded pause/input frames
permit replay through the named research runner. TTY stdin must remain open.

## Newly observed defects and limits

Independent GameAsciiFont masks match complete letters and blank cell positions
for the discovery message, input prompt and rejected-answer response.
The real request is instead split into these captured lines:

```text
Captain, the village chief asks to h
ear
 the promised words.
```

All three line masks are exact, including the second line at y312 and the final
line at x22,y328. The compiled first line is confirmed against its existing
relocated manuscript bytes in live RAM. This is a real wrapping defect; the old
controlled formatter/raster evidence did not establish this actual parent layout.
The letters are present, but the word split and extra line are unacceptable.
Repair must address this village formatting contract and recheck the other
messages/clues, rather than editing an expected screenshot to accept the defect.

The visible village menu retains six Japanese source strings, independently
located unchanged in current and clean ARM9: 補給, 宿泊, 船修理, 水夫募集, 出港,
約束の言葉. The village model's name pointer also still resolves to イヌビク.
These are newly exposed UI/name translation gaps, not untranslated PXL lettering.
Their English rendering, bounds and actual input contexts remain to be fixed and
tested. The small editor title is visually observed; no complete title-font mask
or successful Aurora entry is claimed in this checkpoint.

None of nine selected complete upper-screen images equals any of the eight
translated village-card assets (168-171,206-209). The sequence uses the sea/map
presentation. This does not prove that any card is globally unused, nor close
other village families, development states, endings, legacy art or other graphics.

## Preservation and evidence

- `scripts/native_village_water_v607.py`, `run_village_water_v607.py`,
  `verify_village_water_v607.py` and `record_village_water_v607.py`.
- `work/analysis/village_water_v607/native_village_proof.json` and final inputs.
- Original terrain grid probes under `work/analysis/village_location_v606`.
- Raw captures, exports and report:
  `E:/Rota Nova translations/Generated/work/emulation_v193/village_water_v607_inuvik`.
- Selected unmodified captures, research scripts and provenance:
  `E:/Rota Nova translations/Screenshots/Test fixtures/V607 Village discovery`.
  These are fixture evidence, not ordinary guide screenshots.

Production remains experimental V604, SHA256
`fb8de61d20e94e742574bded2d8e4251305f2b56265ff8624dd766eaa6cf9158`;
its patch is unchanged. All 18 plaque/hint objects remain incomplete, and all 22
historical requirement objects retain their exact scope. The goal remains active;
the older record-based review remains due at full completion.
