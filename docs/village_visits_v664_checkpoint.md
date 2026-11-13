# V664: complete initial village menus across all 24 locations

This is a verification checkpoint on the unchanged integrated V653 ROM, not a new
ROM release. The preceding status-only turn made no authoritative project change;
this checkpoint resumes verification of the already completed village captures.

## Actual game coverage

All 24 original villages now have captured and independently verified:

- Their complete `Discovered NAME.` message, using the current native name getter.
- Two retained docking-prompt frames, including the complete place name.
- Their actual initial menu: 97 complete labels across 24 menus.
- The complete two-line request to hear the promised words.

The locations are Inuvik, Hawaii, Rio de Janeiro, Churchill, Valparaiso, Nome,
Cape Cod, Montevideo, Hekla, Karibib, Forel, Tahiti, Dikson, Azores, Santa Barbara,
Narvik, Leveque, Callao, Ezo, Perth, Guam, Tiksi, Korf and Wanganui. Established
name decisions and shipped prose are unchanged.

The paired docking captures are identical prompt images; they do not establish
separate Yes/No choice outcomes. There are 29 terminal cold boots, 354 original
PNG capture records and 325 distinct run/frame pairs after final-frame duplicates.

The original menu-building instructions at 020789AC..02078A54 execute for all 24
indices. Their original modulo filters produce the three-, four-, five- and
six-row variants; no menu is forced to match an assumed common layout. Resupply,
Stay, Repair Ship, Recruit Sailors, Set Sail and Promised Words retain their
existing meanings and availability rules.

Independent ROM-font masks check every glyph and blank cell. Each dialogue
comparison also covers the entire 224x48 foreground field. Each menu comparison
covers the entire 96x120 foreground field. Actual first/final glyph deletion
controls are rejected, including 48 controls that remove the first or final
letter of the 24 village names. All complete names and their native discovery
bit masks are checked in the actual live village models. Development remains
zero in all 24 final request states; this batch does not develop the villages.

## Fixtures and Ezo's distinct branch

Every run starts from a fresh emulator cold boot and an exact isolated copy of
the same Syracuse donor save. No savestate is loaded. The donor remains
SHA256 `958d6e36f521e4f8b0940e0c60a4de08df8fcae71f9e6f6e3271156cf25beadb`.

The authorized approach fixture owns only the active ship's eight coordinate
bytes. Original village/fleet/ship getters supply the objects and coordinates;
original terrain decoding and collision checks establish nearby water. All
other RAM bytes remain exact during each mutation. The game performs discovery,
docking, menu construction and dialogue normally. No discovery, development,
story, scene, menu or resource flag is injected. These runs verify the reached
contexts, not earned long-distance voyages or user-save progression.

The first Ezo approach discovers Ezo but then sails out of range. Original
02078654 returns village18 at5800 and no-nearby-village25 at6200. This failed
approach is retained and receives no menu/request credit. A second coordinate-only
approach reaches the ordinary docking prompt. Accepting it invokes an original
villager story before the initial village menu. Normal buttons advance that
scene; the real five-row menu at11400 and chief request at12200 then pass.

The first return, exploratory story run and final chief run are retained
separately. Their common captured prefixes match exactly. An original Japanese
ROM control repeats the same two approaches and button schedule. Its entire
upper screen is identically black at all 12 retained story/menu/request samples,
matching all 589,824 compared current upper-screen pixels. That upper-screen
appearance is present in this original fixture context; it is not evidence of a
new translation regression. No claim is made about unrelated black-screen cases.

Two rejected verifier assumptions are also retained: the current queued portrait
docking prompt starts at x22, while the modal discovery message starts at x16;
and the original discovery getter returns `1 << village_index`, not a normalized
Boolean. Correcting those verification assumptions required no ROM change.

## Village cards remain open

None of the eight complete white village-card files is resident in the sampled
RAM snapshots from these approaches and the extended Ezo runs. This bounded
observation does not establish that the cards are unused, never transiently
loaded, or absent from every development/event branch. The V549 supplied-image
display proof remains valid, and ordinary triggers for all eight cards remain
open. The actual gameplay branches tested here do not justify closing them.

## Evidence and integration

- Verifier: `scripts/verify_village_visits_v664.py`.
- Proof: `work/analysis/village_visits_v664/proof.json`.
- Eight derived comparison sheets retain arrival/menu/request views for all24.
- Archive: `E:/Rota Nova translations/Screenshots/Test fixtures/V664 Village visits`.
- All captures retain their original bytes; the sheets are labeled derived
  comparisons and the location fixtures are disclosed. No guide approval is inferred.
- V653 ROM, patch, manifest, release registry and canonical/verified release
  pointers remain unchanged. Candidate SHA256 remains
  `c4e9c4faf18c212e5b6572d61e6b2821493f38bbc1dc89d601b37b16058b3ade`.
- All18 original plaque/hint objects remain incomplete, all22 historical scope
  objects remain exact, and the graphics goal remains active. Other actual
  resource consumers, material acceptance, deeper gameplay and older record
  checks remain part of the goal.
