"""Review all Square store captions and improve five compound names."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from types import FunctionType
import sys

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from scripts import register_square_rumor_followup_20261122 as parent
from scripts import register_square_label_wording_20261119 as history
from scripts import stage_square_label_wording_20261119 as square
from scripts import stage_rafael_deck_tutorial_followup_20261122 as precedent
from scripts import replay_lisbon_shopkeeper_20261119 as lisbon
from scripts import checkpoint_regional_town_dialogue_20261115 as regional
from dk4tool.patch.category_dialogue_lookup import ADDRESS_BASE
from dk4tool.patch.captain_name_delete import CAPTAIN_PROVIDERS, SECTION_LIMIT


base,native = parent.base,parent.native
ARM,COMMON,CLEAN = square.ARM,square.COMMON,square.CLEAN
ROOT = Path("work/analysis/square_shop_names_20261122")
ROM,PROOF = ROOT/"Square_Shop_Names_STAGED.nds",ROOT/"stored_proof.json"
PATCH,REBUILT = ROOT/"translation.xdelta",ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT/"startup/capture/capture_report.json"
SHEET = ROOT/"all_square_captions.png"
LEAD = Path("translations/editorial_checkpoints/SharedText_20261110_v1/square_spice_caption_lead_20261122_v1.json")
NAMES = {3:"Spice Shop",7:"Craft Shop",10:"Scent Shop",12:"Gem Shop",14:"Dye Shop"}
NOTES = {
    3:"Spice is the idiomatic modifier for the shop that sells pepper, cloves and other spices.",
    7:"Craft Shop names the finished wares category. Its glass, china, lacquerware and inlaid ware are products of skilled craft.",
    10:"Scent Shop covers aromatic materials such as frankincense, musk and ambergris without implying finished perfume.",
    12:"Gem Shop names the retailer of loose gemstones and pearls. Jewelry remains the separate label for ornamental materials.",
    14:"Dye Shop names the retailer of colorants such as indigo, cochineal and turmeric.",
}
CAPTURES = {"syracuse": (4750,6750,7150,7550,10350), "lisbon": (4750,5150,5550,9550)}


def transform(arm):
    code = MainCodeFile(arm,square.BASE)
    owner = code.sections[-1]
    original = bytes(owner.data)
    assert bytes(code.save()) == arm and owner.ramAddress == CAPTAIN_PROVIDERS and not owner.bssSize
    assert square.target(arm,square.CALL) == square.STUB
    assert square.target(arm,square.FORMAT_CALL) == square.BASE+0xABFCC
    assert unpack_from("<I",arm,0x5FDEC)[0] == square.SCRATCH
    entry = owner.ramAddress + len(original)
    instr = []
    for n in NAMES:
        instr.extend((f"cmp r0,#{n}",f"adreq r2,caption_{n}","beq caption_format"))
    instr.extend((f"b {square.STUB}","caption_format:","ldr r0,scratch","adr r1,copy_format",
        f"b {square.BASE+square.FORMAT_CALL}","scratch:",f".word {square.SCRATCH}",
        "copy_format:",'.asciz "%s"'))
    for n,name in NAMES.items():
        instr.extend((f"caption_{n}:",f'.asciz "{name}"'))
    instr.append(".align 2")
    payload = square.assemble("\n".join(instr),entry)
    stop = entry+len(payload)
    assert entry%4==stop%4==0 and stop <= SECTION_LIMIT
    assert all(s.ramAddress + len(s.data) + s.bssSize <= CAPTAIN_PROVIDERS or s.ramAddress >= SECTION_LIMIT
               for s in code.sections[:-1])
    owner.data.extend(payload)
    word = square.assemble(f"bl {entry}",square.BASE+square.CALL)
    code.sections[0].data[square.CALL:square.CALL+4] = word
    installed = bytes(code.save())
    assert square.target(installed,square.CALL)==entry
    assert square.cache_plan(arm) == square.cache_plan(installed)
    owner.data = bytearray(original)
    code.sections[0].data[square.CALL:square.CALL+4] = arm[square.CALL:square.CALL+4]
    assert bytes(code.save()) == arm
    return installed,dict(original_call=square.BASE+square.CALL, old_formatter=square.STUB,
        helper=entry,helper_end=stop,helper_hex=payload.hex(),extended_autoload_owner=owner.ramAddress,
        original_prefix_sha256=native.digest(original),format_call=square.BASE+square.FORMAT_CALL,
        replacement_categories=sorted(NAMES),whole_ARM9_inverse=True)


def review(source,arm,after):
    prior = square.prior
    before_cpu,next_cpu = map(prior.cpu_for,(arm,after))
    font = prior.GameAsciiFont.from_arm9(after)
    assert font.glyphs == prior.GameAsciiFont.from_arm9(arm).glyphs
    previous = {r["category"]:r for r in base.load(history.REVIEW)["records"]}
    assert len(previous)==18 and source[square.prior.stage.FORMAT_SLOT:square.prior.stage.FORMAT_SLOT+5]==b"%s\x93\x58\0"
    rows, getter_cases = [], []
    for owner in (*prior.UI_RETURNS,0x0205FC48):
        for key in (*range(18),-1,-2,-3,18,19,255):
            old,new = [prior.getter(cpu,key,owner) for cpu in (before_cpu,next_cpu)]
            assert old==new
            text = None
            if 0<=key<18:
                text = prior.string(before_cpu,old)
                assert prior.string(next_cpu,new)==text
            getter_cases.append(dict(actual_return_pc=owner,category=key,pointer=new,text=text))
    for key in (3,7,10,12,14):
        assert any(r["category"]==key and r["text"] for r in getter_cases)
    sheet = Image.new("RGB",(768,252),"#263238")
    draw = ImageDraw.Draw(sheet)
    for n in range(18):
        old = previous[n]
        word, = unpack_from("<I",source,square.TABLE+4*n)
        offset = word-square.BASE
        jp = source[offset:source.index(0,offset)+1]
        ref = old["source_reference"]
        assert jp.hex()==ref["category_hex"] and offset==ref["string_offset"]
        assert all(old["review"].values())
        before,caption = [square.run_caption(cpu,n) for cpu in (before_cpu,next_cpu)]
        assert before == old["english"] and caption==NAMES.get(n,before)
        left,right = (prior.native(arm,before),prior.native(after,caption))
        for text,(pixels,_,_) in ((before,left),(caption,right)):
            expected = prior.expected_pixels(font,text)
            assert all(0<=x<64 and 0<=y<12 for x,y in expected)
            assert pixels == bytes(int((i%64,i//64) in expected) for i in range(768))
        if n not in NAMES:
            assert left[:2] == right[:2]
        raw, = unpack_from("<I",arm,square.TABLE+4*n)
        value = (raw&0xFFFFFF)+ADDRESS_BASE-square.BASE
        current_ref = dict(file_path=ARM,table_entry=square.TABLE+4*n,value_offset=value,
            category_field_hex=arm[square.TABLE+4*n:square.TABLE+4*n+4].hex(),
            selector=square.BASE+square.CALL,formatter=square.BASE+square.FORMAT_CALL,
            exact_caption_hex=(before.encode("ascii")+b"\0").hex())
        pixels = right[0]
        tile = Image.frombytes("L",(64,12),bytes(v*230 for v in pixels))
        x,y = n%3*256,n//3*42
        draw.text((x+4,y+10),str(n),fill="white")
        sheet.paste(tile.resize((192,36),Image.Resampling.NEAREST),(x+39,y+3))
        rows.append(dict(id=old["id"],category=n,file_path=ARM,Japanese=old["Japanese"],speaker="Square shop menu",
            source_reference=ref,current_reference=current_ref,previous_English=before,english=caption,
            source_meaning=old["source_meaning"],localization_note=NOTES.get(n,old["localization_note"]),
            decision="revision" if n in NAMES else "retention",review=old["review"],
            native_display=dict(complete_single_row=True,ink_rightmost_x=max(x for x,_ in prior.expected_pixels(font,caption)),
                glyph_plane_sha256=native.digest(pixels),width=64,height=12),
            exact_installed_caption_hex=(caption.encode("ascii")+b"\0").hex()))
    return rows,getter_cases,sheet


def stage():
    assert not ROOT.exists()
    meta,lead = map(base.load,(parent.RELEASE,LEAD))
    assert base.digest(parent.ROM)==meta["candidate_sha256"]==lead["candidate_sha256"]
    assert base.digest(base.REGISTRY)==meta["registry_sha256"] and base.digest(parent.MANIFEST)==meta["manifest_sha256"]
    image,clean = map(base.NdsImage.open,(parent.ROM,CLEAN))
    assert base.digest(CLEAN)==meta["clean_input_sha256"]
    before = native.files(image)
    arm = before[ARM]
    assert native.digest(arm)==meta["target_ARM9_sha256"]
    revised,allocation = transform(arm)
    rows,getters,picture = review(clean.read_file(ARM),arm,revised)
    assert rows[3]["previous_English"]==lead["shown"] and rows[3]["english"]==lead["proposed"]
    image.replace_file(ARM,revised)
    final = native.files(image)
    assert before.keys()==final.keys() and {p for p in before if before[p]!=final[p]}=={ARM}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean),final)
    assert guard["total_exact_source_bound_relocated_leading25_count"]==7
    result = bytes(image.rom.save())
    image.replace_file(ARM,arm)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    picture.save(SHEET)
    candidate = base.digest(ROM)
    for row in rows:
        row["registered_reference"] = row["current_reference"] | dict(candidate_sha256=candidate,
            exact_caption_hex=row["exact_installed_caption_hex"])
    base.save(PROOF,dict(candidate_sha256=candidate,predecessor_sha256=meta["candidate_sha256"],
        clean_sha256=meta["clean_input_sha256"],target_ARM9_sha256=native.digest(revised),whole_parent_inverse=True,
        records=rows,source25=guard,native_scope=allocation,independent_category_getter_controls=getters,
        sheets={str(SHEET):base.digest(SHEET)},exact_lead_sha256=base.digest(LEAD)))
    print(f"Staged {candidate}. All 18 complete glyph masks and {len(getters)} independent category getter cases passed.",flush=True)


def itinerary(city):
    if city=="syracuse":
        events,_,_,history,donor = regional.capture.schedule(city)
        end = 10600
        return [r for r in events if r["start"]<end],end,history,donor
    events,_,end,history,donor = lisbon.schedule(city)
    return events,end,history,donor


def replay(city):
    proof = base.load(PROOF)
    assert base.digest(ROM)==proof["candidate_sha256"]
    events,end,history,donor = itinerary(city)
    assert base.digest(donor["source"])==donor["source_sha256"]
    assert base.load(history)["cold_boot"]
    root = ROOT/city
    root.mkdir()
    inputs = root/"inputs.json"
    base.save(inputs,events)
    harness = regional.capture.playback.harness
    argv = sys.argv
    try:
        sys.argv = [harness.__file__,"--rom",str(ROM),"--out",str(root/"capture"),"--frames",str(end),
            "--inputs-json",str(inputs),"--press-start","-1","--touchscreen","--battery-save",donor["source"],
            "--capture-every","999999","--capture-at",*map(str,CAPTURES[city])]
        harness.main()
    finally:
        sys.argv = argv
    assert base.digest(donor["source"])==donor["source_sha256"]


if __name__=="__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","patch","startup",*CAPTURES))
    action = cli.parse_args().action
    if action=="stage":
        stage()
    elif action in CAPTURES:
        replay(action)
    else:
        inherited = getattr(precedent,action)
        FunctionType(inherited.__code__,inherited.__globals__ | globals())()
