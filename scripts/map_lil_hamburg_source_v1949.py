"""Full B74 source/current context, typed choices and current role/room terms."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Hamburg_source_v1949')
ROM=Path('out/all_routes_combined_v1945_candidate.nds')
PRIOR=Path('work/analysis/lil_Hamburg_arrival_navigation_v1933/full_source_context_uncredited.json')
ACTUAL=Path('work/analysis/lil_Speyer_original_audit_v1935b/original_Hamburg79_Speyer51_and_three_access_fixture_audit.json')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_revised_run_v1938_RESEARCH_ONLY/frame_093780_arm9_ram.bin')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    prior,actual=map(read,(PRIOR,ACTUAL))
    current,clean=NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    source=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[74]
    block=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks[74]
    assert sha(source)==prior['clean_block_sha256']and sha(block)==prior['current_block_sha256']
    arm=current.read_file('/__arm9__.bin')
    original,ja_speeches=inventory(clean.read_file('/__arm9__.bin'),source)
    commands,speeches=inventory(arm,block)
    assert original==prior['all_clean_native_commands']and commands==prior['all_current_native_commands']
    assert len(commands)==123 and len(speeches)==len(ja_speeches)==79
    raw=SNAP.read_bytes()
    receipt=read('work/analysis/lil_Speyer_revised_audit_v1941/revised_Speyer51_choice_and_three_access_fixture_audit.json')
    assert sha(ROM.read_bytes())==receipt['candidate_sha256']
    cpu,get=get_machine(arm,raw)
    selectors={p:get(0x2434C,p)for p in(2,9,14,16,20)}
    assert all(k==v for k,v in selectors.items())and bytes(cpu.mem_read(BASE,0x400000))==raw
    terms=[]
    for index,name in((8,'Boarding Leader'),(9,'Gunner')):
        field=get(0x86314,index)
        pointer=struct.unpack('<I',cpu.mem_read(field,4))[0]
        value=bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
        assert value.rstrip()==name.encode('ascii')
        terms.append(dict(kind='crew-role',native_index=index,original_getter=BASE+0x86314,
            pointer_field=field,pointer=pointer,complete_native_hex=value.hex(),English=name))
    assert bytes(cpu.mem_read(BASE,0x400000))==raw
    cleanarm=clean.read_file('/__arm9__.bin')
    for at,japanese,name in((0x12FFFC,'海兵詰所','Quarters'),(0x130008,'武装砲台','Battery')):
        old,value=cleanarm[at:at+12],arm[at:at+12]
        assert old.split(b'\0')[0].decode('cp932')==japanese and value==name.encode('ascii').ljust(12,b'\0')
        terms.append(dict(kind='ship-room',ARM9_file_offset=at,source_Japanese=japanese,
            source_hex=old.hex(),current_hex=value.hex(),English=name,
            existing_source_locked_release='translations/ship_battery_labels_v1.json'))
    rows=[]
    for jp,now in zip(ja_speeches,speeches,strict=True):
        ja,at=jp['offset']+5,now['offset']+5
        original_text=source[ja:source.index(b'\0',ja)]
        value=block[at:block.index(b'\0',at)]
        prefix=original_text[0]
        assert prefix in(2,9,14,16,20,254)and value[0]==prefix
        assert source[ja-5:ja+1]==block[at-5:at+1]==bytes.fromhex('0040ffff00')+bytes([prefix])
        rows.append(dict(id=f'DK4_MES_B74_R{source[:ja].count(bytes([0])):04d}',file_path='/data/SC2.DK4',block=74,
            record_index=source[:ja].count(b'\0'),source_reference=dict(offset=ja,bytes=len(original_text),header_offset=ja-5),
            current_reference=dict(offset=at,bytes=len(value),header_offset=at-5,record_index=block[:at].count(b'\0')),
            source_hex=original_text.hex(),current_text_hex=value.hex(),source_complete_preamble_hex=source[ja-5:ja+1].hex(),
            source_presentation_prefix_hex=f'{prefix:02x}',source_Japanese=original_text[1:].decode('cp932'),
            current_stored_English=value[1:].decode('cp932'),ancestor_0100_offsets=jp['ancestor_0100_offsets']))
    choices=[]
    for c in commands:
        if c['word']!=0x2100:continue
        assert c['offset']==3504
        for index in(0,1):
            refs=[]
            for data in(source,block):
                at=c['offset']+6+struct.unpack_from('<H',data,c['offset']+2+index*2)[0]
                end=data.index(b'\0',at)
                refs.append(dict(offset=at,bytes=end-at,hex=data[at:end].hex(),text=data[at:end].decode('cp932')))
            choices.append(dict(id=f'DK4_CHOICE_B74_C3504_O{index}',file_path='/data/SC2.DK4',block=74,
                command_offset=3504,option_index=index,source_reference=refs[0],current_reference=refs[1],
                source_hex=refs[0]['hex'],current_text_hex=refs[1]['hex']))
    assert len(choices)==2
    scene=next(r for r in actual['scenes']if r['block']==74)
    assert len(scene['speech_observations'])==79 and not scene['unvisited_speech_IDs']
    ROOT.mkdir(parents=True)
    save(ROOT/'all79_source_native_context_and_two_choices.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),ARM9_sha256=sha(arm),block=74,
        clean_block_sha256=sha(source),current_block_sha256=sha(block),all_clean_native_commands=original,
        all_current_native_commands=commands,records=rows,choices=choices,native_current_terms=terms,
        source_snapshot=str(SNAP),source_snapshot_sha256=sha(raw),all_role_and_selector_queries_preserve4MiB=True,
        actual_original_speeches=79,actual_original_context_proof=str(ACTUAL),actual_original_context_proof_sha256=sha(ACTUAL.read_bytes()),
        B74_unchanged_from_original_V1909_capture_in_registered_V1945=True,
        source_context_focus='Recruitment,manners/wife misunderstanding,defense ofCamille,Gerhard apology,naval-admiral/private-fleet history,reluctant acceptance,title/first-name change,andboth battle-lesson choices areoneexchange. Do not invent literaluncle,formalGrandAdmiral rank,marriage,permanentpast mentorship orretirement.',
        terminology_focus='航海士 are named officers;水夫 are hired sailors. Current UI usesBattery andQuarters,not legacyGun Deck/Marine Quarters. Boarding Leader isrole8;Gunner role9. Preserve sourcecombat rules andautomatic gunfire/boarding without guaranteed victories.',
        source_inventory_not_prose_native_format_orcompletion_credit=True,
        new_B74_scoped_progressive_and_FE_format_approval_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_speeches=79,typed_labels=2,native_commands=123,
        current_terms=[r['English']for r in terms],no_prose_orcompletion_credit=True))
