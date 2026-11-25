"""Register Maria's tutorial and coin-game follow-up with an exact clean-input patch."""

from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_maria_B21_B32_20261122 as template
from scripts import register_maria_B51_B70_20261122 as parent
from scripts import replay_maria_tutorial_followup_20261122 as live
from scripts import stage_maria_tutorial_followup_20261122 as writer
from scripts import verify_maria_tutorial_followup_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
stage=SimpleNamespace(ROOT=writer.ROOT,ROM=writer.ROM,OUTPUT=writer.MANUSCRIPT,PROOF=writer.PROOF)
PROFILE="all-routes-maria-tutorial-followup-v1-20261122"
ROOT=parent.ROOT.with_name("maria_tutorial_followup_registered_20261122")
ROM=ROOT/"Translation_DS_Maria_Tutorial_Followup_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_tutorial_followup_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_maria_tutorial_followup_registered_20261122.md")
EVIDENCE=writer.ROOT
STARTUP,QA,STARTUP_CAPTURE=EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",EVIDENCE/"startup/capture/capture_report.json"
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
CHECKPOINT=("Closed all 87 later Maria evidence bindings. Six improvements in Cesare, Fernando and Manuel's exchanges "
            "include a one-page trade example and a clearer Lumber Room instruction.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def observed_names():
    seen=set(base.load(live.LIVE)["observed_ids"])
    return len({r["speaker"] for r in base.load(stage.OUTPUT)["records"] if r["id"] in seen})


def pages_saved():
    return base.load(display.PROOF)["reclaimed_previous_native_pages"]


startup_check=FunctionType(parent.startup_check.__code__,parent.startup_check.__globals__|
    {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE})
prior_verify=template.verification
old_sheets=prior_verify[prior_verify.index('    assert {row["id"]'):prior_verify.index('    assert viewed==')]
verification=checked_text(prior_verify,{
    old_sheets:'''    assert rendered["revised_speech_pages"]==6 and rendered["alternate_name_pages"]==0
    assert rendered["reclaimed_previous_native_pages"]==1
    assert {row["id"] for row in draft["records"]}==set(maria_play["observed_ids"])
    sheets=rendered["sheets"]+maria_play["sheets"]
''',
    '==len(draft["records"])==132':'==len(draft["records"])==12',
    'draft["findings"]=={"wording":37,"wrap-only":3,"retention":92}':
        'draft["findings"]=={"wording":6,"retention":6}',
    'draft["contextual_records_revisited"]==116 and draft["contextual_decisions_reused"]==16':
        'draft["contextual_records_revisited"]==12 and draft["contextual_decisions_reused"]==3827',
    '    assert not references\n    draft.update':'''    assert not references
    draft["review_gates"]=["source","context","localization","naturalness","formatting"]
    validate_natural_dialogue_batch(draft)
    draft.update''',
    'direct_keys=132':'direct_keys=12',
    'native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),full_editorial_goal_complete=False':
        'native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),full_editorial_goal_complete=False',
})
old_readme=template.build[template.build.index('    (PACKAGE / "README.md").write_text'):template.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(template.build,{
    'len(batches) == 1039 and len(checks) == 374':'len(batches) == 1042 and len(checks) == 377',
    'verified_maria_opening_hodram_wraps_predecessor=predecessor':'verified_maria_B51_B70_predecessor=predecessor',
    'previously_localized_records=132, contextual_records_revisited=116, contextual_decisions_reused=16':
        'previously_localized_records=12, contextual_records_revisited=12, contextual_decisions_reused=3827',
    'prose_revisions=37':'prose_revisions=6',
    'wrap_only_revisions=3':'wrap_only_revisions=0',
    'justified_retentions=76':'justified_retentions=6',
    'prior_records_reviewed=116, contextual_decisions_reused=16, observed_Maria_panels=observed_count()':
        'prior_records_reviewed=12, contextual_decisions_reused=3827, observed_Maria_panels=observed_count()',
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Maria's ship lessons and Fernando's wager

The [testing ROM](../../{ROM.as_posix()}) includes the refinements to Cesare's advice, Fernando's wager and Manuel's refit explanation. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("maria_B21_B32","maria_tutorial_followup").replace("initialized_Maria_B21_B32","initialized_Maria_tutorial_followup")
note=template.commit[template.commit.index("    DOC.write_text"):template.commit.index("    prefix =")]
commit=checked_text(template.commit,{
    "Preserve the Maria alliance candidate":"Preserve the Maria tutorial candidate",
    note:'''    DOC.write_text(f"""# Maria's ship lessons and Fernando's wager

Six revisions make Cesare's ship-buying example easier to read, give Fernando back his personal boast and make clear that shipwrights work in the Lumber Room. Six neighboring lines keep their wording for individual reasons. The wider Maria comparison restored the exact registered evidence for all 87 flagged records. [Source, prior text, and registered review](../{REVIEW.as_posix()})

Native and visual checks cover all six revised pages and verify that Cesare's one percent example now fits on a single page. Initialized Maria playback verified {observed_count()} pages and the original host continuation after the excerpts. The original event triggers and hardware remain unvisited. [Native and emulator results](../{VERIFY.as_posix()})

The staged ROM's own startup and 17 focused tests passed. The build carries all 114 accepted layers, the ASCII right-bound correction and the Hangzhou briefing. The patch reconstructs the testing ROM byte for byte. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_B21_B32","maria_tutorial_followup")
scope=template.scope|globals()
for source in (verification,build,commit):
    exec(compile(source,__file__+"::Maria-tutorial-followup-registered","exec"),scope)

if __name__=="__main__":
    scope["main"]()

