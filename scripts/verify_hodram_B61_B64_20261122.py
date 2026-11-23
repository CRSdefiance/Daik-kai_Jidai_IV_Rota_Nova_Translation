"""Verify the native pages and nameplates of Hodram's four linked scenes."""

from types import FunctionType

from scripts import stage_hodram_B61_B64_20261122 as stage
from scripts import verify_hodram_B54_B60_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, PATH = stage.base, stage.native, stage.parent, previous.PATH
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
CONTEXT_SHORT_NAMES = {"DK4_MES_B63_R0045": ("Hodram", "Hodram Bergstrom")}
check_progressive = FunctionType(previous.check_progressive.__code__,
    previous.check_progressive.__globals__ | {"stage": stage})
verification = checked_text(previous.verification, {
    'len(entries) == 82 and fe_count == 1 and not style_objects':
        'len(entries) == 96 and fe_count == 0 and not style_objects',
    '"hodram_B54_B60_progressive"': '"hodram_B61_B64_progressive"',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the nameplate; Sera calls him by his given name and the trader addresses him as admiral.",
        16: "Gerhard Adernkatz recognizes Nagarpur and gives his own appraisal of the company.",
        17: "Al Shin reacts to the insulting offer of a tip without an added shipboard title.",
        18: "Charles Rochefort interprets Nagarpur's boast for the other crew members.",
        20: "Fernando Dias distinguishes enjoying money from treating it as everything.",
        24: "Sera Shahrbaraz uses the established nameplate while her fluency develops through the exchanges.",
        38: "Zamorin Nagarpur is the established displayed form. The escort uses Nagarpur in the procession.",
        105: "Trader fits the occupational label for the giver of the item in the opening of the legend exchange.",
        154: "Sailor is the role label for the voice clearing the road for Nagarpur's party.",
    }
''',
})


def qualified_panels(ctx, draft, staged):
    assert all(row["source_selector"] != 254 for row in draft["records"])
    return {}, []


scope = previous.scope | globals()
for source in (verification, names):
    exec(compile(source, __file__ + "::native-pages", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()
