"""Register the revised Square labels after native and ordinary gameplay checks."""

from inspect import getsource
from types import SimpleNamespace
from xml.etree import ElementTree as ET

from scripts import register_square_rumor_followup_20261122 as parent
from scripts import stage_square_shop_names_20261122 as stage
from scripts import verify_square_shop_names_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow = parent.base,parent.native,parent.workflow
ARM,COMMON = stage.ARM,stage.COMMON
PROFILE = "all-routes-square-shop-names-v1-20261122"
ROOT = parent.ROOT.with_name("square_shop_names_registered_20261122")
ROM = ROOT/"Translation_DS_Square_Shop_Names_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_square_shop_names_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_square_shop_names_registered_20261122.md")
EVIDENCE = stage.ROOT
STARTUP,STARTUP_CAPTURE,QA = EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_passed.xml"
VISUAL = EVIDENCE/"visual_review.json"
live = SimpleNamespace(LIVE=display.LIVE)
CHECKPOINT = "Registered five revised Square shop names and thirteen justified retentions."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_source = checked_text(parent.startup_source,{
    "only_COMMON_directory_and_offset_fields_changed=True":"square_caption_dispatch_only=True",
})
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP,STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(startup_source,__file__+"::startup","exec"),startup_scope)


def native_count():
    return len(base.load(stage.PROOF)["records"])


def observed_count():
    return len(base.load(live.LIVE)["actual_changed_categories"])


def verify(registry,previous,viewed):
    proof,played,visual = map(base.load,(stage.PROOF,live.LIVE,VISUAL))
    candidate = base.digest(stage.ROM)
    assert candidate==proof["candidate_sha256"]==played["candidate_sha256"]==base.digest(stage.REBUILT)
    assert previous["candidate_sha256"]==proof["predecessor_sha256"]==played["predecessor_sha256"]==base.digest(parent.ROM)
    assert proof["whole_parent_inverse"] and played["unchanged_syracuse_pixels_outside_spice_cell"]
    assert visual["reviewed_candidate_sha256"]==candidate
    assert viewed==visual["sheets"]==proof["sheets"] | played["sheets"]
    assert all(base.digest(p)==h for evidence in (viewed,played["evidence"]) for p,h in evidence.items())
    assert played["actual_changed_categories"] == [3,7] and played["offline_only_changed_categories"] == [10,12,14]
    assert all(row["ordinary_saved_gameplay"] for row in played["observed"].values())
    assert len(proof["independent_category_getter_controls"])==144
    assert base.digest(stage.LEAD)==proof["exact_lead_sha256"]
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]
    clean,old,target = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==proof["clean_sha256"]==previous["clean_input_sha256"]
    before,after = map(native.files,(old,target))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={ARM}
    assert stage.transform(before[ARM])==(after[ARM],proof["native_scope"])
    assert native.digest(after[ARM])==proof["target_ARM9_sha256"]
    assert native.digest(after[COMMON])==previous["target_COMMON_sha256"]
    target.replace_file(ARM,before[ARM])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard==guard_spec()
    checks = bind_registered_story_percent_guard(guard)(native.files(clean),after)
    assert checks==proof["source25"] and checks["total_exact_source_bound_relocated_leading25_count"]==7
    startup_scope["startup_proof"](previous,candidate,after[ARM])
    rows = proof["records"]
    assert len(rows)==18 and all(all(row["review"].values()) for row in rows)
    assert {r["category"]:r["english"] for r in rows if r["decision"]=="revision"}==stage.NAMES
    earlier = base.load(stage.history.REVIEW)
    assert {r["id"] for r in earlier["records"]}=={r["id"] for r in rows}
    records = [r | {"observed_revised_caption":r["category"] in played["actual_changed_categories"]} for r in rows]
    result = dict(candidate_sha256=candidate,records=records,checked_story_format_guard=checks,
        visual_review=viewed,ordinary_square_menus=played,reviewed_UI_labels=18,caption_revisions=5,
        justified_retentions=13,earlier_registered_UI_review=dict(path=str(stage.history.REVIEW),sha256=base.digest(stage.history.REVIEW)),
        historical_source_credit=dict(by_census_id={},direct_keys=0),full_editorial_goal_complete=False,hardware=False)
    return proof,result,{p:native.digest(after[p]) for p in (ARM,COMMON)}


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1052 and len(checks) == 387":"len(batches) == 1053 and len(checks) == 388",
    "    batches.append(str(REVIEW))":"    assert str(stage.history.REVIEW) in batches\n        batches.append(str(REVIEW))",
    "source_bound_square_rumor_storage=stored['allocations']":"source_bound_square_caption_scope=stored['native_scope']",
    "changed_component_hashes=archives":"changed_component_hashes={stage.ARM:archives[stage.ARM]}",
    "changed_internal_files=sorted(archives)":"changed_internal_files=[stage.ARM]",
    "changed_components=2":"changed_components=1",
    "previously_localized_records=21, contextual_records_revisited=21":"previously_localized_records=18, contextual_records_revisited=18",
    "prior_records_reviewed=21":"prior_records_reviewed=18",
    "prose_revisions=3":"prose_revisions=0",
    "justified_retentions=18":"justified_retentions=13",
    "reviewed_UI_labels=0":"reviewed_UI_labels=18",
    "name_label_revisions=0, text_display_revisions=3":"name_label_revisions=5, text_display_revisions=0",
    "ordinary_Valencia_and_Syracuse=True, offline_China_rumor=True":
        "ordinary_Syracuse_and_Lisbon=True, offline_additional_shop_categories=3",
    "observed_ordinary_regional_rumors":"observed_ordinary_revised_captions",
    "(live.LIVE, DISPLAY)":"(live.LIVE, stage.PROOF)",
    'assert all((row["file_path"], aliases.get(row["id"], row["id"])) in credited for row in draft["records"])':
        'assert all(row["file_path"] == stage.ARM and row["id"].startswith("SQUARE_SHOP_CAPTION_") for row in draft["records"])',
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Square shop name testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes Spice Shop, Craft Shop, Scent Shop, Gem Shop and Dye Shop. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("square_rumor_followup","square_shop_names").replace(
    "verified_hodram_opening_reply_predecessor","verified_square_rumor_followup_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit,{
    "Preserve the Square rumor candidate, predecessor and staged ROM":
        "Preserve the Square shop candidate, predecessor and staged ROM",
    old_doc:'''    DOC.write_text(f"""# Square shop names

The Square now uses Spice Shop, Craft Shop, Scent Shop, Gem Shop and Dye Shop. These names match the original categories and the goods each shop sells. The other 13 captions retain their individual source-based wording. The independent commodity headings keep their category terms. [Source, installed references and decisions](../{REVIEW.as_posix()})

Ordinary Syracuse and Lisbon replays verified Spice Shop and Craft Shop. In Syracuse the two-screen changes were confined to the Spice Shop caption cell. Every caption passed the complete native glyph and bounds checks. Startup and 17 regression tests passed, and the clean-input patch reconstructs the ROM byte for byte. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("square_rumor_followup","square_shop_names")
scope = parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::register","exec"),scope)


if __name__=="__main__":
    scope["main"]()
