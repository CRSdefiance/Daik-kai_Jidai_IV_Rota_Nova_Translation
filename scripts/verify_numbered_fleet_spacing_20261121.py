"""Verify the separated fleet name in both live map text surfaces."""
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_numbered_fleet_spacing_20261121 as replay


build, base = replay.build, replay.base
PROOF = replay.ROOT / "verified_map.json"
SHEET = replay.ROOT / "fleet_header_and_marker.png"


def glyph_mask(text, ascii_font, kanji, mapping):
    x = 0
    ideal = set()
    for char in text:
        if char.isascii():
            glyph = ascii_font.decode(char)
            ideal.update((x + j, y) for y in range(11) for j in range(6) if glyph.getpixel((j, y)))
            x += 6
        else:
            index = mapping.index(int.from_bytes(char.encode("cp932"), "big"))
            cell = kanji[index * 22:(index + 1) * 22]
            ideal.update((x + j, y - 1) for y in range(11) for j in range(11)
                         if cell[y * 2 + j // 8] & (0x80 >> (j % 8)))
            x += 12
    return ideal, x


def check(im, box, color, label, font):
    l, t, r, b = box
    seen = {(x, y) for x in range(l,r) for y in range(t,b) if im.getpixel((x,y)) == color}
    ideal, width = glyph_mask(label, *font)
    ox = min(x for x,_ in seen) - min(x for x,_ in ideal)
    oy = min(y for _,y in seen) - min(y for _,y in ideal)
    assert seen == {(x + ox,y + oy) for x,y in ideal}, (label, box, len(seen), len(ideal))
    assert l <= ox < ox + width <= r and width <= 192
    return dict(label=label, exact_mask_pixels=len(seen), origin=[ox,oy], layout_width=width)


def main():
    assert not PROOF.exists()
    staged = base.load(build.PROOF)
    original = build.play.ROOT / "capture/capture_report.json"
    assert base.digest(original) == staged["evidence"][str(original)]
    prior, changed = map(base.load, (original,replay.REPORT))
    assert prior["ROM_sha256"] == staged["predecessor_sha256"]
    assert changed["ROM_sha256"] == staged["candidate_sha256"] == base.digest(build.ROM)
    assert changed["cold_boot"] and not changed["savestate_loaded"] and not changed["callback_errors"]
    assert changed["frames"] == prior["frames"] == 5960
    assert not any(value for key,value in changed.items() if key.startswith("synthetic_"))
    assert changed["scripted_input_schedule"] == prior["scripted_input_schedule"]
    for key in ("source","source_sha256","copied_byte_exact_before_cold_boot"):
        assert changed["battery_save_preloaded"][key] == prior["battery_save_preloaded"][key]
    image = base.NdsImage.open(build.ROM)
    arm, kanji = (image.read_file(path) for path in (build.native.ARM, "/GRP/KANJI.FNT"))
    font = GameAsciiFont.from_arm9(arm), kanji, unpack_from("<3340H", arm,0x125EC4)
    shots, panels = [], []
    for report, suffix in ((prior,"_navigation.png"), (changed,"_cold_boot.png")):
        frames = {row["frame"]:row for row in report["frames_captured"] if row["path"].endswith(suffix)}
        shot, panel = build.display.read_frame(frames, 5960)
        shots.append(shot)
        panels.append(panel)
    delta = ImageChops.difference(*panels)
    delta.paste((0,0,0),(0,0,256,16))
    delta.paste((0,0,0),(0,275,165,300))
    assert delta.getbbox() is None
    before, after = [check(panel,(0,0,256,17),(230,230,230),label,font)
                    for panel,label in zip(panels,("CliffordFleet ２","Clifford Fleet ２"),strict=True)]
    markers = [check(panel,(6,278,158,294),(0,8,0),label,font)
               for panel,label in zip(panels,("CliffordFleet ２ + more","Clifford Fleet ２ + more"),strict=True)]
    assert after["layout_width"] == before["layout_width"] + 6
    assert markers[1]["layout_width"] == markers[0]["layout_width"] + 6
    sheet = Image.new("RGB",(1024,175),"#263238")
    renderer = ImageDraw.Draw(sheet)
    for i, (caption,panel) in enumerate(zip(("Before","Revised"),panels,strict=True)):
        x = i * 512
        renderer.text((x+4,3),caption,fill="white")
        sheet.paste(panel.crop((0,0,256,18)).resize((512,36),Image.Resampling.NEAREST),(x,20))
        sheet.paste(panel.crop((0,263,256,320)).resize((512,114),Image.Resampling.NEAREST),(x,60))
    sheet.save(SHEET)
    output = dict(candidate_sha256=staged["candidate_sha256"], predecessor_sha256=staged["predecessor_sha256"],
        ordinary_route_map=True, original_ordinal_and_cluster_suffix_preserved=True,
        live_header=[before,after], live_markers=markers, changed_surfaces_limited_to_header_and_marker=True,
        observations=shots, visual_review=dict(path=str(SHEET),sha256=base.digest(SHEET)), hardware_verified=False,
        evidence={str(path):base.digest(path) for path in (original,replay.REPORT,build.PROOF)})
    base.save(PROOF,output)
    print("Both live fleet-name surfaces match complete native glyph masks, including the ordinal and cluster suffix.")


if __name__ == "__main__":
    main()
