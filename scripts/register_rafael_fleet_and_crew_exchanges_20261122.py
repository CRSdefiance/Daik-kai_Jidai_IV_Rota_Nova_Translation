"""Register Rafael's six fleet and crew exchanges and their verified displays."""

from pathlib import Path
from types import FunctionType

from scripts import register_rafael_charlotte_and_maria_20261122 as prior
from scripts import replay_rafael_fleet_and_crew_exchanges_20261122 as live
from scripts import stage_rafael_fleet_and_crew_exchanges_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
parent = stage.active
PROFILE = "all-routes-rafael-fleet-and-crew-v1-20261122"
ROOT = prior.ROOT.with_name("rafael_fleet_and_crew_exchanges_registered_20261122")
WORK = stage.BATCH.parent / "registration"
ROM = ROOT / "Translation_DS_Rafael_Fleet_And_Crew_Exchanges_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261122_rafael_fleet_and_crew_exchanges_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_rafael_fleet_and_crew_exchanges_registered_20261122.md")
DISPLAY, EVIDENCE, GLYPHS, FE, ROLES = stage.NATIVE, stage.ROOT, live.GLYPHS, stage.FE_PROOF, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's fleet and crew exchanges from Seville through the Ninja Garb rumor."
RUNS = ("0",)
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def retained_roles_and_panels(records, candidate):
    modal, roles = map(base.load, (FE, ROLES))
    assert modal["candidate_sha256"] == roles["candidate_sha256"] == candidate
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 4
    assert roles["offline_native_getters_only"] and roles["new_editorial_credit"] == 0
    panels = {r["id"]:r for r in modal["records"]}
    owners = {r["id"]:r for r in records if r["source_selector"] == 254}
    assert panels.keys() == owners.keys()
    for ident, owner in owners.items():
        panel, installed = panels[ident], owner["registered_reference"]
        assert not panel["second_page"] and owner["decision"] == "retention" and owner["observed_focused"]
        assert panel["stored_offset"] == installed["command_offset"]
        assert panel["exact_command_hex"] == installed["exact_command_hex"] == owner["current_reference"]["exact_command_hex"]
    assert {r["actor_ID"] for r in roles["records"]} == live.role_notes.keys()
    by_id = {row["id"]: row for row in records}
    for item in roles["records"]:
        assert all(item["review"].values()) and item["decision"] == "retention"
        bound = [by_id[ident] for ident in item["context_records"]]
        assert bound and all(r["source_selector"] == item["actor_ID"] for r in bound)
        assert any(r["observed_focused"] for r in bound)
    return dict(retained_modal_pages=len(panels), modal_proof_sha256=base.digest(FE),
                retained_supporting_roles=len(roles["records"]), role_proof_sha256=base.digest(ROLES))


verify_source = checked_text(prior.verify_source, {
    'checked["sheets"] + played["sheets"] + ordinary_proof(candidate)["sheets"]':
        'checked["sheets"] + played["sheets"] + base.load(FE)["sheets"]',
    'observed_count() == 17': 'observed_count() == 25',
    'native_count() == 12': 'native_count() == 15',
    'len(records) == 134': 'len(records) == 224',
    '        ordinary_town_gameplay=ordinary_proof(candidate),\n':
        '        retained_roles_and_modal_panels=retained_roles_and_panels(records, candidate),\n',
    'justified_retentions=122, choice_label_retentions=0': 'justified_retentions=212, choice_label_retentions=0',
})

readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(prior.build, {
    "len(batches) == 1073 and len(checks) == 408": "len(batches) == 1074 and len(checks) == 409",
    "previously_localized_records=134, contextual_records_revisited=134": "previously_localized_records=224, contextual_records_revisited=224",
    "prior_records_reviewed=134": "prior_records_reviewed=224",
    "justified_retentions=122": "justified_retentions=212",
    "default_substitution_panels=2": "default_substitution_panels=3, retained_modal_pages=4, supporting_roles=9",
    "ordinary_saved_town_visits=True": "ordinary_saved_town_visits=False",
    "verified_hodram_lil_predecessor": "verified_charlotte_east_asia_predecessor",
    "stage.REVIEW, ORDINARY": "stage.REVIEW, FE, ROLES",
    "DISPLAY, GLYPHS, ORDINARY, args.visual_review,": "DISPLAY, GLYPHS, FE, ROLES, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's fleet and crew exchanges

The [testing ROM](../../{ROM.as_posix()}) carries 12 dialogue revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_charlotte_and_maria", "rafael_fleet_and_crew_exchanges")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    "Preserve the Rafael Charlotte and East Asia candidate, predecessor and focused ROM":
        "Preserve the Rafael fleet and crew candidate, predecessor and focused ROM",
    old_doc:'''    DOC.write_text(f"""# Rafael's fleet and crew exchanges

The clean-Japanese review covers 224 texts across six complete exchanges. Twelve revisions address the flagged wraps, and 212 texts have individual retention reasons. Julio's question tag stays with his retort, Rafael's full name stays together at maximum width, and Janus's explanation fits in four complete rows. [Exact review](../{REVIEW.as_posix()})

Fifteen revised display cases and four original modal panels passed native checks. Focused emulator gameplay verified 25 holds and the return to port. Nine supporting roles have source-bound dialogue and catalogue getter checks. These story tests used initialized excerpts. Handheld display and regular activation of the six story scenes remain unverified. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_charlotte_and_maria", "rafael_fleet_and_crew_exchanges")

scope = prior.scope | globals() | {
    name: parent.scope[name] for name in ("guard_spec", "bind_registered_story_percent_guard")
}
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
