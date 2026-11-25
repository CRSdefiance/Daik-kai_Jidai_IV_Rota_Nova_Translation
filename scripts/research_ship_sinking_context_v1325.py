"""Bind sinking prose to exact original callers and ship-name substitutions.

Read-only CPU getter tests use existing objects from terminal V1316 RAM.
They are not sinking events or gameplay completion evidence.
"""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.powder_fire_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_context_v1325')
ROM = Path('out/all_routes_combined_v1316_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/powder_fire_v1320_1316')
BASE = 0x02000000
TABLES = [(0x021179C0,2058,0x0207287C,0x02072884,0x02053D44,0x02053DB8,0x27C),
          (0x02117A80,2066,0x02075548,0x02075550,0x02053F0C,0x02053F40,0x274)]


def main():
    assert not ROOT.exists()
    release = read('work/analysis/powder_fire_release_v1315/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    clean,rom = NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    source,arm = clean.read_file('/__arm9__.bin'),rom.read_file('/__arm9__.bin')
    common = rom.read_file('/COMMON/MESFILE.DK4')
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),source)
    en = current_entries(common,arm)
    report = read(CAP/'capture_report.json')
    assert report['frames']==7590 and report['ROM_sha256']==release['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    snapshots = report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']
    snapshot = next(row for row in snapshots if row['frame']==7590)
    raw_path = Path(snapshot['path'])
    raw = raw_path.read_bytes()
    assert len(raw)==0x400000 and sha(raw)==snapshot['sha256']
    cpu,get = get_machine(arm,raw)
    actors,fleets,captain = get(0xCB184),get(0xCB1A8),get(0x7F244)
    role_actor = get(0x82428,fleets+0x2090,1)
    assert get(0x82478,fleets+0x2090,1)==18 and role_actor==actors+4+18*32
    own_mobile = get(0x36C70,fleets+4+132+12)
    native_gunners = [get(0x55DC4,own_mobile,index) for index in range(4)]
    assert actors+4+16*32 in native_gunners
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    spans = [(0x72660,0x72BD8),(0x753F0,0x75560),(0x564C8,0x565B0),
             (0x55DC4,0x55E6C),(0x53D44,0x53DCC),(0x53F0C,0x53F9C),(0x2E5D4,0x2E5F8)]
    preserved = []
    for lo,hi in spans:
        assert source[lo:hi]==arm[lo:hi]
        preserved.append({'source_span':[BASE+lo,BASE+hi],'sha256':sha(source[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for i in md.disasm(source[lo:hi],BASE+lo)]})
    table_rows = []
    for table,first,load,call,entry,parent,stack in TABLES:
        values = list(struct.unpack_from('<8I',source,table-BASE))
        assert values==list(range(first,first+8)) and arm[table-BASE:table-BASE+32]==source[table-BASE:table-BASE+32]
        literals = {BASE+o for o in range(0,0x130000,4) if struct.unpack_from('<I',source,o)[0]==table}
        callers = []
        for o in range(0,0x130000,4):
            word = struct.unpack_from('<I',source,o)[0]
            if word&0x0F7F0000 != 0x051F0000:
                continue
            literal = BASE+o+8+(word&4095)*(1 if word&0x00800000 else -1)
            if literal in literals:
                callers.append(BASE+o)
        assert callers==[load]
        assert next(md.disasm(source[call-BASE:call-BASE+4],call)).op_str==f'#{entry:#x}'
        selections = []
        for identity in range(207):
            if identity==captain:
                continue
            actor = actors+4+identity*32
            voice,number = get(0x7E988,actor),get(0x53F4C,actor,table)
            assert get(0x7EE08,actor)==identity and 0<=voice<8 and number==values[voice]
            selections.append({'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number})
        assert len(selections)==206 and {r['source_voice'] for r in selections}==set(range(8))
        table_rows.append({'table':table,'raw8_voice_table':values,'literal_load':load,'original_call':call,
            'original_native_entry':entry,'original_native_parent':parent,'selector_stack_offset':stack,
            'all206_existing_actor_selections':selections,'no_fallback_holes':True})
    names = []
    for fleet_index in range(63):
        for slot in range(5):
            mobile = get(0x36C70,fleets+4+fleet_index*132+12+slot*8)
            if not mobile:
                continue
            vtable = struct.unpack('<I',cpu.mem_read(mobile,4))[0]
            name_method = struct.unpack('<I',cpu.mem_read(vtable+4,4))[0]
            name_pointer = get(name_method-BASE,mobile)
            name = bytes(cpu.mem_read(name_pointer,80)).split(b'\0')[0]
            assert name and len(name)<64
            names.append({'fleet_index':fleet_index,'ship_slot':slot,'mobile':mobile,
                'native_virtual_name_getter':name_method,'name_pointer':name_pointer,
                'name_hex':name.hex(),'name':name.decode('cp932')})
    assert names and any(n['name']=='Vestaros' for n in names)
    ledger = read('translations/editorial_review_current_v1.json')
    completed = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    pending = set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    records = []
    for number in range(2058,2074):
        assert number not in completed|pending
        assert jp[number].text.count(b'%s')==en[number].text.count(b'%s')==1
        records.append({'message_id':number,
            'source_reference':{k:v for k,v in asdict(jp[number]).items() if k!='text'},
            'source_hex':jp[number].text.hex(),'source_Japanese':jp[number].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[number]).items() if k!='text'},
            'current_text_hex':en[number].text.hex(),'current_English':en[number].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_consumer_binding.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'snapshot':str(raw_path),'snapshot_sha256':sha(raw),'terminal_capture_report':str(CAP/'capture_report.json'),
        'terminal_report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'voice_tables':table_rows,'unchanged_clean_code_spans':preserved,'records':records,
        'source_selected_current_FirstMate_actor':{'role':1,'actor_ID':18,'actor_object':role_actor},
        'source_current_gun_position_actors':native_gunners,'original_live_ship_name_getters':names,
        'argument_contract':'Exactly one original C-string ship name in r2;no added rank,name,faction or numeric argument.',
        'own_loss_context':'Original active-mobile loop tests virtual Hull getter+24==0,sets mobile state0D to1,then processes flagship outcomes separately. When the original side0-or1 predicate2E5D4 permits the later report,virtual name getter+4 supplies%s and role1/53D44 selects2058-2065.',
        'enemy_loss_context':'Original projectile damage path753F0-75560 requires a formerly positive target Hull and zero Hull after original damage. An existing active firing ship must pass5652C while target fails it.55DC4 receives the firing ship and source gun-position index;53F0C selects2066-2073 with the target virtual name getter+4.',
        'neighbor_caution':'The adjacent cleanup branch72990 uses02117AC0/2074-2081 for capture after crew exhaustion;it is not the enemy sinking table02117A80. Do not infer table ownership from adjacency.',
        'no_actual_sinking_activation_or_new_native_layout_or_completion_claimed':True,
        'all_tests_read_only_existing_object_getters_no_identity_RNG_or_result_edits':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'16 exact clean/current records;two original call sites;412 existing voice selections;{len(names)} native ship-name bindings verified. No sinking gameplay claimed.',flush=True)


if __name__=='__main__':
    main()
