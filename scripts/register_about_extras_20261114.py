"""Publish the verified About Extras sequence using the registered successor workflow."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import stage_extras_tie_in_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base,parent=stage.base,stage.parent
source=SimpleNamespace(OUTPUT=stage.REVIEW,ARM=stage.ARM,current=parent.source.current)
PROFILE="all-routes-about-extras-v1-20261114"
CHECK="registered_about_extras_promised_words_and_complete_parent_inverse"
ROOT=Path("out/about_extras_registered_20261114_v1")
ROM=ROOT/"Translation_DS_All_Routes_About_Extras_20261114_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261114_about_extras_candidate")
PATCH,VERIFY=PACKAGE/"translation.xdelta",PACKAGE/"verification"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
QA=stage.original.ROOT/"repository_qa.xml"
STARTUP=stage.ROOT/"own_startup_verification.json"
DOC=Path("docs/editorial_about_extras_registered_20261114.md")
VIEWED="dba384625e6572932403cd70870c6690efb082b79e1218aaf3716b3249a5dd84"


def verify(previous,guard):
    stored,live,startup=map(base.load,(stage.STORED,stage.LIVE,STARTUP))
    sha=base.digest(stage.ROM)
    assert sha==stored["target_sha256"]==live["target_ROM_sha256"]==startup["candidate_sha256"]
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==stored["parent_sha256"]
    assert base.digest(stage.REVIEW)==stored["review_sha256"]
    assert live["complete_revised_and_retained_masks"] and len(live["exact_navigation_control_frames"])==3
    assert base.digest(live["sheet"])==live["sheet_sha256"]==VIEWED
    assert startup["cold_boot"] and not startup["savestate"] and startup["complete_deployed_payload_exact"]
    assert len(startup["exact_matching_frames"])==6 and len(startup["original_protected_name_getters"])==24
    for proof in (live["initial_evidence"],live["live_evidence"],startup["evidence"]):
        assert all(base.digest(path)==digest for path,digest in proof.items())
    tests=list(ElementTree.parse(QA).iter("testsuite"))
    assert sum(int(item.get("tests",0)) for item in tests)==34
    assert not any(int(item.get(k,0)) for item in tests for k in ("errors","failures","skipped"))
    before,after=map(base.NdsImage.open,(parent.ROM,stage.ROM))
    original,target=files(before),files(after)
    assert original.keys()==target.keys() and {p for p in original if original[p]!=target[p]}=={stage.ARM}
    a,b=original[stage.ARM],target[stage.ARM]
    assert len(a)==len(b)
    receipt=bytearray(b)
    for lo,hi in stored["owned_body_and_pointer_spans"]:
        receipt[lo:hi]=a[lo:hi]
    assert receipt==a
    stage.verify_runtime(b,previous)
    assert source.current.assets.edit.digest(b)==stored["target_ARM9_sha256"]
    clean=base.NdsImage.open(parent.parent.stage.CLEAN)
    guard_result=bind_registered_story_percent_guard(guard)(files(clean),target)
    assert guard_result["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(guard_result["source_bound_new_command_counts"].values())
    after.replace_file(stage.ARM,a)
    assert bytes(after.rom.save())==parent.ROM.read_bytes()
    assert len(live["records"])==6 and sum(row["decision"]=="revision" for row in live["records"])==5
    live_rows=[]
    for row in live["records"]:
        own=row.get("revised_reference",row["current_reference"])
        off=own["ARM9_offset"]
        current_bytes=bytes.fromhex(own["exact_stored_hex"])
        assert b[off:off+len(current_bytes)]==current_bytes
        live_rows.append(row | dict(registered_reference=own | {"candidate_sha256":sha}))
    return live | dict(records=live_rows,registered_candidate_sha256=sha,direct_visual_review_complete=True,
        actual_visual_review_pending=False,checked_story_format_guard=guard_result)


def publish():
    template=getsource(parent.main)
    checkpoint_start='    base.replace_checked(DOC,f"""'
    end='""".encode())'
    lo=template.index(checkpoint_start)
    hi=template.index(end,lo)+len(end)
    document='''    base.replace_checked(DOC,f"""# About Extras and the Online tie-in

The [registered review](../{REVIEW.as_posix()}) covers the six visible About Extras panels. The introduction is retained. Five revisions use the village menu's **Promised Words** name, keep trade goods distinct from inventory items, restore the official website reference and remove an unsupported claim about notice before service changes. The original two step headings stay on their own lines. The formatter keeps the full game name and feature name together.

Two cold boots confirmed all six panels through ordinary A presses. The revised replay matched every complete line and found three exact menu and return frames. The cumulative cold boot matched six startup frames and 24 protected name getters. All 34 formatter and review tests passed. Hardware remains unvisited.

The visible panels come from six independent ARM9 pointers. This About Extras route requests no COMMON text. Legacy COMMON 3317–3319 remain open for other possible callers. The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers. The dialogue ledger credits 27,699 and 277 mapped shared keys stay in scope.
""".encode())'''
    template=template[:lo]+document+template[hi:]
    old_metadata=',changed_arm9_body_slot_offset=0x137D7D'
    assert template.count(old_metadata)==1
    template=template.replace(old_metadata,'')
    edits={
        "parent.stage.CLEAN":"parent.parent.stage.CLEAN",
        'len(manifest["batches"])==808 and len(manifest["checks"])==143':'len(manifest["batches"])==809 and len(manifest["checks"])==144',
        'len(manifest["batches"])==809 and len(manifest["checks"])==144\n    base.save':'len(manifest["batches"])==810 and len(manifest["checks"])==145\n    base.save',
        "stage.RECEIPT":"stage.STORED",
        "release_stack.grand_race_stopping.pending.json":"release_stack.about_extras.pending.json",
        "editorial_review_current.grand_race_stopping.pending.json":"editorial_review_current.about_extras.pending.json",
        "release_stack_before_grand_race_stopping.json":"release_stack_before_about_extras.json",
        "verified_alexandria_cooking_predecessor":"verified_grand_race_stopping_predecessor",
        "grand_race_stopping_help_release":"about_extras_promised_words_release",
        "Natural wording and verified native display for Grand Race’s stopping rule.":"Full About Extras contextual review with Promised Words and original panel controls.",
        '''    ident=next(row["id"] for row in proof["records"] if row["decision"]=="revision")
    owned=manifest["changed_records"][source.ARM]
    if ident not in owned:
        owned.append(ident)''':'''    owned=manifest["changed_records"][source.ARM]
    for row in proof["records"]:
        if row["decision"]=="revision" and row["id"] not in owned:
            owned.append(row["id"])''',
        "grand_race_stopping_registered_successor_pipeline":"about_extras_promised_words_registered_successor_pipeline",
        "unchanged_descriptor_and_whole_parent_inverse=True":"complete_parent_inverse=True,owned_ARM9_spans=base.load(stage.STORED)['owned_body_and_pointer_spans']",
        'registered_manifest_entries=809':'registered_manifest_entries=810',
        "passing_release_checks=144,repository_tests=46":"passing_release_checks=145,repository_tests=34",
        "prose_revisions=1,justified_retentions=8":"prose_revisions=5,justified_retentions=1",
        "observed_rules_pages=9,\n            revised_page_mask_pass=True,exact_unrelated_and_return_frames=5,wireless_race_started=False":"observed_about_extras_pages=6,\n            complete_page_glyph_checks=True,exact_menu_and_return_frames=3,legacy_common_requested=False",
        "Grand Race rules review and the stopping-page revision are registered.":"About Extras and the Promised Words instructions are registered.",
        "grand_race_stopping_rules_20261114":"about_extras_promised_words_20261114",
        "revised_help_pages=1,retained_help_pages=8,new_dialogue_credit=0,exhibition_COMMON_318_consumer_pending=True":"revised_pages=5,retained_pages=1,new_dialogue_credit=0,legacy_COMMON_3317_to_3319_other_callers_pending=True",
        "Grand Race Help review candidate":"About Extras review candidate",
        "the revised Stopping a Race page and all prior cumulative work":"the reviewed About Extras sequence and all earlier cumulative work",
        "Preserve Grand Race stopping-page release and verification.":"Preserve About Extras release and verification.",
        "809 entries, 114 accepted layers, 144 checks.":"810 entries, 114 accepted layers, 145 checks.",
    }
    namespace=vars(parent)|globals()
    exec(compile(checked_text(template,edits),__file__+"::registered-cumulative-publication","exec"),namespace)
    namespace["main"]()


if __name__=="__main__":
    publish()

