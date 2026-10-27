# V554 local plaque texture review

The previous goal turn made progress: four ordinary World Map states gained
complete156160-pixel composition evidence and a source caption translation check.
This turn returns to the user's global plaque texture concern. V546 is unchanged.

## Findings from current source comparisons

V542 replaced the17 plaque interiors with fine grain from clean towninfo Share
strips; V546 restored genuine source bevels. Those changes remove the earlier
coarse donor artifacts, but do not preserve each individual plaque's original
visible texture. Current V546 versus clean Japanese atlas comparisons are now
saved for both Assign Sailors and Sailor Info.

The six statistic plaques have pink source backgrounds and receive wooden
English plaques under the user's requested redesign. They are excluded from
same-position wooden source recovery. Seven crew plaques and four left-hand
Sailor Info plaques have original wooden texture available for comparison.

## Rejected per-pixel restoration

The first research prototype restored3327 original background pixels across
11 plaques while retaining all17 English ink masks, bevels, palettes, dimensions
and unrelated pixels. Dark Japanese strokes have RGB sums96..123; sampled
material begins at286..328. An initial assertion of300 was disproved in the
Unassigned plaque; the complete11-region palette census established the gap.

Despite those exact preservation checks, visual review rejects this prototype.
Restoring background around each excluded Japanese ink pixel creates faint
Japanese glyph-shaped seams because reconstructed and original grain differ.
This is a new failure mode for the restoration workflow, not a production defect
introduced into V546. No research atlas is registered or shipped.

## Conservative alternative

A second prototype preserves contiguous reconstructed text bands with a2-pixel
margin around the original Japanese ink bounds. It restores424 source margin
pixels while preserving all17 English masks and existing borders. Visual review
does not show the first prototype's Japanese ghosts. It has not received native
crop or actual game verification and is not credited as an integrated correction.
It also does not recover all concealed text-region texture. The proof records
the protected bounds and exact per-plaque recovery counts for later review.

## Translation review

| Japanese | Current English | Review |
|---|---|---|
|艦隊水夫数|Fleet Crew|Fleet's sailor count; concise label|
|未編成水夫数|Unassigned|Sailors not assigned to the fleet|
|航行可能日数|Endurance|Remaining sailing days; concise label|
|海兵詰所|Quarters|Marine quarters; shortened for the plaque|
|砲種|Cannon|Cannon type; concise label|
|縦帆性能|Fore/Aft|Fore-and-aft sail performance|
|横帆性能|Square|Square sail performance|
|身体|Health|Physical condition|
|精神|Mood|Mental state in the condition field|
|レベル|Level|Direct equivalent|
|HP|HP|Established game abbreviation retained|
|体力|Stamina|Physical endurance stat|
|敏捷|Agility|Agility stat|
|魅力|Charm|Charm stat|
|知力|Wits|Intellect stat; concise natural label|
|精神|Spirit|Spirit stat, distinct from the condition field|
|運勢|Luck|Luck stat|

The source wording is recorded in the existing reviewed graphics batches and
cross-checked against the source atlas where baked in. Source stat plaques are
blank in the atlas; their Japanese labels are runtime text, not newly recovered
image lettering. No wording changes are needed from this review.

## Evidence and remaining gates

- `scripts/review_local_plaque_texture_v554.py`; Ruff passes.
- `work/analysis/plaque_source_review_v554/local_texture_prototype_proof.json`
  and `crew/person_local_texture_review.png`: rejected per-pixel prototype.
- `margin_local_texture_prototype_proof.json` and
  `margin_crew/person_local_texture_review.png`: conservative alternative.
- `crew/person_source_current.png`: original/current full atlas comparisons.

All research PXLs are explicitly named RESEARCH_ONLY. Final screenshots belong
in the guide collection only after actual display review; these are comparison
sheets. All22 historical requirements remain unchanged and all18 plaque/hint
entries remain incomplete. Global material-family review and native/gameplay
verification stay open. The graphics goal remains active.

Candidate remains `out/all_routes_combined_v546_candidate.nds`, SHA256
499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
