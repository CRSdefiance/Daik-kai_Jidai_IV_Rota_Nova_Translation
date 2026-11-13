"""Rebuild against the registered parent with an exactly qualified native runtime."""

from scripts import rebuild_reviewed_editorial_batch_v6 as previous
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(previous.source, {
        "    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==native['runtime']['candidate_sha256']":
            """    runtime=native['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=runtime['captain'])
    assert ctx.receipt()==runtime
    scope=qualified_current_native_context(doc,ctx)
    assert scope==packet['exact_native_context_reuse']
    assert sha(args.release.read_bytes())==scope['target_release_sha256']
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==scope['target_candidate_sha256']
    image=NdsImage.open(doc['current_ROM'])""",
        "        groups=groups,changed_blocks=changed,": "        native_context_reuse=scope,groups=groups,changed_blocks=changed,",
    })
    env = {**previous.env, **globals()}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
