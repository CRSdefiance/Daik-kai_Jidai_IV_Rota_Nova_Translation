"""Verify the linked scenes' pagination, substitutions, punctuation, and roles."""

from types import FunctionType

from scripts import stage_hodram_B54_B60_20261122 as stage
from scripts import verify_hodram_B0_B23_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {
    "DK4_MES_B58_R0172": ("Hodram", "Hodram Bergstrom"),
    "DK4_MES_B58_R0239": ("Manuel", "Manuel Almeida"),
}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verification = checked_text(previous.verification, {
    'len(entries) == 201 and fe_count == 9 and not style_objects':
        'len(entries) == 82 and fe_count == 1 and not style_objects',
    '"hodram_B0_B23_progressive"': '"hodram_B54_B60_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the short header. Sera uses his given name in her first attempts to speak.",
        20: "Fernando Dias is the speaker who condemns Espinosa's conduct and sees no reason for leniency.",
        23: "Manuel Almeida is the crewmate whose own experience in Sao Jorge leads to his vow against slavers.",
        24: "Sera Shahrbaraz is the short header. Sera Altos Shahrbaraz remains the catalogue form. Use the inherited unidentified caption before her portrait and name appear.",
        36: "Geronimo Espinosa is the short header. The catalogue preserves the separate de field in Geronimo de Espinosa.",
        84: "Shopkeeper is the natural role label for the shop owner from the Square. His testimony and later request establish no other occupation or title.",
        113: "Port Worker fits the source's familiar label for someone working at the departure office. This variant relays a guildmaster's request.",
        114: "Port Worker is the same source occupation for the villager who confronts Espinosa about his family's disappearance.",
        119: "Port Worker covers the same departure-office role in this port. The source's regional field describes the variant and is not a nameplate title.",
        141: "Innkeeper identifies the woman by her occupation without turning the source form of address into a familial relationship.",
    }
''',
})
panels = checked_text(previous.previous.panel_source, {"len(panels) == 9": "len(panels) == 1"})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::linked-native-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
