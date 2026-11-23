"""Review the visible Trade panel labels and allocate their complete native cells."""

from itertools import combinations
from pathlib import Path
from struct import pack, pack_into, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_MEM, ARM_REG_PC

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import observe_trade_label_layout_20261119 as observe
from scripts import register_inn_numerals_20261119 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime

base,native = parent.base,parent.native
ARM,COMMON,CLEAN,PENDING = parent.stage.ARM,parent.stage.COMMON,parent.stage.CLEAN,parent.stage.PENDING
BASE,ATLAS = 0x02000000,(256,96)
ROOT = observe.replay.ROOT/"staged_v1"
ROM,PROOF = ROOT/"Trade_Labels_STAGED.nds",ROOT/"staged.json"
TRACE = observe.replay.ROOT/"baseline_trace"
LAYOUT = 0x159A5C
LABELS = (
    (0x159FA4,8,0x0C1FFC,0x0C1374,0x28,"総収入","Income","Income","Keep the plain heading for proceeds from the pending sale."),
    (0x159FAC,8,0x0C2000,0x0C1398,0x44,"総支出","Spent","Spent","Keep the direct label for outgoing money. It remains distinct from the proceeds and running total."),
    (0x159FB4,8,0x0C2004,0x0C13BC,0x60,"合計","Sum","Total","Total is the natural label for the projected balance below the income and spending rows."),
    (0x159FBC,8,0x0C2038,0x0C1878,0x3FC,"交易","Deal","Trade","Use the same name as the Market command that opens this screen."),
    (0x159FC4,8,0x0C203C,0x0C189C,0x418,"収支","Net","Ledger","The panel lists current funds, income, spending and the total. Ledger describes the whole account panel."),
    (0x159FCC,12,0x0C2040,0x0C18C0,0x434,"選択船名","Ship","Ship","The selected ship name appears immediately beneath the heading, so Ship supplies enough context."),
    (0x159FD8,12,0x0C2044,0x0C18E4,0x450,"交易都市","City","City","Keep the concise heading above the city where the trade is taking place."),
    (0x159FE4,12,0x0C2048,0x0C1908,0x46C,"交易品詳細","Goods Info","Goods Info","The panel gives the selected commodity's name, market percentage and arrival calendar."),
    (0x159FF0,8,0x0C2068,0x0C1BB4,0x3A8,"規模","Size","Size","The label describes the city's size classification directly."),
    (0x159FF8,8,0x0C206C,0x0C1BD8,0x3C4,"状態","Status","Status","The current wording describes the city condition. The original four-cell atlas slot crops it, so the full word needs six cells."),
    (0x15A000,8,0x0C2090,0x0C1FC8,0x3E0,"入荷月","Arr.","Arr.","The established compact caption works next to the numbered arrival calendar."),
    (0x15A008,8,0x0C2308,0x0C229C,0x38C,"所持金","Funds","Funds","Keep the established label for the available base funds above the proposed transaction rows."),
)
EXPAND = {
    0x3FC:(113,2,0,72,36,12),
    0x418:(46,18,180,60,36,12),
    0x60:(16,86,204,72,36,12),
    0x3C4:(16,166,216,60,36,12),
}
GLOSSES = {
    "総収入":"Total income from the proposed transactions.",
    "総支出":"Total spending from the proposed transactions.",
    "合計":"The resulting total after income and spending.",
    "交易":"Trading, the same action named by the Market menu.",
    "収支":"The account of incoming and outgoing funds.",
    "選択船名":"The name of the selected ship.",
    "交易都市":"The city where the transaction takes place.",
    "交易品詳細":"Details for the selected trade good.",
    "規模":"The city's size classification.",
    "状態":"The city's current condition.",
    "入荷月":"The months when the good comes into stock.",
    "所持金":"The funds the player has before the proposed transactions.",
}


def occupied(geometry):
    _,_,x,y,width,height = geometry
    return {(i,j) for i in range(x,x+width) for j in range(y,y+height)}


def transform(clean, current, observed):
    start,end = LAYOUT+0x0C,LAYOUT+0x4F8+24
    entries = tuple(range(start,start+46*28,28))
    assert entries[-1]==0x159F54 and entries[-1]+24<=end
    original = {i:unpack_from("<6I",current,i) for i in entries}
    assert all(unpack_from("<6I",clean,i)==row for i,row in original.items())
    installed = original|{LAYOUT+k:v for k,v in EXPAND.items()}
    atlas = {(x,y) for x in range(ATLAS[0]) for y in range(ATLAS[1])}
    for values in (original,installed):
        rectangles = list(map(occupied,values.values()))
        assert all(r<=atlas for r in rectangles)
        assert all(a.isdisjoint(b) for a,b in combinations(rectangles,2))
    new = bytearray(current)
    dis = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    dis.detail = True
    records = []
    for offset,size,field,load,layout,japanese,old,words,note in LABELS:
        assert clean[offset:offset+size]==japanese.encode("cp932").ljust(size,b"\0")
        before = current[offset:offset+size]
        assert before.split(b"\0",1)[0]==old.encode("ascii") and all(b==0 for b in before[len(old):])
        assert unpack_from("<I",clean,field)==unpack_from("<I",current,field)==(offset+BASE,)
        refs = [i for i in range(0,len(current)-3,4) if current[i:i+4]==pack("<I",offset+BASE)]
        assert refs==[field]
        call = 0xC209C if layout==0x3E0 else load+12
        assert clean[load:call+4]==current[load:call+4]
        insn = next(dis.disasm(current[load:load+4],BASE+load))
        operand = insn.operands[1]
        assert insn.mnemonic=="ldr" and operand.type==ARM_OP_MEM and operand.mem.base==ARM_REG_PC
        assert load+8+operand.mem.disp==field
        invoke = next(dis.disasm(current[call:call+4],BASE+call))
        assert invoke.mnemonic=="bl" and invoke.operands[0].imm==0x020D5404
        row = observed[BASE+call+4]
        at = LAYOUT+layout
        assert tuple(row["clip_rect"])==(0,0,*ATLAS) and tuple(row["cursor"])==original[at][2:4]
        assert row["text"]==old and row["pointer"]==BASE+offset
        changed = layout in EXPAND
        assert len(words)<size and 6*len(words)<=installed[at][4]
        if words!=old:
            new[offset:offset+size] = words.encode("ascii").ljust(size,b"\0")
        if changed:
            pack_into("<6I",new,at,*installed[at])
        records.append(dict(id=f"TRADE_LABEL_{offset:X}",file_path=ARM,speaker="Trade panel",context="Trade shows the selected ship and city, proposed monetary movements, and the conditions for the selected goods.",
            source_meaning=GLOSSES[japanese],clean_Japanese=japanese,previous_English=old,english=words,localization_note=note,
            decision="revision" if changed else "retention",wording_changed=old!=words,display_changed=changed,
            source_reference=dict(string_offset=offset,length=size,draw=BASE+call,pointer_field=BASE+field,layout_offset=at),
            current_reference=dict(string_offset=offset,length=size,draw=BASE+call,pointer_field=BASE+field,layout_offset=at),
            source_hex=clean[offset:offset+size].hex(),current_hex=before.hex(),staged_hex=new[offset:offset+size].hex(),
            original_geometry=original[at],staged_geometry=installed[at],observed_original_draw=row,
            review=dict.fromkeys(REQUIRED_REVIEW_GATES,True)))
    inverse = bytearray(new)
    for row in records:
        ref = row["current_reference"]
        offset,size,at = ref["string_offset"],ref["length"],ref["layout_offset"]
        inverse[offset:offset+size] = current[offset:offset+size]
        inverse[at:at+24] = current[at:at+24]
    assert bytes(inverse)==current
    return bytes(new),records


def main():
    assert not ROOT.exists()
    previous,ledger = map(base.load,(parent.RELEASE,base.LEDGER))
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY)==previous["registry_sha256"] and base.digest(CLEAN)==previous["clean_input_sha256"]
    report,trace = map(base.load,(TRACE/"capture/capture_report.json", TRACE/"requests.json"))
    assert report["ROM_sha256"]==previous["candidate_sha256"]
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    assert len(trace["rows"])==12
    image = base.NdsImage.open(parent.ROM)
    clean = base.NdsImage.open(CLEAN)
    arm = image.read_file(ARM)
    target,records = transform(clean.read_file(ARM),arm,{r["caller_LR"]:r for r in trace["rows"]})
    verify_runtime(target,previous)
    image.replace_file(ARM,target)
    data = bytes(image.rom.save())
    image.replace_file(ARM,arm)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    review = dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES),candidate_sha256=native.digest(data),records=records)
    validate_natural_dialogue_batch(review)
    ROOT.mkdir(parents=True)
    ROM.write_bytes(data)
    base.save(PROOF,review|dict(parent_sha256=previous["candidate_sha256"],clean_input_sha256=previous["clean_input_sha256"],
        target_ARM9_sha256=native.digest(target),entire_parent_inverse=True,atlas_bound=list(ATLAS),atlas_rectangles=46,
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE,TRACE/"requests.json",TRACE/"capture/capture_report.json",Path(__file__))}))
    print("Staged twelve reviewed Trade captions, three wording changes and four complete atlas regions.")


if __name__=="__main__":
    main()
