"""Align the story's remaining Proof of Supremacy references with Help."""

from inspect import getsource
from pathlib import Path
import re

from scripts import register_story_phrase_wraps_20261118 as parent
from scripts import stage_palace_and_village_exchanges_20261115 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

native, base = precedent.native, precedent.base
ROOT = Path("work/proof_of_conquest_terms_20261118_v2")
ROM, STORED = ROOT / "Proof_of_Conquest_Terms_RESEARCH_ONLY.nds", ROOT / "staged.json"
MANUSCRIPT = precedent.MANUSCRIPT.with_name("proof_of_conquest_terms_20261118_v2.json")
OLD_TERM = re.compile(r"\bProofs?\s+of\s+Supremacy\b")
OFFSETS = {
    (1, 49, 10): 41, (1, 151, 33): 475, (1, 154, 48): 429, (1, 154, 58): 541,
    (2, 61, 55): 477, (2, 62, 110): 831, (2, 63, 65): 601, (2, 63, 80): 879,
    (2, 68, 90): 703, (2, 68, 96): 753, (2, 121, 586): 5649, (2, 122, 152): 1317,
    (2, 131, 5): 17, (2, 131, 82): 539, (2, 139, 5): 17, (2, 139, 48): 805,
    (2, 149, 100): 1211, (2, 149, 115): 1341,
}
BLOCKS = {(route, block): (route, block) for route, block, _ in OFFSETS}
HISTORY = (
    (),
    ("hodram_B49_contextual_final_review_v1", "hodram_B151_B170_contextual_final_review_v1"),
    ("lil_kuhn_resolution_contextual_final_review_v1", "lil_clifford_north_new_world_contextual_final_review_v1",
     "lil_B122_B127_contextual_final_review_v1", "lil_B131_B133_contextual_final_review_v1",
     "lil_B139_B140_contextual_final_review_v1"),
    (),
)
CONTEXT = {
    (1, 49): "Lil teases Hodram about holding the local Proof and sets the terms of their bargain.",
    (1, 151): "Hodram's crew watches a pattern appear on the blade and interprets it as the New World map.",
    (1, 154): "Hodram congratulates Charles or Yifa on the Mediterranean map, depending on who assisted.",
    (2, 61): "A demand for the collected Proofs follows a hostage threat. Lil confronts the demand.",
    (2, 62): "The crew examines the sheath after learning where it came from. Lil wonders whether it relates to a Proof.",
    (2, 63): "The New World map emerges from the blade. The crew's matching discoveries preserve different voices.",
    (2, 68): "Lil and her crew recognize the stolen Proof before the exchange turns to Clifford's letter.",
    (2, 121): "The speaker gives the recipient an item needed to decipher a map. The next reply acknowledges the gift.",
    (2, 122): "The crew recognizes the stolen Proof again as the event turns to a letter.",
    (2, 131): "Lil suspects the Old Parchment is a map. The result confirms her hunch about the North Sea.",
    (2, 139): "Lil pairs the Evergreen Lotus Leaf with the Kushan Platter. The crew is ready to seek the Indian Ocean Proof.",
    (2, 149): "The crew takes the Tang Bamboo Craft apart using its plan. Lil and her companions react to the map hidden on its reverse.",
}
# This block predates the individual final reviews used for the other blocks.
# The existing route ledger credits it. Read the complete clean exchange here.
B149_NOTES = {
    5: "Lil complains the Tang Bamboo Craft is so intricate that looking at it makes her head hurt.",
    17: "The companion counters that just looking at it makes him hungry. Keep the joke as an echo of Lil's complaint.",
    28: "Camille says to follow the drawing in the Bamboo Assembly Plan.",
    32: "Lil protests she is no good at this and points to Camille's skill.",
    35: "Camille starts working the pieces off, narrating the first steps.",
    38: "Camille thinks he has taken everything apart. His relief still leaves room for doubt.",
    41: "Lil praises Camille's skill with delicate work.",
    44: "Camille calls the captain a flatterer. Preserve the native first-name substitution.",
    48: "Lil says the praise was sincere and playfully insists she will not praise him again. Keep the comic bonk.",
    53: "The companion admires whoever designed the object.",
    56: "The companion suggests following the diagram to take the craft apart.",
    60: "Lil insists she already cannot do it and tells him to take over.",
    63: "He starts picking out the steps and grumbles that it is more troublesome than reading dice.",
    67: "He thinks he has disassembled it completely.",
    79: "Camille says he was joking, then notices a drawing on the reverse of the bamboo.",
    85: "Lil stammers through an impressed acknowledgment.",
    89: "The companion credits his own skill in a clipped boast.",
    93: "The companion notices a drawing on the reverse of the bamboo.",
    100: "Lil identifies the drawing as a map to East Asia's Proof. Preserve her excitement and the regional identification.",
    110: "Camille celebrates and suggests looking immediately.",
    115: "The companion calls it good luck and says they can find the Proof quickly.",
}

def revise_term(route, block, number, source, previous):
    assert (route, block, number) in OFFSETS
    assert "覇者の証" in source or "覇者のしるし" in source or (route, block, number) == (2, 121, 586) and "『証』" in source
    match, = list(OLD_TERM.finditer(previous))
    phrase = match[0].replace("Supremacy", "Conquest")
    protect = {
        (2, 61, 55): ("Hand them over,",),
        (2, 139, 5): ("Evergreen Lotus Leaf", "Kushan Platter"),
    }
    return OLD_TERM.sub(phrase, previous), (phrase, *protect.get((route, block, number), ())), (
        "Use the Help term for this same quest item. Keep its number, region, the speaker's meaning and the full title together."
    )


SCOPE = vars(precedent) | globals() | {"RETENTIONS": {}, "EDITS": OFFSETS}
exec(compile(getsource(precedent.historical), __file__ + "::history", "exec"), SCOPE)
old_lookup = '''        old_path, old_index, earlier = past[ident]
        assert all(earlier["review"].get(g) is True for g in native.GATES), (route, ident)
        before, fixed = [bytes.fromhex(row["raw_hex"]) for row in (source, current)]
        earlier_source = bytes.fromhex(earlier["source_hex"]).rstrip(b"\0")
        assert earlier_source.endswith(before) or before.endswith(earlier_source), (route, ident, earlier_source, before)
        previous = " ".join(fixed[1:].decode("cp932").split())
        old_english = earlier["english"]'''
# inspect.getsource contains the literal backslash in b"\0".
old_lookup = old_lookup.replace(chr(0), "\\0")
new_lookup = '''        before, fixed = [bytes.fromhex(row["raw_hex"]) for row in (source, current)]
        previous = " ".join(fixed[1:].decode("cp932").split())
        if (route, block) == (2, 149):
            note = B149_NOTES[number]
            roles = {2: "Lil", 9: "Camille", 14: "Crew member", 20: "Crew member"}
            earlier = dict(speaker=roles[selector], english=previous, source_meaning=note,
                           localization_note=note + " The current wording carries this beat.",
                           review=dict.fromkeys(native.GATES, True))
            old_path, old_index = base.LEDGER, None
        else:
            old_path, old_index, earlier = past[ident]
            assert all(earlier["review"].get(g) is True for g in native.GATES), (route, ident)
            earlier_source = bytes.fromhex(earlier["source_hex"]).rstrip(bytes(1))
            assert earlier_source.endswith(before) or before.endswith(earlier_source), (route, ident)
        old_english = earlier["english"]'''
source = checked_text(getsource(precedent.review_exchange), {
    old_lookup: new_lookup,
    '        edit = EDITS.get((route, block, number))':
        '''        key = route, block, number
        assert bool(OLD_TERM.search(previous)) == (key in OFFSETS)
        edit = None
        if key in OFFSETS:
            assert current["offset"] == OFFSETS[key]
            edit = revise_term(*key, before[1:].decode("cp932"), previous)''',
})
exec(compile(source, __file__ + "::exact-exchanges", "exec"), SCOPE)
source = checked_text(getsource(precedent.collect), {
    '        for group, blocks in BLOCKS.items():\n            n = blocks[route]':
        '        for group, (owner, n) in BLOCKS.items():\n            if owner != route:\n                continue',
})
exec(compile(source, __file__ + "::current-input", "exec"), SCOPE)
source = checked_text(getsource(precedent.main), {
    '    assert len(groups) == 20': '    assert len(groups) == len(BLOCKS) and len(edited) == len(OFFSETS)',
    '    ROOT.mkdir(parents=True)':
        '''    assert not any(OLD_TERM.search(data.decode("latin1")) for data in native.files(ctx.image).values())
    ROOT.mkdir(parents=True)''',
})
exec(compile(source, __file__ + "::validated-output", "exec"), SCOPE)

if __name__ == "__main__":
    SCOPE["main"]()
