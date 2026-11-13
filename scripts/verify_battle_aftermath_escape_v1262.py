"""All13 unchanged escape paragraphs through the new generic native gate."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.duel_editorial import owned_entries
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_escape_v1262')


def main():
    assert not ROOT.exists()
    plan_path = Path('work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json')
    plan = read(plan_path)
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')
    raw = Path(context['snapshot']).read_bytes()
    assert sha(raw) == context['snapshot_sha256']
    entries = owned_entries(common,arm,plan['directory_sha256'])
    cpu,get = get_machine(arm,raw)
    root = get(0xCB184)
    captain_id = get(0x7F244)
    captain = root+0x19E4
    vtable = struct.unpack('<I',cpu.mem_read(captain,4))[0]
    pointer = get(struct.unpack('<I',cpu.mem_read(vtable+0x20,4))[0]-0x02000000,captain)
    name = bytes(cpu.mem_read(pointer,64)).split(b'\0')[0]
    assert get(0x7EE08,captain) == captain_id
    objects = [root+4+i*32 for i in range(207) if i != captain_id]+[captain]
    selected = {}
    for table in (0x02117500,0x02117620):
        for actor in objects:
            n = get(0x53F4C,actor,table)
            selected.setdefault(n,(actor,table))
    assert set(selected) == {*range(1951,1957),*range(1973,1980)}
    reference_path = Path('work/analysis/escape_direct_fonts_v1185/native_direct_escape_fonts.json')
    reference = read(reference_path)
    cases = []
    for n,(actor,table) in sorted(selected.items()):
        native = consumer(arm,common,raw,plan,0x53F0C,actor,table,name)
        assert native['input_hex'] == entries[n].text.replace(b'%s',name).hex()
        expected = [r for r in reference['cases'] if r['message_ID'] == n and (not r['variant'] or r['variant']['name_hex'] == name.hex())]
        assert expected and all(r['formatted_hex'] == native['formatted_hex'] for r in expected)
        cases.append({'message_ID':n,'original_actor_object':actor,'original_table':table,
            'native_captain_compact_name_hex':name.hex(),**native,
            'formatted_bytes_exact_to_original_complete_font_approval':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'original_direct_escape_regression.json',{'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),
        'payload_plan':str(plan_path),'payload_plan_sha256':sha(plan_path.read_bytes()),
        'reference_font_proof':str(reference_path),'reference_font_proof_sha256':sha(reference_path.read_bytes()),
        'all13_original_direct_pipeline_cases':cases,'actual_captain_ID':captain_id,
        'all13_prior_escape_formats_fonts_and_source_getters_preserved':True,
        'no_actor_ID_RNG_or_emulator_event_injected':True,'CPU_only_no_new_gameplay_claim':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All13 original direct escape pipelines retain their approved native formatted bytes.',flush=True)


if __name__ == '__main__':
    main()
