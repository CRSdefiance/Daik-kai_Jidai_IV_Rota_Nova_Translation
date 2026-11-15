"""Keep complete three-choice native guards with explicit current captain and source bank."""
from scripts.check_rafael_three_choice_single_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous, {
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n    args=parser.parse_args();assert not args.out.exists()",
    'ctx=RegisteredRuntime(args.release,args.startup,captain=0)':
        'ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)',
    "    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']":
        "    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']\n    assert doc['file_path']==f'/data/SC{args.captain}.DK4'\n    assert all(r['file_path']==doc['file_path'] and all(r[k].get('file_path',doc['file_path'])==doc['file_path'] for k in ['source_reference','current_reference']) for r in rows)",
    "image.read_file(ref['file_path'])":"image.read_file(ref.get('file_path',doc['file_path']))",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-complete-three-index-provider-pixels-canaries-andrejections','exec'),globals())
