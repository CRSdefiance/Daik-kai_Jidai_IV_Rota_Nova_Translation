"""Derive independent B51 production reconstruction with eight native relatives."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_reconstruction_v8585')
    assert not root.exists()
    source = Path('dk4tool/patch/hodram_B49_reconstruction_v2.py').read_text('utf-8')
    menu = source[source.index("    require(len(group['choice_commands'])"):source.index('    patches.sort(')]
    menu_refs = source[source.index("    require(mapped(choice['old_offset'])"):source.index('    for clean_version in [False,True]:')]
    result = derive('dk4tool/patch/hodram_B49_reconstruction_v2.py', 'dk4tool/patch/hodram_B51_reconstruction_v1.py', {
        'Hodram B49 reconstruction:': 'Hodram B51 reconstruction:',
        'def reconstruct(old,clean,group,packet,rows,edges,choice_rows,typed):': 'def reconstruct(old,clean,group,packet,rows,edges):',
        "    end=8+struct.unpack_from('<H',old,4)[0]":
            "    require(group['block']==51 and len(rows)==5 and not group['choice_commands'],'exact B51 five-record no-menu scope')\n    require(len(packet['all_current_commands'])==20 and sum(c['word'] in [0x8000,0x8100] for c in packet['all_current_commands'])==2 and not any(c['word']==0x2100 for c in packet['all_current_commands']),'complete20commands/twoqueries/no-menu')\n    end=8+struct.unpack_from('<H',old,4)[0]",
        menu: '', menu_refs: '',
        "        elif word==0x2100:require(a==choice['old_offset'] and z==choice['new_offset'] and target[z:z+new['native_extent']]==typed,'complete original-provider menu')\n": '',
        "len(selected)==len(group['relative_fixups'])": "len(selected)==len(group['relative_fixups'])==8",
    })
    from dk4tool.patch.hodram_B51_reconstruction_v1 import reconstruct
    packetpath = Path('work/analysis/Hodram_B51_current_v8559/current_effective.json')
    mappingpath = Path('work/analysis/Hodram_B51_references_v8572/source_current_final_map.json')
    sourcepath = Path('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')
    docpath = Path('translations/hodram_B51_editorial_manuscript_v5.json')
    mapping, packet, controls, doc = map(read, [mappingpath, packetpath, sourcepath, docpath])
    group, packet = mapping['groups'][0], packet['groups'][0]
    original = dict(old=bytes.fromhex(packet['current_block_hex']), clean=bytes.fromhex(packet['clean_block_hex']),
        group=group, packet=packet, rows=doc['records'], edges=controls['operands_requiring_adjustment_when_resizing'])
    expected = Path(group['target_block']).read_bytes()
    target = reconstruct(**original)
    assert target == expected and sha(target) == group['target_block_sha256']
    cases = []
    def reject(label, mutate):
        changed = deepcopy(original)
        mutate(changed)
        assert changed != original
        try:
            reconstruct(**changed)
        except ValueError as error:
            cases.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed reconstruction input accepted: ' + label)
    reject('missing-relative-site', lambda d: d['edges'].pop())
    reject('missing-relative-fixup', lambda d: d['group']['relative_fixups'].pop())
    reject('relative-endpoint', lambda d: d['group']['relative_fixups'][0].__setitem__('new_matched_skip_target', d['group']['relative_fixups'][0]['new_matched_skip_target'] + 2))
    reject('relative-source-span', lambda d: d['edges'][0].__setitem__('source_span', d['edges'][0]['source_span'] + 2))
    reject('relative-target-span', lambda d: d['group']['relative_fixups'][0].__setitem__('target_span', d['group']['relative_fixups'][0]['target_span'] + 2))
    reject('unapproved-menu', lambda d: d['group']['choice_commands'].append(dict(word=0x2100)))
    nested = next(i for i, c in enumerate(group['all_target_commands']) if c['ancestor_0100_offsets'])
    reject('nested-source-scope', lambda d: d['group']['command_map'][nested].__setitem__('source_0100_ancestors', []))
    reject('nested-target-scope', lambda d: d['group']['all_target_commands'][nested].__setitem__('ancestor_0100_offsets', []))
    query = next(i for i, c in enumerate(group['all_target_commands']) if c['word'] == 0x8000)
    reject('raw-query-body', lambda d: d['group']['all_target_commands'][query].__setitem__('whole_command_hex', '0080ffff12fe0130'))
    reject('truncated-full-end', lambda d: d['group']['all_target_commands'][-1].__setitem__('native_extent', 2))
    reject('invented-tail', lambda d: d['group'].__setitem__('target_tail_bytes', 2))
    reject('wrong-target-header', lambda d: d['group'].__setitem__('target_header_hex', '4353000100000000'))
    reject('wrong-source-block', lambda d: d.__setitem__('old', bytes([d['old'][0] ^ 1]) + d['old'][1:]))
    reject('wrong-clean-block', lambda d: d.__setitem__('clean', bytes([d['clean'][0] ^ 1]) + d['clean'][1:]))
    reject('record-missing', lambda d: d['rows'].pop())
    reject('record-duplicate', lambda d: d['rows'].__setitem__(1, deepcopy(d['rows'][0])))
    reject('speaker-preamble', lambda d: d['rows'][0].__setitem__('source_complete_preamble_hex', '0040ffff0070'))
    reject('current-body-reference', lambda d: d['rows'][0]['current_reference'].__setitem__('offset', d['rows'][0]['current_reference']['offset'] + 2))
    reject('compiled-final-glyph', lambda d: d['rows'][0].__setitem__('compiled_hex', d['rows'][0]['compiled_hex'][:-2]))
    reject('parity-space', lambda d: d['group']['text_records'][0].__setitem__('parity_space_added', not d['group']['text_records'][0]['parity_space_added']))
    assert len(cases) == 20
    root.mkdir(parents=True)
    save(root / 'independent_reconstruction_validation.json', dict(derivation=result, target_block_sha256=sha(target), entire_research_block_byte_exact=True,
        complete20_commands5_preambles8_relatives2_queries_fullend_tail_andboth_inverse_guards_preserved=True,
        positive_cases=1, negative_count=20, negative_cases=cases, every_negative_actual_input_changed_andguard_rejected=True,
        no_dependency_hash_bypass_file_orROM_mutation_atomic_commit_orcompletion_credit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [packetpath, mappingpath, sourcepath, docpath, Path(__file__), Path('dk4tool/patch/hodram_B51_reconstruction_v1.py')]}))
    print('B51 independent production reconstruction equals the full tested block; twenty changed semantic inputs reject. Eight relatives/two queries/end/tails and both inverses preserved; no ROM commit.')
