"""Register Rafael's complete Gerhard recruitment and training review."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace
import xml.etree.ElementTree as ET

from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from scripts import check_rafael_B84_training_gameplay_20261122 as gameplay
from scripts import register_north_sea_and_hodram_reconciliation_20261122 as parent
from scripts import replay_rafael_B84_training_20261122 as replay
from scripts import stage_rafael_B84_training_20261122 as stage
from scripts import verify_rafael_B84_training_20261122 as verification
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base,parent.native
ARM,COMMON=parent.ARM,parent.COMMON
guard_spec=parent.scope["guard_spec"]
bind_registered_story_percent_guard=parent.scope["bind_registered_story_percent_guard"]
PROFILE="all-routes-rafael-B84-training-v1-20261122"
ROOT=parent.ROOT.with_name("rafael_B84_training_registered_20261122")
ROM=ROOT/"Translation_DS_Rafael_Training_20261122_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=parent.PACKAGE.with_name("all_routes_editorial_20261122_rafael_B84_training_candidate")
VERIFY,PATCH=PACKAGE/"verification",PACKAGE/"translation.xdelta"
REVIEW,RELEASE=VERIFY/"registered_review.json",VERIFY/"registered_release_verification.json"
DOC=parent.DOC.with_name("editorial_rafael_B84_training_registered_20261122.md")
EVIDENCE,DISPLAY=stage.ROOT,stage.NATIVE
GLYPHS, FE = verification.GLYPH_PROOF,verification.FE_PROOF
MENU=stage.ROOT/"installed_choice_verification.json"
HISTORICAL_MENU=Path("translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json")
STARTUP,STARTUP_CAPTURE,QA=EVIDENCE/"own_startup_verification.json",stage.STARTUP_CAPTURE,EVIDENCE/"qa_focused.xml"
VISUAL=EVIDENCE/"visual_review.json"
live=SimpleNamespace(LIVE=gameplay.OUTPUT)
CHECKPOINT="Registered Rafael’s complete Gerhard recruitment and naval training review."
startup_scope=parent.startup_scope|dict(STARTUP=STARTUP,STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"]=FunctionType(parent.startup_scope["startup_proof"].__code__,startup_scope)


def native_count():
    glyphs,display=map(base.load,(GLYPHS,DISPLAY))
    assert glyphs["native_report_sha256"]==base.digest(DISPLAY)
    assert glyphs["candidate_sha256"]==display["candidate_sha256"]
    assert glyphs["complete_font_pixels"] and glyphs["exact_contact_sheet_pixels"]
    assert len(glyphs["pages"])==display["pages"]==9
    return display["pages"]


def observed_count():
    return base.load(live.LIVE)["observed_speech_pages"]


def sheets():
    rendered,fe,menu,played=map(base.load,(DISPLAY,FE,MENU,live.LIVE))
    return rendered["sheets"]+fe["sheets"]+[menu["sheet"]]+played["sheets"]


def original_choice_credits(records):
    historical = {row["id"]:row for row in base.load(HISTORICAL_MENU)["records"]
                  if row["block"]==84 and row["kind"]=="typed-choice-label"}
    known={}
    for row in records:
        if row["kind"]!="choice":
            continue
        slot,=row["variant_slots"]
        alias=f'SC0_B84_NATIVE_CHOICE_{row["source_command_offset"]}_{slot}'
        earlier=historical.pop(alias)
        assert earlier["source_index"]==slot
        assert earlier["source_command_offset"]==row["source_command_offset"]
        assert earlier["source_hex"]==labels(bytes.fromhex(row["source_command_hex"]))[slot].hex()
        known[row["id"]]=alias
    assert not historical and len(known)==5
    return dict(by_census_id=known,direct_keys=0,source_ledger_sha256=base.digest(HISTORICAL_MENU))


def verify(registry,previous,viewed):
    proof, rendered, fe, menu, played = map(base.load,(stage.PROOF,DISPLAY,FE,MENU,live.LIVE))
    candidate=base.digest(stage.ROM)
    assert candidate==base.digest(stage.REBUILT)
    assert all(x["candidate_sha256"]==candidate for x in (proof,rendered,fe,menu,played))
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==proof["predecessor_sha256"]
    assert rendered["stage_sha256"]==base.digest(stage.PROOF)
    assert all(base.digest(p)==sha for p,sha in proof["evidence"].items())
    assert viewed=={s["path"]:s["sha256"] for s in sheets()}
    assert all(base.digest(p)==sha for p,sha in viewed.items())
    assert native_count()==9 and observed_count()==15 and proof["relative_commands"]==20
    assert proof["exact_FE_continuations"]==2 and fe["complete_stored_page_count"]==4
    assert played["focused_original_excerpts"] and played["natural_trigger_unvisited"]
    assert played["native_FE_panels_observed"]==4
    assert [(o["selected"],o["response"]) for o in played["original_menu_choices"]]==[(0,"R0234"),(1,"R0327"),(1,"R0511")]
    assert all(o["executed_original_branch"] for o in played["original_menu_choices"])
    assert all(base.digest(p)==h for p,h in played["report_sha256"].items())
    assert menu["provider_proof_sha256"]==base.digest(verification.MENU_PROOF)
    suite,=ET.parse(QA).iter("testsuite")
    assert [int(suite.get(k,"0")) for k in ("tests","failures","errors","skipped")]==[17,0,0,0]

    clean,old,image=map(base.NdsImage.open,(native.CLEAN,parent.ROM,stage.ROM))
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]==proof["clean_sha256"]
    a,b=map(native.files,(old,image))
    assert a.keys()==b.keys() and {p for p in a if a[p]!=b[p]}=={stage.PATH}
    assert native.digest(b[ARM])==previous["target_ARM9_sha256"] and native.digest(b[COMMON])==previous["target_COMMON_sha256"]
    assert proof["archive_hashes"]=={stage.PATH:native.digest(b[stage.PATH])}
    image.replace_file(stage.PATH,a[stage.PATH])
    assert proof["whole_parent_inverse"] and bytes(image.rom.save())==parent.ROM.read_bytes()
    guard=registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    assert guard==guard_spec()
    checks=bind_registered_story_percent_guard(guard)(native.files(clean),b)
    assert checks==proof["source25"] and not any(checks["source_bound_new_command_counts"].values())
    startup_scope["startup_proof"](previous,candidate,b[ARM])

    bank=native.IlnkContainer.parse(b[stage.PATH])
    group,=proof["groups"]
    block=bank.blocks[84]
    assert native.digest(block)==group["after"]
    commands={key:c for c in group["commands"] for key in c["record_ids"]}
    continuations={c["retained_continuation_of"]:c for c in group["commands"] if c["retained_continuation_of"]}
    displays={r["id"]:r for r in rendered["records"]}
    records=[]
    for row in proof["editorial_records"]:
        ident=row["id"]
        c=commands[ident]
        at,raw=c["stored_offset"],bytes.fromhex(c["stored"])
        assert block[at:at+len(raw)]==raw
        if row["kind"]=="choice":
            count,start=count_and_base(raw)
            slot,=row["variant_slots"]
            assert slot<count
            body=labels(raw)[slot]
            offset=at+start+unpack_from("<H",raw,2+slot*2)[0]
            assert body.decode("ascii")==row["english"]
            if row["decision"]=="revision":
                assert c["stored"]==menu["exact_command_hex"] and at==menu["installed_offset"]
        else:
            offset=at+5
            body=raw[6:raw.index(0,6)]
            assert raw[5]==row["source_selector"]
            if row["decision"]=="revision":
                assert displays[ident]["exact_command_hex"]==raw.hex()
                assert " ".join(body.decode("ascii").split())==row["english"]
            else:
                assert c["stored"]==c["current"]
        registered=dict(candidate_sha256=candidate,file_path=stage.PATH,block=84,command_offset=at,offset=offset,
            exact_command_hex=raw.hex(),exact_body_hex=body.hex(),archive_sha256=proof["archive_hashes"][stage.PATH],
            block_sha256=group["after"])
        if ident in continuations:
            extra=continuations[ident]
            assert extra["stored"]==extra["current"]
            registered["unchanged_second_page"]=dict(command_offset=extra["stored_offset"],exact_command_hex=extra["stored"])
        records.append(row|dict(file_path=stage.PATH,block=84,registered_reference=registered,
            display_proof=displays.get(ident),review=row["review"]|dict(formatting=True),
            observed_focused=[o for o in played["observations"] if o["id"]==ident]))
    assert len(records)==131 and sum(r["decision"]=="revision" for r in records)==9
    result=dict(candidate_sha256=candidate,records=records,translation_policy="natural-dialogue-v2",target_locale="en-US",
        visual_review=viewed,focused_gameplay=played,verified_two_choice=menu,unchanged_FE=fe,
        checked_story_format_guard=checks,wording_revisions=8,choice_label_revisions=1,justified_retentions=122,
        historical_source_credit=original_choice_credits(records),full_editorial_goal_complete=False,hardware=False)
    return proof,result,{p:native.digest(b[p]) for p in (stage.PATH,ARM,COMMON)}


readme=parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build=checked_text(parent.build,{
    "len(batches) == 1065 and len(checks) == 400":"len(batches) == 1066 and len(checks) == 401",
    "previously_localized_records=74, contextual_records_revisited=74":"previously_localized_records=131, contextual_records_revisited=131",
    "prior_records_reviewed=74":"prior_records_reviewed=131",
    "prose_revisions=9":"prose_revisions=8",
    "justified_retentions=65, retained_choice_labels=0":"justified_retentions=122, retained_choice_labels=4",
    "choice_label_revisions=0":"choice_label_revisions=1",
    "changed_components=2":"changed_components=1",
    "focused_initialized_Rafael_and_Hodram=True":"focused_initialized_Rafael=True, original_menu_branch_cases=3",
    "DISPLAY, GLYPHS, args.visual_review,":"DISPLAY, GLYPHS, FE, MENU, verification.MENU_PROOF, args.visual_review,",
    '(source.parent.name + "_" + source.name) if source.name == "scenes.png" else source.name':
        '(source.parent.name + "_" + source.name) if source.parent.name == "retained_FE" else source.name',
    "(live.LIVE, DISPLAY, stage.PROOF, GLYPHS, stage.HISTORICAL)":"(live.LIVE, DISPLAY, stage.PROOF, GLYPHS, FE, MENU)",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's Gerhard recruitment and training candidate

The [testing ROM](../../{ROM.as_posix()}) contains eight speech revisions and a restored choice caption. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("north_sea_and_hodram_reconciliation","rafael_B84_training").replace(
    "verified_palace_eirene_pereira_london_predecessor","verified_north_sea_and_hodram_reconciliation_predecessor")
old_doc=parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit=checked_text(parent.commit,{
    "earlier = [live.ROM, live.HODRAM_ROM, FIRST_STAGE]":
        'earlier = [Path(base.load(replay.ROOT / name / "fixture.json")["path"]) for name in ("speech","pact_entry","lesson_entry")]',
    "Preserve the North Sea and Hodram candidate, predecessor and unique focused ROMs":
        "Preserve the Rafael B84 training candidate, predecessor and unique focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael’s Gerhard recruitment and naval training

The clean-Japanese review covers 131 texts with eight revised speeches, a revised choice and 122 individual retentions. Rafael can explicitly say they do not need to defeat Vels. The typed two-choice menu and all original destinations survive relocation. The three training captions and both two-page naval instructions are byte-exact. [Registered review](../{REVIEW.as_posix()})

All nine changed-speech layout variants passed exact font checks. Emulator fixtures verified 15 complete panels, including both original notice continuations, and used controller input to follow both Vels choices and the training lesson-only option into their original responses. Native checks also verified all 20 relative destinations and the original choice provider. Natural town activation and hardware were outside this batch. Startup and 17 focused regressions passed. [Testing candidate and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("north_sea_and_hodram_reconciliation","rafael_B84_training")
scope=parent.scope|globals()
for code in (build,commit):
    exec(compile(code,__file__+"::registered-training-release","exec"),scope)


if __name__=="__main__":
    scope["main"]()
