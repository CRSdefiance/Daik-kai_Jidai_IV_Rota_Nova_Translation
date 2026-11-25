"""Verify the revised sailing and room instructions in the emulator excerpts."""
from inspect import getsource

from scripts import replay_refit_sailing_parallel_routes_20261121 as replay
from scripts import verify_fernando_parallel_gameplay_20261121 as template
from scripts import verify_refit_sailing_parallel_routes_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native = replay.stage, replay.base, replay.native
PROOF = replay.ROOT / "verified_gameplay.json"
HEADERS = {2: "Lil Argot", 9: "Camille Overijssel", 23: "Manuel Almeida", 109: "Shipwright"}


source = checked_text(getsource(template.main), {
    'previews.append(("Play / Pass", shot))': 'previews.append((" / ".join(labels), shot))',
    'changed = data["decision"] == "revision" and ident != display.BYTE_EXACT':
        'changed = data["decision"] == "revision"',
    'fernando_SC{route}_actual_': 'lesson_SC{route}_actual_',
    'len(holds) == 30 and len(kept) == 4 and len(menus) == 1':
        'len(holds) == 36 and len(kept) == 1 and len(menus) == 2',
    '''    assert {r["speaker"] for r in holds}.issuperset({"Man", "Woman", "Camille Overijssel", "Fernando Dias"})
    assert menus[0]["route"] == 1 and set(menus[0]["labels"]) == {"Play", "Pass"}''':
        '''    assert {r["speaker"] for r in holds}.issuperset({"Shipwright", "Manuel Almeida", "Lil Argot", "Camille Overijssel"})
    assert {r["id"] for r in holds}.issuperset({"DK4_MES_B171_R0075", "DK4_MES_B171_R0098",
                                               "DK4_MES_B166_R0157", "DK4_MES_B166_R0161", "DK4_MES_B166_R0165"})
    assert [m["route"] for m in menus] == [1, 2]
    assert [m["labels"] for m in menus] == [["Listen.", "No thanks"], ["Please do", "Decline"]]''',
    "Matched 30 revised pages, four retained speeches and Hodram's complete choice menu.":
        "Matched 36 revised pages, one retained speech and both complete lesson menus.",
})
scope = vars(template) | globals()
exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
