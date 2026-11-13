"""Resolve singular-coin stress examples against every original item and native skill bound."""
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R4,UC_ARM_REG_R7,UC_ARM_REG_R8
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/guild_price_domain_v2245')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
BASE=0x02000000
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=((0x4A410,0x4A430),(0x4A55C,0x4A590),(0x7DCC8,0x7DE20),(0x5BEE0,0x5BEF0),(0x5BF68,0x5BF94),(0x5C308,0x5C334),(0x5C474,0x5C478),(0x5C098,0x5C09C),(0x5C0A8,0x5C0AC))
    assert all(arm[a:b]==clean[a:b]for a,b in spans)
    snap=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']
    u,get=get_machine(arm,raw);root=get(0xCB190)
    prices=[dict(item_ID=i,original_native_base_price=get(0x4A410,root+4+i*20))for i in range(218)]
    bases=sorted({r['original_native_base_price']for r in prices});assert min(bases)==100 and max(bases)==420000
    clamps=[]
    for v in(-2**31,-1,0,1,499,500,501,2**31-1):
        u.reg_write(UC_ARM_REG_R4,v&0xFFFFFFFF);u.emu_start(BASE+0x7DDFC,BASE+0x7DE10,count=20)
        result=u.reg_read(UC_ARM_REG_R4);assert result==max(0,min(v,500));clamps.append(dict(supplied_preclamp=v,native_ability=result))
    ranges=[];buy_min,sell_min,plain_sell_min=2**32,2**32,2**32;cases=0
    for base in bases:
        buys=[];sells=[]
        u.reg_write(UC_ARM_REG_R0,base);u.emu_start(BASE+0x5BEE0,BASE+0x5BEF0,count=20);plain=u.reg_read(UC_ARM_REG_R7);assert plain==(base//10)*8;plain_sell_min=min(plain_sell_min,plain)
        for skill in range(501):
            u.reg_write(UC_ARM_REG_R0,skill);u.reg_write(UC_ARM_REG_R8,base);u.emu_start(BASE+0x5C308,BASE+0x5C334,count=40);buy=u.reg_read(UC_ARM_REG_R8)
            u.reg_write(UC_ARM_REG_R0,skill);u.reg_write(UC_ARM_REG_R7,base);u.emu_start(BASE+0x5BF68,BASE+0x5BF94,count=40);sell=u.reg_read(UC_ARM_REG_R7)
            assert buy==base*(100-skill//50)//100 and sell==base*(80+skill//50)//100
            buys.append(buy);sells.append(sell);cases+=2
        ranges.append(dict(base=base,buy_min=min(buys),buy_max=max(buys),sale_min=min(sells),sale_max=max(sells),unbargained_sale=plain))
        buy_min=min(buy_min,min(buys));sell_min=min(sell_min,min(sells))
    assert(buy_min,sell_min,plain_sell_min)==(90,80,80)
    save(ROOT/'original_item_prices_skill_clamp_and_English_unit_contract.json',dict(current_ROM=str(ROM),current_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_snapshot=snap,source_clean_exact_spans=[dict(span=[a,b],sha256=sha(arm[a:b]))for a,b in spans],all218_original_native_item_base_prices=prices,source_ability_clamp_cases=clamps,all_source_skill_values0_to500_for_every_distinct_base_price=True,distinct_base_prices=len(bases),native_arithmetic_cases=cases,source_native_price_ranges=ranges,minimum_unbargained_buy=100,minimum_bargained_buy=90,minimum_unbargained_sale=80,minimum_bargained_sale=80,no_multiply_overflow_max_base420000_factor100=True,one_coin_is_not_an_eligible_Guild_item_offer=True,one_coin_numeric_layout_vectors_are_declared_size_stress_not_earned_prices=True,retained_plural_coins_in1072_1073_1083_1086_1095_is_grammatical_for_source_price_domain=True,no_English_runtime_price_or_live_save_change=True,CPU_fragment_scalar_checks_not_actual_bargaining_events=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(items=218,distinct_bases=len(bases),native_price_cases=cases,buy_min=buy_min,sell_min=sell_min,one_coin_eligible=False),flush=True)
