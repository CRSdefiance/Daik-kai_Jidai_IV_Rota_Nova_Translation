"""Run the current native item and Deck display paths for the three room names."""

from argparse import ArgumentParser
from struct import iter_unpack
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import prepare_work_comments_v842 as snapshots
from scripts import probe_physical_fatigue_fonts_v960 as physical
from scripts import probe_work_fonts_v843 as deck
from scripts import stage_ship_room_names_20261122 as stage
from scripts.stage_deck_comments_20261119 import current_pixels
from scripts import stage_utility_weapon_item_cards_v1 as items
from scripts import verify_item_gallery_wraps_native_20261121 as gallery
from scripts.source_locked_derivation_v5118 import checked_text


base,native,parent=stage.base,stage.native,stage.parent
ROOT=stage.ROOT/"native_display"
ITEMS,DECK=ROOT/"item_proof.json",ROOT/"deck_proof.json"


def resources():
    stored,ledger,release=map(base.load,(stage.PROOF,stage.MANUSCRIPT,parent.RELEASE))
    sha=base.digest(stage.ROM)
    assert sha==stored["candidate_sha256"]==ledger["candidate_sha256"]
    assert release["candidate_sha256"]==stored["predecessor_sha256"]==base.digest(parent.ROM)
    assert base.digest(stage.MANUSCRIPT)==stored["manuscript_sha256"]
    current=base.NdsImage.open(stage.ROM)
    arm,common,font=(current.read_file(p) for p in (stage.ARM,stage.COMMON,"/GRP/KANJI.FNT"))
    runtime=native.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    clone=items.with_components(runtime,arm,common)
    assert runtime.image.read_file("/GRP/KANJI.FNT")==font
    assert stored["stored_components"]=={stage.ARM:native.digest(arm),stage.COMMON:native.digest(common)}
    cpu,get,provider=clone.machine(arm,common,clone.raw,clone.plan)
    for row in ledger["records"]:
        data=bytes.fromhex(row["installed_hex"])
        addr=get(0x5528C,row["message_ID"])
        assert bytes(cpu.mem_read(addr,len(data)+1))==data+b"\0"
    assert provider.reads
    clone.calls.clear()
    return runtime,clone,current,stored,ledger,font


def item_pages():
    assert not ITEMS.exists()
    previous,current,_,proof,ledger,font=resources()
    arm,common=current.arm,current.common
    rows={r["message_ID"]:r for r in ledger["records"]}
    projections=[r|{"new_pointer":r["pointer"]} for r in proof["private_item_allocations"]]
    plans=items.native_getters(previous,current,{"ownership":{"item_paragraphs":projections}})
    assert len(plans)==2
    directory=native.digest(arm[items.DIRECTORY_OFFSET:items.TABLE_OFFSET])
    draw=gallery.make_execute(directory,arm)
    pixels,_=gallery.oracle()
    snaps=[]
    sheet=Image.new("RGB",(960,384),"#283442")
    captions=ImageDraw.Draw(sheet)
    for n,(item,plan) in enumerate(sorted(plans.items())):
        for j,(screen,config) in enumerate((("main",(0,4)),("standalone",(0,1)))):
            for mode in (4,16):
                result=draw(arm,"fixture",item_page=screen,item_case=config,surface_size=(240,96),
                    kanji_font=font,mode=mode,item_resource_index=item,item_common=common)
                y=36 if screen=="main" else 24
                actual=[r for r in result["item_draws"] if y<=r["y"]<=y+24]
                lines=[r["text"] for r in actual]
                assert lines==plan["compiled_rows"] and " ".join(lines)==rows[plan["message_ID"]]["english"]
                assert actual[0]["pointer"]==plan["pointer"]
                assert result["item_actual_common_ids"]==[plan["message_ID"]]
                glyphs=result["glyph_events"]
                assert [r["code"] for r in glyphs]==[c for d in result["item_draws"] for c in gallery.glyph_codes(d["text"],d["tracking"])]
                assert all(0<=g["x"]<=234 and 0<=g["y"]<=84 for g in glyphs)
                assert result["pixels"]==pixels(arm,font,glyphs,mode,background=0)
                snaps.append(dict(message_ID=plan["message_ID"],item_ID=item,page=screen,mode=mode,
                    complete_mask_sha256=native.digest(result["pixels"]),line_draws=actual,exact_plane_and_bounds=True))
                if mode==16:
                    panel=Image.new("RGB",(256,192))
                    panel.putdata([(242,231,205) if value==0 else (22,20,17) for (value,) in iter_unpack("<H",result["pixels"])])
                    sheet.paste(panel.crop((0,0,240,84)).resize((480,168),Image.Resampling.NEAREST),(480*j,192*n+18))
                    captions.text((480*j+4,192*n+2),f"COMMON {plan['message_ID']}   {screen} view",fill="white")
    ROOT.mkdir(exist_ok=True)
    assert len(snaps)==8
    path=ROOT/"item_room_names.png"
    sheet.save(path)
    base.save(ITEMS,dict(candidate_sha256=proof["candidate_sha256"],sheet=str(path),sheet_sha256=base.digest(path),
        tested_all_native_getters=218,unchanged_description_getters=216,cases=snaps,offline_original_renderer=True))
    print("Both item descriptions passed both views, both bitmap modes, and all 218 getters.")


def deck_page():
    assert not DECK.exists()
    runtime,clone,rom,proof,ledger,_=resources()
    a,ctx=clone.arm,runtime.arm
    for lo,hi in ((0x12104,0x12920),(0x15334,0x154E8),(0x53914,0x53A00),(0x7E100,0x7E108)):
        assert a[lo:hi]==ctx[lo:hi]
    source,old= snapshots.snapshot("battle_personal_v897_893_Julio",14700)
    ui,related=snapshots.snapshot("personal_cabin_v840_838_Charles_after",4600)
    fixture,binding=deck.prepare_model(a,source,7,2,ui)
    draw_ranges=((0xD16B4,0xD1898),(0x125A20,0x126000))
    assert all(runtime.raw[lo:hi]==a[lo:hi] for lo,hi in draw_ranges)
    current_fixture=bytearray(fixture)
    for lo,hi in draw_ranges:
        current_fixture[lo:hi]=runtime.raw[lo:hi]
    paint=FunctionType(deck.execute.__code__,deck.execute.__globals__|{"expected_pixels":current_pixels})
    row=ledger["records"][0]
    assert row["message_ID"]==1784
    text=bytes.fromhex(row["installed_hex"])
    lines=row["expected_lines"]
    assert " ".join(lines)==row["english"]
    cases,planes=[],[]
    for name,mode in (("ordinary",(0,0)),("battle",(0,1))):
        model,condition=physical.prepare_condition(a,bytes(current_fixture),7,mode)
        result,plane=paint(rom,model,7,2,1784,text,lines)
        assert result["complete_native_copy_macro_draw_and_ABI"]
        assert result["full252x96_native_and_independent_canvas_equal"]
        assert not any(plane[y*252+x] for y in range(60,96) for x in range(216,252))
        cases.append(result|{"mode":name,"condition_CPU_fixture":condition})
        planes.append(plane)
    assert planes[0]==planes[1]
    ROOT.mkdir(exist_ok=True)
    path=ROOT/"deck_lounge_name.png"
    Image.frombytes("L",(252,96),bytes(0 if v else 255 for v in planes[0])).crop((0,60,216,96)).resize((864,144),Image.Resampling.NEAREST).save(path)
    base.save(DECK,dict(candidate_sha256=proof["candidate_sha256"],sheet=str(path),sheet_sha256=base.digest(path),
        CPU_actor_snapshot=old,CPU_widget_snapshot=related,CPU_role_fixture=binding,current_font_and_draw_ranges=draw_ranges,
        cases=cases,identical_ordinary_and_battle_body=True,offline_original_renderer=True))
    print("The original ordinary and battle Deck display paths verified the complete Lounge reply.")


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("scope",choices=("items","deck"))
    scope=parser.parse_args().scope
    (item_pages if scope=="items" else deck_page)()

