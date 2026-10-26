"""Current source fee/night domains and complete Palace menu label providers."""
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_PC,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/palace_inn_domains_v2254')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    doc=read('translations/palace_inn_contextual_editorial_manuscript_v1.json');rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];raw=Path(snapshot['path']).read_bytes();assert sha(raw)==snapshot['sha256'];u,get=get_machine(arm,raw)
    assert arm[0x5D1A8:0x5D2AC]==clean[0x5D1A8:0x5D2AC]and arm[0x5E004:0x5E03C]==clean[0x5E004:0x5E03C]
    u.reg_write(UC_ARM_REG_SP,STACK);u.emu_start(BASE+0x5D1DC,BASE+0x5D1EC,count=10)
    assert [u.reg_read(r)for r in(UC_ARM_REG_R7,UC_ARM_REG_R6,UC_ARM_REG_R5)]==[3,10,30]
    choices=[]
    for choice,expected in enumerate((3,10,30,None)):
        u.reg_write(UC_ARM_REG_R0,choice);u.reg_write(UC_ARM_REG_R8,0)
        stop=0x5D244 if expected is None else 0x5D24C;u.emu_start(BASE+0x5D210,BASE+stop,count=20)
        assert u.reg_read(UC_ARM_REG_PC)==BASE+stop and u.reg_read(UC_ARM_REG_R8)==(0 if expected is None else expected)
        choices.append(dict(source_selected_index=choice,night_count=expected,cancel_before_return=expected is None,original_branch_executed=True))
    townroot=get(0xCB178);fees=[]
    for n in range(114):
        town=townroot+4+n*108;u.reg_write(UC_ARM_REG_R7,town);u.reg_write(UC_ARM_REG_SP,STACK);u.emu_start(BASE+0x5E004,BASE+0x5E03C,count=100000)
        assert u.reg_read(UC_ARM_REG_PC)==BASE+0x5E03C;value=u.reg_read(UC_ARM_REG_R6)
        fees.append(dict(town_index=n,original_current_minimum_fee=value,not_all_towns_claimed_Palace_eligible=True))
    monthly=read('work/analysis/palace_context_v2250d/native_context.json')['all218_native_item_monthly_price_providers'];assert min(r['native_monthly_amount']for r in monthly)==2
    labels=[]
    for r in doc['auxiliary_labels'][:6]:
        p=r['current_reference']['pointer'];text=r['english'].encode('ascii');call(u,0xCED28,(p,));assert u.reg_read(UC_ARM_REG_R0)==len(text)
        dest=0x02470020;u.mem_write(dest-16,bytes([165])*128);call(u,0xCEC74,(dest,p,len(text)+1))
        assert bytes(u.mem_read(dest,len(text)+1))==text+bytes(1)and bytes(u.mem_read(dest-16,16))==bytes([165])*16 and bytes(u.mem_read(dest+len(text)+1,16))==bytes([165])*16
        labels.append(dict(id=r['id'],pointer=p,complete_NUL_copy_strlen_and_guards_and_ABI=True))
    table=doc['auxiliary_labels'][0]['current_reference']['field'];u.mem_write(STACK-16,bytes([165])*160);u.reg_write(UC_ARM_REG_SP,STACK);u.emu_start(BASE+0x5D4FC,BASE+0x5D518,count=1000)
    assert u.reg_read(UC_ARM_REG_PC)==BASE+0x5D518 and bytes(u.mem_read(STACK+12,96))==arm[table:table+96]
    save(ROOT/'original_domains_and_auxiliary_providers.json',dict(ARM9_sha256=sha(arm),source_snapshot=snapshot,source_three_night_choices_and_cancel=choices,one_night_separate1177_and1178=True,all114_original_contract_fee_providers=fees,minimum_current_catalog_contract_fee=min(r['original_current_minimum_fee']for r in fees),source_contract_fee_fragments_clean_exact=True,all218_original_item_monthly_providers_bound='work/analysis/palace_context_v2250d/native_context.json',minimum_source_monthly_payment=2,plural_monthly_gold_coins_valid_for_original_item_domain=True,plural_nights_valid_only3_10_30_choices=True,current_six_Palace_label_cases=labels,original_menu_initializer_all96bytes_exact=True,six_labels_geometry_and_actual_menu_historical_binding_pending=True,scalar_choice_inputs_not_earned_or_actual_gameplay=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(night_choices=[3,10,30],contract_fees=114,minimum_fee=min(r['original_current_minimum_fee']for r in fees),monthly_minimum=2,complete_label_copies=6))
