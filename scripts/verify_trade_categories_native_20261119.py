"""Check the two Trade callers, the Square argument and all stock display inputs."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.patch.category_dialogue_lookup import FAMILY
from dk4tool.patch.market_goods_info_terminator_v1 import FIELDS, FORMAT, NEW_FORMAT
from scripts import stage_departure_warnings_20261119 as port
from scripts import stage_trade_categories_20261119 as stage
from scripts.probe_button_prompt_native import SAVED, STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_barmaid_scoped_layout_v780 import formatter
from scripts.verify_category_lookup_v754 import UI_RETURNS, getter, string
from scripts.verify_personal_gameplay_v841 import get_machine

base,native,patch = stage.base,stage.native,stage.patch
AMOUNTS = (0,99,100,101,65535)
FULL_RETURN = 0x0205FC48
SENTINELS = (-3,-2,-1,18,19,255)
WIDTH = 112


def callers(cpu,address,index):
    cpu.reg_write(UC_ARM_REG_SP,STACK)
    cpu.reg_write(UC_ARM_REG_R0,index&0xffffffff)
    saved = {reg:0xA5A51000+i for i,reg in enumerate(SAVED)}
    for reg,value in saved.items():
        cpu.reg_write(reg,value)
    cpu.emu_start(address,address+4,count=1000)
    assert cpu.reg_read(UC_ARM_REG_PC)==address+4 and cpu.reg_read(UC_ARM_REG_SP)==STACK
    assert all(cpu.reg_read(reg)==value for reg,value in saved.items())
    return cpu.reg_read(UC_ARM_REG_R0)


def native_pairs(runtime,arm):
    original,current = runtime.arm,arm
    after = bytearray(runtime.raw)
    for at in (*[pc-patch.BASE for pc in patch.CALLS],patch.TABLE+4*patch.TEXTILE_INDEX):
        assert after[at:at+4]==original[at:at+4]
        after[at:at+4] = current[at:at+4]
    old,_ = get_machine(original,runtime.raw)
    cpu,get = get_machine(current,bytes(after))
    assert bytes(cpu.mem_read(patch.OLD_FORMAT,len(patch.TEXTILES)))==patch.TEXTILES
    assert bytes(cpu.mem_read(NEW_FORMAT,len(FORMAT)))==FORMAT
    categories,checks = {},[]
    for n in (*range(18),*SENTINELS):
        for call in patch.CALLS:
            a,b = callers(old,call,n),callers(cpu,call,n)
            if n in SENTINELS:
                assert a==b
            else:
                assert string(cpu,b)==stage.LABELS[n][0]
                prior = string(old,a)
                assert (prior!=stage.LABELS[n][0])==(n in stage.REVISED)
                categories[n] = (a,b,prior)
            checks.append(dict(index=n,call=call,previous_pointer=a,current_pointer=b))
        for owner in UI_RETURNS+(FULL_RETURN,):
            a,b = getter(old,n,owner),getter(cpu,n,owner)
            if n==patch.TEXTILE_INDEX and owner==FULL_RETURN:
                assert string(old,a)=="Fiber" and string(cpu,b)=="Textiles"
            else:
                assert a==b and (n in SENTINELS or string(cpu,b)==string(old,a))
            checks.append(dict(index=n,original_getter_return=owner,previous_pointer=a,current_pointer=b))
    assert len(checks)==192
    return cpu,get,categories,checks


def glyph_pixels(font,lines,advance,width,height):
    ink = set()
    for row,line in enumerate(lines):
        for i,char in enumerate(line):
            glyph = font.decode(char)
            ink.update((i*advance+x,row*12+y+1) for x in range(6) for y in range(11) if glyph.getpixel((x,y)))
    assert all(0<=x<width and 0<=y<height for x,y in ink)
    return ink


def rendered_panel(font,lines):
    panel = Image.new("L",(WIDTH,24),255)
    for point in glyph_pixels(font,lines,5,WIDTH,24):
        panel.putpixel(point,0)
    return panel.convert("RGB")


def inspect_stock(clean, arm, cpu, get, categories, font):
    previous = base.load(stage.square.REVIEW)["records"]
    stock = {r["product_ID"]:(group["category"],r) for group in previous for r in group["clean_and_current_category_stock"]}
    assert sorted(stock)==list(range(124))
    assert arm[0xB3660:0xB366C]==clean[0xB3660:0xB366C]==bytes.fromhex("810080e0b204d0e11eff2fe1")
    # The original caller loads this unsigned halfword for the displayed percentage.
    for field in FIELDS:
        assert unpack_from("<I",arm,field)==(NEW_FORMAT,)
    products = get(0xCB124)+4
    cases,previews,native_text = [],{},[]
    for n,(expected_category,record) in sorted(stock.items()):
        item = products+16*n
        category = cpu.mem_read(item+12,1)[0]
        assert category==expected_category and record["source_category_byte"]==category+(category>=9)
        vtable, = unpack_from("<I",cpu.mem_read(item,4))
        name_method, = unpack_from("<I",cpu.mem_read(vtable+8,4))
        name_pointer = get(name_method-patch.BASE,item)
        name = string(cpu,name_pointer)
        assert name==record["current_English"]
        _,category_pointer,_ = categories[category]
        label = stage.LABELS[category][0]
        assert string(cpu,category_pointer)==label
        for field in FIELDS:
            ring, = unpack_from("<I",arm,field-4)
            assert ring==0x022A44EC
            for value in AMOUNTS:
                sp_guard = bytes(cpu.mem_read(STACK+4,16))
                cpu.mem_write(STACK,pack("<I",value))
                pointer = get(0xABFCC,ring,NEW_FORMAT,name_pointer,category_pointer)
                actual = bytes(cpu.mem_read(pointer,128)).split(b"\0",1)[0]
                expectation = f"{name}\n  {label} {value}%".encode("ascii")
                assert actual==expectation and len(actual)<128
                assert bytes(cpu.mem_read(STACK+4,16))==sp_guard
                assert string(cpu,name_pointer)==name and string(cpu,category_pointer)==label
                lines = actual.decode("ascii").split("\n")
                native_width = max(5*len(line) for line in lines)
                assert native_width<=WIDTH
                glyph_pixels(font,lines,5,WIDTH,24)
                if category in stage.REVISED and value==65535 and category not in previews:
                    previews[category] = (f"{label}  {name}",rendered_panel(font,lines))
                cases.append(dict(product_ID=n,category=category,consumer_format_pointer_field=patch.BASE+field,
                    value=value,formatted_hex=actual.hex(),native_width=native_width))
    for n,(word,note) in enumerate(stage.LABELS):
        source = unpack_from("<I",clean,patch.TABLE+4*n)[0]
        japanese = clean[source-patch.BASE:source-patch.BASE+32].split(b"\0",1)[0]
        assert (japanese+b"\0").hex()==previous[n]["source_reference"]["category_hex"]
        pointer_a,pointer_b,prior = categories[n]
        assert pointer_a==patch.BASE+FAMILY[0]+(unpack_from("<I",arm,patch.TABLE+4*n)[0]>>24)
        native_text.append(dict(id=f"TRADE_CATEGORY_{n:02d}",category=n,file_path=stage.ARM,speaker="Goods Info",
            context="The selected commodity appears above its category and city market percentage, next to the arrival calendar.",
            source_meaning=previous[n]["source_meaning"],clean_Japanese=japanese.decode("cp932"),
            previous_English=prior,english=word,localization_note=note,decision="revision" if n in stage.REVISED else "retention",
            source_reference=dict(table_entry=patch.BASE+patch.TABLE+4*n,pointer=source,hex=japanese.hex()),
            current_reference=dict(table_entry=patch.BASE+patch.TABLE+4*n,pointer=pointer_a,hex=prior.encode("ascii").hex()),
            staged_reference=dict(table_entry=patch.BASE+patch.TABLE+4*n,pointer=pointer_b,hex=word.encode("ascii").hex()),
            stock_members=[r["product_ID"] for r in previous[n]["clean_and_current_category_stock"]],
            review=dict.fromkeys(REQUIRED_REVIEW_GATES,True)))
    assert len(cases)==1240 and set(previews)==stage.REVISED
    return native_text,cases,list(previews.values())


def square_rumor(image,clean,arm,cpu):
    w = stage.parent.parent.stage.workflow
    common = image.read_file(stage.COMMON)
    directory = native.digest(arm[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    english = w.owned_entries(common,arm,directory)[730]
    source = w.common_message_entries(clean.read_file(stage.COMMON),clean.read_file(stage.ARM))[730]
    assert source.text.count(b"%s")==english.text.count(b"%s")==1
    assert arm[0x5FC40:0x5FC58]==clean.read_file(stage.ARM)[0x5FC40:0x5FC58]
    words = english.text.decode("ascii").strip()
    assert words=="Something in the %s market is sure to catch on soon."
    fmt,_ = formatter()
    row = dict(message_id=730,english=words,English_argument_source_indices=[0])
    prior,new = [fmt(cpu,row,(label,)) for label in (b"Fiber",b"Textiles")]
    assert not new["findings"] and "Textiles" in " ".join(new["lines"])
    arm_fonts = image.read_file("/GRP/KANJI.FNT")
    raster,independent,_ = port.font_tools(image)
    lines,plane = port.render(arm,bytes.fromhex(new["formatted_hex"]),raster,independent,arm_fonts)
    assert lines==new["lines"]
    native_page = Image.frombytes("L",(228,48),bytes(0 if p else 255 for p in plane)).convert("RGB")
    scope = dict(message_ID=730,source_reference=w.reference(source),current_reference=w.reference(english),
        source_hex=source.text.hex(),current_hex=english.text.hex(),previous_layout=prior,new_layout=new,
        original_return=FULL_RETURN,offline_only=True,retention="Keep the full rumor. Textiles describes the cloth and fiber market and remains natural in the original substitution.")
    return scope,("Square market rumor",native_page)


def save_sheets(previews,square):
    canvas = Image.new("RGB",(936,296),"#263238")
    draw = ImageDraw.Draw(canvas)
    for i,(label,image) in enumerate(previews):
        x,y = i%3*312,i//3*92
        draw.text((x+6,y+3),label,fill="white")
        canvas.paste(image.resize((224,48),Image.Resampling.NEAREST),(x+6,y+22))
    label,img = square
    draw.text((6,190),label,fill="white")
    canvas.paste(img.resize((456,96),Image.Resampling.NEAREST),(6,200))
    path = stage.ROOT/"trade_category_page_checks.png"
    canvas.save(path)
    return [dict(path=str(path),sha256=base.digest(path))]


def main():
    assert not stage.NATIVE.exists()
    staged,predecessor = map(base.load,(stage.PROOF,stage.parent.RELEASE))
    runtime = RegisteredRuntime(stage.parent.RELEASE,predecessor["own_registered_startup"],captain=3)
    image = base.NdsImage.open(stage.ROM)
    clean = base.NdsImage.open(stage.CLEAN)
    arm = image.read_file(stage.ARM)
    assert base.digest(stage.ROM)==staged["candidate_sha256"] and native.digest(arm)==staged["target_ARM9_sha256"]
    cpu,get,categories,checks = native_pairs(runtime,arm)
    rows,cases,pages = inspect_stock(clean.read_file(stage.ARM),arm,cpu,get,categories,GameAsciiFont.from_arm9(arm))
    rumor,square = square_rumor(image,clean,arm,cpu)
    review = dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",target_locale="en-US",
        review_gates=sorted(REQUIRED_REVIEW_GATES),candidate_sha256=staged["candidate_sha256"],records=rows)
    validate_natural_dialogue_batch(review)
    base.save(stage.NATIVE,review|dict(real_native_format_cases=cases,category_getter_cases=checks,
        square_rumor_scope=rumor,trade_expected_glyph_previews=6,sheets=save_sheets(pages,square),
        original_full_width_unsigned_percentage_maximum=65535,
        evidence={str(p):base.digest(p) for p in (stage.PROOF,stage.square.REVIEW,Path(__file__))}))
    print("Verified 192 getter cases, 1,240 native Trade strings, and the original Square rumor layout.")


if __name__=="__main__":
    main()
