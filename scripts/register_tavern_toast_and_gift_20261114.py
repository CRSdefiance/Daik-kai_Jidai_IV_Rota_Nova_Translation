"""Register the Tavern toast and Hodram’s gift reply with exact release ancestry."""

from inspect import getsource
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import checkpoint_tavern_drinks_and_gifts_20261114 as context
from scripts import stage_tavern_toast_and_gift_20261114 as stage
from scripts import verify_tavern_toast_and_gift_20261114 as live
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files

base,parent=stage.base,stage.parent
PROFILE="all-routes-tavern-toast-and-gift-v1-20261114"
ROOT=Path("out/tavern_toast_and_gift_registered_20261114_v1")
ROM=ROOT/"Translation_DS_All_Routes_Tavern_Toast_and_Gift_20261114_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261114_tavern_toast_and_gift_candidate")
PATCH,VERIFY=PACKAGE/"translation.xdelta",PACKAGE/"verification"
REVIEW=VERIFY/"registered_review.json"
RELEASE=VERIFY/"registered_release_verification.json"
DOC=Path("docs/editorial_tavern_toast_and_gift_registered_20261114.md")
STARTUP,QA=stage.ROOT/"own_startup_verification.json",stage.ROOT/"repository_qa.xml"
VIEWED="ee7369ec8225b6257d43324215571ef9f85b0d25e1da7341dfc025d1e110b998"


def verify(prior,guard):
    storage,batch,boot,review=map(base.load,(stage.STORED,live.OUT,STARTUP,context.OUT))
    assert base.digest(stage.CLEAN)==prior["clean_input_sha256"]==storage["clean_sha256"]
    assert base.digest(parent.ROM)==prior["candidate_sha256"]==storage["previous_sha256"]==review["candidate_sha256"]
    assert base.digest(stage.ROM)==storage["candidate_sha256"]==batch["candidate_sha256"]==boot["candidate_sha256"]
    assert storage["whole_parent_inverse"] and storage["preserved_entries"]==3666 and storage["preserved_blocks"]==40
    native=batch["native_layout"]
    assert len(native["cases"])==222 and native["current_item_getters"]==218
    assert len(native["original_eight_gift_selectors"])==len(native["native_fonts"])==8
    assert base.digest(native["sheet"])==native["sheet_sha256"]==VIEWED
    assert base.digest(native["current_snapshot"])==native["snapshot_sha256"]
    assert not any(row["findings"] for row in native["cases"])
    assert len(batch["observed_gameplay"]["exact_same_frame_controls"])==13
    assert review["reviewed_source_keys"]==34 and review["retentions"]==32
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"])==6 and len(boot["original_protected_name_getters"])==24
    assert all(base.digest(path)==digest for group in (batch["observed_gameplay"]["evidence"],boot["evidence"])
               for path,digest in group.items())
    tests,=ElementTree.parse(QA).iter("testsuite")
    assert tuple(int(tests.get(k,0)) for k in ("tests","failures","errors","skipped"))==(20,0,0,0)
    validate_natural_dialogue_batch(batch)
    previous,changed=map(base.NdsImage.open,(parent.ROM,stage.ROM))
    a,b=files(previous),files(changed)
    assert a.keys()==b.keys() and {p for p in a if a[p]!=b[p]}=={stage.COMMON}
    verify_runtime(b[stage.ARM],prior)
    assert base.digest(stage.ROM)==batch["candidate_sha256"]
    assert parent.parent.source.current.assets.edit.digest(b[stage.COMMON])==storage["target_COMMON_sha256"]
    scoped=bind_registered_story_percent_guard(guard)(files(base.NdsImage.open(stage.CLEAN)),b)
    assert scoped["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(scoped["source_bound_new_command_counts"].values())
    changed.replace_file(stage.COMMON,a[stage.COMMON])
    assert bytes(changed.rom.save())==parent.ROM.read_bytes()
    for row in batch["records"]:
        row["registered_reference"]=row["staged_reference"]|dict(exact_stored_hex=row["staged_hex"],
            candidate_sha256=storage["candidate_sha256"])
    return storage,batch|dict(checked_story_format_guard=scoped,direct_visual_review_complete=True,
        complete_exchange_review=str(context.OUT),complete_exchange_review_sha256=base.digest(context.OUT))


def main():
    source=getsource(parent.main)
    lo=source.index('    base.replace_checked(DOC,f"""')
    hi=source.index('""".encode())',lo)+len('""".encode())')
    document='''    base.replace_checked(DOC,f"""# Tavern introductions and gifts

Faticia now confirms the player's name and toasts their meeting. Hodram's gift reply gives the item's name directly. The other captains keep their original replies and follow-up questions. The [exchange ledger](../{context.OUT.as_posix()}) records the full clean Japanese comparison, two revisions and 32 justified retentions across prices, rumors, the drink offer and the gift sequence.

The ordinary Istanbul replay displayed the revised toast. The separate No path displayed the existing teasing reply and returned to town. Thirteen surrounding frames on the paid path were pixel-identical. Offline, all four captain names and all 218 current item names passed the native substitution and wrap checks. Eight gift selectors and eight complete native glyph previews passed. The gift branch remains unvisited in this batch's gameplay. The cumulative startup matched six frames and 24 protected names, using the existing system-only unlock fixture. All 20 targeted tests passed.

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers. The only changed archive is COMMON, with two records revised in place. The ledger credits 27,699 reviews and 277 mapped shared keys remain to review or classify. Hardware verification remains open.
""".encode())'''
    source=source[:lo]+document+source[hi:]
    edits={
        'len(manifest["batches"]) == 810 and len(manifest["checks"]) == 145':'len(manifest["batches"]) == 811 and len(manifest["checks"]) == 146',
        'release_stack.tavern_influence.pending.json':'release_stack.tavern_toast_and_gift.pending.json',
        'editorial_review_current.tavern_influence.pending.json':'editorial_review_current.tavern_toast_and_gift.pending.json',
        'release_stack_before_tavern_influence.json':'release_stack_before_tavern_toast_and_gift.json',
        'for p in (stage.STORED,live.OUT,STARTUP,QA,TOWNS):':'for p in (stage.STORED,live.OUT,STARTUP,QA,context.OUT):',
        'verified_about_extras_predecessor=lineage, tavern_influence_release':'verified_tavern_influence_predecessor=lineage, tavern_toast_and_gift_release',
        'Natural barkeep wording and verified native display for COMMON 821.':'Contextual Tavern toast and gift wording with verified native display.',
        'registered_tavern_influence_and_complete_parent_inverse':'registered_tavern_toast_and_gift_and_complete_parent_inverse',
        '    if "COMMON_MESSAGE_821" not in ids:\n        ids.append("COMMON_MESSAGE_821")':'''    for row in review["records"]:
        if row["id"] not in ids:
            ids.append(row["id"])''',
        'tavern_influence_registered_successor_pipeline':'tavern_toast_and_gift_registered_successor_pipeline',
        'registered_manifest_entries=811,passing_release_checks=146,repository_tests=26,legacy_fixture_tests_skipped=2':'registered_manifest_entries=812,passing_release_checks=147,repository_tests=20,legacy_fixture_tests_skipped=0',
        'prose_revisions=1,justified_retentions=11':'prose_revisions=2,justified_retentions=32',
        'actual_emulator=True,hardware=False,observed_revised_rumors=1,retained_observed_holds=13,\n            offline_role_and_name_variants=17':'actual_emulator=True,hardware=False,observed_revised_toast=1,retained_observed_holds=13,\n            retained_drink_refusal_observed=True,offline_substitutions=222,offline_gift_only=True',
        'The Istanbul barkeep’s influence rumor is registered, with current coverage in three towns.':'The Tavern introduction and gift exchange are reviewed, with the toast and Hodram’s reply registered.',
        'ledger["tavern_influence_review_20261114"] = dict(review=str(REVIEW),release=str(RELEASE),town_coverage=str(TOWNS),\n        revised_existing_key=821,new_dialogue_credit=0,followup_key=827,known_pending_counts_unchanged=True)':'ledger["tavern_toast_and_gift_review_20261114"] = dict(review=str(REVIEW),release=str(RELEASE),exchange_review=str(context.OUT),\n        revised_existing_keys=[827,831],retentions=32,new_dialogue_credit=0,known_pending_counts_unchanged=True)',
        'digest = parent.source.current.assets.edit.digest':'digest = parent.parent.source.current.assets.edit.digest',
        'Tavern Influence test candidate':'Tavern Toast and Gift test candidate',
        'includes the revised Istanbul Tavern rumor':'includes the revised Tavern toast and Hodram’s item reply',
        'Preserve Tavern rumor release and verified replay.':'Preserve Tavern toast and gift release and verified replay.',
        '811 entries, 114 accepted layers, 146 checks.':'812 entries, 114 accepted layers, 147 checks.',
    }
    env=vars(parent)|globals()
    exec(compile(checked_text(source,edits),__file__+"::registered-publication","exec"),env)
    env["main"]()


if __name__=="__main__":
    main()
