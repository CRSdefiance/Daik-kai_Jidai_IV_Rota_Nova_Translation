# Gameplay reference data provenance

Recorded 2026-10-11 for guide v0.4. No ROM was modified, built, or promoted. No new emulator/hardware tests were performed.

## Static DS items

Read-only source: `work/analysis/generated_item_advice_research_arm9.bin`, SHA-256 `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf`. Its identity matches the pinned source in `scripts/verify_item_role_eligibility.py`.

The 24-byte static records start at ARM9 offset `0x11E210`. Existing `scripts/verify_item_interface_research.py` explicitly reads category at +16, attribute at +18, effect at +19, and base value at +4. Its native mapping assigns attributes to the 16 crew duties. This extraction follows those established fields; it does not infer new mechanics from neighboring bytes.

Names: `translations/all_item_names_arm9_v1.json`, records `DK4_ITEM_POINTER_000` through `187`. Export: [ds-static-item-reference.json](ds-static-item-reference.json), 188 distinct rows. Player tables: weapons (25), armor (25), duty equipment (43); remaining categories appear as name lists.

The guide calls the numeric field a listed Effect rating. It does not claim the rating is fixed damage, HP, sale price, a percentage, or a guaranteed stat increase. Base values are retained in the research export but not presented as current market prices.

Dynamic promotional/Mystery Hunting records 188–197 are excluded here. Names beyond that range in the global name batch do not establish DS obtainability. The item-name directory covers the 188 regular records only, not complete locations or the full 198-item Gallery collection.

## Labels and use advice

- `docs/crew_sailor_ui_translation_v247.md`: Stamina, Agility, Charm, Wits, Spirit, Luck; skills; crew/endurance fields. These are wording evidence, not growth formulas.
- `docs/crew_roles_v326.md`: all 16 crew duties. `scripts/verify_item_role_eligibility.py` supplies evidence for the role eligibility check; no numerical assignment threshold is inferred.
- `docs/sailor_status_audit_v274.md`: 6 Mood and 7 Health states. Apply later corrections from `translations/condition_labels_review_v1.json`: Confused, Hurt, Wounded. State labels do not establish guaranteed recovery methods.
- `docs/sailing_condition_names_v309.md`: 26 sailing labels. Table presence does not demonstrate every condition through gameplay or prove a fixed danger/effect rate.
- `translations/common_b30_manuscript_v2.json`, items 020–023: utility-item descriptions.
- `translations/common_japanese_b34_manuscript_v1.json`, messages 3053 and 3056: rat/infection item advice. The game describes intended benefit, not success percentages.
- `translations/swordsmanship_status_manuscript_v1.json`: Fencing in duel stats; skill and HP are distinct.

No scurvy cure is inferred from real-world lime nutrition. Its exact game treatment procedure needs a DS source or mechanics test. Likewise, an NPC's claim that sleep cures an epidemic is not accepted as a guaranteed fleet disease cure.

## Character attributes

[Wiki officer page](https://w.atwiki.jp/offlinedaikoukai/pages/90.html), retrieved 2026-10-11. Eight selected rows preserve the source's six base attributes. English column labels follow the project wording. The page mixes releases; these numbers remain **Cross-platform-unverified**. Level columns and example level-50 numbers were deliberately not copied into guaranteed DS starting/growth tables.

The player guide explicitly labels these stats provisional. Native DS character numerical records still need their own demonstrated decoder/field mapping; the `work/full_characters.csv` file contains translation strings, not numeric stats.

## Reproduction and remaining gaps

[build_reference_sections.py](build_reference_sections.py) updates the player tables from the saved 188-row export. It asserts distinct complete indices, effect bounds, and 80-column output. It does not test gameplay effects or DS compatibility of the wiki stats.

Outstanding: item acquisition coordinates/prerequisites, all 10 added DS treasures, figurehead mechanics, role thresholds and effects, condition remedies, verified DS character numerical stats, and complete ship/combat/trading references. This turn adds reference content; it does not complete the active full-guide goal.
