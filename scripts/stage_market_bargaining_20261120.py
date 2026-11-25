"""Review the complete Market confirmation and bargaining exchange on the current build."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_market_english_region_20261120 as parent
from scripts import stage_market_conversation_20261115 as workflow
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_ruin_discovery_display_20261120 import apply_xdelta, make_xdelta


base = parent.base
ROOT = Path("work/market_bargaining_20261120_v1")
ROM, STORED, MANUSCRIPT = ROOT / "Market_Bargaining_RESEARCH_ONLY.nds", ROOT / "staged.json", ROOT / "review.json"
ARM, COMMON, CLEAN = workflow.ARM, workflow.COMMON, workflow.CLEAN
PRIOR = workflow.MANUSCRIPT
REVISIONS = {
    14: "All set, then?",
    25: "Come on, can't you do a bit better?",
}
PHRASES = {}
NOTES = workflow.NOTES | {
    14: (workflow.NOTES[14][0],
         "Keep the direct check with a natural short tag. The same words work for either side of the deal."),
    18: (workflow.NOTES[18][0],
         "Keep the sentence about the fee and the complete town question. London’s own quote is zero coins, and the trader leaves the exact amount to the selector."),
    25: (workflow.NOTES[25][0],
         "The excited opening and a bit preserve the insistence and size of the request. A better price can favor a buyer or a seller."),
}


def main():
    prior = {row["message_ID"]: row for row in base.load(PRIOR)["records"]}
    source = checked_text(getsource(workflow.main), {
        "    edited = encoded_changes()\n": """
    assert prior.keys() == NOTES.keys()
    for n, row in prior.items():
        assert row["source_hex"] == source[n].text.hex()
        assert row["english"] == " ".join(old[n].text.decode("ascii").split())
    edited = encoded_changes()
""",
        "        assert 1 <= len(after) <= 3 and all(after)": """
        assert 1 <= len(after) <= 3 and all(after)
        assert " ".join(body.decode("ascii").split()) == REVISIONS.get(n, prior[n]["english"])
        assert all(len(line) <= 38 for line in after)
""",
        "            plane, _ = render_portrait(raster, arm, kanji, body)": """
            assert after == [REVISIONS[n]]
            plane, glyphs = render_portrait(raster, arm, kanji, body)
            assert glyphs[0]["code"] == ord(REVISIONS[n][0]) and glyphs[-1]["code"] == ord(REVISIONS[n][-1])
""",
        "    print(f'Reviewed":
            "    build_patch()\n    print(f'Reviewed",
    })
    scope = vars(workflow) | globals() | {"prior": prior}
    scope["encoded_changes"] = FunctionType(workflow.encoded_changes.__code__, scope)
    exec(compile(source, __file__ + "::same-market-native-consumers", "exec"), scope)
    scope["main"]()


def build_patch():
    delta, rebuilt = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
    make_xdelta(CLEAN, ROM, delta)
    apply_xdelta(CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()


if __name__ == "__main__":
    main()
