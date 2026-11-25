"""Register the four verified cross-route wrap and pagination fixes."""

from pathlib import Path
from types import FunctionType

from scripts import register_hodram_late_story_wraps_20261123 as parent
from scripts import stage_observed_wrap_followups_20261123 as stage
from scripts import verify_observed_wrap_followups_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-observed-wrap-followups-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Observed_Wrap_Followups_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_observed_wrap_followups_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_observed_wrap_followups_registered_20261123.md")
DISPLAY, EVIDENCE, FE = stage.NATIVE, stage.ROOT, stage.FE_PROOF
GLYPHS, CHOICE, ROLES = live.GLYPHS, live.CHOICES, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered the four observed wrap fixes for Cesare, Zhuge Liang, Vivian and Gerhard."
RUNS = ("0", *live.RUNS)
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    choices, roles, modal = map(base.load, (CHOICE, ROLES, FE))
    assert all(proof["candidate_sha256"] == candidate for proof in (choices, roles, modal))
    assert modal["complete_stored_page_count"] == 0 and not any(r["kind"] == "system" for r in records)
    assert choices["stored_tables_exact"] and len(choices["choices"]) == 7
    archive = "/data/SC1.DK4"
    expected = {row["id"]:row for row in base.load(stage.REVIEW)["retained_choice_labels"]}
    observed = {(row["block"], row["slot"]):row for row in played["original_menu_choices"]}
    assert observed.keys() == {(167, 0), (216, 2)}
    captions = []
    for label in choices["choices"]:
        row = expected.pop(label["id"])
        block = label["block"]
        payload = banks[archive].blocks[block]
        capture = None
        if (block, label["command_word"]) in ((167, 0x2100), (216, 0x2200)):
            capture = observed.pop((block, label["slot"]), None)
            if capture:
                assert capture["original_branch_executed"] and capture["caption"] == label["caption"]
        current, offset = row["current_reference"], label["offset"]
        at = offset - current["offset"] + current["command_offset"]
        raw, body = (bytes.fromhex(current[k]) for k in ("exact_command_hex", "exact_body_hex"))
        assert payload[at:at+len(raw)] == raw and raw.hex() == label["exact_command_hex"]
        assert payload[offset:offset+len(body)+1] == body+b"\x00" and label["caption"] == row["english"]
        ref = current | dict(candidate_sha256=candidate, archive_sha256=base.load(stage.PROOF)["archive_hashes"][archive],
            block_sha256=native.digest(payload), offset=offset, command_offset=at)
        captions.append(row | dict(registered_reference=ref, observed_focused=capture, review=row["review"] | {"formatting": True}))
    assert not expected and not observed
    assert roles["offline_native_getters_only"] and roles["new_editorial_credit"] == 0
    assert {row["actor_ID"] for row in roles["records"]} == live.NOTES.keys()
    assert all(all(row["review"].values()) for row in roles["records"])
    return dict(retained_modal_pages=0, retained_choice_labels=captions, retained_supporting_roles=10,
        modal_proof_sha256=base.digest(FE), choice_proof_sha256=base.digest(CHOICE), role_proof_sha256=base.digest(ROLES))


scene_checks = parent.verify_source[parent.verify_source.index('    signature, ='):parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    'observed_count() == 31': 'observed_count() == 9',
    'native_count() == 22': 'native_count() == 5',
    'archives = {stage.ARCHIVE}': 'archives = {"/data/SC0.DK4", "/data/SC1.DK4"}',
    '    observed = {(r["file_path"], r["id"]): r for r in played["observations"]}':
        '    observed = {}\n'
        '    for observation in played["observations"]:\n'
        '        observed.setdefault((observation["file_path"], observation["id"]), []).append(observation)',
    '        records.append(row | dict(registered_reference=registered, display_proof=display,\n'
    '            review=row["review"] | {"formatting":True}, observed_focused=observed.pop((path, ident), None)))':
        '        pages = observed.pop((path, ident), [])\n'
        '        records.append(row | dict(registered_reference=registered, display_proof=display,\n'
        '            review=row["review"] | {"formatting":True}, observed_focused=pages[0] if pages else None,\n'
        '            observed_focused_pages=pages))',
    'len(records) == 259': 'len(records) == 77',
    'len(changed) == 22': 'len(changed) == 4',
    'for r in changed) == 22': 'for r in changed) == 4',
    'assert set(manuscript["wrap_leads_covered"]) == {row["id"] for row in changed}':
        'assert not manuscript["wrap_leads_covered"]',
    scene_checks:'''    cesare, = [row for row in changed if row["id"] == "DK4_MES_B167_R0122"]
    liang, = [row for row in changed if row["id"] == "DK4_MES_B216_R0078"]
    assert len(cesare["display_proof"]["layouts"][0]["pages"]) == 2
    assert [page["page_number"] for page in cesare["observed_focused_pages"]] == [1, 2]
    assert len(liang["display_proof"]["layouts"][0]["pages"]) == 1
''',
    'stage.paired.QUEUE': 'stage.PLAN_PROOF',
    'heuristic_triage_sha256=': 'observed_findings_preflight_sha256=',
    'wording_revisions=22': 'wording_revisions=4',
    'justified_retentions=237, choice_label_retentions=22': 'justified_retentions=73, choice_label_retentions=7',
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    'len(batches) == 1084 and len(checks) == 419': 'len(batches) == 1085 and len(checks) == 420',
    'assert len(checks) == 420': 'assert len(checks) == 421',
    'verified_hodram_late_midroute_wraps_predecessor': 'verified_active_predecessor',
    'previously_localized_records=288, contextual_records_revisited=288, contextual_decisions_reused=266':
        'previously_localized_records=84, contextual_records_revisited=84, contextual_decisions_reused=80',
    'prior_records_reviewed=288, contextual_decisions_reused=266': 'prior_records_reviewed=84, contextual_decisions_reused=80',
    'justified_retentions=237, retained_choice_labels=22, retained_style_variants=7':
        'justified_retentions=73, retained_choice_labels=7, retained_style_variants=0',
    'prose_revisions=22': 'prose_revisions=4',
    'focused_initialized_Hodram=True, default_substitution_panels=1, retained_modal_pages=17, revised_modal_pages=0, native_choice_outcomes=3':
        'focused_initialized_Hodram=True, focused_initialized_Rafael=True, default_substitution_panels=0, retained_modal_pages=0, revised_modal_pages=0, native_choice_outcomes=2',
    'live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE, ROLES, STYLES':
        'live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.REVIEW, FE, CHOICE, ROLES, stage.PLAN_PROOF',
    'DISPLAY, GLYPHS, FE, CHOICE, ROLES, STYLES, args.visual_review':
        'DISPLAY, GLYPHS, FE, CHOICE, ROLES, stage.PLAN_PROOF, args.visual_review',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Observed wrap and pagination fixes

The [testing ROM](../../{ROM.as_posix()}) includes four revised passages in the Rafael and Hodram routes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_late_story_wraps", "observed_wrap_followups").replace(
    "verified_active_predecessor", "verified_hodram_late_story_wraps_predecessor")

pins = parent.commit[parent.commit.index("    excerpt_rom = "):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins:'''    earlier = [Path(base.load(live.rafael_scope["receipt"](0))["rom"])]
    for block in live.PROMPTS:
        _, fixture, receipt = live.choice_paths(block)
        assert base.digest(fixture) == base.load(receipt)["rom_sha256"]
        earlier.append(fixture)
''',
    'Preserve the Hodram wrap candidate, predecessor and focused ROMs':
        'Preserve the observed-wrap candidate, predecessor and focused ROMs',
    old_doc:'''    DOC.write_text(f"""# Observed wrap and pagination fixes

Four complete exchanges reconcile 84 previously reviewed texts, including 73 speech retentions and seven original choice captions. Four revisions reflow Cesare's trade routes lesson, the Zhuge Liang reply, Vivian's Avalon clue and Gerhard's account of Noritsune. [Exact review](../{REVIEW.as_posix()})

All five revised pages passed native glyph and stored layout checks. Nine focused holds cover both pages of Cesare's revised lesson, the following panel, the new single-page Zhuge Liang response and both Rafael passages. Other choices and ordinary scene activation remain unvisited on this candidate. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_late_story_wraps", "observed_wrap_followups")

scope = parent.scope | globals()
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
