"""Register the Maria follow-up and the ordinary Hangzhou briefing as one cumulative candidate."""

from inspect import getsource
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_hangzhou_briefing_followup_20261122 as town
from scripts import register_maria_B21_B32_20261122 as parent
from scripts import replay_maria_hangzhou_followup_20261122 as live
from scripts import stage_maria_hangzhou_followup_20261122 as writer
from scripts import verify_maria_hangzhou_followup_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
stage=SimpleNamespace(ROOT=writer.ROOT,ROM=writer.ROM,OUTPUT=writer.MANUSCRIPT,PROOF=writer.PROOF)
PROFILE="all-routes-maria-hangzhou-followup-v1-20261122"
ROOT=parent.ROOT.with_name("maria_hangzhou_followup_registered_20261122")
ROM=ROOT/"Translation_DS_Maria_Hangzhou_Followup_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_hangzhou_followup_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_maria_hangzhou_followup_registered_20261122.md")
EVIDENCE=writer.ROOT
STARTUP,QA,STARTUP_CAPTURE=EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",EVIDENCE/"startup/capture/capture_report.json"
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
CHECKPOINT=("Closed 17 changed Maria records across nine story blocks and carried forward 343 exact earlier decisions. "
            "Two earlier name-driven wraps and the Hangzhou Luxury Shop briefing are included.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]+1


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def observed_names():
    playback=base.load(live.LIVE)
    seen=set(playback["observed_ids"])
    return len({r["speaker"] for r in base.load(stage.OUTPUT)["records"] if r["id"] in seen})


def pages_saved():
    return 0


startup_check=FunctionType(parent.startup_check.__code__,parent.startup_check.__globals__|
    {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE})
previous_verify=parent.verification
old_sheets=previous_verify[previous_verify.index('    assert {row["id"]'):previous_verify.index('    assert viewed==')]
verification=checked_text(previous_verify,{
    old_sheets:'''    town_play=base.load(town.PROOF)
    assert candidate==town_play["candidate_sha256"]
    assert town_play["ordinary_facility_navigation"] and not town_play["hardware"]
    assert town_play["report_sha256"]==base.digest(town.REPORT)
    assert town_play["native_report_sha256"]==base.digest(display.PROOF)
    assert town_play["changed_record"]["message_ID"]==writer.shared.KEY
    assert town_play["changed_record"]["observed_lines"]==rendered["briefing"]["lines"]
    assert len(town_play["changed_record"]["exact_body"])==4
    assert len(town_play["panels"])==6 and len(town_play["observed_unchanged_menu_returns"])==3
    assert {row["id"] for row in draft["records"] if row["decision"]=="revision"}<=set(maria_play["observed_ids"])
    sheets=rendered["sheets"]+maria_play["sheets"]+town_play["sheets"]
''',
    'changed=={"/data/SC3.DK4"}':'changed=={writer.ARCHIVE,writer.COMMON}',
    '    for path in sorted(changed):':'''    for path in (writer.ARCHIVE,):''',
    '    assert bytes(after.rom.save())==parent.ROM.read_bytes()':'''    briefing=stored["briefing"]
    assert briefing["fixed_slot_and_complete_COMMON_inverse"] and briefing["original_directory_and_table_exact"]
    assert briefing["parent_shared_sha256"]==previous["target_COMMON_sha256"]==native.digest(first[writer.COMMON])
    assert briefing["target_shared_sha256"]==native.digest(final[writer.COMMON])
    a,b=(native.IlnkContainer.parse(parts[writer.COMMON]) for parts in (first,final))
    allocation=briefing["allocation"]
    n,lo,hi=(allocation[k] for k in ("block","start","end"))
    old,new=(bytes.fromhex(allocation[k]) for k in ("before","after"))
    assert a.blocks[n][lo:hi]==old and b.blocks[n][lo:hi]==new
    assert b.blocks[n]==a.blocks[n][:lo]+new+a.blocks[n][hi:]
    b.blocks[n]=a.blocks[n]
    assert b.to_bytes()==first[writer.COMMON]
    after.replace_file(writer.COMMON,first[writer.COMMON])
    archive_hashes[writer.COMMON]=briefing["target_shared_sha256"]
    assert bytes(after.rom.save())==parent.ROM.read_bytes()''',
    '    assert native.digest(final["/COMMON/MESFILE.DK4"])==previous["target_COMMON_sha256"]\n':'',
    '==len(draft["records"])==132':'==len(draft["records"])==19',
    'draft["findings"]=={"wording":37,"wrap-only":3,"retention":92}':
        'draft["findings"]=={"wording":8,"wrap-only":1,"retention":10}',
    'draft["contextual_records_revisited"]==116 and draft["contextual_decisions_reused"]==16':
        'draft["contextual_records_revisited"]==19 and draft["contextual_decisions_reused"]==343',
    '    assert not references\n    draft.update':'''    assert not references
    row=briefing["record"]
    assert row["staged_hex"]==rendered["briefing"]["stored_hex"] and row["decision"]=="revision"
    row["registered_reference"]=row["staged_reference"]|dict(candidate_sha256=candidate,
        archive_sha256=archive_hashes[writer.COMMON],exact_stored_hex=row["staged_hex"])
    row["observed_in_ordinary_town_play"]=True
    row["review"]["formatting"]=True
    draft["records"].append(row)
    draft["contextual_records_revisited"]+=1
    draft["findings"]["wording"]+=1
    draft["review_gates"]=["source","context","localization","naturalness","formatting"]
    validate_natural_dialogue_batch(draft)
    draft.update''',
    'direct_keys=132':'direct_keys=20',
    'native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),full_editorial_goal_complete=False':
        'native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),ordinary_Hangzhou_evidence=str(town.PROOF),full_editorial_goal_complete=False',
})
old_readme=parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    'len(batches) == 1039 and len(checks) == 374':'len(batches) == 1040 and len(checks) == 375',
    'verified_maria_opening_hodram_wraps_predecessor=predecessor':'verified_maria_B21_B32_predecessor=predecessor',
    'live.LIVE, display.PROOF, args.visual_review':'live.LIVE, town.PROOF, display.PROOF, args.visual_review',
    'native_and_emulator_evidence_sha256=base.digest(live.LIVE),':
        'native_and_emulator_evidence_sha256=base.digest(live.LIVE), ordinary_Hangzhou_evidence_sha256=base.digest(town.PROOF),',
    '    release = previous | dict(profile=PROFILE,':'    release = previous | dict(profile=PROFILE, target_COMMON_sha256=archives[writer.COMMON],',
    'changed_components=1, repository_tests=17,':'changed_components=2, repository_tests=17,',
    'previously_localized_records=132, contextual_records_revisited=116, contextual_decisions_reused=16':
        'previously_localized_records=20, contextual_records_revisited=20, contextual_decisions_reused=343',
    'prose_revisions=37':'prose_revisions=9',
    'wrap_only_revisions=3':'wrap_only_revisions=1',
    'justified_retentions=76':'justified_retentions=10',
    'initialized_Maria_B21_B32=True,':'initialized_Maria_dialogue=True, ordinary_Hangzhou=True,',
    'prior_records_reviewed=116, contextual_decisions_reused=16, observed_Maria_panels=observed_count()':
        'prior_records_reviewed=20, contextual_decisions_reused=343, observed_Maria_panels=observed_count(), observed_Hangzhou_holds=6',
    'registered_release_verification=str(RELEASE),\n            **':
        'registered_release_verification=str(RELEASE), COMMON_sha256=archives[writer.COMMON],\n            **',
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Maria follow-up and Hangzhou briefing

The [testing ROM](../../{ROM.as_posix()}) includes the revised Maria exchanges and the Hangzhou Luxury Shop briefing. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("maria_B21_B32","maria_hangzhou_followup").replace(
    "verified_maria_hangzhou_followup_predecessor","verified_maria_B21_B32_predecessor")
note=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit=checked_text(parent.commit,{
    "Preserve the Maria alliance candidate":"Preserve the Maria and Hangzhou candidate",
    note:'''    DOC.write_text(f"""# Maria follow-up and Hangzhou briefing

Reviewed 17 Maria lines whose installed text differed from prior proof. The pass revised six, rewrapped Lil's retort and individually justified ten retentions. Another 343 decisions carry forward on exact stored bytes. Two earlier name-driven wraps now have fuller opening rows. The Hangzhou Luxury Shop briefing keeps each of its four thoughts on its own line. [Exact source, current references and five review gates](../{REVIEW.as_posix()})

Native review verified nine story pages, six alternate name layouts and the four-line briefing. Focused Maria playback verified {observed_count()} pages and two return holds. Ordinary Hangzhou navigation verified all four briefing rows, the Shopkeeper label, five neighboring holds and three menu returns. Original story triggers, alternate shared callers and hardware remain unvisited. [Display and emulator proof](../{VERIFY.as_posix()})

The byte-exact clean-input patch, startup and 17 focused regression tests passed. An optional broad test invocation was stopped after host native-test exceptions. All 114 accepted layers and the registered ASCII right-bound correction carry forward. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_B21_B32","maria_hangzhou_followup")
scope=parent.scope|globals()
for source in (verification,build,commit):
    exec(compile(source,__file__+"::registered-story-and-town","exec"),scope)

if __name__=="__main__":
    scope["main"]()

