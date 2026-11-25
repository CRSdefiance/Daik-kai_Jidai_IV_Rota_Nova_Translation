"""Check the Port warning with one bounded crew-count change in a disposable save."""

from argparse import ArgumentParser
from io import StringIO
import json
from pathlib import Path
from struct import pack_into, unpack
import sys
from types import FunctionType

from PIL import Image

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as adapter
from scripts import replay_deck_comments_20261119 as boot
from scripts import replay_lisbon_shopkeeper_20261119 as lisbon
from scripts import replay_square_label_wording_20261119 as patch_workflow
from scripts import stage_departure_warnings_20261119 as stage
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.finish_refit_display_v712 import load as load_capture
from scripts.verify_personal_gameplay_v841 import get_machine

base = stage.base
STARTUP = stage.ROOT / "own_startup"
STARTUP_PROOF = stage.ROOT / "own_startup_verification.json"
CAPTURE = stage.ROOT / "lisbon_short_crew_v2"
PLAYBACK = stage.ROOT / "verified_lisbon_departure.json"
HOLDS = (4100,4300)
RETURN = 5200
SCHEDULE = [
    dict(until=3700,buttons=["A"],duration=8,condition_fixture={"port_crew":"one_short"}),
    dict(until=4100,buttons=["A"],duration=8),
    dict(until=4300),
    dict(until=4600,buttons=["B"],duration=8),
    dict(until=4900,buttons=["B"],duration=8),
    dict(until=RETURN,buttons=["B"],duration=8),
    dict(stop=True),
]


def crew_state(arm,raw):
    cpu,get=get_machine(arm,raw)
    assert get(0xB65E4)==11
    fleet=get(0xCB1A8)+4+get(0x2E58C)*0x84
    ships=[get(0x36C94,fleet+12+8*i) for i in range(5)]
    ship,*empty=ships
    assert ship and not any(empty)
    vtable,=unpack("<I",cpu.mem_read(ship,4))
    native_crew,=unpack("<I",cpu.mem_read(vtable+0x28,4))
    assert native_crew==0x020181BC
    return ship,get(0x181BC,ship),get(0xAB1C4,ship)


def fixture(arm,raw,request):
    assert request=={"port_crew":"one_short"} and len(raw)==0x400000
    assert arm==base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    ja=base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert arm[0x181BC:0x181C4]==ja[0x181BC:0x181C4]==bytes.fromhex("b404d0e11eff2fe1")
    assert arm[0x60A68:0x60C28]==ja[0x60A68:0x60C28]
    ship,count,minimum=crew_state(arm,raw)
    assert (count,minimum)==(39,39)
    index=ship+0x44-0x02000000
    target=bytearray(raw)
    pack_into("<H",target,index,minimum-1)
    assert target[:index]==raw[:index] and target[index+1:]==raw[index+1:]
    altered=bytes(target)
    assert crew_state(arm,altered)==(ship,38,39)
    return altered,dict(ship=ship,before_count=count,after_count=minimum-1,minimum_required=minimum,
        changes=[dict(address=ship+0x44,before=count,after=minimum-1)],
        original_native_selector_unchanged=True,all_other_RAM_bytes_exact=True,
        before_RAM_sha256=stage.native.digest(raw),after_RAM_sha256=stage.native.digest(target))


def capture():
    assert not CAPTURE.exists()
    events,_,_,_,donor=lisbon.schedule("lisbon")
    source=Path(donor["source"])
    assert base.digest(source)==donor["source_sha256"]
    inputs=stage.ROOT/"lisbon_inputs.json"
    base.save(inputs,[e for e in events if e["start"]<=2801])
    argv=[harness.__file__,"--rom",str(stage.ROM),"--out",str(CAPTURE),"--battery-save",str(source),
        "--inputs-json",str(inputs),"--touchscreen","--frames",str(RETURN+1),"--capture-every","999999",
        "--capture-at","3200","--pause-at","3200","--dump-capture-ram","--dump-pause-ram","--allow-condition-fixtures"]
    old,stdin,old_argv=adapter.set_condition,sys.stdin,sys.argv
    try:
        adapter.set_condition=fixture
        sys.argv=argv
        sys.stdin=StringIO("".join(json.dumps(c)+"\n" for c in SCHEDULE))
        harness.main()
    finally:
        adapter.set_condition,sys.stdin,sys.argv=old,stdin,old_argv
    assert base.digest(source)==donor["source_sha256"]


def startup():
    FunctionType(boot.startup.__code__,vars(boot)|globals())()


def patch():
    FunctionType(patch_workflow.patch.__code__,vars(patch_workflow)|globals())()


def verify():
    assert not PLAYBACK.exists()
    digest=base.digest(stage.ROM)
    report,shots,receipt=load_capture(CAPTURE,digest,RETURN)
    journal=CAPTURE/"navigation_command_journal.json"
    assert [r["command"] for r in base.load(journal)["commands_received"]]==SCHEDULE
    fixture_row,=report["synthetic_condition_fixtures"]
    assert len(fixture_row["changes"])==1 and fixture_row["frame"]==3200
    ram={}
    for s in report["read_only_pause_RAM_snapshots"]+report["read_only_capture_RAM_snapshots"]:
        raw=Path(s["path"]).read_bytes()
        assert s["read_only_export"] and stage.native.digest(raw)==s["sha256"] and len(raw)==0x400000
        assert ram.setdefault(s["frame"],raw)==raw
    rom=base.NdsImage.open(stage.ROM)
    arm=rom.read_file(stage.ARM)
    target,proof=fixture(arm,ram[3200],{"port_crew":"one_short"})
    assert proof=={k:v for k,v in fixture_row.items() if k!="frame"}
    from dk4tool.dialogue.font_audit import GameAsciiFont
    font=GameAsciiFont.from_arm9(arm)
    row,=(r for r in base.load(stage.PROOF)["records"] if r["message_ID"]==28)
    holds=[dict(frame=frame,lines=body_mask(shots[frame],font,row["revised_native"]["lines"])) for frame in HOLDS]
    assert crew_state(arm,ram[RETURN])==crew_state(arm,target)
    assert shots[RETURN].crop((0,0,256,192)).tobytes()==shots[3200].crop((0,0,256,192)).tobytes()
    sheet=stage.ROOT/"lisbon_departure_warning_and_return.png"
    canvas=Image.new("RGB",(768,384))
    for i,frame in enumerate((*HOLDS,RETURN)):
        canvas.paste(shots[frame],(256*i,0))
    canvas.save(sheet)
    base.save(PLAYBACK,dict(candidate_sha256=digest,normal_return_frame=RETURN,complete_revised_holds=holds,
        fixture=fixture_row,ordinary_input_after_one_byte_crew_fixture=True,natural_activation=False,hardware=False,
        sheets=[dict(path=str(sheet),sha256=base.digest(sheet))],
        evidence={str(p):base.digest(p) for p in (receipt["report"],journal,sheet)}))
    print("Lisbon replay verified two full warning holds and the normal return.")


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("capture","verify","startup","patch"))
    globals()[parser.parse_args().action]()
