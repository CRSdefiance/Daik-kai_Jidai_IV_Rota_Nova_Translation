"""Extend strict predicate ownership only for the original operand scratch helper."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    print(derive('scripts/prove_lil_B182_predicate500_v4883.py','scripts/prove_lil_B182_predicate500_v4896.py',{
        'Original500 predicate: strict threshold result and exactly one owned RNG write.':
        'Original500 predicate: exact RNG and source-owned unaligned operand scratch writes.',
        'predicate500_v4883':'predicate500_v4896',
        '(0x29874,0x29968)]':'(0x29874,0x29968),(0x2A5BC,0x2A600)]',
        "    writes=[];calls=[];returns=[]":
        "    scratch_address=struct.unpack_from('<I',arm,0x2A5E8)[0];assert scratch_address==0x02279600\n    unaligned=(stream+command['offset']+4)%4!=0\n    assert (stream+command['offset']+4)%4 in [0,2]\n    scratch_before=bytes(cpu.mem_read(scratch_address,4));helper_inputs=[]\n    writes=[];calls=[];returns=[]",
        "        if pc==BASE+0x519D4:calls.append(dict(PC=pc,bound=u.reg_read(UC_ARM_REG_R0)))":
        "        if pc==BASE+0x2A5BC:helper_inputs.append(u.reg_read(UC_ARM_REG_R0))\n        elif pc==BASE+0x519D4:calls.append(dict(PC=pc,bound=u.reg_read(UC_ARM_REG_R0)))",
        "hooks=[cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x519D4,end=BASE+0x519D4),":
        "hooks=[cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x2A5BC,end=BASE+0x2A5BC),\n           cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x519D4,end=BASE+0x519D4),",
        "    expected_writes=[dict(PC=BASE+0xD984C,address=seed_address,size=4,value=next_seed)]":
        "    assert helper_inputs==[stream+command['offset']+4]\n    scratch_writes=[dict(PC=BASE+0x2A5D8,address=scratch_address,size=4,value=500)] if unaligned else []\n    expected_seed_writes=[dict(PC=BASE+0xD984C,address=seed_address,size=4,value=next_seed)]\n    expected_writes=scratch_writes+expected_seed_writes",
        "    assert bytes(cpu.mem_read(BASE,0x400000))==expected":
        "    if unaligned:struct.pack_into('<I',expected,scratch_address-BASE,500)\n    assert bytes(cpu.mem_read(BASE,0x400000))==expected",
        "    cpu.mem_write(seed_address,struct.pack('<I',seed))\n    assert bytes(cpu.mem_read(BASE,0x400000))==before":
        "    cpu.mem_write(seed_address,struct.pack('<I',seed))\n    if unaligned:cpu.mem_write(scratch_address,scratch_before)\n    assert bytes(cpu.mem_read(BASE,0x400000))==before",
        'original_native_seed_writes=writes':'original_native_seed_writes=expected_seed_writes,all_original_native_writes=writes,unaligned_operand_scratch_writes=scratch_writes,original_operand_helper_inputs=helper_inputs,operand_pointer_unaligned=unaligned',
        'full4MiB_difference_exactly_one_original_owned_RNG_word=True':
        'full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch=True',
        'cleanup_restores_owned_seed_and_recovers_all4MiB=True':
        'cleanup_restores_only_owned_seed_and_optional_scratch_and_recovers_all4MiB=True',
        "    predicates=[c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0x8000]":
        "    predicates=[c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0x8000]\n    relocation=read('work/analysis/lil_B182_relocation_v4893/nested_source_relocation_research.json')['blocks'][0]\n    blocks.append(Path(relocation['research_block']).read_bytes())\n    assert sha(blocks[-1])==relocation['research_block_sha256']\n    mapping={c['old_offset']:c['new_offset'] for c in relocation['command_map']}",
        "for label,block in zip(['clean','current'],blocks,strict=True):\n        for c in predicates:":
        "for label,block in zip(['clean','current','relocated'],blocks,strict=True):\n        for original_c in predicates:\n            c={**original_c,'offset':mapping[original_c['offset']] if label=='relocated' else original_c['offset']}",
        'len(cases)==16 and sum(r[\'unforced_current_snapshot\'] for r in cases)==4':
        'len(cases)==24 and sum(r[\'unforced_current_snapshot\'] for r in cases)==6',
        "    save(ROOT/'all16_original500_predicate_RNG_ownership_cases.json'":
        "    for original_at in [512,544]:\n        for fixture in [None,*fixtures.values()]:\n            pair=[r for r in cases if r['version'] in ['current','relocated'] and r['offset']==(mapping[original_at] if r['version']=='relocated' else original_at) and r['supplied_CPU_only_seed_fixture']==fixture]\n            assert len(pair)==2 and pair[0]['native_result']==pair[1]['native_result'] and pair[0]['after_seed']==pair[1]['after_seed']\n            assert not pair[0]['operand_pointer_unaligned'] and pair[1]['operand_pointer_unaligned']\n    save(ROOT/'all24_aligned_and_unaligned_original500_ownership_cases.json'",
        'unforced_cases=4,CPU_only_boundary_fixture_cases=12':'unforced_cases=6,CPU_only_boundary_fixture_cases=18',
        'all16_seed_transitions_native_results_and_unowned4MiB_checks_pass':'all24_seed_and_operand_scratch_transitions_native_results_and_unowned4MiB_checks_pass',
        'cases=16,unforced=4,CPU_boundary_fixtures=12':'cases=24,unforced=6,CPU_boundary_fixtures=18'
    }))
