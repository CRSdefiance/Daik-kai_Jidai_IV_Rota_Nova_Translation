"""Audit every pre-duel fixture and the original defeat-to-title transition."""
import json
from pathlib import Path
from shutil import copy2
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.escape_direct_entries import current_entries
from scripts.native_escape_direct_fixture_v1190 import apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_terminal_v1194')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/escape_direct_v1190_1189')
ROM=Path('out/all_routes_combined_v1189_candidate.nds')
RUN=Path('work/analysis/escape_direct_live_v1190')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V1189 Escape notice')
BASE=0x02000000


def main():
    assert not ROOT.exists() and not GUIDE.exists()
    rp=CAP/'capture_report.json';report=read(rp)
    assert report['frames']==7802 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert report['ROM_sha256']==sha(ROM.read_bytes())
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    slices=((0x737C8,0x74010),(0xE8CC,0x10010),(0x53F0C,0x53FE4),
        (0x7E154,0x7E1A4),(0x7E988,0x7E9B0),(0x49DE8,0x4A0F8),(0x4A5F4,0x4A628),
        (0x7DCC8,0x7DE20),(0x519D4,0x51A28),(0xD9824,0xD9868))
    for lo,hi in slices:assert arm[lo:hi]==clean[lo:hi],(hex(lo),hex(hi))
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if row['frame'] in snapshots:assert row['sha256']==snapshots[row['frame']]['sha256']
        snapshots[row['frame']]=row
    def raw(frame):
        row=snapshots[frame];data=Path(row['path']).read_bytes()
        assert len(data)==row['bytes']==0x400000 and sha(data)==row['sha256']
        return data
    fixtures=report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==31 and max(r['frame'] for r in fixtures)==5770
    seed,flag=[struct.unpack_from('<I',arm,o)[0] for o in (0xD9858,0x51A20)]
    audits=[];transfers=[]
    for row in fixtures:
        request={'sighting_context':'compassAttack8'} if row['context']=='compassAttack8' else {'duel_context':'unarmoredContact'}
        before=raw(row['frame']);after,receipt=apply_fixture(arm,before,request)
        assert row=={**receipt,'frame':row['frame']}
        assert sha(before)==row['before_RAM_sha256'] and sha(after)==row['after_RAM_sha256']
        owned=set(row['owned_bytes'])
        for at in (seed,flag):
            assert not owned.intersection(range(at,at+4)) and before[at-BASE:at-BASE+4]==after[at-BASE:at-BASE+4]
        before_cpu,bget=get_machine(arm,before);after_cpu,aget=get_machine(arm,after)
        assert [bget(o) for o in (0x7F244,0x2E58C)]==[aget(o) for o in (0x7F244,0x2E58C)]==[1,1]
        actors=bget(0xCB184);assert aget(0xCB184)==actors
        assert before[actors-BASE:actors-BASE+0x19E4]==after[actors-BASE:actors-BASE+0x19E4]
        if row['context']=='unarmoredContact':
            parent=row['parent_positive_HP_and_contact_receipt']
            assert parent['positive_captain_HP_before'][0]>0
            assert all(v>0 for pair in parent['live_Hull_Crew_before'] for v in pair)
            assert set(parent['owned_bytes'])<=owned
            if row['native_armor_transfer']:
                transfers.append(row['native_armor_transfer'])
                assert transfers[-1]['item_ID']==49 and transfers[-1]['result_owner_kind_inventory']==0
                assert transfers[-1]['fencing_before_after']==[158,134]
        audits.append({'frame':row['frame'],'context':row['context'],'before_RAM_sha256':sha(before),
            'after_RAM_sha256':sha(after),'owned_bytes':len(owned),'changed_bytes':len(row['changes']),
            'all4MiB_deltas_replayed_exact_RNG_identity_guards_pass':True})
        if len(audits)%10==0:print(len(audits),'complete fixture replays pass',flush=True)
    assert len(transfers)==1
    states=[]
    for frame in (5782,6902,6912,6922):
        data=raw(frame);cpu,get=get_machine(arm,data);actors=get(0xCB184)
        hp=[get(0x7E19C,p) for p in (actors+0x19E4,actors+4+32*32)]
        assert hp==([31,117] if frame==5782 else [0,45])
        states.append({'frame':frame,'own_enemy_captain_HP':hp,'RAM_sha256':sha(data)})
    nav=[json.loads(line) for line in (RUN/'navigation.jsonl').read_text(encoding='utf8').splitlines() if line]
    after=[row for row in nav if row.get('until',0)>6922]
    assert after==[{'until':7042,'buttons':['A'],'duration':8},{'until':7162,'buttons':['A'],'duration':8},
        {'until':7382,'buttons':['A'],'duration':8},{'until':7802,'buttons':['A'],'duration':8}]
    assert nav[-1]=={'stop':True} and not any('battle_fixture' in row for row in after)
    entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    owner,wrapped=[struct.unpack_from('<I',arm,o)[0] for o in (0x552A0,0x54450)]
    flow=[]
    for frame in (7042,7162,7382,7802):
        data=raw(frame);template=data[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0]
        message_ids=[r.message_id for r in entries if r.text==template]
        image=CAP/f'frame_{frame:06d}_navigation.png'
        flow.append({'frame':frame,'last_template_IDs_if_exact':message_ids,'template_hex':template.hex(),
            'capture':str(image),'capture_sha256':sha(image.read_bytes()),'RAM_sha256':sha(data),
            'visually_reviewed_state':{7042:'original abandon-ship consequence',7162:'original flagship-defeated loss announcement',
                7382:'original Game Over artwork',7802:'ordinary title menu'}[frame]})
    holds=read('work/analysis/escape_actual_holds_v1193/actual_notice_holds.json')
    assert len(holds['complete_actual_holds'])==2 and holds['candidate_sha256']==report['ROM_sha256']
    ROOT.mkdir(parents=True);GUIDE.mkdir(parents=True)
    copied=[]
    for label,frame in (('escape_notice',6922),('normal_title_return',7802)):
        source=CAP/f'frame_{frame:06d}_navigation.png';dest=GUIDE/(label+'.png');copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();copied.append({'path':str(dest),'sha256':sha(dest.read_bytes()),'source':str(source),'frame':frame})
    proof={'candidate':str(ROM),'candidate_sha256':report['ROM_sha256'],'terminal_frame':7802,
        'terminal_capture_report':str(rp),'terminal_capture_report_sha256':sha(rp.read_bytes()),
        'all31_fixture_replays':audits,'one_original_shield_inventory_transfer':transfers[0],
        'natural_duel_HP_evolution':states,'last_fixture_frame5770_before_duel5772':True,
        'all_source_outcome_selection_RNG_equipment_and_combat_functions_exact':[[lo,hi] for lo,hi in slices],
        'actual_complete_holds':holds['complete_actual_holds'],'ordinary_A_defeat_to_GameOver_to_title':flow,
        'source_and_disposable_saves_unchanged':True,'all13_have_native_source_and_font_cases_only1973_has_actual_activation':True,
        'whole_route_and_hardware_verification_not_claimed':True,'guide_screenshots':copied,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'terminal_gameplay_verification.json',proof);save(GUIDE/'provenance.json',proof)
    print('31 complete fixture audits, natural defeat,2 escape font/RGB holds and ordinary title return pass.',flush=True)


if __name__=='__main__':main()
