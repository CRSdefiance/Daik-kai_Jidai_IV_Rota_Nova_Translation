"""Open the two equipment descriptions with ordinary controls after bounded inventory seeding."""

from argparse import ArgumentParser
from io import StringIO
import json
import sys
from types import FunctionType

from scripts import headless_desmume_v193 as emulator
from scripts import native_inventory_fixture_v481 as inventory
from scripts import stage_ship_room_names_20261122 as stage
from scripts.replay_setup_save_equipment_v2 import REFERENCE


base,native=stage.base,stage.native
ROOT=stage.ROOT/"item_gameplay"
REPORT=ROOT/"capture/capture_report.json"
PROOF=ROOT/"verified_gameplay.json"
ITEMS=[104,105]
PANELS={104:10800,105:10400}


def play():
    assert not ROOT.exists()
    proof,reference=map(base.load,(stage.PROOF,REFERENCE))
    donor=reference["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and reference["cold_boot"] and not reference["savestate_loaded"]
    assert base.digest(donor["source"])==donor["source_sha256"]
    assert proof["candidate_sha256"]==base.digest(stage.ROM)
    assert [p["item_ID"] for p in proof["private_item_allocations"]]==ITEMS
    arm=base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert native.digest(arm)==proof["stored_components"][stage.ARM]
    original=base.NdsImage.open(stage.parent.ROM).read_file(stage.ARM)
    assert arm[:0x160000]==original[:0x160000]
    prefix=[r for r in reference["scripted_input_schedule"] if r["start"]<8400]
    commands=[
        {"until":8800,"duration":8,"buttons":["X"],"inventory_items":ITEMS},
        {"until":9200,"duration":8,"touch":[143,54]},
        {"until":9600,"duration":8,"buttons":["A"]},
        *({"until":frame,"duration":8,"buttons":["RIGHT"]} for frame in (10000,10400,10800)),
        {"until":11200,"duration":8,"buttons":["B"]},
        {"until":11600,"duration":8,"buttons":["B"]},
        {"stop":True},
    ]
    ROOT.mkdir()
    inputs=ROOT/"inputs.json"
    base.save(inputs,prefix)
    base.save(ROOT/"commands.json",commands)
    transfer=inventory.transfer
    scoped=FunctionType(transfer.__code__,transfer.__globals__|{"SUPPORTED_ARM_SHA":(native.digest(arm),)})
    old_argv,old_stdin=sys.argv,sys.stdin
    inventory.transfer=scoped
    try:
        sys.stdin=StringIO("".join(json.dumps(row)+"\n" for row in commands))
        sys.argv=[emulator.__file__,"--rom",str(stage.ROM),"--out",str(ROOT/"capture"),"--frames","11601",
            "--inputs-json",str(inputs),"--battery-save",donor["source"],"--touchscreen",
            "--capture-every","999999","--pause-at","8400","--allow-inventory-fixtures"]
        emulator.main()
    finally:
        inventory.transfer,sys.argv,sys.stdin=transfer,old_argv,old_stdin
    assert base.digest(donor["source"])==donor["source_sha256"]


def verify():
    from struct import unpack
    from PIL import Image, ImageDraw
    from scripts import verify_item_gallery_wraps_native_20261121 as gallery
    from scripts.verify_captain_biographies_v1 import captured
    from scripts.verify_item_parent_layout import EXPECTED, compose

    assert not PROOF.exists()
    stored,report=map(base.load,(stage.PROOF,REPORT))
    assert report["ROM_sha256"]==stored["candidate_sha256"]==base.digest(stage.ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"]==11600 and report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    donor=report["battery_save_preloaded"]
    assert base.digest(donor["source"])==donor["source_sha256"]
    fixture,=report["synthetic_inventory_fixtures"]
    assert [r["item_id"] for r in fixture["items"]]==ITEMS and fixture["frame"]==8400
    assert report["normal_acquisition_verified"] is False
    nav={r["frame"]:r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
    assert all(base.digest(nav[frame]["path"])==nav[frame]["PNG_sha256"] for frame in (*PANELS.values(),8400,11600))
    assert captured(nav[8400]).tobytes()==captured(nav[11600]).tobytes()
    assert captured(nav[11200]).tobytes()!=captured(nav[11600]).tobytes()

    image=base.NdsImage.open(stage.ROM)
    arm,common,font=(image.read_file(name) for name in (stage.ARM,stage.COMMON,"/GRP/KANJI.FNT"))
    hdr=stage.common
    draw=gallery.make_execute(native.digest(arm[hdr.DIRECTORY_OFFSET:hdr.TABLE_OFFSET]),arm)
    requests=[dict(source_origin=a,size=b,destination_origin=c) for a,b,c in EXPECTED]
    fields=[x for x in requests if x["source_origin"] in ([48,0],[0,12],[0,36],[0,48],[0,60])]
    rows=[]
    sheet=Image.new("RGB",(1024,410),"#283442")
    labels=ImageDraw.Draw(sheet)
    for index,plan in enumerate(stored["private_item_allocations"]):
        ident=plan["item_ID"]
        actual=captured(nav[PANELS[ident]])
        result=draw(arm,"fixture",item_page="main",item_case=(0,4),surface_size=(240,96),
            kanji_font=font,mode=4,item_resource_index=ident,item_common=common)
        assert result["item_actual_common_ids"]==[plan["message_ID"]]
        matrix,_=compose(result,requests)
        pixels=unpack("<49152H",matrix)
        masks=[]
        for field in fields:
            x,y=field["destination_origin"]
            width,height=field["size"]
            foreground={(xx,yy) for yy in range(height) for xx in range(width)
                        if actual.getpixel((x+xx,y+yy))==(230,230,230)}
            expected={(xx,yy) for yy in range(height) for xx in range(width)
                      if pixels[(y+yy)*256+x+xx]==1}
            assert foreground==expected,(ident,field,len(foreground^expected))
            masks.append(dict(destination=[x,y],size=[width,height],complete_foreground_and_blank_cells=True))
        rows.append(dict(message_ID=plan["message_ID"],item_ID=ident,frame=PANELS[ident],
            lines=plan["compiled_rows"],capture=nav[PANELS[ident]],screen_masks=masks))
        labels.text((512*index+4,3),f"COMMON {plan['message_ID']}   Items",fill="white")
        sheet.paste(actual.crop((0,0,256,192)).resize((512,384),Image.Resampling.NEAREST),(512*index,20))
    path=ROOT/"observed_item_descriptions.png"
    sheet.save(path)
    base.save(PROOF,dict(candidate_sha256=stored["candidate_sha256"],report_sha256=base.digest(REPORT),observed=rows,
        sheet=str(path),sheet_sha256=base.digest(path),seeded_inventory_fixture=fixture,ordinary_item_controls=True,
        observed_return=nav[11600],original_town_return_exact=True,hardware=False))
    print("Both full Nursery descriptions appeared in Items and returned to the same Lisbon screen.")


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("play","verify"))
    globals()[parser.parse_args().action]()

