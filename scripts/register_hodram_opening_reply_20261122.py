"""Register the verified opening exchange and its exact clean-input patch."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

from scripts import register_story_literal_names_20261122 as parent
from scripts import stage_hodram_opening_reply_20261122 as stage
from scripts import verify_hodram_opening_reply_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-hodram-opening-reply-v1-20261122"
ROOT = parent.ROOT.with_name("hodram_opening_reply_registered_20261122")
ROM = ROOT/"Translation_DS_Hodram_Opening_Reply_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_hodram_opening_reply_candidate")
VERIFY, PATCH = PACKAGE/"verification", PACKAGE/"translation.xdelta"
REVIEW, RELEASE = VERIFY/"registered_review.json", VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_opening_reply_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, display.NATIVE
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_passed.xml"
VISUAL = EVIDENCE/"visual_review.json"
live = SimpleNamespace(LIVE=display.LIVE)
CHECKPOINT = "Registered three revisions and twelve justified retentions in the response to Hodram's opening speech."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP,STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(getsource(parent.parent.original),__file__+"::startup","exec"),startup_scope)


def native_count():
    return sum("fresh_native_page" in row for row in base.load(DISPLAY)["records"])


def observed_count():
    return len(base.load(live.LIVE)["observed"])


def verify(registry,previous,viewed):
    stored, frames, native_report, visual = map(base.load,(stage.PROOF,live.LIVE,DISPLAY,VISUAL))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == frames["candidate_sha256"] == native_report["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == frames["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.DRAFT)
    assert frames["actual_original_opening"] and frames["ordinary_controls_only"] and frames["retained_Charles_surname_panel"]
    assert native_report["offline_native_only"] and native_report["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert frames["exact_changed_body_masks"] == native_count() == 3 and observed_count() == 9
    assert {r["id"] for r in frames["observed"] if r.get("mask_exact")} == stage.CHANGED
    assert visual["reviewed_candidate_sha256"] == candidate
    assert viewed == visual["sheets"] == native_report["sheets"] | frames["sheets"]
    assert all(base.digest(p)==h for evidence in (viewed,frames["evidence"]) for p,h in evidence.items())
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]

    clean, old, target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    before, after = map(native.files,(old,target))
    path = stage.PATH
    assert before.keys() == after.keys() and {p for p in before if before[p]!=after[p]} == {path}
    a,b = [native.IlnkContainer.parse(f[path]).blocks for f in (before,after)]
    changed_blocks = [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]
    assert changed_blocks == stored["changed_blocks"][path] == [stage.BLOCK]
    assert [native.digest(bank[stage.BLOCK]) for bank in (a,b)] == [stored["before_block_sha256"],stored["after_block_sha256"]]
    assert native.digest(after[ARM]) == previous["target_ARM9_sha256"] == stored["unchanged_ARM9_sha256"]
    assert native.digest(after[COMMON]) == previous["target_COMMON_sha256"]
    target.replace_file(path,before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard == guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean),after)
    assert checks == stored["source25"] and checks["total_exact_source_bound_relocated_leading25_count"]==7
    startup_scope["startup_proof"](previous,candidate,after[ARM])

    refs = {r["id"]:r for r in native_report["records"]}
    observed = {r["id"]:r for r in frames["observed"] if r.get("mask_exact")}
    records = []
    for row in stored["records"]:
        ident = row["id"]
        proof = refs.pop(ident)
        assert (ident in observed) == (ident in stage.CHANGED) == ("fresh_native_page" in proof)
        records.append(row | dict(localization_note=row["editorial_finding"],registered_reference=proof["reference"],
            review=row["review"] | {"formatting":True}, observed_changed_page=observed.get(ident),
            display_proof={k:v for k,v in proof.items() if k not in ("id","reference")}))
    assert not refs and len(records) == 15 and all(all(r["review"].values()) for r in records)
    result = dict(candidate_sha256=candidate,records=records,checked_story_format_guard=checks,
        visual_review=viewed,ordinary_opening=frames,native_display_sha256=base.digest(DISPLAY),
        native_cases=native_count(),hardware=False,full_editorial_goal_complete=False,
        prior_records_reviewed=15,wording_revisions=2,wrap_only_revisions=1,justified_retentions=12,
        historical_source_credit=dict(by_census_id={},direct_keys=0))
    return stored,result,{p:native.digest(after[p]) for p in (ARM,COMMON,path)}


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1050 and len(checks) == 385": "len(batches) == 1051 and len(checks) == 386",
    "source_bound_story_literal_names=stored['protected_story_frames']":
        "source_bound_hodram_reply_block={stage.PATH:stored['after_block_sha256']}",
    "changed_component_hashes={stage.native.ARM:archives[stage.native.ARM]}":
        "changed_component_hashes={stage.PATH:archives[stage.PATH]}",
    "changed_internal_files=[stage.native.ARM]": "changed_internal_files=[stage.PATH]",
    "previously_localized_records=0, contextual_records_revisited=0":
        "previously_localized_records=15, contextual_records_revisited=15",
    "prior_records_reviewed=0": "prior_records_reviewed=15",
    "prose_revisions=0": "prose_revisions=2",
    "wrap_only_revisions=0": "wrap_only_revisions=1",
    "justified_retentions=0": "justified_retentions=12",
    "text_display_revisions=1, story_name_substitution_corrections=1": "text_display_revisions=1",
    "ordinary_Hodram_opening=True, focused_system_dialogue=True":
        "ordinary_Hodram_opening=True, all_three_changed_records_observed=True",
    "pagination_fixes=1": "pagination_fixes=0",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram opening reply testing candidate

The [testing ROM](../../{ROM.as_posix()}) revises three lines in the response to Hodram's speech. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("story_literal_names","hodram_opening_reply").replace(
    "verified_captain_name_delete_predecessor","verified_story_literal_names_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit,{
    "Preserve the story name candidate, predecessor, staged and focused ROMs":
        "Preserve the Hodram opening reply candidate, predecessor and staged ROM",
    "research = [played.FOCUSED_ROM]": "research = []",
    old_doc:'''    DOC.write_text(f"""# Hodram's opening reply

The crew's reaction to Hodram's speech, his abrupt change of subject and the officers' replies now have fifteen contextual decisions. Twelve lines retain their existing wording. His reply keeps its comparison together and gives “Anyway...” its own beat. The next lines explain how the state sets naval rewards and restore the urgency of checking the Hanseatic report. [Exact Japanese, installed text and decisions](../{REVIEW.as_posix()})

All three revised pages matched the native glyph planes in a normal New Game replay, which also showed the surrounding replies in order. The replay retained the complete custom surname in Charles's preceding line. Startup and 17 focused tests passed. The clean-input patch reconstructs the candidate byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("story_literal_names","hodram_opening_reply")
scope = parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register","exec"),scope)


if __name__ == "__main__":
    scope["main"]()
