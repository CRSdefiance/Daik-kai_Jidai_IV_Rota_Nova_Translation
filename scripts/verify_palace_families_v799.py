"""Actual Palace families:letters,defense,paid contract and low-funds refusal."""

import struct
from pathlib import Path
from types import FunctionType

from PIL import Image
from unicorn.arm_const import (UC_ARM_REG_R0,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,
    UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_SP,UC_ARM_REG_PC)

from dk4tool.patch import palace_editorial as prose
from dk4tool.patch import palace_label_boundaries as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts import verify_shared_newgame_v782 as startup
from scripts.native_palace_fixture_v799 import set_condition
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(name,terminal,fixture_count):
    path=CAP/name/'capture_report.json';rep=read(path)
    assert rep['frames']==terminal and rep['cold_boot'] and not rep['savestate_loaded'] and not rep['callback_errors']
    assert sha(Path(rep['ROM']).read_bytes())==rep['ROM_sha256']=='f855781b6b2a23482874a81c4d3f8f77262fe7f7db2846399b1409da8cc67c79'
    donor=rep['battery_save_preloaded'];assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    frames={r['frame']:r for r in rep['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in rep.get('read_only_capture_RAM_snapshots',[])+rep.get('read_only_pause_RAM_snapshots',[]):
        raw=Path(r['path']).read_bytes();assert r['read_only_export'] and len(raw)==0x400000 and sha(raw)==r['sha256']
        if r['frame'] in ram:assert ram[r['frame']]==raw
        ram[r['frame']]=raw
    fixtures=rep.get('synthetic_condition_fixtures',[]);assert len(fixtures)==fixture_count
    assert not any(v for k,v in rep.items() if k.startswith('synthetic_') and k!='synthetic_condition_fixtures')
    if fixtures:
        adapter=rep['Palace_fixture_adapter_v799'];assert adapter['one_fixture_import_replacement'] and adapter['no_dialogue_menu_transaction_outcome_or_game_logic_replacement']
        assert all(sha(Path(p).read_bytes())==h for p,h in adapter['source_hashes'].items())
        for row in fixtures:
            _,proof=set_condition(ARM,ram[row['frame']],{'mode':row['mode']})
            assert row=={**proof,'frame':row['frame']}
        journal=read(path.parent/'navigation_command_journal.json')['commands_received']
        assert all(r['validation_passed'] for r in journal) and journal[-1]['command']=={'stop':True}
    return path,rep,frames,ram


def observation(raw):
    cpu=machine(ARM);cpu.mem_write(BASE,raw)
    def get(n,args=()):call(cpu,n,args);return cpu.reg_read(UC_ARM_REG_R0)
    town=get(0xB6618);clock=get(0xCB1B4);admiral=get(0xCB184)+0x19E4
    return {**state(ARM,raw),'letter_mode':get(0x82F60,(admiral,)),
        'tick':struct.unpack('<I',cpu.mem_read(clock+8,4))[0],
        'intro_additional_restriction':get(0xB521C,(town,))}


def replay_town(before,after,start,stop,registers):
    cpu=machine(ARM);cpu.mem_write(BASE,before)
    call(cpu,0xB6618,());town=cpu.reg_read(UC_ARM_REG_R0)
    cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_R7,town)
    for reg,value in registers:cpu.reg_write(reg,value)
    cpu.emu_start(BASE+start,BASE+stop,count=300000)
    assert cpu.reg_read(UC_ARM_REG_PC)==BASE+stop
    actual=after[town-BASE:town-BASE+108]
    assert bytes(cpu.mem_read(town,108))==actual
    return {'original_transaction_span':[BASE+start,BASE+stop],'whole108_byte_town_record_matches_original_replay':True,
        'clock_not_replayed_and_unrelated_daily_random_objects_not_globally_approved':True}


def main():
    global ARM
    rom=NdsImage.open('out/all_routes_combined_v799_candidate.nds');ARM=rom.read_file('/__arm9__.bin')
    expanded=load('palace_v799_expanded_menu',15200,2)
    positive=load('palace_v799_contract_success',6800,0)
    negative=load('palace_v799_insufficient',5600,1)
    entries=owned.current_entries(rom.read_file('/COMMON/MESFILE.DK4'),ARM)
    rows={r['message_id']:r for r in read('translations/palace_editorial_manuscript_v3.json')['records']}
    owner,wrapped=[struct.unpack_from('<I',ARM,n)[0] for n in (0x552A0,0x54450)]
    source=(prose.ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(prose.ROOT/'effective_format_case.py'),'exec'),env)
    holds=[]
    expected=[(expanded,[(5400,1164),(6200,1166),(6600,1167),(8200,1153),(8600,1176),(9800,1169),(10600,1171),(12200,1154),(13000,1160),(14000,1155),(14400,1174)]),
        (positive,[(4800,1156),(5200,1157),(6000,1159)]),(negative,[(4800,1149),(5200,1162)])]
    for package,expected_ids in expected:
        path,rep,frames,ram=package
        for frame,n in expected_ids:
            raw=ram[frame];assert cstring(raw,owner+0x2030)==entries[n].text
            if n in (1149,1156):value='２８４２'.encode('cp932')
            elif n==1166:value='２５０'.encode('cp932')
            elif n==1154:value=bytes.fromhex(read('work/analysis/palace_editorial_v795/native_context.json')['native_player_address_hex'])
            else:value=b''
            values=(value,) if rows[n]['source_native_arguments'] else ()
            result=env['format_case'](prepared(ARM),rows[n],values)
            assert result['formatted_hex']==cstring(raw,wrapped).hex() and not result['findings']
            pixels=raster(ARM,bytes.fromhex(result['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
            assert pixels==independent_font(ARM,rom.read_file('/GRP/KANJI.FNT'),result['lines'])
            image=Image.open(frames[frame]['path']).convert('RGB')
            glyphs={(16+i%228,296+i//228) for i,p in enumerate(pixels) if p==1}
            actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
            assert glyphs==actual,(path,frame,n,len(glyphs-actual),len(actual-glyphs))
            holds.append({'report':str(path),'frame':frame,'id':n,'lines':result['lines'],
                'capture':frames[frame],'all_complete_glyphs_substitutions_and_blank_paper_exact':True})
    er=expanded[3];pr=positive[3];nr=negative[3]
    before,after=observation(er[7400]),observation(er[9000])
    assert (before['share'],before['letter_mode'],before['cash'])==(0,1,8371)
    assert (after['share'],after['letter_mode'],after['cash'])==(1,2,8371)
    assert after['tick']==before['tick']+48
    defense=[observation(er[f]) for f in (13000,13400)]
    assert defense[0]['cash']==8371 and defense[1]['cash']==5371
    assert defense[1]['tick']==defense[0]['tick']+48 and defense[1]['share']==defense[0]['share']==1
    defense_replay=replay_town(er[13000],er[13400],0x5DE1C,0x5DE94,((UC_ARM_REG_R4,3000),(UC_ARM_REG_R5,1),(UC_ARM_REG_R8,3000)))
    intro=[observation(er[f]) for f in (14000,14400,14800,15200)]
    assert all(p==intro[0] for p in intro) and intro[0]['letter_mode']==0 and intro[0]['intro_additional_restriction']==1
    paid=[observation(pr[f]) for f in (6000,6400,6800)]
    assert paid[0]['cash']==8371 and paid[1]['cash']==paid[2]['cash']==5529
    assert paid[0]['share']==0 and paid[1]['share']==paid[2]['share']==1
    assert paid[1]['tick']==paid[0]['tick']+48
    paid_replay=replay_town(pr[6000],pr[6400],0x5E120,0x5E1B0,((UC_ARM_REG_R4,2842),(UC_ARM_REG_R6,2842)))
    low=[observation(nr[f]) for f in (3600,4800,5200,5600)]
    assert all(p==low[0] for p in low) and low[0]['cash']==1 and low[0]['share']==0
    for fn in (models,state,persistent_objects,tasks):assert fn(ARM,nr[3600])==fn(ARM,nr[5600])
    guard=read(ROOT/'guard_speaker_context_erratum.json');assert guard['clean_Japanese']=='衛兵' and guard['English']=='Guard'
    FunctionType(startup.main.__code__,{**startup.__dict__,'ROOT':ROOT,
        'REPORT':CAP/'palace_v799_newgame/capture_report.json','OLD':CAP/'palace_v797_newgame/capture_report.json',
        '__file__':str(Path('scripts/verify_palace_families_v799.py').resolve())})()
    geometry=read(ROOT/'actual_menu_geometry_verification.json');assert geometry['total_actual_rows']==12 and geometry['all_six_labels_complete_in_actual_menus']
    save(ROOT/'actual_family_verification.json',{'candidate_sha256':sha(Path('out/all_routes_combined_v799_candidate.nds').read_bytes()),
        'reports':[{'path':str(p[0]),'sha256':sha(p[0].read_bytes()),'terminal_frames':p[1]['frames']} for p in (expanded,positive,negative)],
        'sixteen_actual_holds':holds,'recommendation_before_after':[before,after],
        'defense_before_after':defense,'defense_original_replay':defense_replay,
        'introduction_refusal_observations':intro,'paid_contract_observations':paid,'paid_contract_original_replay':paid_replay,
        'low_funds_quote1149_then_warning1162_and_normal_Palace_menu_dismissal':low,
        'all_six_menu_labels_native_geometry_and_full_fonts_verified':True,'seven_startup_whole_frames_exact':True,
        'all_original_donor_saves_unchanged':True,
        'not_every_Palace_branch_price_culture_or_voice_individually_activated':True,
        'no_monthly_payment_full_route_hardware_or_graphics_completion_claim':True,
        'producer_sha256':sha(Path('scripts/verify_palace_families_v799.py').read_bytes()),'full_goal_complete':False})
    print('Sixteen actual Palace holds,paid/refused contract,letter outcomes,defense payment,original Town replays,all6 menu labels and7 startup controls pass.',flush=True)


if __name__=='__main__':main()
