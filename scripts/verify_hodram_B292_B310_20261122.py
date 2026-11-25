"""Check the native expedition displays and source-bound nameplates."""

from types import FunctionType

from scripts import stage_hodram_B292_B310_20261122 as stage
from scripts import verify_hodram_B261_B291_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage":stage})
verify_menu_with_block = FunctionType(previous.verify_menu_with_block.__code__,
    previous.verify_menu_with_block.__globals__ | {"ROOT":ROOT})
panels = checked_text(previous.panels, {
    'assert len(panels) == 27 and len(pictures) == 28': 'assert len(panels) == 17 and len(pictures) == 18',
})
verification = checked_text(previous.verification, {
    'len(entries) == 371 and fe_count == 27 and len(style_objects) == 15':
        'len(entries) == 439 and fe_count == 17 and len(style_objects) == 26',
    '[(243, 2), (290, 3), (290, 2), (291, 2)]':
        '[(294, 2), (300, 2), (302, 2), (302, 2), (304, 2), (309, 3)]',
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 108':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 175',
    '"hodram_B261_B291_progressive"': '"hodram_B292_B310_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the approved label. The crew addresses him by rank and by the given-name substitution in different turns.",
        16: "Gerhard Adernkatz remains the officer's name. He warns the crew about the smoke and comes to Hodram's aid in the bog.",
        18: "Charles Rochefort keeps his registered speaker name. Gerhard calls him Charles, and the absent-character checks use the same given name.",
        68: "Jacob Portunto is the approved caption for the man caught with the cargo in the carried Calicut scene.",
        120: "Guard is the source role for the court attendant welcoming Hodram in the carried audience.",
        125: "King is the nameplate for the Swedish ruler. Your Majesty is Hodram's address in speech.",
        137: "Senior Monk remains the established label for the monk at Kinkaku-ji, who identifies the keepsake and gives the village directions.",
        147: "Guildmaster is the source role for the official who asks for help with the monster and later pays the reward.",
        148: "Guildmaster remains the source role for the person giving the gate and ruin directions in the carried Calicut exchange.",
        151: "Sailor is the regular label for the speaker who reacts to expedition danger or answers Gerhard's head count.",
        192: "Matilda gives the Colosseum lead and reminds the captain to buy a map. Retain the established spelling.",
        194: "Faticia gives the unconfirmed story of a Christian village. Retain her established speaker spelling.",
        197: "Safia speaks about dancing and offers the tip about the mosque as thanks.",
        201: "Mihwa gives directions to the gate in confidence and refers to her country's isolation policy.",
        203: "Sakura invites Hodram to visit a temple, guides him partway, and gives the farewell in the preceding expedition block.",
    }
''',
})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::native-expeditions", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
