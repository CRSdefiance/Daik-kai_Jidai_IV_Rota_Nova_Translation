"""Bind the current DS setup, sound and default names to their reviewed owners."""

from pathlib import Path
from struct import unpack_from

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_early_setup_current_20261122 as live
from scripts import reconcile_shared_display_20261121 as shared
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_rafael_setup_labels_20261115 as labels
from scripts import register_setup_confirmation_prose_20261115 as confirmation
from scripts import register_sound_bgm_titles_v1 as sound
from scripts import verify_rafael_setup_labels_20261115 as setup_verify
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask


base, current = live.current.base, live.current
ROOT = live.ROOT
BOOK = shared.OUTPUT.parent
OUTPUT = BOOK / "early_setup_current_20261122_v1.json"
PREVIOUS = confirmation.stage.ROOT
LEGACY = BOOK / "legacy_dialogue_review_20261115_v1.json"
DEFAULT_NAMES = BOOK / "default_actor_names_current_20261120_v1.json"
IDS = (*range(100,108), *range(330,334))


def capture(case, candidate):
    root = ROOT/case
    report_path, requests_path, terminal_path = (root/"capture/capture_report.json", root/"requests.json",
        root/"terminal.json")
    report, native, terminal = map(base.load,(report_path,requests_path,terminal_path))
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded")
    assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
    assert all(base.digest(path)==sha for path,sha in terminal["evidence"].items())
    calls = native["source_requests"]
    assert not native["errors"] and not native["mismatches"] and native["callbacks"] == len(calls)
    assert native["all_host_slots_restored_and_core_file_exact"]
    assert terminal["COMMON_requests"] == len(calls) and not terminal["caption_calls"]
    assert all(row["message_ID"] not in IDS for row in calls)
    holds = {row["frame"]:row for row in report["frames_captured"]}
    assert all(base.digest(row["path"]) == row["PNG_sha256"] for row in holds.values())
    return report, calls, holds, terminal_path


def range_ref(data, span):
    raw = data[span[0]:span[1]]
    assert len(raw) == span[1] - span[0]
    return dict(start=span[0], end=span[1], sha256=current.native.digest(raw))


def name_bindings(release, clean_arm):
    old = base.load(DEFAULT_NAMES)
    rows = old["source_and_current_default_name_fields"]
    assert old["original_default_names_exact_for_207_actors"] and len(rows) == 207
    ctx = RegisteredRuntime(current.RELEASE,release["own_registered_startup"],captain=3)
    result = names.current_getters(ctx)["rows"]
    earlier_ledger = Path(old["original_default_editorial_ledger"])
    assert base.digest(earlier_ledger)==old["original_default_editorial_ledger_sha256"]
    original_decisions = {r["actor_ID"]:r for r in base.load(earlier_ledger)["records"]}
    assert len(original_decisions)==13
    exact_fields, installed = [], []
    evidence = {}
    for i,row in enumerate(rows):
        assert row["actor_ID"] == i
        decision = row["completed_default_decision"]
        if decision is None:
            approved = original_decisions[i]
            assert all(approved["review"].values())
            assert approved["english"]==row["progressive_nameplate"]
            assert approved["catalogue_english"]==row["full_catalogue"]
            precedent = str(earlier_ledger),approved["id"],old["original_default_editorial_ledger_sha256"]
        elif "precedent" in decision:
            assert (decision["english"],decision["catalogue_english"])==(row["progressive_nameplate"],row["full_catalogue"])
            precedent = decision["precedent"],decision["record"],decision["precedent_sha256"]
        else:
            assert all(decision["review"].values())
            assert (decision["progressive"],decision["catalogue"])==(row["progressive_nameplate"],row["full_catalogue"])
            precedent = decision["path"],decision["record_id"],decision["sha256"]
        evidence[precedent[0]] = precedent[2]
        short,long = result[2*i:2*i+2]
        assert short["actor_ID"] == long["actor_ID"] == i
        assert [short["text"],long["text"]] == [row["progressive_nameplate"],row["full_catalogue"]]
        assert all(r["text"].isascii() and r["text"].isprintable() for r in (short,long))
        for index, prior in enumerate(row["exact_fields"]):
            off = names.TABLE+i*32+index*4
            assert off == prior["offset"]
            for image, prev in ((clean_arm,prior["clean"]),(ctx.raw,prior["current"])):
                ptr, = unpack_from("<I",image,off)
                assert ptr == (prev["pointer"] if prev else 0)
                if prev:
                    expected = bytes.fromhex(prev["hex"])+b"\0"
                    assert image[ptr-names.BASE:ptr-names.BASE+len(expected)] == expected
            exact_fields.append((i,off))
        installed.append(dict(actor_ID=i,progressive=short["text"],catalogue=long["text"],
            previous_review_path=precedent[0],previous_review_record=precedent[1]))
    assert len(exact_fields)==621
    assert all(base.digest(path)==sha for path,sha in evidence.items())
    return dict(earlier_review=str(DEFAULT_NAMES),earlier_review_sha256=base.digest(DEFAULT_NAMES),
        checked_clean_and_current_field_slots=len(exact_fields), original_default_getter_cases=len(result),
        joined_names_or_custom_actors_tested=False, runtime=ctx.receipt(), editorial_precedent_hashes=evidence, outputs=installed,
        original_getter_execution_offline=True, no_new_editorial_credit=True)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"]
    assert base.digest(current.MANIFEST)==release["manifest_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(current.native.CLEAN)==release["clean_input_sha256"]
    assert base.load(current.ROOT/"drive_latest_build_receipt.json")["sha256"]==candidate
    clean,active = map(base.NdsImage.open,(current.native.CLEAN,current.ROM))
    clean_arm,arm = (img.read_file(shared.ARM) for img in (clean,active))
    assert current.native.digest(arm)==release["target_ARM9_sha256"]
    assert current.native.digest(active.read_file(shared.COMMON))==release["target_COMMON_sha256"]
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON),clean_arm)
    installed = shared.entries(active)

    stored = {row["message_ID"]:row for row in base.load(shared.OUTPUT)["records"]}
    prose = {row["message_ID"]:row for row in base.load(LEGACY)["records"]}
    entries = []
    for n in IDS:
        a,b = source[n],installed[n]
        row = prose[n]
        assert (a.text.hex(),b.text.hex())==(row["source_hex"],row["current_hex"])
        assert (shared.workflow.reference(a),shared.workflow.reference(b))==(
            stored[n]["source_reference"],stored[n]["current_reference"])
        assert a.text.decode("cp932")==row["Japanese"] and not row["review"]["formatting"]
        ent = {k:row[k] for k in ("id","context","source_meaning","localization_note","source_hex",
            "current_hex","Japanese","previous_English","english","decision","preserved_format_arguments","review")}
        entries.append(ent | dict(source_reference=stored[n]["source_reference"],
            current_reference=stored[n]["current_reference"],requests_in_checked_replays=0,
            global_owner_status="open"))
    assert len(stored)==276

    report, setup_calls, setup_frames, setup_terminal = capture("setup",candidate)
    option_report, option_calls, option_frames, option_terminal = capture("options",candidate)
    assert [(r["frame"],r["message_ID"],r["PC"]) for r in setup_calls]==[
        (f,120,pc) for f in (1800,6003) for pc in (0x0205528C,0x020534F4)]
    assert [(r["frame"],r["message_ID"],r["PC"]) for r in option_calls]==[
        (f,3251,pc) for f in (2810,3210,4010,4810,5610) for pc in (0x0205528C,0x020534F4)]
    # The reviewed original confirmation replay used the same editor actions.
    original_capture = PREVIOUS/"after/capture/capture_report.json"
    original = base.load(original_capture)
    previous_live = base.load(confirmation.VERIFY/"gameplay_verification.json")
    assert original["ROM_sha256"] == previous_live["candidate_sha256"]
    assert base.digest(original_capture)==previous_live["evidence"][str(original_capture)]
    assert original["scripted_input_schedule"]==report["scripted_input_schedule"]
    reference = {row["frame"]:row for row in original["frames_captured"]}
    exact = [setup_frames[n] for n in (1800,2200,2591,2991,3391,3791,4191,4591,4991,5391,5791,6191,6591)]
    assert all(row["framebuffer_sha256"]==reference[row["frame"]]["framebuffer_sha256"] for row in exact)
    font = GameAsciiFont.from_arm9(arm)
    load_screen = lambda ref: Image.open(ref["path"]).convert("RGB")
    headed = []
    for frame,text in setup_verify.EDIT_FIELDS.items():
        headed.append(dict(frame=frame,**find_mask(font,text.ljust(16),load_screen(setup_frames[frame]),setup_verify.HEAD)))
    dates = [dict(frame=frame,**find_mask(font,date.ljust(12),load_screen(setup_frames[frame]),setup_verify.DATE))
        for frame,date in ((2200,"3/5"),(5791,"4/13"),(6591,"4/13"))]
    mask = complete_mask(font,"Is everything OK?",load_screen(setup_frames[6191]),16,333,(0,8,0))

    active = []
    for n,path in ((120,confirmation.REVIEW),(3251,sound.REVIEW)):
        doc = base.load(path)
        row, = [r for r in doc["records"] if r["message_ID"]==n]
        assert all(row["review"].values()) and source[n].text.hex()==row["source_hex"]
        assert shared.workflow.reference(source[n])==row["source_reference"]
        registered = row.get("deployed_hex") or row["registered_reference"]["exact_stored_hex"]
        assert installed[n].text.hex()==registered
        active.append(row | dict(earlier_registered_review=str(path),earlier_registered_review_sha256=base.digest(path),
            checkpoint_decision="retention",current_reference=shared.workflow.reference(installed[n]),
            current_hex=installed[n].text.hex(),active_current_calls=4 if n==120 else 10))
    validate_natural_dialogue_batch(base.load(confirmation.REVIEW) | {"records":active})
    track = active[1]
    x0,_ = track["native_center"]
    expected = {(x0+i*5+gx,259+gy) for i,ch in enumerate(track["english"])
                for gx in range(6) for gy in range(11) if font.decode(ch).getpixel((gx,gy))}
    title_holds = []
    for frame in (3000,3400,3800,4200,5000,5400,5800):
        img = load_screen(option_frames[frame])
        actual = {(x,y) for x in range(128) for y in range(258,271) if img.getpixel((x,y))==(230,230,230)}
        assert actual==expected, (frame,len(actual),len(expected))
        title_holds.append(dict(frame=frame,ink_pixels=len(actual),capture=option_frames[frame]))

    owned = []
    for row in base.load(labels.REVIEW)["records"]:
        before, after = row["source_reference"], row["registered_reference"]
        start, count, pointer = before["ARM9_offset"],before["allocation"],before["pointer_field"]
        assert unpack_from("<I",clean_arm,pointer)==unpack_from("<I",arm,pointer)==(0x02000000+start,)
        assert (clean_arm[start:start+count].hex(),arm[start:start+count].hex())==(before["raw_hex"],after["raw_hex"])
        owned.append(dict(id=row["id"],english=row["english"],source_reference=before,
            current_reference=range_ref(arm,(start,start+count)),review=row["review"],
            approved_localization_reason=row["localization_note"]))
    assert len(owned)==8
    result = dict(candidate_sha256=candidate,clean_input_sha256=release["clean_input_sha256"],
        release=str(current.RELEASE), ordinary_current_emulator=True, hardware=False, new_contextual_credit=0,
        active_retained_records=active, current_registered_editor_fields=owned, other_consumers_still_open=entries,
        legacy_and_other_shared_leads_still_tracked=len(stored), full_goal_complete=False,
        character_editor=dict(terminal=str(setup_terminal),matches_prior_framebuffers=exact,heading_masks=headed,
            birth_date_masks=dates,consumed_setup_calls=setup_calls,confirmation_mask=mask,cancel_returns_to_editor=True),
        sound_setup=dict(terminal=str(option_terminal),consumed_setup_calls=option_calls,complete_current_title_masks=title_holds,
            audio_output_assessed=False,returned_to_options=option_frames[6200]),
        default_actor_names=name_bindings(release,clean_arm),
        reviewed_sheets={str(p):base.digest(p) for p in (ROOT/"setup_observed.png",ROOT/"options_observed.png")})
    base.save(OUTPUT,result)
    print(f"Recorded {len(exact)} matching setup screens, {len(title_holds)} exact track-title holds, "
          f"{len(entries)} scoped legacy records and 414 default name getter matches.",flush=True)


if __name__ == "__main__":
    main()

