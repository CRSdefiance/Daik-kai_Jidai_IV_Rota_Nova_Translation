"""Check the original number callers, substitution layouts and glyphs on the Inn build."""

from collections import defaultdict
from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_tavern_continuation_layout_v768 as formatting
from scripts import stage_inn_numerals_context_20261119 as stage
from scripts.probe_button_prompt_native import STACK
from scripts.verify_personal_gameplay_v841 import get_machine

base,native = stage.base,stage.native
patch = stage.patch
inn = stage.parent.stage
WIDE = "０１２３４５６７８９"
ASCII_DIGITS = str.maketrans(WIDE,"0123456789")
RING = 0x022A44EC
RING_SIZE = 0x100C


def normalize(value):
    return value.decode("cp932").translate(ASCII_DIGITS).encode("cp932")


def read_cstring(cpu, pointer):
    return bytes(cpu.mem_read(pointer,32)).split(b"\0",1)[0]


def return_points(cpu):
    calls = []

    def capture(core,address,size,_):
        pointer = core.reg_read(UC_ARM_REG_R0)
        calls.append((address-4,pointer,read_cstring(core,pointer)))

    for pc in patch.CALLS:
        cpu.hook_add(UC_HOOK_CODE,capture,begin=pc+4,end=pc+4)
    return calls


def comparisons(runtime, arm, installed):
    # Execute over the same regular initialized state and explicitly install only
    # the three instruction differences in the test's main-memory image.
    raw = bytearray(runtime.raw)
    for pc in patch.CALLS:
        at = pc-patch.BASE
        assert raw[at:at+4]==arm[at:at+4]
        raw[at:at+4] = installed[at:at+4]
    old_cpu,old_get = get_machine(arm,runtime.raw)
    new_cpu,new_get = get_machine(installed,bytes(raw))
    old_calls,new_calls = return_points(old_cpu),return_points(new_cpu)
    cpus = (old_cpu,new_cpu)
    ring = bytes(old_cpu.mem_read(RING,RING_SIZE))
    assert ring==bytes(new_cpu.mem_read(RING,RING_SIZE))
    assert unpack_from("<I",arm,0xABFC0)[0]==unpack_from("<I",arm,0x5CB28)[0]==RING

    def prepare(slot):
        for cpu in cpus:
            cpu.mem_write(RING,ring[:8]+pack("<I",slot)+ring[12:])
        old_calls.clear()
        new_calls.clear()

    def compare_ring(ranges):
        old = old_cpu.mem_read(RING,RING_SIZE)
        new = new_cpu.mem_read(RING,RING_SIZE)
        allowed = {i-RING for p,length in ranges for i in range(p,p+length)}
        assert all(12<=i<RING_SIZE for i in allowed)
        assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(old,new,strict=True)))

    numbers = []
    site = patch.CALLS[-1]
    for slot in range(32):
        for amount in (3,10,30):
            prepare(slot)
            results = []
            for cpu in cpus:
                cpu.reg_write(UC_ARM_REG_SP,STACK)
                cpu.reg_write(UC_ARM_REG_R0,amount)
                cpu.emu_start(site,site+8,count=10000)
                assert cpu.reg_read(UC_ARM_REG_PC)==site+8 and cpu.reg_read(UC_ARM_REG_SP)==STACK
                results.append(cpu.reg_read(UC_ARM_REG_R0))
            (before_site,original,prior), = old_calls
            (after_site,pointer,digits), = new_calls
            assert before_site==after_site==site and results==[pointer,pointer] and original==pointer
            assert digits==normalize(prior)==str(amount).encode("ascii")
            assert pointer+len(prior)==RING+12+128*(slot+1)-1
            compare_ring([(pointer,len(digits)+1)])
            numbers.append(dict(choice=amount,ring_slot=slot,old_hex=prior.hex(),current_hex=digits.hex(),pointer=pointer))
    months, sites = [],set()
    event = 0x02450000
    for now in range(12):
        for then in range(12):
            prepare((now*12+then)%32)
            for cpu in cpus:
                cpu.mem_write(event,bytes(8)+bytes([then])+bytes(3))
            pointer_a,pointer_b = (get(stage.lead.MONTH-patch.BASE,0,event,now) for get in (old_get,new_get))
            assert pointer_a==pointer_b
            original = read_cstring(old_cpu,pointer_a)
            digits = read_cstring(new_cpu,pointer_b)
            delta = (now-then)%12
            if delta<2:
                assert digits==original==(b"This month" if delta==0 else b"Last month")
                assert not old_calls and not new_calls
                compare_ring([])
            else:
                assert digits==normalize(original)==f"{delta} months ago".encode("ascii")
                (before_site,old_pointer,before), = old_calls
                (after_site,new_pointer,after), = new_calls
                assert before_site==after_site and old_pointer==new_pointer and normalize(before)==after
                sites.add(after_site)
                compare_ring([(new_pointer,len(after)+1),(pointer_b,len(original)+1)])
            months.append(dict(current_month=now,event_month=then,delta=delta,old_hex=original.hex(),current_text=digits.decode("ascii")))
    assert sites==set(patch.CALLS[:2]) and len(numbers)==96 and len(months)==144
    return new_cpu,numbers,months


def checked_layouts(image, arm, cpu):
    past = {r["message_ID"]:r for r in base.load(stage.parent.REVIEW)["records"]}
    templates = {r["message_ID"]:r for r in base.load(inn.HISTORY)["records"]}
    scope = vars(formatting).copy()
    exec(compile(inn.FORMATTER.read_text(encoding="utf-8"),str(inn.FORMATTER),"exec"),scope)
    raster,independent,oracle_hash = inn.physical_renderers(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    checked, previews, rejected = [],[],[]
    for n in stage.AFFECTED:
        row = past[n]
        words = stage.WORDS if n==stage.REVISED else row["english"]
        template = templates[n]|{"english":words}
        cases, groups = [],defaultdict(list)
        for previous in row["layout_cases"]:
            supplied = tuple(bytes.fromhex(v) for v in previous["source_values_hex"])
            current = (normalize(supplied[0]),*supplied[1:])
            if n==stage.REVISED:
                uncorrected = scope["format_case"](cpu,templates[n]|{"english":row["english"]},current)
                if uncorrected["findings"]:
                    rejected.append(uncorrected)
            case = scope["format_case"](cpu,template,current)
            assert not case["findings"] and len(case["lines"])<=4, (n,case)
            if n==1180:
                groups[current[0]].append(case)
            elif supplied[0]!=current[0] or n==stage.REVISED:
                groups[len(case["lines"]),supplied[0]==current[0]].append(case)
            else:
                assert case["formatted_hex"]==previous["formatted_hex"]
            case["predecessor_arguments_hex"] = previous["source_values_hex"]
            cases.append(case)
        for group in groups.values():
            case = max(group,key=lambda c:len(bytes.fromhex(c["formatted_hex"])))
            raw = bytes.fromhex(case["formatted_hex"])
            events = []
            plane,used = raster(arm,raw,0x01FFCE40-patch.BASE,size=(228,64),complete=False,
                instruction_limit=2000000,glyph_events=events)
            assert used==len(raw) and plane==independent(arm,kanji,case["lines"])
            assert [g["code"] for g in events if g["code"]!=32]==inn.port.glyph_codes(raw)
            assert all(0<=g["x"]<=228-(12 if g["code"]>255 else 6) and 0<=g["y"]<=52 for g in events)
            assert sorted({g["y"] for g in events})==list(range(0,16*len(case["lines"]),16))
            case["native_physical_page_sha256"] = native.digest(plane)
            text = bytes.fromhex(case["source_values_hex"][0]).decode("ascii")
            previews.append((f"{n}   {text}   {len(case['lines'])} rows",plane))
        record = {k:row[k] for k in ("id","message_ID","file_path","speaker","context","source_meaning","english",
            "clean_Japanese","source_reference","current_reference","registered_reference","source_hex","staged_hex",
            "native_binding","native_arguments_in_order","review")}
        record.update(decision="retention",layout_cases=cases,
            localization_note="Retain the reviewed wording, voices and argument order. Only glyph width in the first native argument changes. "
                + row["localization_note"])
        if n==stage.REVISED:
            edit, = base.load(stage.PROOF)["text_changes"]
            record.update(decision="revision",english=words,previous_English=row["english"],
                current_reference=edit["current_reference"],staged_reference=edit["staged_reference"],
                current_hex=edit["previous_hex"],staged_hex=edit["staged_hex"],localization_note=stage.NOTE)
        checked.append(record)
    assert sum(len(r["layout_cases"]) for r in checked)==529
    assert len(rejected)==23 and all(r["lines"][-1]=="do!" and
        r["findings"]==["short_final_row","weak_line_end"] for r in rejected)
    return checked,previews,oracle_hash,rejected


def save_sheets(previews):
    sheets = []
    for start in range(0,len(previews),8):
        batch = previews[start:start+8]
        sheet = Image.new("RGB",(932,152*((len(batch)+1)//2)),"#263238")
        canvas = ImageDraw.Draw(sheet)
        for i,(label,plane) in enumerate(batch):
            x,y = 466*(i%2),152*(i//2)
            canvas.text((x+5,y+3),label,fill="white")
            tile = Image.frombytes("L",(228,64),bytes(0 if p==1 else 180 if p else 255 for p in plane))
            sheet.paste(tile.resize((456,128),Image.Resampling.NEAREST),(x+5,y+21))
        path = stage.ROOT/f"native_numerals_{start//8+1}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path),sha256=base.digest(path),pages=len(batch)))
    return sheets


def main():
    assert not stage.NATIVE_PROOF.exists()
    staged,predecessor = map(base.load,(stage.PROOF,stage.parent.RELEASE))
    runtime = stage.workflow.RegisteredRuntime(stage.parent.RELEASE,predecessor["own_registered_startup"],captain=3)
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(stage.ARM)
    assert base.digest(stage.ROM)==staged["candidate_sha256"] and native.digest(arm)==staged["target_ARM9_sha256"]
    cpu,numbers,months = comparisons(runtime,runtime.arm,arm)
    records,pages,oracle_hash,rejected = checked_layouts(image,arm,cpu)
    review = {k:base.load(stage.parent.REVIEW)[k] for k in ("translation_policy","target_locale","encoder","review_gates")}
    review.update(candidate_sha256=staged["candidate_sha256"],records=records)
    validate_natural_dialogue_batch(review)
    base.save(stage.NATIVE_PROOF,review|dict(stay_number_calls=numbers,calendar_cases=months,layout_cases=529,
        exact_current_active_calls=list(patch.CALLS),regular_digits_in_original_ring_buffer=True,
        visual_pages=len(pages),independent_physical_oracle_sha256=oracle_hash,sheets=save_sheets(pages),
        rejected_orphaned_town_raid_layouts=rejected,
        evidence={str(p):base.digest(p) for p in (stage.PROOF,stage.parent.REVIEW,Path(__file__))}))
    print(f"96 stay number calls, 144 calendar cases, 529 layouts and {len(pages)} native pages verified.")


if __name__=="__main__":
    main()
