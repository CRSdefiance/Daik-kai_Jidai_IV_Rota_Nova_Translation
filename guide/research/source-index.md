# Research source index

Target: Nintendo DS release of **大航海時代IV ROTA NOVA**. Resources supplied by the user and rechecked on **2026-10-11**. Access checks mean that page content was retrieved, not that all facts were extracted, translated, or tested in the game. No complete copyrighted walkthrough is reproduced here.

## Priority and verification overview

| ID | Source | Priority | Platform scope | Access / verification status |
|---|---|---|---|---|
| S1 | Dekuno Blog | CRITICAL; primary | Explicitly DS | Homepage and Rafael walkthrough retrieved; databases linked below; gameplay claims not independently tested |
| S2 | Kurogane.biz | HIGH | Multiple versions | Recovered over normal HTTP on October 12; 21 Hodram/Lil/Maria regional charts, seven maps, item categories, ship table, recruitment and FAQ inspected; DS applicability qualified |
| S3 | Strategy wiki: general guide | CRITICAL | Mixed versions | Retrieved; DS applicability must be checked per claim |
| S3A | Strategy wiki: version differences / bugs | CRITICAL | Rota Nova, earlier versions, HD, and platform distinctions | Retrieved; explicit DS/PSP distinctions located; source reports, not gameplay confirmation |
| S3B | Strategy wiki: settlements / passwords | HIGH | Mixed versions | Retrieved; 24 settlements compared with DS-specific coordinates and translated passwords; services and goods remain qualified mixed-version claims |
| S4 | Wazap Japan | MEDIUM | DS listing supplied by user | Listing retrieved; title reports 18 submissions; individual tips not audited |
| S5 | Official Koei guidebook | HIGH | DS and PSP | Publisher and retailer listings retrieved; book text unavailable to this research |

## S1 — Dekuno Blog / デクノブログ

- Homepage: <https://dekunobou-rotanova.seesaa.net/>
- Access update, 2026-10-12: direct discovery article <https://dekunobou-rotanova.seesaa.net/article/28642373.html> retrieved successfully. The earlier category-URL error does not mean its underlying article is inaccessible. All 76 saved discovery rows and their clue requirements are represented in section 12.3 and ds-discovery-reference.json. The earlier [item-location review](item-location-review.md) describes an intermediate extraction, not current table coverage.
- Japanese title: 大航海時代Ⅳ ROTA NOVA DS版攻略.
- Rafael walkthrough: <https://dekunobou-rotanova.seesaa.net/category/2333211-1.html>
- Direct Rafael article: <https://dekunobou-rotanova.seesaa.net/article/48270717.html>, dated 2007-07-18; retrieved 2026-10-11. The opening draft cites its スタート and アフリカ sections. Category and article are the same underlying author/content, not independent corroboration.
- The homepage expressly identifies DS coverage and excludes PC, PS, and PSP. It displays one Rafael walkthrough entry and zero entries for Hodram, Lil, and Maria; do not infer that those other walkthroughs exist.
- Research uses: scenario progression; recruitment and dialogue options; item discovery and purchases; ports, facilities, goods, tavern characters, passwords, and a linked navigation map.
- The Rafael walkthrough contains explicit recruitment and item-choice warnings. Extract these into individual evidence records before turning them into guide instructions. Preserve ambiguous wording and apparent typos for review rather than silently correcting prerequisites.

### Internal navigation recovered from the original homepage

| Section | Original URL | Check on 2026-10-11 |
|---|---|---|
| Rafael / ラファエル | <https://dekunobou-rotanova.seesaa.net/category/2333211-1.html> | Retrieved |
| Hodram / ホドラム | <https://dekunobou-rotanova.seesaa.net/category/2333214-1.html> | Homepage shows 0 entries; category body not inspected |
| Lil / リル | <https://dekunobou-rotanova.seesaa.net/category/2333213-1.html> | Homepage shows 0 entries; category body not inspected |
| Maria / マリア | <https://dekunobou-rotanova.seesaa.net/category/2342198-1.html> | Homepage shows 0 entries; category body not inspected |
| Discovery items by region / アイテム＞探索（地域別） | <https://dekunobou-rotanova.seesaa.net/category/2333278-1.html> | Retry returned 403 Forbidden; content not inspected |
| Purchasable items by region / アイテム＞購入（地域別） | <https://dekunobou-rotanova.seesaa.net/category/2388676-1.html> | Retrieved; direct article /article/29158147.html supplies 48 purchase rows in 12.4, checked against DS base values |
| Trade goods by region / 交易品＞地域別 | <https://dekunobou-rotanova.seesaa.net/category/2333225-1.html> | Retrieved; 87 ports and 326 goods listings in 10.6 and ds-trade-goods-reference.json |
| Port facilities / 街＞施設 | <https://dekunobou-rotanova.seesaa.net/category/2333258-1.html> | Retrieved; 87 facility rows, including 22 guild towns, in 11.3 and ds-port-facility-reference.json |
| Tavern women / 街＞酒場娘 | <https://dekunobou-rotanova.seesaa.net/category/2333267-1.html> | Retrieved; all 21 gift pairings extracted in section 11.4 |
| Passwords / 街＞約束の言葉 | <https://dekunobou-rotanova.seesaa.net/category/2333339-1.html> | Retrieved; 24 settlement coordinates/passwords in 11.1; English answers matched to translated records |
| Ports and items map / 航海図＞港とアイテム | <http://dekunoblog.web.fc2.com/map/chart.htm> | Original HTTP link preserved; retry reported 503 Service Unavailable on HTTPS; map not inspected |

Homepage categories showing zero entries also include all-items lists by region/type, discovery items by type, purchasable items by type, trade goods by type, and shipyards. Treat these as incomplete navigation, not available databases.

## S2 — Kurogane.biz / 鋼鉄.biz

- URL: <https://www.kurogane.biz/dk4/>
- Supplied Japanese title: 鋼鉄.biz 大航海時代 IV -PORT ESTADO/ROTA NOVA- 攻略.
- The user reports a timeout on October 11, 2026 and a link from the strategy wiki. This run returned a retrieval error; it did not establish that the site is permanently offline.
- Potential coverage supplied by the user: protagonist walkthroughs, item and character databases, hidden settlements, and mechanics. None of that content was independently inspected in this run.
- Current access update, October 12: normal HTTP retrieval at <http://www.kurogane.biz/dk4/> succeeded. The preceding failure notes describe the initial HTTPS attempt, not current coverage. EUC-JP source pages and decoded text are saved in this research directory. See [recovery review](kurogane-recovery-review.md), the guide's S2 citations and the structured regional, ship, item and coordinate references. Archive retrieval timed out; no archived content is claimed. All recovered gameplay instructions retain their mixed-version qualification unless separately corroborated for DS.

## S3 — 大航海時代シリーズ攻略wiki

- General guide: <https://w.atwiki.jp/offlinedaikoukai/pages/19.html>
- Supplied research scope: protagonist mechanics, trading and money-making, ships, combat, events, recruitment, equipment, exploration, FAQs, and external references.
- The general page and linked protagonist, item, trading, recruitment, ship, version and settlement pages have been consulted. Exact child URLs appear in section 15 of the guide. Current citation counts and definitions are in [source-coverage-audit.md](source-coverage-audit.md) and source-coverage-audit.json; these inventory citation use, not independent gameplay verification.
- Rafael child page: <https://w.atwiki.jp/offlinedaikoukai/pages/54.html>, checked 2026-10-11 for northern and Africa corroboration. Differences from Dekuno are recorded in [the v0.2 review](rafael-africa-review.md). Mixed-version conditions remain unverified for DS.
- Mixed-version material requires explicit platform checks; avoid importing additional protagonists or systems from other releases into the four-protagonist DS guide.

### S3A — 機種による変更点・バグ

- URL: <https://w.atwiki.jp/offlinedaikoukai/pages/89.html>
- Use as the version filter for treasure additions, exploration, ports, combat, trading, and bug claims.
- The **ROTA NOVA版追加変更点等** section reports **10 additional treasure items on DS versus 23 on PSP**. It also distinguishes how the two versions award the added treasures. These are wiki-reported platform differences; DS gameplay verification is pending.
- Separate explicitly DS statements from shared Rota Nova claims and the later HD/Steam/Switch sections. A bug appearing on this page is not automatically a DS bug.

### S3B — 補給村と約束の言葉

- URL: <https://w.atwiki.jp/offlinedaikoukai/pages/60.html>
- Research scope supplied by the user: settlement coordinates, required passwords (約束の言葉), goods, and related mechanics.
- Page retrieved; individual rows remain unverified for DS. Compare against S1's password page and map where accessible. Preserve exact Japanese passwords and coordinate hemispheres.

## S4 — Wazap Japan / ワザップ!

- URL: <https://wazap.com/game/14755/cheats/>
- Japanese title: 大航海時代IV -ROTA NOVA- 裏技・攻略.
- Retrieved listing title shows **18** community submissions on the check date. This is a listing count, not 18 verified guide articles.
- User-supplied leads: recruitment (including Aziza), settlement passwords, leveling, money-making, discovery items, weapons, scenario events, and combat.
- Cross-check individual submissions against DS-specific sources. Record each tip's own URL, author/date if visible, prerequisites, and conflicts. Community submission errors remain possible.

## S5 — Official Rota Nova guidebook

- Japanese title: 大航海時代IV ROTA NOVA ガイドブック.
- Publisher listing: <https://www.gamecity.ne.jp/media/book/game/daikokai/dai4/dai4_rn_gb.htm>
- Retailer listing: <https://books.rakuten.co.jp/rb/3978212/>
- Editor: KINGS. Original publisher supplied by the user: Koei; the current retailer publisher field uses Koei Tecmo Games (コーエーテクモゲームス).
- Publication: March 2006; length: 207 pages; ISBN-13: 9784775804032; ISBN-10: 4775804030. Month, length, and ISBN-13 verified in the retailer's product metadata; editor and ISBN-10 verified on the publisher page.
- Publisher explicitly advertises both **Nintendo DS and PSP** support, flowchart walkthroughs for four protagonists, character/ship/city/item/goods data, Golden Routes, and Mystery Hunting. Retailer description also advertises introductory trade routes and navigation/trade/combat advice.
- These are descriptions of advertised coverage, not extracted book findings. Neither listing provides the full text. Do not claim to have read it or cite an unseen book page as evidence.
- [Deeper scan search, 2026-10-11](official-guide-scan-search.md): forum re-upload lead, exact National Diet Library holding, and archive checks. No accessible full scan verified.

## Outstanding verification

- Rafael walkthrough: retrieved but not fully translated, fact-indexed, or tested.
- Hodram, Lil, Maria: find DS-compatible scenario sources; S1's empty categories cannot supply them.
- Item, port, goods, and password pages: extraction and DS cross-checking pending.
- Original map: retry access or locate an archival snapshot; coordinates remain unextracted.
- Kurogane: access and coverage unverified; no archive inspected.
- Wiki version differences and all community tips: source evidence only until DS corroboration or tests are recorded.
- Official book: bibliographic and advertised-content information only; full text not accessed.

## Additional mixed-version item reference

https://w.atwiki.jp/offlinedaikoukai/pages/81.html — retrieved October 12, 2026. PK base data, old/new protagonist rows, and explicitly DS-specific treasure counts. Shakuntala lead and one-run collection limit added with qualifications; all other numerical fields need DS comparison before use.

## DS community combat tips: access limits

Duel tip 461773 and cannon-display report 187344 were attempted October 12, 2026. The former redirected to a notification page; the latter was not retrieved in full. Listing snippets are not used as complete mechanics. See [access review](wazap-combat-access-review.md).

## Additional PSP comparison walkthrough

[日々気の向くままに Rota Nova index](https://hibi-kinomukumamani.blogspot.com/2018/04/ivrota-nova.html), explicitly PSP. Retrieved October 12, 2026 by direct public HTML retrieval after the web reader failed. [Hodram](https://hibi-kinomukumamani.blogspot.com/2018/05/06iv.html), [Lil](https://hibi-kinomukumamani.blogspot.com/2018/05/07iv.html), [Maria](https://hibi-kinomukumamani.blogspot.com/2018/05/08iv.html). Saved/extracted pages under guide/research. They summarize companion and proof-object events, not every proof-map assembly visit. No DS authority is inferred. Maria's temple map preparation added as a qualified comparison; other details still need systematic comparison.

## Kurogane access recovered October 12, 2026

Supersedes earlier inaccessible status for HTTP-fetched content: http://www.kurogane.biz/dk4/ and stage/ship/map index pages. EUC-JP decoding required. HTTPS times out; non-www certificate mismatch not bypassed. Archive CDX timed out, but live HTTP works. Retrieved scenario pages hodo-hokkai.php, riru-hokkai.php, mari-higasi.php under stage/. Multi-version; child-page extraction remains ongoing.

## Recovered item/map databases

Kurogane item/index.php, item/hiho.php, nakama/index.php and all seven map/map-*.php pages fetched October 12, 2026 via HTTP. Ninety coordinate entries extracted, version-qualified. Treasure page distinguishes DS guild map purchase, random locations, five-per-run limit and a possible coordinate-hint path explicitly marked uncertain by its author. Systematic treasure extraction remains next; do not treat map examples as fixed DS coordinates.
