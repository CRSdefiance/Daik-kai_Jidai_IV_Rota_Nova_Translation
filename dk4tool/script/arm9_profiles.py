from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Arm9ProfileEntry:
    row_id: str
    offset: int
    japanese: str
    suggested_english: str
    context: str
    notes: str = ""
    slot_size: int | None = None

    @property
    def source_bytes(self) -> bytes:
        return self.japanese.encode("cp932")

    @property
    def source_length(self) -> int:
        return self.slot_size or len(self.source_bytes)

    @property
    def expected_bytes(self) -> bytes:
        source = self.source_bytes
        return source + b"\0" * (self.source_length - len(source))


STARTUP_ENTRIES = (
    Arm9ProfileEntry("DK4_TITLE_OPTIONS", 1276268, "設定", "Opts", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_CONTINUE", 1276400, "つづきから", "Continue", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_EXTRAS", 1276412, "おまけ機能", "Extras", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_NEW_GAME", 1276424, "はじめから", "New Game", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_GALLERY", 1276436, "ギャラリー", "Gallery", "Title menu"),
    Arm9ProfileEntry("DK4_TITLE_RACE", 1276568, "大航海レース", "Grand Race", "Title menu"),
    Arm9ProfileEntry("DK4_BUTTON_BACK", 1160460, "戻る", "Back", "Shared controller prompts"),
    Arm9ProfileEntry("DK4_BUTTON_DONE", 1160476, "決定", "Done", "Shared controller prompts"),
    Arm9ProfileEntry("DK4_BUTTON_EDIT", 1160516, "変更", "Edit", "Shared controller prompts"),
    Arm9ProfileEntry("DK4_SELECT_BORN", 1376968, "生まれ", "Born", "Character selection"),
    Arm9ProfileEntry(
        "DK4_SELECT_HEADING",
        1376976,
        "キャラクター選択",
        "Choose Captain",
        "Character selection",
    ),
)


CHARACTER_ENTRIES = (
    Arm9ProfileEntry("DK4_LIL_NAME", 1423728, "リル", "Lil", "Lil character record"),
    Arm9ProfileEntry("DK4_LIL_LAST", 1428632, "アーゴット", "Argot", "Lil character record"),
    Arm9ProfileEntry(
        "DK4_LIL_ORG", 1434148, "アーゴット商会", "Argot Co.", "Lil character record"
    ),
    Arm9ProfileEntry(
        "DK4_LIL_BIO_1",
        1375612,
        "商魂たくましいオランダの少女",
        "A bold Dutch merchant girl  ",
        "Lil biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_LIL_BIO_2",
        1375641,
        "幼なじみの相棒カミルとともに、",
        "With childhood friend Camille,",
        "Lil biography",
    ),
    Arm9ProfileEntry(
        "DK4_LIL_BIO_3",
        1375672,
        "一旗揚げようと世界の海に飛び出す",
        "Sails the world to make her mark",
        "Lil biography",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_NAME", 1428032, "ラファエル", "Raphael", "Raphael character record"
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_LAST", 1428572, "カストール", "Castor", "Raphael character record"
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_ORG",
        1434132,
        "カストール商会",
        "Castor Co.",
        "Raphael character record",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_BIO_1",
        1375708,
        "船乗りに漠然と憧れるポルトガルの少年",
        "Portuguese youth dreaming of the sea",
        "Raphael biography",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_BIO_2",
        1375745,
        "友人にそそのかされて海に出ることになる",
        "A friend urges him to sail the world. ",
        "Raphael biography",
        "Trailing space preserves the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_RAPHAEL_BIO_3",
        1375784,
        "初めてプレイする方におすすめ",
        "Recommended for new players.",
        "Raphael biography",
    ),
    Arm9ProfileEntry("DK4_HODRAM_NAME", 1425716, "ホドラム", "Hodram", "Hodram character record"),
    Arm9ProfileEntry(
        "DK4_HODRAM_MIDDLE", 1426388, "ヨアキム", "Joachim", "Hodram character record"
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_LAST", 1433556, "ベルグストロン", "Bergstrom", "Hodram character record"
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_ORG",
        1435492,
        "ベルグストロン軍",
        "Bergstrom Fleet",
        "Hodram character record",
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_BIO_1",
        1375816,
        "再独立を果たしたスウェーデンの提督",
        "An admiral of newly free Sweden   ",
        "Hodram biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_BIO_2",
        1375851,
        "海軍とは名ばかりの私掠艦隊を率いる",
        "Commands a navy of privateers     ",
        "Hodram biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_HODRAM_BIO_3",
        1375886,
        "自国の艦隊を世界最強にすべく活動する",
        "Aims to make his fleet the strongest",
        "Hodram biography",
    ),
    Arm9ProfileEntry("DK4_MARIA_NAME", 1425456, "マリア", "Maria", "Maria character record"),
    Arm9ProfileEntry("DK4_MARIA_LAST", 1424056, "リー", "Lee", "Maria character record"),
    Arm9ProfileEntry("DK4_MARIA_ORG", 1424736, "リー家", "LiFam", "Maria character record"),
    Arm9ProfileEntry(
        "DK4_MARIA_BIO_1",
        1375924,
        "倭寇に苦しめられる人々を守るために",
        "Guards people from pirate raids   ",
        "Maria biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
    Arm9ProfileEntry(
        "DK4_MARIA_BIO_2",
        1375959,
        "国法である鎖国政策をあえて無視し、",
        "Defying the national isolation law",
        "Maria biography",
    ),
    Arm9ProfileEntry(
        "DK4_MARIA_BIO_3",
        1375994,
        "私設艦隊を率いて戦う明（みん）の女提督",
        "A Ming admiral leading her own fleet  ",
        "Maria biography",
        "Trailing spaces preserve the original line delimiter.",
    ),
)


CITY_SCREEN_ENTRIES = (
    Arm9ProfileEntry(
        "DK4_CITY_COMMON",
        0x11B57C,
        "共通",
        "Common",
        "City screen shared-information button",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_CITY_STATUS_NORMAL",
        0x1565D8,
        "通常",
        "Normal",
        "City status value",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_CITY_STATUS_NORMAL_VISIBLE",
        0x15633C,
        "通常",
        "Normal",
        "City status value used by the Lisbon information screen",
        slot_size=8,
    ),
    Arm9ProfileEntry("DK4_CITY_TYPE_CITY", 0x1565E4, "都市", "City", "City type value"),
    Arm9ProfileEntry(
        "DK4_CITY_HEADINGS",
        0x15692C,
        "種類状態発展度武装度",
        "TypeStatGrowthArms  ",
        "City information headings",
        "Four fixed fields: Type, Stat, Growth, Arms.",
    ),
    Arm9ProfileEntry(
        "DK4_CITY_PORT",
        0x156AEC,
        "出港所",
        "Port",
        "City location button",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_GOOD_SALT",
        0x15B78C,
        "塩",
        "Sal",
        "Commodity-name abbreviation; the fixed slot needs one byte for its terminator.",
        slot_size=4,
    ),
    Arm9ProfileEntry("DK4_GOOD_GUNS", 0x15BAE8, "鉄砲", "Guns", "Commodity name"),
    Arm9ProfileEntry(
        "DK4_CITY_LISBON_A",
        0x15C068,
        "リスボン",
        "Lisbon",
        "Lisbon city-name slot",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_CITY_LISBON_B",
        0x15C11C,
        "リスボン",
        "Lisbon",
        "Lisbon city-name slot",
        slot_size=12,
    ),
    Arm9ProfileEntry("DK4_GOOD_SAFFRON", 0x15C1AC, "サフラン", "Saffron", "Commodity name"),
    Arm9ProfileEntry("DK4_GOOD_ALMOND", 0x15D550, "アーモンド", "Almond", "Commodity name"),
    Arm9ProfileEntry("DK4_GOOD_OLIVE_OIL", 0x15D58C, "オリーブ油", "Olive Oil", "Commodity name"),
)


MENU_ENTRIES = (
    # Reusable command labels.
    Arm9ProfileEntry("DK4_MENU_INDEX", 0x11B524, "目次", "Index", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_SEARCH", 0x11B52C, "探索", "Search", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_MIN", 0x11B534, "最小", "Lo", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_NEXT", 0x11B53C, "次頁", "Next", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_ASSIGN", 0x11B54C, "配置", "Assign", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_DONE", 0x11B554, "完了", "Done", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_DELETE", 0x11B55C, "削除", "Delete", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_EQUIP", 0x11B564, "装備", "Equip", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_USE", 0x11B56C, "使う", "Use", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_PREV", 0x11B574, "前頁", "Prev", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_FACTION", 0x11B584, "勢力", "Faction", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_QUIT", 0x11B58C, "終了", "Quit", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_DECLARE", 0x11B594, "宣戦", "Declare", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_MAX", 0x11B59C, "最大", "Hi", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_STAFF", 0x11B5A4, "人事", "Staff", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_WORLD", 0x11B5AC, "世界", "World", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_WITHDRAW", 0x11B5B4, "全搬出", "Withdraw", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_REMOVE", 0x11B5BC, "はずす", "Remove", "Common menu command", slot_size=8),
    Arm9ProfileEntry("DK4_MENU_SORT", 0x11B5C4, "ソート", "Sort", "Common menu command", slot_size=8),
    # Deck screen rooms and policies.
    Arm9ProfileEntry("DK4_DECK_ADD_ROOM", 0x12FFC0, "追加１", "Add 1", "Deck room label", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_NURSERY", 0x12FFC8, "飼育室", "Nursery", "Deck room label", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_LOUNGE", 0x12FFD0, "娯楽室", "Lounge", "Deck room label", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_MATE", 0x12FFD8, "副官室", "Mate", "Deck room label", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_CAPTAIN", 0x12FFE0, "艦長室", "Captain", "Deck room label", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_LOOKOUT", 0x12FFE8, "見張台", "Lookout", "Deck room label", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_CARGO", 0x12FFF0, "積荷倉庫", "Cargo", "Deck room label", slot_size=12),
    Arm9ProfileEntry("DK4_DECK_MARINES", 0x12FFFC, "海兵詰所", "Marines", "Deck room label", slot_size=12),
    Arm9ProfileEntry("DK4_DECK_GUN_DECK", 0x130008, "武装砲台", "Gun Deck", "Deck room label", slot_size=12),
    Arm9ProfileEntry("DK4_DECK_SUPPLIES", 0x130014, "物資倉庫", "Supplies", "Deck room label", slot_size=12),
    Arm9ProfileEntry("DK4_POLICY_BATTLE", 0x130C84, "海戦", "Battle", "Deck policy", slot_size=8),
    Arm9ProfileEntry("DK4_POLICY_TRADE", 0x130C8C, "交易", "Trade", "Deck policy", slot_size=8),
    Arm9ProfileEntry("DK4_POLICY_EXPLORE", 0x130CA0, "探検航海", "Explore", "Deck policy", slot_size=12),
    # Crew assignment screen labels.
    Arm9ProfileEntry("DK4_DECK_CREW_SETUP", 0x131EDC, "人事配置", "Crew Setup", "Deck assignment heading", slot_size=12),
    Arm9ProfileEntry("DK4_DECK_UNASSIGNED", 0x131EE8, "未配置", "None", "Deck assignment status", slot_size=8),
    Arm9ProfileEntry("DK4_DECK_SKILL", 0x131EF8, "必要技能　%s", "Skill: %s", "Deck requirement label", slot_size=16),
    Arm9ProfileEntry("DK4_DECK_NEED_NONE", 0x131F08, "必要値　　－－", "Need: --", "Deck requirement label", slot_size=16),
    Arm9ProfileEntry("DK4_DECK_NEED_VALUE", 0x131F18, "必要値　　%4d", "Need: %4d", "Deck requirement label", slot_size=16),
    Arm9ProfileEntry("DK4_DECK_VIEW_A", 0x131F30, "甲板画面", "Deck View", "Deck screen heading", slot_size=12),
    Arm9ProfileEntry("DK4_DECK_VIEW_B", 0x131F3C, "甲板画面", "Deck View", "Deck screen heading", slot_size=12),
    Arm9ProfileEntry("DK4_DECK_VIEW_C", 0x132044, "甲板画面", "Deck View", "Deck screen heading", slot_size=12),
    # City navigation menu.
    Arm9ProfileEntry("DK4_NAV_DEPART_A", 0x144644, "出港", "Depart", "City navigation menu", slot_size=8),
    Arm9ProfileEntry("DK4_NAV_DEPART_B", 0x14464C, "出港", "Depart", "City navigation menu", slot_size=8),
    Arm9ProfileEntry("DK4_NAV_SAIL_A", 0x144654, "洋上へ", "Sail", "City navigation menu", slot_size=8),
    Arm9ProfileEntry("DK4_NAV_SAIL_B", 0x14465C, "洋上へ", "Sail", "City navigation menu", slot_size=8),
    Arm9ProfileEntry("DK4_NAV_DOCK_A", 0x144664, "ドック", "Dock", "City navigation menu", slot_size=8),
    Arm9ProfileEntry("DK4_NAV_DOCK_B", 0x144674, "ドック", "Dock", "City navigation menu", slot_size=8),
    Arm9ProfileEntry("DK4_NAV_DECK_A", 0x144684, "甲板画面", "Deck View", "City navigation menu", slot_size=12),
    Arm9ProfileEntry("DK4_NAV_AUTO_A", 0x144690, "自動移動", "Auto Move", "City navigation menu", slot_size=12),
    Arm9ProfileEntry("DK4_NAV_DECK_B", 0x14469C, "甲板画面", "Deck View", "City navigation menu", slot_size=12),
    Arm9ProfileEntry("DK4_NAV_AUTO_B", 0x1446A8, "自動移動", "Auto Move", "City navigation menu", slot_size=12),
    Arm9ProfileEntry("DK4_NAV_CARGO_SETUP_A", 0x1446B4, "積み荷編成", "Cargo Setup", "City navigation menu", slot_size=12),
    Arm9ProfileEntry("DK4_NAV_CARGO_SETUP_B", 0x1446C0, "積み荷編成", "Cargo Setup", "City navigation menu", slot_size=12),
)

WORLD_CITY_ENTRIES = (
    Arm9ProfileEntry("DK4_CITY_SEVILLE", 0x15C080, "セビリア", "Seville", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_MALACCA_A", 0x15C128, "マラッカ", "Malacca", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_OVIEDO", 0x15C14C, "オビエド", "Oviedo", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_SOCOTRA", 0x15C170, "ソコトラ", "Socotra", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_ALGIERS", 0x15C23C, "アルジェ", "Algiers", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_SOFALA_A", 0x15C278, "ソファラ", "Sofala", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_MALACCA_B", 0x15C2C0, "マラッカ", "Malacca", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_SURABAYA", 0x15C3E0, "スラバヤ", "Surabaya", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_LONDON", 0x15C62C, "ロンドン", "London", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_LUANDA", 0x15C6EC, "ルアンダ", "Luanda", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_SOFALA_B", 0x15C758, "ソファラ", "Sofala", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_TUNIS", 0x15C800, "チュニス", "Tunis", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_MADEIRA", 0x15C818, "マディラ", "Madeira", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_TRIPOLI", 0x15C830, "トリポリ", "Tripoli", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_HAMBURG", 0x15CA34, "ハンブルク", "Hamburg", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_GENOA_A", 0x15CA64, "ジェノヴァ", "Genoa", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_VALENCIA", 0x15CC50, "バレンシア", "Valencia", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_GENOA_B", 0x15CC68, "ジェノヴァ", "Genoa", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_MARSEILLE", 0x15CC80, "マルセイユ", "Marseille", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_BRISTOL", 0x15CCD4, "ブリストル", "Bristol", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_BEIRUT", 0x15CCE0, "ベイルート", "Beirut", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_CALICUT", 0x15CD88, "カリカット", "Calicut", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_CALCUTTA", 0x15CDAC, "カルカッタ", "Calcutta", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_BATAVIA", 0x15CDDC, "バタヴィア", "Batavia", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_TERNATE", 0x15CDF4, "テルナーテ", "Ternate", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_JAMAICA", 0x15CE84, "ジャマイカ", "Jamaica", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_MARACAIBO", 0x15CEA8, "マラカイボ", "Maracaibo", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_MAKASSAR", 0x15CF50, "マカッサル", "Makassar", "World city name", slot_size=12),
    Arm9ProfileEntry("DK4_CITY_ALBACETE", 0x15CF5C, "アルバセテ", "Albacete", "World city name", slot_size=12),
)

SHARED_STORY_ENTRIES = (
    # Early Raphael-story speaker names. These live in the shared ARM9 name pool,
    # so patching them also fixes name plates outside the opening scene.
    Arm9ProfileEntry(
        "DK4_NAME_JULIO",
        0x15BF28,
        "フリオ",
        "Julio",
        "Shared character-name pool",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_NAME_PASAR",
        0x15C060,
        "パサー",
        "Pasar",
        "Shared character surname pool",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_NAME_ERNECO_A",
        0x15C20C,
        "エルネコ",
        "Erneco",
        "Shared character surname pool",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_NAME_JANUS",
        0x15C710,
        "ジェナス",
        "Janus",
        "Shared character-name pool",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_NAME_MANAUS",
        0x15C914,
        "マナウス",
        "Manaus",
        "Shared character surname pool",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_NAME_ERNECO_B",
        0x15C9BC,
        "エルネコ",
        "Erneco",
        "Shared character surname pool",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_NAME_CLAUDIO",
        0x15D784,
        "クラウディオ",
        "Claudio",
        "Shared character-name pool",
        slot_size=16,
    ),
    # City icon hover labels. Every record is an eight-byte terminated slot.
    Arm9ProfileEntry("DK4_PLACE_TAVERN", 0x156A9C, "酒場", "Tavern", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_RUINS", 0x156AA4, "遺跡", "Ruins", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_PALACE", 0x156AAC, "王宮", "Palace", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_CHURCH", 0x156AB4, "教会", "Church", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_INN", 0x156ABC, "宿屋", "Inn", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_GATE", 0x156AC4, "城門", "Gate", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_SQUARE", 0x156ACC, "広場", "Square", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_GUILD", 0x156AD4, "ギルド", "Guild", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_GOVERNOR", 0x156ADC, "総督府", "Govt", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_SHIPYARD", 0x156AE4, "造船所", "Yard", "City location button", slot_size=8),
    Arm9ProfileEntry("DK4_PLACE_MARKET", 0x156AF4, "交易所", "Market", "City location button", slot_size=8),
)

TOWN_UI_ENTRIES = (
    # Tavern commands.
    Arm9ProfileEntry(
        "DK4_TAVERN_RECRUIT",
        0x143B90,
        "水夫を集める",
        "Recruit Crew",
        "Tavern command",
        slot_size=16,
    ),
    Arm9ProfileEntry(
        "DK4_TAVERN_TREAT",
        0x143BA0,
        "みんなにおごる",
        "Treat Everyone",
        "Tavern command",
        slot_size=16,
    ),
    Arm9ProfileEntry(
        "DK4_TAVERN_DRINK",
        0x143BB0,
        "飲み物をたのむ",
        "Order Drink",
        "Tavern command",
        slot_size=16,
    ),
    # Trading-post category menu. The game combines the category name with
    # the separate "%s店" formatter at runtime.
    Arm9ProfileEntry("DK4_SHOP_FORMAT", 0x14463C, "%s店", "%s Shop", "Trading-post category formatter", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_MEDICINE", 0x15A090, "薬", "Med", "Global trade category", slot_size=4),
    Arm9ProfileEntry("DK4_CATEGORY_DYES", 0x15A094, "染料", "Dyes", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_ARMS", 0x15A09C, "武器", "Arms", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_GOODS", 0x15A0A4, "雑貨", "Goods", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_SCENTS", 0x15A0AC, "香料", "Scents", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_DELICACIES", 0x15A0B4, "珍味", "Delic.", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_GEMS", 0x15A0BC, "宝石", "Gems", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_LIQUOR", 0x15A0C4, "酒類", "Liquor", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_ORE", 0x15A0CC, "鉱石", "Ore", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_TEXTILES", 0x15A0D4, "繊維", "Textile", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_LUXURY", 0x15A0DC, "贅沢品", "Luxury", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_FOOD", 0x15A0E4, "食料品", "Food", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_SEASONING", 0x15A0EC, "調味料", "Flavor", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_TREATS", 0x15A0F4, "嗜好品", "Treats", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_JEWELRY", 0x15A0FC, "装飾品", "Jewelry", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_METALS", 0x15A104, "貴金属", "Metals", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_CRAFTS", 0x15A10C, "工芸品", "Crafts", "Global trade category", slot_size=8),
    Arm9ProfileEntry("DK4_CATEGORY_SPICES", 0x15A114, "香辛料", "Spices", "Global trade category", slot_size=8),
    Arm9ProfileEntry(
        "DK4_PLAZA_TRENDS",
        0x143E98,
        "流行情報",
        "Trends",
        "Plaza shop-category menu",
        slot_size=12,
    ),
    # Repeated name-plate role used by tavern dialogue.
    Arm9ProfileEntry(
        "DK4_ROLE_BARKEEP_A",
        0x15D154,
        "酒場の親父",
        "Barkeep",
        "Shared speaker-role pool",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_ROLE_BARKEEP_B",
        0x15D160,
        "酒場の親父",
        "Barkeep",
        "Shared speaker-role pool",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_ROLE_BARKEEP_C",
        0x15D2A4,
        "酒場の親父",
        "Barkeep",
        "Shared speaker-role pool",
        slot_size=12,
    ),
    Arm9ProfileEntry("DK4_ROLE_TRADER_A", 0x15DAC4, "交易所の親父", "Trader", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_TRADER_B", 0x15DAD4, "交易所の親父", "Trader", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_TRADER_C", 0x15DAE4, "交易所の親父", "Trader", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_TRADER_D", 0x15DAF4, "交易所の親父", "Trader", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_TRADER_E", 0x15DB04, "交易所の親父", "Trader", "Shared speaker-role pool", slot_size=16),
    # Repeated name-plate role used by port and resupply dialogue.
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_A", 0x15DB74, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_B", 0x15DB84, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_C", 0x15DB94, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_D", 0x15DBA4, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_E", 0x15DBB4, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_F", 0x15DBC4, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    Arm9ProfileEntry("DK4_ROLE_PORT_WORKER_G", 0x15DBD4, "出港所の兄貴", "Port Worker", "Shared speaker-role pool", slot_size=16),
    # Shared confirmation buttons.
    Arm9ProfileEntry("DK4_BUTTON_NO", 0x133170, "いいえ", "No", "Yes/No prompt", slot_size=8),
    Arm9ProfileEntry("DK4_BUTTON_YES", 0x13317C, "はい", "Yes", "Yes/No prompt", slot_size=4),
    Arm9ProfileEntry("DK4_BUTTON_NO_ALT", 0x15AD10, "いいえ", "No", "Alternate Yes/No prompt", slot_size=8),
    Arm9ProfileEntry("DK4_BUTTON_YES_ALT", 0x15AD1C, "は い ", "Yes", "Alternate Yes/No prompt", slot_size=8),
    # Sailor-allocation screen.
    Arm9ProfileEntry(
        "DK4_CREW_COLUMNS",
        0x133FBC,
        "必要数　現在数　最大数",
        "Need   Now   Max",
        "Sailor allocation column headings",
        slot_size=24,
    ),
    Arm9ProfileEntry(
        "DK4_CREW_HEADING",
        0x133FD4,
        "水夫を編成して下さい",
        "Assign Sailors",
        "Sailor allocation heading",
        slot_size=24,
    ),
    Arm9ProfileEntry(
        "DK4_CREW_AUTO",
        0x1339F8,
        "自動",
        "Auto",
        "Automatic sailor allocation button",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_CREW_EVEN",
        0x133A00,
        "平均化",
        "Even",
        "Even sailor allocation button",
        slot_size=8,
    ),
    Arm9ProfileEntry(
        "DK4_CREW_FLAGSHIP",
        0x133A10,
        "旗艦重視",
        "Flagship",
        "Automatic sailor-allocation strategy",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_CREW_MINIMUM",
        0x133A1C,
        "必要最小",
        "Minimum",
        "Automatic sailor-allocation strategy",
        slot_size=12,
    ),
    Arm9ProfileEntry(
        "DK4_CREW_CAPTAIN_SUFFIX",
        0x13400C,
        "%s艦長",
        "%s Cap",
        "Captain suffix on sailor allocation screen",
        slot_size=8,
    ),
    # Shared faction and commodity records. These feed every city screen that
    # references the same global data table, including Seville.
    Arm9ProfileEntry("DK4_FACTION_VALDES", 0x15D214, "バルデス軍", "Valdes", "Global faction name", slot_size=12),
    Arm9ProfileEntry("DK4_GOOD_SULTANA", 0x15C9D4, "サルタナ", "Sultana", "Global commodity name", slot_size=12),
    Arm9ProfileEntry("DK4_GOOD_COTTON_CLOTH", 0x15BF90, "綿織物", "Cotton", "Global commodity name", slot_size=8),
    Arm9ProfileEntry("DK4_GOOD_ARMOR", 0x15B850, "甲冑", "Armor", "Global commodity name", slot_size=8),
)


PROFILES = {
    "startup": STARTUP_ENTRIES,
    "characters": CHARACTER_ENTRIES,
    "city": CITY_SCREEN_ENTRIES,
    "menus": MENU_ENTRIES,
    "world": WORLD_CITY_ENTRIES,
    "shared": SHARED_STORY_ENTRIES,
    "town": TOWN_UI_ENTRIES,
    "all": STARTUP_ENTRIES
    + CHARACTER_ENTRIES
    + CITY_SCREEN_ENTRIES
    + MENU_ENTRIES
    + WORLD_CITY_ENTRIES
    + SHARED_STORY_ENTRIES
    + TOWN_UI_ENTRIES,
}


def profile_names() -> tuple[str, ...]:
    return tuple(PROFILES)


def export_profile_rows(
    arm9: bytes, profile: str, include_drafts: bool = False
) -> list[dict[str, object]]:
    entries = PROFILES[profile]
    rows: list[dict[str, object]] = []
    for entry in entries:
        source = entry.expected_bytes
        actual = arm9[entry.offset : entry.offset + entry.source_length]
        if actual != source:
            raise ValueError(
                f"{entry.row_id}: ARM9 source mismatch at 0x{entry.offset:X}; "
                f"expected {source.hex().upper()}, found {actual.hex().upper()}"
            )
        rows.append(
            {
                "id": entry.row_id,
                "file_path": "/__arm9__.bin",
                "container_path": "",
                "encoding": "shift_jis",
                "source_offset": entry.offset,
                "source_length": entry.source_length,
                "source_hex": source.hex().upper(),
                "japanese": entry.japanese,
                "english": entry.suggested_english if include_drafts else "",
                "status": "draft" if include_drafts else "untranslated",
                "context": entry.context,
                "speaker": "",
                "notes": entry.notes,
                "max_bytes": entry.source_length,
                "allow_expand": "false",
                "pointer_group": "",
                "control_profile": "default",
                "wrap_width": 38,
            }
        )
    return rows
