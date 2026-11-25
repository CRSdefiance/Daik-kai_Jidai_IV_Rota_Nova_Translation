"""Staged successor with a readable opening page for Yukihisa's letter."""

from types import FunctionType

from scripts import stage_hodram_B201_B220_20261122 as predecessor


from scripts.stage_hodram_B201_B220_20261122 import (  # re-export the stage and parent interfaces
    ARCHIVE, BLOCKS, DEFAULT_NAMES, FE_MACROS, SOURCE, TOKEN, base, engine, logical_end, modal, native, parent, paired,
)


ROOT = predecessor.ROOT.with_name("B201_B220_staged_v2")
OUTPUT = predecessor.OUTPUT.with_name("B201_B220_scoped_manuscript_v2.json")
ROM, PROOF = ROOT / predecessor.ROM.name, ROOT / predecessor.PROOF.name
REFINEMENTS = predecessor.REFINEMENTS | {
    "213_R0027": (
        "Word has reached me of Muramasa, the legendary cursed blade. This masterwork is said to bode ill for Japan's ruler, Tokugawa. Efforts are under way to destroy such blades.",
        ["of Muramasa,", "the legendary cursed blade.", "bode ill for", "Japan's ruler, Tokugawa.", "destroy such blades."],
    ),
}
scope = vars(predecessor) | globals()
scope["collect"] = FunctionType(predecessor.collect.__code__, scope)
if __name__ == "__main__":
    old_main = predecessor.getsource(predecessor.previous.main)
    exec(compile(old_main, __file__ + "::stored-rom", "exec"), scope)
    scope["main"]()
