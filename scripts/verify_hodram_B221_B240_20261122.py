"""Audit the staged letters, ordinary speech, nameplates, and Crusades menu."""

from types import FunctionType

from scripts import stage_hodram_B221_B240_20261122 as stage
from scripts import verify_hodram_B201_B220_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})


verify_menu_with_block = FunctionType(previous.verify_menu_with_block.__code__,
    previous.verify_menu_with_block.__globals__ | {"ROOT": ROOT})


def qualified_panels(ctx, draft, staged):
    assert not draft["planned_FE"] and all(r["source_selector"] != 254 for r in draft["records"])
    return {}, []


verification = checked_text(previous.verification, {
    '            assert (raw != old) == bool(planned) == (row["decision"] == "revision")':
        '''            assert bool(planned) == (row["decision"] == "revision")
            identical = raw == old and planned is not None
            if identical:
                assert ident == "DK4_MES_B226_R0028" and row["english"] == row["previous_English"]
                assert bytes.fromhex(planned["encoded_hex"]) in (
                    old[5:old.index(0, 6)], old[5:old.index(0, 6)-1])
                planned = None
            assert (raw != old) == bool(planned)''',
    '            entries.append(entry)\n            if selector == 254:':
        '            entries.append(entry)\n            if identical:\n                entry["existing_wrap_already_exact"] = True\n            if selector == 254:',
    "len(entries) == 350 and fe_count == 30 and len(style_objects) == 3":
        "len(entries) == 291 and fe_count == 0 and len(style_objects) == 4",
    "[(201, 3), (205, 2), (210, 2), (210, 2), (216, 2), (216, 3)]": "[(224, 2)]",
    'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 22':
        'sum(len(obj["slot_owner_sets"]) for obj in style_objects) == 28',
    '"hodram_B201_B220_progressive"': '"hodram_B221_B240_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the approved nameplate for the admiral. The opinions he hears from the crew stay in their own voices.",
        4: "Janus Pasar is both the approved speaker name and the signature in his letter. The name now has a separate final row in the letter body.",
        11: "Jam Ludwyan is the short nameplate. Jam Jack Ludwyan remains the name he signs in his letter from India.",
        13: "Cesare Tony keeps his approved caption. His disciplined speech distinguishes him from the sailors he criticizes.",
        16: "Gerhard Adernkatz keeps the established surname and distinct voice in the sunset, Attila, and Martel exchanges.",
        17: "Al Shin speaks for himself when discussing Saladin. The shared merchant speaks separately.",
        18: "Charles Rochefort remains the short nameplate. Charles Jean Rochefort is the established signature in his letter.",
        19: "Carlo Sinat gives the lead about the old medical book and addresses Filippo by name in the neighboring trade scene.",
        20: "Fernando Dias is the crewmate scoffing at Jam's boasting. His regular English capital F remains the same in the caption and the letter.",
        21: "Ian Dukov is the approved nameplate and signature. The sender name Ian in the crew announcements refers to him.",
        22: "Samwell Khan is the approved short nameplate for the three matching rumors. The catalogue keeps its longer representation.",
        23: "Manuel Almeida keeps his established name and his reflective, familiar delivery about Attila and the chisel.",
        25: "Yifa Sol is the crewmate practicing the sword. Her teacher's voice is reported within her own turn.",
        26: "Julian Lopes is the speaker making the flattery in both town conversations. Lucia and Safia address him as Julian.",
        85: "Shopkeeper is the shared role for the merchant who challenges the account of the Crusades. No personal name is given.",
        104: "Trader is the standing role for the man Carlo addresses as Filippo. The conversation supplies the personal name.",
        151: "Sailor is the underlying reusable actor role. The mock retreat belongs to the play scene Gerhard describes, and its existing actor and portrait are explicit source controls.",
        162: "Boy is the source role for the child playing Charles Martel. The historical name belongs to the role he plays in speech.",
        197: "Safia is the approved nameplate and the form Julian uses to greet her. The Medusa comparison remains figurative.",
        199: "Lucia is the approved nameplate and the name Julian uses in the square. The empress comparison stays in speech.",
    }
''',
})
scope = previous.scope | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::rumors-and-letters", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
