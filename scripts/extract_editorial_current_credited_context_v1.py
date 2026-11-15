"""Retain full command guards while binding only explicitly uncredited speeches in mixed-context blocks."""
from scripts import extract_editorial_current_v7 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    '    args = ap.parse_args()':
        "    ap.add_argument('--ledger',type=Path,required=True)\n    ap.add_argument('--expected-credited-context-speeches',type=int,required=True)\n    args = ap.parse_args()",
    "    ctx = RegisteredRuntime(args.release,args.startup,captain=args.captain)":
        """    ledger=load(args.ledger)
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    credited_context_speeches=0
    ctx = RegisteredRuntime(args.release,args.startup,captain=args.captain)""",
    "        assert len(commands) == len(original['all_source_commands']) and len(speeches) == len(meaning['records'])":
        """        assert len(commands) == len(original['all_source_commands'])
        full_context=original['complete_clean_context_records']
        full_speech=[r for r in full_context if r['kind']=='ordinary-speech']
        owned=[r for r in full_speech if not r['covered']]
        context=[r for r in full_speech if r['covered']]
        assert len(speeches)==len(full_speech)==len(meaning['records'])+len(context)
        assert [r['id'] for r in owned]==[r['id'] for r in meaning['records']]
        assert all(not r['exact_credited_source_bindings'] and (r['file_path'],r['id']) not in credited for r in owned)
        cleanblock=bytes.fromhex(original['clean_block_hex'])
        for row in context:
            assert len(row['exact_credited_source_bindings'])==1
            binding=row['exact_credited_source_bindings'][0]
            assert (row['file_path'],binding['id']) in credited
            at=row['source_reference']['offset'];raw=bytes.fromhex(row['source_hex'])
            assert cleanblock[at:at+len(raw)]==raw
        source_speeches=[c for c in original['all_source_commands'] if c['word']==0x4000]
        assert [c['offset'] for c in source_speeches]==[r['source_reference']['command_offset'] for r in full_speech]
        assert all(c['word']==0x4000 for c in speeches)
        bysource={c['offset']:now for c,now in zip(source_speeches,speeches,strict=True)}
        selected_speeches=[bysource[r['source_reference']['command_offset']] for r in meaning['records']]
        assert len(selected_speeches)==len(meaning['records'])
        credited_context_speeches+=len(context)""",
    "        for source, command in zip(meaning['records'], speeches, strict=True):":
        "        for source, command in zip(meaning['records'], selected_speeches, strict=True):",
    "    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes":
        "    assert credited_context_speeches==args.expected_credited_context_speeches\n    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes",
    "        original_current_catalogue_lookups=meanings['meanings'], native_macro_expansion_not_executed_here=True,":
        "        original_current_catalogue_lookups=meanings['meanings'],native_macro_expansion_not_executed_here=True,\n        credited_context_speeches_preserved_not_newly_reviewed=credited_context_speeches,exact_current_credit_ledger=str(args.ledger),exact_current_credit_ledger_sha256=sha(args.ledger.read_bytes()),full_source_current_command_count_order_preambles_andunowned_commands_checked=True,",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-whole-command-andnative-lookup-guards-explicit-credited-context-membership', 'exec'), globals())
