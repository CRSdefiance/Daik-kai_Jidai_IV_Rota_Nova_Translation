"""Bind six complete native speech preambles to actual portraits and catalog names."""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_controls_v2039')
RUN=Path('work/analysis/maria_opening_context_v2035')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030')
SOURCE=Path('work/analysis/maria_opening_source_v2034/all38_clean_current_Hangzhou_opening_source.json')
if __name__=='__main__':
    assert not ROOT.exists()
    plan,live,packet=map(read,(RUN/'run_plan.json',RUN/'live_observer_progress.json',SOURCE))
    assert not live['errors']and not live['mismatches'];arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin')
    snapshot=CAP/'frame_004000_arm9_ram.bin';raw=snapshot.read_bytes();assert len(raw)==4194304 and sha(arm)==packet['ARM9_sha256']
    expected={3:'Maria Huamei Li',10:'Xien Yan',11:'Jam Jack Ludwyan',12:'Yukihisa Genjo Shiraki',21:'Ian Dukov',74:'Richard Townsend'}
    controls=[];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
    rows=live['rows'];ROOT.mkdir(parents=True)
    for i,(selector,name)in enumerate(expected.items()):
        cpu,get=get_machine(arm,raw);assert get(0x7F244)==3 and get(0x2434C,selector)==selector
        actors=get(0xCB184);actor=actors+0x19E4 if selector==3 else actors+4+selector*32
        vtable=struct.unpack('<I',cpu.mem_read(actor,4))[0];getter=struct.unpack('<I',cpu.mem_read(vtable+8,4))[0]
        assert getter==0x0207EDD4;address=get(getter-0x02000000,actor)
        found=cstring(bytes(cpu.mem_read(0x02000000,0x400000)),address).decode('cp932');assert found==name
        record=next(r for r in packet['records']if int(r['source_reference']['leading_byte_hex'],16)==selector)
        at=record['provisional_current_reference']['header_offset'];before=next(r for r in rows if r['kind']=='before_command'and r['source']['block']==33 and r['source']['instruction_offset']==at)
        returned=next(r for r in rows if r['kind']=='after_command'and rows[r['entry_row']]==before)
        assert before['source']['whole_resident_payload_exact_ROM']and before['source']['actual_sha256']==packet['current_block_sha256']
        candidates=sorted(p for p in CAP.glob('frame_*_cold_boot.png')if before['frame']<int(p.name.split('_')[1])<returned['frame'])
        assert candidates,(selector,before['frame'],returned['frame'])
        photo=candidates[-1];im=Image.open(photo).convert('RGB');assert im.size==(256,384)
        x,y=256*(i%3),410*(i//3);draw.text((x+3,y+3),f'{selector:02X} / {name}',fill='white');sheet.paste(im,(x,y+22))
        controls.append(dict(selector_hex=f'{selector:02x}',native_actor_ID=selector,native_catalog_name=name,
            catalog_getter_on_separate_disposable_copy_may_write_cache=True,source_record_ID=record['id'],
            exact_source_current_preamble_hex=record['source_reference']['complete_preamble_hex'],
            original_command_before_frame=before['frame'],original_command_return_frame=returned['frame'],
            actual_current_capture=str(photo),capture_sha256=sha(photo.read_bytes()),
            actor_and_full_nameplate_visual_review_pending=True))
    p=ROOT/'six_actual_portraits_and_full_native_nameplates.png';sheet.save(p)
    save(ROOT/'six_source_bound_native_controls_and_catalog.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],
        ARM9_sha256=sha(arm),snapshot=str(snapshot),snapshot_sha256=sha(raw),controls=controls,
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),original_selector=0x0202434C,
        exact_0A_speech_preamble_is_Xien_not_leading_text_LF=True,
        review_sheet=str(p),review_sheet_sha256=sha(p.read_bytes()),visual_review_pending=True,
        live_context_not_terminal_run_proof=True,existing_isolated_system_unlock_not_earned=True,
        no_ROM_profile_or_registry_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(six_controls=[r['selector_hex']for r in controls],full_catalog_names_verified=True,actual_nameplates_review_pending=True))
