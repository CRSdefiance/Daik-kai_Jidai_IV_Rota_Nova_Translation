"""Verify revised sentences, the original menu, and the retained rescue panels."""

from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_B81_B89_20261122 as stage
from scripts import verify_hodram_B71_B80_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
OPAQUE = ROOT / "retained_source_symbols.json"
SYMBOLS = {f"DK4_MES_B{b}_R{n:04d}" for b, n in ((81,39),(81,78),(82,5),(82,12),(82,24))}
HISTORICAL = Path("work/analysis/Hodram_B81_B89_stored_20261101/stored_native_verification.json")
CONTEXT_SHORT_NAMES = {
    "DK4_MES_B81_R0043": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B81_R0051": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B84_R0165": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B85_R0105": ("Cristina", "Cristina Erneco"),
    "DK4_MES_B86_R0037": ("Cristina", "Cristina Erneco"),
    "DK4_MES_B87_R0017": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B87_R0020": ("Janus", "Janus Pasar"),
    "DK4_MES_B88_R0093": ("Kurushima", "Sojin Kurushima"),
}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verification = checked_text(previous.verification, {
    'len(entries) == 144 and fe_count == 4': 'len(entries) == 306 and fe_count == 5',
    'assert [m["block"] for m in choices] == []':
        'assert [m["block"] for m in choices] == [87] and choices[0]["count"] == 2',
    '"hodram_B71_B80_progressive"': '"hodram_B81_B89_progressive"',
})
panels = checked_text(previous.panels, {"len(panels) == 4": "len(panels) == 5"})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "The short header Hodram Bergstrom stays distinct from the two controlled names used in introductions.",
        4: "Janus Pasar gives the same name after Hodram clarifies that he is asking for Janus's name instead of the ship's.",
        6: "Julio Erneco is Cristina's grandfather in this exchange. She calls him Grandpa because the relationship is explicit.",
        7: "Cristina Erneco is the established current header. Mivor's address stays consistent with her introduction.",
        12: "Yukihisa Shiraki is the short header. He introduces himself aloud as Yukihisa Genjo Shiraki.",
        14: "Emilio Ferog is the full spoken introduction and the header, including the registered regular-font F.",
        16: "Gerhard Adernkatz expresses his own doubts about the legend, the investment, and the proposed recruit.",
        18: "Charles Rochefort is the crewmate who names chopsticks and reacts to Yukihisa's speed.",
        24: "Sera Shahrbaraz is the short header when she returns to her homeland and interprets for Sirwood.",
        26: "Julian Lopes is the current short header. Hodram addresses him by his given name at the crown exchange.",
        41: "Sojin Kurushima is the header. He uses his surname in the threat to the visitors.",
        78: "Sirwood Eme is the approved header for the man whose opaque words Sera interprets.",
        79: "Mivor Genz introduces himself by the same name in London. His extravagant address to Cristina reflects his own feelings.",
        82: "Shopkeeper remains the role label for the speaker heard in the bullring crowd.",
        95: "Patron identifies a generic spectator. His laughter and approval convey no shared name or relationship.",
        104: "Trader is the established role label for the spectator who announces the main performer.",
        113: "Port Worker identifies both the source summons speaker and the same role appearing in the crowd.",
        147: "Guildmaster is the existing role label for the spectator who shouts in approval.",
        158: "Sailor is the header for Kurushima's follower. His spoken address to the leader is boss.",
        162: "Boy is the role in the dockside aftermath and the matching literal caption in the earlier rescue panels. Familiar forms of address establish no kinship with the crew.",
        167: "Lady is the existing role header. She explicitly says the boy is hers and thanks his rescuers.",
    }
''',
})
verify_retained_symbols = FunctionType(previous.verify_retained_symbols.__code__,
    previous.verify_retained_symbols.__globals__ | {
        "HISTORICAL": HISTORICAL, "PROOF": PROOF, "OPAQUE": OPAQUE, "SYMBOLS": SYMBOLS, "stage": stage,
    })

scope = previous.scope | globals()
verify_retained_symbols.__globals__["scope"] = scope
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::native-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
    if not OPAQUE.exists():
        verify_retained_symbols()
