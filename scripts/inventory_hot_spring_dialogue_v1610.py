"""Clean-source hot-spring13, original voice fallbacks and surrounding context."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hot_spring_source_v1610')
ROM=Path('out/screenshot_text_repairs_20261022_candidate.nds')
SNAPSHOT=Path('E:/Rota Nova translations/Generated/work/emulation_v193/fatigue_recovery_live_v1606_1594/frame_006200_arm9_ram.bin')
IDS=list(range(2275,2288))

if __name__=='__main__':
    assert not ROOT.exists()
    rom,clean,parent=NdsImage.open(ROM),NdsImage.open('work/clean.nds'),NdsImage.open('out/all_routes_combined_v1594_candidate.nds')
    arm,original,common=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    repair=read('translations/screenshot_text_repairs_20261022_release_v1.json')
    assert {p:sha(rom.read_file(p)) for p in repair['target_file_sha256']}==repair['target_file_sha256']
    assert sha(ROM.read_bytes())=='ba0c910644725ef54a3d817b1754a861244c11fe7c95a06974f32440773bbf54'
    config=read('translations/fatigue_status_editorial_release_v1.json')
    en=owned_entries(common,arm,config['directory_sha256']);old=owned_entries(parent.read_file('/COMMON/MESFILE.DK4'),parent.read_file('/__arm9__.bin'),config['directory_sha256'])
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),original)
    assert all(en[n].text==old[n].text for n in range(2269,2295))
    ledger=read('translations/editorial_review_current_v1.json');covered={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}|set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert not covered&set(IDS)
    code=[];md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    for start,end in [(0x7931C,0x793B4),(0x79728,0x797A0),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x116D60,0x116DA0)]:
        assert original[start:end]==arm[start:end]
        code.append({'span':[0x02000000+start,0x02000000+end],'sha256':sha(arm[start:end]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[start:end],0x02000000+start)] if start<0x100000 else []})
    raw=SNAPSHOT.read_bytes();cpu,get=get_machine(arm,raw);actors,captain=get(0xCB184),get(0x7F244);tables=[]
    for table,expected,call in [(0x02116D80,[2275,2276,2277,2278,2279,2280,2281,-1],0x02079338),
        (0x02116D60,[2282,2283,2284,2285,-1,2286,2287,-1],0x0207937C)]:
        assert list(struct.unpack_from('<8i',arm,table-0x02000000))==expected
        choices=[]
        for actor_id in range(207):
            obj=actors+0x19E4 if actor_id==captain else actors+4+32*actor_id
            assert get(0x7EE08,obj)==actor_id
            voice,number=get(0x7E988,obj),get(0x53F4C,obj,table)
            assert number==(expected[voice] if expected[voice]>=0 else expected[0])
            choices.append({'existing_actor_ID':actor_id,'source_voice':voice,'resolved_message_ID':number,'uses_original_minus1_fallback_to_voice0':expected[voice]<0})
        selected=get(0x82478,get(0xCB1A8)+0x2090,1)
        obj=actors+0x19E4 if selected==captain else actors+4+32*selected;number=get(0x53F4C,obj,table)
        native=consumer(arm,common,raw,{'patches':[]},0x53D44,1,table)
        assert native['parent']==0x02053DB8 and native['selector_offset']==0x27C and native['input_hex']==en[number].text.hex()
        tables.append({'table':table,'signed_members':expected,'original_speech_call':call,'logical_role':1,'all207_existing_actor_choices':choices,
            'current_CPU_only_selection':{'existing_actor_ID':selected,'message_ID':number,'pipeline':native},'no_observed_hot_spring_activation_claim':True})
    records=[]
    for n in range(2269,2295):
        records.append({'message_id':n,'selected_hot_spring_dialogue':n in IDS,
            'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
            'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_text_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932')})
    context=('Original Search callback7931C selects discovery speech via role1/table02116D80,then calls signed fatigue helper79728(-15),which displays309 with original requested amount15. '
        'A separate original skill/RNG branch can select role1/table02116D60 relaxation speech,then the original6624C effect and speakerless310 notice. The thirteen selected IDs are two sets of alternative voices,not one sequential conversation. '
        'Discovery lines preserve reported information where Japanese uses youdesu,moyoudesu,ndatte,or rashii. Relaxation lines describe how the bath feels;2285 explicitly says ki ga suru,not a guaranteed zero fatigue total. '
        '2287 jokes that the water does not taste good;do not add a poisoning,drinking accident or gameplay effect. Native -1 table entries fall back to voice0 through53F4C;there is no eighth distinct line to invent. '
        'No selected source record has a printf argument or executable speech macro. Current2275 has full-width leading I from a historical workaround;use normal ASCII only after verifying the inherited literal-I guard and post-expansion formatting. '
        'The snapshot is from the now-verified friendly-village recovery run,not a hot-spring event. CPU role1 selection/loader/printf/macro probes do not establish hot-spring gameplay reachability or completion.')
    ROOT.mkdir(parents=True);save(ROOT/'original_hot_spring13_source_context.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'directory_sha256':config['directory_sha256'],
        'source_code_spans':code,'voice_tables':tables,'records_and_neighbors':records,'source_context':context,
        'snapshot':str(SNAPSHOT),'snapshot_sha256':sha(raw),'all13_selected_texts_exact_to_V1594_while_preserving_later_screenshot_repairs':True,
        'source_prose_native_release_and_actual_hot_spring_completion_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Hot-spring13 source/context:current optional screenshot profile preserved,two original role1 tables414 actor selections,minus1 fallbacks,discovery/-15/follow-up mapped;no gameplay/completion credit.')
