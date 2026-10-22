# Village names and menu wording

These decisions translate the original 24 village descriptors and six menu
labels. Character names and the previously locked naming policy are unchanged.
The clean Japanese strings, original map points, source pointer owners and
clues are recorded in `translations/village_ui_manuscript_v1.json`.

| ID | Original | English |
| --- | --- | --- |
| 0 | イヌビク | Inuvik |
| 1 | ハワイ | Hawaii |
| 2 | リオデジャネイロ | Rio de Janeiro |
| 3 | チャーチル | Churchill |
| 4 | バルバライソ | Valparaiso |
| 5 | ノーム | Nome |
| 6 | コッド | Cape Cod |
| 7 | モンテビデオ | Montevideo |
| 8 | ヘクラ | Hekla |
| 9 | カリビブ | Karibib |
| 10 | フォレル | Forel |
| 11 | タヒチ | Tahiti |
| 12 | ディクソン | Dikson |
| 13 | アソーレス | Azores |
| 14 | サンタバーバラ | Santa Barbara |
| 15 | ナルビク | Narvik |
| 16 | レバキュー | Leveque |
| 17 | カリャオ | Callao |
| 18 | エゾ | Ezo |
| 19 | パース | Perth |
| 20 | グアム | Guam |
| 21 | チクシ | Tiksi |
| 22 | コルフ | Korf |
| 23 | ワンガヌイ | Wanganui |

## Decisions needing more than a direct spelling

- **Inuvik:** standard local spelling, consistent with its western Arctic
  position. [Town of Inuvik](https://www.inuvik.ca/discovering-inuvik/about-inuvik/).
- **Cape Cod:** an English geographic adaptation of the unqualified コッド,
  supported by the source Atlantic-coast position and Champlain clue. The
  identification is an inference, not an original Latin label discovered in the
  ROM. [National Park Service's Champlain history](https://www.nps.gov/caco/learn/historyculture/samuel-de-champlain.htm).
- **Forel:** retain the source-derived spelling. The game's southeastern
  Greenland location does not justify replacing it with Cape Farewell, which is
  considerably farther south. The regional spelling Mont Forel appears in the
  [Geological Survey of Denmark and Greenland](https://eng.geus.dk/media/13684/nr18_001-126.pdf),
  but that does not establish the fictional village's precise real-world
  identity. No new settlement identity is invented.
- **Leveque:** the source name and location identify the Cape Leveque area.
  Retain the village's unqualified name, without adding Cape to this label.
  Australia's [Bureau of Meteorology](https://www.bom.gov.au/climate/averages/tables/cw_003004_Info.shtml)
  lists Cape Leveque at 16.40 S,122.93 E. The prior unsupported **Lebaque** spelling
  is corrected in the only three active Lil story occurrences. Both spellings
  are seven ASCII bytes, preserving existing layout, control bytes and parity.
- **Korf:** the source position is in the Bering Sea/Kamchatka area and its clue
  is Avacha. It is not the Greek island Corfu. The regional government's
  [administrative reference](https://ns.kamlib.ru/upload/medialibrary/439/vnkwjocij3gn40nt74i5ah7qzb3rcso2/adm-ter-ustr.pdf)
  records Корф in Olyutorsky district; Korf is the direct Latin spelling.
- **Ezo:** preserve the source's historical name. Do not modernize it to Hokkaido.
- **Wanganui:** retain the spelling represented by the original Japanese and
  original release period. Wanganui and Whanganui are recognized alternatives
  for the city; a later district spelling change is not a reason to overwrite
  the game's label. [Land Information New Zealand](https://www.linz.govt.nz/consultations/whanganui).

Other names use established English spellings matching the source and map
region. ASCII accent folding follows the existing font and UI conventions;
Valparaiso is not treated as a new pronunciation or renamed place.

## Menu labels

| Original | English | Meaning |
| --- | --- | --- |
| 補給 | Resupply | Replenish supplies. |
| 宿泊 | Stay | Lodging; the label adds no fixed number of nights. |
| 船修理 | Repair Ship | Repair the ship. |
| 水夫募集 | Recruit Sailors | Recruit crew. |
| 出港 | Set Sail | Depart the village by sea. |
| 約束の言葉 | Promised Words | Use the existing password editor terminology. |

The six original action IDs, order, callbacks and unlock rules remain intact.
This document records wording decisions, not a claim that every village event,
development state or original village-card graphic has been visited.
