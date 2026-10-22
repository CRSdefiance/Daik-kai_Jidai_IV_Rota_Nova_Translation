# Mystery Hunting source review

Added 2026-10-12. `interface_help_manuscript_v1.json`, topic 142, describes Ancient Maps as fragmented and directs visits to guilds. `general_help_manuscript_v2.json`, topic 134, lists Ancient Maps under Info. Existing item-interface evidence describes 198 collection entries, distinct from 218 global name strings.

`work/analysis/promotional_item_default_initialization_proof.json`, source SHA-256 `c55a2530af7816a5f612494c42c16af5911e58791d571d92ad9297b7e87980ee`, lists ten initialized slots 188–197 with the initial English labels copied into the player reference. Its own `full_initializer_return_random_additions_downloaded_states_and_rendering_verified` is false. It is a bounded initialization proof, not ordinary acquisition or final random-value evidence.

`translations/all_item_names_arm9_v1.json` provides corresponding ordinary catalog labels by index. The guide's two-column table records this index association only. It does not establish the naming/appraisal transition, complete obtainable sets in every save, fixed effects or coordinates.

Exploratory pointer comparisons against `work/analysis/generated_item_advice_research_arm9.bin` did not match the old source-pointer fields in the name batch. That compares different localization states and is insufficient to reject a name association or prove random renaming. Neither inequality is presented as a definitive game-mechanics result. Current/raw strings and exact callers need a further consumer audit.

`common_mystery_items_v1.json` supplies treasure/map descriptions and appraisal-related text. Lore such as a horn possibly curing illness is not turned into a guaranteed item remedy or percentage.

Remaining: guild fragment acquisition, full map decoding/puzzles, initialization and subsequent random/naming/appraisal code, ordinary current-ROM acquisition, location behavior and numerical effects. No fixed coordinate or generated outcome is invented. Full guide goal remains active; ROM/save/screenshot files were unchanged.

## Kurogane DS/PSP treasure page recovered

October 12, 2026: http://www.kurogane.biz/dk4/item/hiho.php. Four pieces, DS guild purchases, Info Ancient Maps and Y hints, randomized positions, DS5-per-run, example maps not fixed targets. Coordinate hints from tavern characters are explicitly uncertain in its text and remain qualified. Ten reported ratings agree with wiki81; mask type differs in wording (boarding leader/armor versus armor). Only native ten catalog labels included; PSP-only items and the explicitly joke Harrington sword excluded. PSP run count18 differs from wiki20; DS5 agreement does not establish selection/reset/save behavior. Source old description phrases correspond to the initial-label catalog but do not prove a runtime appraisal transformation or unrandomized effect display.
