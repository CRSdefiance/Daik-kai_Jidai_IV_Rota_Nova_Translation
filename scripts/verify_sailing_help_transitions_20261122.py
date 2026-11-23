"""Qualify both visible Sailing Help prompt directions on the current candidate."""

from pathlib import Path
from struct import unpack_from

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import checkpoint_gallery_options_legacy_20261114 as earlier
from scripts import observe_sailing_help_transitions_20261122 as seen


base, current = seen.current.base, seen.current
ROOT = seen.ROOT/"sailing_help"
OUTPUT = seen.ROOT/"sailing_help_state_transitions.json"


def main():
    assert not OUTPUT.exists()
    terminal, requests, report, release = map(base.load,(
        ROOT/"terminal.json",ROOT/"requests.json",ROOT/"capture/capture_report.json",current.RELEASE))
    assert base.digest(current.ROM)==release["candidate_sha256"]==terminal["ROM_sha256"]==report["ROM_sha256"]
    events, frames, end, _, donor = seen.schedule("sailing_help")
    assert report["cold_boot"] and not report["savestate_loaded"] and not donor
    assert report["scripted_input_schedule"]==events and report["frames"]==end
    assert not report["callback_errors"] and not report.get("battery_save_preloaded")
    assert requests["all_host_slots_restored_and_core_file_exact"] and not requests["errors"] and not requests["mismatches"]
    assert requests["source_requests"]==terminal["target_COMMON_calls"]==[] and terminal["COMMON_requests"]==0
    assert all(base.digest(path)==expected for path,expected in terminal["evidence"].items())

    clean, image = map(base.NdsImage.open,(current.native.CLEAN,current.ROM))
    source,arm = [rom.read_file(current.native.ARM) for rom in (clean,image)]
    assert current.native.digest(arm)==release["target_ARM9_sha256"]
    start,pointer = 0x13880C,0x3FD4C
    assert source[0x3FCD0:0x3FD50]==arm[0x3FCD0:0x3FD50]
    assert unpack_from("<I",arm,pointer)[0]==0x0213880C
    slot = [data[start:start+56].split(b"\0",1)[0] for data in (source,arm)]
    original = slot[0].decode("cp932")
    fmt = slot[1].decode("ascii")
    assert fmt=="Sailing Help is %s. Change to %s?" and original.count("%s")==2
    font = GameAsciiFont.from_arm9(arm)
    captures = {row["frame"]:row for row in report["frames_captured"]}
    questions = ((3800,"On","Off"),(4600,"Off","On"),(5400,"On","Off"))
    pages = []
    for frame,now,proposed in questions:
        shot = captures[frame]
        pixels = earlier.font_mask(earlier.screen(shot),font,fmt % (now,proposed),16,297,(16,296,237,350),(0,8,0))
        pages.append(dict(frame=frame,displayed=fmt % (now,proposed),complete_glyph_pixels=pixels,capture=shot))
    restored = [captures[frame] for frame in (4200,5000,5800,6200)]
    assert all(base.digest(shot["path"])==shot["PNG_sha256"] for shot in restored)

    # Compare the menu rectangles after each response, without treating the animated background as text.
    menu = (82,255,173,323)
    images = [earlier.screen(shot).crop(menu).tobytes() for shot in restored[:3]]
    assert images[0]==images[1]==images[2]
    base.save(OUTPUT,dict(candidate_sha256=release["candidate_sha256"],observed_pages=pages,
        selector_menu_returns=restored[:3],title_return=restored[-1],native_common_request_count=0,
        original_ARM9_controller_exact=True, source_slot={"offset":start,"bytes":56,"hex":slot[0].hex(),"Japanese":original},
        current_slot={"offset":start,"bytes":56,"hex":slot[1].hex(),"English":fmt},
        decision="retention",localization_note="Sailing Help matches the menu and the full question distinguishes the current and proposed states.",
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
        visibility="Native emulator cold boot, ordinary title inputs, no copied save.",
        scope="The normal Options screen draws the independent ARM9 string. Potential alternate callers of stored COMMON 333 remain open.",
        audio_options_existing_receipt=str(earlier.OPTIONS),new_editorial_credit=0,
        evidence=terminal["evidence"]))
    print("Verified both Sailing Help substitutions, two applied changes, cancellation, and return to title.")


if __name__=="__main__":
    main()

