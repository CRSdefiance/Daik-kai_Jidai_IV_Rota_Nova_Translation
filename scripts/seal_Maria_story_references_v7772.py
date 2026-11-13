"""Seal exact67 approved decisions,three original entries andcomplete reversible archive."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.maria_story_reconstruction_v1 import reconstruct
from scripts.Maria_story_final_paths_v7771 import *
from scripts.verify_village_wrap_v608 import read,save
FLAGS=['external_references_complete','all67_sixbyte_preambles_macros_selectors_preserved','all116_commands20_relative_sites_source_bound',
    'all_three_clean_andpredecessor_blocks_andfull_archive_inverse_exact','all303_native_loads606_parent_modes_shipped_callers_bound',
    'all67_final_native_stored_source_current_andactual_refs_bound','two_Julian_conditionals_explicitly_offline',
    'all_measured_timing_RNG_state_RGB_andnatural_activation_limits_preserved','shared155_semantics_full207_names_andbroader_goal_open']
if __name__=='__main__':
    assert not MAP.exists() and not SEALED.exists() and not SEAL.parent.exists()
    mapping,approval,current,doc,branches=map(read,[RELOCATION,APPROVAL,CURRENT,APPROVED,Path(proofs()['source_branch_proof'])])
    assert approval['all67_individual_five_gates_approved'] and approval['manuscript_sha256']==sha(APPROVED.read_bytes())
    loader,census,actual,view=map(read,[proofs()['native_loader_proof'],proofs()['native_caller_proof'],ACTUAL,VIEW])
    assert loader['fresh_native_whole_loads_andcache_hits']==303 and loader['fresh_initial_parent_modes']==606
    assert census['only_original24070_interpreter_call_no_literal_alias'] and view['all130_final_actual_panes_viewed_with_exact_reuse']
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==doc['current_ROM_sha256']
    before,after,clean=[NdsImage.open(p) for p in [PARENT,ROM,'work/clean.nds']]
    oldbank,newbank,cleanbank=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks for im in [before,after,clean]]
    groups=[]
    for spec in mapping['groups']:
        number=spec['block'];packet=next(g for g in current['groups'] if g['block']==number)
        rows=[r for r in doc['records'] if r['block']==number]
        target=reconstruct(oldbank[number],cleanbank[number],spec,packet,rows,branches['operands_requiring_adjustment_when_resizing'])
        assert target==newbank[number]
        cg=next(g for g in census['groups'] if g['block']==number)
        assert cg['all_command_maps']==spec['command_map'] and cg['relative_operand_maps']==spec['relative_fixups']
        sealed=deepcopy(spec);sealed.update(route=3,route_identity='Maria',external_references_complete=True,
            original_entry_payload_offset=8,source_archive_sha256=sha(before.read_file('/data/SC3.DK4')),
            target_archive_sha256=sha(after.read_file('/data/SC3.DK4')),approved_manuscript=str(APPROVED),approved_manuscript_sha256=sha(APPROVED.read_bytes()))
        groups.append(sealed)
    assert [i for i,(a,b) in enumerate(zip(oldbank,newbank,strict=True)) if a!=b]==[34,35,108]
    restored=list(newbank)
    for group in groups:restored[group['block']]=oldbank[group['block']]
    assert IlnkContainer(restored).to_bytes()==before.read_file('/data/SC3.DK4')
    assert [p for _,p,v in before.iter_files() if after.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(after.read_file(p)==v for p,v in before.iter_components())
    evidence={str(p):sha(p.read_bytes()) for p in [RELOCATION,APPROVAL,APPROVED,*map(Path,proofs().values()),Path('dk4tool/patch/maria_story_reconstruction_v1.py'),Path(__file__)]}
    save(MAP,dict(format='dk4-Maria67-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path='/data/SC3.DK4',
        source_archive_sha256=sha(before.read_file('/data/SC3.DK4')),target_archive_sha256=sha(after.read_file('/data/SC3.DK4')),
        groups=groups,preserve_record_parity=True,observed_comparison_contract=read(VIEW)['final_late_limits'],
        evidence=evidence,**{k:True for k in FLAGS},new_credit=0,full_goal_complete=False))
    successor=deepcopy(doc);successor.update(native_approved_manuscript=str(APPROVED),native_approved_manuscript_sha256=sha(APPROVED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),
        reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),status='67 exact decisions andthree-block references sealed;atomic registered integration pending')
    save(SEALED,successor);SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        all67_five_gates_andexact_references_approved=True,all116_commands20_relative_sites_source_bound=True,
        complete_three_source_predecessor_blocks_andwhole_archive_inverse_exact=True,
        final_actual65_eachlanguage_two_Julian_conditionals_offline=True,all_measured_late_andname_scope_limits_preserved=True,
        evidence=evidence,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('67decisions/three blocks sealed;116commands/20relative sites;full clean+predecessor inverse/all300otherblocks exact.Atomic production/release pending;zero credit.')
