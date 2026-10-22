"""Seven clean retreat messages,actual ship transfer and original caller contract."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.battle_reaction_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/retreat_transfer_context_v1506')
ROM=Path('out/all_routes_combined_v1492_candidate.nds')
BASE,TABLE=0x02000000,0x02117080
IDS=list(range(2683,2690))

if __name__=='__main__':
    assert not ROOT.exists()
    clean,rom=NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    original,arm=clean.read_file('/__arm9__.bin'),rom.read_file('/__arm9__.bin')
    common=rom.read_file('/COMMON/MESFILE.DK4');jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),original)
    en=current_entries(common,arm)
    actual_path=Path('work/analysis/stronger_fleet_return_verified_v1505/actual_declaration_defeat_and_transfer_return.json')
    actual=read(actual_path);assert sha(ROM.read_bytes())==actual['candidate_sha256']
    ledger=read('translations/editorial_review_current_v1.json')
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not set(IDS)&(done|set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    report_path=Path(actual['terminal_report']);report=read(report_path)
    assert sha(report_path.read_bytes())==actual['terminal_report_sha256'] and report['frames']==9200
    snapshots={s['frame']:s for s in report['read_only_pause_RAM_snapshots']}
    raw=Path(snapshots[8600]['path']).read_bytes();after=Path(snapshots[8800]['path']).read_bytes()
    assert sha(raw)==snapshots[8600]['sha256'] and sha(after)==snapshots[8800]['sha256']
    values=list(struct.unpack_from('<8i',original,TABLE-BASE));assert values==[2683,2684,2685,-1,2686,2687,2688,2689]
    assert arm[TABLE-BASE:TABLE-BASE+32]==original[TABLE-BASE:TABLE-BASE+32]
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);md.skipdata=True
    spans=[(0x35150,0x35260),(0x36948,0x3697C),(0x36C70,0x36CB8),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570)]
    code=[]
    for lo,hi in spans:
        assert arm[lo:hi]==original[lo:hi]
        code.append({'span':[BASE+lo,BASE+hi],'sha256':sha(original[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[lo:hi],BASE+lo)]})
    op=lambda pc:next(md.disasm(original[pc-BASE:pc-BASE+4],pc)).op_str
    assert op(0x020351C8)=='#0x2036c94' and op(0x020351D4)=='r1, [r1, #4]'
    assert op(0x020351DC)=='r2, r0' and op(0x020351E4)=='r0, #1' and op(0x020351E8)=='#0x2053d44'
    literal=0x020351E0+8+0x68;assert struct.unpack_from('<I',original,literal-BASE)[0]==TABLE
    cpu,get=get_machine(arm,raw);fleets,actors,captain=get(0xCB1A8),get(0xCB184),get(0x7F244)
    duty=fleets+0x2090;identity=get(0x82478,duty,1);actor=actors+4+identity*32
    assert identity==16 and get(0x7EE08,actor)==16 and get(0x7E988,actor)==1 and get(0x53F4C,actor,TABLE)==2684
    old_model=get(0x36C94,fleets+4+132+12)
    old_models=[get(0x36C94,fleets+4+132+12+8*s) for s in range(5)]
    later,lg=get_machine(arm,after);lf=lg(0xCB1A8);new_model=lg(0x36C94,lf+4+132+12)
    assert new_model==old_models[1] and new_model!=old_model
    vt=struct.unpack('<I',later.mem_read(new_model,4))[0];getter=struct.unpack('<I',later.mem_read(vt+4,4))[0]
    ptr=lg(getter-BASE,new_model);name=bytes(later.mem_read(ptr,64)).split(b'\0')[0];assert name==b'Latina'
    owner,wrapped=[struct.unpack_from('<I',arm,o)[0] for o in [0x552A0,0x54450]]
    template=after[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]
    formatted=after[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
    assert template==en[2684].text==en[2687].text
    native=consumer(arm,common,raw,{'patches':[]},0x53D44,1,TABLE,name)
    assert native['formatted_hex']==formatted.hex() and native['input_hex']==template.replace(b'%s',name).hex()
    choices=[]
    for identity in range(207):
        if identity==captain:continue
        actor=actors+4+32*identity;voice=get(0x7E988,actor);number=get(0x53F4C,actor,TABLE)
        assert number==(values[voice] if values[voice]>=0 else values[0])
        choices.append({'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number})
    assert len(choices)==206 and {r['message_ID'] for r in choices}==set(IDS)
    probes=[]
    for value in [b'Latina',b'FALCON',b'ICARUS',b'FIFOFOFU',b'F'+b'A'*17]:
        result=consumer(arm,common,raw,{'patches':[]},0x53D44,1,TABLE,value)
        body=bytes.fromhex(result['formatted_hex']);expected=en[2684].text.replace(b'%s',value)
        probes.append({'name_hex':value.hex(),'native_pipeline':result,
            'literal_argument_bytes_survive_macro_and_wrap':b' '.join(body.split())==expected.strip()})
    records=[]
    for n in range(2680,2692):
        records.append({'message_id':n,'selected_for_review':n in IDS,
            'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_text_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_original_transfer_context.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'native_IDs':IDS,'source_table':TABLE,'source_signed_voice_members':values,'original_entry':0x02053D44,
        'original_parent':0x02053DB8,'selector_stack_offset':0x27C,'original_role':1,
        'source_literal_load':0x020351E0,'source_call':0x020351E8,'original_code_spans':code,
        'all206_existing_actor_choices':choices,'records_and_immediate_neighbors':records,
        'snapshot':snapshots[8600]['path'],'snapshot_sha256':snapshots[8600]['sha256'],
        'actual_transfer':{'before':snapshots[8600],'during':snapshots[8800],'actual_proof':str(actual_path),
            'actual_proof_sha256':sha(actual_path.read_bytes()),'previous_flagship_model':old_model,
            'replacement_model':new_model,'replacement_original_slot':1,'original_virtual_name_getter':getter,
            'literal_replacement_ship_name_hex':name.hex(),'selected_actual_actor_ID':16,'selected_actual_voice':1,'selected_actual_message_ID':2684,
            'identical_current_English2684_2687_disambiguated_by_original_role_voice_table':True,'native_pipeline':native,
            'complete_native_formatted_hex':formatted.hex(),'original9000_9200_sailing_return_and_four_ships_verified':True},
        'current_unscoped_argument_probes':probes,
        'original_context':'After original flagship incapacitation,this fleet method swaps the chosen surviving ship into slot0,uses its original CShip virtual name getter as the single%s argument,and has logical First Mate role1 speak through53D44/table02117080. It then clears/reassigns duties and installs the existing captain on the replacement ship. This is a transfer to another ship,not a town or port name. No specific sinking or death is asserted by the seven Japanese lines.',
        'no_prose_layout_integration_or_new_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Retreat7:206 source actor selections and actual2684/Gerhard16/Latina transfer mapped. Literal-name probe results:',[(p['name_hex'],p['literal_argument_bytes_survive_macro_and_wrap']) for p in probes])
