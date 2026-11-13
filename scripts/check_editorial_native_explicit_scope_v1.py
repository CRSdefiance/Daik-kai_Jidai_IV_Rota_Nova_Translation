"""Combine the explicit captain runners with the qualified exact native scope check."""

import sys

from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.source_locked_derivation_v5118 import checked_text


def body():
    from scripts import check_editorial_compiled_pages_explicit_captain_v2 as runner

    source = checked_text(runner.source, {
        "    assert doc['current_ROM_sha256']==sha(ctx.rompath.read_bytes())":
            "    scope_reuse=qualified_current_native_context(doc,ctx)",
        "save(args.out/'native_run_inputs.json',dict(runtime=ctx.receipt(),font_sha256=sha(font),":
            "save(args.out/'native_run_inputs.json',dict(runtime=ctx.receipt(),native_context_reuse=scope_reuse,font_sha256=sha(font),",
        'runtime=ctx.receipt(),font_sha256=sha(font),records=rows,review_sheets=sheets,':
            'runtime=ctx.receipt(),native_context_reuse=scope_reuse,font_sha256=sha(font),records=rows,review_sheets=sheets,',
    })
    env = {**vars(runner.previous), **vars(runner), **globals()}
    exec(compile(source, __file__, 'exec'), env)


def two_choice():
    from scripts import check_editorial_two_choice_explicit_route_v1 as runner

    source = checked_text(runner.source, {
        "    assert doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']":
            "    scope_reuse=qualified_current_native_context(doc,ctx)",
        'runtime=ctx.receipt(),versions=versions,records=planes,':
            'runtime=ctx.receipt(),native_context_reuse=scope_reuse,versions=versions,records=planes,',
    })
    env = {**runner.main.__globals__, **globals(), '__name__': '_qualified_native_menu'}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


def style():
    from scripts import check_editorial_style_objects_explicit_captain_v1 as runner

    source = checked_text(runner.source, {
        "ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain);assert current['runtime']==ctx.receipt() and doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']":
            "ctx=RegisteredRuntime(args.release,args.startup,captain=args.captain)\n"
            "    assert current['runtime']==ctx.receipt() and current['current_ROM_sha256']==doc['current_ROM_sha256']\n"
            "    scope_reuse=qualified_current_native_context(doc,ctx)",
        'runtime=ctx.receipt(),objects=objects,native_target_slot_cases=cases,':
            'runtime=ctx.receipt(),native_context_reuse=scope_reuse,objects=objects,native_target_slot_cases=cases,',
    })
    env = {**runner.main.__globals__, **globals()}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    runners = {'body': body, 'two-choice': two_choice, 'style': style}
    if len(sys.argv) < 2 or sys.argv[1] not in runners:
        raise SystemExit('Expected body, two-choice, or style before the runner arguments.')
    runners[sys.argv.pop(1)]()
