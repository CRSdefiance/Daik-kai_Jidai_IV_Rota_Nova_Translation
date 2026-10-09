from __future__ import annotations

import json
from pathlib import Path

STACK = Path("translations/release_stack.json")
STAGES = (
    (41, "B127 Fernando's card game, insight lesson and Old Maid recruitment"),
    (42, "B128 Martin Speyer confrontation, two response choices and market-share tutorial"),
    (43, "B129 Amsterdam Crimson Pigment and Lelystad polder scenes"),
    (44, "B130-B132 Clifford's map key, Crimson Pigment reveal and southern Mediterranean warning"),
    (45, "B133 Raphael Castor encounter and Nantes-Lisbon share exchange"),
    (46, "B134 Silveira's West Africa confrontation and B135 Espinosa's drug trade"),
    (47, "B136 Upper and Lower Stone Tablet assembly and Africa Proof map"),
    (48, "B137 Nagalpur tavern confrontation and Lil's money-can't-buy-everything stand"),
    (49, "B138 Nagalpur aftermath, both treasure-map purchase branches and lotus-leaf handoff"),
    (50, "B139 lotus-leaf and Kushan Platter combination revealing the southern Proof map"),
    (51, "B140 polder-funding pledge and Lil's new dream"),
    (52, "B141-B142 alternate million-gold polder funding branches"),
    (53, "B143 shipyard armor-research funding"),
    (54, "B144 armor-upgrade completion and B145 Mediterranean Proof map reveal"),
    (55, "B146 Kamil's separation from Lil and Hodram's sailing invitation"),
    (56, "B147 Maria's warning, Kuhn's deception and the Batavia lead"),
    (57, "B148 Kamil identity discovery and B149 Tang Bamboo Craft Proof map branches"),
    (58, "B150 Clifford's New World alliance plan against Maldonado and Escante"),
    (59, "B151 Maldonado tavern confrontation and alternate crew aftermath"),
    (60, "B152-B153 Ancient Kingdom Coin and Lotion Jar Southeast Asian Proof map"),
    (61, "B154 Al Fasi's bodyguard dismissal and Lil recruitment"),
    (62, "B155 Angelo Puccini recruitment and African trade advice"),
    (63, "B156 Ian Dukov tavern dismissal, ambush and recruitment"),
    (64, "B157 Carlo Sinato merchant illness, grief and recruitment"),
    (65, "B158 Christina's tavern dance and crew reactions"),
    (66, "B159 Samwell's elephant market cooking trial and recruitment"),
    (67, "B160-B162 stolen ship discovery and dockworker updates"),
    (68, "B163 ship return and Jam Jack Ludwyan recruitment"),
    (69, "B168 Mikhail Lett recruitment and item-information tutorial"),
    (70, "B169 Mikhail's Proof of Conqueror explanation and search advice"),
    (71, "B170 Yifa's flight from her master and recruitment"),
    (72, "B171 Sanghyeon's dream visit and Yifa's renewed training"),
    (73, "B172 Julian and Mihwa's Golden Crown of Silla lead"),
    (74, "B173-B174 Golden Crown tomb lead, handoff and Julian recruitment"),
    (75, "B175 Aziza pirate confrontation and sword rivalry"),
    (76, "B176 Seville banana boom"),
    (77, "B177 Genoa tomato boom"),
    (78, "B178 Amsterdam wheat boom"),
    (79, "B179 San Jorge wine boom"),
    (80, "B180-B182 Lisbon spices, Athens rubies and London gems"),
    (81, "B183 Basra painting craze and collector argument"),
    (82, "B184-B186 Sofala tea, Stockholm furs and Alexandria sweets"),
    (83, "B187 Malacca almond-medicine rumor"),
    (84, "B188 Osaka giyaman-glass market scene"),
    (85, "B189 Hamburg ceramics collectors and swindlers"),
    (86, "B190 Havana medicine rumor"),
    (87, "B191 Calicut father-son dye purchase"),
    (88, "B192-B194 Istanbul tobacco, Seoul chilies and Hangzhou sake"),
    (89, "B195 Veracruz cheese-dish market scene"),
    (90, "B196 six-stage charm-item haggling and Buy/Pass choices"),
    (91, "B197 Ian's celestial-maiden book and charm reward"),
    (92, "B198 Yukihisa's namahage dream and mysterious gift"),
    (93, "B199 Rocco Alemkel portrait, book find and Lil gift misunderstanding"),
    (94, "B200 Carlo's collapsed-traveler rescue and charm reward"),
    (95, "B201 enchanted mast-rope bargaining, Buy/Pass and stat rewards"),
    (96, "B202 fleeing stranger, pursuer and Glassmaking Guide handoff"),
    (97, "B203 caterpillar fungus, medicinal book and charm reward"),
    (98, "B204 Jam's shachihoko figurehead and Japanese lord's letter"),
    (99, "B205 Angelo and Lil's talking-parrot capture"),
    (100, "B206 ceramic-earrings merchant and four choice branches"),
    (101, "B207-B214 optional weapon clues, swans and complete companion letters"),
    (102, "B215-B226 Solomon, Avalon, armor legends, tavern scenes and Dukov's letter"),
    (103, "B227-B238 companion treasure clues, Charles and Jam letters and lost gloves"),
    (104, "B239-B249 stolen rose, figurehead challenge, ruins and Lebaque survey"),
    (105, "B250-B254 kind figurehead, melting-ice puzzle and demon figurehead branches"),
    (106, "B255-B282 guild missing-person and bounty quests, rewards and ruin directions"),
    (107, "B283-B287 forest bear encounter, all companion variants and London wine delivery"),
    (108, "B288 jungle cave encounter, tiger branches and companion variants"),
    (109, "B289-B292 Angkor temple elder and both platinum riddle branches"),
    (110, "B293-B294 fog Wait/Hurry branches, lost sailors and cliff guide"),
    (111, "B295-B298 Heavenly Wristband guild quest, one-day loan and emperor reward"),
    (112, "B299-B300 giant snake encounter, bog rescue and Colosseum hint"),
    (113, "B301-B305 desert encounter, mosque treasure and Basra spice exhibition"),
    (114, "B306 river encounter, bridge/ferry branches; bare 97AC variant follows in V115"),
    (115, "B307-B311 temple errands and Proof clue, plus B306 bare 97AC variant"),
    (116, "B312-B313 wolf Shoo/Hit/Run branches, injuries and Japanese city gate clue"),
    (117, "B314-B315 dark forest descent/detour branches and ancient pictorial-map rumor"),
    (118, "B316 scorpion Kill/Shoo/Run branches, sting, cactus and luggage escape"),
    (119, "B317-B319 burner divination and affordable legitimate African trade"),
    (120, "B323 fog advance/wait, dead end and alternate path encounter"),
    (121, "B324 jungle cave feel/light choices, snake and bat branches"),
    (122, "B325-B329 sea crossing, missionary rumor and Genoa tomato boom quest"),
    (123, "B330-B335 final ruins, survey, sextant and Alchemy Book; B22 controls classified"),
)


def main() -> None:
    stack = json.loads(STACK.read_text(encoding="utf-8"))
    profiles = stack["profiles"]
    for version, description in STAGES:
        batch = f"translations/lil_deep_route_v{version}.json"
        previous_lil = f"lil-deep-route-v{version - 1}"
        lil_name = f"lil-deep-route-v{version}"
        unified_name = f"all-routes-unified-v{version - 34}"
        previous_unified = f"all-routes-unified-v{version - 35}"
        lil_batches = [*profiles[previous_lil]["batches"], batch]
        unified_batches = [*profiles[previous_unified]["batches"], batch]
        profiles[lil_name] = {
            "status": "experimental",
            "batches": lil_batches,
            "note": f"Extends Lil V{version - 1} with all records in {description}. Runtime confirmation pending.",
        }
        profiles[unified_name] = {
            "status": "experimental",
            "require_screen_entry_layout": True,
            "batches": unified_batches,
            "note": (
                f"Four-route review build extending unified V{version - 35} with Lil V{version}: "
                f"{description}. Runtime confirmation pending."
            ),
        }
        print(f"registered {lil_name}: {len(lil_batches)} batches")
        print(f"registered {unified_name}: {len(unified_batches)} batches")
    STACK.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
