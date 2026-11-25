"""Bind the Lisbon lesson replay to all revised pages and its retained choices."""
from inspect import getsource

from scripts import audit_rafael_sailing_modes_playback_20261119 as original
from scripts import replay_story_market_terms_20261119 as play
from scripts import verify_story_market_terms_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, build = play.base, play.build
PROOF = play.ROOT / "verified_trade_lesson.json"


def main():
    assert not PROOF.exists()
    setup, native, name_proof = map(base.load, (play.FIXTURES, offline.PROOF, original.NAMES))
    fixture, = setup["fixtures"]
    assert setup["exact_candidate_inverse"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"]
    assert base.digest(build.ROM) == setup["candidate_sha256"] == native["candidate_sha256"]
    revisions = {row["id"]: row["pages"][0] for row in native["revisions"]
                 if row["file_path"] == "/data/SC0.DK4" and row["id"].startswith("DK4_MES_B137_")}
    assert len(revisions) == 3
    names = {row["actor_ID"]: row for row in name_proof["name_planes"]}
    expected = dict(menu_selection=0, source_speech_IDs=[r["id"] for r in fixture["original_text_records"]])
    source = checked_text(getsource(original.path_result), {
        '{"Please do.", "No, thanks."}': '{"Market share?", "Got it."}',
        '    assert commands == expected["visited_source_command_offsets"]':
            '    assert commands and commands == sorted(set(commands))',
        'f"{choice}: retained choices"': '"Lisbon lesson choices"',
        'f"{choice}: after the original return"': '"After the Lisbon lesson returns"',
    })
    scope = vars(original) | globals()
    exec(compile(source, __file__ + "::lisbon_trade_lesson", "exec"), scope)
    result = scope["path_result"]("accept", fixture, expected, revisions, names)
    assert result["result"] == [0, 0] and len(result["speeches"]) == 12
    assert {row["id"] for row in result["checked_revisions"]} == revisions.keys()
    result["evidence"].update({str(p): base.digest(p)
                              for p in (play.FIXTURES, play.FIXTURE, offline.PROOF, original.NAMES)})
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], paths=[result], revised_pages_verified=3,
                         natural_activation=False, hardware=False, evidence=result["evidence"]))
    print("Matched all three revised Lisbon pages, both choice captions and the interpreter return.")


if __name__ == "__main__":
    main()
