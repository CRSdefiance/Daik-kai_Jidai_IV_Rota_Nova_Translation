"""CPU-only original HP/attribute/equipment research for a long-duel fixture.

Does not edit a ROM, emulator, source save or captain identity. This is a
counterfactual prerequisite probe, not original gameplay or editorial credit.
"""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/duel_health_limits_v1238')


def main():
    assert not ROOT.exists()
    rom_path=Path('out/all_routes_combined_v1224_candidate.nds')
    arm=NdsImage.open(rom_path).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x7DF58,0x7E1A4),(0x7E750,0x7E788),(0x7E944,0x7E950),
           (0x49DE8,0x49F30),(0x49F30,0x4A0F8),(0x4A5F4,0x4A628),(0x7DCC8,0x7DE20))
    for lo,hi in spans:assert arm[lo:hi]==clean[lo:hi]
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1232_1224/frame_005770_arm9_ram.bin')
    raw=snapshot.read_bytes();cpu,get=get_machine(arm,raw)
    root=get(0xCB184);actors=[root+0x19E4,root+4+32*32]
    assert [get(0x7EE08,a) for a in actors]==[1,32]
    original=[];result=[];owned=set()
    for actor in actors:
        original.append({'actor_ID':get(0x7EE08,actor),'HP':get(0x7E19C,actor),
            'max_HP':get(0x7DF58,actor,0,0),'fencing':get(0x7DCC8,actor,5),
            'attributes':[get(0x7E944,actor,i) for i in range(6)]})
        assert get(0x7E19C,actor)>0
        for index in (0,1):
            before=get(0x7E944,actor,index)
            get(0x7E750,actor,index,1-before)
            assert get(0x7E944,actor,index)==1
            owned.add(actor+8+index)
        # The original delta0 method clamps current HP to its true maximum.
        get(0x7E108,actor,0)
        assert get(0x7E19C,actor)==get(0x7DF58,actor,0,0)>0
        owned.update(range(actor+0x18,actor+0x1A))
    slots=list(cpu.mem_read(actors[0]+0x1B,5))
    assert slots==[219,49,219,219,219]
    item=get(0xCB190)+4+49*20;scratch=0x02470020
    get(0x49DE8,scratch,item)
    assert struct.unpack('<2I',cpu.mem_read(scratch+4,8))==(2,1)
    get(0x4A610,scratch,0)
    assert get(0x49F30,item,scratch,6,0)==1
    get(0x49DE8,scratch,item)
    assert struct.unpack('<I',cpu.mem_read(scratch+4,4))[0]==0
    history=struct.unpack_from('<I',arm,0x4A0EC)[0]
    owned.update(range(actors[0]+0x1B,actors[0]+0x20))
    owned.update(range(item,item+20));owned.update(range(history,history+28))
    for actor in actors:
        result.append({'actor_ID':get(0x7EE08,actor),'HP':get(0x7E19C,actor),
            'max_HP':get(0x7DF58,actor,0,0),'fencing':get(0x7DCC8,actor,5),
            'attributes':[get(0x7E944,actor,i) for i in range(6)]})
    after=bytes(cpu.mem_read(0x02000000,0x400000))
    changes=[0x02000000+i for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b]
    assert all(a in owned for a in changes)
    for off in (0xD9858,0x51A20):
        at=struct.unpack_from('<I',arm,off)[0]
        assert not owned.intersection(range(at,at+4)) and raw[at-0x02000000:at-0x02000000+4]==after[at-0x02000000:at-0x02000000+4]
    assert [r['actor_ID'] for r in result]==[1,32]
    assert [r['attributes'][5] for r in original]==[r['attributes'][5] for r in result]
    ROOT.mkdir(parents=True)
    save(ROOT/'native_health_limit_and_low_fencing_probe.json',{
        'ROM':str(rom_path),'ROM_sha256':sha(rom_path.read_bytes()),'snapshot':str(snapshot),'snapshot_sha256':sha(raw),
        'original':original,'counterfactual':result,'owned_addresses':sorted(owned),'actual_changes':changes,
        'original_attribute_delta_setter':0x0207E750,'original_HP_delta_clamp':0x0207E108,
        'shield49_transferred_to_inventory_through_original49F30':True,
        'original_actor_IDs_luck_RNG_words_and_special_code_unchanged':True,
        'entire4MiB_delta_confined_to_declared_stats_HP_equipment_and_transfer_history':True,
        'CPU_only_no_new_live_fixture_or_gameplay_claim':True,'no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Original',original,flush=True);print('Counterfactual',result,flush=True)


if __name__=='__main__':main()
