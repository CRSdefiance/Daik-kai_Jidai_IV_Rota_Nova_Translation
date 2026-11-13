"""Reuse native port-paper edges and texture for the two reviewed screens."""

import copy
import json
import struct
import zlib
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import apply_pxl_native_label_batch

ROOT = Path("work/analysis/plaque_style_v247")


def save(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def paper(width, height, palette):
    """Nine-slice native paper: preserve two-pixel corners, tile the interior."""
    batch = json.loads(Path("translations/trading_towninfo_graphics_v2.json").read_text(encoding="utf-8"))
    donor = PxlImage.from_bytes(NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file(batch["file_path"]))
    row = batch["records"][0]
    src = zlib.decompress(bytes.fromhex(row["background_indices_zlib_hex"]))
    sw, sh = row["box"][2] - row["box"][0], row["box"][3] - row["box"][1]
    def coord(i, length, original):
        if i < 2:
            return i
        if i >= length - 2:
            return original - (length - i)
        return 2 + (i - 2) % (original - 4)
    mapping = [min(range(len(palette)), key=lambda n: sum((palette[n][k]-rgb[k])**2 for k in range(3))) for rgb in donor.palette]
    return bytes(mapping[src[coord(y,height,sh)*sw+coord(x,width,sw)]] for y in range(height) for x in range(width))


def other_labels():
    arm = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    def record(offset, english, reason):
        return {"source":arm[offset:offset+80].split(b"\0")[0].decode("cp932"),"english":english,"reason":reason}
    return {
        "retained_skill_labels":[record(o,en,note) for o,en,note in [
            (0x148324,"Command","Leadership/command ability."),(0x148344,"Sailing","Ship-handling skill."),
            (0x14834C,"Survey","Surveying skill."),(0x148354,"Finance","Accounting skill; compact established label."),
            (0x148304,"Aim","Accuracy/hit ability."),(0x14831C,"Observe","Observation ability; compact established label.")]],
        "other_visible_labels":[record(o,en,note) for o,en,note in [
            (0x133FD4,"Assign Sailors","Instruction to allocate sailors."),
            (0x133FBC,"Need / Now / Max","Required, current and maximum sailor counts."),
            (0x133FF4,"%d days","Approximate possible sailing duration; whole days displayed."),
            (0x13400C,"%s Cap","Ship captain name and compact Captain abbreviation."),
            (0x1339F8,"Auto","Automatic allocation."),(0x11B534,"Lo","Set the minimum count; native button leaves only two letters after its L icon. Min was tested and clipped, so retain compact Lo."),
            (0x11B59C,"Hi","Set the maximum count; native button leaves only two letters after its R icon. Max was tested and clipped, so retain compact Hi."),(0x11B554,"Finish","Complete crew allocation."),
            (0x14852C,"Sailor Info","Information about a navigator/ship officer."),
            (0x148498,"Admiral","Fleet/company leader, localized as the naval leadership role."),
            (0x14827C,"Healthy","Healthy physical condition."),(0x1482D4,"Normal","Normal mental condition."),
            (0x11B50C,"Back","Return to the previous screen."),(0x11B51C,"Select","Confirm the highlighted entry.")]],
    }


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    base = NdsImage.open("out/raphael_natural_v2_accepted_base.nds")
    arm = base.read_file("/__arm9__.bin")
    audit = []
    groups = [
        ("crew", "assign_sailors_graphics_v4", "assign_sailors_graphics_v5", [
            ("艦隊水夫数", "Fleet Crew", "Total sailors in the fleet, rather than an assignment command.", [8,18,88,34]),
            ("未編成水夫数", "Unassigned", "Sailors who have not been allocated to ships.", [132,18,216,34]),
            ("航行可能日数", "Endurance", "How many days the fleet can remain at sea; the value explicitly says days.", [5,40,88,56]),
            ("海兵詰所", "Quarters", "Marine quarters count; compact label denotes the rooms, not the number of marines.", [5,109,68,124]),
            ("砲種", "Cannon", "Cannon type, with its gun name displayed immediately to the right.", [84,109,122,124]),
            ("縦帆性能", "Fore/Aft", "Fore-and-aft sail performance, including more than lateen sails.", [5,131,68,146]),
            ("横帆性能", "Square", "Square-sail performance, paired with Fore/Aft.", [132,131,196,146]),
        ]),
        ("person", "person_info_graphics_v2", "person_info_graphics_v3", [
            ("身体", "Health", "Physical condition, followed by Healthy, Sick, Injured or another condition.", [3,103,49,118]),
            ("精神", "Mood", "Current mental condition; distinct from the permanent Spirit stat.", [3,123,49,138]),
            ("レベル", "Level", "Character level.", [3,143,49,158]),
            ("HP", "HP", "Current hit points.", [3,163,49,178]),
            ("体力", "Stamina", "Physical stamina attribute.", [124,99,170,114]),
            ("敏捷", "Agility", "Agility attribute.", [124,114,170,129]),
            ("魅力", "Charm", "Personal charm attribute.", [124,129,170,144]),
            ("知力", "Wits", "Intellectual ability; concise natural English stat label.", [124,144,170,159]),
            ("精神", "Spirit", "Mental fortitude attribute, separate from the current Mood condition.", [124,159,170,174]),
            ("運勢", "Luck", "Luck attribute; exact native source is 運勢.", [124,174,170,189]),
        ]),
    ]
    for name, old, new, entries in groups:
        batch = copy.deepcopy(json.loads(Path("translations/" + old + ".json").read_text(encoding="utf-8")))
        source = base.read_file(batch["file_path"])
        assert sha(source) == batch["source_file_sha256"]
        image = PxlImage.from_bytes(source)
        for row, (jp, en, note, plaque) in zip(batch["records"], entries, strict=True):
            box = row["box"]
            previous = zlib.decompress(bytes.fromhex(row["background_indices_zlib_hex"]))
            width = box[2] - box[0]
            pixels = bytearray(previous)
            if en == "Cannon":
                # Native count begins at x123. Reclaim the old two right columns
                # from the same repeating wallpaper, outside the new plaque.
                for y in range(109,124):
                    for x in (122,123):
                        pixels[(y-box[1])*width+x-box[0]] = image.indices[y*256+x+64]
            tile = paper(plaque[2]-plaque[0], plaque[3]-plaque[1], image.palette)
            for y in range(plaque[1], plaque[3]):
                for x in range(plaque[0], plaque[2]):
                    pixels[(y-box[1])*width+x-box[0]] = tile[(y-plaque[1])*(plaque[2]-plaque[0])+x-plaque[0]]
            row.update(text=en, source_japanese=jp, source_meaning=note,
                       background_indices_zlib_hex=zlib.compress(pixels,9).hex(),
                       draw_box=[plaque[0]+2,plaque[1]+2,plaque[2]-2,plaque[3]-2],
                       plaque_box=plaque, localization_note=note,
                       context="Source-reviewed screen label on native port-information paper.",
                       review={k:True for k in ("source","context","localization","naturalness","formatting")})
            audit.append({"screen":name,"source":jp,"english":en,"reason":note,"source_evidence":"work/clean.nds original artwork and native ARM9 strings"})
        batch.update(supersedes="translations/"+old+".json", trim_blank_top_rows=0,
                     scope="Reviewed English on native textured paper with intact beveled edges.",
                     style_donor="translations/trading_towninfo_graphics_v2.json:DK4_TOWNINFO_TYPE_NATIVE")
        path = Path("translations/"+new+".json")
        save(path,batch)
        data,_ = apply_pxl_native_label_batch(path,source,arm)
        (ROOT/(name+"_target.pxl")).write_bytes(data)
        PxlImage.from_bytes(data).render().resize((768,576)).save(ROOT/(name+"_art.png"))
    # Dynamic equipment hint uses exactly the same native paper, drawn as runs.
    donor = PxlImage.from_bytes(base.read_file("/_pxl/towninfo.pxl"))
    tile = paper(88,16,donor.palette)
    runs = []
    for y in range(16):
        x = 0
        while x < 88:
            index=tile[y*88+x]; end=x+1
            while end<88 and tile[y*88+end]==index:
                end+=1
            rgb=donor.palette[index]
            color=0x8000 | (rgb[0]*31+127)//255 | ((rgb[1]*31+127)//255)<<5 | ((rgb[2]*31+127)//255)<<10
            runs.append([x,y,end-x,1,color])
            x=end
    (ROOT/"tooltip_runs.bin").write_bytes(b"".join(struct.pack("<5I",*r) for r in runs))
    save(ROOT/"translation_review.json", {**other_labels(),"graphics":audit,"tooltip":{"source":"装備アイテム","english":"Equipped Items","reason":"Items currently equipped; source at clean ARM9 0x148CC8."},
         "skill_changes":[{"source":"生命力","was":"Health","english":"Vigor","reason":"Life force or vitality, distinct from current condition and HP. Vigor is a natural synonym that fits the native label/value line."},
                          {"source":"説得力","was":"Social","english":"Speech","reason":"Ability to persuade through speech and negotiation. Speech names the persuasion/negotiation skill in familiar game terminology; the six-letter label leaves room for complete numeric values in the narrow right column."},
                          {"source":"剣闘術","was":"Combat","english":"Swords","reason":"Sword-fighting skill. Swords is a familiar compact skill category and fits the six-character native field without dropping numeric digits."},
                          {"source":"謀略術","was":"Tactics","english":"Guile","reason":"Skill in plots and schemes. Guile captures cunning rather than battlefield maneuvers and fits the native line; eight-letter Intrigue wraps the value."}],
         "style":{"donor_sha256":sha(Path("translations/trading_towninfo_graphics_v2.json").read_bytes()),"tooltip_runs":len(runs),"native_palette_and_font_preserved":True}})
    print("Prepared 17 textured plaques, source review, and",len(runs),"native tooltip paper runs.")


if __name__ == "__main__":
    main()
