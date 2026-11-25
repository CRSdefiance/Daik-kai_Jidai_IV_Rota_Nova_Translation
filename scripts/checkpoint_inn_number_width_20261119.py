"""Locate the remaining wide numeral substitutions before changing their display."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from scripts import stage_inn_conversations_20261119 as stage
from scripts.verify_personal_gameplay_v841 import get_machine

base,native = stage.base,stage.native
BASE = 0x02000000
NUMBER = 0x020ABF50
MONTH = 0x0205CA8C
CALLS = {0x0205CAEC,0x0205CB0C,0x0205D274}
RECEIPT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/inn_number_width_20261119_v1.json")


def calls(section):
    results = []
    for i in range(0,len(section.data)-3,4):
        value, = unpack_from("<I",section.data,i)
        if value & 0x0F000000 != 0x0B000000 or value >> 28 == 15:
            continue
        offset = value & 0x00FFFFFF
        signed = offset - 0x01000000 if offset & 0x00800000 else offset
        pc = section.ramAddress+i
        if pc+8+4*signed==NUMBER:
            results.append(dict(address=pc,word_hex=section.data[i:i+4].hex()))
    return results


def main():
    assert not RECEIPT.exists()
    review,release = map(base.load,(stage.PROOF,stage.parent.RELEASE))
    assert base.digest(stage.ROM)==review["candidate_sha256"]
    assert base.digest(stage.CLEAN)==review["clean_input_sha256"]
    runtime = stage.workflow.RegisteredRuntime(stage.parent.RELEASE,release["own_registered_startup"],captain=3)
    clean = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    assert arm==runtime.arm
    assert arm[NUMBER-BASE:NUMBER-BASE+0x70]==clean[NUMBER-BASE:NUMBER-BASE+0x70]
    assert arm[MONTH-BASE:0x5CB28]==clean[MONTH-BASE:0x5CB28]
    assert arm[0x5D1A8:0x5D2AC]==clean[0x5D1A8:0x5D2AC]
    source_calls, active_calls = ([x for s in MainCodeFile(a,BASE).sections for x in calls(s)] for a in (clean,arm))
    assert CALLS <= {r["address"] for r in active_calls} and len(active_calls)>len(CALLS)
    assert all(r in source_calls for r in active_calls if r["address"] in CALLS)
    cpu,get = get_machine(arm,runtime.raw)
    event = 0x02450000
    wide = str.maketrans("0123456789","０１２３４５６７８９")

    numbers = []
    for nights in (3,10,30):
        ptr = get(NUMBER-BASE,nights)
        text = bytes(cpu.mem_read(ptr,16)).split(b"\0")[0].decode("cp932")
        assert text==str(nights).translate(wide)
        numbers.append(dict(choice=nights,current_text=text,proposed_text=str(nights),return_pointer=ptr))
    months = []
    for now in range(12):
        for then in range(12):
            cpu.mem_write(event,bytes(8)+bytes([then])+bytes(3))
            delta = (now-then)%12
            p = get(MONTH-BASE,0,event,now)
            text = bytes(cpu.mem_read(p,32)).split(b"\0")[0].decode("cp932")
            expected = "This month" if delta==0 else "Last month" if delta==1 else str(delta).translate(wide)+" months ago"
            assert text==expected
            months.append(dict(current_month=now,event_month=then,delta=delta,current_text=text,
                proposed_text=text if delta<2 else f"{delta} months ago"))
    affected = [r for r in review["records"] if r["message_ID"] in (1180,1195,1196,1197,1198)]
    assert len(affected)==5 and sum(r["current_text"]!=r["proposed_text"] for r in months)==120
    base.save(RECEIPT,dict(candidate_sha256=review["candidate_sha256"],arm9_sha256=native.digest(arm),
        exact_common_records=[{k:r[k] for k in ("message_ID","source_reference","staged_reference","staged_hex")} for r in affected],
        original_numeric_formatter=NUMBER,original_month_caller=MONTH,
        original_inn_formatter_call_sites=sorted(CALLS),aligned_ARM_BL_census=active_calls,
        census_scope="All ARM9 SDK sections. The Inn call sites match the clean original.",
        number_choices=numbers,calendar_cases=months,native_only=True,changed_ROM_bytes=0,
        required_followup="Scope any digit-width change to the three Inn calls. Preserve the number, the same/last month cases, and every other user of the shared formatter.",
        evidence={str(p):base.digest(p) for p in (stage.PROOF,stage.parent.RELEASE,Path(__file__))}))
    print(f"{len(active_calls)} aligned main-code number calls. Reproduced 3 wide stay lengths and 120 wide date substitutions.")


if __name__=="__main__":
    main()
