"""Register the revised trade lesson and dialogue from the next eight Rafael scenes."""

from pathlib import Path

from scripts import register_rafael_early_phrase_wraps_20261118 as parent
from scripts import replay_rafael_next_phrase_wraps_20261118 as replay
from scripts import stage_rafael_next_phrase_wraps_20261118 as stage
from scripts import verify_rafael_next_phrase_wraps_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native, workflow = stage.base, stage.native, parent.workflow
PROFILE = "all-routes-rafael-trade-lesson-and-scenes-v1-20261118"
ROOT = Path("out/rafael_trade_lesson_and_scenes_registered_20261118_v1")
ROM = ROOT / "Translation_DS_Rafael_Trade_Lesson_And_Scenes_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_rafael_trade_lesson_and_scenes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_rafael_trade_lesson_and_scenes_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"

bind = checked_text(parent.bind, {"len(retentions) == 148": "len(retentions) == 118"})
verify = checked_text(parent.verify, {
    "early_proof_and_charlotte_reply_observed": "picador_transition_and_trade_lesson_observed",
    'native_proof["revision_count"] == 12 and native_proof["fresh_page_count"] == 12 and native_proof["retention_count"] == 148':
        'native_proof["revision_count"] == 14 and native_proof["fresh_page_count"] == 14 and native_proof["retention_count"] == 118',
    'for item in r["layouts"]) == 12': 'for item in r["layouts"]) == 14',
    'len(draft["records"]) == 160': 'len(draft["records"]) == 132',
    '{"revision": 12, "retention": 148}': '{"revision": 14, "retention": 118}',
    '{"prose": 12, "retention": 148}': '{"prose": 14, "retention": 118}',
})
publish = parent.main
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
main = checked_text(publish, {
    'len(manifest["batches"]) == 878 and len(manifest["checks"]) == 213':
        'len(manifest["batches"]) == 879 and len(manifest["checks"]) == 214',
    "release_stack_before_rafael_early_phrase_wraps.json": "release_stack_before_rafael_trade_lesson_and_scenes.json",
    "release_stack_with_rafael_early_phrase_wraps.json": "release_stack_with_rafael_trade_lesson_and_scenes.json",
    "verified_papal_states_titis_predecessor": "verified_rafael_early_phrase_wraps_predecessor",
    "rafael_early_phrase_wraps_release": "rafael_trade_lesson_and_scenes_release",
    "registered_rafael_early_phrase_wraps_and_complete_parent_inverse":
        "registered_rafael_trade_lesson_and_scenes_and_complete_parent_inverse",
    "rafael_early_phrase_wraps_pipeline": "rafael_trade_lesson_and_scenes_pipeline",
    "prose_revisions=12, wrap_only_revisions=0, justified_retentions=148":
        "prose_revisions=14, wrap_only_revisions=0, justified_retentions=118",
    "text_display_revisions=12, pagination_fixes=0": "text_display_revisions=14, pagination_fixes=0",
    "initialized_Rafael_early_phrase_excerpts": "initialized_Rafael_trade_lesson_and_scenes_excerpts",
    "Eight Rafael wrap leads and their dialogue exchanges are reviewed, starting with Africa's Proof of Conquest.":
        "Julio's trading lesson and seven other Rafael exchanges have passed the dialogue and wrap review.",
    "rafael_early_phrase_wraps_20261118": "rafael_trade_lesson_and_scenes_20261118",
    "existing_credit=160": "existing_credit=132",
    'candidates += [stage.ROOT / "clean_rebuilt.nds"]':
        '''    earlier = stage.ROOT.with_name("research_v1")
    candidates += [stage.ROOT / "clean_rebuilt.nds", earlier / stage.ROM.name,
                   earlier / replay.ROM.relative_to(stage.ROOT)]'''.lstrip(),
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Rafael trade lesson and story dialogue test candidate

The [local ROM](../../{ROM.as_posix()}) includes the cumulative work through Julio's trading lesson and the seven related Rafael exchanges.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits acceptance. Natural scene activation and hardware remain unverified.
""", encoding="utf-8", newline="\\n")
''',
    doc: '''    DOC.write_text(f"""# Rafael trading lesson and story dialogue

Reviewed 132 turns from eight Rafael exchanges. The ledger records 14 revisions, including the eight flagged wraps, and 118 exact retentions. Julio's advice again explains why Las Palmas and Verde matter and what modest investment in Verde can unlock. His explanation of the bullfight keeps the picador and matador distinct. Cristina's relief still turns abruptly to alarm. The Miracle Bullet Charm scene keeps the hundredth person, and the tavern keeper's dismissal keeps its understated lead-in. [Exact review ledger](../{REVIEW.as_posix()})

All 14 revised pages passed the original renderer and direct visual review. Offline checks bound the 118 retentions, their complete glyphs, and the default Rafael, Castor and company-name substitutions. Ten initialized emulator panels matched, including the picador exchange, Cristina's interrupted relief and the trade lesson with its given-name substitution. The original branch and speaker controls carry forward. Natural scene activation, trading or quest effects, and hardware remain unverified. [Native layout sheets](../{(VERIFY / 'before_after_1.png').as_posix()}) · [Rafael excerpts](../{(VERIFY / 'rafael_live_1.png').as_posix()})

The clean-input patch reconstructs the full candidate byte for byte. All 114 accepted layers and the ASCII right-bound correction carry forward. Six startup holds, 24 protected name getters and 32 targeted tests passed. These 132 records already had credit. The ledger stands at 27,700 with 276 stored shared keys open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\\n")
''',
})
env = parent.env | globals()
for source, label in ((bind, "exact-records"), (verify, "release-gates"), (main, "register")):
    exec(compile(source, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
