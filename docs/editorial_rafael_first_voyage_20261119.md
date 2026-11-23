# Rafael's first voyage

The [registered voyage and Ceuta follow-up](editorial_rafael_voyage_ceuta_20261119.md) resolves the R59 wrap found in the original Lisbon replay and verifies the full first voyage again on the cumulative candidate.

## Ordinary Lisbon replay follow-up

On the later [Tavern Recruitment candidate](../releases/all_routes_editorial_20261119_rafael_tavern_lesson_candidate_v2/README.md), Rafael used Recruit Crew, assigned sailors with Flagship, and left the Tavern. The original first-voyage event then ran all 31 commands, including all 28 speech panels. Every body and nameplate matched the native glyph masks, and the game substituted Rafael in Julio's reassurance. Play returned to Lisbon's Port menu and began the Ceuta sailing tutorial. This was an emulator cold boot with an unchanged battery save and ordinary inputs. The Ceuta lesson continued beyond the capture. [Exact source and gameplay references](../releases/all_routes_editorial_20261119_rafael_tavern_lesson_candidate_v2/verification/ordinary_first_voyage_replay.json)

The live pages expose a loose middle line in SC0 B42 R59. Keep Julio's two example regions and bring “say” into the phrase it introduces in the next wrap review. R80's narrow first row reserves room for the longest supported player name, and all three lines displayed in full with Rafael. [Visual review and row findings](../releases/all_routes_editorial_20261119_rafael_tavern_lesson_candidate_v2/verification/ordinary_first_voyage_visual_review.json)

## Original candidate review

Reviewed all 28 turns from the clean Japanese. Julio explains how to resupply at the Port when money is short and what declining the offer lets you adjust. The supply warning fits on one page. Clau's pirate boast and Janus's teasing give way to Julio's practical advice on ports, recruiting and trade. Rafael still takes Julio's reminder about the money seriously before Julio laughs it off. The review records 21 revisions and seven exact retentions. [Exact review](../releases/all_routes_editorial_20261119_rafael_first_voyage_candidate_v2/verification/registered_review.json)

All 21 revised pages and three additional name-width samples passed native rendering and direct visual review. An initialized Rafael excerpt displayed ten pages, including the full supply warning, the game's own Rafael substitution and Julio's reassurance after Rafael promises to repay him. Thirteen revised lines received offline checks only. Natural scene activation and hardware remain unverified. [Native pages](../releases/all_routes_editorial_20261119_rafael_first_voyage_candidate_v2/verification/before_after_1.png) · [Emulator excerpt](../releases/all_routes_editorial_20261119_rafael_first_voyage_candidate_v2/verification/rafael_live_1.png)

Only Rafael's first-voyage block changes. The clean-input patch reconstructs the candidate byte for byte. It preserves the Deck lesson, all 114 accepted layers and the ASCII right-bound correction. Six startup holds, 24 protected getters and 34 focused tests passed. The ledger stays at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../releases/all_routes_editorial_20261119_rafael_first_voyage_candidate_v2/README.md)
