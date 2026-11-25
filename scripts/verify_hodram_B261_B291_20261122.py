"""Verify the staged guild, forest, and cave displays with the registered runtime."""

from types import FunctionType

from scripts import stage_hodram_B261_B291_20261122 as stage
from scripts import verify_hodram_B241_B260_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verify_menu_with_block = FunctionType(previous.verify_menu_with_block.__code__,
    previous.verify_menu_with_block.__globals__ | {"ROOT": ROOT})
panels = checked_text(previous.panels, {
    'assert len(panels) == 20 and len(pictures) == 23': 'assert len(panels) == 27 and len(pictures) == 28',
})
verification = checked_text(previous.verification, {
    'len(entries) == 240 and fe_count == 20 and len(style_objects) == 3':
        'len(entries) == 371 and fe_count == 27 and len(style_objects) == 15',
    '[(243, 2), (251, 2), (252, 3), (252, 2)]': '[(243, 2), (290, 3), (290, 2), (291, 2)]',
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 23':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 108',
    '"hodram_B241_B260_progressive"': '"hodram_B261_B291_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom remains the approved nameplate. Surname and given-name calls in these scenes use their established separate substitutions.",
        6: "Julio Erneco remains the caption for the crew member who first notices the church figurehead and asks the priest about it.",
        14: "Emilio Ferog remains the established label when his quiet breathing answers Hodram's question. Emilio is the form Hodram uses in the exchange.",
        16: "Gerhard Adernkatz is the established officer's label in the conversations about the Proofs, the pirate hunt and the cave.",
        18: "Charles Rochefort is the established officer's nameplate. The cave shortcut is his suggestion.",
        22: "Samwell Khan is the established short nameplate. In the bear encounter his warning is separate from the crew style variants.",
        63: "Julian Vermeer is the established spelling in the assignment and on the captured man's nameplate. The separate courier role belongs to his story.",
        65: "Plett Perrault is the established name in the bounty and the captive's response. Keep the same spelling in both.",
        66: "Jean Ramusio is the name the guildmaster gives and the established caption when Jean defends himself.",
        67: "Gabriel Cardocci appears by the same full name at the tavern and when Hodram returns him to the guild.",
        68: "Jacob Portunto matches the guildmaster's wanted man. The cargo complaint supplies character voice.",
        71: "William Clive is the established captive's nameplate. The guildmaster identifies him as William in speech.",
        72: "Hernan Berio is the established name in the assignment and his pompous demand for passage.",
        92: "Barkeep is a familiar label for the person demanding Gabriel settle his tab.",
        113: "Port Worker is the shared role for the messenger from the Stockholm guild. The scene supplies no personal name.",
        114: "Port Worker is the same role for the man passing on the Sao Jorge guild's message.",
        119: "Port Worker is the same role for the Havana messenger. He asks the captain's surname before giving the news.",
        120: "Guard is the established court role for the speaker announcing the summons and welcoming the admiral back.",
        125: "King is the established caption for the Swedish ruler. Your Majesty is Hodram's spoken address.",
        139: "Priest remains the contextual label for the keeper of the church figurehead. The two revised lines describe its history and return.",
        147: "Guildmaster is the established role for the official handling Gabriel, Julian and William.",
        148: "Guildmaster is the established role for the official who commissions the bounty and pays the rewards for Jean, Jacob and Hernan.",
        149: "Guildmaster is the established role for the official who asks for help with Plett and defers to the woman who brought the case.",
        151: "Sailor is the shared role for the crew member reporting what Gabriel hid and for the attendees in the later alerts.",
        179: "Villager is the established role for the man asking for help finding his ancestors' ruins. The conversation supplies his perspective and no personal name.",
    }
''',
})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::guild-forest-and-cave", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
