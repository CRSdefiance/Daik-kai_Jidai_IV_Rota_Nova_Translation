"""Read-only original full eligibility and exact packed-set prefix on copied RAM."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_B24_event_context_v1832')
ROM=Path('out/all_routes_combined_v1807_candidate.nds')
SNAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B24_research_run_v1831_RESEARCH_ONLY/frame_041420_arm9_ram.bin')
BASE=0x02000000
SCRATCH=0x02640000

if __name__=='__main__':
    assert not ROOT.exists()
    current=NdsImage.open(ROM);clean=NdsImage.open('work/clean.nds')
    arm=current.read_file('/__arm9__.bin');oldarm=clean.read_file('/__arm9__.bin')
    ev=current.read_file('/data/EV2.DK4');assert ev==clean.read_file('/data/EV2.DK4')
    ranges=[(0x220D8,0x22ECC),(0x23840,0x238D8),(0x23B88,0x23DE8),(0x2A690,0x2A6C0)]
    assert all(arm[a:b]==oldarm[a:b]for a,b in ranges)
    raw=SNAP.read_bytes();assert len(raw)==0x400000
    header=raw.find(ev[:96]);assert header>=0 and raw.find(ev[:96],header+1)<0
    owner=BASE+header-0x34
    cpu,get=get_machine(arm,raw)
    assert list(struct.unpack('<2I',cpu.mem_read(owner+0x2454,8)))==[5,3]
    assert get(0x2E58C)==2
    fleet=get(0xCB1A8)+4+2*132
    assert bytes(cpu.mem_read(fleet+0x3C,1))==b'\x03'
    get(0x23888,SCRATCH,owner+4,24)
    pointer=struct.unpack('<I',cpu.mem_read(SCRATCH,4))[0]
    original=bytes(cpu.mem_read(pointer,28))
    # Runtime word0 includes original bookkeeping bits; remaining source bytes exact.
    spec=read('work/analysis/lil_followup_inventory_v1821b/source_event_state_and_dependency_inventory.json')['all336_original_events'][24]
    assert spec['must_be_completed']==[120] and spec['SC2_action_block']==24
    assert original[4:]==bytes.fromhex('07ff00cb00017800ffffff00000001010000000010000e00')
    assert original[12:16]==bytes.fromhex('ffffff00')
    packed=struct.unpack_from('<I',original,12)[0]
    # Source flag27 follows the dependency prefix and decodes this packed set.
    assert struct.unpack_from('<I',original,4)[0]&(1<<27)
    expected=[0]*8
    ids=[(packed>>(8*i))&255 for i in range(4)]
    for value in ids:
        if value!=255:expected[value//32]|=1<<(value%32)
    cpu.mem_write(SCRATCH+0x100,struct.pack('<I',packed))
    get(0x23D34,SCRATCH+0x120,SCRATCH+0x100)
    decoded=list(struct.unpack('<8I',cpu.mem_read(SCRATCH+0x124,32)))
    assert decoded==expected==[1,0,0,0,0,0,0,0]
    get(0x22E98,SCRATCH+0x160,owner+4)
    native_set=list(struct.unpack('<8I',cpu.mem_read(SCRATCH+0x164,32)))
    independent=list(struct.unpack('<8I',raw[owner-BASE+12:owner-BASE+44]))
    assert native_set==independent and native_set[0]&1
    get(0x23C1C,SCRATCH+0x1A0,SCRATCH+0x160,SCRATCH+0x120)
    intersection=list(struct.unpack('<8I',cpu.mem_read(SCRATCH+0x1A4,32)))
    assert intersection==[a&b for a,b in zip(decoded,native_set,strict=True)]
    assert get(0x23B88,SCRATCH+0x1A0)==0
    assert bytes(cpu.mem_read(BASE,0x400000))==raw
    cases=[]
    for town,clear_bit,expected_result in [(3,False,0),(2,False,1),(4,False,1),(2,True,0)]:
        cpu,get=get_machine(arm,raw)
        # Counterfactual inputs exist only in independent offline Unicorn memory.
        # The live DeSmuME test is never modified by these context queries.
        cpu.mem_write(fleet+0x3C,bytes([town]))
        cpu.mem_write(owner+0x2458,struct.pack('<I',town))
        if clear_bit:
            value=struct.unpack('<I',cpu.mem_read(owner+12,4))[0]
            cpu.mem_write(owner+12,struct.pack('<I',value&~1))
        get(0xCC9A8,SCRATCH+0x80,get(0xCB1B4))
        before=bytes(cpu.mem_read(BASE,0x400000))
        result=get(0x220D8,owner,pointer,SCRATCH+0x80,0)
        assert result==expected_result and bytes(cpu.mem_read(BASE,0x400000))==before
        cases.append({'offline_town':town,'offline_owner_bit0_cleared':clear_bit,
                      'full_original_predicate_result':result,'predicate_all4MiB_unchanged':True})
    ROOT.mkdir(parents=True)
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    (ROOT/'original_full_predicate_and_set_helpers.txt').write_text('\n'.join(
        f'{i.address:08X} {i.mnemonic} {i.op_str}'
        for a,b in ranges for i in dis.disasm(arm[a:b],BASE+a)),encoding='utf-8')
    save(ROOT/'original_full_event24_and_packed_set_prefix.json',{
        'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'EV2_sha256':sha(ev),'snapshot':str(SNAP),'snapshot_sha256':sha(raw),
        'original_source_code_ranges_equal_clean':ranges,'event24':spec,
        'owner':owner,'original_category_and_context':[5,3],
        'source_prefix_hex':original[12:16].hex(),'source_prefix_word':packed,
        'source_flag27_requires_nonempty_intersection_with_original_owner_set':True,
        'native_packed_set_members':[v for v in ids if v!=255],
        'native_owner_set_words':native_set,'native_intersection_words':intersection,
        'whole_original_full_predicate_cases':cases,
        'no_hidden_context_relocation_or_script_bytes_changed':True,
        'counterfactuals_only_disposable_offline_RAM_not_live_gameplay':True,
        'original_flags_macros_and_event_outcomes_preserved_in_research_ROM':True,
        'live_B24_activation_display_and_return_still_pending':True,
        'not_actual_visits_to_counterfactual_towns':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'original_prefix_members':[v for v in ids if v!=255],'full_predicate_cases':len(cases),
           'Bruges_fails_other_towns_pass_original_bit0_required':True},flush=True)
