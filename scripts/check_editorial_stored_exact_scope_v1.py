"""Verify rebuilt bytes and native pages with the qualified unchanged runtime."""

from scripts import check_editorial_stored_explicit_captain_v1 as previous
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(previous.source, {
        "    assert ctx.receipt()==runtime and rebuilt['parent_sha256']==runtime['candidate_sha256']":
            """    assert ctx.receipt()==runtime
    path=Path(rebuilt['manuscript'])
    assert sha(path.read_bytes())==rebuilt['manuscript_sha256']==native['manuscript_sha256']
    doc=load(path)
    scope=qualified_current_native_context(doc,ctx)
    assert scope==rebuilt['native_context_reuse']
    assert rebuilt['parent_sha256']==scope['target_candidate_sha256']==sha(Path(rebuilt['parent']).read_bytes())
    assert sha(Path(rebuilt['plan']).read_bytes())==rebuilt['plan_sha256']""",
        '                    rendered=painter(expanded)':
            "                    rendered=painter(expanded)\n"
            "                    rendered['planned_native_row_comparison']=check_FE_rows(expanded,rendered)",
        "        native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=ctx.receipt(),":
            "        native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=ctx.receipt(),native_context_reuse=scope,",
    })
    env = {**vars(previous), **globals(), '__name__': '_stored_exact_scope'}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
