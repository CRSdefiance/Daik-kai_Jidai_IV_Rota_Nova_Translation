"""Register the two wording-preserving regional rumor wraps."""

from types import SimpleNamespace
from xml.etree import ElementTree as ET

from scripts import register_square_shop_names_20261122 as parent
from scripts import stage_square_rumor_wraps_20261122 as stage
from scripts import verify_square_rumor_wraps_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow = parent.base,parent.native,parent.workflow
ARM,COMMON = stage.ARM,stage.COMMON
PROFILE = "all-routes-square-rumor-wraps-v1-20261122"
ROOT = parent.ROOT.with_name("square_rumor_wraps_registered_20261122")
ROM = ROOT/"Translation_DS_Square_Rumor_Wraps_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_square_rumor_wraps_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_square_rumor_wraps_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP,STARTUP_CAPTURE,QA = EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_passed.xml"
VISUAL = EVIDENCE/"visual_review.json"
live = SimpleNamespace(LIVE=display.LIVE)
CHECKPOINT = "Registered wording-preserving wrap corrections for two Square rumors."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_source = checked_text(parent.startup_source,{"square_caption_dispatch_only=True":"square_rumor_layout_and_COMMON_offsets_only=True"})
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP,STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(startup_source,__file__+"::startup","exec"),startup_scope)


def native_count():
    return len(base.load(stage.PROOF)["records"])


def observed_count():
    return len(base.load(live.LIVE)["cases"])


def verify(registry,previous,viewed):
    proof,played,visual = map(base.load,(stage.PROOF,live.LIVE,VISUAL))
    candidate = base.digest(stage.ROM)
    assert candidate==proof["candidate_sha256"]==played["candidate_sha256"]==base.digest(stage.REBUILT)
    assert previous["candidate_sha256"]==proof["predecessor_sha256"]==played["predecessor_sha256"]==base.digest(parent.ROM)
    assert proof["whole_parent_inverse"] and proof["allocations"]["all_unselected_native_copy_spans_exact"]
    assert proof["allocations"]["all_41_blocks_fit_8KiB"] and proof["allocations"]["complete_COMMON_and_ARM9_table_inverse"]
    assert len(proof["unchanged_formatter_control_keys"])==51
    assert visual["reviewed_candidate_sha256"]==candidate
    assert viewed==visual["sheets"]==proof["sheets"] | played["sheets"]
    assert all(base.digest(p)==h for evidence in (viewed,played["evidence"]) for p,h in evidence.items())
    assert played["focused_gameplay"] and not played["natural_activation"] and observed_count()==2
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]
    clean,old,target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==proof["clean_sha256"]==previous["clean_input_sha256"]
    before,after = map(native.files,(old,target))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={ARM,COMMON}
    scoped,reason = stage.transform(old,before[ARM])
    lo,hi = stage.town.DIRECTORY_OFFSET,stage.relocate.__globals__["TABLE_END"]
    assert reason==proof["native_scope"] and scoped[:lo]==after[ARM][:lo] and scoped[hi:]==after[ARM][hi:]
    assert native.digest(after[ARM])==proof["target_ARM9_sha256"]
    assert native.digest(after[COMMON])==proof["target_COMMON_sha256"]
    for p in (ARM,COMMON):
        target.replace_file(p,before[p])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard==guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean),after)
    assert checks==proof["source25"] and checks["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous,candidate,after[ARM])
    evidence = {c["message_ID"]:c for c in played["cases"].values()}
    rows = proof["records"]
    assert len(rows)==2 and {r["message_ID"] for r in rows}==evidence.keys()==stage.PHRASES.keys()
    assert all(r["previous_English"]==r["english"] and all(r["review"].values()) for r in rows)
    records = [r | {"observed_focused_page":evidence[r["message_ID"]]} for r in rows]
    captions = parent.stage.square.prior
    font = captions.GameAsciiFont.from_arm9(after[ARM])
    gem_holds = []
    for case in played["cases"].values():
        menu, = [shot for shot in case["frames"] if shot["frame"]==6050]
        pixels = captions.live_caption(font,captions.captured(menu),2,"Gem Shop")
        gem_holds.append(dict(frame=menu,complete_caption_mask=pixels))
    result = dict(candidate_sha256=candidate,records=records,translation_policy="natural-dialogue-v2",
        target_locale="en-US",checked_story_format_guard=checks,gem_shop_focused_gameplay=gem_holds,
        visual_review=viewed,focused_square_rumors=played,wrap_only_revisions=2,
        historical_source_credit=dict(by_census_id={},direct_keys=0),full_editorial_goal_complete=False,hardware=False)
    return proof,result,{p:native.digest(after[p]) for p in (ARM,COMMON)}


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1053 and len(checks) == 388":"len(batches) == 1054 and len(checks) == 389",
    "        assert str(stage.history.REVIEW) in batches\n":"",
    "source_bound_square_caption_scope=stored['native_scope']":"source_bound_square_rumor_layout=stored['native_scope']",
    "changed_component_hashes={stage.ARM:archives[stage.ARM]}":"changed_component_hashes=archives",
    "changed_internal_files=[stage.ARM]":"changed_internal_files=sorted(archives)",
    "changed_components=1":"changed_components=2",
    "previously_localized_records=18, contextual_records_revisited=18":"previously_localized_records=2, contextual_records_revisited=2",
    "prior_records_reviewed=18":"prior_records_reviewed=2",
    "justified_retentions=13":"justified_retentions=0",
    "reviewed_UI_labels=18":"reviewed_UI_labels=0",
    "name_label_revisions=5, text_display_revisions=0":"name_label_revisions=0, text_display_revisions=2",
    "wrap_only_revisions=0":"wrap_only_revisions=2",
    "ordinary_Syracuse_and_Lisbon=True, offline_additional_shop_categories=3":
        "focused_original_Square_rumor_selection=True, natural_activation=False",
    "observed_ordinary_revised_captions":"observed_focused_rumors",
    'assert all(row["file_path"] == stage.ARM and row["id"].startswith("SQUARE_SHOP_CAPTION_") for row in draft["records"])':
        'assert all((row["file_path"], aliases.get(row["id"], row["id"])) in credited for row in draft["records"])',
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Square rumor wrap testing candidate

The [testing ROM](../../{ROM.as_posix()}) keeps two complete phrases together in the Square rumors. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("square_shop_names","square_rumor_wraps").replace(
    "verified_square_rumor_followup_predecessor","verified_square_shop_names_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit,{
    "Preserve the Square shop candidate, predecessor and staged ROM":
        "Preserve the Square rumor wrap candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Square rumor wraps

Two retrospective wrap fixes keep “Times certainly have changed!” and “in the Indian Ocean” together. The Japanese meaning, existing English words and Shopkeeper role are preserved. The original regional path retains its mode for 51 neighboring cases, including substitutions. [Installed decisions and evidence](../{REVIEW.as_posix()})

Two focused emulator runs used the original Square selector and rendering path, with the region and random seed set explicitly on a copied save. Both full pages, nameplates and their menu returns were checked. Startup and 17 tests passed, and the clean-input patch reproduces the candidate byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("square_shop_names","square_rumor_wraps")
scope = parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register","exec"),scope)


if __name__=="__main__":
    scope["main"]()
