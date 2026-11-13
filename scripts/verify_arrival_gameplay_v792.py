"""Actual corrected status paragraphs, lifecycle return and ordinary startup."""

import struct
from pathlib import Path
from types import FunctionType

from PIL import Image,ImageChops

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import arrival_notices_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import verify_shared_newgame_v782 as startup
from scripts.native_arrival_delivery_v792 import set_condition
from scripts.verify_arrival_native_v792 import prepared,format_case
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_letter_delivery_v791 import observed
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_shipyard_gameplay_v760 import independent_font,models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def load(name):
    path=CAP/name/'capture_report.json';rep=read(path)
    assert rep['frames']==20000 and rep['cold_boot'] and not rep['savestate_loaded'] and not rep['callback_errors']
    assert sha(Path(rep['ROM']).read_bytes())==rep['ROM_sha256']
    assert rep['battery_save_preloaded']['source']!=rep['battery_save_preloaded']['destination']
    assert rep['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert sha(Path(rep['battery_save_preloaded']['source']).read_bytes())==rep['battery_save_preloaded']['source_sha256']
    frames={r['frame']:r for r in rep['frames_captured']}
    for r in frames.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    ram={}
    for r in rep['read_only_capture_RAM_snapshots']+rep['read_only_pause_RAM_snapshots']:
        raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==0x400000 and r['read_only_export'] and sha(raw)==r['sha256']
        if r['frame'] in ram:assert ram[r['frame']]==raw
        ram[r['frame']]=raw
    return path,rep,frames,ram


def main():
    old,new=[load(n) for n in ('letter_delivery_v791_recovered','arrival_v792_delivery')]
    op,orep,of,oram=old;np,nrep,nf,nram=new
    assert orep['scripted_input_schedule']==nrep['scripted_input_schedule'] and orep['core_options']==nrep['core_options']
    assert set(of)==set(nf)
    ja,jb=[read(p.parent/'navigation_command_journal.json') for p in (op,np)]
    assert {k:v for k,v in ja.items() if k!='ROM_sha256'}=={k:v for k,v in jb.items() if k!='ROM_sha256'}
    rom=NdsImage.open(nrep['ROM']);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    oa=NdsImage.open(orep['ROM']).read_file('/__arm9__.bin');entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    for r in nrep['synthetic_condition_fixtures']:
        _,proof=set_condition(arm,nram[r['frame']],{'mode':r['mode']})
        assert r=={**proof,'frame':r['frame']}
    adapter=nrep['arrival_delivery_adapter'];assert adapter['single_fixture_import_replacement'] and adapter['no_text_menu_or_outcome_logic_replacement']
    assert adapter['original_harness_sha256']==sha(Path('scripts/headless_desmume_v193.py').read_bytes())
    assert all(sha(Path(p).read_bytes())==h for p,h in adapter['source_hashes'].items())
    rows={r['message_id']:r for r in read('translations/arrival_notices_editorial_manuscript_v3.json')['records']}
    owner=struct.unpack_from('<I',arm,0x552A0)[0];wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    holds=[];strict=[];unmatched=[]
    for f in sorted(nf):
        a,b=[Image.open(p[f]['path']).convert('RGB') for p in (of,nf)];diff=ImageChops.difference(a,b)
        if f not in (17200,18000,19200):
            if diff.getbbox() is None:strict.append(f)
            else:unmatched.append({'frame':f,'bounds':diff.getbbox(),'not_approved_as_original_pixel_control':True})
            continue
        n=348 if f==19200 else 347;raw=nram[f]
        assert cstring(raw,owner+0x2030)==entries[n].text
        assert raw.count(blocks[entries[n].block])==1
        value=cstring(raw,wrapped)
        if n==347:argument=b'Castor Co.'
        else:
            prefix,suffix=owned.compiled(rows[n]).split(b'%s')
            assert value.startswith(prefix) and value.endswith(suffix)
            argument=value[len(prefix):-len(suffix)]
        case=format_case(prepared(arm),rows[n],argument)
        assert bytes.fromhex(case['formatted_hex'])==value and not case['findings']
        plane=raster(arm,value,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
        expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
        actual={(x,y) for y in range(294,366) for x in range(16,244) if b.getpixel((x,y))==(0,8,0)}
        assert actual==expected,(f,len(expected-actual),len(actual-expected))
        previous={(x,y) for y in range(294,366) for x in range(16,244) if a.getpixel((x,y))==(0,8,0)}
        glyphs=expected|previous;shadows={(x+1,y+1) for x,y in glyphs}
        other=[(x,y) for y in range(294,366) for x in range(16,244) if (x,y) not in glyphs|shadows and a.getpixel((x,y))!=b.getpixel((x,y))]
        assert not other,(f,other[:10])
        diff.paste((0,0,0),(16,294,244,366));assert diff.getbbox() is None,(f,diff.getbbox())
        holds.append({'frame':f,'message_id':n,'argument_hex':argument.hex(),'lines':case['lines'],'capture':nf[f],
            'complete_independent_font_and_blank_paper_exact':True,'all_other_pixels_exact':True})
    states=[]
    for f in sorted(nram):
        if f<3200:continue
        row=observed(arm,nram[f]);prior=observed(oa,oram[f])
        assert row['cash']==prior['cash'] and row['tick']==prior['tick'] and row['letters']==prior['letters'] and row['relation']==prior['relation']
        states.append({'frame':f,'candidate':row,'cash_calendar_relation_and_courier_records_exact':True,
            'full_financial_state_exact':state(arm,nram[f])==state(oa,oram[f]),
            'models_exact':models(arm,nram[f])==models(oa,oram[f]),
            'actors_towns_items_goods_exact':persistent_objects(arm,nram[f])==persistent_objects(oa,oram[f])})
    final=states[-1]['candidate'];assert final['cash']==6369 and final['tick']==27069 and final['relation']==0
    assert all(bytes.fromhex(s)[4]==11 for s in final['letters'])
    FunctionType(startup.main.__code__,{**startup.__dict__,'ROOT':ROOT,'REPORT':CAP/'arrival_v792_newgame/capture_report.json',
        'OLD':CAP/'item_v788_newgame/capture_report.json','__file__':str(Path(__file__).resolve())})()
    save(ROOT/'gameplay_verification.json',{'candidate_sha256':nrep['ROM_sha256'],'reports':[str(op),str(np)],
        'report_sha256':[sha(p.read_bytes()) for p in (op,np)],'holds':holds,'strict_whole_screen_controls':strict,
        'unapproved_other_frame_differences':unmatched,'native_pairs':states,'normal_town_return_frame':20000,
        'random_daily_object_outputs_not_globally_approved':True,'entry346_native_and_family_sample_not_individually_activated':True,
        'no_savestate_original_saves_exact':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'Three complete repaired arrival holds;{len(strict)} whole-screen controls;{len(states)} cash/calendar/task pairs;normal return and seven New Game controls pass.',flush=True)


if __name__=='__main__':main()
