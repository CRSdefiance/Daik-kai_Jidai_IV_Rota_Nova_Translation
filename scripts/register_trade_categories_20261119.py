"""Register the verified category labels and the Square Textiles substitution."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_trade_categories_20261119 as game
from scripts import stage_trade_categories_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

parent,base,native = stage.parent,stage.base,stage.native
workflow = parent.env["workflow"]
PROFILE = "all-routes-trade-categories-v1-20261119"
ROOT = Path("out/trade_categories_registered_20261119_v1")
ROM = ROOT/"Translation_DS_Trade_Categories_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_trade_categories_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = Path("docs/editorial_trade_categories_20261119.md")
STARTUP,QA = game.STARTUP_PROOF,stage.ROOT/"registered_qa.xml"
CHECKPOINT = "Goods Info uses six clearer category names, including Seasonings verified in both Trade views."
verified = SimpleNamespace(PROOF=stage.NATIVE,LIVE=game.PLAYBACK)


def verify(registry,previous,viewed):
    stored,review,live,boot = map(base.load,(stage.PROOF,stage.NATIVE,game.PLAYBACK,STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==review["candidate_sha256"]==live["candidate_sha256"]==boot["candidate_sha256"]
    assert stored["parent_sha256"]==previous["candidate_sha256"]==base.digest(parent.ROM)
    assert base.digest(stage.CLEAN)==stored["clean_input_sha256"]==previous["clean_input_sha256"]
    assert stored["entire_parent_inverse"]
    assert all(base.digest(p)==sha for receipt in (review,live,boot) for p,sha in receipt["evidence"].items())
    assert all(base.digest(p)==sha for p,sha in stored["source_proofs"].items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"])==6 and len(boot["original_protected_name_getters"])==24
    assert live["ordinary_input"] and not live["hardware"] and live["only_category_and_shifted_percentage_pixels_changed"]
    assert live["goods_name_and_suffix_masks_complete"]
    assert [r["view"] for r in live["local_and_cargo_holds"]]==["Local","Cargo"]
    assert all(r["registered"]["text"]=="Olive Oil\n  Seasonings 100%" for r in live["local_and_cargo_holds"])
    assert len(review["real_native_format_cases"])==1240 and len(review["category_getter_cases"])==192
    assert viewed=={r["path"]:r["sha256"] for r in live["sheets"]+review["sheets"]}
    assert all(base.digest(p)==sha for p,sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k,0)) for k in ("tests","failures","errors","skipped")]==[51,0,0,2]
    assert (stage.ROOT/"clean_rebuilt.nds").read_bytes()==stage.ROM.read_bytes()

    clean,predecessor,target = map(base.NdsImage.open,(stage.CLEAN,parent.ROM,stage.ROM))
    old,new = map(native.files,(predecessor,target))
    assert old.keys()==new.keys() and {p for p in old if old[p]!=new[p]}=={stage.ARM}
    assert native.digest(new[stage.ARM])==stored["target_ARM9_sha256"]
    expected,helper = stage.stage_arm(predecessor,old[stage.ARM],previous)
    assert expected==new[stage.ARM] and helper.hex()==stored["helper_hex"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean),new)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(stage.ARM,old[stage.ARM])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    shared = parent.parent.stage.workflow
    directory = native.digest(expected[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[stage.COMMON],expected,directory)
    pending = base.load(stage.PENDING)["records"]
    assert len(pending)==276
    assert all(r["current_reference"]==shared.reference(entries[r["message_ID"]]) and
               r["current_hex"]==entries[r["message_ID"]].text.hex() for r in pending)
    assert [r["category"] for r in review["records"]]==list(range(18))
    assert {r["category"] for r in review["records"] if r["decision"]=="revision"}==stage.REVISED
    for row in review["records"]:
        row["registered_reference"] = row["staged_reference"]|dict(candidate_sha256=candidate)
        row["observed_in_ordinary_trade"] = row["category"]==1
    review.update(checked_story_format_guard=controls,new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],direct_visual_review=viewed,
        observed_gameplay=live,source_and_native_dependency_proofs=stored["source_proofs"])
    validate_natural_dialogue_batch(review)
    return stored,review,{stage.ARM:native.digest(expected)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
program = checked_text(publish,{
    'len(manifest["batches"]) == 920 and len(manifest["checks"]) == 255':
        'len(manifest["batches"]) == 921 and len(manifest["checks"]) == 256',
    "verified_inn_numerals_predecessor":"verified_trade_labels_predecessor",
    "trade_labels":"trade_categories",
    "reviewed_UI_labels=12":"reviewed_UI_labels=18",
    "previously_localized_records=12":"previously_localized_records=18",
    "prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=8":
        "prose_revisions=6, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=12",
    "text_display_revisions=4":"text_display_revisions=6",
    "Preserve Trade label ROM or reconstruction":"Preserve Trade category ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Trade categories test candidate

The [local ROM](../../{ROM.as_posix()}) includes six revised Goods Info category names and the earlier Trade labels.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Trade commodity categories

Goods Info now uses Seasonings, Delicacy, Textiles, Jewelry, Medicine and Sundries. The review ties all 18 names to the clean Japanese and the 124 commodities. Twelve labels retain their wording. Metals fits alongside the maximum number allowed by the existing price field. The Square rumor also uses Textiles through its original category substitution. [Exact review and source references](../{REVIEW.as_posix()})

The native formatter passed 1,240 cases across both Trade callers, including the five-digit unsigned limit. Five revised categories received offline width and font checks. Ordinary Lisbon gameplay verified Seasonings and the complete percentage in both Local and Cargo. Every changed pixel stayed on that line, and the other sampled pixels matched. The Square rumor passed offline native layout and glyph checks. Hardware remains unvisited. [Native and gameplay evidence](../{VERIFY.as_posix()})

The two Trade calls use the revised category lookup. The earlier terminated Goods Info format and registered ASCII right bound still pass their exact guards. The clean-input patch rebuilds the ROM byte for byte. Six startup holds, 24 protected getters and 49 focused tests passed, with two optional older ROM fixture tests skipped. All 276 open shared records retain their mapped references and contents. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env|globals()
exec(compile(program,__file__+"::register","exec"),env)


if __name__=="__main__":
    env["main"]()
