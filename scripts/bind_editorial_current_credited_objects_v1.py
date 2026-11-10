"""Bind selected objects while explicitly preserving exact credited source context."""
from scripts import bind_editorial_current_objects_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    '    args=parser.parse_args();assert not args.out.exists();current,styles,choices=map(load,[args.current,args.styles,args.choices])':
        """    parser.add_argument('--source-packet',type=Path,required=True)
    parser.add_argument('--ledger',type=Path,required=True)
    parser.add_argument('--expected-credited-style-objects',type=int,required=True)
    parser.add_argument('--expected-credited-style-records',type=int,required=True)
    args=parser.parse_args();assert not args.out.exists();current,styles,choices=map(load,[args.current,args.styles,args.choices])
    packet=load(args.source_packet);ledger=load(args.ledger)
    assert packet['file_path']==current['file_path']
    sourcegroups={g['block']:g for g in packet['groups']}
    assert set(sourcegroups)=={g['block'] for g in current['groups']}
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    selected={(r['block'],r['source_command_offset']) for r in styles['records']}
    credited_context=[]
    for group in current['groups']:
        original=sourcegroups[group['block']]
        assert original['clean_block_hex']==group['clean_block_hex']
        assert original['all_source_commands']==group['all_source_commands']
        assert sha(bytes.fromhex(group['clean_block_hex']))==original['clean_block_sha256']
        for mapped in group['command_map']:
            if mapped['word']!=0x4100 or (group['block'],mapped['source_offset']) in selected:continue
            context=[r for r in original['complete_clean_context_records']
                if r['kind']=='physical-style-alternative' and r['source_reference']['command_offset']==mapped['source_offset']]
            assert context and all(r['covered'] for r in context)
            assert not any(r['source_reference']['command_offset']==mapped['source_offset'] and r['kind']=='physical-style-alternative' for r in original['records'])
            cleanblock=bytes.fromhex(original['clean_block_hex'])
            for row in context:
                assert len(row['exact_credited_source_bindings'])==1
                binding=row['exact_credited_source_bindings'][0]
                assert (row['file_path'],binding['id']) in credited
                assert binding['source_hex']==row['source_hex']
                assert binding['block']==row['block'] and binding['offset']==row['source_reference']['offset']
                at=row['source_reference']['offset'];raw=bytes.fromhex(row['source_hex'])
                assert cleanblock[at:at+len(raw)]==raw
            credited_context.append(dict(block=group['block'],source_command_offset=mapped['source_offset'],
                current_command_offset=mapped['current_offset'],source_object_hex=mapped['source_hex'],
                current_object_hex=mapped['current_hex'],source_records=context,
                already_credited_not_newly_reviewed=True))
    assert len(credited_context)==args.expected_credited_style_objects
    assert sum(len(r['source_records']) for r in credited_context)==args.expected_credited_style_records""",
    "            if mapped['word']!=0x4100:continue":
        """            if mapped['word']!=0x4100:continue
            if (block,mapped['source_offset']) not in selected:
                assert sum(r['block']==block and r['source_command_offset']==mapped['source_offset'] for r in credited_context)==1
                continue""",
    "        style_records=style_rows,choice_records=choice_rows,style_objects=objects,choice_objects=choice_objects,native_style_getter_cases=native_cases,":
        """        style_records=style_rows,choice_records=choice_rows,style_objects=objects,choice_objects=choice_objects,native_style_getter_cases=native_cases,
        credited_style_context_preserved_not_newly_reviewed=credited_context,
        exact_credit_ledger=str(args.ledger),exact_credit_ledger_sha256=sha(args.ledger.read_bytes()),
        complete_clean_context_packet=str(args.source_packet),complete_clean_context_packet_sha256=sha(args.source_packet.read_bytes()),""",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-selected-native-guards-plus-exact-credited-context-membership', 'exec'), globals())
