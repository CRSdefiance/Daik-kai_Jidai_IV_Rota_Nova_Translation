"""Verify the native displays, panels, puzzle choices, and speaker labels."""

from types import FunctionType

from scripts import stage_hodram_B241_B260_20261122 as stage
from scripts import verify_hodram_B201_B220_20261122 as template
from scripts import verify_hodram_B221_B240_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verify_menu_with_block = FunctionType(template.verify_menu_with_block.__code__,
    template.verify_menu_with_block.__globals__ | {"ROOT": ROOT})
expansion = template.expansion
panels = checked_text(template.panels, {
    'f"{name}: {stage.FE_MACROS[ident]} +1!"': 'f"{name}{stage.FE_MACROS[ident]}"',
    'assert len(panels) == 30 and len(pictures) == 33': 'assert len(panels) == 20 and len(pictures) == 23',
})
verification = checked_text(template.verification, {
    "len(entries) == 350 and fe_count == 30 and len(style_objects) == 3":
        "len(entries) == 240 and fe_count == 20 and len(style_objects) == 3",
    "[(201, 3), (205, 2), (210, 2), (210, 2), (216, 2), (216, 3)]": "[(243, 2), (251, 2), (252, 3), (252, 2)]",
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 22':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 23',
    '"hodram_B201_B220_progressive"': '"hodram_B241_B260_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom remains the approved short nameplate. The source calls to his name and surname use their separate substitutions.",
        4: "Janus Pasar is the established navigator's caption. Hodram recognizes him before explaining his injury.",
        6: "Julio Erneco is the speaker who notices the figurehead and calls to the priest and admiral in turn.",
        13: "Cesare Tony gives his own view of the warm figurehead. The rewards distinguish his given name from the captain's substitution.",
        18: "Charles Rochefort remains the short nameplate for his convoy letter. His registered signature elsewhere in that letter remains intact.",
        20: "Fernando Dias remains the nameplate for the sailor who reads the puzzle and reacts to the voice. Use the established ASCII capital F.",
        64: "Yuris Huygens is the established caption, and the dialogue establishes his name, estate, and duties.",
        113: "Port Worker stays the shared source role for the man offering gloves and the messenger who brings news from the guild.",
        139: "Priest matches the source church role. Father is Julio's form of address in dialogue.",
        147: "Guildmaster identifies the official giving the survey and search assignments. His familiarity with Yuris belongs to the conversation.",
        178: "Follower is the existing role for the visitor buying maps. The encounter supplies no new name or rank.",
        186: "Francisca is the approved caption for the woman who identifies the stolen Frozen Rose and offers the church tip.",
        188: "Margrete keeps her approved spelling and speaks about a sailor's story in her own voice.",
        189: "Wanda gives her own answer about the town's ruins. Her caution differs from the other hostesses' leads.",
        190: "Julia greets the captain and gives a separate account of the ruins around her town.",
        193: "Myrine greets the captain and points out the visible hill. The approved short name stays consistent.",
        195: "Nelly promises directions to the pyramids and keeps her own familiar greeting.",
        196: "Hatra recommends seeing the ruins on a fine day. The treasury remains a claim she attributes to rumor.",
        200: "Titis is the established short caption for the hostess who makes an exception when sharing the nearby clue.",
    }
''',
})
scope = template.scope | previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::ruins-and-guild", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
