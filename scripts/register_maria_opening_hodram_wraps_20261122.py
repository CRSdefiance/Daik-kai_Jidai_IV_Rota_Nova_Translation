"""Register Maria's opening pass and the three Hodram phrase repairs."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET

from scripts import register_maria_B18_B20_20261122 as parent
from scripts import replay_hodram_wraps_mixed_20261122 as hodram
from scripts import replay_maria_opening_mixed_20261122 as live
from scripts import stage_maria_opening_hodram_wraps_20261122 as writer
from scripts import verify_maria_opening_hodram_wraps_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text


base,native,workflow=parent.base,parent.native,parent.workflow
stage=SimpleNamespace(ROOT=writer.ROOT,ROM=writer.ROM,OUTPUT=writer.MANUSCRIPT,PROOF=writer.PROOF)
PROFILE="all-routes-maria-opening-hodram-wraps-v1-20261122"
ROOT=parent.ROOT.with_name("maria_opening_hodram_wraps_registered_20261122")
ROM=ROOT/"Translation_DS_Maria_Opening_Hodram_Wraps_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_opening_hodram_wraps_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_maria_opening_hodram_wraps_registered_20261122.md")
EVIDENCE=writer.ROOT
STARTUP,QA,STARTUP_CAPTURE=EVIDENCE/"own_startup_verification.json",EVIDENCE/"qa_passed.xml",EVIDENCE/"startup/capture/capture_report.json"
guard_spec=parent.guard_spec
bind_registered_story_percent_guard=parent.bind_registered_story_percent_guard
CHECKPOINT=("Revisited Maria's first 101 dialogue records and repaired three earlier Hodram wraps. "
            "The pass revises 43 Maria records, justifies 58 retentions and carries 67 exact prior Hodram decisions.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"] + len(base.load(hodram.PROOF)["holds"])


def observed_names():
    return len(base.load(stage.OUTPUT)["Maria_names_and_roles"])


pages_saved = parent.pages_saved
startup_check=FunctionType(parent.startup_check.__code__,parent.startup_check.__globals__ |
    {"parent":parent.parent,"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE})


def verify(registry,previous,viewed):
    stored,draft,rendered,maria_play,hodram_play = map(base.load,(stage.PROOF,stage.OUTPUT,display.PROOF,live.LIVE,hodram.PROOF))
    candidate=base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==rendered["candidate_sha256"]==maria_play["candidate_sha256"]==hodram_play["candidate_sha256"]
    assert stored["predecessor_sha256"]==draft["previous_sha256"]==previous["candidate_sha256"]==base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"]==base.digest(stage.OUTPUT)
    assert draft["source_packet_sha256"]==base.digest(draft["source_packet"])
    assert rendered["offline_native_only"] and rendered["stage_proof_sha256"]==base.digest(stage.PROOF)
    assert all(maria_play[tag] for tag in ("initialized_excerpts","observed_speech_pages"))
    assert not maria_play["natural_story_triggers_claimed"] and not hodram_play["natural_activation"]
    assert hodram_play["exact_native_glyph_matches"] and not hodram_play["hardware_verified"]
    assert maria_play["report_sha256"]==base.digest(live.REPORT)
    assert set(maria_play["observed_ids"])==set(live.PLAY_ORDER)
    assert all(base.digest(path)==value for path,value in hodram_play["evidence"].items())
    assert {"DK4_MES_B312_R0010","DK4_MES_B318_R0125","DK4_MES_B324_R0144"}<=set(hodram_play["observed_ids"])
    sheets=rendered["sheets"]+maria_play["sheets"]+hodram_play["sheets"]
    assert viewed=={s["path"]:s["sha256"] for s in sheets}
    assert all(base.digest(path)==value for path,value in viewed.items())
    settings=rendered["exact_shared_prompt_consumer"]
    assert base.digest(settings["path"])==settings["sha256"]
    suite=ET.parse(QA).getroot().find("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")]==[17,0,0,0]
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    assert (EVIDENCE/"clean_rebuilt.nds").read_bytes()==stage.ROM.read_bytes()

    clean,before,after=map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    first,final=map(native.files,(before,after))
    changed={path for path in first if first[path]!=final[path]}
    assert first.keys()==final.keys() and changed=={"/data/SC1.DK4","/data/SC3.DK4"}
    block_groups={(g["file_path"],g["block"]):g for g in stored["groups"]}
    banks,archive_hashes={},{}
    for path in sorted(changed):
        a,b=[native.IlnkContainer.parse(value).blocks for value in (first[path],final[path])]
        diffs=[i for i,(old,new) in enumerate(zip(a,b,strict=True)) if old!=new]
        assert diffs==stored["changed_blocks"][path]
        for (archive,block),group in block_groups.items():
            if path==archive:
                assert native.digest(a[block])==group["before"] and native.digest(b[block])==group["after"]
        after.replace_file(path,first[path])
        banks[path]=b
        archive_hashes[path]=native.digest(final[path])
    assert bytes(after.rom.save())==parent.ROM.read_bytes()
    for path in changed:
        after.replace_file(path,final[path])
    assert bytes(after.rom.save())==stage.ROM.read_bytes()
    arm=final[native.ARM]
    assert native.digest(arm)==previous["target_ARM9_sha256"]
    assert native.digest(final["/COMMON/MESFILE.DK4"])==previous["target_COMMON_sha256"]
    assert registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]==guard_spec()
    controls=bind_registered_story_percent_guard(guard_spec())(native.files(clean),final)
    assert controls==stored["source25"] and controls["total_exact_source_bound_relocated_leading25_count"]==7
    startup_check(previous,candidate,arm)
    print("Verified startup, clean-input patch, both replays, and two changed story archives.",flush=True)

    references={(r["route"],r["id"]):r for r in rendered["records"]}
    assert len(references)==len(draft["records"])==171
    assert draft["findings"]=={"wording":45,"wrap-only":1,"retention":125}
    assert draft["contextual_records_revisited"]==104 and draft["contextual_decisions_reused"]==67
    observed={1:set(hodram_play["observed_ids"]),3:set(maria_play["observed_ids"])}
    for row in draft["records"]:
        ident,block,path,route=[row[k] for k in ("id","block","file_path","route")]
        context=references.pop((route,ident))
        cmd,=context["stored_pages"]
        raw,span=bytes.fromhex(cmd["stored"]),bytes.fromhex(context["body_hex"])
        at,offset=cmd["stored_offset"],context["body_offset"]
        body=banks[path][block]
        assert context["block"]==block and body[at:at+len(raw)]==raw and body[offset:offset+len(span)]==span
        assert bool(context["layouts"])==(row["decision"]=="revision")
        if row["kind"]=="progressive":
            assert span[0]==row["source_selector"] and " ".join(span[1:].decode("ascii").split())==row["english"]
        if row.get("decision_carried"):
            assert span.hex()==row["previous_registered_reference"]["exact_stored_hex"]
        row["registered_reference"]=dict(file_path=path,block=block,archive_sha256=archive_hashes[path],
            block_sha256=native.digest(body),candidate_sha256=candidate,command_offset=at,offset=offset,
            exact_stored_hex=span.hex(),exact_command_hex=raw.hex())
        assert all(row["review"][key] for key in ("source","context","localization","naturalness"))
        row["review"]["formatting"]=True
        row["observed_in_initialized_excerpt"]=ident in observed[route]
        row["native_formatting_evidence"]=context
    assert not references
    draft.update(candidate_sha256=candidate,status="registered",direct_visual_review=viewed,
        historical_source_credit=dict(by_census_id={},direct_keys=171),new_contextual_credit=0,
        checked_story_format_guard=controls,shared_payload_and_lookup_exact=True,
        native_preview_evidence=str(display.PROOF),Maria_replay=str(live.LIVE),Hodram_replay=str(hodram.PROOF),
        shared_settings_evidence=settings,full_editorial_goal_complete=False)
    return stored,draft,archive_hashes


readme=parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                    parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    "len(batches) == 1037 and len(checks) == 372":"len(batches) == 1038 and len(checks) == 373",
    "verified_hodram_B311_B324_predecessor=predecessor":"verified_maria_B18_B20_predecessor=predecessor",
    "live.LIVE, display.PROOF, CARRIED, args.visual_review":"live.LIVE, hodram.PROOF, display.PROOF, args.visual_review",
    'filename = "refreshed_" + source.name if source.parent in (display.ROOT, live.ROOT) else source.name':
        'filename = source.parent.name + "_" + source.name if source in (live.LIVE,hodram.PROOF) else source.name',
    "native_and_emulator_evidence_sha256=base.digest(live.LIVE),":
        "native_and_emulator_evidence_sha256=base.digest(live.LIVE), Hodram_emulator_evidence_sha256=base.digest(hodram.PROOF),",
    "previously_localized_records=88, contextual_records_revisited=88, contextual_decisions_reused=0":
        "previously_localized_records=171, contextual_records_revisited=104, contextual_decisions_reused=67",
    "prior_records_reviewed=88, contextual_decisions_reused=0, observed_Maria_panels":
        "prior_records_reviewed=104, contextual_decisions_reused=67, observed_route_panels",
    "contextual_nameplate_retentions=11":"contextual_nameplate_retentions=observed_names()",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Maria's opening and Hodram phrase repairs

The [testing ROM](../../{ROM.as_posix()}) includes the checked opening scenes, the wrap repairs and earlier cumulative changes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
})
build=build.replace("maria_B18_B20","maria_opening_hodram_wraps").replace(
    "verified_maria_opening_hodram_wraps_predecessor","verified_maria_B18_B20_predecessor")
build=build.replace("initialized_Maria_B18_B20","initialized_Maria_opening_and_Hodram_wraps").replace(
    "prose_revisions=43","prose_revisions=45").replace("justified_retentions=45","justified_retentions=58").replace(
    "wrap_only_revisions=0","wrap_only_revisions=1")
note=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
pin=parent.commit[parent.commit.index("    earlier = sorted"):parent.commit.index("    for path in (ROM")]
commit=checked_text(parent.commit,{
    pin:'''    earlier = [stage.ROM]
    research = [live.ROM, hodram.ROOT / "Hodram_Wraps_FOCUSED_ONLY.nds"]
''',
    "Preserve the Maria early scene candidate":"Preserve the mixed-route candidate",
    note:'''    DOC.write_text(f"""# Maria's opening and Hodram phrase repairs

Reviewed 101 Maria records across the opening Proof of Conquest discussion, the naval confrontations, and Lil and Hodram's exchanges. The pass revises 43 and justifies 58 retentions. Kurushima now offers to surrender as the Japanese says. The changes preserve the difference between Maria's offer of reassurance and her firmer order to keep watch. The batch repairs three earlier Hodram phrase breaks and carries 67 exact decisions from their surrounding conversations. [Exact source, prior English and registered records](../{REVIEW.as_posix()})

The native renderer checked {native_count()} changed pages plus alternate-name layouts. Focused emulator excerpts verified {observed_count()} pages across the two routes. The ordinary Options run also verified both Sailing Help directions through the independently stored prompt. Original story triggers, alternate COMMON callers and hardware remain unvisited. [Native and emulator evidence](../{VERIFY.as_posix()})

Startup and 17 regression checks passed. All 114 accepted layers and the ASCII right-bound correction are carried forward. The clean-input patch reconstructs the candidate byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("maria_B18_B20","maria_opening_hodram_wraps")

scope=parent.scope|globals()
for program in (build,commit):
    exec(compile(program,__file__+"::mixed-registered-checkpoint","exec"),scope)


if __name__=="__main__":
    scope["main"]()

