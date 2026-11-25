"""Fresh325 archive-offset loads;14 changed parent cases,636 exact prior cases reused."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_loaders_v8813')
RECEIPT=Path('work/analysis/Hodram_B54_B60_reference_v8812/research_image_receipt.json')
PRIOR=Path('work/analysis/Hodram_B31_B53_loaders_v8737/325_whole_native_loads_cache_hits650_initial_parent_modes.json')

if __name__=='__main__':
    assert not ROOT.exists();receipt,prior=map(read,[RECEIPT,PRIOR]);rompath=Path(receipt['research_ROM']);parentpath=Path(receipt['parent'])
    assert sha(rompath.read_bytes())==receipt['research_ROM_sha256'] and sha(parentpath.read_bytes())==receipt['parent_sha256']==prior['research_ROM_sha256']
    oldmodes_path=Path(prior['parent_mode_proof']);oldload_path=Path(prior['load_proof'])
    assert sha(oldmodes_path.read_bytes())==prior['parent_mode_sha256'] and sha(oldload_path.read_bytes())==prior['load_sha256']
    oldmodes,oldloads=map(read,[oldmodes_path,oldload_path]);image,baseline=NdsImage.open(rompath),NdsImage.open(parentpath)
    arm=image.read_file('/__arm9__.bin');assert arm==baseline.read_file('/__arm9__.bin')
    before,after=[IlnkContainer.parse(i.read_file('/data/SC1.DK4')).blocks for i in [baseline,image]]
    changed=set(receipt['only_changed_blocks']);assert changed==set(range(54,61)) and len(before)==len(after)==325
    assert [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==sorted(changed)
    assert image.read_file('/data/EV1.DK4')==baseline.read_file('/data/EV1.DK4')==NdsImage.open('work/clean.nds').read_file('/data/EV1.DK4')
    cases_by_block={n:[c for c in oldmodes['native_handoff_and_first_read_cases'] if c['route']==1 and c['block']==n] for n in range(325)}
    old_actions={c['native_selected_block']:c for c in oldloads['routes'][0]['actions'] if c['kind']==2}
    for index in range(325):
        assert len(cases_by_block[index])==2 and {c['mode'] for c in cases_by_block[index]}=={0,1}
        assert old_actions[index]['payload_sha256']==sha(before[index])
        if index not in changed:
            assert before[index]==after[index]
            assert all(c['source_block_sha256']==sha(after[index]) and c['whole_source_header_payload_cache_metadata_and_tail_guard_exact'] and c['first_instruction_pointer_and_mode_derived_by_original_parent'] for c in cases_by_block[index])
    ev=image.read_file('/data/EV1.DK4');begin,end=struct.unpack_from('<2I',ev,0x4C);expected=(end-begin)//2;assert expected==326
    loader_adapter=prior['source_owned_loader_adapter'];env={**loader.__dict__,'EXPECTED_ACTIONS':expected}
    exec(compile(loader_adapter,__file__+'::fresh-changed-archive-offsets','exec'),env)
    parent_adapter=checked_text(prior['source_owned_parent_adapter'],{
        '                for mode in (0, 1):':"""                if index not in CHANGED_BLOCKS:
                    cases.extend(REUSED_PARENT_CASES[index])
                    continue
                for mode in (0, 1):"""
    })
    penv={**parent.__dict__,'CHANGED_BLOCKS':changed,'REUSED_PARENT_CASES':cases_by_block}
    exec(compile(parent_adapter,__file__+'::fresh14-exact636-reuse','exec'),penv)
    ROOT.mkdir(parents=True);loads=env['run'](image,'research');lp=ROOT/'whole_SC1_native_loads.json';save(lp,loads)
    modes=penv['run'](image,'research',loads);mp=ROOT/'whole_SC1_native_parent_modes.json';save(mp,modes)
    fresh=[c for c in modes['native_handoff_and_first_read_cases'] if c['block'] in changed]
    reused=[c for c in modes['native_handoff_and_first_read_cases'] if c['block'] not in changed]
    assert len(fresh)==14 and len(reused)==636 and len(loads['routes'][0]['actions'])==326
    assert all(c in cases_by_block[c['block']] for c in reused)
    save(ROOT/'325_loads14fresh636reused_parent_modes.json',dict(research_ROM=str(rompath),research_ROM_sha256=receipt['research_ROM_sha256'],parent=str(parentpath),parent_sha256=receipt['parent_sha256'],
        original_action_count=326,fresh_native_whole_loads_andcache_hits=325,fresh_initial_parent_modes=14,exact_reused_initial_parent_modes=636,total_bound_initial_parent_modes=650,
        fresh_parent_blocks=sorted(changed),load_proof=str(lp),load_sha256=sha(lp.read_bytes()),parent_mode_proof=str(mp),parent_mode_sha256=sha(mp.read_bytes()),
        prior_complete_loader_proof=str(PRIOR),prior_complete_loader_proof_sha256=sha(PRIOR.read_bytes()),prior_mode_proof=str(oldmodes_path),prior_mode_proof_sha256=sha(oldmodes_path.read_bytes()),
        fresh_whole_bank_loads_justified_by_relocated_archive_file_offsets=True,unchanged318_parent_inputs_reused_only_by_exact_payload_andwhole_current_ARM9_binding=True,
        all_original_EV1_actions_select_block_indices_not_interior_offsets=True,both_original_parent_modes_begin_payload_plus8=True,
        all_payload_cache_metadata_neighbor_guards_SP_PC_andABI_exact=True,original_executed_instructions_exact_only_SDK_IO_bridges=True,
        source_owned_loader_adapter=loader_adapter,source_owned_parent_adapter=parent_adapter,controlled_native_route_global_inputs_not_ordinary_event_activation=True,
        no_new_caller_census_oractual_gameplay_claim=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RECEIPT,PRIOR,oldmodes_path,oldload_path,Path(loader.__file__),Path(parent.__file__),Path(__file__)]}))
    print('325 fresh archive loads/cache hits/326actions;14fresh parent modes plus636 exact reuses;full payload/metadata/ABI/first-read guards pass.No gameplay/credit.',flush=True)
