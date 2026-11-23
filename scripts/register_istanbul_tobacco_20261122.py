"""Register the two revised Istanbul replies after native and gameplay checks."""

from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree as ET

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import register_osaka_glass_20261122 as parent
from scripts import replay_istanbul_tobacco_20261122 as replay
from scripts import stage_istanbul_tobacco_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
PROFILE = "all-routes-istanbul-tobacco-followup-v1-20261122"
ROOT = parent.ROOT.with_name("istanbul_tobacco_registered_20261122")
ROM = ROOT / "Translation_DS_Istanbul_Tobacco_20261122_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261122_istanbul_tobacco_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_istanbul_tobacco_registered_20261122.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
live = SimpleNamespace(LIVE=replay.LIVE)
CHECKPOINT = "Registered two natural-dialogue corrections in Lil's Istanbul tobacco scene and verified Hodram's original Square activation."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup = FunctionType(parent.startup.__code__, parent.startup.__globals__ |
                       {"STARTUP": STARTUP, "STARTUP_CAPTURE": STARTUP_CAPTURE})


def native_count():
    return len(base.load(stage.PROOF)["native_pages"])


def observed_count():
    return len(base.load(replay.LIVE)["cases"]["2"]["sightings"]) + len(base.load(replay.NORMAL)["exact_complete_panels"])


def observed_names():
    return 14


def pages_saved():
    return 0


def verify(registry, previous, viewed):
    stored, draft, played, normal = map(base.load, (stage.PROOF, stage.MANUSCRIPT, replay.LIVE, replay.NORMAL))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == played["candidate_sha256"] == base.digest(stage.REBUILT)
    assert previous["candidate_sha256"] == stored["predecessor_sha256"] == normal["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["whole_parent_inverse"] and base.digest(stage.MANUSCRIPT) == stored["manuscript_sha256"]
    visual = base.load(VISUAL)
    assert visual["reviewed_candidate_sha256"] == candidate
    assert viewed == visual["sheets"] == (played["sheets"] | normal["sheets"] | {stored["sheet"]: stored["sheet_sha256"]})
    assert all(base.digest(path) == sha for path, sha in viewed.items())
    assert played["initialized_scenes"] and played["original_scene_commands"] and not played["natural_Istanbul_trigger"]
    assert not played["hardware"] and normal["natural_square_activation"] and not normal["hardware"]
    assert native_count() == 2 and observed_count() == 16
    suite, = ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]

    clean, source, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    before, after = map(native.files, (source,target))
    path = "/data/SC2.DK4"
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == set(stored["changed"]) == {path}
    assert native.digest(after[native.ARM]) == previous["target_ARM9_sha256"]
    assert native.digest(after["/COMMON/MESFILE.DK4"]) == previous["target_COMMON_sha256"]
    changed = stored["changed"][path]
    a,b = [native.IlnkContainer.parse(data) for data in (before[path],after[path])]
    assert [i for i,(x,y) in enumerate(zip(a.blocks,b.blocks,strict=True)) if x!=y] == [changed["block"]]
    assert native.digest(b.blocks[changed["block"]]) == changed["target_block"]
    assert native.digest(before[path]) == changed["before"] and native.digest(after[path]) == changed["after"]
    target.replace_file(path,before[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    controls = bind_registered_story_percent_guard(registry["profiles"][previous["profile"]]["source25_multiarchive_guard"])(
        native.files(clean),after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(controls["source_bound_new_command_counts"].values())
    startup(previous,candidate,after[native.ARM])

    holds = {r["id"]:r for r in played["cases"]["2"]["sightings"]}
    ordinary_holds = {r["id"]:r for r in normal["exact_complete_panels"]}
    assert {r["id"] for r in stored["native_pages"]} == {r["id"] for r in draft["records"] if r["decision"] == "revision"} <= set(holds)
    commands = {r["record_ids"][0]:r for r in changed["commands"] if r["record_ids"]}
    inventory, _, _ = native.scoped_inventory()
    for route,index in enumerate(stage.BLOCKS):
        archive = f"/data/SC{route}.DK4"
        block = native.IlnkContainer.parse(after[archive]).blocks[index]
        if route != 2:
            assert native.digest(block) == stored["original_town_entries"][route]["installed_block_sha256"]
        rows = [r for r in draft["records"] if r["route"] == route]
        assert len(rows) == 8
        for row in rows:
            ident = row["id"]
            if route == 2:
                command = commands[ident]
                raw = bytes.fromhex(command["stored"])
                offset = command["stored_offset"]
                assert raw[:6] == bytes.fromhex(command["source"])[:6]
                row["initialized_Lil_gameplay_hold"] = holds[ident]
            else:
                ref = row["prior_approved_reference"]
                offset = ref["command_offset"]
                command, = [c for c in inventory(after[native.ARM],block)[0] if c["offset"] == offset]
                raw = bytes.fromhex(command["whole_command_hex"])
                assert raw[5:raw.index(0,6)].hex() == row["current_hex"]
                if route == 1:
                    row["ordinary_Hodram_gameplay_hold"] = ordinary_holds[ident]
                else:
                    row["reused_display_evidence"] = str(stage.PRIOR)
            assert raw == block[offset:offset+len(raw)] and raw[5] == row["source_selector"]
            row["registered_reference"] = dict(candidate_sha256=candidate,file_path=archive,block=index,
                command_offset=offset,offset=offset+5,exact_stored_hex=raw[5:raw.index(0,6)].hex(),
                complete_preamble_hex=raw[:6].hex(),complete_command_hex=raw.hex())
            row["review"]["formatting"] = True

    draft.update(candidate_sha256=candidate,checked_story_format_guard=controls,direct_visual_review=viewed,
        focused_Lil_playback=str(replay.LIVE),ordinary_unchanged_Hodram_playback=str(replay.NORMAL),
        offline_native_preflight=str(DISPLAY),natural_Istanbul_trigger_in_Lil_route=False,
        unchanged_pending_records=276,historical_source_credit=dict(by_census_id={},direct_keys=32),
        full_editorial_goal_complete=False)
    validate_natural_dialogue_batch(draft)
    return stored,draft,{path:changed["after"]}


old_readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(parent.build,{
    "len(batches) == 1046 and len(checks) == 381": "len(batches) == 1047 and len(checks) == 382",
    "verified_kurushima_surrender_predecessor=predecessor": "verified_osaka_glass_predecessor=predecessor",
    "changed_components=2": "changed_components=1",
    "previously_localized_records=44, contextual_records_revisited=44": "previously_localized_records=32, contextual_records_revisited=32",
    "prior_records_reviewed=44": "prior_records_reviewed=32",
    "observed_Osaka_panels": "observed_Istanbul_panels",
    "justified_retentions=42": "justified_retentions=30",
    "initialized_Osaka_scenes=True": "initialized_Lil_scene=True, ordinary_Hodram_Square_on_exact_predecessor=True",
    "native_and_emulator_evidence_sha256={str(p):base.digest(p) for p in (live.LIVE, DISPLAY)}":
        "native_and_emulator_evidence_sha256={str(p):base.digest(p) for p in (live.LIVE, replay.NORMAL, stage.PROOF)}",
    "live.LIVE, DISPLAY, args.visual_review": "live.LIVE, replay.NORMAL, stage.MANUSCRIPT, args.visual_review",
    old_readme:'''    (PACKAGE / "README.md").write_text(f"""# Istanbul tobacco testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes two revised replies in Lil's Istanbul scene. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("osaka_glass","istanbul_tobacco").replace(
    "verified_istanbul_tobacco_predecessor","verified_osaka_glass_predecessor")
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    '    research = [Path(base.load(stage.ROOT / f"route{r}/fixture.json")["rom"]) for r in stage.CASES]':
        '    research = [Path(base.load(replay.ROOT / "route2/fixture.json")["rom"]),'
        ' stage.VOYAGE/"editorial/Istanbul_Tobacco_Lil_STAGED.nds",'
        ' stage.VOYAGE/"editorial/focused/route2/Istanbul_Lil_FOCUSED_ONLY.nds"]',
    "Preserve the Osaka Glass candidate, predecessor and focused ROMs": "Preserve the Istanbul candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Istanbul tobacco Square exchange

Reviewed eight turns across each of the four routes. Lil's sailor now says he hasn't had the chance to smoke and asks if the port worker really thinks he's the only one in town. The sailor's stammer and complete expression of interest stay together. Thirty lines retain their wording for individual reasons. [Exact source and English decisions](../{REVIEW.as_posix()})

Ordinary Hodram play reached August 12 through the Inn and triggered the original Square event. All eight panels, including the forecast, and the Square return passed. An initialized Lil replay verified the complete eight-panel exchange with the two revisions, nameplates, and the return from the original commands. Natural activation was observed on Hodram's unchanged route. Hardware remains untested. [Gameplay and native evidence](../{VERIFY.as_posix()})

Only Lil's Istanbul block changes. All 114 accepted layers, the ASCII right-bound correction, startup and 17 regressions passed. The clean-input patch reconstructs the candidate exactly. [Testing ROM and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("osaka_glass","istanbul_tobacco")
scope = parent.scope | globals()
for program in (build,commit):
    exec(compile(program,__file__+"::registered","exec"),scope)


if __name__ == "__main__":
    scope["main"]()

