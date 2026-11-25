"""Verify stored dialogue, FE substitutions, menus and the scoped nameplates."""

from inspect import getsource
from types import FunctionType

from scripts import stage_hodram_B171_B180_20261122 as stage
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
    '        assert all(token == "FI" for token in tokens)\n        expanded = body.replace(b"FI", b"Hodram")':
        '        assert tokens == (["FO"] if ident == stage.FLEET_PANEL else [])\n'
        '        expanded = body.replace(b"FO", stage.FLEET_NAMES[0].encode("ascii"))',
    '        rows, plane = render(expanded, "Hodram")': '        rows, plane = render(expanded, stage.FLEET_NAMES[0])',
    '            for name in ("I", "ABCDEFGHIJKLMNO", "ABCDEFGHIJKLMNOP"):\n'
    '                sample = body.replace(b"FI", name.encode("ascii"))':
        '            assert preflight and len(preflight["width_cases"]) == len(stage.FLEET_NAMES)\n'
        '            for name in stage.FLEET_NAMES[1:]:\n'
        '                sample = body.replace(b"FO", name.encode("ascii"))',
    '                if len(name) == 16:':
        '                planned, = [case for case in preflight["width_cases"] if case["name"] == name]\n'
        '                assert planned["rows"] == [list(value) for value in test]\n'
        '                assert planned["plane_sha256"] == native.digest(raster)\n'
        '                if name == stage.FLEET_NAMES[-1]:',
    'f"{ident} (16-cell name)"': 'f"{ident} (maximum fleet name)"',
    'assert len(panels) == 25': 'assert len(panels) == 17 and len(pictures) == 18',
})

verification = checked_text(previous.verification, {
    "len(entries) == 331 and fe_count == 25 and not style_objects":
        "len(entries) == 315 and fe_count == 17 and not style_objects",
    '    assert not choices': '    assert [(m["block"], m["count"]) for m in choices] == [(171,2)]',
    '"hodram_B151_B160_progressive"': '"hodram_B171_B180_progressive"',
    '    assert not style_objects\n    assert all(sum(map(len, obj["slot_owner_sets"])) == 8 for obj in style_objects)':
        '    assert not style_objects',
})
start, end = previous.names.index("    notes = {"), previous.names.index("    assert set(notes)")
names = checked_text(previous.names, {
    previous.names[start:end]: '''    notes = {
        1: "Hodram Bergstrom is the approved captain's nameplate. His spoken given name and surname keep their original substitutions.",
        4: "Janus Pasar is the crewmate reacting to the shipwright's lesson. Keep his turns separate from Manuel's and Cesare's.",
        6: "Julio Erneco recognizes Mikhail and protects Cristina. He explicitly calls her his granddaughter in speech.",
        7: "Cristina Erneco gives her approved first name and objects when Mikhail calls after her. The caption stays independent of her grandfather's address.",
        13: "Cesare Tony is the trained sailor who can react to the optional lesson. The existing caption identifies the speaker without adding another shipboard role.",
        16: "Gerhard Adernkatz advises Hodram about the Proofs and tests Yifa. Preserve his own role, as distinct from the person he addresses as Admiral.",
        23: "Manuel Almeida answers the shipwright's question about masts. His turn is part of the already qualified lesson.",
        24: "Sera Shahrbaraz remains the caption on her route through Mikhail's recruitment. Her name in speech belongs to Hodram's explanation and Mikhail's calls.",
        25: "Yifa Sol gives only Yifa when she signs on. Sanghyeon's account explains their closeness without changing her own name.",
        26: "Julian Lopes promises Mihwa the Silla Gold Crown and later credits Hodram. Preserve the established name she uses in reply.",
        76: "Mikhail Letzel is the short caption. The native catalogue carries a separate middle field, and the notice identifies his function as scholar.",
        81: "Sanghyeon Kan remains the established nameplate. He introduces himself by his given name and identifies his seniority under their shared master.",
        87: "Shopkeeper identifies the source square merchant who tells Hodram about Mikhail. This dialogue supplies no personal name.",
        109: "Shipwright is the source shop role. Giving the optional lesson does not make him an officer.",
        153: "Sailor identifies the anonymous voice answering the pirate's order. The scene supplies no individual rank or name.",
        165: "Woman is the shared caption for the onlooker who admires Mikhail and then rebukes him. Her familiar address establishes no kinship.",
        166: "Lady identifies the other onlooker. Her questions about the peppercorn are distinct from the first woman's reactions.",
        174: "Owner follows the clean role label for the woman who orders more bananas. Her confidence belongs to her forecast.",
        175: "Cook follows the source occupation for the man carrying out the order. His replies remain skeptical despite his compliance.",
        183: "Angel is the established name the pirate uses when he interrupts. Leave his standing aboard implicit.",
        201: "Mihwa is the approved short nameplate in the crown exchange and the name Julian uses when addressing her.",
        202: "Reika is the established short nameplate for the tavern worker in Seoul. Her description of Julian supplies the link to his visit.",
    }
''',
})
scope = previous.scope | globals()
for source in (panels, verification, names):
    exec(compile(source, __file__ + "::stored-proof-crown-pirate", "exec"), scope)


if __name__ == "__main__":
    if not PROOF.exists():
        scope["verify"]()
    if not NAMES.exists():
        scope["verify_names"]()

