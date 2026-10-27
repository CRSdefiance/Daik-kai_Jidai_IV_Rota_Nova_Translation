"""Bind ordinary town requests and the original monthly tribute payment direction."""
from pathlib import Path
import struct
from PIL import Image
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R4,UC_ARM_REG_R7,UC_ARM_REG_R10,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/town_services_roles_v2056b')
RUN=Path('work/analysis/town_services_actual_v2053')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_actual_v2053_V2047')
OBS=CAP/'common_observer/requests.json'
if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,obs=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',OBS))
    assert terminal['terminal']and terminal['all_observer_host_slots_restored']and terminal['frames']==report['frames']==38500
    assert report['ROM_sha256']==plan['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert report['scripted_input_schedule']==read(plan['inputs'])and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    assert len(report['synthetic_gallery_fixtures'])==1 and not report['synthetic_gallery_fixtures'][0]['earned_unlock_verified']
    assert all(k=='synthetic_gallery_fixtures'or not v for k,v in report.items()if k.startswith('synthetic_'))
    assert report['synthetic_gallery_fixtures'][0]['manifest_sha256']==plan['fixture_manifest_sha256']==sha(Path(plan['fixture_manifest']).read_bytes())
    assert sha(Path(plan['existing_isolated_system_unlock']).read_bytes())==plan['donor_sha256']==report['battery_save_preloaded']['source_sha256']
    assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
    assert [r['message_ID']for r in obs['rows']]==[49,8,51,53,55,56,59,61]
    for r in obs['rows']:
        assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        for snap in r['complete_readonly_snapshots'].values():assert sha(Path(snap['path']).read_bytes())==snap['sha256']and len(Path(snap['path']).read_bytes())==snap['bytes']
    # New source text is earlier in SC3 only. The entire following town frames
    # must still match the earlier ordinary run rather than relying on intent.
    prior=read(plan['prior_report']);assert sha(Path(plan['prior_report']).read_bytes())==plan['prior_report_sha256']
    photos={r['frame']:r for r in report['frames_captured']};old={r['frame']:r for r in prior['frames_captured']};pairs=[]
    for frame,p in photos.items():
        assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        if frame<31000:continue
        assert Image.open(p['path']).convert('RGB').tobytes()==Image.open(old[frame]['path']).convert('RGB').tobytes()
        pairs.append(dict(frame=frame,whole256x384_RGB_exact_to_prior_context=True,capture=p['path'],capture_sha256=p['PNG_sha256']))
    row49=next(r for r in obs['rows']if r['message_ID']==49);row55=next(r for r in obs['rows']if r['message_ID']==55)
    raw=Path(row49['complete_readonly_snapshots']['WRAM']['path']).read_bytes();name_raw=Path(row55['complete_readonly_snapshots']['WRAM']['path']).read_bytes()
    assert cstring(raw,row49['registers'][2])=='６００'.encode('cp932')
    assert cstring(name_raw,row55['registers'][2])==b'Mihwa'
    assert all(r['caller_LR']==(0x02053FB0 if r['message_ID']in(49,59)else 0x02053FF8)for r in obs['rows'])
    image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=[(0x2DC68,0x2DC84),(0x2DE14,0x2DEA4),(0x3CC80,0x3CCD0),(0x59E44,0x59F24),(0x1189C0,0x1189E0)]
    assert all(arm[a:b]==clean[a:b]for a,b in spans)
    table=list(struct.unpack_from('<8I',arm,0x1189C0));assert table==[76,77,78,79,80,81,0xffffffff,82]
    cpu,get=get_machine(arm,raw);own_ID=get(0x397D8);force_table=get(0xCB160);own=force_table+4+76*own_ID
    assert get(0x7F244)==own_ID==3 and get(0x3CCC8,own)==40000
    assert bytes(cpu.mem_read(0x02000000,4194304))==raw
    other=force_table+4+76*((own_ID+1)%20);branch=[]
    for amount in(1,600,12345):
        cpu,get=get_machine(arm,raw)
        # Controlled cloned native RAM only. No emulator,ROM or save is changed.
        cpu.mem_write(own+12,struct.pack('<I',40000));cpu.mem_write(other+12,struct.pack('<I',100000))
        cpu.reg_write(UC_ARM_REG_R4,amount);cpu.reg_write(UC_ARM_REG_R7,own);cpu.reg_write(UC_ARM_REG_R10,other)
        before=bytes(cpu.mem_read(0x02000000,4194304));sp=cpu.reg_read(UC_ARM_REG_SP)
        cpu.emu_start(0x0202DE54,0x0202DE6C,count=10000)
        after=bytes(cpu.mem_read(0x02000000,4194304));expected=bytearray(before)
        struct.pack_into('<I',expected,own+12-0x02000000,40000+amount);struct.pack_into('<I',expected,other+12-0x02000000,100000-amount)
        assert after==bytes(expected)and cpu.reg_read(UC_ARM_REG_SP)==sp
        assert cpu.reg_read(UC_ARM_REG_R4)==amount and cpu.reg_read(UC_ARM_REG_R7)==own and cpu.reg_read(UC_ARM_REG_R10)==other
        branch.append(dict(amount=amount,donor_before=100000,donor_after=100000-amount,player_before=40000,player_after=40000+amount,
            original_branch_and_both_original_gold_mutators_executed=True,only_two_owned_balance_words_changed=True,
            isolated_native_branch_test_not_actual_monthly_tribute_gameplay=True))
    quantities=[]
    for amount in(1,600,999999999):
        q,get=get_machine(arm,raw);at=get(0xABF50,amount);value=cstring(bytes(q.mem_read(0x02000000,4194304)),at)
        quantities.append(dict(amount=amount,native_formatted_hex=value.hex(),native_formatted_text=value.decode('cp932'),
            cloned_native_formatter_may_write_its_owned_ring_not_a_purity_claim=True))
    ROOT.mkdir(parents=True);cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    code=[dict(start=0x02000000+a,end=0x02000000+b,hex=arm[a:b].hex(),sha256=sha(arm[a:b]),
        disassembly=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str)for i in cs.disasm(arm[a:b],0x02000000+a)])for a,b in spans]
    save(ROOT/'active_eight_requests_and_tribute_payment_direction.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],ARM9_sha256=sha(arm),
        source_contract=str(RUN/'source_contract.json'),source_contract_sha256=sha((RUN/'source_contract.json').read_bytes()),
        report=str(CAP/'capture_report.json'),report_sha256=sha((CAP/'capture_report.json').read_bytes()),observer=str(OBS),observer_sha256=sha(OBS.read_bytes()),
        observed_native_IDs=[r['message_ID']for r in obs['rows']],full_town_RGB_pairs=pairs,
        resupply_first_argument_role='native gold-quantity string',resupply_actual_amount_hex='６００'.encode('cp932').hex(),
        barkeep_call_first_argument_role='named serving attendant',barkeep_actual_name='Mihwa',barkeep_actual_name_hex=b'Mihwa'.hex(),
        IDs54_and55_share_original_barkeep_call_and_attendant_name_getter=True,
        IDs49_and59_original_yes_no_parent_while_other_six_are_direct_display=True,
        tribute_message_table=table,player_force_ID=own_ID,player_force_address=own,selected_player_balance=40000,
        tribute_branch_cases=branch,native_quantity_examples=quantities,
        tribute76_to82_is_incoming_to_current_player_not_a_payment_demand=True,
        caller_spans_exact_clean_source=code,original_system_unlock_only_not_earned=True,
        later_native_glyph_word_wrap_cache_repacking_revised_gameplay_and_release_pending=True,
        no_ROM_registry_or_save_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_IDs=8,full_town_RGB_pairs=len(pairs),Mihwa_native_argument=True,incoming_tribute_cases=3,all_other_native_memory_exact=True))
