"""Clean-source inventory of32 unreviewed battle reactions;caller leads only."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.ship_loss_surrender_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reactions_source_v1478')
BASE=0x02000000
FAMILIES=[('battle_reaction',2147),('eager_reaction',2155),('surprised_reaction',2163),('wounded_reaction',2171)]

if __name__=='__main__':
    assert not ROOT.exists()
    clean_path=Path('work/clean.nds');rom_path=Path('out/all_routes_combined_v1456_candidate.nds')
    clean,rom=NdsImage.open(clean_path),NdsImage.open(rom_path)
    original,arm=clean.read_file('/__arm9__.bin'),rom.read_file('/__arm9__.bin')
    common,source_common=rom.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/COMMON/MESFILE.DK4')
    release=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    assert sha(rom_path.read_bytes())==release['candidate_sha256']
    assert sha(clean_path.read_bytes())==release['clean_input_sha256']
    jp,en=common_message_entries(source_common,original),current_entries(common,arm)
    ledger=read('translations/editorial_review_current_v1.json')
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    selected=set(range(2147,2179));assert not selected&(done|set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/loss_surrender_control_v1461b_1456')
    report=read(cap/'capture_report.json');snapshot=next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame']==13200)
    raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256']
    cpu,get=get_machine(arm,raw);actors=get(0xCB184);captain=get(0x7F244)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);families=[]
    for family,first in FAMILIES:
        pattern=struct.pack('<8I',*range(first,first+8));at=original.find(pattern)
        assert at>=0 and original.find(pattern,at+1)<0 and arm[at:at+32]==pattern
        table=BASE+at;references=[]
        literals={BASE+i for i in range(0,len(original)-3,4) if struct.unpack_from('<I',original,i)[0]==table}
        for offset in range(0x800,min(0x130000,len(original)-3),4):
            word=struct.unpack_from('<I',original,offset)[0]
            if word&0x0F7F0000!=0x051F0000:continue
            literal=BASE+offset+8+(word&4095)*(1 if word&0x00800000 else -1)
            if literal not in literals:continue
            lo,hi=max(0x800,offset-96),min(len(original),offset+160)
            assert arm[lo:hi]==original[lo:hi]
            references.append({'load':BASE+offset,'literal':literal,'preserved_window_sha256':sha(original[lo:hi]),
                'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[lo:hi],BASE+lo)]})
        assert references
        choices=[]
        for identity in range(207):
            if identity==captain:continue
            actor=actors+4+identity*32;voice=get(0x7E988,actor);number=get(0x53F4C,actor,table)
            assert get(0x7EE08,actor)==identity and number==first+voice
            choices.append({'existing_actor_ID':identity,'voice':voice,'message_ID':number})
        assert len(choices)==206 and {r['voice'] for r in choices}==set(range(8))
        families.append({'family_lead':family,'first_ID':first,'table':table,'native_message_IDs':list(range(first,first+8)),
            'all206_existing_actor_choices':choices,'original_PC_relative_reference_leads':references,
            'enclosing_function_and_runtime_consumer_not_yet_approved':True})
    records=[]
    for n in range(2145,2181):
        records.append({'message_ID':n,'selected':n in selected,
            'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'source_hex':jp[n].text.hex(),
            'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_hex':en[n].text.hex(),
            'current_English':en[n].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_inventory.json',{'source_ROM':str(clean_path),'source_ROM_sha256':sha(clean_path.read_bytes()),
        'candidate':str(rom_path),'candidate_sha256':release['candidate_sha256'],'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'snapshot':snapshot,'families':families,'records':records,'native_actor_selections':824,
        'context_prose_native_layout_and_original_event_approval_pending':True,
        'no_ledger_prose_count_ROM_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('32 clean/current battle-reaction records,four source tables,824 existing-actor selections;caller/context/prose gates remain open.')
    for f in families:print(f['family_lead'],hex(f['table']),[hex(r['load']) for r in f['original_PC_relative_reference_leads']])
