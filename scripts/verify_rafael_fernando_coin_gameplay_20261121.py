"""Check Fernando's full native dialogue masks in the initialized replay."""
from inspect import getsource

from scripts import replay_rafael_fernando_coin_game_20261121 as replay
from scripts import verify_rafael_fernando_coin_game_20261121 as display
from scripts import verify_rafael_refit_sailing_gameplay_20261121 as template
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native = replay.stage, replay.base, replay.native
PROOF = replay.ROOT / "verified_gameplay.json"
STRATEGY, CLUE = "DK4_MES_B178_R0147", "DK4_MES_B178_R0257"
FOLLOWUPS = {"DK4_MES_B178_R0020", "DK4_MES_B178_R0024", "DK4_MES_B178_R0234", "DK4_MES_B178_R0240"}
BYTE_EXACT = "DK4_MES_B178_R0237"


source = checked_text(getsource(template.main), {
    '''            assert record["decision"] == "retention" and raw[:6] in (b"\\x00\\x40\\xff\\xff\\x00\\x6d", b"\\x00\\x40\\xff\\xff\\x00\\x17")''':
        '''            assert record["decision"] == "retention" and raw[:6] == b"\\x00\\x40\\xff\\xff\\x00" + bytes([rows[ident]["source_selector"]])''',
    '(followups if ident in FOLLOWUPS else holds).append(proof)':
        '(followups if ident in FOLLOWUPS or ident == BYTE_EXACT else holds).append(proof)',
    '''    question, = [r for r in holds if r["id"] == QUESTION]
    assert tuple(r["id"] for r in followups) == ("DK4_MES_B180_R0106", "DK4_MES_B180_R0110")
    assert question["frame"] < followups[0]["frame"] < followups[1]["frame"]
    assert checked[QUESTION]["native_pages"] == 1
    assert len(holds) == 19 and [m["block"] for m in menus] == [179, 180]''':
        '''    leads = [r for r in holds if r["id"] in (STRATEGY, CLUE)]
    assert [r["id"] for r in leads] == [STRATEGY, CLUE]
    assert all(checked[r["id"]]["native_pages"] == 1 for r in leads)
    assert {r["id"] for r in followups} == FOLLOWUPS | {BYTE_EXACT}
    assert len(holds) == 19 and [m["block"] for m in menus] == [178]''',
    'rafael_tutorials_gameplay_': 'fernando_gameplay_',
    'uninterrupted_wind_angle_question=question, unchanged_immediate_followups=followups':
        'uninterrupted_strategy_and_clue=leads, unchanged_sample_panels=followups',
    "Matched 19 revised pages, both lesson menus, and the one-page wind question followed by Manuel's reply.":
        "Matched 19 revised pages, five retained panels, and both game captions.",
})
scope = vars(template) | globals()
exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
