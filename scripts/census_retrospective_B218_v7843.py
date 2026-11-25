"""Bound all15 original commands and shipped static callers for the one wrap change."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_caller_census_v7843')
REF=Path('work/analysis/retrospective_B218_reference_v7841/research_image_receipt.json')
MAP=Path('work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json')
LOAD=Path('work/analysis/retrospective_B218_loader_v7842/whole_SC2_336_loads_cache_hits672_original_parent_modes.json')
PRIOR=Path('work/analysis/lil_B218_reference_census_v6898/all15_commands_no_relative_or_typed_sites_and_shipped_census.json')
SOURCE=Path('work/analysis/lil_B218_source_v6875/thirteen_clean_current_Ares_legend_exchange_source_references.json')
if __name__=='__main__':
    assert not ROOT.exists();ref,mapping,load,prior,source=map(read,[REF,MAP,LOAD,PRIOR,SOURCE])
    current,target,clean=[NdsImage.open(p) for p in [ref['parent'],ref['research_ROM'],'work/clean.nds']]
    assert sha(Path(ref['parent']).read_bytes())==ref['parent_sha256']==mapping['candidate_sha256']
    assert sha(Path(ref['research_ROM']).read_bytes())==ref['research_ROM_sha256']==load['research_ROM_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==source['source_ROM_sha256']=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert load['all336_native_loads_cache_hits_and672_modes_pass'] and load['original_parent_both_modes_start_at_loaded_payload_plus8']
    assert current.read_file('/__arm9__.bin')==target.read_file('/__arm9__.bin')
    assert all(target.read_file(p)==v for _,p,v in current.iter_files() if p!='/data/SC2.DK4')
    assert all(target.read_file(p)==v for p,v in current.iter_components())
    fresh=census(target)
    assert [r['address'] for r in fresh['branches']]==[0x02024070] and not fresh['literal_aliases']
    previous_clean=deepcopy(prior['native_call_census']['clean'])
    assert [r['address'] for r in previous_clean['branches']]==[0x02024070] and not previous_clean['literal_aliases']
    banks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [clean,current,target]]
    assert all(len(b)==336 for b in banks) and [i for i,(a,b) in enumerate(zip(banks[1],banks[2],strict=True)) if a!=b]==[218]
    inventory,_,_=scoped_inventory();jp=inventory(clean.read_file('/__arm9__.bin'),banks[0][218])[0]
    old=mapping['current_packet']['all_current_commands'];g=mapping['groups'][0];new=g['all_target_commands']
    assert len(jp)==len(old)==len(new)==15 and not g['relative_fixups']
    rows=[]
    for a,b,c,m in zip(jp,old,new,g['command_map'],strict=True):
        assert a['word']==b['word']==c['word']==m['word']
        assert m['old_offset']==b['offset'] and m['new_offset']==c['offset']
        if a['word']==0x4000:
            assert banks[0][218][a['offset']:a['offset']+6]==banks[1][218][b['offset']:b['offset']+6]==banks[2][218][c['offset']:c['offset']+6]
        else:assert a['whole_command_hex']==b['whole_command_hex']==c['whole_command_hex']
        rows.append(dict(clean=a,current=b,target=c,mapping=m))
    assert sum(r['target']['word']==0x4000 for r in rows)==13
    assert [r['target']['word'] for r in rows if r['target']['word']!=0x4000]==[0xA000,0]
    ROOT.mkdir(parents=True);save(ROOT/'all15_commands_original_entry_andbounded_shipped_callers.json',dict(
        parent=ref['parent'],parent_sha256=ref['parent_sha256'],research_ROM=ref['research_ROM'],research_ROM_sha256=ref['research_ROM_sha256'],
        fresh_target_native_call_census=fresh,current_census_reused_byall_native_units_exact_to_target=True,
        exact_immutable_clean_census_reused=previous_clean,prior_clean_census=str(PRIOR),prior_clean_census_sha256=sha(PRIOR.read_bytes()),
        all15_clean_current_target_commands_bound=rows,all13_six_byte_preambles_andopaque_A000_full_end_exact=True,
        no_relative_predicate_typed_or_interior_byte_targets=True,original_VM_entry_offset=8,
        only_original24070_interpreter_call_andno_literal_alias=True,
        bounded_shipped_unit_census_does_not_prove_arbitrary_dynamic_mutation=True,
        current_actual_scene_policy_atomic_andregistered_release_pending=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [REF,MAP,LOAD,PRIOR,SOURCE,Path(__file__)]},full_goal_complete=False))
    print('All15 clean/current/target commands and13 preambles bound;one fresh bounded shipped census/original24070 caller/no literal alias pass.')
