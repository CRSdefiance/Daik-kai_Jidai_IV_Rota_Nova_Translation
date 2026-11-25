"""Register the Basra and Map Key release after native and gameplay checks."""

from pathlib import Path
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_midroute_exchanges_20261122 as prior
from scripts import replay_rafael_basra_and_map_keys_20261123 as live
from scripts import stage_rafael_basra_and_map_keys_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native, parent = prior.base, prior.native, stage.active
PROFILE = "all-routes-rafael-basra-and-map-keys-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Rafael_Basra_And_Map_Keys_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261123_rafael_basra_and_map_keys_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_rafael_basra_and_map_keys_registered_20261123.md")
DISPLAY, EVIDENCE, GLYPHS, FE, CHOICE, ROLES = stage.NATIVE, stage.ROOT, live.GLYPHS, stage.FE_PROOF, live.CHOICES, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's Basra negotiations, Map Key discoveries, and encounters with Escante's and Maldonado's men."
RUNS = ("0", *live.RUNS)
labels = SimpleNamespace(NOTES=live.NOTES)
bind_registered_story_percent_guard = parent.scope["bind_registered_story_percent_guard"]
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def guard_spec():
    return dict(path=str(stage.GUARD), sha256=base.digest(stage.GUARD))


controls_source = checked_text(getsource(prior.retained_controls), {
    'modal["complete_stored_page_count"] == 17': 'modal["complete_stored_page_count"] == 2',
    '        assert panel["changed"] == (row["decision"] == "revision")\n'
    '        if panel["changed"]:\n'
    '            assert row["observed_focused"] and ident == "DK4_MES_B118_R0125"\n'
    '        else:\n'
    '            assert installed["exact_command_hex"] == row["current_reference"]["exact_command_hex"]':
        '        assert row["decision"] == "retention" and row["observed_focused"] and not panel["second_page"]\n'
        '        assert installed["exact_command_hex"] == row["current_reference"]["exact_command_hex"]',
    'len(choices["choices"]) == 5': 'len(choices["choices"]) == 6',
    'retained_modal_pages=16, revised_modal_pages=1': 'retained_modal_pages=2, revised_modal_pages=0',
})
verify_source = checked_text(prior.verify_source, {
    'observed_count() == 50': 'observed_count() == 28',
    'native_count() == 32': 'native_count() == 17',
    '    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]\n'
    '    assert guard == guard_spec()\n'
    '    checks = bind_registered_story_percent_guard(guard)(native.files(clean), b)':
        '    old_guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]\n'
        '    assert old_guard == base.load(stage.GUARD)["source25_predecessor_receipt"]\n'
        '    checks = bind_registered_story_percent_guard(guard_spec())(native.files(clean), b)',
    'len(records) == 275': 'len(records) == 207',
    'len(changed) == 31': 'len(changed) == 15',
    '    assert sum(r["change_class"] == "prose" for r in changed) == 30\n'
    '    assert [r["id"] for r in changed if r["change_class"] == "wrap_only"] == ["DK4_MES_B118_R0125"]':
        '    assert all(r["change_class"] == "prose" for r in changed)\n'
        '    company, = [r for r in changed if r["id"] == "DK4_MES_B154_R0084"]\n'
        '    default, maximum = company["display_proof"]["layouts"]\n'
        '    assert b"Castor Co.," in bytes.fromhex(default["expanded_hex"])\n'
        '    assert b"W" * 20 + b"," in bytes.fromhex(maximum["expanded_hex"])\n'
        '    assert all(row["lines"][0].startswith("You\\x27re with ") for row in (default, maximum))',
    'wording_revisions=30, wrap_only_revisions=1': 'wording_revisions=15, wrap_only_revisions=0',
    'justified_retentions=244, choice_label_retentions=5': 'justified_retentions=192, choice_label_retentions=6',
})

readme = prior.main[prior.main.index('    (PACKAGE / "README.md").write_text'):prior.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(prior.main, {
    "len(batches) == 1076 and len(checks) == 411": "len(batches) == 1079 and len(checks) == 414",
    "verified_hodram_early_and_midroute_predecessor": "verified_hodram_recruitment_and_sails_predecessor",
    "previously_localized_records=280, contextual_records_revisited=280":
        "previously_localized_records=213, contextual_records_revisited=213",
    "prior_records_reviewed=280": "prior_records_reviewed=213",
    "justified_retentions=244, retained_choice_labels=5": "justified_retentions=192, retained_choice_labels=6",
    "prose_revisions=30": "prose_revisions=15",
    "wrap_only_revisions=1": "wrap_only_revisions=0",
    "default_substitution_panels=2, retained_modal_pages=16, revised_modal_pages=1, native_choice_outcomes=5":
        "default_substitution_panels=2, retained_modal_pages=2, revised_modal_pages=0, native_choice_outcomes=6",
    "FE, CHOICE, ROLES)": "FE, CHOICE, ROLES, stage.GUARD, stage.GUARD_SC0)",
    "FE, CHOICE, ROLES, args.visual_review,": "FE, CHOICE, ROLES, stage.GUARD, stage.GUARD_SC0, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's Basra and Map Key scenes

The [testing ROM](../../{ROM.as_posix()}) includes the refreshed dialogue. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_midroute_exchanges", "rafael_basra_and_map_keys").replace("rafael_basra_and_map_keys_20261122", "rafael_basra_and_map_keys_20261123")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(prior.commit, {
    '    earlier = [excerpt_rom, *(live.choice_paths(block)[1] for block in live.PROMPTS)]':
        '    prototype_root = stage.BATCH.parent / "staged"\n'
        '    prototype = prototype_root / stage.ROM.name\n'
        '    receipt = base.load(prototype_root / stage.PROOF.name)\n'
        '    assert receipt["whole_parent_inverse"] and base.digest(prototype) == receipt["candidate_sha256"] != candidate\n'
        '    earlier = [excerpt_rom, *(live.choice_paths(block)[1] for block in live.PROMPTS), prototype]\n'
        '    former_gameplay = prototype_root / live.ROOT.name\n'
        '    for path in list(earlier)[:-1]:\n'
        '        older_fixture = former_gameplay / path.relative_to(live.ROOT)\n'
        '        assert older_fixture.is_file()\n'
        '        earlier.append(older_fixture)',
    "Preserve the Rafael midroute candidate, predecessor and focused ROMs":
        "Preserve the Rafael Basra and Map Key candidate, predecessor and focused ROMs",
    "2026-11-22": "2026-11-23",
    old_doc:'''    DOC.write_text(f"""# Rafael's Basra and Map Key scenes

The clean-Japanese review covers 213 texts across ten complete exchanges. Fifteen revisions address fourteen flagged wraps and restore the interrupted reference to Escante's homeland. The ledger records 192 dialogue and panel retentions and all six choice captions. [Exact review](../{REVIEW.as_posix()})

Seventeen revised layouts, two market-share notices and twelve name or role labels passed native checks. Focused gameplay verified 28 holds across the revised dialogue and all six original choice outcomes. The layout also preserves the punctuation of the default company name and the five original Uddin actor controls at their new offsets. Ordinary activation and handheld testing remain open for these scenes. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("rafael_midroute_exchanges", "rafael_basra_and_map_keys")

scope = prior.scope | globals()
for source in (controls_source, verify_source, main, commit):
    exec(compile(source, __file__ + "::source-bound-registration", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
