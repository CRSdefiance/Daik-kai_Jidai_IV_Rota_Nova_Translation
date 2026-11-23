"""Register the four retained Inn paragraphs and one revised raid reply."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_inn_numerals_finish_20261119 as game
from scripts import stage_inn_numerals_finish_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

parent,base,native = stage.parent,stage.base,stage.native
workflow = parent.env["workflow"]
PROFILE = "all-routes-inn-numerals-v2-20261119"
ROOT = Path("out/inn_numerals_registered_20261119_v2")
ROM = ROOT/"Translation_DS_Inn_Numerals_20261119_candidate.nds"
PRESERVED_PREPARATION = Path("out/inn_numerals_registered_20261119_v1")/ROM.name
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261119_inn_numerals_candidate_v2")
VERIFY, PATCH = PACKAGE/"verification", PACKAGE/"translation.xdelta"
REVIEW, RELEASE = VERIFY/"registered_review.json", VERIFY/"registered_release_verification.json"
DOC = Path("docs/editorial_inn_numerals_20261119.md")
STARTUP, QA = game.STARTUP_PROOF, stage.ROOT/"registered_qa.xml"
CHECKPOINT = "Regular dialogue numerals replace wide digits in five Inn records, with a complete raid reaction verified in Istanbul."
verified = SimpleNamespace(PROOF=stage.NATIVE_PROOF,LIVE=game.PLAYBACK)


def verify(registry,previous,viewed):
    staged,review,playback,boot = map(base.load,(stage.PROOF,stage.NATIVE_PROOF,game.PLAYBACK,STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate==staged["candidate_sha256"]==review["candidate_sha256"]==playback["candidate_sha256"]==boot["candidate_sha256"]
    assert staged["parent_sha256"]==previous["candidate_sha256"]==base.digest(parent.ROM)
    assert base.digest(stage.CLEAN)==staged["clean_input_sha256"]==previous["clean_input_sha256"]
    assert staged["entire_parent_inverse"] and staged["other_aligned_main_formatter_calls_preserved"]==66
    assert all(base.digest(p)==sha for receipt in (review,playback,boot) for p,sha in receipt["evidence"].items())
    assert all(base.digest(p)==sha for p,sha in staged["source_proofs"].items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"])==6 and len(boot["original_protected_name_getters"])==24
    assert len(review["stay_number_calls"])==96 and len(review["calendar_cases"])==144 and review["layout_cases"]==529
    assert len(review["rejected_orphaned_town_raid_layouts"])==23
    stay,raid = playback["ordinary_stay"],playback["initialized_raid"]
    assert stay["message_ID"]==1180 and stay["actual_numeric_argument"]=="3" and stay["normal_return_frame"]==8600
    assert raid["message_ID"]==1197 and raid["lines"][-1].endswith("What a lousy thing to do!")
    assert raid["native_argument_bytes"][0]==b"10 months ago".hex() and raid["history_consumed"]
    assert not raid["natural_activation"] and not playback["hardware"]
    assert viewed=={r["path"]:r["sha256"] for r in review["sheets"]+playback["sheets"]}
    assert all(base.digest(p)==sha for p,sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(key,0)) for key in ("tests","failures","errors","skipped")]==[51,0,0,2]
    assert (stage.ROOT/"clean_rebuilt.nds").read_bytes()==stage.ROM.read_bytes()

    clean,predecessor,target = map(base.NdsImage.open,(stage.CLEAN,parent.ROM,stage.ROM))
    old,new = map(native.files,(predecessor,target))
    archives = {p:native.digest(new[p]) for p in old if old[p]!=new[p]}
    assert old.keys()==new.keys() and archives=={stage.ARM:staged["target_ARM9_sha256"],stage.COMMON:staged["target_COMMON_sha256"]}
    compiled,helper = stage.previous.recompile(predecessor,old[stage.ARM],previous)
    assert compiled==new[stage.ARM] and helper.hex()==staged["helper_hex"]
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean),new)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    for path in archives:
        target.replace_file(path,old[path])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    w = stage.workflow
    directory = native.digest(compiled[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    before,installed = [w.owned_entries(f[stage.COMMON],f[stage.ARM],directory) for f in (old,new)]
    assert {r.message_id for r,q in zip(before,installed,strict=True) if r.text!=q.text}=={stage.REVISED}
    pending = base.load(stage.PENDING)["records"]
    assert len(pending)==276
    assert all(r["current_reference"]==w.reference(installed[r["message_ID"]]) and
               r["current_hex"]==installed[r["message_ID"]].text.hex() for r in pending)
    clean_entries = w.common_message_entries(clean.read_file(stage.COMMON),clean.read_file(stage.ARM))
    assert tuple(r["message_ID"] for r in review["records"])==stage.AFFECTED
    for row in review["records"]:
        n = row["message_ID"]
        assert row["source_hex"]==clean_entries[n].text.hex() and row["staged_hex"]==installed[n].text.hex()
        row["current_reference"] = w.reference(before[n])
        row["current_hex"] = before[n].text.hex()
        row["registered_reference"] = w.reference(installed[n])|dict(candidate_sha256=candidate)
        row["observed_gameplay"] = "ordinary stay" if n==1180 else "initialized raid" if n==1197 else "offline"
    review.update(checked_story_format_guard=controls,new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],direct_visual_review=viewed,
        observed_gameplay=playback,source_and_native_dependency_proofs=staged["source_proofs"])
    validate_natural_dialogue_batch(review)
    return staged,review,archives


publish = parent.program
readme = publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc = publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
program = checked_text(publish,{
    'len(manifest["batches"]) == 918 and len(manifest["checks"]) == 253':
        'len(manifest["batches"]) == 919 and len(manifest["checks"]) == 254',
    "verified_hostess_conversations_predecessor": "verified_inn_conversations_predecessor",
    "inn_conversations": "inn_numerals",
    "prose_revisions=4, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=19":
        "prose_revisions=1, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=4",
    "previously_localized_records=23": "previously_localized_records=5",
    "text_display_revisions=4": "text_display_revisions=5",
    "ordinary_Istanbul_stays_and_return=True": "ordinary_Istanbul_stay_and_return=True, initialized_raid_rumor_and_return=True",
    "natural_activation=True, hardware=False": "natural_activation=True, raid_natural_activation=False, hardware=False",
    "changed_components=1, target_COMMON_sha256=archives[stage.COMMON]":
        "changed_components=2, target_ARM9_sha256=archives[stage.ARM], target_COMMON_sha256=archives[stage.COMMON]",
    "ARM9_sha256=previous['target_ARM9_sha256']": "ARM9_sha256=archives[stage.ARM]",
    "Preserve Inn dialogue ROM or reconstruction": "Preserve Inn numeral ROM or reconstruction",
    '    for path in candidates:': '    if PRESERVED_PREPARATION.exists():\n        candidates.append(PRESERVED_PREPARATION)\n    for path in candidates:',
    '    profile.update(verified_hostess_conversations_predecessor=predecessor, inn_conversations_release=str(REVIEW))':
        '    profile.update(verified_inn_conversations_predecessor=predecessor, inn_numerals_release=str(REVIEW), inn_numeral_call_sites=stored["original_calls"])',
    readme: """    (PACKAGE / "README.md").write_text(f\"\"\"# Inn numerals test candidate

The [local ROM](../../{ROM.as_posix()}) uses regular dialogue digits for Inn stays and rumors and includes the revised raid reaction.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc: """    DOC.write_text(f\"\"\"# Inn dialogue numerals

The three original Inn number-format calls now display regular dialogue digits in the stay confirmation and four dated rumors. The original formatter still allocates the string and supplies the value. The Inn conversion preserves the return pointer, all other known number-format call sites and the registered ASCII right-bound correction. [Exact records, layout and caller evidence](../{REVIEW.as_posix()})

The narrower numbers exposed an isolated final “do!” in 23 versions of the town-raid rumor. The innkeeper's revised reaction keeps the disapproval while fitting together in the Istanbul replay. Four other paragraphs retain their wording. Native checks covered all 32 ring positions for the three stay counts, all 144 calendar cases and 529 paragraph layouts. The 13 representative pages were visually checked. [Native evidence](../{VERIFY.as_posix()})

Ordinary Istanbul inputs verified the regular 3, the confirmation and the return to town. A declared history fixture activated the original 10-month raid rumor, showing the revised reaction in full. The game consumed the event and returned to town. Hardware and natural raid activation remain unvisited. The exact patch rebuilds the ROM from the clean input. Six startup holds, 24 protected name getters and 49 focused tests passed, with two optional older ROM fixture tests skipped. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env = parent.env|globals()
exec(compile(program,__file__+"::register","exec"),env)


if __name__=="__main__":
    env["main"]()
