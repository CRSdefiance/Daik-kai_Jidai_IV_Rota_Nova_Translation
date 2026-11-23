"""Check native dialogue, trade notices, choices, and Hodram's speaker labels."""

from inspect import getsource
from types import FunctionType

from scripts import stage_hodram_B181_B200_20261122 as stage
from scripts import verify_hodram_B151_B160_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {}
expansion = previous.previous.expansion
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})

panels = checked_text(getsource(previous.qualified_panels), {
    "library = previous.expansion": "library = expansion",
    '        assert all(token == "FI" for token in tokens)':
        '        assert tokens == (["FI"] if ident == stage.CHARM_PANEL else [])',
    '                variants.append(dict(name=name, rows=test, expanded_hex=sample.hex(),':
        '                assert test == [(0, 0, f"{name}: Charm +1!")]\n'
        '                variants.append(dict(name=name, rows=test, expanded_hex=sample.hex(),',
    'assert len(panels) == 25': 'assert len(panels) == 21 and len(pictures) == 22',
})
verification = checked_text(previous.verification, {
    "len(entries) == 331 and fe_count == 25 and not style_objects":
        "len(entries) == 284 and fe_count == 21 and not style_objects",
    '    assert not choices': '    assert [(m["block"], m["count"]) for m in choices] == [(200, 2)] * 6',
    '"hodram_B151_B160_progressive"': '"hodram_B181_B200_progressive"',
})

start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the approved nameplate. His customary flag and given-name substitutions stay native.",
        6: "Julio Erneco speaks as the crewmate who brings the sake advice directly to Hodram.",
        19: "Carlo Sinat is the speaker who recognizes the seller's markup. His aside keeps the negotiated price advice private.",
        20: "Fernando Dias is the source companion who reacts to the merchants' information about the market.",
        25: "Yifa Sol uses her established nameplate when discussing the peppers in Seoul.",
        82: "Shopkeeper identifies the source merchant who cannot tie up working money in decorative ceramics.",
        85: "Shopkeeper identifies the source merchant negotiating over the framing of the painting in Basra.",
        86: "Shopkeeper identifies the source merchant selling the dye in Calicut.",
        87: "Shopkeeper identifies the anonymous merchant who passes along the almond rumor.",
        92: "Barkeep fits the source tavern role serving drinks in Sao Jorge and cheese in Veracruz.",
        96: "Patron identifies the anonymous wine customer whose drink and opinion are interrupted.",
        103: "Patron identifies the second customer who hears about the cheese and asks to try it.",
        104: "Trader identifies the commerce role that overhears the ceramics offer.",
        110: "Shipwright is the source occupation for the man competing for the painting.",
        113: "Port Worker is the existing role for the ceramics eavesdropper's companion in Hamburg.",
        115: "Port Worker keeps the source regional labor role for the man discussing tobacco.",
        117: "Port Worker identifies the Hangzhou customer who comments on the sake.",
        119: "Port Worker fits this shared role for the customer in the Havana and Veracruz exchanges.",
        130: "Daimyo preserves the explicitly Japanese feudal title in the glass scene.",
        132: "Officiant preserves the source ceremonial role for a separate bidder on the painting.",
        147: "Guildmaster identifies the source guild official who discusses the purchase of ceramics.",
        148: "Guildmaster identifies the different guild official among the painting bidders.",
        150: "Guildmaster preserves the existing source role for the Osaka speaker who addresses the daimyo respectfully.",
        152: "Sailor is the shared generic caption for the man arguing that wine is in fashion.",
        153: "Sailor identifies the anonymous speaker in the art and tobacco conversations.",
        154: "Sailor reflects the informal role of the companion who urges an immediate dye purchase.",
        155: "Sailor identifies the speaker with a cough without implying medical authority.",
        156: "Sailor identifies the anonymous crew member talking about sake.",
        159: "Sailor preserves the distinct speaker ID for the answer about the alleged Havana remedy.",
        164: "Man is the localized nameplate for the other speaker in the tea and winter scenes. The shared source couple category adds no spoken kinship.",
        165: "Woman is the localized nameplate for the speaker who requests tea and later asks for a fur coat. Her caption fits both scenes.",
        166: "Lady fits the first speaker in the women's shared social conversations. Any husband or friend mentioned belongs to the specific dialogue.",
        167: "Lady fits the second speaker in the women's conversations and preserves her separate actor selection.",
        168: "Lady fits the third speaker in the women's conversations. Her lines supply her own opinions.",
        173: "Shady Man preserves the established anonymous role in all six rounds of bargaining.",
        174: "Owner is the clean storefront role in both the tomato and the sweets exchanges.",
        175: "Cook preserves the source occupation of the man asked to prepare the food.",
    }
''',
})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::town-and-market", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
