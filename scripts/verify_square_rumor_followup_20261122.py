"""Verify the original Valencia and Syracuse rumor selection and complete glyph masks."""

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_square_rumor_followup_20261122 as stage
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as masks
from scripts import verify_story_literal_names_20261122 as sheets
from scripts.audit_captain_name_latin_20261119 import LABEL_COLOR,glyphs


base = stage.base
LIVE = stage.ROOT/"ordinary_dialogue.json"
SHEET = stage.ROOT/"regional_ordinary.png"


def verify():
    assert not LIVE.exists()
    stored = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] and stored["whole_parent_inverse"]
    rom = base.NdsImage.open(stage.ROM)
    font = GameAsciiFont.from_arm9(rom.read_file(stage.ARM))
    native = {row["message_ID"]:row for row in stored["records"]}
    evidence = {str(stage.PROOF):base.digest(stage.PROOF)}
    prior = base.load(stage.regional.OUTPUT)
    assert prior["actual_cold_boot_saved_gameplay"]
    evidence[str(stage.regional.OUTPUT)] = base.digest(stage.regional.OUTPUT)
    reports, pictures = {}, []
    for city,holds in stage.HOLDS.items():
        root = stage.WITNESSES/city
        paths = [root/p for p in ("capture/capture_report.json","requests.json","terminal.json")]
        report,trace,terminal = map(base.load,paths)
        events,_,end,_,donor = stage.regional.capture.schedule(city)
        assert report["ROM_sha256"] == terminal["ROM_sha256"] == candidate
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
        assert report["frames"] == end and report["scripted_input_schedule"] == events
        battery = report["battery_save_preloaded"]
        assert battery["copied_byte_exact_before_cold_boot"]
        assert battery["source_sha256"] == donor["source_sha256"] == base.digest(donor["source"])
        assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
        assert terminal["target_COMMON_calls"] == trace["source_requests"]
        assert all(base.digest(p)==sha for p,sha in terminal["evidence"].items())
        evidence.update({str(p):base.digest(p) for p in paths})
        frames = stage.regional.shots(report)
        checks = []
        last_panel = None
        for frame,key in holds:
            captured = frames[frame]
            assert base.digest(captured["path"])==captured["PNG_sha256"]
            im = stage.regional.captured(captured).convert("RGB")
            if key in stage.PROSE:
                original, = [r for r in prior["original_town_dialogue"][city] if r["message_ID"] == key]
                assert original["source_hex"] == native[key]["source_hex"]
                assert original["current_hex"] == native[key]["current_hex"]
                calls = [r for r in trace["source_requests"] if frame-149 <= r["frame"] <= frame]
                selected = [r for r in calls if r["message_ID"] == key]
                assert [r["PC"] for r in selected] == [0x0205528C,0x020534F4]
                assert selected[0]["frame"] == selected[1]["frame"]
                assert masks.mask_check(bytes.fromhex(native[key]["native_plane_hex"]),228,im), (city,frame,key)
                plate = glyphs(font,im,"Shopkeeper",(16,277),LABEL_COLOR,124)
                checks.append(dict(frame=captured,message_ID=key,nameplate=plate,selects=selected,
                                   native_mask_exact=True,earlier_capture_reference=original["capture"]))
                last_panel = im
            elif key == 51:
                assert any(r["message_ID"]==key and frame-149<=r["frame"]<=frame for r in trace["source_requests"])
                checked = stage.regional.body_mask(im,font,stage.regional.TEXT[key][0])
                glyphs(font,im,"Barkeep",(16,277),LABEL_COLOR,124)
                checks.append(dict(frame=captured,message_ID=key,control_body=checked))
            else:
                assert last_panel is not None and im.tobytes()!=last_panel.tobytes()
                checks.append(dict(frame=captured,transition_context=True))
            label = f"{city.title()} / COMMON {key}" if key else f"{city.title()} / following input"
            pictures.append((label,im))
        reports[city] = checks
    assert {r.get("message_ID") for rows in reports.values() for r in rows if r.get("native_mask_exact")} == {714,715}
    path,sha = sheets.make_sheet(SHEET,pictures)
    base.save(LIVE,dict(candidate_sha256=candidate,predecessor_sha256=stored["predecessor_sha256"],
        original_saved_gameplay=True,observed=reports,revised_gameplay_records=[714,715],
        revised_offline_only_records=[725],sheets={path:sha},evidence=evidence,hardware=False))
    print("Both revised Square panels have complete in-game glyphs and the original Shopkeeper nameplate.",flush=True)


if __name__=="__main__":
    verify()
