"""Register five source-bound departure warning revisions on the Square build."""

from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import register_square_label_wording_20261119 as parent
from scripts import replay_departure_warnings_20261119 as game
from scripts import stage_departure_warnings_20261119 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base,native=stage.base,stage.native
PROFILE="all-routes-departure-warnings-v1-20261119"
ROOT=Path("out/departure_warnings_registered_20261119_v1")
ROM=ROOT/"Translation_DS_Departure_Warnings_20261119_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261119_departure_warnings_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=Path("docs/editorial_departure_warnings_20261119.md")
STARTUP,QA=game.STARTUP_PROOF,stage.ROOT/"registered_qa.xml"
VISUAL_REVIEW=stage.ROOT/"direct_visual_review.json"
CHECKPOINT="Five Port departure warnings have revised wording and wrapping, with the crew shortage warning verified in Lisbon."
verified=SimpleNamespace(PROOF=stage.PROOF,LIVE=game.PLAYBACK)


def verify(registry,previous,viewed):
    staged,playback,boot=map(base.load,(stage.PROOF,game.PLAYBACK,STARTUP))
    candidate=base.digest(stage.ROM)
    assert candidate==staged["candidate_sha256"]==playback["candidate_sha256"]==boot["candidate_sha256"]
    assert staged["parent_sha256"]==previous["candidate_sha256"]==base.digest(parent.ROM)
    assert base.digest(stage.CLEAN)==staged["clean_input_sha256"]==previous["clean_input_sha256"]
    assert staged["entire_parent_inverse"]
    assert all(base.digest(p)==sha for receipt in (playback,boot) for p,sha in receipt["evidence"].items())
    assert all(base.digest(p)==sha for p,sha in staged["source_proofs"].items())
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"])==6 and len(boot["original_protected_name_getters"])==24
    assert len(playback["complete_revised_holds"])==2 and playback["normal_return_frame"]==game.RETURN
    assert playback["ordinary_input_after_one_byte_crew_fixture"] and not playback["hardware"]
    capture=base.load(game.CAPTURE/"capture_report.json")
    menus={s["frame"]:s for s in capture["frames_captured"] if s["frame"] in (3700,game.RETURN)}
    assert {f:base.digest(s["path"]) for f,s in menus.items()}=={f:s["PNG_sha256"] for f,s in menus.items()}
    assert menus[3700]["framebuffer_sha256"]==menus[game.RETURN]["framebuffer_sha256"]
    assert viewed=={s["path"]:s["sha256"] for s in staged["sheets"]+playback["sheets"]}
    assert all(base.digest(p)==sha for p,sha in viewed.items())
    suite,=ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(p,0)) for p in ("tests","failures","errors","skipped")]==[51,0,0,2]
    assert (stage.ROOT/"clean_rebuilt.nds").read_bytes()==stage.ROM.read_bytes()
    clean,parent_rom,target=map(base.NdsImage.open,(stage.CLEAN,parent.ROM,stage.ROM))
    old,new=map(native.files,(parent_rom,target))
    assert old.keys()==new.keys()
    assert {p for p in old if old[p]!=new[p]}=={stage.COMMON}
    assert native.digest(new[stage.COMMON])==staged["target_COMMON_sha256"]
    arm=new[stage.ARM]
    parent.stage.verify_runtime(arm,previous)
    guard=registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    controls=bind_registered_story_percent_guard(guard)(native.files(clean),new)
    assert controls["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(controls["source_bound_new_command_counts"].values())
    target.replace_file(stage.COMMON,old[stage.COMMON])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    w=stage.workflow
    digest=native.digest(arm[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    before,installed=[w.owned_entries(rom[stage.COMMON],arm,digest) for rom in (old,new)]
    assert {r.message_id for r,q in zip(before,installed,strict=True) if r.text!=q.text}==stage.EDITS.keys()
    ja=w.common_message_entries(clean.read_file(stage.COMMON),clean.read_file(stage.ARM))
    pending=base.load(stage.PENDING)["records"]
    assert len(pending)==276
    assert all(r["current_reference"]==w.reference(installed[r["message_ID"]]) and
               r["current_hex"]==installed[r["message_ID"]].text.hex() for r in pending)
    records=staged["records"]
    assert [r["message_ID"] for r in records]==list(range(27,50))
    for row in records:
        n=row["message_ID"]
        assert row["source_hex"]==ja[n].text.hex() and row["current_hex"]==before[n].text.hex()
        assert row["staged_hex"]==installed[n].text.hex()
        row["registered_reference"]=w.reference(installed[n])|dict(candidate_sha256=candidate)
        row["emulator_shortage_replay_observed"]=n==28
    review={k:staged[k] for k in ("translation_policy","target_locale","encoder","review_gates","records")}
    review.update(candidate_sha256=candidate,checked_story_format_guard=controls,new_contextual_credit=0,
        shared_storage_scope=base.load(parent.REVIEW)["shared_storage_scope"],direct_visual_review=viewed,
        observed_gameplay=playback|{"exact_port_menu_before_and_after":menus},
        source_and_native_dependency_proofs=staged["source_proofs"])
    validate_natural_dialogue_batch(review)
    return staged,review,{stage.COMMON:native.digest(new[stage.COMMON])}


publish=parent.program
readme=publish[publish.index('    (PACKAGE / "README.md").write_text'):publish.index('    base.save(PACKAGE / "checksums.json",')]
doc=publish[publish.index("    DOC.write_text"):publish.index("    prefix =")]
program=checked_text(publish,{
    'len(manifest["batches"]) == 915 and len(manifest["checks"]) == 250':
        'len(manifest["batches"]) == 916 and len(manifest["checks"]) == 251',
    "verified_deck_comments_predecessor":"verified_square_label_wording_predecessor",
    "square_label_wording":"departure_warnings",
    "owned_caption_records=[row":"owned_shared_records=[row",
    "target_ARM9_sha256=archives[stage.ARM]":"target_COMMON_sha256=archives[stage.COMMON]",
    "repository_tests=29, legacy_fixture_tests_skipped=0, reviewed_UI_labels=18":
        "repository_tests=49, legacy_fixture_tests_skipped=2, reviewed_UI_labels=0",
    "prose_revisions=0, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=16":
        "prose_revisions=5, spacing_revisions=0, wrap_only_revisions=0, justified_retentions=18",
    "text_display_revisions=2":"text_display_revisions=5",
    "ordinary_Lisbon_Square_captions_and_return=True":"initialized_Lisbon_crew_warning_and_return=True",
    "natural_activation=True, hardware=False":"natural_activation=False, hardware=False",
    "ARM9_sha256=archives[stage.ARM], MESFILE_sha256=previous['target_COMMON_sha256']":
        "ARM9_sha256=previous['target_ARM9_sha256'], MESFILE_sha256=archives[stage.COMMON]",
    "previously_localized_records=18, caption_revisions=2":"previously_localized_records=23",
    "    candidates.append(PRESERVED_FIRST_ROM)\n":"",
    "Preserve Square label ROM or reconstruction":"Preserve departure warning ROM or reconstruction",
    readme:"""    (PACKAGE / "README.md").write_text(f\"\"\"# Departure warnings test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Port warnings and the preceding cumulative fixes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
The candidate is available for acceptance testing.
\"\"\", encoding="utf-8", newline="\\n")
""",
    doc:"""    DOC.write_text(f\"\"\"# Port departure warnings

Reviewed the 23 clean Japanese records that cover the crew checks, repair and supply warnings, and the resupply offer. The five revisions improve the worker’s crew warning and the phrasing of four companion warnings. Eighteen individual retentions preserve the alternative voices, the distinction between no sailors and too few, and the resupply price substitution. [Exact review ledger](../{REVIEW.as_posix()})

All five changed messages passed native glyph, wrapping and one-page checks within the 228×48 window. A Lisbon replay used one crew-count byte in a disposable test session to activate the original shortage check. Two complete holds show the two revised lines. The Port menu after dismissal matches the menu before the warning pixel for pixel. The other revisions received offline checks. Hardware remains unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

Only the five reviewed COMMON slots change. The clean-input patch rebuilds the ROM byte for byte. Six startup holds, 24 protected name getters and 49 focused tests passed, with two optional older ROM fixture tests skipped. The dialogue tally remains 27,700 and the 276 pending shared references retain their positions and contents. [Candidate and patch](../{PACKAGE.as_posix()}/README.md)
\"\"\", encoding="utf-8", newline="\\n")
""",
})
env=parent.env|globals()
exec(compile(program,__file__+"::register","exec"),env)

if __name__=="__main__":
    env["main"]()
