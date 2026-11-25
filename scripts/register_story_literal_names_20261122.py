"""Register the verified story name substitution correction."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree as ET

from ndspy.code import MainCodeFile

from scripts import register_captain_name_delete_20261122 as parent
from scripts import replay_story_literal_names_20261122 as played
from scripts import stage_story_literal_names_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON = parent.ARM, parent.COMMON
PROFILE = "all-routes-story-literal-names-v1-20261122"
ROOT = parent.ROOT.with_name("story_literal_names_registered_20261122")
ROM = ROOT / "Translation_DS_Story_Literal_Names_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_story_literal_names_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_story_literal_names_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, parent.DISPLAY
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE/"own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE/"qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
live = SimpleNamespace(LIVE=EVIDENCE / "verified_gameplay.json")
CHECKPOINT = "Registered the correction for custom names being expanded twice in story dialogue."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard

startup_source = checked_text(parent.startup_source, {
    "source_bound_captain_name_delete_only=True": "source_bound_story_literal_names_only=True",
})
startup_scope = parent.original.__globals__ | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(startup_source, __file__+"::story-name-startup", "exec"), startup_scope)


def native_count():
    proof = base.load(stage.PROOF)
    return len(proof["all_native_story_cases"]) + len(proof["unrelated_direct_cases"])


def observed_count():
    return len(base.load(live.LIVE)["ordinary"]["fixed_story_holds"])


def verify(registry, previous, viewed):
    stored, live_report, defect, visual = map(base.load,(stage.PROOF,live.LIVE,DISPLAY,VISUAL))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == live_report["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == live_report["predecessor_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["story_and_common_file_bytes_exact"]
    assert defect["observed_in_ordinary_opening"]
    assert visual["reviewed_candidate_sha256"] == candidate
    assert viewed == visual["sheets"] == live_report["sheets"]
    assert all(base.digest(p)==h for entries in (viewed,live_report["evidence"]) for p,h in entries.items())
    assert live_report["ordinary"]["actual_original_opening"]
    assert live_report["ordinary"]["formerly_extra_page_removed"]
    assert live_report["focused_system"]["system_body_mask_exact"]
    assert live_report["focused_system"]["fixture"]["fixture_sha256"] == base.digest(played.FOCUSED_ROM)
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]
    assert native_count() == 36
    clean, old, target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    before, after = map(native.files,(old,target))
    assert before.keys() == after.keys() and {p for p in before if before[p]!=after[p]} == {ARM}
    assert native.digest(after[ARM]) == stored["target_ARM9_sha256"]
    assert native.digest(after[COMMON]) == previous["target_COMMON_sha256"]
    original, current = map(lambda data:MainCodeFile(data,stage.patch.BASE),(before[ARM],after[ARM]))
    helpers = stored["protected_story_frames"]
    tail = b"".join(bytes.fromhex(row["helper_hex"]) for row in helpers["hooks"])
    assert bytes(current.sections[-1].data) == bytes(original.sections[-1].data)+tail
    current.sections[-1].data = bytearray(original.sections[-1].data)
    for site in stage.patch.FRAMES:
        current.sections[0].data[site:site+4] = original.sections[0].data[site:site+4]
    assert bytes(current.save()) == before[ARM]
    target.replace_file(ARM,before[ARM])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    checks = bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean),after)
    assert checks["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous,candidate,after[ARM])
    result = dict(candidate_sha256=candidate, records=[], checked_story_format_guard=checks, stored_helpers=helpers,
        visual_review=viewed, ordinary_opening=live_report["ordinary"], focused_system=live_report["focused_system"],
        previous_finding=dict(path=str(DISPLAY),sha256=base.digest(DISPLAY)), retained_line=defect["exact_record"],
        retained_neighbors=defect["nameplate_and_neighbor_refs"], localization_retention_reason=
        "Charles addresses his admiral by surname in Japanese and credits his speech for stirring his eagerness for battle. "
        "The existing English keeps that address, emotion and reply sequence. Only the rendering is corrected.",
        changed_text_records=0, new_editorial_credit=0,native_cases=native_count(),hardware=False,
        historical_source_credit=dict(by_census_id={},direct_keys=0),full_editorial_goal_complete=False)
    return stored,result,{ARM:native.digest(after[ARM]),COMMON:native.digest(after[COMMON])}


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1049 and len(checks) == 384": "len(batches) == 1050 and len(checks) == 385",
    "original_name_fields_and_limits_preserved=True": "original_name_fields_limits_and_controls_preserved=True",
    "stored['source_bound_helper']": "stored['protected_story_frames']",
    "text_display_revisions=0, editor_control_corrections=1": "text_display_revisions=1, story_name_substitution_corrections=1",
    "two_page_count_explanations=0, pagination_fixes=0": "two_page_count_explanations=0, pagination_fixes=1",
    "ordinary_Hodram_name_editor=True, unresolved_surname_expansion=True": "ordinary_Hodram_opening=True, focused_system_dialogue=True",
    "native_deletion_cases=native_count()": "native_formatting_cases=native_count()",
    "observed_Hodram_name_editor_holds": "observed_Hodram_story_holds",
    "choice_label_revisions=0, pagination_fixes=0)": "choice_label_revisions=0, pagination_fixes=1)",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Story name testing candidate

The [testing ROM](../../{ROM.as_posix()}) keeps accepted custom names intact in story dialogue. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("captain_name_delete","story_literal_names").replace(
    "verified_ceuta_supply_alerts_predecessor","verified_captain_name_delete_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit,{
    "Preserve the captain-name deletion candidate, predecessor and staged ROM":
        "Preserve the story name candidate, predecessor, staged and focused ROMs",
    "    research = []": "    research = [played.FOCUSED_ROM]",
    old_doc:'''    DOC.write_text(f"""# Custom names in story dialogue

An ordinary Hodram New Game reproduced the surname corruption in Charles's opening dialogue, SC1 B42 R0113. The previous display treated letter pairs inside the surname as substitutions and added a page. Matching controls on the candidate display the full surname once, finish the original speech on a single page, and advance to Hodram's reply. The Japanese address, English text, formatting controls and accepted names stay intact. [Exact record and comparison](../{REVIEW.as_posix()})

The correction is scoped to the three story call frames that already expanded the dialogue. An original system notification was exercised through a focused fixture. Native checks covered all three story modes and unrelated direct callers. The fixture supplies the original command to the running game without meeting its normal event conditions. Startup and 17 tests passed. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("captain_name_delete","story_literal_names")
scope = parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register", "exec"),scope)


if __name__ == "__main__":
    scope["main"]()
