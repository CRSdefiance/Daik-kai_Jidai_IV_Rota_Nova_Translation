"""Register the Maria B21–32 pass and the four earlier phrase repairs."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_maria_opening_hodram_wraps_20261122 as parent
from scripts import replay_maria_B21_B32_20261122 as live
from scripts import stage_maria_B21_B32_20261122 as writer
from scripts import verify_maria_B21_B32_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
stage=SimpleNamespace(ROOT=writer.ROOT,ROM=writer.ROM,OUTPUT=writer.MANUSCRIPT,PROOF=writer.PROOF)
PROFILE="all-routes-maria-B21-B32-v1-20261122"
ROOT=parent.ROOT.with_name("maria_B21_B32_registered_20261122")
ROM=ROOT/"Translation_DS_Maria_B21_B32_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_B21_B32_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_maria_B21_B32_registered_20261122.md")
EVIDENCE=writer.ROOT
STARTUP,QA,STARTUP_CAPTURE=EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",EVIDENCE/"startup/capture/capture_report.json"
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
CHECKPOINT=("Revisited 112 Maria records across the ghost-ship, naval pursuit and alliance exchanges. "
            "The pass revises 36, justifies 76 retentions and repairs four earlier wraps.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def observed_names():
    return len(base.load(stage.OUTPUT)["Maria_names_and_roles"])


pages_saved=parent.pages_saved
startup_check=FunctionType(parent.startup_check.__code__,parent.startup_check.__globals__|
    {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE})
source=getsource(parent.verify)
old_live=source[source.index('    assert all(maria_play[tag]'):source.index('    suite=ET.parse(QA)')]
verification=checked_text(source,{
    "stored,draft,rendered,maria_play,hodram_play = map(base.load,(stage.PROOF,stage.OUTPUT,display.PROOF,live.LIVE,hodram.PROOF))":
        "stored,draft,rendered,maria_play = map(base.load,(stage.PROOF,stage.OUTPUT,display.PROOF,live.LIVE))",
    '==maria_play["candidate_sha256"]==hodram_play["candidate_sha256"]':'==maria_play["candidate_sha256"]',
    old_live:'''    assert maria_play["initialized_excerpts"] and not maria_play["natural_story_triggers_claimed"]
    assert maria_play["report_sha256"]==base.digest(live.REPORT)
    assert set(maria_play["observed_ids"])==set(live.PLAY_ORDER)
    assert {row["id"] for row in base.load(writer.review.FOLLOW)["records"]}<=set(maria_play["observed_ids"])
    assert all([len(rendered["menus"])==1,rendered["menus"][0]["count"]==2,len(rendered["lookout_voice_owners"])==7])
    assert sorted(slot for row in rendered["lookout_voice_owners"] for slot in row["slots"])==list(range(8))
    sheets=rendered["sheets"]+maria_play["sheets"]
    assert viewed=={s["path"]:s["sha256"] for s in sheets}
    assert all(base.digest(path)==value for path,value in viewed.items())
''',
    'changed=={"/data/SC1.DK4","/data/SC3.DK4"}':'changed=={"/data/SC3.DK4"}',
    "Verified startup, clean-input patch, both replays, and two changed story archives.":
        "Verified startup, clean-input patch, focused replay and the changed Maria archive.",
    '==len(draft["records"])==171':'==len(draft["records"])==132',
    '{"wording":45,"wrap-only":1,"retention":125}':'{"wording":37,"wrap-only":3,"retention":92}',
    'draft["contextual_records_revisited"]==104 and draft["contextual_decisions_reused"]==67':
        'draft["contextual_records_revisited"]==116 and draft["contextual_decisions_reused"]==16',
    'observed={1:set(hodram_play["observed_ids"]),3:set(maria_play["observed_ids"])}':
        'observed={3:set(maria_play["observed_ids"])}',
    "direct_keys=171":"direct_keys=132",
    "native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),Hodram_replay=str(hodram.PROOF),\n        shared_settings_evidence=settings,full_editorial_goal_complete=False":
        "native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),full_editorial_goal_complete=False",
})
readme=parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                    parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    "len(batches) == 1038 and len(checks) == 373":"len(batches) == 1039 and len(checks) == 374",
    "verified_maria_B18_B20_predecessor=predecessor":"verified_maria_opening_hodram_wraps_predecessor=predecessor",
    "live.LIVE, hodram.PROOF, display.PROOF, args.visual_review":"live.LIVE, display.PROOF, args.visual_review",
    'filename = source.parent.name + "_" + source.name if source in (live.LIVE,hodram.PROOF) else source.name':
        'filename = source.parent.name + "_" + source.name if source==live.LIVE else source.name',
    "native_and_emulator_evidence_sha256=base.digest(live.LIVE), Hodram_emulator_evidence_sha256=base.digest(hodram.PROOF),":
        "native_and_emulator_evidence_sha256=base.digest(live.LIVE),",
    "previously_localized_records=171, contextual_records_revisited=104, contextual_decisions_reused=67":
        "previously_localized_records=132, contextual_records_revisited=116, contextual_decisions_reused=16",
    "prior_records_reviewed=104, contextual_decisions_reused=67, observed_route_panels":
        "prior_records_reviewed=116, contextual_decisions_reused=16, observed_Maria_panels",
    "initialized_Maria_opening_and_Hodram_wraps":"initialized_Maria_B21_B32",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Maria's ghost ship and alliance exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the checked Maria dialogues and four earlier wrap fixes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
})
build=build.replace("maria_opening_hodram_wraps","maria_B21_B32").replace(
    "verified_maria_B21_B32_predecessor","verified_maria_opening_hodram_wraps_predecessor")
build=build.replace("prose_revisions=45","prose_revisions=37").replace("justified_retentions=58","justified_retentions=76").replace(
    "wrap_only_revisions=1","wrap_only_revisions=3")
note=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit=checked_text(parent.commit,{
    '    research = [live.ROM, hodram.ROOT / "Hodram_Wraps_FOCUSED_ONLY.nds"]':'    research = [live.ROM]',
    "Preserve the mixed-route candidate":"Preserve the Maria alliance candidate",
    note:'''    DOC.write_text(f"""# Maria's ghost ship and alliance exchanges

Revisited 112 Maria records in the ghost-ship, pursuit, Lil rescue, Clifford and Kuhn exchanges. The pass revises 36 and justifies 76 retentions. Maria and Lil's repeated use of “helpless” keeps their argument connected, and the changed fleet report avoids a duplicated “fleet” with expanded faction names. The four earlier phrase repairs keep the Proof of Conquest name, the praise and surname, Maria's thanks, and Hodram's warning together. Sixteen surrounding decisions carry forward. [Exact Japanese, previous English and review gates](../{REVIEW.as_posix()})

The native renderer verified {native_count()} changed pages and the alternate-name cases. Offline checks preserved the B29 choice and the seven B32 lookout bodies across all eight slots. Focused emulator playback verified {observed_count()} pages, including the four repairs and the original name substitutions. The original event triggers and hardware remain unvisited. [Native and emulator verification](../{VERIFY.as_posix()})

Startup and 17 regression checks passed. The candidate preserves all 114 accepted layers and the registered ASCII right-bound correction. Its clean-input patch rebuilds the whole ROM exactly. [Registered ROM and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_opening_hodram_wraps","maria_B21_B32")
scope=parent.scope|globals()
for program in (verification,build,commit):
    exec(compile(program,__file__+"::Maria-B21-B32-registered-checkpoint","exec"),scope)


if __name__=="__main__":
    scope["main"]()

