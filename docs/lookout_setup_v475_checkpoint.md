# V475 real Lookout preparation and city geometry

V474 is unchanged. Cold boot of the repaired/rested Genoa save opens normal Deck
View. Manuel Almeida moves from Survey Room to Lookout. The selection screen
shows Skill: Observe,Need70 and Manuel128;he qualifies. The assignment is confirmed
through XFinish/A and a normal slot6 overwrite finishes after4200 further frames.

A separate cold load retains Lookout,Manuel Almeida and On watch! Eyes open.
Every first/interior/final glyph passes complete masks;the entire upper192 rows
(49152 pixels) match the pre-save assignment screen. The lower selection cursor
differs because selection and placement end in different states;no whole-screen
equality claim. Original repaired Genoa donor bytes remain unchanged.

Help124's Japanese source says a Lookout needs Observe70 and helps discover towns
and other places at sea. Survey is a different role. The live new assignment is
verified;whether it changes Istanbul discovery is not yet verified in gameplay.

## Original city coordinate evidence

Read-only queries in the preserved V472 approach snapshot execute all114 city
actor index getters and both point virtuals. B566C returns each marker from static
metadata4/8;B5648 returns its separate entrance from12/16. Output guards and saved
register ABI pass;all captured RAM remains unchanged. These getter ranges are
byte-identical to clean. Istanbul marker is23184,5408;entrance23192,5464 in native
map units. This establishes the distinction,not a docking guarantee.

The route helper now accepts1/2/4/8/16-map-unit spacing;16 remains the default.
Fine original collision queries near the old Istanbul approach still select the
outer point rather than the requested inner-harbor goal. Do not force a course
through the intervening land or claim that finer sampling solved docking.

Verifier: scripts/verify_lookout_setup_v475.py;Ruff passes.
Proof: work/analysis/harbor_geometry_v475/lookout_proof.json.
Reports: work/emulation_v193/lookout_setup_v475/capture_report.json and
work/emulation_v193/lookout_reload_v475/capture_report.json.

Prepared normal save on E:
Saves/hodram-genoa-repaired-lookout-blue-oak-v474.dsv.
The verified Lookout screen is archived unchanged in E Screenshots.

These are targeted DeSmuME/source checks,not hardware or full-playthrough evidence.
Continue the supplied,repaired fleet toward the actual Golden Cutlass purchase;
verify city discovery before attempting the old failed approach. Occupied Weapon
and all wider graphics requirements remain open. All22 historical requirements
and all18 incomplete plaques retained. No canonical promotion. Revisit older
record-based checks at actual full-goal completion.
