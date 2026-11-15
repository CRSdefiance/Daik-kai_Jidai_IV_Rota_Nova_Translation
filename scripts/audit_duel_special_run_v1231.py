"""Terminal whole-RAM fixture/input audit of the first natural no-special run."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_duel_special_fixture_v1225 import apply_fixture, ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_special_terminal_v1231')
RUN = Path('work/analysis/duel_special_live_v1225')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_special_v1225_1224')
BASE = 0x02000000


def main():
    assert not ROOT.exists()
    report = read(CAP/'capture_report.json')
    assert report['frames'] == 12302 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['ROM_sha256'] == sha(ROM.read_bytes())
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert read(RUN/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0xE8CC,0x11000),(0x7DF58,0x7E1A4),(0xD458,0xD540),(0x519D4,0x51A28),(0xD9824,0xD9868))
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi]
    snapshots = {}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        if r['frame'] in snapshots:
            assert snapshots[r['frame']]['sha256'] == r['sha256']
        snapshots[r['frame']] = r
    def raw(frame):
        row = snapshots[frame]
        data = Path(row['path']).read_bytes()
        assert len(data) == row['bytes'] == 0x400000 and sha(data) == row['sha256']
        return data
    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 31 and max(r['frame'] for r in fixtures) == 5770
    seed, flag = [struct.unpack_from('<I',arm,o)[0] for o in (0xD9858,0x51A20)]
    audits = []
    for r in fixtures:
        request = {'sighting_context':'compassAttack8'} if r['context']=='compassAttack8' else {'duel_context':'healthyContact'}
        before = raw(r['frame'])
        after, receipt = apply_fixture(arm,before,request)
        assert r == {**receipt,'frame':r['frame']}
        owned = set(r['owned_bytes'])
        assert all(BASE+i in owned for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b)
        for at in (seed,flag):
            assert not owned.intersection(range(at,at+4)) and before[at-BASE:at-BASE+4] == after[at-BASE:at-BASE+4]
        bc,bget = get_machine(arm,before)
        ac,aget = get_machine(arm,after)
        assert [bget(o) for o in (0x7F244,0x2E58C)] == [aget(o) for o in (0x7F244,0x2E58C)] == [1,1]
        actors = bget(0xCB184)
        assert aget(0xCB184) == actors
        objects = [actors+4+i*32 for i in range(207)]+[actors+0x19E4]
        assert [bget(0x7EE08,o) for o in objects] == [aget(0x7EE08,o) for o in objects]
        if r['context']=='healthyContact':
            assert all(v>0 for v in r['positive_captain_HP_before'])
            assert all(v>=2000 for v in r['positive_captain_HP_after'])
            assert len(owned)==28
        audits.append({'frame':r['frame'],'context':r['context'],'owned_bytes':len(owned),
            'before_RAM_sha256':sha(before),'after_RAM_sha256':sha(after),
            'all4MiB_changes_declared_all208_actor_IDs_and_RNG_unchanged':True})
        if len(audits)%10==0:
            print(len(audits),'full fixture replays and208 original actor identities pass',flush=True)
    journal = read(CAP/'navigation_command_journal.json')
    assert all(r['validation_passed'] for r in journal['commands_received'])
    schedule = read(RUN/'original_load_inputs.json')
    for r in journal['commands_received']:
        c = r['command']
        if c.get('stop'):
            continue
        assert c['until'] in snapshots and c['until']>r['frame']
        if r['frame']>=5772:
            assert 'battle_fixture' not in c
        if c.get('buttons') or c.get('touch') is not None:
            event = {'start':r['frame']+1,'duration':c.get('duration',12),'buttons':c.get('buttons',[])}
            if c.get('touch') is not None:
                event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    scan = read('work/analysis/duel_special_actual_v1228/scan_through12302.json')
    assert not scan['complete_visible_holds']
    assert scan['original_HP_evolution'][-1]['own_enemy_HP']==[128,0]
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_fixture_input_and_no_special_result.json', {
        'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'terminal_frame':12302,
        'report':str(CAP/'capture_report.json'),'report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'fixture_replays':audits,'all31_fixtures_before_duel5772':True,
        'actual_controller_schedule_matches_accepted_commands':True,
        'all_original_duel_HP_and_RNG_source_spans_unchanged':[[lo,hi] for lo,hi in spans],
        'extra_positive_HP_clamps_to_original_maximum_on_first_damage':True,
        'natural_victory_without_special_observed':True,'no_special_completion_credit':True,
        'source_and_disposable_saves_unchanged':True,
        'no_healing_revival_relocation_actor_ID_RNG_or_result_edits_during_or_after_duel':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Terminal12302:31 full fixture audits and exact ordinary inputs pass;no special activation credit.',flush=True)


if __name__ == '__main__':
    main()
