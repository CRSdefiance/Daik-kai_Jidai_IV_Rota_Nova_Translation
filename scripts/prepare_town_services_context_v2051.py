"""Complete primary town/service exchanges, preserving raw versus actual scope."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/town_services_source_v2051')
ROM=Path('out/all_routes_combined_v2047_candidate.nds')
CENSUS=Path('work/analysis/editorial_source_census_v1992/all3668_clean_current_native_COMMON_entries.json')
IDS=tuple(n for n in range(85)if n!=64)
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030')

if __name__=='__main__':
    assert not ROOT.exists()
    image,clean=map(NdsImage.open,(ROM,'work/clean.nds'));census=read(CENSUS)
    assert sha(ROM.read_bytes())=='096945ba367a10edbe3e116e49072734a7b6373fdda2b07083c828f72292e227'
    current,original=[im.read_file('/COMMON/MESFILE.DK4')for im in(image,clean)];arm=image.read_file('/__arm9__.bin')
    assert sha(current)==census['current_COMMON_sha256']and sha(original)==census['clean_COMMON_sha256']and sha(arm)==census['current_ARM9_sha256']
    now=entries(current,arm,census['directory_sha256']);before=common_message_entries(original,clean.read_file('/__arm9__.bin'))
    rows=[]
    for n in IDS:
        row=census['records'][n];a,b=before[n],now[n]
        assert row['message_id']==n and a.text.hex()==row['source_hex']and b.text.hex()==row['current_hex']
        assert not row['historical_completed_ID']
        rows.append({**row,'file_path':'/COMMON/MESFILE.DK4',
            'source_reference':{**row['source_reference'],'record_index':a.record_index,'table_offset':a.table_offset,'start_in_record':a.start},
            'current_reference':{**row['current_reference'],'record_index':b.record_index,'table_offset':b.table_offset,'start_in_record':b.start}})
    actual={8:34500,49:31400,51:36100,53:36900,55:37300,56:37700,59:38100,61:38500}
    samples=[]
    for n,frame in actual.items():
        p=CAP/f'frame_{frame:06d}_navigation.png';assert p.exists()
        samples.append(dict(message_id_candidate=n,frame=frame,capture=str(p),capture_sha256=sha(p.read_bytes()),
            visible_text_context_seen=True,native_runtime_message_ID_not_yet_instrumented=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'all84_clean_current_primary_town_service_exchanges.json',dict(candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_COMMON_sha256=sha(current),clean_COMMON_sha256=sha(original),
        ARM9_sha256=sha(arm),directory_sha256=census['directory_sha256'],file_path='/COMMON/MESFILE.DK4',records=rows,
        families=[dict(name='Square crowd alerts',IDs=list(range(8))),dict(name='Trader price checks bargaining and confirmation',IDs=list(range(8,27))),
            dict(name='Port crew repair and supply warnings with resupply offer',IDs=list(range(27,50))),
            dict(name='Formal and casual tavern greetings drink calls and confirmations',IDs=list(range(50,62))),
            dict(name='Facility greetings',IDs=[62,63]),dict(name='Docking and unassigned sailor confirmations',IDs=list(range(65,76))),
            dict(name='Monthly tribute exclusive-contract receipts and item rent',IDs=list(range(76,85)))],
        excluded_neighbor64=dict(source=census['records'][64],reason='Separate ritual-officiant exchange,previously completed. Revisit withits full ceremony family,not asan isolated neighboring shop line. No fresh credit here.'),
        previous_registered_scene_samples=samples,
        source_findings=[
            '54 directly addresses the named barmaid andasks her topour for theguest;currentEnglish changes theguest into the%s recipient.',
            '55 omits theannouncement thatacustomer hasarrived;full drink exchange supplies context.',
            '18 isaper-view fee forcity market quotations,notanunspecified generic report.',
            '27 requires zero sailors andreturn afterhiring orreorganizing;28 isarecommendation forshort crews.',
            '29 loses theexistence ofships needingrepairs;39/40 rawcurrent selections containunrelated crowd text.',
            'Voicevariants mustretain their distinct levels ofpoliteness,urgency andfood concern without invented kinship orranks.',
        ],
        raw_current_selection_is_not_a_blanket_gameplay_or_consumer_reachability_claim=True,
        all84_clean_Japanese_and_current_entries_read_as_complete_functional_exchanges=True,
        native_copy_bounds_format_arguments_active_consumer_and_release_gates_pending=True,
        source_prose_credit=0,completion_credit=0,all_ROMs_and_translations_preserved=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_entries=84,historical_completed_selected=0,excluded_separate_ritual64=True,actual_context_samples=8,new_editorial_credit=0))
