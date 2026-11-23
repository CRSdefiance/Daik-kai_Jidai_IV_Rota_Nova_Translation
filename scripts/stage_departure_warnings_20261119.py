"""Review the complete Port departure checks and stage five revised warnings."""

from pathlib import Path
from struct import pack

from PIL import Image, ImageDraw

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import register_square_label_wording_20261119 as parent
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.probe_button_prompt_native import STACK
from scripts.probe_primary_town_research_routes_v2083 import INPUT, OUTPUT, callsite
from scripts.stage_port_supply_dialogue_20261115 import owned_deployment
from scripts.stage_square_shop_followup_20261119 import precedent as workflow

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN
ROOT = Path("work/departure_warnings_20261119/staged_v3")
ROM = ROOT / "Departure_Warnings_STAGED.nds"
PROOF = ROOT / "staged.json"
SHEET = ROOT / "departure_pages.png"
HISTORY = Path("translations/primary_town_services_contextual_final_review_v1.json")
PENDING = parent.parent.stage.PENDING
CALLERS = Path("work/analysis/town_services_callers_v2068/nine_source_table_caller_parent_contracts.json")
TABLES = {0x021174A0, 0x02118A20, 0x02118A40}
EDITS = {
    28: ("You need more sailors on one ship. Check fleet setup before you sail.",
         "The worker gives the reason and the action in direct spoken English. The original recommends checking the formation before departure."),
    32: ("Admiral, let's fix the ships first. It's risky to sail like this!",
         "Keep the brash companion's urgency and the explicit danger of leaving before repairs."),
    33: ("Admiral, we'd best repair the ships first.",
         "The measured advice fits the older voice and keeps repairs ahead of departure."),
    40: ("Hey, we'll be out of food soon at this rate, won't we?",
         "Keep the easygoing challenge and the concern about having nothing to eat with the current stores."),
    46: ("Admiral, are our supplies too low?",
         "The direct question fits the older companion and keeps the complete concern together."),
}
RETENTIONS = {
    27: "The worker explicitly distinguishes no sailors from a shortage and leaves both remedies open.",
    29: "The formal warning gives the required repair and names the moment before departure.",
    30: "The hesitation suits the more tentative companion and preserves that some ships need work.",
    31: "Hold on catches the captain's attention. The companion states the repair problem in plain terms.",
    34: "The fear of drowning preserves the young companion's exaggeration, followed by the practical suggestion.",
    35: "The polite suggestion preserves the order of repairs and sailing.",
    36: "The deferential opening and trailing pause suit the warning, with the risk of running out explicit.",
    37: "At this rate ties the worry to the supplies already aboard and keeps the urgency.",
    38: "The companion gets the immediate problem out first, then addresses the captain.",
    39: "The firm wording makes the shortage feel urgent, with no extra claim about how the ships were provisioned.",
    41: "Goodness and the measured phrasing suit the companion's register. Both the low amount and near exhaustion remain.",
    42: "The mild warning expresses uncertainty about whether supplies will be enough.",
    43: "The question and just a bit preserve the informal concern of this voice.",
    44: "The personal worry and trailing pause distinguish this companion's gentler delivery.",
    45: "The companion asks a short direct question and keeps the original degree of shortage.",
    47: "The first question is about the companion's own meals. The second brings the concern back to the fleet.",
    48: "The reflective opening and tentative wording fit the last alternative.",
    49: "The worker's short price question follows the crew's warning and keeps the gold amount dynamic.",
}


def routed_format(cpu, body, parent_pc, selector, field):
    for offset in (0x264,0x270,0x274,0x27C):
        cpu.mem_write(STACK+offset,bytes(4))
    cpu.mem_write(STACK+0x264,pack("<I",parent_pc))
    cpu.mem_write(STACK+field,pack("<I",selector))
    cpu.mem_write(INPUT-16,b"\xA5"*1056)
    cpu.mem_write(INPUT,body+b"\0")
    old = bytes(cpu.mem_read(INPUT-16,1056))
    cpu.mem_write(OUTPUT-16,b"\xA5"*1056)
    callsite(cpu,0x02054160,(OUTPUT,INPUT,0))
    assert bytes(cpu.mem_read(INPUT-16,1056)) == old
    assert bytes(cpu.mem_read(OUTPUT-16,16)) == b"\xA5"*16
    text, tail = bytes(cpu.mem_read(OUTPUT,1024)).split(b"\0",1)
    # The literal copy can leave its old trailing padding beyond the formatter's
    # new terminator. Those bytes stay within the original bounded output.
    prior_tail = (b" "+body+b"\0")[len(text)+1:]
    assert all(b in (0,32) for b in prior_tail)
    assert tail == prior_tail.ljust(len(tail),b"\xA5")
    assert b" ".join(text.split()) == body.rstrip(b" ")
    return text


def render(arm, formatted, raster, independent, kanji):
    events = []
    pixels, used = raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,48),complete=False,
                          instruction_limit=2000000,glyph_events=events)
    assert used == len(formatted)
    assert [e["code"] for e in events if e["code"]!=32] == glyph_codes(formatted)
    assert all(0 <= e["x"] and e["x"]+6<=228 and 0 <= e["y"] and e["y"]+12<=48 for e in events)
    lines = [line.strip().decode("ascii") for line in formatted.split(b"\n") if line.strip()]
    assert 0 < len(lines) <= 3
    expected = independent(arm,kanji,lines)
    # The current registered ASCII painter draws one pixel down within each row.
    assert bytes(228)+expected[:-228] == pixels
    return lines,pixels


def main():
    assert not ROOT.exists()
    release, ledger = map(base.load,(parent.RELEASE,base.LEDGER))
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(parent.ROM)==release["candidate_sha256"]==ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(CLEAN)==release["clean_input_sha256"]
    runtime = workflow.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    arm,common = runtime.arm,runtime.common
    clean = base.NdsImage.open(CLEAN)
    ja = clean.read_file(ARM)
    source = workflow.common_message_entries(clean.read_file(COMMON),ja)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    before = workflow.owned_entries(common,arm,directory)
    history = {r["message_id"]:r for r in base.load(HISTORY)["records"]}
    credited = {(r["file_path"],r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    assert sorted(EDITS.keys()|RETENTIONS.keys())==list(range(27,50))
    routes = {27:(0x02054014,27,0x274),28:(0x02054014,28,0x274)}
    assert arm[0x60A68:0x60C28]==ja[0x60A68:0x60C28]
    for table in base.load(CALLERS)["tables"]:
        addr=table["table"]
        if addr not in TABLES:
            continue
        start=addr-0x02000000
        assert arm[start:start+32]==ja[start:start+32]
        for n in table["source_members"]:
            if n>=0:
                routes[n]=(table["original_parent"],addr,table["original_selector_stack_offset"])
    assert set(routes)==set(range(27,49))

    storage={n:words.encode("ascii") for n,(words,_) in EDITS.items()}
    assert all(len(value)<=len(before[n].text) for n,value in storage.items())
    # Preserve each NUL boundary and the parser's record ordinals. The original
    # paragraph router normalizes this storage padding before rendering.
    storage={n:value.ljust(len(before[n].text),b" ") for n,value in storage.items()}
    after, installed, allocation = owned_deployment(common,arm,before,storage)
    for row in base.load(PENDING)["records"]:
        entry=installed[row["message_ID"]]
        assert workflow.reference(entry)==row["current_reference"] and entry.text.hex()==row["current_hex"]

    staged = workflow.with_components(runtime,arm,after)
    cpu,get,provider = staged.machine(arm,after,staged.raw,staged.plan)
    raster, independent, font = font_tools(runtime.image)
    kanji=runtime.image.read_file("/GRP/KANJI.FNT")
    sheet=Image.new("RGB",(940,120*len(EDITS)),"#263238")
    draw=ImageDraw.Draw(sheet)
    rows=[]
    for n in range(27,50):
        old, clean_entry, new = before[n],source[n],installed[n]
        prior=history[n]
        assert (COMMON,prior["id"]) in credited and all(prior["review"].values())
        assert prior["source_hex"]==clean_entry.text.hex()
        paragraph=" ".join(old.text.decode("ascii").split())
        assert paragraph==prior["english"].removesuffix("{PAD}")
        english,note=EDITS[n] if n in EDITS else (paragraph,RETENTIONS[n])
        assert clean_entry.text.count(b"%s")==old.text.count(b"%s")==new.text.count(b"%s")==int(n==49)
        assert bytes(cpu.mem_read(get(0x5528C,n),len(new.text)+1))==new.text+b"\0"
        row=dict(id=prior["id"],message_ID=n,file_path=COMMON,speaker=prior["speaker"],
            context="Port departure checks. The Port Worker warns about crew levels, then different companion voices warn about repairs or supplies. The Port Worker offers resupply.",
            clean_Japanese=clean_entry.text.decode("cp932"),source_meaning=prior["source_meaning"],
            english=english,previous_English=paragraph,localization_note=note,decision="revision" if n in EDITS else "retention",
            source_reference=workflow.reference(clean_entry),current_reference=workflow.reference(old),staged_reference=workflow.reference(new),
            source_hex=clean_entry.text.hex(),current_hex=old.text.hex(),staged_hex=new.text.hex(),
            original_substitutions=int(n==49),review=dict.fromkeys(REQUIRED_REVIEW_GATES,True))
        if n in EDITS:
            panels=[]
            for column,entry in enumerate((old,new)):
                formatted=routed_format(cpu,entry.text,*routes[n])
                lines,pixels=render(arm,formatted,raster,independent,kanji)
                panels.append(dict(lines=lines,formatter_output_hex=formatted.hex(),
                    full_native_plane_sha256=native.digest(pixels),page_count=1))
                x,y=column*470,list(EDITS).index(n)*120
                draw.text((x+5,y+4),f"{n} {'before' if column==0 else 'revised'}",fill="white")
                tile=Image.frombytes("L",(228,48),bytes(0 if p else 255 for p in pixels))
                sheet.paste(tile.resize((456,96),Image.Resampling.NEAREST),(x+5,y+21))
            row.update(native_route=routes[n],before_native=panels[0],revised_native=panels[1])
            if n in (28,32,40):
                assert " ".join(panels[1]["lines"])==english and len(panels[1]["lines"])==2
            if n==28:
                primary,instruction=english.split(". ",1)
                assert panels[1]["lines"]==[primary+".",instruction]
            if n==46:
                assert panels[1]["lines"]==[english]
        rows.append(row)
    assert provider.reads and bytes(cpu.mem_read(runtime.actor_root,0x1A04))==runtime.actor_bytes
    image=base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON,after)
    target=bytes(image.rom.save())
    image.replace_file(COMMON,common)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    sheet.save(SHEET)
    review=dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES),candidate_sha256=base.digest(ROM),records=rows)
    validate_natural_dialogue_batch(review)
    base.save(PROOF,review|dict(parent_sha256=release["candidate_sha256"],clean_input_sha256=release["clean_input_sha256"],
        target_COMMON_sha256=native.digest(after),entire_parent_inverse=True,allocation=allocation,font=font,
        sheets=[dict(path=str(SHEET),sha256=base.digest(SHEET))],
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE,HISTORY,PENDING,CALLERS,Path(__file__))}))
    print("Reviewed all 23 departure records and rendered the five revised warnings.")


if __name__ == "__main__":
    main()
