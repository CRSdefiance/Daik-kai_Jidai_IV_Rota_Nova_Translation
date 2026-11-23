"""Match the initialized Lil dialogue to its complete native glyph masks."""

from inspect import getsource

from scripts import replay_company_name_dialogue_20261121 as replay
from scripts import verify_company_name_dialogue_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, stage = replay.base, replay.build.native, replay.build
ROOT, ROM, SETUP = replay.ROOT, replay.ROM, replay.SETUP
LIVE = ROOT / "verified_playback.json"


def main():
    original = replay.earlier
    proof = base.load(display.PROOF)
    assert proof["candidate_sha256"] == base.digest(stage.ROM)
    names = proof["default_name_macros"]["2"]
    source = checked_text(getsource(original.verify), {
        '    fe_paint = stage.stage.system.native_painter(lil_context())\n': '',
        '        ("maria", MARIA_SETUP, MARIA_ROM.parent / "live/capture/capture_report.json"),\n': '',
        '            body = raw[6:raw.index(0, 6)].replace(b"FO", b"Argot Co.").replace(b"FI", b"Lil").replace(b"FA", b"Argot")':
            '            body = display.prior.prior.default_text(raw[6:raw.index(0, 6)], names)',
        '''            if raw[5] == 254:
                physical = fe_paint(body)["physical"]
                planes = [bytes(int(bool(v)) for y in range(64) for v in physical[y * 228:y * 228 + 216])]
            else:
                planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''':
            '''            assert raw[5] < 207
            planes = [bytes.fromhex(p["native_plane_hex"]) for p in paint(arm, font, body)["pages"]]''',
        '    assert len(observed) == 19': '    assert len(observed) == 10',
        '    assert any(b"77,000" in bytes.fromhex(row["body_hex"]) for row in observed)':
            '''    fixes = {r["id"] for r in proof["punctuation_fixes"]}
    checked = {row["id"] for row in observed if row["id"] in fixes}
    assert checked == fixes
    for row in observed:
        if row["id"] in fixes:
            body = bytes.fromhex(row["body_hex"])
            assert b"Argot Co." in body and b"Argot Co.." not in body''',
        "initialized_Lil_and_Maria=True": "initialized_Lil=True",
        "actual_substitution_and_FE_receipt=True": "actual_company_substitution=True",
        "inventory_and_payment_accounting=False": "original_quest_effects=False",
        "initialized Lil and Maria dialogue holds": "initialized Lil dialogue holds",
    })
    scope = vars(original) | globals() | {"names": names, "proof": proof}
    exec(compile(source, __file__ + "::actual-Lil-company-rendering", "exec"), scope)
    scope["verify"]()


if __name__ == "__main__":
    main()
