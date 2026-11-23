"""Check the opening pages, name widths, and unchanged speakerless controls."""

from inspect import getsource
from types import FunctionType

from scripts import stage_hodram_B0_B23_20261122 as stage
from scripts import verify_hodram_opening_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {
    "DK4_MES_B3_R0047": ("Gerhard", "Gerhard Adernkatz"),
    "DK4_MES_B5_R0005": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B17_R0269": ("Yukihisa", "Yukihisa Shiraki"),
}

check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})


def audit_macro_widths():
    original = previous.display.display.paragraph
    source = checked_text(getsource(original), {
        '{macro: example for macro in tokens}':
            '{macro: example + " Fleet" if macro == "FO" else example for macro in tokens}',
    })
    scope = vars(previous) | original.__globals__
    exec(compile(source, __file__ + "::Hodram-fleet-expansion-width", "exec"), scope)
    return scope["paragraph"]


verification = checked_text(previous.verification, {
    'len(entries) == 120 and fe_count == 9 and len(style_objects) == 1':
        'len(entries) == 201 and fe_count == 9 and not style_objects',
    '[49, 52] and [m["count"] for m in choices] == [2, 2]': '[]',
    '"hodram_B24_B53_progressive"': '"hodram_B0_B23_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Keep the short Hodram Bergstrom nameplate and the full Hodram Joakim Bergstrom catalogue form.",
        7: "Cristina Erneco is the name of the crewmate who steps into the mutiny alongside Al Shin.",
        12: "Yukihisa Shiraki identifies Muramasa, offers Al Shin formal aid, and later comments on loyalty.",
        16: "Gerhard Adernkatz is the named officer who reports on the prisoners, recognizes the recovered object, and warns Hodram.",
        17: "Keep Al Shin in the header. Yukihisa and Hodram use Al in direct address, as in the Japanese.",
        18: "Charles Rochefort is the short form. The alternate prisoner report and his excited response to the mutineers use that header.",
        23: "Manuel Almeida gives one of the prisoner reports and delivers the three-part elegy.",
        27: "Aziza Nurennahar introduces her full name in the retreat. She explicitly asks to be called Aziza after joining.",
        34: "Barbarossa Hayreddin is the established name of the captain issuing the Caribbean challenge.",
        63: "Julian Vermeer is the man Hodram stops and later takes to Sao Jorge.",
        65: "Plett Perrault is the named fugitive in the confrontation and Hangzhou transfer.",
        66: "Jean Ramusio is the trader called out by Gerhard. Hodram mentions the Basra guild after the encounter.",
        68: "Jacob Portunto is named in the smuggling exchange and keeps the same identity on the Calicut transfer.",
        71: "William Clive is the named pirate whose distinctive laughter and repeated threats remain in his dialogue.",
        72: "Hernan Berio is the established name of the opponent who boasts that others flee at sight of him.",
        73: "Iscal Yasar is the opponent named in the king's order and keeps the same header when he accepts.",
        153: "Sailor is the source role. The crew's cheers introduce no individual name or shipboard rank.",
        183: "Angel is Aziza's crew member, named when she gives the steering order and identified by the same control in the mutiny.",
        184: "Snake is Aziza's crew member, named when she gives a command and identified by the same control in the mutiny.",
        185: "Dandy is Aziza's gunner in the confrontation and the same man who names the price for her release.",
    }
''',
})
scope = previous.scope | globals()
for source in (previous.panel_source, verification, names):
    exec(compile(source, __file__ + "::opening-native-display", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
