"""Register Maria's early scene revisions after native and focused checks."""

from pathlib import Path

from scripts import register_hodram_B311_B324_20261122 as parent
from scripts import replay_maria_B18_B20_20261122 as live
from scripts import stage_maria_B18_B20_20261122 as writer
from scripts import verify_maria_B18_B20_20261122 as display
from scripts.source_locked_derivation_v5118 import checked_text
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET


base, native, workflow = parent.base, parent.native, parent.workflow
stage = SimpleNamespace(ROOT=writer.ROOT, ROM=writer.ROM, PROOF=writer.PROOF, OUTPUT=writer.MANUSCRIPT)
PROFILE = "all-routes-maria-B18-B20-v1-20261122"
ROOT = parent.ROOT.with_name("maria_B18_B20_registered_20261122")
ROM = ROOT / "Translation_DS_Maria_B18_B20_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_maria_B18_B20_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_maria_B18_B20_registered_20261122.md")
EVIDENCE = writer.ROOT
STARTUP, QA, STARTUP_CAPTURE = EVIDENCE/"own_startup_verification.json", EVIDENCE/"qa_passed.xml", EVIDENCE/"startup/capture/capture_report.json"
EARLIER = writer.FIRST_ROOT/"focused_gameplay/verified_gameplay.json"
CARRIED = EVIDENCE/"earlier_gameplay_binding.json"
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.scope["bind_registered_story_percent_guard"]
CHECKPOINT = ("Revisited 88 Maria records in Manuel's naval elegy and Aziza's mutiny, "
              "recruitment and retreat exchanges. The batch revises 43 and justifies 45 retentions.")


def native_count():
    return base.load(display.PROOF)["revised_speech_pages"]


def observed_count():
    return len(base.load(CARRIED)["representative_unique_ids"])


def pages_saved():
    return 0


def startup_check(previous, candidate, arm):
    original = parent.startup_reference.startup_check
    check = original.__globals__["checked_report"]
    bound = FunctionType(check.__code__, check.__globals__ | {"STARTUP_CAPTURE":STARTUP_CAPTURE})
    run = FunctionType(original.__code__, original.__globals__ |
                       {"STARTUP":STARTUP,"STARTUP_CAPTURE":STARTUP_CAPTURE,"checked_report":bound})
    return run(previous,candidate,arm)


def carry_gameplay(stored, rendered, playback):
    prior, first_commands = map(base.load,(EARLIER,writer.FIRST_ROOT/writer.PROOF.name))
    assert prior["candidate_sha256"] == first_commands["candidate_sha256"] == base.digest(writer.FIRST_ROOT/writer.ROM.name)
    assert prior["initialized_excerpts"] and not prior["natural_story_triggers_claimed"]
    def contents(proof):
        return {ident:cmd["stored"] for group in proof["groups"] for cmd in group["commands"] for ident in cmd["record_ids"]}
    before, after = map(contents,(first_commands,stored))
    current = set(playback["observed_ids"])
    assert current == set(live.PLAY_ORDER) and len(current) == playback["observed_speech_pages"] == 5
    assert set(writer.review.VISUAL_REFINEMENTS) <= current
    usable = [ident for ident in prior["observed_ids"] if ident not in current and before[ident] == after[ident]]
    assert len(usable) == 23 and rendered["exact_predecessor_pages_reused"] == 41
    assert all(base.digest(s["path"]) == s["sha256"] for s in prior["sheets"])
    evidence = dict(previous_replay=str(EARLIER), previous_replay_sha256=base.digest(EARLIER),
        latest_candidate_sha256=stored["candidate_sha256"], latest_directly_observed_ids=sorted(current),
        earlier_unchanged_commands={ident:after[ident] for ident in usable},
        representative_unique_ids=sorted(current | set(usable)), previous_sheets=prior["sheets"])
    if CARRIED.exists():
        assert base.load(CARRIED) == evidence
    else:
        base.save(CARRIED,evidence)
    return evidence


def verify(registry, previous, viewed):
    stored,draft,rendered,playback = map(base.load,(stage.PROOF,stage.OUTPUT,display.PROOF,live.LIVE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == rendered["candidate_sha256"] == playback["candidate_sha256"]
    assert stored["predecessor_sha256"] == draft["previous_sha256"] == previous["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and stored["manuscript_sha256"] == base.digest(stage.OUTPUT)
    assert draft["source_packet_sha256"] == base.digest(draft["source_packet"])
    assert rendered["offline_native_only"] and rendered["revised_speech_pages"] == 43 and rendered["alternate_name_pages"] == 3
    assert playback["initialized_excerpts"] and not playback["natural_story_triggers_claimed"]
    assert playback["report_sha256"] == base.digest(live.REPORT)
    carried = carry_gameplay(stored,rendered,playback)
    sheets = rendered["sheets"] + playback["sheets"] + carried["previous_sheets"]
    assert viewed == {s["path"]:s["sha256"] for s in sheets}
    assert all(base.digest(path) == sha for path,sha in viewed.items())
    suite = ET.parse(QA).getroot().find("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")] == [17,0,0,0]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    assert (EVIDENCE/"clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()

    clean,before,after = map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    first, final = map(native.files,(before,after))
    archive = writer.review.ARCHIVE
    assert first.keys() == final.keys() and {path for path in first if first[path] != final[path]} == {archive}
    unmodified = first[archive]
    before_blocks, blocks = [native.IlnkContainer.parse(raw).blocks for raw in (unmodified,final[archive])]
    touched = [i for i,(a,b) in enumerate(zip(before_blocks,blocks,strict=True)) if a != b]
    assert touched == stored["changed_blocks"][archive] == list(writer.BLOCKS[3])
    for group in stored["groups"]:
        n = group["block"]
        assert native.digest(before_blocks[n]) == group["before"] and native.digest(blocks[n]) == group["after"]
    after.replace_file(archive,unmodified)
    assert bytes(after.rom.save()) == parent.ROM.read_bytes()
    after.replace_file(archive,final[archive])
    assert bytes(after.rom.save()) == stage.ROM.read_bytes()
    arm = final[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(final["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    assert registry["profiles"][previous["profile"]]["source25_multiarchive_guard"] == guard_spec()
    controls = bind_registered_story_percent_guard(guard_spec())(native.files(clean),final)
    assert controls == stored["source25"] and controls["total_exact_source_bound_relocated_leading25_count"] == 7
    startup_check(previous,candidate,arm)
    print("Verified the Maria candidate's startup, clean-input patch, gameplay and stored scripts.",flush=True)
    references = {row["id"]:row for row in rendered["records"]}
    assert len(references) == len(draft["records"]) == 88 and len(draft["current_names_and_roles"]) == 11
    assert draft["findings"] == {"wording":43,"retention":45}
    archive_sha = native.digest(final[archive])
    for row in draft["records"]:
        ident, block = row["id"], row["block"]
        info = references.pop(ident)
        cmd, = info["stored_pages"]
        raw, span = bytes.fromhex(cmd["stored"]), bytes.fromhex(info["body_hex"])
        at, offset = cmd["stored_offset"], info["body_offset"]
        assert info["block"] == block and blocks[block][at:at+len(raw)] == raw
        assert offset == at+5 and raw[5:5+len(span)] == span
        assert span[0] == row["source_selector"] and " ".join(span[1:].decode("ascii").split()) == row["english"]
        assert (cmd["current"] != cmd["stored"]) == (row["decision"] == "revision")
        row["registered_reference"] = dict(file_path=archive,block=block,archive_sha256=archive_sha,
            block_sha256=native.digest(blocks[block]),candidate_sha256=candidate,
            command_offset=at,offset=offset,exact_stored_hex=span.hex(),exact_command_hex=raw.hex())
        assert all(row["review"][key] for key in ("source","context","localization","naturalness"))
        row["review"]["formatting"] = True
        row["observed_in_final_initialized_excerpt"] = ident in carried["latest_directly_observed_ids"]
        row["observed_earlier_with_same_command"] = ident in carried["earlier_unchanged_commands"]
        row["native_formatting_evidence"] = info
    assert not references
    draft.update(candidate_sha256=candidate,status="registered",direct_visual_review=viewed,
        historical_source_credit=dict(by_census_id={},direct_keys=88),new_contextual_credit=0,
        checked_story_format_guard=controls,shared_payload_and_lookup_exact=True,
        native_preview_evidence=str(display.PROOF),initialized_replay_evidence=str(live.LIVE),
        seeded_gameplay_binding=str(CARRIED),full_editorial_goal_complete=False)
    return stored,draft,{archive:archive_sha}


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):
                       parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1036 and len(checks) == 371": "len(batches) == 1037 and len(checks) == 372",
    "profile.update(verified_hodram_B292_B310_predecessor=predecessor": "profile.update(verified_hodram_B311_B324_predecessor=predecessor",
    "live.PROOF, display.PROOF, names.PROOF, args.visual_review": "live.LIVE, display.PROOF, CARRIED, args.visual_review",
    "base.digest(live.PROOF)": "base.digest(live.LIVE)",
    'filename = "refreshed_" + source.name if source.parent == display.ROOT else source.name':
        'filename = "refreshed_" + source.name if source.parent in (display.ROOT, live.ROOT) else source.name',
    "previously_localized_records=590, contextual_records_revisited=404, contextual_decisions_reused=186":
        "previously_localized_records=88, contextual_records_revisited=88, contextual_decisions_reused=0",
    'two_page_count_explanations=sum(len(t)==3 for t in base.load(live.PROOF)["page_transitions"].values())': "two_page_count_explanations=0",
    "prior_records_reviewed=404, contextual_decisions_reused=186, observed_Hodram_panels":
        "prior_records_reviewed=88, contextual_decisions_reused=0, observed_Maria_panels",
    "contextual_nameplate_retentions=13": "contextual_nameplate_retentions=11",
    "actual_menu_samples=15, actual_style_objects=len(live.STYLE_OBJECTS)": "actual_menu_samples=0, actual_style_objects=0",
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Maria's early naval and Aziza exchanges

The [testing ROM](../../{ROM.as_posix()}) includes the review and accepted cumulative layers. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
})
build = build.replace("hodram_B311_B324","maria_B18_B20").replace("verified_maria_B18_B20_predecessor","verified_hodram_B311_B324_predecessor")
build = build.replace("initialized_Hodram_B311_B324","initialized_Maria_B18_B20").replace("prose_revisions=79","prose_revisions=43")
build = build.replace("justified_retentions=324","justified_retentions=45").replace("wrap_only_revisions=1","wrap_only_revisions=0")

note = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    '    assert plan["registry_before"] == base.digest(base.REGISTRY) == base.digest(registry_backup)\n'
    '    assert plan["ledger_before"] == base.digest(base.LEDGER) == base.digest(ledger_backup)':
        '''    assert plan["registry_before"] == base.digest(registry_backup)
    assert plan["ledger_before"] == base.digest(ledger_backup)
    registry, ledger = base.digest(base.REGISTRY), base.digest(base.LEDGER)
    before = (plan["registry_before"], plan["ledger_before"])
    after = (plan["registry_after"], plan["ledger_after"])
    assert (registry, ledger) in (before, after)''',
    '    try:\n        copy_in_place(registry_next, base.REGISTRY)\n'
    '        update_ledger_in_place(ledger_backup.read_bytes(), ledger_next.read_bytes())':
        '''    try:
        if (registry, ledger) == before:
            copy_in_place(registry_next, base.REGISTRY)
            update_ledger_in_place(ledger_backup.read_bytes(), ledger_next.read_bytes())''',

    note: '''    DOC.write_text(f"""# Maria's early naval and Aziza exchanges

Reviewed 88 records in Manuel's elegy, Aziza's mutiny and her decision to leave piracy. The review revises 43 turns and justifies 45 retentions across 11 named speakers and roles. The first line of the mutiny keeps Aziza's startled reaction and sets up Angel's echo of "next time." The scene keeps the Bloodstained Shamshir and the original dynamic fleet name. [Exact source and current evidence](../{REVIEW.as_posix()})

All 43 revised pages and three alternate-name layouts passed native and visual review. The earlier emulator replay covered 25 pages. Five final pages were replayed after the refinements, and exact command bindings carry 23 additional earlier pages. The original event triggers and hardware are still unvisited. [Verification](../{VERIFY.as_posix()})

Startup and 17 regression checks passed. The cumulative build carries 114 accepted layers and the ASCII right-bound correction. The clean-input patch rebuilt the ROM byte for byte. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
    "Hodram_B311_B324_FOCUSED_ONLY.nds":"Maria_B18_B20_FOCUSED_ONLY.nds",
    "Preserve the final Hodram range candidate":"Preserve the Maria early scene candidate",
}).replace("hodram_B311_B324","maria_B18_B20").replace("B311_B324_staged","B18_B20_staged").replace('base.load(live.PROOF)','base.load(live.LIVE)')

scope = parent.scope | globals()
for source in (build,commit):
    exec(compile(source,__file__+"::registered-Maria", "exec"),scope)

if __name__ == "__main__":
    scope["main"]()

