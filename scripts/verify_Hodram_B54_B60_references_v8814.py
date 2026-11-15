"""Bind152 complete maps and82 final references to native entries and exact caller units."""
from copy import deepcopy
from pathlib import Path
from ndspy.code import MainCodeFile,loadOverlayTable
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_references_v8814')
REFERENCE=Path('work/analysis/Hodram_B54_B60_reference_v8812/research_image_receipt.json')
CURRENT=Path('work/analysis/Hodram_B54_B60_current_v8799/current_effective.json')
MAP=Path('work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json')
LOADER=Path('work/analysis/Hodram_B54_B60_loaders_v8813/325_loads14fresh636reused_parent_modes.json')
STORED=Path('work/analysis/Hodram_B54_B60_stored_v8811/stored_pages_controls_andreferences.json')
PRIOR=Path('work/analysis/Hodram_B31_B53_references_v8738/references.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
CONTROL=Path('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json')

if __name__=='__main__':
    assert not ROOT.exists();reference,current,mapping,loader,stored,prior,doc,control=map(read,[REFERENCE,CURRENT,MAP,LOADER,STORED,PRIOR,DOC,CONTROL])
    assert loader['research_ROM_sha256']==reference['research_ROM_sha256'] and loader['fresh_native_whole_loads_andcache_hits']==325
    assert [loader[k] for k in ['fresh_initial_parent_modes','exact_reused_initial_parent_modes','total_bound_initial_parent_modes']]==[14,636,650]
    for key in ['load','parent_mode']:assert sha(Path(loader[key+'_proof']).read_bytes())==loader[key+'_sha256']
    image,parent=[NdsImage.open(reference[k]) for k in ['research_ROM','parent']]
    assert all(sha(Path(reference[k]).read_bytes())==reference[k+'_sha256'] for k in ['research_ROM','parent'])
    assert all(image.read_file(p)==v for p,v in parent.iter_components())
    assert image.read_file('/data/EV1.DK4')==parent.read_file('/data/EV1.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV1.DK4')
    units=[('section'+str(n),s.ramAddress,bytes(s.data)) for n,s in enumerate(MainCodeFile(image.read_file('/__arm9__.bin'),BASE).sections)]
    units += [('overlay'+str(n),s.ramAddress,bytes(s.data)) for n,s in loadOverlayTable(image.rom.arm9OverlayTable,lambda _,f:image.rom.files[f]).items()]
    hashes=[dict(name=n,base=b,bytes=len(d),sha256=sha(d)) for n,b,d in units];assert hashes==prior['native_call_census']['units']
    bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    route=next(r for r in read(loader['load_proof'])['routes'] if r['route']==1);groups=[];allmaps=[];events=[];selections=[]
    for a in current['groups']:
        number=a['block'];b=deepcopy(next(g for g in mapping['groups'] if g['block']==number));block=bank[number]
        source_control=next(g for g in control['groups'] if g['block']==number)
        assert a['all_source_commands']==source_control['all_original_source_commands'] and a['source_event_records']==source_control['source_event_records']
        assert sha(block)==b['target_block_sha256'] and block[:8].hex()==b['target_header_hex'];maps=[]
        for source,old,target,m in zip(a['all_source_commands'],a['all_current_commands'],b['all_target_commands'],b['command_map'],strict=True):
            assert source['word']==old['word']==target['word']==m['word'] and old['offset']==m['old_offset'] and target['offset']==m['new_offset']
            assert old['native_extent']==m['old_extent'] and target['native_extent']==m['new_extent']
            assert old['ancestor_0100_offsets']==m['source_0100_ancestors'] and target['ancestor_0100_offsets']==m['target_0100_ancestors']
            assert block[target['offset']:target['offset']+target['native_extent']].hex()==target['whole_command_hex']
            if target['word']==0x4000:assert source['whole_command_hex'][:12]==old['whole_command_hex'][:12]==target['whole_command_hex'][:12]
            elif target['word'] not in [0x100,0x200,0x300,0x400]:assert source['whole_command_hex']==old['whole_command_hex']==target['whole_command_hex']
            maps.append(deepcopy(m))
        assert len(maps)==len(a['all_source_commands']) and maps[-1]['word']==0 and maps[-1]['new_offset']+4==b['target_logical_end']
        selected=[r for r in route['actions'] if r['kind']==2 and r['native_selected_block']==number]
        assert len(selected)==1 and selected[0]['payload_sha256']==sha(block)
        assert len(a['source_event_records'])==1
        event=a['source_event_records'][0];assert selected[0]['action']==event['action_index'] and selected[0]['word']==event['native_action_word'] and event['script_block']==number
        for ref in b['text_records']:
            row=next(r for r in doc['records'] if r['id']==ref['id'])
            for key in ['source_reference','current_reference','source_selector','source_complete_preamble_hex']:assert ref[key]==row[key]
            final=next(r for r in stored['records'] if r['id']==ref['id'])['final_reference'];at=final['offset'];raw=bytes.fromhex(ref['target_hex'])
            assert final['target_block_sha256']==sha(block) and final['bytes']==len(raw) and block[at:at+len(raw)+1]==raw+b'\0' and block[:at].count(b'\0')==final['record_index']
        b['all_source_commands']=a['all_source_commands'];groups.append(b);allmaps.extend(dict(block=number,**m) for m in maps);events.extend(a['source_event_records']);selections.append(selected[0])
    assert len(allmaps)==152 and sum(len(g['relative_fixups']) for g in groups)==24 and sum(len(r['cases']) for g in groups for r in g['relocated_skip_cases'])==120
    assert len(stored['records'])==82 and len(stored['fresh_target_query_cases'])==6 and len(events)==7
    ROOT.mkdir(parents=True);qualified={**mapping,'groups':groups,'external_references_complete':True,'source_current_final_references_complete':True}
    qualified_path=ROOT/'source_current_final_map.json';save(qualified_path,qualified)
    save(ROOT/'references.json',dict(parent=reference['parent'],parent_sha256=reference['parent_sha256'],research_ROM=reference['research_ROM'],research_ROM_sha256=reference['research_ROM_sha256'],
        file_path='/data/SC1.DK4',blocks=list(range(54,61)),all_command_maps=allmaps,groups=groups,all82_speech_records=stored['records'],source_event_records=events,original_selected_actions=selections,
        native_call_census=deepcopy(prior['native_call_census']),fresh_caller_censuses=0,exact_reused_caller_censuses=1,
        all_original_census_section_overlay_names_bases_lengths_andpayload_hashes_exact=True,exact_prior_census=str(PRIOR),exact_prior_census_sha256=sha(PRIOR.read_bytes()),
        all_shipped_decoded_native_units_andcomponents_bound=True,only_original24070_interpreter_call_no_literal_alias=True,
        all_original_EV1_block_indices325freshloads14fresh636reused_parent_modes_verified=True,
        all152commands82fullpreambles24relatives6queries33nonprose_controls7normalends_bound=True,
        original_entry_payload_offset=8,no_interior_entry_offsets_orunmapped_nested_relative_targets=True,
        source_event_dependencies_preserved_not_natural_eligibility_location_orchronology_proof=True,external_references_complete=True,
        reference_scope_not_arbitrary_dynamic_pointer_orall_attainable_paths_proof=True,
        actual_headers_FE_progressive_transitions_policy_atomic_registered_release_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [REFERENCE,CURRENT,MAP,LOADER,STORED,PRIOR,DOC,CONTROL,Path(__file__)]}))
    print('All152commands/82finalrefs/7EV1entries bound;24relative sites120cases/6queries/fullends;exact native caller-unit census reused.No actual/credit.',flush=True)
