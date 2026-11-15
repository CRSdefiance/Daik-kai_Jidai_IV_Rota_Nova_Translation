"""Map24 neighboring ship-loss/surrender reports from clean code and V1430."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.enemy_capture_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_loss_surrender_context_v1439')
ROM = Path('out/all_routes_combined_v1430_candidate.nds')
BASE = 0x02000000
FAMILIES = [
    ('own_ship_capture',2074,0x02117AC0,0x02072988,0x02072990),
    ('own_ship_surrender',2090,0x02117B80,0x02072B34,0x02072B3C),
    ('enemy_ship_surrender',2098,0x02117C60,0x02072B74,0x02072B7C)]

if __name__=='__main__':
    assert not ROOT.exists()
    release = read('work/analysis/enemy_capture_release_v1429/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    clean,rom = NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    source,arm = clean.read_file('/__arm9__.bin'),rom.read_file('/__arm9__.bin')
    common,original_common = rom.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/COMMON/MESFILE.DK4')
    jp,en = common_message_entries(original_common,source),current_entries(common,arm)
    ids = [n for f,first,t,l,c in FAMILIES for n in range(first,first+8)]
    ledger = read('translations/editorial_review_current_v1.json')
    completed = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not set(ids)&(completed|set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    actual = read('work/analysis/enemy_capture_verified_v1435b/actual_capture_and_return_verification.json')
    observed = actual['complete_actual2082_holds'][-1]
    report = read(actual['report']);assert sha(Path(actual['report']).read_bytes())==actual['report_sha256']
    snap = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==observed['frame'])
    raw_path = Path(snap['path']);raw = raw_path.read_bytes()
    assert sha(raw)==snap['sha256']==observed['RAM_sha256'] and len(raw)==0x400000
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM);md.skipdata = True
    spans = [(0x72484,0x7251C),(0x7251C,0x72BE0),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x82428,0x82570)]
    preserved = []
    for lo,hi in spans:
        assert arm[lo:hi]==source[lo:hi]
        preserved.append({'span':[BASE+lo,BASE+hi],'sha256':sha(source[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str}
                for i in md.disasm(source[lo:hi],BASE+lo)]})
    assert next(md.disasm(source[0x726D0:0x726D4],0x020726D0)).op_str=='r4, #1'
    cpu,get = get_machine(arm,raw)
    actors,captain,fleets = get(0xCB184),get(0x7F244),get(0xCB1A8)
    assert get(0x82478,fleets+0x2090,1)==16 and get(0x82428,fleets+0x2090,1)==0
    families = []
    for family,first,table,load,call in FAMILIES:
        assert list(struct.unpack_from('<8I',source,table-BASE))==list(range(first,first+8))
        assert arm[table-BASE:table-BASE+32]==source[table-BASE:table-BASE+32]
        literals = {BASE+o for o in range(0,len(source)-4,4) if struct.unpack_from('<I',source,o)[0]==table}
        loads = []
        for o in range(0,0x130000,4):
            word = struct.unpack_from('<I',source,o)[0]
            if word&0x0F7F0000==0x051F0000:
                literal = BASE+o+8+(word&4095)*(1 if word&0x00800000 else -1)
                if literal in literals:
                    loads.append(BASE+o)
        assert loads==[load]
        assert next(md.disasm(source[call-BASE:call-BASE+4],call)).op_str=='#0x2053d44'
        choices = []
        for identity in range(207):
            if identity==captain:
                continue
            actor = actors+4+identity*32
            voice,number = get(0x7E988,actor),get(0x53F4C,actor,table)
            assert get(0x7EE08,actor)==identity and number==first+voice
            choices.append({'existing_actor_ID':identity,'actor_object':actor,'source_voice':voice,'message_ID':number})
        assert len(choices)==206 and {r['source_voice'] for r in choices}==set(range(8))
        probes = []
        for name in [b'Vestaros',b'Hanse Cog',b'FALCON',b'ICARUS',b'FIFOFOFU',b'F'+b'A'*17]:
            native = consumer(arm,common,raw,{'patches':[]},0x53D44,1,table,name)
            value = en[first+1].text.replace(b'%s',name)
            assert native['input_hex']==value.hex()
            formatted = bytes.fromhex(native['formatted_hex'])
            probes.append({'name_hex':name.hex(),'message_ID':first+1,'native_pipeline':native,
                'source_argument_bytes_preserved_after_macro_and_wrap':b' '.join(formatted.split())==value.strip(),
                'native_formatted_lines':[v.decode('cp932') for v in formatted.split(b'\n')]})
        families.append({'family':family,'first_ID':first,'native_IDs':list(range(first,first+8)),
            'source_table':table,'source_literal_load':load,'source_call':call,
            'original_entry':0x02053D44,'original_parent':0x02053DB8,'selector_stack_offset':0x27C,
            'original_role':1,'all206_existing_actor_choices':choices,
            'earlier_actual_RAM_used_only_for_CPU_role_context_not_these_gameplay_events':True,
            'current_unscoped_role1_argument_probes':probes,
            'original_virtual_name_getter_plus4_to_r2':True})
    selected = set(ids)
    numbers = sorted({n for first in [2074,2090,2098] for n in range(first-2,first+10)})
    records = []
    for n in numbers:
        if n in selected:
            assert jp[n].text.count(b'%s')==en[n].text.count(b'%s')==1
        records.append({'message_id':n,'selected_for_review':n in selected,
            'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},
            'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},
            'current_text_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_and_original_loss_surrender_context.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'families':families,'all24_native_IDs':ids,'all618_existing_actor_voice_selections_verified':True,
        'unchanged_clean_code_spans':preserved,'records_and_immediate_neighbors':records,
        'original_context':'Three mutually exclusive named-ship reports inside original7251C battle-state processing. r4 is initialized to role1. Each branch calls original53D44 with role1,its exact voice table,and the affected ship virtual name getter+4 in r2. Capture uses the source zero-crew branch and party eligibility tests;it is distinct from zero-Hull sinking. Surrender requires the original72484 predicate and party/status/slot branches;the source handles flagship outcomes separately from the named nonflagship surrender reports. Preserve those original tests and RNG.',
        'surrender_predicate_exact_source':'72484 compares virtual getter+24 against half AB8F0,requires virtual getter+28 below AB1C4,and compares original519D4(100) with50*(AB1C4-getter28)/AB1C4. Do not lower Hull/crew or force this probability in an emulator.',
        'source_gloss_cautions':'2091,2103,2105 explicitly express apparent surrender;2099 reports a white flag then infers surrender;2104 relays the enemy ship\'s stated surrender. Do not turn these into unconditional destruction,capture,crew death or whole-fleet capitulation.',
        'argument_contract':'Exactly one affected ship-name C string in r2. No new captain,faction or casualty argument.',
        'original_role1_source_constant_address':0x020726D0,
        'snapshot':str(raw_path),'snapshot_sha256':sha(raw),'snapshot_frame':observed['frame'],
        'original_role1_current_logical_member':16,'physical_FirstMate_slot_empty':True,
        'all_read_only_source_tables_existing_actors_no_fixture_ID_RNG_or_result_edit':True,
        'no_individual_own_capture_or_surrender_gameplay_activation_claimed':True,
        'no_source_prose_formatting_release_or_completion_credit_yet':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('24 named loss/surrender reports mapped:3 exact role1 callers,618 voice selections,and original surrender predicate. No completion credit.',flush=True)
