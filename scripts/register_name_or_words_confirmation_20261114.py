"""Register the verified name and Promised Words confirmation repair."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_diplomatic_outcomes_v2 as ledger_model
from scripts import register_tavern_influence_20261114 as publisher
from scripts import stage_name_or_words_literal_20261114 as stage
from scripts import verify_name_or_words_confirmation_20261114 as live
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files

base,parent=stage.base,stage.parent
PROFILE="all-routes-name-or-words-confirmation-v1-20261114"
ROOT=Path("out/name_or_words_confirmation_registered_20261114_v1")
ROM=ROOT/"Translation_DS_All_Routes_Name_or_Words_Confirmation_20261114_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261114_name_or_words_confirmation_candidate")
PATCH,VERIFY=PACKAGE/"translation.xdelta",PACKAGE/"verification"
REVIEW=VERIFY/"registered_review.json"
RELEASE=VERIFY/"registered_release_verification.json"
DOC=Path("docs/editorial_name_or_words_confirmation_20261114.md")
STARTUP,QA=stage.ROOT/"own_startup_verification.json",stage.ROOT/"repository_qa.xml"
VIEWED=(
    "23aeed13ce2186f33ac9c8fce4ae0c74b835ece8225d91ab5b43452f836db9ed",
    "a67afcfc1df6a3ae959d011e1a8c08fd2887a8dd1ffd0de06a501a395e4df309",
)
FAMILY="shared_name_or_words_confirmation_20261114"


def verify(prior,guard):
    storage,review,boot=map(base.load,(stage.STORED,live.OUT,STARTUP))
    assert base.digest(stage.ROM)==storage["candidate_sha256"]==review["candidate_sha256"]==boot["candidate_sha256"]
    assert base.digest(parent.ROM)==prior["candidate_sha256"]==storage["previous_sha256"]
    assert base.digest(stage.CLEAN)==prior["clean_input_sha256"]==storage["clean_sha256"]
    assert storage["whole_parent_inverse"] and storage["preserved_entries"]==3667 and storage["preserved_blocks"]==40
    assert storage["literal_dispatch"]["unchanged_ITCM_extents"]
    assert review["selector_scope_comparisons"]==11010
    native=review["native_layout"]
    assert len(native["cases"])==39
    assert all(case["exact_complete_mask"] and bytes.fromhex(case["display_hex"])==
               stage.DRAFT.encode("ascii")%bytes.fromhex(case["value_hex"]) for case in native["cases"])
    assert tuple(base.digest(row["path"]) for row in native["sheets"])==tuple(row["sha256"] for row in native["sheets"])==VIEWED
    live_rows=review["observed_gameplay"].values()
    assert sum(len(row["confirmations"]) for row in live_rows)==3
    assert sum(len(row["byte_exact_other_holds"]) for row in live_rows)==9
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"])==6 and len(boot["original_protected_name_getters"])==24
    assert all(base.digest(path)==digest for bundle in (review["evidence"],boot["evidence"]) for path,digest in bundle.items())
    tests,=ElementTree.parse(QA).iter("testsuite")
    assert tuple(int(tests.get(k,0)) for k in ("tests","failures","errors","skipped"))==(20,0,0,0)
    validate_natural_dialogue_batch(review)
    previous,changed=map(base.NdsImage.open,(parent.ROM,stage.ROM))
    a,b=files(previous),files(changed)
    assert a.keys()==b.keys() and {p for p in a if a[p]!=b[p]}=={stage.ARM,stage.COMMON}
    verify_runtime(b[stage.ARM],prior)
    expected_arm,details=stage.select(a[stage.ARM])
    assert b[stage.ARM]==expected_arm and details==storage["literal_dispatch"]
    digest=parent.parent.parent.source.current.assets.edit.digest
    assert digest(b[stage.COMMON])==storage["target_COMMON_sha256"]
    assert digest(b[stage.ARM])==storage["target_ARM9_sha256"]
    scoped=bind_registered_story_percent_guard(guard)(files(base.NdsImage.open(stage.CLEAN)),b)
    assert scoped["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(scoped["source_bound_new_command_counts"].values())
    for path in (stage.ARM,stage.COMMON):
        changed.replace_file(path,a[path])
    assert bytes(changed.rom.save())==parent.ROM.read_bytes()
    row,=review["records"]
    assert row["id"]=="COMMON_MESSAGE_296"
    row.update(file_path=stage.COMMON,new_credit=1,registered_reference=row["staged_reference"]|dict(
        exact_stored_hex=row["staged_hex"],candidate_sha256=storage["candidate_sha256"]))
    return storage,review|dict(checked_story_format_guard=scoped,direct_visual_review_complete=True)


def update_ledger(ledger,review,release):
    text=checked_text(getsource(ledger_model.update_ledger),{
        "diplomatic-and-scheme-outcome-notices":"shared-name-or-words-confirmation",
        "Thirty-four diplomacy and scheme outcomes are registered.":"The ship-name and Promised Words confirmation is reviewed and registered.",
        "== 25985":"== 27700","== 15438":"== 16591","== 10547":"== 11109",
    })
    env=vars(ledger_model)|globals()|dict(TOTAL=1,REVISED=0,RETAINED=1,PREVIOUS_TOTAL=27699,
        VERIFICATION=VERIFY,LIVE_VERIFICATION=live.OUT)
    exec(compile(text,__file__+"::registered-contextual-ledger","exec"),env)
    env["update_ledger"](ledger,review["records"],release,release["actual_verification_scope"])
    pending=ledger["pending_shared_consumer_checkpoint_20261114"]
    assert pending["remaining_total"]==277 and pending["remaining_promotional_and_scene_keys"]==245
    assert len(pending["remaining_legacy_keys"])==32
    pending["remaining_legacy_keys"].remove(296)
    pending.update(remaining_total=276,candidate_sha256=release["candidate_sha256"],
        latest_completed_legacy_confirmation=str(REVIEW))


def main():
    source=getsource(publisher.main)
    lo=source.index('    base.replace_checked(DOC,f"""')
    hi=source.index('""".encode())',lo)+len('""".encode())')
    doc='''    base.replace_checked(DOC,f"""# Ship-name and Promised Words confirmation

COMMON 296 confirms the text entered when buying or renaming a ship and when submitting Promised Words. The original code retains message 296 in r5 while the keyboard is open. The earlier local constant inventory missed these three paths. The clean Japanese asks whether the supplied text is acceptable. “Is %s all right?” still fits all three contexts, with a regular ASCII capital I.

The previous formatter expanded name-like tokens inside the player's text. A controlled run of the earlier release turned FIONA into HodramONA. The correction routes this one confirmation to an existing literal output path. It reuses an existing selector span without expanding ITCM. All 11,010 selector comparisons preserve the prior messages and fallback behavior. The [registered review](../{REVIEW.as_posix()}) records the exact source, previous text, deployed bytes, owner references and complete glyph checks.

Ordinary emulator gameplay verified a completed purchase in Syracuse and a Copenhagen rename confirmation with both No and Yes. Three complete panels passed and nine surrounding frames matched byte for byte. Thirteen inputs per original caller passed 39 offline layout and glyph checks, including an 18-byte name, mixed script, and literal percent signs. Promised Words received offline checks in this batch. The cumulative startup matched six frames and 24 protected getters using the existing system-only unlock fixture. All 20 targeted tests passed.

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right-bound correction. The ledger credits 27,700 reviews, with 276 mapped shared records still to review or classify. Hardware verification remains open.
""".encode())'''
    source=source[:lo]+doc+source[hi:]
    ledger_start=source.index('    ledger["current_integrated_candidate"].update(')
    ledger_end=source.index('    write_pending(ledger_tmp,encode_ledger(ledger))',ledger_start)
    source=source[:ledger_start]+"    update_ledger(ledger,review,release)\n"+source[ledger_end:]
    edits={
        'len(manifest["batches"]) == 810 and len(manifest["checks"]) == 145':'len(manifest["batches"]) == 812 and len(manifest["checks"]) == 147',
        'release_stack.tavern_influence.pending.json':'release_stack.name_or_words_confirmation.pending.json',
        'editorial_review_current.tavern_influence.pending.json':'editorial_review_current.name_or_words_confirmation.pending.json',
        'release_stack_before_tavern_influence.json':'release_stack_before_name_or_words_confirmation.json',
        'for p in (stage.STORED,live.OUT,STARTUP,QA,TOWNS):':'for p in (stage.STORED,live.OUT,STARTUP,QA):',
        'verified_about_extras_predecessor=lineage, tavern_influence_release':'verified_tavern_toast_and_gift_predecessor=lineage, name_or_words_confirmation_release',
        'Natural barkeep wording and verified native display for COMMON 821.':'Bounded literal input and consistent text rendering for COMMON 296.',
        'registered_tavern_influence_and_complete_parent_inverse':'registered_literal_name_or_words_confirmation_and_complete_parent_inverse',
        '    if "COMMON_MESSAGE_821" not in ids:\n        ids.append("COMMON_MESSAGE_821")':'''    assert "COMMON_MESSAGE_296" not in ids
    ids.append("COMMON_MESSAGE_296")
    manifest["changed_records"][stage.ARM].append("DK4_LITERAL_NAME_OR_WORDS_CONFIRMATION_20261114")''',
        'tavern_influence_registered_successor_pipeline':'name_or_words_confirmation_registered_successor_pipeline',
        'native_allocation=staged["byte_allocation"])':'native_allocation=staged["byte_allocation"],literal_dispatch=staged["literal_dispatch"])',
        'registered_manifest_entries=811,passing_release_checks=146,repository_tests=26,legacy_fixture_tests_skipped=2':'registered_manifest_entries=813,passing_release_checks=148,repository_tests=20,legacy_fixture_tests_skipped=0,\n        target_ARM9_sha256=staged["target_ARM9_sha256"]',
        'changed_components=[],changed_internal_files=[stage.COMMON],new_contextual_records=0,\n        prose_revisions=1,justified_retentions=11,reviewed_UI_labels=0':'changed_components=[stage.ARM],changed_internal_files=[stage.COMMON],new_contextual_records=1,\n        prose_revisions=0,justified_retentions=1,text_display_revisions=1,reviewed_UI_labels=0',
        'actual_emulator=True,hardware=False,observed_revised_rumors=1,retained_observed_holds=13,\n            offline_role_and_name_variants=17':'actual_emulator=True,hardware=False,observed_ship_confirmation_panels=3,other_exact_holds=9,\n            offline_native_cases=39,observed_promised_words_entry=False',
        'The Istanbul barkeep’s influence rumor is registered, with current coverage in three towns.':'The ship-name and Promised Words confirmation is reviewed and registered.',
        'digest = parent.source.current.assets.edit.digest':'digest = parent.parent.parent.source.current.assets.edit.digest',
        'Tavern Influence test candidate':'Name and Promised Words Confirmation test candidate',
        'includes the revised Istanbul Tavern rumor':'includes the literal input confirmation and normal ASCII I',
        'Preserve Tavern rumor release and verified replay.':'Preserve name and Promised Words confirmation release and verified replay.',
        '811 entries, 114 accepted layers, 146 checks.':'813 entries, 114 accepted layers, 148 checks.',
    }
    env=vars(publisher)|globals()
    exec(compile(checked_text(source,edits),__file__+"::registered-publication","exec"),env)
    env["main"]()


if __name__=="__main__":
    main()
