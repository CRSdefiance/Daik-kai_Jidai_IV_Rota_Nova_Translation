"""Actual contract glyphs, no extra page, original cancellation and startup."""

import struct
from pathlib import Path
from types import FunctionType

from PIL import Image,ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import palace_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_continuation_layout_v768 as original
from scripts import verify_shared_newgame_v782 as startup
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


def load(folder,terminal):
    path=CAP/folder/'capture_report.json';rep=read(path)
    assert rep['frames']==terminal and rep['cold_boot'] and not rep['savestate_loaded'] and not rep['callback_errors']
    assert sha(Path(rep['ROM']).read_bytes())==rep['ROM_sha256']
    assert not any(v for k,v in rep.items() if k.startswith('synthetic_'))
    donor=rep['battery_save_preloaded']
    assert donor['source']!=donor['destination'] and donor['copied_byte_exact_before_cold_boot']
    assert sha(Path(donor['source']).read_bytes())==donor['source_sha256']=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    frames={r['frame']:r for r in rep['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in rep['read_only_capture_RAM_snapshots']+rep['read_only_pause_RAM_snapshots']:
        raw=Path(r['path']).read_bytes();assert len(raw)==0x400000 and sha(raw)==r['sha256'] and r['read_only_export']
        if r['frame'] in ram:assert ram[r['frame']]==raw
        ram[r['frame']]=raw
    return path,rep,frames,ram


def main():
    op,orep,of,oram=load('palace_v794_context',7200)
    np,nrep,nf,nram=load('palace_v797_contract',6800)
    assert orep['core_options']==nrep['core_options']
    # The repaired quote removes exactly one old blank-page advance. Match
    # the otherwise identical events explicitly, shifting later events400
    # frames; do not claim an identical full schedule across that repair.
    old_schedule=orep['scripted_input_schedule']
    assert next(r for r in old_schedule if r['start']==5201)=={'start':5201,'duration':8,'buttons':['A']}
    adjusted=[{**r,'start':r['start']-(400 if r['start']>5201 else 0)}
              for r in old_schedule if r['start']!=5201]
    assert adjusted==nrep['scripted_input_schedule']
    rom=NdsImage.open(nrep['ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    rows={r['message_id']:r for r in read('translations/palace_editorial_manuscript_v3.json')['records']}
    source=(ROOT/'effective_format_case.py').read_text(encoding='utf-8')
    env={**original.__dict__};exec(compile(source,str(ROOT/'effective_format_case.py'),'exec'),env)
    owner,printed,wrapped=[struct.unpack_from('<I',arm,n)[0] for n in (0x552A0,0x5444C,0x54450)]
    holds=[];outside=[]
    for f,n,oldf in ((4800,1156,4800),(5200,1157,5600),(6000,1158,6400)):
        raw=nram[f];assert cstring(raw,owner+0x2030)==entries[n].text
        assert raw.count(blocks[entries[n].block])==1
        values=('２８４２'.encode('cp932'),) if n==1156 else ()
        case=env['format_case'](prepared(arm),rows[n],values)
        assert cstring(raw,wrapped).hex()==case['formatted_hex'] and not case['findings']
        if n==1156:
            assert values[0] in cstring(raw,printed) and values[0] in cstring(raw,wrapped)
        plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        b=Image.open(nf[f]['path']).convert('RGB');a=Image.open(of[oldf]['path']).convert('RGB')
        expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if b.getpixel((x,y))==(0,8,0)}
        assert expected==actual,(f,len(expected-actual),len(actual-expected))
        diff=ImageChops.difference(a,b);diff.paste((0,0,0),(16,294,244,366))
        outside.append({'frame':f,'old_corresponding_frame':oldf,'difference_bounds':diff.getbbox(),
            'whole_outside_dialogue_plane_exact':diff.getbbox() is None})
        holds.append({'frame':f,'message_id':n,'capture':nf[f],'lines':case['lines'],
            'complete_independent_font_exact_including_all_four_fee_digits':True,
            'native_resident_complete_block_exact':True,'no_unexpected_dark_ink_on_blank_paper':True})
    # A once dismisses the quote and reaches the next distinct paragraph. The
    # previous run required an additional A for an empty page with owner1156.
    assert cstring(nram[4800],owner+0x2030)==entries[1156].text
    assert cstring(nram[5200],owner+0x2030)==entries[1157].text
    old_journal=read(op.parent/'navigation_command_journal.json')['commands_received']
    journal=read(np.parent/'navigation_command_journal.json')['commands_received']
    assert [r['command'] for r in journal[:5]]==[r['command'] for r in old_journal[:5]]
    assert len(journal)==10 and journal[-1]['frame']==6800 and journal[-1]['command']=={'stop':True}
    assert journal[4]['frame']==4800 and journal[4]['command']['buttons']==['A']
    cash=[]
    for f,raw in sorted(nram.items()):
        if f>=3200:
            assert state(arm,raw)['cash']==8371
            cash.append({'frame':f,'cash':8371})
    for fn in (state,models,persistent_objects,tasks):assert fn(arm,nram[3200])==fn(arm,nram[6800]),fn.__name__
    controls=[]
    for newf,oldf in ((3200,3200),(3600,3600),(4000,4000),(4400,4400),(5600,6000),(6400,6800),(6800,7200)):
        a,b=[Image.open(r[f]['path']).convert('RGB') for r,f in ((of,oldf),(nf,newf))]
        diff=ImageChops.difference(a,b)
        controls.append({'new_frame':newf,'old_frame':oldf,'whole_screen_exact':diff.getbbox() is None,'difference_bounds':diff.getbbox()})
    assert all(r['whole_outside_dialogue_plane_exact'] for r in outside)
    assert all(r['whole_screen_exact'] for r in controls)
    FunctionType(startup.main.__code__,{**startup.__dict__,'ROOT':ROOT,
        'REPORT':CAP/'palace_v797_newgame/capture_report.json','OLD':CAP/'arrival_v792_newgame/capture_report.json',
        '__file__':str(Path('scripts/verify_palace_gameplay_v797.py').resolve())})()
    save(ROOT/'contract_gameplay_verification.json',{'candidate_sha256':nrep['ROM_sha256'],
        'report_paths':[str(op),str(np)],'report_hashes':[sha(op.read_bytes()),sha(np.read_bytes())],
        'actual_repaired_holds':holds,'outside_body_comparisons':outside,'control_frames':controls,
        'quote_extra_blank_page_removed_one_A_reaches1157':True,'cash_observations':cash,
        'paired_schedule_only_old_blank_page_A_at5201_removed_later_events_shift400_frames':True,
        'cash_models_actors_towns_items_goods_couriers_exact_initial_to_return':True,
        'normal_town_return_frame':6800,'protected_donor_save_unchanged':True,
        'other_Palace_letters_defense_loan_and_success_outcomes_still_pending':True,
        'family_editorial_completion_credit':0,'full_goal_complete':False,
        'producer_sha256':sha(Path('scripts/verify_palace_gameplay_v797.py').read_bytes())})
    print('Actual1156/1157/1158 full glyphs,2842 digits,no blank page,cancellation8371 coins and normal return pass;seven startup controls pass.',flush=True)


if __name__=='__main__':main()
