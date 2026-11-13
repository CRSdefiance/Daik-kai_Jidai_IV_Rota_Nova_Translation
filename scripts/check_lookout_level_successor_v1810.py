"""Validate survival/contact fixture preserving naturally earned level changes."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lookout_contact_v1798c import apply_fixture,ROM,BASE
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lookout_level_successor_v1810')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/observed_lookout_v1799_1775')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');cases=[]
    for frame,context in((5503,'qualify'),(6195,'maintain'),(6471,'maintain')):
        path=CAP/f'frame_{frame:06d}_arm9_ram.bin';raw=path.read_bytes();cpu,get=get_machine(arm,raw)
        actor=get(0xCB184)+4+16*32;level=get(0x7E728,actor)
        after,receipt=apply_fixture(arm,raw,{'lookout_contact':context});verify_cpu,verify=get_machine(arm,after)
        assert verify(0x7E728,actor)==level==receipt['unchanged_level']
        assert not(set(receipt['owned_bytes'])&set(range(actor,actor+32))-{actor+13})
        cases.append({'source_snapshot':str(path),'source_snapshot_sha256':sha(raw),'frame':frame,'fixture':receipt,
            'original_level_after':level,'native_Aim_after':receipt['native_Aim_after'],'level_experience_and_all_non_Luck_actor_bytes_exact':True})
    assert[c['original_level_after']for c in cases]==[37,37,38]
    assert[c['native_Aim_after']for c in cases]==[166,166,168]
    save(ROOT/'level_preserving_fixture_preflight.json',{'cases':cases,'candidate_sha256':sha(ROM.read_bytes()),
        'initial_known_source_actor_qualification_stays_strict':True,'maintenance_accepts_current_original_level_and_Aim':True,
        'no_level_experience_RNG_cursor_message_or_outcome_override':True,'next_live_run_not_yet_performed':True,
        'successor_fixture':'scripts/native_lookout_contact_v1798c.py',
        'successor_fixture_sha256':sha(Path('scripts/native_lookout_contact_v1798c.py').read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Three source snapshots pass:initial37/Aim166 andoriginally earned38/Aim168 preserved. No new live run.',flush=True)
