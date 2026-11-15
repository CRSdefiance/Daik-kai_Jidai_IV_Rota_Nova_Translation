"""Clean source and original amount/caller context for fatigue status308/309."""
import struct
from dataclasses import asdict
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from ndspy.code import MainCodeFile,loadOverlayTable
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.inspection_status_editorial import current_entries
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_status_source_v1587')
ROM=Path('out/all_routes_combined_v1578_candidate.nds')
BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists()
    rom,clean=NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    release=read('work/analysis/inspection_status_release_v1577/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']
    arm,original=rom.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),original);en=current_entries(common,arm)
    assert jp[308].text.decode('cp932')=='疲労度が\n%s上がりました' and jp[309].text.decode('cp932')=='疲労度が\n%s回復しました'
    spans=[(0x79728,0x797A0),(0x34540,0x34564),(0xABF50,0xABFC8),(0x79274,0x7931C),(0x7931C,0x793B4),
        (0x795A4,0x796A4),(0x79BEC,0x79FD0),(0x7B168,0x7B194),(0x119164,0x119194)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM);md.skipdata=True
    code=[{'span':[BASE+a,BASE+b],'sha256':sha(original[a:b]),'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(original[a:b],BASE+a)]} for a,b in spans]
    units=[('main_section'+str(i),sec.ramAddress,bytes(sec.data)) for i,sec in enumerate(MainCodeFile(original,BASE).sections)]
    units += [('overlay'+str(i),sec.ramAddress,bytes(sec.data)) for i,sec in loadOverlayTable(clean.rom.arm9OverlayTable,lambda _,f:clean.rom.files[f]).items()]
    refs=[];pointers=[]
    for label,base,data in units:
        for off in range(0,len(data)-3,4):
            word=struct.unpack_from('<I',data,off)[0];relative=word&0xffffff
            if relative&(1<<23):relative-=1<<24
            if word>>24==0xEB and base+off+8+4*relative==BASE+0x79728:refs.append({'unit':label,'call':base+off})
        off=data.find(struct.pack('<I',BASE+0x79728))
        while off>=0:pointers.append({'unit':label,'address':base+off});off=data.find(struct.pack('<I',BASE+0x79728),off+1)
    assert sorted(r['call'] for r in refs)==[BASE+x for x in [0x792D4,0x792EC,0x79340,0x795F0]] and not pointers
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/inspection_status_lookout_v1582_1578/frame_006100_arm9_ram.bin');raw=snapshot.read_bytes()
    cpu,get=get_machine(arm,raw);values=[]
    for n in range(101):
        pointer=get(0xABF50,n);value=bytes(cpu.mem_read(pointer,64)).split(b'\0')[0]
        expected=''.join(chr(0xff10+int(c)) for c in str(n))
        assert value.decode('cp932')==expected
        values.append({'amount':n,'original_ABF50_hex':value.hex(),'source_full_width_digits':expected,'actual_source_amount':n in [3,5,10,15],
            'other_values_CPU_only_layout_stress_not_real_event_claim':n not in [3,5,10,15]})
    rows=[{'message_id':n,'source_reference':{k:v for k,v in asdict(jp[n]).items() if k!='text'},'source_hex':jp[n].text.hex(),'source_Japanese':jp[n].text.decode('cp932'),
        'current_reference':{k:v for k,v in asdict(en[n]).items() if k!='text'},'current_text_hex':en[n].text.hex(),'current_English':en[n].text.decode('cp932')} for n in range(305,313)]
    context=('These are speakerless original546B8 system statuses after land search/expedition actions. Signed helper79728 exits for zero;otherwise34540 adds the signed input to current fleet fatigue at+3D and clamps the stored total to0..100. Positive input uses308;negative input uses309 with its positive magnitude. The message formats the requested change,not the new total and not a measured post-clamp difference. All original main/overlay ARM BL references to79728 are four constant call sites: oasis success-5,mirage failure+5,hot spring-15,and friendly-native event-10. A separate original foraging/search-failure branch79F90 adds+3 and directly invokes308 at79FB8. The original ABF50 formatter produces CP932 full-width decimal digits;one real source %s must be preserved. Known actual amounts are3,5,10,15. Values0..100 are CPU-only numeric layout stress,not additional real event values. No points/percent unit,currency,health outcome or actor relationship is supplied by these source messages. Original expedition dispatcher79BEC is called at7B18C after normal Search result2 and selects environmental callbacks through02119164 using original terrain/region/RNG. Hot-spring and mirage outcomes must not be forced to claim actual gameplay. Existing registered modal/literal-F/I hooks remain intact as verified in1572b;no new formatting or cursor code is proposed.')
    ROOT.mkdir(parents=True);target=ROOT/'source_amounts_and_original_expedition_context.json'
    save(target,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'records_and_neighbors':rows,'original_code':code,
        'all_original_main_overlay_direct_helper_callers':refs,'no_aligned_or_unaligned_helper_pointer_aliases':not pointers,
        'code_units_examined':[{'name':label,'base':base,'bytes':len(data),'sha256':sha(data)} for label,base,data in units],
        'original_number_formatter_cases':values,'actual_signed_delta_call_sites':{'020792D4':-5,'020792EC':5,'02079340':-15,'020795F0':-10,'02079FB8':3},
        'snapshot':str(snapshot),'snapshot_sha256':sha(raw),'context':context,'no_actual_fatigue_event_or_review_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger=read('translations/editorial_review_current_v1.json');ledger['next_fatigue_status_source_packet']={'packet':str(target),'packet_sha256':sha(target.read_bytes()),
        'native_message_IDs':[308,309],'status':'source-consumer-and-full-width-numeric-argument-mapped;prose-font-release-actual-pending'}
    ledger['research_checkpoints'].append({'id':'V1587-fatigue-status2-source-context','proof':str(target),'source_prose_reviews_added':0,'completed_entries_added':0,'full_goal_complete':False})
    save('translations/editorial_review_current_v1.json',ledger)
    Path('docs/fatigue_status_v1587_context.md').write_text('# V1587 fatigue status source context\n\n'+context+'\n\nSource/native number formatting is mapped;prose,fonts,registered release and actual fatigue events remain pending. Full goal active.\n',encoding='utf-8')
    print('Original308/309 signed changes,all main/overlay helper callers,full-width0..100 number strings and Search event path mapped;no prose/gameplay completion credit.')
