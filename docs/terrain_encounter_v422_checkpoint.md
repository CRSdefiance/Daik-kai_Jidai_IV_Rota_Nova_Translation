# Read-only terrain routing and actual Speyer encounter V421–V422

Registered V414 remains unchanged, SHA-256
`699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c`.
The graphics goal remains active; no ROM or artwork change.

## Original terrain evidence

Ordinary departure from the verified Copenhagen save first encounters shoreline
blocks. The original sailing path calls collision predicate02069B5C after converting
ship coordinates to physical map pixels. Its original map-cell/cache routines use
50x25 uint16 pages from WORLDMAP.DK4. The original overlay decoder01FFA10C
decompresses real ROM data; original water classifier020693EC executes for all1024
masked terrain values. Coarse certain-water-only routing has no local path here.

The improved local query supplies four genuine native-decoded pages as an explicit
loaded-cache contract, then executes original mixed-shoreline predicate69B5C on
5000 local cell centers. An A* path joins collision-free centers through the gaps.
Page input/output guards, exact source data and saved registers pass. This is an
isolated read-only source query, not a live injection or complete file-loader/GPU
proof. Cell-center safety does not prove every continuous segment or docking.

Planner: `scripts/plan_water_route_v422.py`; targeted Ruff passes.
Proof: `work/analysis/lubeck_voyage_v421/water_route_proof.json`.
WORLDMAP remains source-exact. Hashes identify every decoded page and input ROM.

## Actual normal navigation and encounter

Normal steering follows the channel waypoints, declines an intermediate Copenhagen
docking prompt and continues. Small course corrections account for varying speed
and turning drift. The approach triggers an original story scene: Manuel spots a
ship; Hodram identifies Speyer's ship; the conversation discusses the encounter,
then gives a naval-battle tutorial. The run reaches Battle stations! at20000 frames.
No battle result, Lubeck docking, new item or occupied equipment is credited.

All report/PNG hashes, normal input schedules and original/test donor hashes pass.
Complete source-font masks verify There it is!, Speyer's ship?, and Use the classic
T formation., including first/final letters and punctuation. The long upper black
dialogue background is observed only; its intended caller/background composition
has not been independently checked and is not labeled a defect or cleared globally.
Older awkward tutorial wording remains for the required older-record review.

Evidence: `work/analysis/lubeck_voyage_v421/encounter_proof.json`.
Actual report: `work/emulation_v193/lubeck_voyage_v421/capture_report.json`.
Exact next-run prefix: `work/analysis/lubeck_voyage_v421/full_encounter_inputs.json`.
The20000-frame run is terminal; replay with a longer frame limit to finish this
scene and inspect actual battle controls before proceeding to the next port.
There is no normal mid-dialogue save checkpoint and no synthetic state load.
This unfinished encounter capture is not archived as a finalized guide image.

## Scope retained

Original Copenhagen donor and test copy are unchanged. The earned shield clue is
retained by the starting checkpoint; armor is not acquired/equipped. All18 plaques
remain fully_completed:false and all22 historical requirements remain. Original
legacy/environment consumers, Gallery/endings, condition/equipment variants and
full-goal audit are still open. Low-resolution Online images remain user-exempt.
These are targeted emulator/source tests, not full gameplay or hardware verification.
No canonical promotion. Revisit older record-based checks at actual full completion.
