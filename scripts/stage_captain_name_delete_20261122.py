"""Stage and exercise captain-name deletion using the ordinary Hodram editor snapshot."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.patch import captain_name_delete as patch
from scripts import observe_hodram_custom_names_20261122 as run
from scripts import stage_rafael_deck_tutorial_followup_20261122 as precedent
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_rafael_custom_name_20261119 import EDITOR, snapshot


base, parent, native = run.base, run.current, run.current.native
ROOT = run.ROOT/"delete_staged"
ROM = ROOT/"Captain_Name_Delete_STAGED.nds"
PROOF = ROOT/"stored_proof.json"
PATCH, REBUILT = ROOT/"translation.xdelta",ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT/"startup/capture/capture_report.json"
OLD_NAME_RELEASE = Path("releases/all_routes_editorial_20261119_captain_name_latin_candidate_v2/verification/registered_release_verification.json")
OLD_PLAN = Path("E:/Rota Nova translations/Generated/work/captain_name_latin_20261119_autoload_v2/native_and_stored.json")
BASELINE = run.ROOT/"capture/capture_report.json"
FIELD = EDITOR+0xB4
CHILD = EDITOR+0x38


def checked_cases(arm, ready, baseline):
    # Use the real widget and stock delete/strlen. Bridge the two redraw boundaries for the isolated matrix.
    uc = machine(arm)
    raw,receipt = snapshot(baseline["read_only_pause_RAM_snapshots"],6570,"sha256")
    uc.mem_write(BASE,raw)
    assert unpack_from("<I",raw,EDITOR+4-BASE)[0]==patch.CAPTAIN_PROVIDERS
    assert bytes(uc.mem_read(ready["entry"],ready["size"])).hex()==ready["helper_hex"]
    assert bytes(uc.mem_read(FIELD,17))==b"HodramFIFIFIFIFI\0"
    assert unpack_from("<I",raw,CHILD+0xA0-BASE)[0]==16
    original = bytes(uc.mem_read(CHILD,0xA8))
    trace = []

    def bridge(u, address, size, _):
        assert u.reg_read(UC_ARM_REG_R0)==CHILD
        if address == patch.MOVE_CURSOR:
            n=u.reg_read(UC_ARM_REG_R1)
        elif address == patch.MOVE_CURSOR_END:
            n=len(bytes(u.mem_read(FIELD,19)).split(b"\0",1)[0])
        else:
            n=None
        trace.append((address,n))
        if n is not None:
            u.mem_write(CHILD+0x40,pack("<I",n))
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))

    for address in (patch.MOVE_CURSOR,patch.MOVE_CURSOR_END,patch.REDRAW):
        uc.hook_add(UC_HOOK_CODE,bridge,begin=address,end=address)
    examples=("", "FI", "FIFI", "BergstromFIFAFOF", "カ", "FoカI", "カFゆ", "ｶI", "MＩA", "F"*17+"I")
    results=[]
    for text in examples:
        data=text.encode("cp932")
        for index in range(len(text)+1):
            cursor=len(text[:index].encode("cp932"))
            wanted=(text[:index-1]+text[index:] if index else text[1:]).encode("cp932")
            new_cursor=len(text[:max(0,index-1)].encode("cp932"))
            cap=18 if len(data)>16 else 16
            before=bytearray(original)
            before[0x7c:0xa0]=data+b"\0"+bytes([0xA5])*(0x23-len(data))
            before[0x40:0x44]=pack("<I",cursor)
            before[0xa0:0xa4]=pack("<I",cap)
            uc.mem_write(CHILD,bytes(before))
            trace.clear()
            instructions=call(uc,ready["entry"]-BASE,(CHILD,))
            assert uc.reg_read(UC_ARM_REG_R0)==int(bool(text)), (text,index)
            actual=bytes(uc.mem_read(CHILD,0xA8))
            body=actual[0x7c:0xa0]
            assert body.split(b"\0",1)[0]==wanted,(text,index,wanted,body.hex())
            assert body[len(data)+1:]==before[0x7c+len(data)+1:0xa0]
            assert unpack_from("<I",actual,0x40)[0]==new_cursor
            assert actual[:0x40]==before[:0x40] and actual[0x44:0x7c]==before[0x44:0x7c]
            assert actual[0xa0:]==before[0xa0:]
            assert trace[-1]==(patch.REDRAW,None) and sum(pc==patch.REDRAW for pc,_ in trace)==1
            if text and len(text[max(0,index-1)].encode("cp932"))==2:
                assert patch.STOCK_DELETE in instructions
            results.append(dict(input=text,cursor=cursor,result=wanted.decode("cp932"),result_cursor=new_cursor,
                byte_limit=cap,native_stock_path=patch.STOCK_DELETE in instructions))
    stock, village=0x0215591C,0x01FF9E38
    fallbacks=[]
    for marker in (stock,village):
        uc.mem_write(EDITOR+4,pack("<I",marker))
        starts=bytearray(original)
        buffer=b"FIFI\0"
        starts[0x7c:0x7c+len(buffer)]=buffer
        starts[0x40:0x44]=pack("<I",4)
        memory=[]
        for entry in (patch.STOCK_DELETE,ready["entry"]):
            uc.mem_write(CHILD,bytes(starts))
            trace.clear()
            executed=call(uc,entry-BASE,(CHILD,))
            assert patch.STOCK_DELETE in executed
            memory.append((bytes(uc.mem_read(CHILD,len(starts))),list(trace),uc.reg_read(UC_ARM_REG_R0)))
        assert memory[0]==memory[1]
        fallbacks.append(dict(provider=marker,byte_exact_to_stock=True))
    return dict(baseline_widget=receipt,cases=results,noncaptain_scopes=fallbacks,
        original_cursor_and_redraw_bridged_for_this_matrix=True)


def stage():
    assert not ROOT.exists()
    baseline,source,name_release,owner = map(base.load,(BASELINE,parent.RELEASE,OLD_NAME_RELEASE,OLD_PLAN))
    assert baseline["cold_boot"] and not baseline["savestate_loaded"] and not baseline.get("battery_save_preloaded")
    assert not any(v for k,v in baseline.items() if k.startswith("synthetic_")) and not baseline["callback_errors"]
    assert baseline["ROM_sha256"]==source["candidate_sha256"]==base.digest(parent.ROM)
    assert base.digest(base.REGISTRY)==source["registry_sha256"] and base.digest(parent.MANIFEST)==source["manifest_sha256"]
    assert base.digest(native.CLEAN)==source["clean_input_sha256"]
    historic=Path(name_release["candidate"])
    assert base.digest(historic)==name_release["candidate_sha256"]==owner["candidate_sha256"]
    old_arm=base.NdsImage.open(historic).read_file(native.ARM)
    assert native.digest(old_arm)==owner["target_arm9_sha256"]==name_release["target_ARM9_sha256"]
    historical_section=MainCodeFile(old_arm,BASE).sections[-1]
    assert [historical_section.ramAddress,historical_section.ramAddress+len(historical_section.data)]==owner["autoload_span"]
    owner["registered_provider_and_helpers_hex"]=bytes(historical_section.data).hex()
    clean,target=map(base.NdsImage.open,(native.CLEAN,parent.ROM))
    old=target.read_file(native.ARM)
    updated,helper=patch.stage(old,clean.read_file(native.ARM),owner)
    native_matrix=checked_cases(updated,helper,baseline)
    assert len(native_matrix["cases"])>=40
    files=native.files(target)
    target.replace_file(native.ARM,updated)
    present=native.files(target)
    assert files.keys()==present.keys() and {p for p in files if files[p]!=present[p]}=={native.ARM}
    body=bytes(target.rom.save())
    target.replace_file(native.ARM,old)
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(body)
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),predecessor_sha256=source["candidate_sha256"],
        target_ARM9_sha256=native.digest(updated),source_bound_helper=helper,native_character_deletion=native_matrix,
        whole_parent_inverse=True,macro_like_name_display_defect_remains_open=True,
        older_registered_name_layer=str(OLD_NAME_RELEASE),older_registered_name_layer_sha256=base.digest(OLD_NAME_RELEASE)))


if __name__=="__main__":
    cli=ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","patch","startup"))
    action=cli.parse_args().action
    if action=="stage":
        stage()
    else:
        existing=getattr(precedent,action)
        FunctionType(existing.__code__,existing.__globals__|globals())()

