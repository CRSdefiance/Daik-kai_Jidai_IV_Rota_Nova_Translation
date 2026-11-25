"""Retain the native FE diagnostic with explicit captain and exact macro expansions."""
import inspect
from scripts import diagnose_editorial_FE_rows_v1 as previous
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "    p.add_argument('--record',required=True);a=p.parse_args();assert not a.out.exists()":
        "    p.add_argument('--record',required=True);p.add_argument('--captain',type=int,choices=range(4),required=True);p.add_argument('--macro-proof',type=Path,required=True);a=p.parse_args();assert not a.out.exists()",
    'ctx=RegisteredRuntime(a.release,a.startup)':'ctx=RegisteredRuntime(a.release,a.startup,captain=a.captain)',
    "text=encoded[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')":
        "macros=load(a.macro_proof);assert macros['runtime']==ctx.receipt()\n    text=encoded[1:]\n    for token,value in macros['defaults'].items():text=text.replace(token.encode(),value['text'].encode())",
    'a.manuscript,a.plan,a.release,a.startup,Path(__file__)':
        'a.manuscript,a.plan,a.release,a.startup,a.macro_proof,Path(__file__)',
})
env={**vars(previous),'RegisteredRuntime':RegisteredRuntime,'__file__':__file__}
exec(compile(source,__file__+'::same-native-row-andglyph-diagnostic-explicit-runtime','exec'),env)
if __name__=='__main__':env['main']()
