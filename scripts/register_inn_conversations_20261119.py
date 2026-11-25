"""Register the Inn dialogue after the native checks and Istanbul replay."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts.checkpoint_inn_number_width_20261119 import RECEIPT as NUMERAL_LEAD
from scripts import register_hostess_conversations_20261119 as parent
from scripts import replay_inn_conversations_20261119 as game
from scripts import stage_inn_conversations_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
PROFILE = "all-routes-inn-conversations-v1-20261119"
ROOT = Path("out/inn_conversations_registered_20261119_v1")
ROM = ROOT/"Translation_DS_Inn_Conversations_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_inn_conversations_candidate")
VERIFY, PATCH = PACKAGE/"verification", PACKAGE/"translation.xdelta"
REVIEW, RELEASE = VERIFY/"registered_review.json", VERIFY/"registered_release_verification.json"
DOC = Path("docs/editorial_inn_conversations_20261119.md")
STARTUP, QA = game.STARTUP_PROOF, stage.ROOT/"registered_qa.xml"
CHECKPOINT = "The Inn review covers 23 stays, reports and rumor records, with the revised price and duration question verified in Istanbul."
verified = SimpleNamespace(PROOF=stage.PROOF,LIVE=game.PLAYBACK)

verify_source = checked_text(getsource(parent.verify),{
    'staged["visual_layout_cases"] == 273': 'staged["native_layout_cases"] == 1169',
    'playback["hostess_holds"]': 'playback["holds"]',
    'assert observed == {827, 992} and playback["observed_revised_IDs"] == [992]':
        'assert observed == set(game.HOLDS.values()) and playback["observed_revised_IDs"] == [1179]',
    'assert not playback["pending_shared_requests"]': 'assert playback["exact_previous_transition_frames"]',
    'list(range(989, 1020))': 'list(range(1177, 1200))',
    '"observed_in_lisbon"': '"observed_in_istanbul"',
    '    validate_natural_dialogue_batch(review)':'    review["pending_numeral_width"] = {str(NUMERAL_LEAD): base.digest(NUMERAL_LEAD)}\n    validate_natural_dialogue_batch(review)',
})
env = parent.env | globals()
exec(compile(verify_source,__file__+"::verify","exec"),env)

publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
program = checked_text(publish,{
    'len(manifest["batches"]) == 917 and len(manifest["checks"]) == 252':
        'len(manifest["batches"]) == 918 and len(manifest["checks"]) == 253',
    "verified_departure_warnings_predecessor": "verified_hostess_conversations_predecessor",
    "hostess_conversations": "inn_conversations",
    "justified_retentions=27": "justified_retentions=19",
    "previously_localized_records=31": "previously_localized_records=23",
    "ordinary_Lisbon_tavern_and_return=True": "ordinary_Istanbul_stays_and_return=True",
    "Preserve hostess dialogue ROM or reconstruction": "Preserve Inn dialogue ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Inn conversations test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Inn replies and preceding cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Inn conversations

Reviewed 23 records covering stays, market news, crew reports and rumors. The four revisions give the nightly price and the duration question separate lines, and make the innkeeper's price crash and fleet reports sound more conversational. Nineteen retentions preserve the different crew voices and the sequence of each exchange. [Exact review ledger](../{REVIEW.as_posix()})

The original formatter passed 1,169 layout and substitution cases. Nine representative changed pages passed native glyph and visual checks, including the four-row company-name cases. In Istanbul, ordinary inputs verified five full dialogue holds, including the revised quote, the three-night confirmation and the return to town. The three changed rumor turns received offline checks. [Native and gameplay evidence](../{VERIFY.as_posix()})

The original number formatter supplies full-width numerals to the stay confirmation and dated rumors. The current native check identifies all three Inn call sites, reproduces all three stay counts and locates 120 calendar cases with wide digits. The shared number formatter also has other callers. The three Inn sites remain the scope of a future display correction. [Exact numeral lead](../{NUMERAL_LEAD.as_posix()})

Only four reviewed COMMON slots change. The clean-input patch rebuilds the ROM byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed, with two optional older ROM fixture tests skipped. The dialogue ledger still credits 27,700 records, with all 276 open shared references preserved. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
exec(compile(program,__file__+"::register","exec"),env)


if __name__=="__main__":
    env["main"]()
