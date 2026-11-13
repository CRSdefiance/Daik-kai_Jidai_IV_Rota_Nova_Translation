# V714: current V712 plaque material and terminology review

## Result

A fresh7,100-frame cold boot of V712 exercises Assign Sailors, Sailor Info and
three equipment hints using the original14-action controller schedule. The
historical save is copied exactly. No savestate, inventory injection, location
fixture or live code/RAM fixture is used.

All17 independent complete font masks pass, including leading and trailing
letters. All14,272 static plaque/frame/material pixels match the current source
assets. Equipped Items, Weapon and Blue Oak Shield match three complete native
hint planes totaling3,552 pixels. The two plaque atlases remain exact to V555;
the equipment backing tile remains exact to V581. Every one of the four complete
two-screen captures also matches the earlier V666 review exactly.

Two new source/current comparison sheets contain all18 entries at4x nearest
neighbor scale. Both sheets and the individual native crops were opened for
review. No new large light-pixel block, vertical texture seam, clipped letter or
Japanese-shaped residue was identified in these selected views. This is a
visual review of the current reconstruction, not exact recovery of grain hidden
by original lettering. Existing source-donor, visible-material and wrap-boundary
uncertainties remain documented in the texture workflow.

## Translation review

Every current label was checked against its original Japanese and actual field:

|Current English|Japanese|Meaning/context|
|---|---|---|
|Fleet Crew|艦隊水夫数|Number of sailors in the fleet.|
|Unassigned|未編成水夫数|Sailors not assigned to a formation.|
|Endurance|航行可能日数|Duration at sea; the displayed unit is days.|
|Quarters|海兵詰所|Marine-quarters compartments, rather than a head count.|
|Cannon|砲種|Cannon type; the adjacent field supplies its model/quantity.|
|Fore/Aft|縦帆性能|Fore-and-aft sail performance.|
|Square|横帆性能|Square-sail performance.|
|Health|身体|Physical condition, with Healthy/illness values.|
|Mood|精神|Mental condition in a condition/status field.|
|Level|レベル|Level.|
|HP|HP|Original Latin abbreviation retained.|
|Stamina|体力|Physical stamina/strength attribute.|
|Agility|敏捷|Agility/quickness attribute.|
|Charm|魅力|Charm/personal appeal attribute.|
|Wits|知力|Intellect/mental ability attribute.|
|Spirit|精神|Mental strength as a numeric attribute, distinct from Mood.|
|Luck|運勢|Luck/fortune attribute.|
|Equipped Items|装備アイテム|Equipment currently assigned to the item slots.|

No terminology change is required by this review. The full machine-readable
matrix binds every decision to its actual original/current crop and source
proof; it is not a transcript inferred from generated English alone.

## User review and remaining scope

The two concrete comparison sheets were presented for feedback on material and
borders. Opening their Codex tabs returned queued; the source images themselves
were displayed through the image viewer. No user acceptance is inferred. All18
original audit entries remain incomplete and all22 historical requirements
remain exact.

A separate clarification asks whether the four low-resolution Online screenshot
bodies should stay excluded under the earlier instruction or be reopened under
the newly stated goal. That question is pending; no new scope decision is
invented from elapsed time.

The previous turn registered the new goal without implementing graphics work.
This checkpoint adds the latest-build native review packet and the source-bound
terminology matrix. The full graphics goal remains active. Small-control normal
contexts, village cards, legacy/embedded/comic contexts, restoration review,
previously recorded native-model gaps and final acceptance remain open. The
older record-based checks remain queued for revisiting after the full goal.

## Evidence and storage

- Analysis: `work/analysis/plaque_review_v714/`.
- Current native captures: `E:/Rota Nova translations/Generated/work/emulation_v193/plaque_review_v714_current/`.
- Original Japanese captures: retained `plaque_compare_v574_original/`.
- Comparisons: `E:/Rota Nova translations/Screenshots/Audit comparisons/V714 Plaques/`.
- Four unmodified guide candidates: `E:/Rota Nova translations/Screenshots/Guide candidates/V712 Plaques/`.
- Proof: `current_plaque_review_proof.json`; source/context matrix:
  `terminology_review.json`.
- ROM remains `out/all_routes_combined_v712_candidate.nds`, SHA256
  `6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030`.

The first verifier invocation retained the older V666 whole-ROM hash and stopped
before evaluating the new captures. It was corrected to the already frozen V712
hash. Material targets, pixel expectations and source locks were not changed to
make a test pass. The successful producer was not replayed or edited.

No ROM, patch, registry, canonical baseline or experimental pointer changes are
needed. Guide candidates retain their ordinary saved-game scope and are not
publication-approved. No commit or push.
