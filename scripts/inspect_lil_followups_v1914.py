"""Inspect next clean exchanges and classify the copied-state RNG predicate."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_followups_after_London_v1914')
INV=Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    inv=read(INV)
    image=NdsImage.open(inv['candidate'])
    clean=NdsImage.open('work/clean.nds')
    arm=image.read_file('/__arm9__.bin')
    raw=Path(inv['snapshot']).read_bytes()
    assert sha(raw)==inv['snapshot_sha256']
    cpu,get=get_machine(arm,raw)
    ev=image.read_file('/data/EV2.DK4')
    owner=BASE+raw.find(ev[:96])-0x34
    names={}
    for n in (0,2,5,13,113):
        cp,q=get_machine(arm,raw)
        town=q(0xCB178)+4+n*108
        vt=struct.unpack('<I',cp.mem_read(town,4))[0]
        fn=struct.unpack('<I',cp.mem_read(vt+8,4))[0]
        pointer=q(fn-BASE,town)
        names[n]=bytes(cp.mem_read(pointer,100)).split(b'\0')[0].decode('cp932')
    get(0xCC9A8,0x02640080,get(0xCB1B4))
    before=bytes(cpu.mem_read(BASE,0x400000))
    writes=[]
    def write(c,access,address,size,value,user):
        if BASE<=address<BASE+0x400000:writes.append(dict(PC=c.reg_read(UC_ARM_REG_PC),address=address,bytes=size,value=value))
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    result=get(0x220D8,owner,inv['all336_original_events'][80]['actual_native_event_pointer'],0x02640080,0)
    after=bytes(cpu.mem_read(BASE,0x400000))
    assert len(writes)==1 and writes[0]['PC']==BASE+0xD984C and writes[0]['address']==0x02168EB8
    multiplier,increment=struct.unpack_from('<2I',arm,0xD985C)
    seed_before=struct.unpack_from('<I',before,0x168EB8)[0]
    seed_after=struct.unpack_from('<I',after,0x168EB8)[0]
    assert seed_after==(seed_before*multiplier+increment)&0xffffffff
    assert all(BASE+i in range(0x02168EB8,0x02168EBC) for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b)
    current_blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    clean_blocks=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    packets=[]
    for number in (25,30,58,61,128):
        jp,current=clean_blocks[number],current_blocks[number]
        original,speeches=inventory(clean.read_file('/__arm9__.bin'),jp)
        now,spoken=inventory(arm,current)
        shape=lambda rs:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in rs]
        assert shape(original)==shape(now)
        rows=[]
        for a,b in zip(speeches,spoken,strict=True):
            ja,at=a['offset']+5,b['offset']+5
            source=jp[ja:jp.index(b'\0',ja)]
            english=current[at:current.index(b'\0',at)]
            assert source[:1]==english[:1]
            prefix=source[:1].hex()
            ident=f'DK4_MES_B{number:02d}_R{jp[:ja].count(bytes([0])):04d}'
            rows.append(dict(id=ident,source_offset=ja,current_offset=at,source_hex=source.hex(),current_hex=english.hex(),
                provisional_first_byte_hex=prefix,source_Japanese_after_first_byte=source[1:].decode('cp932'),
                current_English_after_first_byte=english[1:].decode('cp932'),
                complete_source_preamble_hex=jp[ja-5:ja+1].hex(),ancestor_0100_offsets=a['ancestor_0100_offsets'],
                new_scene_presentation_scope_not_yet_approved=True))
        packets.append(dict(block=number,source_block_sha256=sha(jp),current_block_sha256=sha(current),
            native_commands=len(original),speeches=len(rows),all_clean_native_commands=original,
            all_current_native_commands=now,records=rows,source_event=inv['all336_original_events'][number]))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_followup_packets_and_random_query_classification.json',dict(candidate=inv['candidate'],
        candidate_sha256=inv['candidate_sha256'],snapshot=inv['snapshot'],snapshot_sha256=inv['snapshot_sha256'],
        town_names=names,packets=packets,
        event80=dict(result=result,WRAM_writes=writes,seed_before=seed_before,seed_after=seed_after,
            multiplier=multiplier,increment=increment,only_original_LCG_word_changes_on_disposable_copy=True),
        B25_event128_incomplete_not_assumed_next=True,no_live_RNG_or_state_changes=True,
        no_source_prose_review_orcompletion_credit_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('TOWNS',names)
    print('RNG80',dict(result=result,writes=len(writes),only_disposable_copy=True))
    for p in packets:
        print('SCENE',p['block'],'SPEECHES',p['speeches'],'COMMANDS',p['native_commands'])
        for r in p['records'][:4]:print(r['id'],r['provisional_first_byte_hex'],r['source_Japanese_after_first_byte'],r['current_English_after_first_byte'])
