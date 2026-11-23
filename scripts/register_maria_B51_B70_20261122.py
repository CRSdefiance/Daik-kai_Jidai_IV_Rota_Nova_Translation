"""Register the Maria B51–70 contextual follow-up and exact clean-input patch."""

from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_maria_B21_B32_20261122 as template
from scripts import register_maria_hangzhou_followup_20261122 as parent
from scripts import replay_maria_B51_B70_20261122 as live
from scripts import stage_maria_B51_B70_20261122 as writer
from scripts import verify_maria_B51_B70_20261122 as display
from scripts import verify_maria_B51_B70_retentions_20261122 as retention
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
stage=SimpleNamespace(ROOT=writer.ROOT,ROM=writer.ROM,OUTPUT=writer.MANUSCRIPT,PROOF=writer.PROOF)
PROFILE="all-routes-maria-B51-B70-v1-20261122"
ROOT=parent.ROOT.with_name("maria_B51_B70_registered_20261122")
ROM=ROOT/"Translation_DS_Maria_B51_B70_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_B51_B70_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_maria_B51_B70_registered_20261122.md")
EVIDENCE=writer.ROOT
STARTUP,QA,STARTUP_CAPTURE=EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",EVIDENCE/"startup/capture/capture_report.json"
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
CHECKPOINT=("Reviewed 18 later text variants across the Proofs of Conquest and Maria's companion exchanges. "
            "Six wording revisions, two wrap-only fixes and ten retentions pass. Another 595 decisions carry forward.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def observed_names():
    seen=set(base.load(live.LIVE)["observed_ids"])
    return len({r["speaker"] for r in base.load(stage.OUTPUT)["records"] if r["id"] in seen})


def pages_saved():
    return 0


startup_check=FunctionType(parent.startup_check.__code__,parent.startup_check.__globals__|
    {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE})
prior_verify=template.verification
old_sheets=prior_verify[prior_verify.index('    assert {row["id"]'):prior_verify.index('    assert viewed==')]
verification=checked_text(prior_verify,{
    old_sheets:'''    retained=base.load(retention.PROOF)
    assert retained["candidate_sha256"]==candidate and retained["source_proof_sha256"]==base.digest(display.PROOF)
    retained_rows={r["id"]:r for r in retained["records"]}
    assert len(retained_rows)==10
    assert rendered["revised_speech_pages"]==8 and rendered["alternate_name_pages"]==0
    body_matches={r["id"]:r["body_hex"] for r in rendered["records"] if not r["layouts"]}
    assert body_matches=={i:r["body_hex"] for i,r in retained_rows.items()}
    assert {row["id"] for row in draft["records"] if row["decision"]=="revision"}-set(maria_play["observed_ids"])=={"DK4_MES_B54_R0074"}
    variants={r["id"]:r for r in rendered["records"] if r["layouts"]}
    assert variants["DK4_MES_B54_R0074"]["body_hex"]==variants["DK4_MES_B53_R0069"]["body_hex"]
    sheets=rendered["sheets"]+retained["sheets"]+maria_play["sheets"]
''',
    '==len(draft["records"])==132':'==len(draft["records"])==18',
    'draft["findings"]=={"wording":37,"wrap-only":3,"retention":92}':
        'draft["findings"]=={"wording":6,"wrap-only":2,"retention":10}',
    'draft["contextual_records_revisited"]==116 and draft["contextual_decisions_reused"]==16':
        'draft["contextual_records_revisited"]==18 and draft["contextual_decisions_reused"]==595',
    '        row["native_formatting_evidence"]=context':
        '        row["native_formatting_evidence"]=context|{"retained_preview":retained_rows.get(ident)}',
    '    assert not references\n    draft.update':'''    assert not references
    draft["review_gates"]=["source","context","localization","naturalness","formatting"]
    validate_natural_dialogue_batch(draft)
    draft.update''',
    'direct_keys=132':'direct_keys=18',
    'native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),full_editorial_goal_complete=False':
        'native_preview_evidence=str(display.PROOF),retention_preview_evidence=str(retention.PROOF),Maria_replay=str(live.LIVE),full_editorial_goal_complete=False',
})
old_readme=template.build[template.build.index('    (PACKAGE / "README.md").write_text'):template.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(template.build,{
    'len(batches) == 1039 and len(checks) == 374':'len(batches) == 1041 and len(checks) == 376',
    'verified_maria_opening_hodram_wraps_predecessor=predecessor':'verified_maria_hangzhou_followup_predecessor=predecessor',
    'live.LIVE, display.PROOF, args.visual_review':'live.LIVE, display.PROOF, retention.PROOF, args.visual_review',
    'previously_localized_records=132, contextual_records_revisited=116, contextual_decisions_reused=16':
        'previously_localized_records=18, contextual_records_revisited=18, contextual_decisions_reused=595',
    'prose_revisions=37':'prose_revisions=6',
    'wrap_only_revisions=3':'wrap_only_revisions=2',
    'justified_retentions=76':'justified_retentions=10',
    'prior_records_reviewed=116, contextual_decisions_reused=16, observed_Maria_panels=observed_count()':
        'prior_records_reviewed=18, contextual_decisions_reused=595, observed_Maria_panels=observed_count()',
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Maria B51–70 follow-up

The [testing ROM](../../{ROM.as_posix()}) includes the dialogue and wrap refinements. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("maria_B21_B32","maria_B51_B70").replace("initialized_Maria_B21_B32","initialized_Maria_B51_B70")
note=template.commit[template.commit.index("    DOC.write_text"):template.commit.index("    prefix =")]
commit=checked_text(template.commit,{
    "Preserve the Maria alliance candidate":"Preserve the Maria B51–70 candidate",
    '    earlier = [stage.ROM]':'''    earlier = [stage.ROM, *(stage.ROOT.with_name(f"B51_B70_staged_v{i}")/stage.ROM.name for i in (1,2))]''',
    note:'''    DOC.write_text(f"""# Maria B51–70 follow-up

Revisited 18 installed text variants from clean Japanese. The review restores Xien's deliberately abridged list and Janus's separate ship-handling and repair skills. It keeps the doubt about the relics on its own line in both branches, records six wording changes and explains ten retentions. Another 595 earlier decisions carry forward by exact saved bytes. [Source, prior text, and registered review](../{REVIEW.as_posix()})

Native rendering and visual review cover the eight revised pages and all ten retained variants. Initialized Maria playback verified {observed_count()} pages and observed the original host continuation after the excerpts. The matching alternate Proofs panel was checked offline. The original events and hardware remain unvisited. [Native and emulator results](../{VERIFY.as_posix()})

The staged ROM's own startup and 17 focused tests passed. The build carries all 114 accepted layers, the ASCII right-bound correction and the Hangzhou briefing. The patch reconstructs the testing ROM byte for byte. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_B21_B32","maria_B51_B70")
scope=template.scope|globals()
for source in (verification,build,commit):
    exec(compile(source,__file__+"::Maria-B51-B70-registered","exec"),scope)

if __name__=="__main__":
    scope["main"]()

