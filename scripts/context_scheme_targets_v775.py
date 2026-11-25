"""Original target exclusions and player-only mutable-name getter contract."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R4,UC_ARM_REG_R6,UC_ARM_REG_R9,UC_ARM_REG_PC,UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_scheme_targets_v775')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('out/all_routes_combined_v773_candidate.nds')
    arm=NdsImage.open(path).read_file('/__arm9__.bin')
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x51A28,0x51B44),(0x51BD4,0x51C5C),(0x56F14,0x57058),
           (0x57194,0x571DC),(0x56D8C,0x56DD0),(0x3CF9C,0x3CFEC))
    assert all(arm[a:b]==source[a:b] for a,b in spans)
    context=read('work/analysis/tavern_schemes_editorial_v774/native_context.json')
    raw=Path(context['read_only_snapshot']['path']).read_bytes()
    assert sha(raw)==context['read_only_snapshot']['sha256']
    u=machine(arm)
    u.mem_write(BASE,raw)
    def get(fn,args=()):
        call(u,fn,args)
        return u.reg_read(UC_ARM_REG_R0)
    def ptr(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    factions=get(0xCB160)
    current=get(0x397D8,(factions,))
    officers=get(0xCB184)
    shared=officers+0x1A39
    getters=[]
    for n in range(20):
        obj=factions+4+76*n
        is_player=get(0x3CFC8,(obj,))
        name=get(0x3CF9C,(obj,))
        assert is_player==int(n==current)
        assert name==(shared if n==current else ptr(obj+4))
        getters.append({'faction':n,'is_player':bool(is_player),'name_pointer':name,
                        'uses_mutable_player_name':name==shared})
    def stop(c,p,s,d):c.emu_stop()
    hooks=[u.hook_add(UC_HOOK_CODE,stop,begin=BASE+p,end=BASE+p)
           for p in (0x51C2C,0x51C48,0x51AD0,0x51B38)]
    first=[]
    second=[]
    try:
        for player in range(20):
            for candidate in range(20):
                u.reg_write(UC_ARM_REG_SP,STACK)
                u.reg_write(UC_ARM_REG_R4,candidate)
                u.reg_write(UC_ARM_REG_R6,player)
                u.emu_start(BASE+0x51C24,BASE+0x51C54,count=10)
                excluded=u.reg_read(UC_ARM_REG_PC)==BASE+0x51C48
                assert excluded==(candidate==player)
                first.append({'player':player,'candidate':candidate,'excluded_before_status_getter':excluded})
            for selected in range(20):
                for candidate in range(20):
                    u.reg_write(UC_ARM_REG_SP,STACK)
                    u.mem_write(STACK,struct.pack('<I',selected))
                    u.reg_write(UC_ARM_REG_R9,player)
                    u.reg_write(UC_ARM_REG_R6,candidate)
                    u.emu_start(BASE+0x51ABC,BASE+0x51AD4,count=10)
                    excluded=u.reg_read(UC_ARM_REG_PC)==BASE+0x51B38
                    assert excluded==(candidate in (player,selected))
                    second.append({'player':player,'first_target':selected,'candidate':candidate,
                                   'excluded_before_relationship_filter':excluded})
    finally:
        for h in hooks:u.hook_del(h)
    save(ROOT/'source_contract.json',{'source_ROM_sha256':sha(path.read_bytes()),
        'source_current_spans_exact':spans,'captured_current_faction':current,
        'actual20_name_getter_bindings':getters,'all400_first_target_exclusions':first,
        'all8000_second_target_exclusions':second,
        'first_filter':{'source_current_getter':0x02051C04,'compare_and_exclusion':0x02051C24},
        'second_filter':{'source_current_getter':0x02051A3C,'current_and_first_exclusions':0x02051ABC},
        'original_Tavern_flow':'56F60 calls57194 ->51BD4 first list;Forge Papers56DAC calls51A28 mode4 for second list.',
        'scope':'Native comparison fragments and real current getter. Inputs enumerate all20 hypothetical player IDs,not20 actual route playthroughs.',
        'complete_external_caller_and_name_pointer_mutation_closure_pending':True,
        'no_production_or_gameplay_approval':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('400 first-target and8000 second-target exclusions verified;only the current faction getter uses the editable name. Complete caller closure remains pending.',flush=True)


if __name__=='__main__':main()
