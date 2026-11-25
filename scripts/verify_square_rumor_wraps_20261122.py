"""Check both revised wraps on the original running Square portrait consumer."""

from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_square_rumor_wraps_20261122 as stage
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as masks
from scripts import verify_story_literal_names_20261122 as sheets
from scripts.audit_captain_name_latin_20261119 import LABEL_COLOR,glyphs
from scripts.verify_captain_biographies_v1 import captured


base,native = stage.base,stage.native
LIVE = stage.ROOT/"focused_rumors.json"
SHEET = stage.ROOT/"focused_square_wraps.png"


def snapshot(report,key,frame):
    item, = [r for r in report[key] if r["frame"]==frame]
    raw = Path(item["path"]).read_bytes()
    assert item["read_only_export"] and len(raw)==item["bytes"]==0x400000
    assert native.digest(raw)==item["sha256"]
    return raw,item


def verify():
    assert not LIVE.exists()
    stored = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"] and stored["whole_parent_inverse"]
    image = base.NdsImage.open(stage.ROM)
    font = GameAsciiFont.from_arm9(image.read_file(stage.ARM))
    banks = native.IlnkContainer.parse(image.read_file(stage.COMMON)).blocks
    rows = {r["message_ID"]:r for r in stored["records"]}
    evidence = {str(stage.PROOF):base.digest(stage.PROOF)}
    cases,pictures = {},[]
    historical,old,donor = stage.play.history(0)
    for region in (1,4):
        n = 709+region
        row = rows[n]
        path = stage.FOCUSED/f"region{region}"/"capture/capture_report.json"
        terminal_path = path.parent.parent/"terminal.json"
        report,terminal = map(base.load,(path,terminal_path))
        assert report["ROM_sha256"]==candidate and report["frames"]==old["frames"]
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert report["scripted_input_schedule"]==old["scripted_input_schedule"]
        assert terminal["original_save_unchanged"] and terminal["history_sha256"]==base.digest(historical)
        assert terminal["report_sha256"]==base.digest(path)
        assert terminal["donor_sha256"]==base.digest(donor)
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        mark, = report[stage.play.FIXTURE_RECEIPT]
        assert mark["synthetic_regional_rumor_fixture"] and mark["expected_native_rumor_message"]==n
        assert mark["first_nine_original_random4_results"] == [3]*9
        assert mark["original_native_getters_and_selector_all_verified"] and mark["all_other_code_and_RAM_bytes_unchanged"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_") and k!=stage.play.FIXTURE_RECEIPT)
        before,old_ram = snapshot(report,"read_only_pause_RAM_snapshots",5800)
        after,new_ram = snapshot(report,"read_only_capture_RAM_snapshots",5900)
        assert native.digest(before)==mark["before_RAM_sha256"]
        initial = bytearray(before)
        for change in mark["changes"]:
            at=change["address"]-stage.BASE
            assert initial[at]==change["before"]
            initial[at]=change["after"]
        assert native.digest(initial)==mark["after_RAM_sha256"]
        block = banks[row["registered_reference"]["block"]]
        offset = after.find(block)
        assert offset>=0 and after.find(block,offset+1)<0
        frames = report["frames_captured"]
        observed = {frame:next(f for f in frames if f["frame"]==frame) for frame in stage.FRAMES}
        panels = {frame:captured(shot).convert("RGB") for frame,shot in observed.items()}
        display = panels[5900]
        assert masks.mask_check(bytes.fromhex(row["native_plane_hex"]),228,display)
        title = glyphs(font,display,"Shopkeeper",(16,277),LABEL_COLOR,124)
        assert panels[6050].tobytes()!=display.tobytes()
        for frame in (5600,5900,6050,6250):
            pictures.append((f"Region {region} / COMMON {n}" if frame==5900 else f"Region {region} / frame {frame}",panels[frame]))
        for proof in observed.values():
            assert base.digest(proof["path"])==proof["PNG_sha256"]
            evidence[proof["path"]]=proof["PNG_sha256"]
        evidence.update({str(p):base.digest(p) for p in (path,terminal_path,historical)})
        for proof in (old_ram,new_ram):
            evidence[proof["path"]]=proof["sha256"]
        cases[region]=dict(message_ID=n,report=str(path),frames=list(observed.values()),before_RAM=old_ram,held_RAM=new_ram,
            original_game_selected=n,complete_body_mask=True,nameplate=title,exact_live_block_sha256=native.digest(block),
            live_block_address=stage.BASE+offset,fixture=mark)
    path,sha=sheets.make_sheet(SHEET,pictures)
    base.save(LIVE,dict(candidate_sha256=candidate,predecessor_sha256=stored["predecessor_sha256"],
        focused_gameplay=True,natural_activation=False,hardware=False,cases=cases,sheets={path:sha},evidence=evidence))
    print("Both complete revised rumor pages and their Shopkeeper nameplates match in focused emulator play.",flush=True)


if __name__=="__main__":
    verify()
