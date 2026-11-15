"""Bind the original inline evidence dictionary; keep the exact transition guard."""
import inspect
from scripts import analyze_maria321_refusal_stable_v1 as original
from scripts.source_locked_derivation_v5118 import checked_text

_source = checked_text(inspect.getsource(original.stable_source), {
    'evidence = {str(p): sha(p.read_bytes()) for p in [':
        'evidence={str(p): sha(p.read_bytes()) for p in [',
})
_env = {**original.stable_source.__globals__, '__file__':__file__}
exec(compile(_source, __file__+'::same-stable-header-guard-correct-inline-evidence-anchor', 'exec'), _env)

if __name__ == '__main__':
    exec(compile(original.previous.source, __file__+'::same-complete-pixels-andtwo-stable-holds-one-bound-transition', 'exec'),
        {**vars(original.previous), **vars(original), '__file__':__file__, '__name__':'__main__', 'maria_source':_env['stable_source']})
