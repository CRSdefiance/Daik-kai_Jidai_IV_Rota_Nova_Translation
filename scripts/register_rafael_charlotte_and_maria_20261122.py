"""Register Rafael's Charlotte and East Asia review over the cumulative candidate."""

from pathlib import Path
from types import FunctionType

from scripts import register_hodram_and_lil_followups_20261122 as prior
from scripts import replay_rafael_charlotte_and_maria_20261122 as live
from scripts import stage_rafael_charlotte_and_maria_20261122 as stage
from scripts import verify_ceuta_and_lisbon_20261122 as town
from scripts.source_locked_derivation_v5118 import checked_text


base, native = prior.base, prior.native
parent = stage.active
PROFILE = "all-routes-rafael-charlotte-and-maria-v1-20261122"
ROOT = prior.ROOT.with_name("rafael_charlotte_and_maria_registered_20261122")
WORK = stage.BATCH.parent / "registration"
ROM = ROOT / "Translation_DS_Rafael_Charlotte_And_Maria_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261122_rafael_charlotte_and_maria_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_rafael_charlotte_and_maria_registered_20261122.md")
DISPLAY, EVIDENCE, GLYPHS = stage.NATIVE, stage.ROOT, live.GLYPHS
ORDINARY = town.OUTPUT
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's Charlotte exchange and his first East Asia scenes with Maria."
RUNS = live.RUNS
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(prior.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(prior.native_count.__code__, prior.native_count.__globals__ | globals())
observed_count = FunctionType(prior.observed_count.__code__, prior.observed_count.__globals__ | globals())


def ordinary_proof(candidate):
    evidence = base.load(ORDINARY)
    assert evidence["candidate_sha256"] == candidate
    assert evidence["ordinary_saved_gameplay"] and evidence["original_controller_and_touch"] and not evidence["hardware"]
    assert set(evidence["visits"]) == {"Ceuta", "Lisbon"}
    assert sum(len(visit["panels"]) for visit in evidence["visits"].values()) == 12
    assert all(all(panel["review"].values()) for visit in evidence["visits"].values() for panel in visit["panels"])
    assert all(base.digest(path) == sha for path, sha in evidence["evidence"].items())
    return evidence


verify_source = checked_text(prior.verify_source, {
    'checked["sheets"] + base.load(FE)["sheets"] + played["sheets"]':
        'checked["sheets"] + played["sheets"] + ordinary_proof(candidate)["sheets"]',
    'observed_count() == 30': 'observed_count() == 17',
    'native_count() == 18': 'native_count() == 12',
    'archives = {"/data/SC1.DK4", "/data/SC2.DK4"}': 'archives = {"/data/SC0.DK4"}',
    'len(records) == 288': 'len(records) == 134',
    'len(changed) == 18': 'len(changed) == 12',
    '        retained_native_controls=retained_controls(records, played, banks, candidate),\n':
        '        ordinary_town_gameplay=ordinary_proof(candidate),\n',
    'wording_revisions=18, wrap_only_revisions=0': 'wording_revisions=12, wrap_only_revisions=0',
    'justified_retentions=270, choice_label_retentions=2': 'justified_retentions=122, choice_label_retentions=0',
})

readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(prior.build, {
    "len(batches) == 1072 and len(checks) == 407": "len(batches) == 1073 and len(checks) == 408",
    "previously_localized_records=290, contextual_records_revisited=290": "previously_localized_records=134, contextual_records_revisited=134",
    "prior_records_reviewed=290": "prior_records_reviewed=134",
    "justified_retentions=270, retained_choice_labels=2": "justified_retentions=122, retained_choice_labels=0",
    "prose_revisions=18": "prose_revisions=12",
    "changed_components=2": "changed_components=1",
    "focused_initialized_Hodram_and_Lil=True, retained_modal_pages=4, original_Lil_branches=2":
        "focused_initialized_Rafael=True, default_substitution_panels=2",
    "ordinary_saved_town_visits=False": "ordinary_saved_town_visits=True",
    "verified_rafael_followup_predecessor": "verified_hodram_lil_predecessor",
    "stage.REVIEW, FE, CHOICE": "stage.REVIEW, ORDINARY",
    "DISPLAY, GLYPHS, FE, CHOICE, args.visual_review,": "DISPLAY, GLYPHS, ORDINARY, args.visual_review,",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's Charlotte and East Asia exchanges

The [testing ROM](../../{ROM.as_posix()}) carries 12 dialogue revisions. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_and_lil_followups", "rafael_charlotte_and_maria")

old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
start, stop = (prior.commit.index(name) for name in ("    earlier = ", "    research = "))
commit = checked_text(prior.commit, {
    prior.commit[start:stop]: '    earlier = [Path(base.load(live.scope["receipt"](0))["rom"])]\n',
    "Preserve the Hodram and Lil candidate, predecessor and focused ROM":
        "Preserve the Rafael Charlotte and East Asia candidate, predecessor and focused ROM",
    old_doc:'''    DOC.write_text(f"""# Rafael's Charlotte and East Asia exchanges

The clean-Japanese review records 134 decisions, including 12 revisions and 122 justified retentions. Charlotte's gift and Rafael's embarrassment stay understated. The wako explanation retains the coastal raids and the pirates' frequent escapes. Maria's agreement and her later delivery of the Bamboo Assembly Plan preserve her terms. [Exact review](../{REVIEW.as_posix()})

All 12 revised pages passed complete native glyph and layout checks. Focused emulator gameplay verified 17 dialogue holds, both default-name substitution cases and the return to port. The natural story triggers and handheld display remain unvisited. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)

Ordinary saved gameplay verified twelve displayed panels across Ceuta Square, Lisbon Square and the Lisbon Tavern. The sailor question keeps its tag together on the first line. [Town dialogue evidence](../{(VERIFY / ORDINARY.name).as_posix()})
""",encoding="utf-8")
''',
}).replace("hodram_and_lil_followups", "rafael_charlotte_and_maria")

scope = prior.scope | globals() | {
    name: parent.scope[name] for name in ("guard_spec", "bind_registered_story_percent_guard")
}
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
