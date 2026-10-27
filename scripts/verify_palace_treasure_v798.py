"""Actual treasure loan/reclaim, complete glyphs and original method replays."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import palace_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts.native_palace_fixture_v798 import set_condition
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/palace_gameplay_v798')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/palace_v798_treasure')


def main():
    rep=read(CAP/'capture_report.json')
    assert rep['frames']==10200 and rep['cold_boot'] and not rep['savestate_loaded'] and not rep['callback_errors']
    rom=NdsImage.open(rep['ROM']);arm=rom.read_file('/__arm9__.bin')
    assert sha(Path(rep['ROM']).read_bytes())==rep['ROM_sha256']=='79696a0e6aa8b19f58cb26c3115cfcf01687f46b363bd6f469054e104f9af590'
    donor=rep['battery_save_preloaded'];assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    adapter=rep['Palace_fixture_adapter'];assert adapter['one_fixture_import_replacement'] and adapter['no_dialogue_menu_transaction_outcome_or_game_logic_replacement']
    assert all(sha(Path(p).read_bytes())==h for p,h in adapter['source_hashes'].items())
    frames={r['frame']:r for r in rep['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in rep['read_only_capture_RAM_snapshots']+rep['read_only_pause_RAM_snapshots']:
        raw=Path(r['path']).read_bytes();assert r['read_only_export'] and len(raw)==0x400000 and sha(raw)==r['sha256']
        if r['frame'] in ram:assert ram[r['frame']]==raw
        ram[r['frame']]=raw
    fixtures=rep['synthetic_condition_fixtures'];assert len(fixtures)==1 and fixtures[0]['frame']==3200
    fixture_raw,proof=set_condition(arm,ram[3200],{'mode':'Istanbul-treasure-headquarters'})
    assert fixtures[0]=={**proof,'frame':3200} and len(proof['changes'])==2
    assert persistent_objects(arm,fixture_raw)==persistent_objects(arm,ram[3600])
    rows={r['message_id']:r for r in read('translations/palace_editorial_manuscript_v3.json')['records']}
    entries=owned.current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    source=(owned.ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(owned.ROOT/'effective_format_case.py'),'exec'),env)
    owner,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x54450)]
    holds=[]
    for f,n in ((5200,1164),(6000,1166),(6400,1167),(8200,1169),(9000,1171)):
        raw=ram[f];assert cstring(raw,owner+0x2030)==entries[n].text
        values=('２５０'.encode('cp932'),) if n==1166 else ()
        case=env['format_case'](prepared(arm),rows[n],values)
        assert case['formatted_hex']==cstring(raw,wrapped).hex() and not case['findings']
        plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        image=Image.open(frames[f]['path']).convert('RGB')
        expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if image.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(f,len(expected-actual),len(actual-expected))
        holds.append({'frame':f,'id':n,'lines':case['lines'],'capture':frames[f],
            'complete_independent_font_and_blank_paper_ink_exact':True})
    replays=[]
    for before,after,position in ((6400,6800,1),(9000,9400,0)):
        cpu=machine(arm);cpu.mem_write(BASE,ram[before])
        def get(fn,args=()):call(cpu,fn,args);return cpu.reg_read(UC_ARM_REG_R0)
        item=get(0xCB190)+4+13*20;scratch=0x02470000
        assert get(0x4A410,(item,))==12500
        get(0x4A610,(scratch,position));get(0x49F30,(item,scratch,6,0))
        result=bytes(cpu.mem_read(BASE,0x400000))
        for fn in (persistent_objects,models,state,tasks):assert fn(arm,result)==fn(arm,ram[after]),(before,fn.__name__)
        cpu.mem_write(BASE,ram[after])
        assert get(0x4A224,(item,))==(0 if position else 4)
        assert get(0x4A1F8,(item,))==(16 if position else 0)
        replays.append({'before_frame':before,'after_frame':after,'original_constructor':BASE+0x4A610,
            'original_transfer':BASE+0x49F30,'position':position,'item_id':13,'name':'Alchemy Book',
            'whole_actors_items_towns_goods_models_finances_tasks_match_original_replay':True})
    assert all(state(arm,raw)['cash']==8371 for f,raw in ram.items() if f>=3200)
    assert persistent_objects(arm,fixture_raw)==persistent_objects(arm,ram[10200])
    for fn in (models,state,tasks):assert fn(arm,fixture_raw)==fn(arm,ram[10200])
    save(ROOT/'treasure_gameplay_verification.json',{'candidate_sha256':rep['ROM_sha256'],
        'capture_report':str(CAP/'capture_report.json'),'report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'fixture':fixtures[0],'five_repaired_holds':holds,'native_transfer_replays':replays,
        'quoted_monthly_payment250_for_price12500_exact':True,'no_calendar_month_elapsed_or_actual_monthly_payment_claim':True,
        'item_reclaimed_all_persistent_objects_match_post_fixture_start':True,'cash_remains8371':True,
        'normal_town_return_frame':10200,'source_donor_unchanged':True,
        'other_Palace_letters_defense_success_refusal_and_menu_boundary_repair_pending':True,
        'no_Palace_family_completion_credit':True,'full_goal_complete':False,
        'producer_sha256':sha(Path('scripts/verify_palace_treasure_v798.py').read_bytes())})
    print('Five actual Palace treasure holds and original loan/reclaim world-state replays pass;item returned,8371 coins,donor unchanged.',flush=True)


if __name__=='__main__':main()
