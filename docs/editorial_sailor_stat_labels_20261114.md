# Sailor Info stat-label overlap

The hardware report showed partial white letters and doubled labels while checking a crew skill. I reproduced the problem with ordinary input on the registered Rafael Early Wraps candidate. The clean Japanese ROM displays only the two stats associated with the selected skill. All six come back after selecting an equipment slot. The Deck assignment roster showing Vigor and other skills in columns is a separate screen.

The English build baked the six labels into the paper plaques in `/_pxl/personinfo.pxl`. The original Sailor Info overlay at `0207FA6C` still drew all labels on restore and cleared unneeded labels with two Japanese space cells during skill selection. The English label widths and the baked lettering made both operations leave mixed lettering.

The [registered fix](../releases/all_routes_editorial_20261114_sailor_stat_labels_candidate/README.md) restores a clean paper background beneath the six labels and uses the original runtime drawing and selection paths for their full English names. The two original coordinates tables place the labels inside their English plaques. The clear string covers seven English cells. The value and shadow locations, skill-to-stat table and numeric getters are preserved. The six localized words remain Stamina, Agility, Charm, Wits, Spirit and Luck.

The clean, previous and corrected ROMs each cold-booted with copies of the same Syracuse save and identical inputs. All ten skill states, the initial state and the restored state passed 72 full plaque-mask comparisons. Every pixel outside the six plaques matched the previous English build in those 12 screenshots. The first and last letters, blank paper, bars, numbers and footer were checked. A separate cumulative cold boot matched six frames and 24 protected name getters. All 22 targeted tests passed. The corrected ROM awaits testing on hardware.

## Cumulative candidate recheck

The later [Maria Final Wrap Review candidate](../releases/all_routes_editorial_20261114_maria_final_wraps_candidate/README.md) contains the same ARM9 and Person Info PXL bytes as the registered stat fix. A fresh 10,601-frame cold boot on that exact ROM with the same Syracuse save replayed all ten skill selections plus the initial and restored screens. All 12 full two-screen frames match the verified stat-fix captures pixel for pixel. The selected pair shows complete white labels and the other four plaques are blank, as on the Japanese build. [Local replay receipt](../work/sailor_stats_cumulative_recheck_20261114/verified_selection_frames.json)

That replay used Hodram. The Fernando Deck View follow-up is recorded below.

## Fernando Dias in Deck View

The [About Extras cumulative candidate](../releases/all_routes_editorial_20261114_about_extras_candidate/README.md) reproduced the photographed crew assignment path in the emulator. Three cold boots from Lil's New Game used equivalent ordinary inputs on the clean Japanese ROM, the earlier English candidate with the defect, and the current candidate. Fernando was assigned to a mast as Sail Handler and opened through Deck View's R Info command. No copied saves, savestates, or state fixtures were used. The hardware photo shows an Excited mood. This replay reached Normal.

The earlier English candidate reproduced the overlapping stat letters. The current candidate matched the original selected stat pairs for Sailing, Command, Survey and Vigor, and all six labels returned after moving to an equipment slot. All 36 complete plaque masks passed, along with six Sail Handler role masks and six Sailor Info title masks. Every pixel outside the six stat plaques matched the earlier English candidate in all six states, including the title bar. The title overlap in the hardware photo did not appear on these runs and remains open for the photographed build and hardware state. [Comparison](../work/sailor_fernando_followup_20261114_v1/fernando_deck_comparison.png) · [Replay receipt](../work/sailor_fernando_followup_20261114_v1/fernando_deck_verification.json)

The [Name and Promised Words Confirmation candidate](../releases/all_routes_editorial_20261114_name_or_words_confirmation_candidate/README.md) passed a fresh ordinary New Game replay through Fernando’s assignment and the Sailor Info panel. All nine captured two-screen frames matched the verified About Extras replay pixel for pixel, including the four selected skill states, restored labels and exit to Deck View. The title was clear in all six panel captures. [Current replay receipt](../work/sailor_fernando_latest_20261114_v1/latest_deck_verification.json)

The [Expedition Report Wraps candidate](../releases/all_routes_editorial_20261115_expedition_report_wraps_candidate/README.md) carries the same fix. A ROM comparison against the Name and Promised Words build confirmed that the only changed internal file is `/COMMON/MESFILE.DK4`. ARM9 and `/_pxl/personinfo.pxl` match byte for byte, and all 29 patched words match the registered stat-label contract. This is an offline check of the November 15 candidate. The Fernando replay above supplies the emulator evidence, and the photographed Excited state still needs hardware confirmation.

## Fernando as an Excited Sail Handler

Two fresh Lil New Game replays on the [Town and Market Wraps candidate](../releases/all_routes_editorial_20261115_town_market_wraps_candidate/README.md) assigned Fernando to the mast and opened **Sailor Info** from Deck. The second run set his original mood byte to **Excited** just before opening the panel. Both runs used the same inputs and produced the photographed level, HP and base stat values. The replays used no copied saves or savestates.

The six held panel states show complete names, title and role text. All 36 stat plaques passed, including the blanks for unselected stats and the restored six labels. The opening title matched across 34 sampled frames. The lower skill ratings change with mood, and all 120 label-and-value rows matched the original game getters and complete font masks. The Deck return also uses different dialogue. **Normal** selected COMMON 1527, the Half Open sailing advice. **Excited** selected COMMON 1837, “Bring it on!” Both lines were retained after checking the clean Japanese and complete captured glyphs. [Replay report](../translations/editorial_checkpoints/SharedText_20261110_v1/fernando_excited_deck_20261115_v1.json) · [Normal and Excited comparison](../work/fernando_excited_deck_20261115_v1/fernando_normal_excited_comparison.png)

The hardware report (2840.jpg) also shows overlapping letters in the Sailor Info title. The title rendered clearly in both emulator runs. The exact ROM used for the photo is unconfirmed.

The [Square Samples Wraps candidate](../releases/all_routes_editorial_20261115_square_samples_wraps_candidate/README.md) preserves the replayed ROM's ARM9 and Person Info PXL byte for byte. The photographed Deck interaction still needs a check on hardware with this candidate.

The [All Routes Crew Review candidate](editorial_promotion_candidate_20261115_crew_review.md) repeats the two cold-boot replays on the exact test ROM. All 36 stat plaque checks, 120 skill rows, six held title masks, 34 title transition samples and both Deck return comments pass. The Normal run used ordinary inputs. The Excited run used the same inputs and set Fernando’s original mood byte just before opening Sailor Info. The title overlap from the photo remains unconfirmed on hardware. [Frame comparison](../releases/all_routes_editorial_20261115_barmaid_town_labels_candidate/verification/fernando_deck_replay.png)

## Follow-up on the reported deck position

The November 6 Rafael 2952 candidate named in the earlier Trade report still contains the original English plaque asset and none of the 29 corrected ARM9 words. The [November 15 London and Stockholm candidate](editorial_london_stockholm_dialogue_20261115.md) contains the corrected plaque asset and all 29 words. Its stat-label draw, selection and restore routines, stat tables and relevant glyph masks also match the replayed Crew Review candidate. This comparison was offline. The ROM used for the deck photo remains unconfirmed.

The promoted November 13 Wrap Review ROM also contains the original plaque asset and none of the 29 repair words. An offline comparison on the exact registered [Special Target Labels candidate](editorial_special_target_labels_20261115.md) matched the Crew Review candidate across all 29 repair words, the corrected plaque asset, seven stat display code and data ranges, and the relevant stat and title glyph masks. The Crew Review replay remains the gameplay evidence for Fernando's Deck assignment. Hardware confirmation of the photographed title overlap is open.

The [Seoul Recruitment candidate](editorial_seoul_recruitment_20261115.md) contains the corrected plaques and all 29 repair words. A fresh Lil New Game replay assigned Fernando to the mast and opened Sailor Info three times, including a close and reopen 30 frames apart. All 66 plaque comparisons, 11 held title masks and 120 transition frames passed. The selected stats drew once, unselected plaques cleared, and all six labels returned on reopening or selecting equipment. This was ordinary emulator gameplay with Fernando in a Normal mood. The title overlap in photo 2840.jpg did not reproduce, and the filename of the photographed ROM remains unconfirmed. [Replay receipt](../translations/editorial_checkpoints/SharedText_20261110_v1/fernando_deck_reopen_20261115_v1.json) · [Frame comparison](../work/fernando_deck_reopen_20261115_v1/fernando_deck_reopen.png)

## Fleet Sighting Alerts candidate recheck

The exact [Fleet Sighting Alerts candidate](editorial_fleet_sighting_alerts_20261115.md) passed two cold boots from Lil’s New Game through Fernando’s mast assignment. The Normal run used controller inputs. The Excited run set his original mood byte before opening Sailor Info. All 36 stat plaque masks, 120 skill rows, six held title masks and 34 sampled opening-title frames passed. Sailing, Command, Survey and Vigor each displayed the original pair of complete labels. Moving to equipment restored all six. The title overlap visible in photo 2840.jpg still needs hardware confirmation. [Replay receipt](../translations/editorial_checkpoints/SharedText_20261110_v1/fernando_deck_fleet_candidate_20261115_v1.json) · [Frame comparison](../work/fleet_sighting_fernando_deck_20261115_v1/fernando_normal_excited_comparison.png)

An offline comparison verified all three ROM hashes. The Fleet Sighting Alerts and Crew Review candidates contain the corrected plaque asset and all 29 ARM9 words, with identical glyph masks for the affected labels and title. The promoted November 13 Wrap Review ROM contains the original plaques and zero repair words.

The exact [Setup Confirmation candidate](editorial_setup_confirmation_prose_20261115.md) retains the corrected plaque asset and all 29 repair words. Seven stat drawing, selection, restoration and data ranges and all 29 distinct glyphs used in the stat names, title, role and Fernando’s name match the Crew Review ROM offline. The Crew Review replays supply the gameplay evidence. The photographed Sailor Info title overlap still needs hardware confirmation.

## Market Trade Dialogue candidate

The [Market Trade Dialogue candidate](../releases/all_routes_editorial_20261115_market_trade_dialogue_candidate/README.md) contains the same corrected plaques, all 29 repair words, the same seven display ranges and all 29 matching glyphs verified above against Crew Review. The currently promoted Wrap Review ROM retains the old plaques and original word values. Both ROM hashes were verified offline. For hardware follow-up on the title, use the exact Market Trade Dialogue ROM or the replayed Crew Review ROM and open Fernando’s Sailor Info from his mast assignment. Check the title both on entry and while selecting a skill. [Crew Review replay](../releases/all_routes_editorial_20261115_barmaid_town_labels_candidate/verification/fernando_deck_replay.png)

## Trade and Armed Ship Labels candidate

The [Trade and Armed Ship Labels candidate](editorial_trade_and_armed_ship_labels_20261115.md) matches the replayed Crew Review ROM for the corrected plaque asset, all 29 ARM9 repair words, seven stat-display ranges and 29 glyphs used in the stat names, title, role and Fernando’s name. This is an offline comparison of both exact registered ROMs. The promoted November 13 Wrap Review ROM has the original plaque asset and none of the 29 repair words. Use a fixed candidate for the photographed hardware path. The Sailor Info title overlap still needs confirmation on a known build.

## Release scope

The ROM changes are confined to ARM9 and the six plaque interiors. The clean-input patch reconstructs the exact candidate. There is no additional dialogue credit. The registration checkpoint then had 279 shared keys and 808 unadjudicated wrap leads. The separate wider artwork audit remains open.

The All Routes Wrap Review accepted on November 13 remains the promoted main build.
