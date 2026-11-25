"""Record current Gallery message retentions and the observed Options owners."""

from inspect import getsource
from pathlib import Path
from struct import pack

from PIL import Image, ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_gallery_empty_common_20261114 as gallery
from scripts import observe_options_legacy_common_20261114 as options
from scripts import register_diplomatic_outcomes_v2 as ledger_workflow
from scripts.checkpoint_market_shared_consumers_20261114 import ARM, COMMON, font_mask
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text


base, current = gallery.base, gallery.current
CHECKPOINT = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
REVIEW = CHECKPOINT / "gallery_empty_collections_reviewed_20261114_v1.json"
OPTIONS = CHECKPOINT / "options_legacy_observed_consumers_20261114_v1.json"
LEGACY = CHECKPOINT / "legacy_common_35_checkpoint_v1.json"
FAMILY = "gallery_empty_collection_notices_20261114"
GATES = ("source","context","localization","naturalness","formatting")
NOTICES = {
    98: (4300, "You haven't acquired any items.",
        "There are no previously obtained items in the collection.",
        "The notice follows an Items selection. The second-person wording describes what the player has obtained and doesn’t imply the game contains no items."),
    99: (5500, "You haven't discovered any ruins.",
        "The collection contains no previously discovered historical sites.",
        "The notice answers the Ruins selection using the same term as the menu. It leaves the absence specific to this save and mirrors the Items notice."),
}


def verify_report(module, case, release):
    folder = module.ROOT / case
    terminal, trace, report = [base.load(folder / filename) for filename in (
        "terminal.json","requests.json","capture/capture_report.json")]
    events, frames, end, _, donor = module.schedule(case)
    assert terminal["ROM_sha256"] == report["ROM_sha256"] == release["candidate_sha256"]
    assert terminal["completed_frames"] == report["frames"] == end
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == events
    assert bool(donor) == bool(report.get("battery_save_preloaded"))
    if donor:
        assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert all(base.digest(path)==expected for path,expected in terminal["evidence"].items())
    return terminal, trace["source_requests"], {row["frame"]:row for row in report["frames_captured"] if row["frame"] in frames}


def screen(row):
    assert base.digest(row["path"]) == row["PNG_sha256"]
    with Image.open(row["path"]) as image:
        assert image.size == (256,384)
        return image.convert("RGB")


def verify_options(release, source, current_text, clean_arm, arm, font):
    terminal, calls, frames = verify_report(options,"options",release)
    assert terminal["COMMON_requests"] == len(calls) == 10 and not terminal["target_COMMON_calls"]
    assert {row["message_ID"] for row in calls} == {3251}
    sheet = options.ROOT/"options/options_review.png"
    assert base.digest(sheet) == "9246a631cc9c25f6c20d51f6650eae9e023404e73b32c3d1a0bc8aae613995be"
    fmt = 0x13880C
    width = 56
    ja, en = (data[fmt:fmt+width].split(b"\0")[0] for data in (clean_arm,arm))
    assert en == b"Sailing Help is %s. Change to %s?"
    assert all(data[0x3FD4C:0x3FD50]==pack("<I",0x0213880C) for data in (clean_arm,arm))
    assert clean_arm[0x3FCD0:0x3FD50] == arm[0x3FCD0:0x3FD50]
    confirmation = "Sailing Help is On. Change to Off?"
    exact_ink = font_mask(screen(frames[7400]),font,confirmation,16,297,(16,296,237,350),(0,8,0))
    sound_captures = [3000,3400,3800,4200,4600,5000,5400,5800,6200]
    for start, middle, end, bounds in ((3000,3400,5800,(24,320,103,338)),(3000,4200,5000,(152,320,231,338))):
        normal, reduced, restored = [screen(frames[frame]).crop(bounds) for frame in (start,middle,end)]
        assert ImageChops.difference(normal,reduced).getbbox()
        assert ImageChops.difference(normal,restored).getbbox() is None
    pending = []
    for ident in sorted(options.FOCUS):
        s,c = source[ident],current_text[ident]
        pending.append(dict(message_ID=ident,source_reference=reference(s),current_reference=reference(c),
            Japanese=s.text.decode("cp932"),stored_English=c.text.decode("cp932"),
            source_hex=s.text.hex(),current_hex=c.text.hex(),
            other_callers_pending=True,requests_in_tested_options_paths=[]))
    return dict(candidate_sha256=release["candidate_sha256"], checked_pending_legacy_keys=pending, observed_requests=calls,
        sound_setup=dict(bgm_and_sfx_meters_reduced_and_restored=True,program_inputs_visited=["Sound Setup","L","R","A","B"],
                         captures=[frames[n] for n in sound_captures]),
        sailing_help=dict(clean_source=ja.decode("cp932"),current_fmt=en.decode("ascii"),
            exact_clean_fmt_hex=ja.hex(),exact_current_fmt_hex=en.hex(),ARM9_slot_offset=fmt,
            source_and_current_pointer_field=0x3FD4C,pointer_value=0x0213880C,
            verified_unchanged_preparation_start=0x3FCD0,actual_text=confirmation,glyph_pixels=exact_ink,
            shown=frames[7400],cancel=frames[7800],title_return=frames[8200]),
        viewed_sheet=str(sheet),viewed_sheet_sha256=base.digest(sheet), new_editorial_credit=0,
        full_goal_complete=False, trace_evidence=terminal["evidence"])


def update_ledger(ledger, records, release, scope):
    old = ledger["records_editorially_completed"]
    revised = ledger["records_revised_and_integrated"]
    retained = ledger["retained_wordings_editorially_completed"]
    stock = getsource(ledger_workflow.update_ledger)
    start = stock.index("    ledger['current_integrated_candidate'].update(")
    end = stock.index("    ledger[FAMILY] = ",start)
    source = checked_text(stock,{
        stock[start:end]: "    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']\n",
        "diplomatic-and-scheme-outcome-notices": "gallery-empty-collection-notices",
        "Thirty-four diplomacy and scheme outcomes are registered.": "The two Gallery empty-collection notices are reviewed.",
        "== 25985": f"== {old+len(records)}", "== 15438": f"== {revised}", "== 10547": f"== {retained+len(records)}",
        "str(VERIFICATION / LIVE_VERIFICATION.name)": "str(REVIEW)",
    })
    env = vars(ledger_workflow) | dict(TOTAL=len(records),REVISED=0,RETAINED=len(records),PREVIOUS_TOTAL=old,
        FAMILY=FAMILY,REVIEW=REVIEW,RELEASE=current.RELEASE)
    exec(compile(source,__file__+"::same-ledger-owner-and-retention-credit-rules","exec"),env)
    env["update_ledger"](ledger, records, release, scope)


def main():
    assert not REVIEW.exists() and not OPTIONS.exists()
    release = base.load(current.RELEASE)
    clean_path = current.stage.CLEAN
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(clean_path) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.MANIFEST) == release["manifest_sha256"]
    assert base.digest(current.PATCH) == release["patch_sha256"]
    clean,rom = map(base.NdsImage.open,(clean_path,current.ROM))
    clean_arm,arm = [obj.read_file(ARM) for obj in (clean,rom)]
    font = GameAsciiFont.from_arm9(arm)
    assert current.assets.edit.digest(arm) == release["target_ARM9_sha256"]
    common = rom.read_file(COMMON)
    assert current.assets.edit.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(COMMON),clean_arm)
    active = owned_entries(common,arm,current.assets.edit.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    legacy = {row["message_ID"]:row for row in base.load(LEGACY)["records"]}
    terminal,calls,frames = verify_report(gallery,"gallery_empty",release)
    assert len(calls) == terminal["COMMON_requests"] == 4 and terminal["target_COMMON_calls"] == calls
    gallery_rows = []
    for (ident,(at,english,meaning,note)),lookup,copy in zip(NOTICES.items(), calls[::2], calls[1::2],strict=True):
        assert [lookup["PC"],copy["PC"]] == [0x0205528C,0x020534F4]
        assert lookup["message_ID"] == copy["message_ID"] == ident
        assert lookup["caller_LR"] == copy["caller_LR"] == 0x020546CC
        assert lookup["frame"] == copy["frame"] and 0 < at - lookup["frame"] < 300
        ja,en = source[ident],active[ident]
        assert ja.text.hex() == legacy[ident]["clean_hex"]
        assert en.text.hex() == legacy[ident]["current_hex"]
        assert en.text.decode("ascii").strip() == english
        assert b"%" not in ja.text+en.text
        showing = frames[at]
        ink = font_mask(screen(showing),font,english,16,297,(16,296,237,349),(0,8,0))
        collection = "Items" if ident == 98 else "Ruins"
        gallery_rows.append(dict(id=f"COMMON_MESSAGE_{ident}",message_ID=ident,speaker="Game notice",file_path=COMMON,
            english=english,decision="retention",source_meaning=meaning,localization_note=note,
            context=f"The title Gallery player opens {collection} with no collection entries, dismisses the notice with A, and returns to the Gallery.",
            review=dict.fromkeys(GATES,True),source_Japanese=ja.text.decode("cp932"),
            source_reference=reference(ja),current_reference=reference(en),
            source_hex=ja.text.hex(),current_hex=en.text.hex(),
            registered_reference=reference(en) | {"candidate_sha256":release["candidate_sha256"],"exact_stored_hex":en.text.hex()},
            original_native_requests=[lookup,copy],actual_gameplay=showing,complete_glyph_mask_pixels=ink,new_credit=1))
    option_evidence = verify_options(release,source,active,clean_arm,arm,font)
    scope = dict(actual_emulator=True, hardware=False, completely_observed_notice_IDs=[98,99],
        ordinary_save_copy=True, synthetic_unlock=False, full_mask_check=True)
    batch = dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=list(GATES),records=gallery_rows,candidate_sha256=release["candidate_sha256"],
        exact_existing_release=str(current.RELEASE),actual_verification_scope=scope,
        evidence=terminal["evidence"],rom_change_needed=False)
    validate_natural_dialogue_batch(batch)
    before = base.digest(base.LEDGER)
    ledger = base.load(base.LEDGER)
    assert ledger["current_integrated_candidate"]["sha256"] == release["candidate_sha256"]
    base.save(REVIEW,batch)
    base.save(OPTIONS,option_evidence)
    update_ledger(ledger,gallery_rows,release,scope)
    node = ledger["current_integrated_candidate"]
    refreshed = {}
    for route in range(4):
        key = f"SC{route}"
        digest = current.assets.edit.digest(rom.read_file(f"/data/{key}.DK4"))
        if digest != node[key+"_sha256"]:
            refreshed[key] = {"previous":node[key+"_sha256"],"verified":digest}
            node[key+"_sha256"] = digest
    history = {row["message_ID"] for row in legacy.values()} - {98,99,336}
    assert len(history) == 32
    ledger["pending_shared_consumer_checkpoint_20261114"] = dict(
        remaining_legacy_keys=sorted(history),remaining_promotional_and_scene_keys=245,
        remaining_total=277,options_scope_review=str(OPTIONS),candidate_sha256=release["candidate_sha256"],
        source_review=str(REVIEW), verified_candidate_archive_hash_refresh=refreshed,full_goal_complete=False)
    assert base.digest(base.LEDGER) == before
    current.archive_file(base.LEDGER.read_bytes(), gallery.ROOT/"editorial_ledger_before_gallery_empty.json.gz")
    base.replace_checked(base.LEDGER,encode_ledger(ledger))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.PATCH) == release["patch_sha256"]
    print(f"Verified both complete live Gallery notice masks. {ledger['records_editorially_completed']} credited and 277 shared keys still open.")


if __name__ == "__main__":
    main()

