"""Register the Trade caption revisions and complete Status label."""

from json import dumps
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_trade_labels_20261119 as game
from scripts import stage_trade_labels_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

parent,base,native = stage.parent,stage.base,stage.native
workflow = parent.env["workflow"]
PROFILE = "all-routes-trade-labels-v1-20261119"
ROOT = Path("out/trade_labels_registered_20261119_v1")
ROM = ROOT/"Translation_DS_Trade_Labels_20261119_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_trade_labels_candidate")
VERIFY,PATCH = PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE = VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC = Path("docs/editorial_trade_labels_20261119.md")
STARTUP,QA = game.STARTUP_PROOF,stage.ROOT/"registered_qa.xml"
CHECKPOINT = "Trade, Ledger, Total and the complete Status now appear in both Market Trade views."
verified = SimpleNamespace(PROOF=stage.PROOF,LIVE=game.PLAYBACK)


def verify(registry,previous,viewed):
    stored,live,boot = map(base.load,(stage.PROOF,game.PLAYBACK,STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==live["candidate_sha256"]==boot["candidate_sha256"]
    assert stored["parent_sha256"]==previous["candidate_sha256"]==base.digest(parent.ROM)
    assert base.digest(stage.CLEAN)==stored["clean_input_sha256"]==previous["clean_input_sha256"]
    assert stored["atlas_bound"]==[256,96] and stored["atlas_rectangles"]==46 and stored["entire_parent_inverse"]
    assert all(base.digest(p)==sha for receipt in (live,boot) for p,sha in receipt["evidence"].items())
    assert all(base.digest(p)==sha for p,sha in stored["source_proofs"].items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"])==6 and len(boot["original_protected_name_getters"])==24
    assert live["ordinary_input"] and not live["hardware"] and live["pixels_outside_changed_text_exact"]
    assert live["visible_status_glyphs_complete"] and live["registered_Goods_Info_complete_in_both_views"]
    assert [r["view"] for r in live["local_and_cargo_holds"]]==["Local","Cargo"]
    assert all(len(r["captions"])==12 for r in live["local_and_cargo_holds"])
    assert viewed=={r["path"]:r["sha256"] for r in live["sheets"]}
    assert all(base.digest(p)==sha for p,sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k,0)) for k in ("tests","failures","errors","skipped")]==[51,0,0,2]
    assert (stage.ROOT/"clean_rebuilt.nds").read_bytes()==stage.ROM.read_bytes()

    clean,predecessor,target = map(base.NdsImage.open,(stage.CLEAN,parent.ROM,stage.ROM))
    old,new = map(native.files,(predecessor,target))
    assert old.keys()==new.keys() and {p for p in old if old[p]!=new[p]}=={stage.ARM}
    assert native.digest(new[stage.ARM])==stored["target_ARM9_sha256"]
    trace = {r["caller_LR"]:r for r in base.load(stage.TRACE/"requests.json")["rows"]}
    expected,records = stage.transform(clean.read_file(stage.ARM),old[stage.ARM],trace)
    assert expected==new[stage.ARM]
    assert dumps(records,sort_keys=True)==dumps(stored["records"],sort_keys=True)
    stage.verify_runtime(expected,previous)
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean),new)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(stage.ARM,old[stage.ARM])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    shared = parent.stage.workflow
    directory = native.digest(expected[shared.DIRECTORY_OFFSET:shared.TABLE_OFFSET])
    entries = shared.owned_entries(new[stage.COMMON],expected,directory)
    pending = base.load(stage.PENDING)["records"]
    assert len(pending)==276
    assert all(r["current_reference"]==shared.reference(entries[r["message_ID"]]) and
               r["current_hex"]==entries[r["message_ID"]].text.hex() for r in pending)
    assert sum(r["wording_changed"] for r in records)==3 and sum(r["display_changed"] for r in records)==4
    for row in records:
        row["registered_reference"] = row["current_reference"]|dict(candidate_sha256=candidate)
    review = {k:stored[k] for k in ("translation_policy","target_locale","encoder","review_gates")}
    review.update(candidate_sha256=candidate,records=records,checked_story_format_guard=controls,new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],direct_visual_review=viewed,
        observed_gameplay=live,source_and_native_dependency_proofs=stored["source_proofs"])
    validate_natural_dialogue_batch(review)
    return stored,review,{stage.ARM:native.digest(expected)}


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
program = checked_text(publish,{
    'len(manifest["batches"]) == 919 and len(manifest["checks"]) == 254':
        'len(manifest["batches"]) == 920 and len(manifest["checks"]) == 255',
    '    profile.update(verified_inn_conversations_predecessor=predecessor, inn_numerals_release=str(REVIEW), inn_numeral_call_sites=stored["original_calls"])':
        '    profile.update(verified_inn_numerals_predecessor=predecessor, trade_labels_release=str(REVIEW))',
    "inn_numerals":"trade_labels",
    "owned_shared_records=[row":"owned_label_records=[row",
    "target_COMMON_sha256=archives[stage.COMMON]":"target_ARM9_sha256=archives[stage.ARM]",
    "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]":
        "changed_components=1, target_ARM9_sha256=archives[stage.ARM]",
    "MESFILE_sha256=archives[stage.COMMON]":"MESFILE_sha256=previous['target_COMMON_sha256']",
    "reviewed_UI_labels=0":"reviewed_UI_labels=12",
    "previously_localized_records=5":"previously_localized_records=12",
    "prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=4":
        "prose_revisions=3, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=8",
    "text_display_revisions=5":"text_display_revisions=4",
    "ordinary_Istanbul_stay_and_return=True, initialized_raid_rumor_and_return=True": "ordinary_Lisbon_Trade_Local_and_Cargo=True",
    "natural_activation=True, raid_natural_activation=False, hardware=False":"natural_activation=True, hardware=False",
    "    if PRESERVED_PREPARATION.exists():\n        candidates.append(PRESERVED_PREPARATION)\n":"",
    "Preserve Inn numeral ROM or reconstruction":"Preserve Trade label ROM or reconstruction",
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Trade labels test candidate

The [local ROM](../../{ROM.as_posix()}) includes the full Trade, Ledger, Total and Status labels and preceding cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Market Trade labels

The Trade window now says Trade, Ledger and Total. The game already held the complete word Status, but its label region showed only the first four letters. The enlarged regions fit the existing Trade text atlas, and all 46 regions remain inside its bounds with no overlaps. The other eight captions keep their wording and geometry, with source glosses and individual reasons in the review. [Exact source, current and registered records](../{REVIEW.as_posix()})

Paired ordinary Lisbon replays verified the complete 12-caption masks in both Local and Cargo. Every sampled pixel outside the four changed label regions matches the predecessor. The Goods Info fix still shows the complete Olive Oil entry with an empty suffix area, and the amount changes during the drag match the original. Hardware remains unvisited. [Native and gameplay evidence](../{VERIFY.as_posix()})

Only three caption strings and four draw rectangles change in ARM9. The clean-input patch reconstructs the ROM byte for byte. Six startup holds, 24 protected getters and 49 focused tests passed, with two optional older-ROM fixture tests skipped. All 276 open shared entries and their mapped references carry forward. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env|globals()
exec(compile(program,__file__+"::register","exec"),env)


if __name__=="__main__":
    env["main"]()
