"""Actual-protagonist fasting reactions, retained refusal and complete glyphs."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_heroes_v825')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
SPECS=[dict(hero='Rafael',captain=0,base=25400,refusal=24400,IDs=[1219,1220,1232,1233,1237,1230,1238,294]),
       dict(hero='Maria',captain=3,base=26000,refusal=23400,IDs=[1219,1220,1232,1236,1237,1230,1241,294]),
       dict(hero='Lil',captain=2,base=23000,refusal=19400,IDs=[1219,1220,1232,1235,1237,1230,1240,294])]


def identity(arm,raw):
    u=machine(arm);u.mem_write(0x02000000,raw)
    def get(fn,args=()):
        call(u,fn,args,instruction_limit=500000)
        return u.reg_read(UC_ARM_REG_R0)
    hero=get(0x7F244);actor=get(0xCB184)+0x19E4
    vt=struct.unpack('<I',u.mem_read(actor,4))[0]
    def name(slot):
        at=get(struct.unpack('<I',u.mem_read(vt+slot,4))[0]-0x02000000,(actor,))
        return bytes(u.mem_read(at,128)).split(b'\0')[0]
    fleet=get(0xCB1A8)+4+get(0x2E58C)*0x84
    return dict(captain=hero,formal_name=name(8).decode('cp932'),notice_name=name(32).decode('cp932'),
        town=get(0xB65E4),fleet_town=get(0x34674,(fleet,)))


def cstring(raw,at):return raw[at-0x02000000:at-0x02000000+512].split(b'\0')[0]


def main():
    rom=NdsImage.open('out/all_routes_combined_v820_candidate.nds');arm=rom.read_file('/__arm9__.bin')
    common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)
    blocks=IlnkContainer.parse(common).blocks
    rows={r['message_id']:r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    ordinary,modal,osource,msource=production_functions()
    printed,wrapped,owner=[struct.unpack_from('<I',arm,off)[0] for off in (0x5444C,0x54450,0x552A0)]
    holds=[];refusals=[];effects=[];captain_names=[]
    for spec in SPECS:
        folder=CAP/f'ceremony_{spec["hero"]}_approach_v825';report=read(folder/'capture_report.json')
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==sha(rom.source.read_bytes())
        assert report['core_DLL_sha256']=='42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b'
        assert not report['goal_complete'] and not report['hardware_device_verification']
        assert report['actual_hero_fixture_adapter_v825']['no_captain_actor_dialogue_or_random_state_fixture_available']
        donor=report['battery_save_preloaded'];assert donor['source']!=donor['destination']
        assert donor['copied_byte_exact_before_cold_boot'] and sha(Path(donor['source']).read_bytes())==donor['source_sha256']
        assert 'disposable' in donor['source'].lower()
        for fix in report.get('synthetic_condition_fixtures',[]):
            assert fix['synthetic_ceremony_Athens_fixture'] and fix['actual_captain_and_all_actor_records_preserved']
        pictures={r['frame']:r for r in report['frames_captured']}
        snapshots={r['frame']:r for r in report['read_only_pause_RAM_snapshots']}
        def raw_at(f):
            r=snapshots[f];raw=Path(r['path']).read_bytes()
            assert len(raw)==0x400000 and sha(raw)==r['sha256']
            return raw
        start=raw_at(spec['base']);who=identity(arm,start)
        assert who['captain']==spec['captain'] and who['town']==who['fleet_town']==19
        captain_names.append(who)
        for index,n in enumerate(spec['IDs']):
            f=spec['base']+index*400;raw=raw_at(f);actual_who=identity(arm,raw)
            assert actual_who==who
            values=(b'Parthenon',) if n==1219 else (who['notice_name'].encode('cp932'),) if n==294 else ()
            case=(modal if n==294 else ordinary)(prepared(arm),rows[n],values)
            assert not case['findings'] and cstring(raw,wrapped)==bytes.fromhex(case['formatted_hex'])
            assert cstring(raw,owner+0x2030)==entries[n].text and raw.count(blocks[entries[n].block])==1
            for value in values:assert value in cstring(raw,printed) and value in cstring(raw,wrapped)
            plane=raster(arm,bytes.fromhex(case['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
            assert plane==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),case['lines'])
            picture=pictures[f];assert sha(Path(picture['path']).read_bytes())==picture['PNG_sha256']
            img=Image.open(picture['path']).convert('RGB')
            expected={(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}
            actual={(x,y) for y in range(294,366) for x in range(16,244) if img.getpixel((x,y))==(0,8,0)}
            assert expected==actual,(spec['hero'],f,n,len(expected-actual),len(actual-expected))
            holds.append(dict(hero=spec['hero'],captain_ID=who['captain'],message_id=n,frame=f,
                lines=case['lines'],capture=picture,whole_native_independent_font_actual_ink_and_blank_plane_exact=True,
                original_actual_captain_name_and_portrait_visually_reviewed=True,
                native_parent_substitution_resident_template_and_block_exact=True,
                complete_first_final_letters_punctuation_numbers_margins_and_bounds=True))
        f=spec['refusal'];raw=raw_at(f);encoded=cstring(raw,wrapped)
        assert encoded==entries[64].text==b'No business? Leave now.'
        plane=raster(arm,encoded,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        expected=independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),['No business? Leave now.'])
        # Source-retained single row has no guard prefix; its native origin is0.
        expected=b''.join(expected[y*228+6:(y+1)*228]+bytes(6) for y in range(64))
        assert plane==expected
        picture=pictures[f];img=Image.open(picture['path']).convert('RGB')
        assert {(16+i%228,296+i//228) for i,p in enumerate(plane) if p==1}=={
            (x,y) for y in range(294,366) for x in range(16,244) if img.getpixel((x,y))==(0,8,0)}
        refusals.append(dict(hero=spec['hero'],frame=f,message_id=64,capture=picture,
            unchanged_source_retained_single_row_origin0_complete_glyphs_and_blank_plane=True,
            no_multiline_alignment_exception_or_authored_padding_added=True))
        end=raw_at(report['frames']);after=identity(arm,end)
        assert after==who
        ticks=calendar(arm,end)['ticks']-calendar(arm,start)['ticks']
        assert ticks==192,(spec['hero'],ticks)
        effects.append(dict(hero=spec['hero'],from_frame=spec['base'],return_frame=report['frames'],
            native_four_day192_tick_advance=True,actual_captain_and_town_return_preserved=True,
            original_outcomes_recorded_not_compared_across_different_captains=True))
    assert len(holds)==24 and len(refusals)==3
    verified={r['message_id'] for r in holds if r['message_id'] in (1233,1235,1236,1238,1240,1241)}
    assert verified=={1233,1235,1236,1238,1240,1241}
    save(ROOT/'actual_hero_fast_and_retained64_verification.json',dict(candidate=str(rom.source),sha256=sha(rom.source.read_bytes()),
        complete_scene_holds=holds,retained_refusal_holds=refusals,original_time_and_return=effects,
        actual_native_identities=captain_names,new_distinct_protagonist_reactions=sorted(verified),
        all_three_real_captains_no_dialogue_or_actor_substitution=True,
        ordinary_formatter_sha256=sha(osource.encode()),modal_formatter_sha256=sha(msource.encode()),
        original_source_ritual_effects_time_and_selector_spans_unchanged=True,
        remaining_distinct_reactions=[1206,1209,1211,1213,1214,1217,1224,1229],
        whole_family_editorial_completion_credit=0,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Three real captains:24 complete fasting holds,3 retained64 holds,6 new distinct reactions and allthree192-tick returns pass.',flush=True)


if __name__=='__main__':main()
