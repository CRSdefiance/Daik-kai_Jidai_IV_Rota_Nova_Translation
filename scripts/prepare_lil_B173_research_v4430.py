"""Prepare B173 research references;reuse the byte-identical verified parent loader."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B173_research_tools_v4430')
PARENT=Path('out/all_routes_combined_v4404_candidate.nds')
ROM=Path('out/lil_B173_reference_v4431_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B173_relocation_v4428/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4353' and len(registry['accepted_layers'])==114
    assert 'all-routes-unified-v4404' in registry['profiles']
    tools=[derive('scripts/create_lil_B172_reference_v4384.py','scripts/create_lil_B173_reference_v4431.py',{
        'V4353':'V4404','lil_B172_research_v4384':'lil_B173_research_v4431',
        'all_routes_combined_v4353':'all_routes_combined_v4404','lil_B172_reference_v4384':'lil_B173_reference_v4431',
        'lil_B172_relocation_v4381':'lil_B173_relocation_v4428',
        'lil_B172_stored_v4382/all27_final_stored_targets108':'lil_B173_stored_v4429/all11_final_stored_targets44',
        'editorial_handoff_verification_v4380':'editorial_handoff_verification_v4427','all27_final_targets':'all11_final_targets',
        "current_final_stored_macro_alignment_cases']==108":"current_final_stored_macro_alignment_cases']==44",
        'current_final_stored_macro_alignment_cases=108':'current_final_stored_macro_alignment_cases=44',
        '[172]':'[173]','actual_selected_B172_IDs':'actual_selected_B173_IDs',
    })]
    source=Path('scripts/verify_lil_B172_loader_v4385.py');target=Path('scripts/verify_lil_B173_loader_v4432.py');assert not target.exists()
    text=source.read_text(encoding='utf-8')
    loop="    for label, path in [('current', PARENT), ('research', ROM)]:"
    assert loop in text
    text=text.replace(loop,'''    prior_path=Path('work/analysis/lil_B172_loader_v4385/whole_SC2_and_B172_initial_entry_proof.json')
    prior=read(prior_path)
    reused=next(row for row in prior['versions'] if row['label']=='research')
    assert sha(PARENT.read_bytes())==reused['ROM_sha256']
    for key in ['load','parent']:
        assert sha(Path(reused[key+'_proof']).read_bytes())==reused[key+'_sha256']
    assert prior['all336_whole_blocks_and672_modes_each_pass'] and prior['all_payload_cache_metadata_and_tail_guards_exact']
    results.append({**reused,'label':'current','proof_method':'Exact whole-ROM hash reuse of prior research image,now identical to registered V4404;no parent rerun.',
        'prior_loader_proof':str(prior_path),'prior_loader_proof_sha256':sha(prior_path.read_bytes()),'prior_version_label':'research'})
    for label, path in [('research', ROM)]:''')
    changes={'prepare_lil_B172_research_v4383':'prepare_lil_B173_research_v4430',
        'lil_B172_loader_v4385':'lil_B173_loader_v4432','lil_B172_research_v4384':'lil_B173_research_v4431',
        'whole_SC2_and_B172_initial_entry_proof':'whole_SC2_and_B173_initial_entry_proof','B172_fits':'B173_fits',
        'one B172 resized block':'one B173 resized block',
        "        'versions': results,":"        'versions': results,'fresh_research_whole_SC2_loads':336,'exact_parent_reused_whole_SC2_loads':336,'fresh_parent_modes':672,'exact_parent_reused_modes':672,",
        "Both ROMs:336 original loads/cache hits and672 parent entry modes pass;source entry contracts pass;representative/release approval pending.":"New B173 research:336 original loads/cache hits and672 modes pass;byte-identical V4404 parent proof reused exactly. Representative/release pending.",
    }
    for key in changes:assert key in text,key
    # Preserve the literal prior-proof path while replacing independent identifiers.
    changes['work/analysis/lil_B172_loader_v4385/whole_SC2_and_B172_initial_entry_proof.json']='work/analysis/lil_B172_loader_v4385/whole_SC2_and_B172_initial_entry_proof.json'
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
    tools.append(dict(previous=str(source),previous_sha256=sha(source.read_bytes()),successor=str(target),successor_sha256=sha(target.read_bytes())))
    common={'prepare_lil_B172_research_v4383':'prepare_lil_B173_research_v4430'}
    tools.append(derive('scripts/verify_lil_B172_references_v4386.py','scripts/verify_lil_B173_references_v4433.py',{
        **common,'lil_B172_reference_census_v4386':'lil_B173_reference_census_v4433',
        'lil_B172_loader_v4385':'lil_B173_loader_v4432','B172':'B173','[172]':'[173]',
        'for r in result)==38':'for r in result)==23','all38':'all23','native_commands_each=38':'native_commands_each=23',
        '38-command/zero-span':'23-command/four-span',
        "sum(r['typed_relative_span_count']for r in result)==0":"sum(r['typed_relative_span_count']for r in result)==4",
        "sum(r['target_native_skip_cases']for r in result)==0":"sum(r['target_native_skip_cases']for r in result)==20",
        'commands_zero_relative_sites_and_shipped_entry_census':'commands_four_relative_sites_and_shipped_entry_census',
        'commands_and_zero_relative_sites_reexecuted':'commands_and_four_relative_sites_reexecuted',
        'relative_sites=0,target_native_skip_cases=0':'relative_sites=4,target_native_skip_cases=20',
    }))
    tools.append(derive('scripts/prove_lil_B172_ends_v4387.py','scripts/prove_lil_B173_ends_v4434.py',{
        **common,'B172':'B173','lil_B172_ends_v4387':'lil_B173_ends_v4434','n==172':'n==173',
        'two_declared_end_decodes_and_zero_relative_sites':'two_declared_end_decodes_and_four_relative_sites',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=173,structural_commands=23,relative_sites=4,target_cases=20,pause=0,C200=0,endwords=1,
        nonrelative_leaves=8,source_resources=[0x6329,0x6340],source_A000_offsets=[720,748],source_predicate_offset=728,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),promoted_main='all-routes-unified-v4353',
        research_parent='all-routes-unified-v4404',whole_ROM_exact_parent_loader_reuse=True,no_registry_ledger_credit_change=True,full_goal_complete=False))
    print('Prepared B173 research image,one fresh whole loader with exact parent reuse,23-command/four-span census and guarded single end.')
