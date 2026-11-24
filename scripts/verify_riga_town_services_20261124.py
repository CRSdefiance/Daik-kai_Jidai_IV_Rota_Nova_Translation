"""Bind Riga's ordinary Palace and Inn exchange to the clean and installed records."""

import json

from PIL import Image, ImageDraw

from scripts import observe_riga_town_services_20261124 as play
from scripts import verify_nagasaki_town_services_20261124 as tools
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write

panels = tools.panels
OUT = tools.OUT.with_name("riga_town_services_current_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 8800
RECORDS = (
    (4800, 1154, "King", ("Bergstrom",), ("Ah, Bergstrom! I hear you want", "to help defend our city."),
     "The ruler addresses the captain directly and describes the contribution as support for his city's defense.", None),
    (5600, 1160, "King", (), ("Hmm. That's an admirable gesture.", "Very commendable."),
     "The King admires the captain's spirit, then praises him directly. The current reply describes the gesture twice.",
     "Hmm. You've shown admirable spirit. I commend you."),
    (7200, 63, "Innkeeper", (), ("Welcome! Come in.",),
     "The warm invitation reads naturally before the lodging choices open.", None),
    (8000, 1177, "Innkeeper", (), ("That'll be 1 gold coin.",),
     "The singular coin is the actual price. The short statement leaves the confirmation buttons to ask for the decision.", None),
    (8400, 1178, "Innkeeper", (), ("Sleep well!",),
     "The brief goodnight follows acceptance of the quoted one-night charge.", None),
)


def main():
    current = play.current
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    paths = [play.ROOT / p for p in ("capture/capture_report.json", "trace/requests.json",
                                    "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"] == release["candidate_sha256"]
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    assert terminal["total_frames"] == capture["frames"] == journal["last_command_frame"] == END
    assert all(digest(path) == sha for path, sha in terminal["evidence"].items())
    assert not trace["mismatches"] and not trace["errors"] and trace["all_host_slots_restored_and_core_file_exact"]
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    commands = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert commands[:len(play.OPENING)] == list(play.OPENING) and commands[-1] == {"stop": True}
    assert commands == [r["command"] for r in journal["commands_received"]]
    assert all(r["validation_passed"] for r in journal["commands_received"])

    got = trace["source_requests"]
    assert got == terminal["common_requests"] and len(got) == 2 * len(RECORDS)
    frames = panels.shots(capture, "_navigation.png")
    screens = {f: panels.picture(row) for f, row in frames.items()}
    before, after = (NdsImage.open(p) for p in (CLEAN, current.ROM))
    clean_arm, arm = (image.read_file(current.ARM) for image in (before, after))
    source = tools.common_message_entries(before.read_file(current.COMMON), clean_arm)
    installed = tools.common_rows(after.read_file(current.COMMON), arm)
    font = tools.GameAsciiFont.from_arm9(arm)
    rows = []
    for (frame, key, speaker, args, lines, reason, draft), (getter, copier) in zip(RECORDS, zip(got[::2], got[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < frame - getter["frame"] < 400
        ja, en = source[key], installed[key]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(args)
        expanded = (en.text % tuple(a.encode("ascii") for a in args)).decode("ascii")
        assert expanded.split() == " ".join(lines).split()
        seen = dict(frame=frame, glyph_pixels=panels.exact_body(font, lines, screens[frame]),
                    nameplate=panels.nameplate(font, speaker, screens[frame]), requests=[getter, copier], capture=frames[frame])
        current_ref = panels.text_reference(en) | dict(exact_hex=en.text.hex())
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker=speaker,
                         context="Riga Military Investment" if key > 1100 and key < 1177 else "Riga Inn one-night stay",
                         clean_Japanese=ja.text.decode("cp932"), english=en.text.decode("ascii").strip(), args=args,
                         source_reference=panels.text_reference(ja) | dict(exact_hex=ja.text.hex()),
                         current_reference=current_ref, installed_reference=current_ref, observed=seen, actual_lines=lines,
                         decision="revision proposed" if draft else "retention", proposed_English=draft,
                         localization_note=reason, review=dict.fromkeys(GATES, True) | (dict(formatting=False) if draft else {})))

    status = []
    for frame, coins, share, day in ((3200, 44552, 20, 9), (6000, 43452, 21, 10), (8800, 43451, 21, 11)):
        parts = [(str(coins), (55, 346, 138, 370)), (str(share), (95, 91, 150, 115)),
                 (str(day), (119, 330, 149, 347))]
        masks = [panels.find_mask(font, text, screens[frame], area) for text, area in parts]
        status.append(dict(frame=frame, funds=coins, share_percent=share, day=day, masks=masks))
    quote = panels.find_mask(font, "1100", screens[5200], (145, 327, 190, 347))
    choices = [panels.find_mask(font, choice, screens[8000], box) for choice, box in
               (("No", (118, 360, 165, 377)), ("Yes", (188, 360, 235, 377)))]
    assert status[0]["funds"] - status[1]["funds"] == 1100 and status[1]["funds"] - status[2]["funds"] == 1
    selected = ((4800, "King's greeting"), (5600, "King's reply"), (7200, "Innkeeper's greeting"),
                (8000, "One-gold quote"), (8400, "Goodnight"), (8800, "Next day"))
    sheet = Image.new("RGB", (1024, 720), "#263238")
    labels = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(selected):
        x, y = (i % 2) * 512, (i // 2) * 240
        labels.text((x + 4, y + 4), label, fill="white")
        sheet.paste(screens[frame].crop((0, 274, 256, 384)).resize((512, 220), Image.Resampling.NEAREST), (x, y + 20))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
                    release=reference(current.RELEASE), donor=reference(donor["source"]), dialogue_records=rows,
                    verified_status=status, unit_investment_quote=quote, inn_confirmation_choices=choices,
                    controller=reference(play.CONTROLLER), evidence=list(map(reference, paths)), sheet=reference(SHEET),
                    new_editorial_credit=0, ROM_changed=False))
    print("Verified five Riga Palace and Inn holds, the 1,100-gold investment, and the one-night charge.")


if __name__ == "__main__":
    main()