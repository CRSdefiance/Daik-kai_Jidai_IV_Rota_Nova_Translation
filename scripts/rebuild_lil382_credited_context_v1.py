"""Use the original batch builder with one explicit relocated credited-context block."""
from scripts import rebuild_reviewed_editorial_batch_v6 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.script.reviewed_credited_context_rebuild_v1 import rebuild_credited_context

source = checked_text(previous.source, {
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--source-context',type=Path,required=True)\n"
        "    parser.add_argument('--ledger',type=Path,required=True)\n"
        '    args=parser.parse_args();assert not args.out.exists()',
    '    digest=sha(args.manuscript.read_bytes())':
        """    assert doc['file_path']=='/data/SC2.DK4' and doc['runtime']['captain']==2
    context_packet=load(args.source_context);ledger=load(args.ledger)
    credited={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    context_group=next(g for g in context_packet['groups'] if g['block']==115)
    digest=sha(args.manuscript.read_bytes())""",
    '        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,compound)':
        """        if block==115:
            assert not compound and len(records)==32
            target,proof=rebuild_credited_context(arm,clean,current,records,compiled,inventory,context_group,credited,
                expected_context_objects=9,expected_context_speeches=4)
        else:
            target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,compound)""",
    "producers={str(p):sha(p.read_bytes()) for p in [Path(__file__),":
        "credited_source_context=str(args.source_context),credited_source_context_sha256=sha(args.source_context.read_bytes()),credit_ledger=str(args.ledger),credit_ledger_sha256=sha(args.ledger.read_bytes()),producers={str(p):sha(p.read_bytes()) for p in [Path(__file__),Path('dk4tool/script/reviewed_credited_context_rebuild_v1.py'),",
})
env = {**previous.env, 'rebuild_credited_context':rebuild_credited_context, '__file__':__file__}
exec(compile(source,__file__+'::same-complete-release-guards-explicit-B115-credited-context-inverse','exec'),env)
if __name__=='__main__':
    env['main']()
